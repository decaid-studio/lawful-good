"""Checks for the skill script. Run after `python tools/lg.py build`:

  python -m unittest discover tests
"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.dont_write_bytecode = True  # keep __pycache__ out of the skill folder that gets zipped
sys.path.insert(0, str(ROOT / "skill" / "lawful-good" / "scripts"))
import lawful_good as lg  # noqa: E402

BUNDLE = json.loads((ROOT / "dist" / "lawful-good.json").read_text("utf-8"))
TREE = BUNDLE["decision_trees"][0]
FRAMEWORK = BUNDLE["frameworks"][0]
CATALOG = BUNDLE["assessment_catalogs"][0]
CRITICAL = {n["id"] for n in TREE["nodes"] if n.get("critical")}


def all_paths(given=()):
    """Every complete path through the tree, found by asking the walker itself."""
    step = lg.triage(TREE, list(given), "de")
    if step["status"] == "outcome":
        yield given, step
        return
    for answer in step["answers"]:
        yield from all_paths((*given, (step["node"], answer["id"], "")))


class Triage(unittest.TestCase):
    def test_starts_with_the_start_node(self):
        self.assertEqual(lg.triage(TREE, [], "de")["node"], TREE["start"])

    def test_every_path_ends_and_unclear_on_critical_stops(self):
        paths = list(all_paths())
        self.assertTrue(any(step["outcome"]["type"] == "continue" for _, step in paths))
        for given, step in paths:
            record = step["record"]
            self.assertEqual(record["approved-by"], "", "a person approves, never the script")
            self.assertEqual(len(record["answers"]), len(given))
            if any(node in CRITICAL and answer == "unclear" for node, answer, _ in given):
                self.assertEqual(step["outcome"]["type"], "stop", given)

    def test_questions_cannot_be_skipped_or_invented(self):
        later = next(n["id"] for n in TREE["nodes"] if n["id"] != TREE["start"])
        for bad in ([(later, "yes", "")], [(TREE["start"], "maybe", "")],
                    [(TREE["start"], "unclear", ""), (later, "yes", "")]):
            with self.assertRaises(lg.UsageError):
                lg.triage(TREE, bad, "de")

    def test_unverified_tree_is_flagged(self):
        _, step = next(all_paths())
        self.assertEqual(bool(step["notices"]), TREE["verification"]["status"] == "unverified")


class Catalog(unittest.TestCase):
    def test_gates_cover_every_item_once(self):
        modules = [m["id"] for m in CATALOG.get("modules", [])]
        seen = [i["id"] for g in CATALOG["gates"]
                for i in lg.gate(CATALOG, BUNDLE["crosswalks"], g["id"], modules, "de")["items"]]
        self.assertEqual(sorted(seen), sorted(i["id"] for i in CATALOG["items"]))

    def test_module_items_need_the_module(self):
        plain = [i for g in CATALOG["gates"]
                 for i in lg.gate(CATALOG, BUNDLE["crosswalks"], g["id"], [], "de")["items"]]
        self.assertFalse(any(i.get("module") for i in plain))

    def test_one_language_only(self):
        text = json.dumps(lg.gate(CATALOG, BUNDLE["crosswalks"], CATALOG["gates"][0]["id"], [], "en"))
        self.assertNotIn('"de":', text)


class Framework(unittest.TestCase):
    def test_controls_follow_the_level(self):
        for level in FRAMEWORK["levels"]:
            got = lg.controls(FRAMEWORK, level["id"], "de")
            self.assertEqual([c["id"] for c in got["controls"]], level["mandatory_controls"])
            self.assertEqual(got["allowed"], level["allowed"])

    def test_unknown_level(self):
        with self.assertRaises(lg.UsageError):
            lg.controls(FRAMEWORK, "level-99", "de")


if __name__ == "__main__":
    unittest.main()
