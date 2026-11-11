#!/usr/bin/env python3
"""lawful-good skill: read the rulebook without loading it whole.

  python scripts/lawful_good.py triage [node=answer ...]
  python scripts/lawful_good.py levels
  python scripts/lawful_good.py controls <level-id>
  python scripts/lawful_good.py gate <gate-id> [--module <module-id> ...]
  python scripts/lawful_good.py triggers

Every command prints JSON in one language (--lang de|en, default de) and
carries the disclaimer. Standard library only, so it runs in any agent sandbox.

Safe to hand to other agents by construction: it reads one fixed file
(data/lawful-good.json, written by `tools/lg.py build`), writes nothing, opens
no network connection, starts no process, and takes only ids as arguments.
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "lawful-good.json"
ID = re.compile(r"[a-z0-9-]+", re.IGNORECASE)

# Wording follows NOTICE.md. Attached to every output so no report can leave without it.
DISCLAIMER = {
    "de": "Keine Rechtsberatung. Das Ergebnis beruht auf Governance-Empfehlungen von DECAID und weist "
          "keine Konformität mit dem EU AI Act oder anderen Gesetzen und Normen nach.",
    "en": "Not legal advice. The result is based on DECAID's governance recommendations and does not "
          "establish conformity with the EU AI Act or any other law or standard.",
}


class UsageError(Exception):
    """The caller asked for something the data does not contain."""


def localise(value, lang: str):
    """Collapse every {de, en} text in a nested structure to the one language."""
    if isinstance(value, dict):
        if value and set(value) <= {"de", "en"}:
            return value.get(lang, value.get("de"))
        return {k: localise(v, lang) for k, v in value.items()}
    if isinstance(value, list):
        return [localise(v, lang) for v in value]
    return value


def notices(doc: dict, lang: str) -> list[str]:
    """What the agent must flag about this document's review status (see AGENTS.md)."""
    out = []
    status = doc.get("verification", {}).get("status")
    if status == "unverified":
        out.append(f"{doc['id']}: verification.status = unverified")
    if lang == "en" and doc.get("translation_status") == "machine-assisted-review-needed":
        out.append(f"{doc['id']}: translation_status = machine-assisted-review-needed")
    return out


def by_id(entries: list[dict], wanted: str, what: str) -> dict:
    for entry in entries:
        if entry["id"] == wanted:
            return entry
    raise UsageError(f"unknown {what} {wanted!r}; known: {', '.join(e['id'] for e in entries)}")


def triage(tree: dict, given: list[tuple[str, str]], lang: str) -> dict:
    """Walk the decision tree with the answers given so far.

    given: (node id, answer id) in any order.
    Returns the next open question, or the outcome with flags, parallel checks
    and the prefilled register record. Raises UsageError for an answer that is
    unknown or not on the path, so no question can be skipped or pre-empted.
    """
    nodes = {n["id"]: n for n in tree["nodes"]}
    pending = {}
    for node_id, answer_id in given:
        if node_id in pending:
            raise UsageError(f"question {node_id!r} answered twice")
        pending[node_id] = answer_id

    flags: list[str] = []
    answered: list[dict] = []
    node = nodes[tree["start"]]
    while True:
        if node["id"] not in pending:
            if pending:
                raise UsageError(
                    f"answers given for {sorted(pending)}, but the next open question is {node['id']!r}"
                )
            return {
                "status": "question",
                "node": node["id"],
                "critical": bool(node.get("critical")),
                "refs": node["refs"],
                "question": localise(node["question"], lang),
                "help": localise(node.get("help"), lang),
                "answers": [{"id": a["id"], "label": localise(a["label"], lang)} for a in node["answers"]],
                "answered": answered,
            }
        answer_id = pending.pop(node["id"])
        answer = by_id(node["answers"], answer_id, f"answer to {node['id']!r}")
        # The justification is written by the caller into the report, never passed through the shell.
        answered.append({"question": node["id"], "answer": answer_id, "justification": ""})
        flags += [f for f in answer.get("flags", []) if f not in flags]
        if "outcome" in answer:
            break
        node = nodes[answer["next"]]

    if pending:
        raise UsageError(f"the tree ended at {node['id']!r}; answers for {sorted(pending)} are not on the path")
    prefill = {
        "tree-version": f"{tree['id']} {tree['version']} / {tree.get('law_version', '')}",
        "answers": answered,
        "outcome": answer["outcome"],
        "flags": flags,
        "date": datetime.date.today().isoformat(),
    }
    return {
        "status": "outcome",
        "outcome": localise(by_id(tree["outcomes"], answer["outcome"], "outcome"), lang),
        "flags": [localise(by_id(tree.get("flags", []), f, "flag"), lang) for f in flags],
        "parallel_checks": localise(tree.get("parallel_checks", []), lang),
        # approved-by stays empty on purpose: a person approves the classification.
        "record": {f["id"]: prefill.get(f["id"], "") for f in tree["record"]["fields"]},
        "notices": notices(tree, lang),
    }


