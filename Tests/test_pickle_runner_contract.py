"""Pure-Python isolated runner contract tests (not a game execution)."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

SCRIPT = Path(__file__).resolve().parents[1] / "Scripts/run-pickle-e2e.py"
spec = importlib.util.spec_from_file_location("ironmaking_runner", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class IsolatedLauncherContracts(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.base = self.root / "From"
        about = self.base / "About"
        about.mkdir(parents=True)
        (about / "About.xml").write_text(
            "<ModMetaData><packageId>" + module.HARNESS_ID +
            "</packageId></ModMetaData>", encoding="utf-8")

    def test_stage_and_cleanup_are_owned_only(self):
        staged = module.stage(self.root, "Harness", module.HARNESS_ID, self.base)
        self.assertEqual(module.mod_id(staged), module.HARNESS_ID)
        module.cleanup(staged, module.HARNESS_ID)
        self.assertFalse(staged.exists())

    def test_unsafe_cleanup_is_refused(self):
        other = self.root / "HumanOwned"
        other.mkdir()
        with self.assertRaisesRegex(RuntimeError, "Unsafe cleanup"):
            module.cleanup(other, module.HARNESS_ID)
        self.assertTrue(other.is_dir())

    def test_empty_or_foreign_source_cannot_be_staged(self):
        foreign = self.root / "Foreign"
        (foreign / "About").mkdir(parents=True)
        (foreign / "About/About.xml").write_text(
            "<ModMetaData><packageId>some.other.mod</packageId></ModMetaData>")
        with self.assertRaisesRegex(RuntimeError, "unexpected packageId"):
            module.stage(self.root, "Foreign", module.HARNESS_ID, foreign)
        self.assertEqual(len(list(self.root.glob("AMJI-Pickle-Foreign-*"))), 0)

    def test_real_game_launch_uses_only_private_desktop(self):
        launcher = self.root / "FakePrivateDesktop.exe"
        game = self.root / "RimWorld"
        exe = game / "RimWorldWin64.exe"
        command = [exe, "-savedatafolder=private", "-logFile", "private.log"]
        got = module.private_desktop_command(launcher, game, 900, command)
        self.assertEqual(got[0], str(launcher))
        self.assertEqual(got[1], str(exe))
        self.assertEqual(got[2], str(game))
        self.assertEqual(got[3], "900")
        self.assertEqual(got[4:], list(map(str, command[1:])))
        self.assertNotIn("-nographics", got)
        with self.assertRaisesRegex(RuntimeError, "Unexpected"):
            module.private_desktop_command(launcher, game, 900,
                                           [self.root / "OtherGame.exe"])
        with self.assertRaisesRegex(RuntimeError, "timeout"):
            module.private_desktop_command(launcher, game, 0, command)

    def test_private_desktop_source_refuses_visible_fallback(self):
        source = module.HIDDEN_LAUNCHER_SOURCE.read_text(encoding="utf-8")
        for token in ("CreateDesktop", 'startup.desktop = "WinSta0', "CreateProcess",
                      "WaitForSingleObject", "TerminateProcess",
                      "visible fallback is forbidden"):
            self.assertIn(token, source)
        self.assertNotIn("-nographics", source)

    def test_runner_invokes_heartbeat_monitor_for_each_profile(self):
        runner_text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("for profile_index, profile in enumerate(profiles, 1):",
                      runner_text)
        self.assertIn("run_hidden_with_status(hidden, report=report", runner_text)
        self.assertNotIn("proc = subprocess.run(hidden", runner_text)
        self.assertIn("validate_pickle_result.py", runner_text)

    def test_profile_xml_is_isolated_and_exact(self):
        prefs = self.root / "Prefs.xml"
        prefs.write_text("<Prefs><devMode>False</devMode></Prefs>")
        for profile in ("Vanilla", "MO"):
            dest = self.root / profile / "Config"
            module.make_config(dest, "1.6.123", profile, prefs)
            mods = [li.text for li in ET.parse(dest / "ModsConfig.xml")
                    .getroot().findall("activeMods/li")]
            self.assertIn(module.IRON_ID, mods)
            self.assertIn(module.HARNESS_ID, mods)
            self.assertEqual("DankPyon.Medieval.Overhaul" in mods, profile == "MO")
            self.assertEqual(ET.parse(dest / "Prefs.xml").getroot().findtext("devMode"), "True")
        self.assertEqual(ET.parse(prefs).getroot().findtext("devMode"), "False")

if __name__ == "__main__":
    unittest.main()
