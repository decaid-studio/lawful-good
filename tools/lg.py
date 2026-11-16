#!/usr/bin/env python3
"""lawful-good tooling.

  python tools/lg.py validate          # schema + reference checks for all catalogs
  python tools/lg.py build             # write dist/lawful-good.json (public content only)
                                       # and the agent skill as dist/lawful-good-skill.zip
  python tools/lg.py build --internal  # also include crosswalks marked "internal"
  python tools/lg.py triage            # walk through the EU AI Act triage interactively (--lang en)

Crosswalks marked "internal" are only bundled with --internal.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = ROOT / "schema"
CATALOG_DIRS = [ROOT / "catalog", ROOT / "crosswalks"]
BASE = "https://github.com/decaid-studio/lawful-good/schema/"


def load_registry() -> tuple[Registry, dict[str, dict]]:
    schemas = {p.stem.replace(".schema", ""): json.loads(p.read_text("utf-8"))
               for p in SCHEMA_DIR.glob("*.schema.json")}
    registry = Registry().with_resources(
        (BASE + f"{name}.schema.json", Resource.from_contents(s)) for name, s in schemas.items()
    )
    return registry, schemas


def iter_files():
    for d in CATALOG_DIRS:
        if d.exists():
            yield from sorted(d.rglob("*.yaml"))


class _Loader(yaml.SafeLoader):
    """SafeLoader that keeps ISO dates as strings (JSON Schema expects strings)."""


_Loader.yaml_implicit_resolvers = {
    k: [(tag, rx) for tag, rx in v if tag != "tag:yaml.org,2002:timestamp"]
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def load(path: Path) -> dict:
    return yaml.load(path.read_text("utf-8"), Loader=_Loader)


def validate() -> int:
    registry, schemas = load_registry()
    errors: list[str] = []
    docs: dict[Path, dict] = {}

    for path in iter_files():
        doc = load(path)
        docs[path] = doc
        kind = doc.get("kind")
        if kind not in schemas:
            errors.append(f"{path.relative_to(ROOT)}: unknown kind {kind!r}")
            continue
        validator = Draft202012Validator(schemas[kind], registry=registry)
        for err in sorted(validator.iter_errors(doc), key=lambda e: list(e.path)):
            loc = "/".join(str(p) for p in err.path) or "<root>"
            errors.append(f"{path.relative_to(ROOT)}: {loc}: {err.message}")

    # --- reference checks ---
    known_ids: set[str] = set()
    for path, doc in docs.items():
        if doc.get("kind") == "framework":
            roles = {r["id"] for r in doc.get("roles", [])}
            for lvl in doc.get("levels", []):
                for role in lvl["approval_roles"]:
                    if role not in roles:
                        errors.append(f"{path.relative_to(ROOT)}: level {lvl['id']} uses unknown role {role!r}")
            ids = [c["id"] for c in doc["controls"]]
            known_ids.update(ids)
            known_ids.add(f"{doc['id']}.levels")
        elif doc.get("kind") == "assessment-catalog":
            ids = [i["id"] for i in doc["items"]]
            gates = {g["id"] for g in doc.get("gates", [])}
            for item in doc["items"]:
                if gates and item["gate"] not in gates:
                    errors.append(f"{path.relative_to(ROOT)}: item {item['id']} uses unknown gate {item['gate']!r}")
            known_ids.update(ids)
        else:
            continue
        dupes = {i for i in ids if ids.count(i) > 1}
        if dupes:
            errors.append(f"{path.relative_to(ROOT)}: duplicate ids {sorted(dupes)}")

    for path, doc in docs.items():
        if doc.get("kind") != "crosswalk":
            continue
        for m in doc["mappings"]:
            for ref in [m["source"], *m["targets"]]:
                internal = ref.startswith("DAG-") or ref.startswith("decaid.") or (len(ref) == 5 and ref[0] == "G")
                if internal and ref not in known_ids:
                    errors.append(f"{path.relative_to(ROOT)}: unknown reference {ref!r}")

    for path, doc in docs.items():
        if doc.get("kind") != "decision-tree":
            continue
        rel = path.relative_to(ROOT)
        nodes = {n["id"]: n for n in doc["nodes"]}
        outcomes = {o["id"]: o for o in doc["outcomes"]}
        flags = {f["id"] for f in doc.get("flags", [])}
        if doc["start"] not in nodes:
            errors.append(f"{rel}: start node {doc['start']!r} not found")
        for f in doc.get("flags", []):
            for link in f.get("links", []):
                if link not in known_ids:
                    errors.append(f"{rel}: flag {f['id']} links unknown id {link!r}")
        rec_ids = [f["id"] for f in doc["record"]["fields"]]
        for must in ("answers", "outcome", "approved-by", "date"):
            if must not in rec_ids:
                errors.append(f"{rel}: record must contain field {must!r}")
        for f in doc["record"]["fields"]:
            for link in f.get("links", []):
                if link not in known_ids:
                    errors.append(f"{rel}: record field {f['id']} links unknown id {link!r}")
        for pc in doc.get("parallel_checks", []):
            for link in pc.get("links", []):
                if link not in known_ids:
                    errors.append(f"{rel}: parallel check links unknown id {link!r}")
        for o in doc["outcomes"]:
            for link in o.get("links", []):
                if not link.startswith("http") and link not in known_ids:
                    errors.append(f"{rel}: outcome {o['id']} links unknown id {link!r}")
        reached = {doc["start"]}
        for n in doc["nodes"]:
            for ans in n["answers"]:
                where = f"{rel}: node {n['id']} answer {ans['id']}"
                if "next" in ans:
                    reached.add(ans["next"])
                    if ans["next"] not in nodes:
                        errors.append(f"{where}: unknown next node {ans['next']!r}")
                if "outcome" in ans and ans["outcome"] not in outcomes:
                    errors.append(f"{where}: unknown outcome {ans['outcome']!r}")
                for fl in ans.get("flags", []):
                    if fl not in flags:
                        errors.append(f"{where}: unknown flag {fl!r}")
                # Safety rule: on critical questions, "unclear" must stop.
                if n.get("critical") and ans["id"] == "unclear":
                    out = outcomes.get(ans.get("outcome", ""))
                    if not out or out["type"] != "stop":
                        errors.append(f"{where}: critical question must stop on 'unclear'")
        for orphan in sorted(set(nodes) - reached):
            errors.append(f"{rel}: node {orphan!r} is never reached")

    for e in errors:
        print(f"ERROR {e}")
    print(f"{len(docs)} files checked, {len(errors)} error(s).")
    return 1 if errors else 0


def build(include_internal: bool) -> int:
    if validate():
        return 1
    allowed = {"public", "internal"} if include_internal else {"public"}
    bundle: dict = {"schema_version": "0.1", "decision_trees": [], "frameworks": [], "assessment_catalogs": [], "crosswalks": []}
    for path in iter_files():
        doc = load(path)
        kind = doc["kind"]
        if kind == "crosswalk":
            if doc["publication_status"] not in allowed:
                print(f"skip  {path.relative_to(ROOT)} ({doc['publication_status']})")
                continue
            bundle["crosswalks"].append(doc)
        elif kind == "framework":
            # Derive which controls are mandatory at each level.
            for lvl in doc.get("levels", []):
                rank = lvl["rank"]
                lvl["mandatory_controls"] = [
                    c["id"] for c in doc["controls"]
                    if rank is not None and c.get("applies_from_level") is not None
                    and rank >= c["applies_from_level"]
                ]
            bundle["frameworks"].append(doc)
        elif kind == "assessment-catalog":
            bundle["assessment_catalogs"].append(doc)
        elif kind == "decision-tree":
            bundle["decision_trees"].append(doc)
        print(f"add   {path.relative_to(ROOT)}")
    out = ROOT / "dist" / "lawful-good.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(bundle, ensure_ascii=False, indent=2, default=str), "utf-8")
    print(f"wrote {out.relative_to(ROOT)}")
    if not include_internal:  # the skill is meant to be shared, so it only ever gets public content
        skill = ROOT / "skill" / "lawful-good"
        (skill / "data").mkdir(exist_ok=True)
        shutil.copyfile(out, skill / "data" / out.name)
        archive = shutil.make_archive(str(out.parent / "lawful-good-skill"), "zip", skill.parent, skill.name)
        print(f"wrote {Path(archive).relative_to(ROOT)}")
    return 0


def triage(lang: str) -> int:
    path = ROOT / "catalog" / "decision-trees" / "eu-ai-act-triage.yaml"
    tree = load(path)
    nodes = {n["id"]: n for n in tree["nodes"]}
    outcomes = {o["id"]: o for o in tree["outcomes"]}
    flag_defs = {f["id"]: f for f in tree.get("flags", [])}
    collected: list[str] = []
    answers: list[tuple[str, str]] = []
    print(tree["title"][lang], "\n")
    print(tree["disclaimer"][lang], "\n")
    node = nodes[tree["start"]]
    while True:
        print(f"[{', '.join(node['refs'])}] {node['question'][lang]}")
        if "help" in node:
            print(f"  ({node['help'][lang]})")
        for i, ans in enumerate(node["answers"], 1):
            print(f"  {i}) {ans['label'][lang]}")
        choice = input("> ").strip()
        if not choice.isdigit() or not 1 <= int(choice) <= len(node["answers"]):
            print("?")
            continue
        ans = node["answers"][int(choice) - 1]
        answers.append((node["id"], ans["id"]))
        collected += [f for f in ans.get("flags", []) if f not in collected]
        print()
        if "outcome" in ans:
            out = outcomes[ans["outcome"]]
            print(f"=> {out['title'][lang]}\n   {out['text'][lang]}")
            if out.get("links"):
                print(f"   -> {', '.join(out['links'])}")
            for fid in collected:
                f = flag_defs[fid]
                extra = f" ({', '.join(f.get('refs', []))})" if f.get("refs") else ""
                since = f" [{f['applies_from']}]" if f.get("applies_from") else ""
                links = f" -> {', '.join(f['links'])}" if f.get("links") else ""
                print(f"   * {f['text'][lang]}{extra}{since}{links}")
            if tree.get("parallel_checks"):
                print("\n" + ("Parallel prüfen:" if lang == "de" else "Check in parallel:"))
                for pc in tree["parallel_checks"]:
                    links = f" -> {', '.join(pc['links'])}" if pc.get("links") else ""
                    print(f"   - {pc['text'][lang]} ({', '.join(pc.get('refs', []))}){links}")
            print_record(tree, lang, answers, ans["outcome"], collected)
            return 0
        node = nodes[ans["next"]]


def print_record(tree: dict, lang: str, answers, outcome: str, flags) -> None:
    """Print a prefilled record (YAML) for the AI register."""
    import datetime
    prefill = {
        "tree-version": f"{tree['id']} {tree['version']} / {tree.get('law_version', '')}",
        "answers": [{"question": q, "answer": a, "justification": ""} for q, a in answers],
        "outcome": outcome,
        "flags": list(flags),
        "date": datetime.date.today().isoformat(),
    }
    rec = {f["id"]: prefill.get(f["id"], "") for f in tree["record"]["fields"]}
    print("\n" + ("Protokoll für das KI-Register (ergänzen, Freigabe durch einen Menschen):"
                  if lang == "de" else "Record for the AI register (complete it; a person approves):"))
    print(yaml.safe_dump(rec, allow_unicode=True, sort_keys=False))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate")
    b = sub.add_parser("build")
    b.add_argument("--internal", action="store_true", help="include crosswalks marked internal")
    t = sub.add_parser("triage")
    t.add_argument("--lang", choices=["de", "en"], default="de")
    args = ap.parse_args()
    if args.cmd == "triage":
        return triage(args.lang)
    return validate() if args.cmd == "validate" else build(args.internal)


if __name__ == "__main__":
    sys.exit(main())