def levels(framework: dict, lang: str) -> dict:
    """List the clearance levels with the capabilities that define them."""
    keys = ("id", "rank", "name", "description", "capabilities", "approval_roles", "allowed")
    return {
        "levels": [localise({k: lvl[k] for k in keys}, lang) for lvl in framework["levels"]],
        "notices": notices(framework, lang),
    }


def controls(framework: dict, level_id: str, lang: str) -> dict:
    """Return the mandatory controls of one level with their assessment questions."""
    level = by_id(framework["levels"], level_id, "level")
    keys = ("id", "title", "statement", "parameters", "assessment_questions")
    mandatory = [c for c in framework["controls"] if c["id"] in level["mandatory_controls"]]
    return {
        "level": level["id"],
        "allowed": level["allowed"],
        "approval_roles": level["approval_roles"],
        "controls": [localise({k: c[k] for k in keys if k in c}, lang) for c in mandatory],
        "notices": notices(framework, lang),
    }


def gate(catalog: dict, crosswalks: list[dict], gate_id: str, modules: list[str], lang: str) -> dict:
    """Return the check items of one gate.

    Module items are left out unless the module is named; the modules that
    exist are listed with their applies_if so the caller can decide.
    """
    for module in modules:
        by_id(catalog.get("modules", []), module, "module")
    supports: dict[str, list[str]] = {}
    for crosswalk in crosswalks:
        for mapping in crosswalk["mappings"]:
            supports.setdefault(mapping["source"], []).extend(mapping["targets"])
    items = [
        {**item, "supports_controls": supports.get(item["id"], [])}
        for item in catalog["items"]
        if item["gate"] == gate_id and item.get("module") in (None, *modules)
    ]
    return {
        "gate": localise(by_id(catalog["gates"], gate_id, "gate"), lang),
        "principles": localise(catalog.get("principles", []), lang),
        "items": localise(items, lang),
        "modules_available": [
            {"id": m["id"], "applies_if": localise(m["applies_if"], lang)} for m in catalog.get("modules", [])
        ],
        "notices": notices(catalog, lang),
    }


def triggers(catalog: dict, lang: str) -> dict:
    """List the reassessment triggers of every check item."""
    return {
        "triggers": [
            {
                "item": item["id"],
                "module": item.get("module"),
                "question": localise(item["question"], lang),
                "reassessment_triggers": localise(item.get("reassessment_triggers", []), lang),
            }
            for item in catalog["items"]
        ],
        "notices": notices(catalog, lang),
    }


def an_id(text: str) -> str:
    """Arguments are ids from the data, never free text."""
    if not ID.fullmatch(text):
        raise argparse.ArgumentTypeError("expected an id made of letters, digits and hyphens")
    return text


def parse_answer(text: str) -> tuple[str, str]:
    node, _, answer = text.partition("=")
    return an_id(node), an_id(answer)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lang", choices=["de", "en"], default="de")
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("triage")
    t.add_argument("answers", nargs="*", type=parse_answer, metavar="node=answer")
    sub.add_parser("levels")
    sub.add_parser("controls").add_argument("level", type=an_id)
    g = sub.add_parser("gate")
    g.add_argument("gate", type=an_id)
    g.add_argument("--module", action="append", default=[], type=an_id)
    sub.add_parser("triggers")
    args = ap.parse_args(argv)

    try:
        bundle = json.loads(DATA.read_text("utf-8"))
    except FileNotFoundError:
        print(f"{DATA} not found; build it with `python tools/lg.py build`", file=sys.stderr)
        return 2
    tree = bundle["decision_trees"][0]
    framework = bundle["frameworks"][0]
    catalog = bundle["assessment_catalogs"][0]
    try:
        if args.cmd == "triage":
            result = triage(tree, args.answers, args.lang)
        elif args.cmd == "levels":
            result = levels(framework, args.lang)
        elif args.cmd == "controls":
            result = controls(framework, args.level, args.lang)
        elif args.cmd == "gate":
            result = gate(catalog, bundle["crosswalks"], args.gate, args.module, args.lang)
        else:
            result = triggers(catalog, args.lang)
    except UsageError as err:
        print(f"ERROR {err}", file=sys.stderr)
        return 2
    result["disclaimer"] = DISCLAIMER[args.lang]
    print(json.dumps(result, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
