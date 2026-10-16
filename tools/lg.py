#!/usr/bin/env python3
"""lawful-good tooling.

  python tools/lg.py validate          # schema + reference checks for all catalogs
  python tools/lg.py build             # write dist/lawful-good.json (public content only)
  python tools/lg.py build --internal  # also include crosswalks marked "internal"

Files with publication_status "blocked-pending-legal-review" are never bundled.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = ROOT / "schema"
CATALOG_DIRS = [ROOT / "catalog", ROOT / "crosswalks", ROOT / "drafts"]
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
    req_ids, control_ids, level_ids = set(), set(), set()
    for path, doc in docs.items():
        if doc.get("kind") == "regulation":
            ids = [r["id"] for r in doc["requirements"]]
            dupes = {i for i in ids if ids.count(i) > 1}
            if dupes:
                errors.append(f"{path.relative_to(ROOT)}: duplicate requirement ids {sorted(dupes)}")
            req_ids.update(ids)
        if doc.get("kind") == "framework":
            roles = {r["id"] for r in doc.get("roles", [])}
            for lvl in doc.get("levels", []):
                level_ids.add(lvl["id"])
                for role in lvl["approval_roles"]:
                    if role not in roles:
                        errors.append(f"{path.relative_to(ROOT)}: level {lvl['id']} uses unknown role {role!r}")
            ids = [c["id"] for c in doc["controls"]]
            dupes = {i for i in ids if ids.count(i) > 1}
            if dupes:
                errors.append(f"{path.relative_to(ROOT)}: duplicate control ids {sorted(dupes)}")
            control_ids.update(ids)
            control_ids.add(f"{doc['id']}.levels")

    for path, doc in docs.items():
        if doc.get("kind") != "crosswalk":
            continue
        for m in doc["mappings"]:
            refs = [m["source"], *m["targets"]]
            for ref in refs:
                base = ref.split("@")[0]
                # Only refs into catalogs we hold are checked; other articles are external refs.
                if base.startswith("eu-ai-act.art-17") and base not in req_ids:
                    errors.append(f"{path.relative_to(ROOT)}: unknown requirement {ref!r}")
                if base.startswith("DAG-") and base not in control_ids:
                    errors.append(f"{path.relative_to(ROOT)}: unknown control {ref!r}")
        if doc["publication_status"] == "blocked-pending-legal-review" and "drafts" not in path.parts:
            errors.append(f"{path.relative_to(ROOT)}: blocked content must live in drafts/")

    for e in errors:
        print(f"ERROR {e}")
    print(f"{len(docs)} files checked, {len(errors)} error(s).")
    return 1 if errors else 0


def build(include_internal: bool) -> int:
    if validate():
        return 1
    allowed = {"public", "internal"} if include_internal else {"public"}
    bundle: dict = {"schema_version": "0.1", "regulations": [], "frameworks": [], "crosswalks": []}
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
        elif kind == "regulation":
            bundle["regulations"].append(doc)
        print(f"add   {path.relative_to(ROOT)}")
    out = ROOT / "dist" / "lawful-good.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(bundle, ensure_ascii=False, indent=2, default=str), "utf-8")
    print(f"wrote {out.relative_to(ROOT)}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate")
    b = sub.add_parser("build")
    b.add_argument("--internal", action="store_true", help="include crosswalks marked internal")
    args = ap.parse_args()
    return validate() if args.cmd == "validate" else build(args.internal)


if __name__ == "__main__":
    sys.exit(main())
