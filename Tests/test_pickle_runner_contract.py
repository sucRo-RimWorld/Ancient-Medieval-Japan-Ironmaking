"""Pure-Python isolated runner contract tests (not a game execution)."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import sys
import xml.etree.ElementTree as ET

SCRIPT = Path(__file__).resolve().parents[1] / "Scripts/run-pickle-e2e.py"
if str(SCRIPT.parent) not in sys.path:
    sys.path.insert(0, str(SCRIPT.parent))
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

    def test_real_game_jobs_advance_ticks_in_pickle_fast_mode(self):
        root = SCRIPT.parent.parent / "Tests/E2E"
        shared = (root / "IronmakingSteps.cs").read_text(encoding="utf-8")
        self.assertIn("PickleRunMode.Mode.Fast", shared)
        self.assertIn("Find.TickManager.DoSingleTick()", shared)
        self.assertIn("await ctx.WaitFrames(1)", shared)
        self.assertIn("await ctx.WaitTicks(ticks)", shared)  # Watch mode only
        for name in ("IronmakingBillSteps.cs", "IronmakingMiningSteps.cs"):
            source = (root / name).read_text(encoding="utf-8")
            self.assertIn("await IronmakingTestThread.AdvanceTicks(ctx, 240)", source)
            self.assertNotIn("await ctx.WaitTicks(240)", source)

    def test_production_uses_bounded_timeout_and_game_tick_markers(self):
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertIn('parser.add_argument("--timeout", type=int, default=300)', source)
        self.assertIn('"-pickle-run-timeout=4"', source)
        self.assertIn('env["AMJI_PROGRESS_PATH"]', source)
        self.assertIn("timeout=timeout, suite=suite", source)
        steps = (SCRIPT.parent.parent / "Tests/E2E/IronmakingBillSteps.cs").read_text()
        for marker in ('Progress("setup:"', 'Progress("job:"',
                       'Progress("tick:"', 'Progress("completed:"'):
            self.assertIn(marker, steps)

    def test_runner_invokes_heartbeat_monitor_for_each_profile(self):
        runner_text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("for profile_index, profile in enumerate(profiles, 1):",
                      runner_text)
        self.assertIn("run_hidden_with_status(hidden, report=report", runner_text)
        self.assertNotIn("proc = subprocess.run(hidden", runner_text)
        self.assertIn("validate_pickle_result.py", runner_text)
        self.assertIn("diagnostic_tail(report)", runner_text)
        self.assertIn("if code != 0:", runner_text)

    def test_private_desktop_logs_startup_snapshots_before_timeout(self):
        source = module.HIDDEN_LAUNCHER_SOURCE.read_text(encoding="utf-8")
        for token in ("[PRIVATE_DESKTOP_DIAG]", "EnumDesktopWindows",
                      "GetWindowThreadProcessId", "TotalProcessorTime",
                      "WorkingSet64", "ReportStartupSnapshot(desktop, child.pid",
                      "Math.Min(30000L, remaining)"):
            self.assertIn(token, source)
        self.assertIn("visible fallback is forbidden", source)
        self.assertNotIn("-nographics", source)


    def test_diagnostic_entry_is_separate_from_full_e2e(self):
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertIn('parser.add_argument("--diagnose-mo-startup"', source)
        self.assertIn('from diagnose_mo_startup import diagnose', source)
        self.assertIn('diagnose(args.game, args.timeout)', source)
        self.assertIn('run(args.game, args.profile, args.timeout, args.suite)', source)

    def test_profile_xml_preserves_real_settings_and_replaces_mods(self):
        prefs = self.root / "Prefs.xml"
        mods_config = self.root / "ModsConfig.xml"
        prefs_text = "<Prefs><devMode>False</devMode><resetModsConfigOnCrash>True</resetModsConfigOnCrash><uiScale>1.25</uiScale></Prefs>"
        mods_text = ("<ModsConfigData><version>1.6.4871</version>"
                     "<activeMods><li>unrelated.current.mod</li></activeMods>"
                     "<knownExpansions><li>ludeon.rimworld.royalty</li>"
                     "<li>ludeon.rimworld.biotech</li></knownExpansions>"
                     "<customContext>preserve-this</customContext></ModsConfigData>")
        prefs.write_text(prefs_text)
        mods_config.write_text(mods_text)
        for profile in ("Vanilla", "MO"):
            dest = self.root / profile / "Config"
            module.make_config(dest, mods_config, profile, prefs)
            parsed = ET.parse(dest / "ModsConfig.xml").getroot()
            ids = [li.text for li in parsed.findall("activeMods/li")]
            self.assertEqual(ids, [v.lower() for v in
                (module.BASE_IDS + (module.MO_IDS if profile == "MO" else [])
                 + [module.IRON_ID, module.HARNESS_ID])])
            self.assertNotIn("unrelated.current.mod", ids)
            self.assertEqual(parsed.findtext("customContext"), "preserve-this")
            self.assertEqual([x.text for x in parsed.findall("knownExpansions/li")],
                             ["ludeon.rimworld.royalty", "ludeon.rimworld.biotech"])
            pref = ET.parse(dest / "Prefs.xml").getroot()
            self.assertEqual(pref.findtext("devMode"), "True")
            self.assertEqual(pref.findtext("resetModsConfigOnCrash"), "False")
            self.assertEqual(pref.findtext("uiScale"), "1.25")
        self.assertEqual(prefs.read_text(), prefs_text)
        self.assertEqual(mods_config.read_text(), mods_text)

    def test_real_prefs_root_is_preserved_without_assuming_tag_name(self):
        prefs = self.root / "Prefs.xml"
        mods = self.root / "ModsConfig.xml"
        prefs.write_text("<PrefsData><uiScale>1.25</uiScale></PrefsData>")
        mods.write_text("<ModsConfigData><version>1.6.4871</version>"
                        "<activeMods/><knownExpansions/></ModsConfigData>")
        dest = self.root / "UnusualRoot" / "Config"
        module.make_config(dest, mods, "MO", prefs)
        root = ET.parse(dest / "Prefs.xml").getroot()
        self.assertEqual(root.tag, "PrefsData")
        self.assertEqual(root.findtext("uiScale"), "1.25")
        self.assertEqual(root.findtext("devMode"), "True")
        self.assertEqual(root.findtext("resetModsConfigOnCrash"), "False")
        self.assertEqual(ET.parse(prefs).getroot().findtext("devMode"), None)

    def test_invalid_template_fails_closed_without_synthetic_dlc(self):
        prefs = self.root / "Prefs.xml"
        mods = self.root / "ModsConfig.xml"
        prefs.write_text("<Prefs/>")
        mods.write_text("<ModsConfigData><version>1.6.4871</version><activeMods/>"
                        "</ModsConfigData>")
        with self.assertRaisesRegex(ValueError, "knownExpansions"):
            module.make_config(self.root / "Invalid", mods, "MO", prefs)
        self.assertFalse((self.root / "Invalid").exists())

if __name__ == "__main__":
    unittest.main()
