"""Offline contracts for the isolated, non-Pickle MO startup matrix."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

SCRIPT = Path(__file__).resolve().parents[1] / "Scripts/diagnose_mo_startup.py"
SPEC = importlib.util.spec_from_file_location("amji_mo_startup", SCRIPT)
diag = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(diag)


class MOStartupDifferentialFixtures(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_baseline_and_pickle_differ_only_by_pickling_tools(self):
        self.assertEqual(diag.PROFILES, ("MO-Baseline", "MO-Pickle"))
        baseline = diag.active_mods("MO-Baseline")
        extended = diag.active_mods("MO-Pickle")
        self.assertEqual(extended[:len(baseline)], baseline)
        self.assertEqual(extended[len(baseline):], list(diag.PICKLE_TOOLS))
        for forbidden in ("sucro.ancientmedievaljapan.ironmaking",
                          "sucro.ancientmedievaljapan.ironmaking.e2e"):
            self.assertNotIn(forbidden, extended)
        with self.assertRaises(ValueError):
            diag.active_mods("Vanilla")

    def test_only_new_save_data_is_written(self):
        prefs = self.root / "Prefs.xml"
        initial = "<Prefs><devMode>False</devMode></Prefs>"
        prefs.write_text(initial, encoding="utf-8")
        for profile in diag.PROFILES:
            directory = self.root / profile / "Config"
            diag.config_for_observation(directory, prefs, "1.6.4871", profile)
            found = ET.parse(directory / "ModsConfig.xml").getroot()
            self.assertEqual(found.findtext("version"), "1.6.4871")
            mods = [x.text for x in found.findall("activeMods/li")]
            self.assertEqual(mods, diag.active_mods(profile))
            self.assertEqual(
                ET.parse(directory / "Prefs.xml").getroot().findtext("devMode"), "True")
            with self.assertRaises(FileExistsError):
                diag.config_for_observation(directory, prefs, "1.6.4871", profile)
        self.assertEqual(prefs.read_text(encoding="utf-8"), initial)

    def test_observation_recognizes_cpu_window_snapshot_and_timeout(self):
        report = self.root / "Reports"
        report.mkdir()
        (report / "launcher.log").write_text(
            "[PRIVATE_DESKTOP] RimWorld pid=11292\n"
            "[PRIVATE_DESKTOP_DIAG] elapsed=30s,pid=11292,"
            "cpu=75.2s,ram=628MiB,windows=UnityWndClass:RimWorld\n"
            "[PRIVATE_DESKTOP_FAIL] System.TimeoutException: "
            "RimWorld Pickle exceeded hidden desktop timeout 180s\n")
        (report / "Player.log").write_text(
            "RimWorld 1.6.4871 rev591\nDirect3D 11.0\n"
            "Fallback handler could not load library\n")
        observed = diag.observe_log(report)
        self.assertTrue(observed["native_timeout"])
        self.assertEqual(observed["diagnostic_snapshot_count"], 1)
        self.assertEqual(observed["last_snapshot"]["cpu_seconds"], 75.2)
        self.assertEqual(observed["last_snapshot"]["ram_mib"], 628)
        self.assertTrue(observed["rimworld_version_logged"])
        self.assertFalse(observed["pickle_scenarios_verified"])
        self.assertFalse(observed["pickle_feature_requested"])
        self.assertEqual(len(observed["last_player_lines"]), 3)
        self.assertEqual(observed["kind"], "STARTUP_OBSERVATION_ONLY")

    def test_missing_logs_never_imply_game_started_or_pickle_passed(self):
        empty = diag.observe_log(self.root)
        self.assertFalse(empty["rimworld_version_logged"])
        self.assertEqual(empty["diagnostic_snapshot_count"], 0)
        self.assertEqual(empty["player_log_bytes"], 0)
        self.assertIsNone(empty["last_snapshot"])
        self.assertFalse(empty["pickle_scenarios_verified"])

    def test_no_picklerun_flag_and_strict_hidden_desktop_reuse(self):
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("runner.private_desktop_command(", source)
        self.assertIn("runner.build_private_desktop_launcher()", source)
        self.assertIn("run_hidden_with_status(", source)
        self.assertIn("diagnostic_only=True", source)
        self.assertIn('result["classification"]', source)
        self.assertIn("DIAGNOSTIC_ONLY", source)
        self.assertNotIn('-pickle-run=', source)
        self.assertNotIn("-nographics", source)
        self.assertNotIn("shutil.rmtree(", source)

if __name__ == "__main__":
    unittest.main()
