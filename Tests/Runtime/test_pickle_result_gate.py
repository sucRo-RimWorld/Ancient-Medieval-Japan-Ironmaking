"""Pure Python result-gate tests (no RimWorld runtime claims)."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[2] / "Scripts/validate_pickle_result.py"
spec = importlib.util.spec_from_file_location("pickle_result_gate", SCRIPT)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class PickleResultGate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.folder = Path(self.tmp.name)
        self.summary = {
            "total": 5, "passed": 5, "failed": 0, "skipped": 0,
            "exitReason": "passed",
            "scenarios": [{"name": name, "outcome": "Passed"}
                          for name in sorted(gate.EXPECTED)]
        }
        self.write()

    def write(self, log="Verse started normally"):
        (self.folder / "summary.json").write_text(json.dumps(self.summary))
        (self.folder / "Player.log").write_text(log)

    def test_passes_only_all_five_named_scenarios(self):
        self.assertEqual(gate.validate(self.folder), 5)

    def test_production_requires_exact_four_bill_scenarios(self):
        self.summary.update(total=4, passed=4, scenarios=[
            {"name": name, "outcome": "Passed"} for name in sorted(gate.PRODUCTION)])
        self.write()
        self.assertEqual(gate.validate(self.folder, "production"), 4)
        with self.assertRaises(ValueError):
            gate.validate(self.folder)
        self.summary["scenarios"][1]["name"] = "Processing Defs and Vanilla or MO result resolve"
        self.write()
        with self.assertRaisesRegex(ValueError, "identity"):
            gate.validate(self.folder, "production")

    def test_no_missing_or_stale_report_is_pass(self):
        (self.folder / "summary.json").unlink()
        with self.assertRaisesRegex(ValueError, "required"):
            gate.validate(self.folder)

    def test_skip_failure_flaky_and_wrong_scenario_are_rejected(self):
        for key, value in [("skipped", 1), ("failed", 1),
                           ("flaky", 1), ("exitReason", "in-progress")]:
            old = self.summary.get(key)
            self.summary[key] = value
            self.write()
            with self.assertRaises(ValueError):
                gate.validate(self.folder)
            if old is None:
                del self.summary[key]
            else:
                self.summary[key] = old
        self.summary["scenarios"][0]["name"] = "Other mod test"
        self.write()
        with self.assertRaisesRegex(ValueError, "identity"):
            gate.validate(self.folder)

    def test_player_log_error_fails_even_if_summary_passed(self):
        self.write("[ERROR] Failed to load XML")
        with self.assertRaisesRegex(ValueError, "ERROR"):
            gate.validate(self.folder)


if __name__ == "__main__":
    unittest.main()
