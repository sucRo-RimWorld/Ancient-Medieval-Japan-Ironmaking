"""Offline watchdog regressions; these do not run RimWorld."""
from contextlib import redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "Scripts/pickle_run_monitor.py"
spec = importlib.util.spec_from_file_location("pickle_run_monitor", SCRIPT)
monitor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(monitor)


class RuntimeMonitorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_success_reaches_report_validation_caller(self):
        output = io.StringIO()
        command = [sys.executable, "-c", "print('hidden-game-exit')"]
        with redirect_stdout(output):
            result = monitor.run_hidden_with_status(
                command, report=self.root, game=self.root, env=None,
                profile="MO", timeout=4, heartbeat=0.04, poll_seconds=0.01)
        self.assertEqual(result, 0)
        self.assertIn("Starting private-desktop RimWorld", output.getvalue())
        self.assertIn("Controller exited code=0", output.getvalue())
        self.assertIn("hidden-game-exit", (self.root / "launcher.log").read_text())

    def test_nonzero_return_is_not_disguised(self):
        command = [sys.executable, "-c", "raise SystemExit(17)"]
        with redirect_stdout(io.StringIO()):
            result = monitor.run_hidden_with_status(
                command, report=self.root, game=self.root, env=None,
                profile="MO", timeout=4, poll_seconds=0.01)
        self.assertEqual(result, 17)

    def test_timeout_kills_only_own_child_and_fails(self):
        command = [sys.executable, "-c", "import time; time.sleep(100)"]
        original = monitor.time.monotonic
        counter = [0]
        def fast_clock():
            counter[0] += 1
            return original() + counter[0] * 20
        monitor.time.monotonic = fast_clock
        try:
            with self.assertRaisesRegex(TimeoutError, "owned game/process tree"):
                with redirect_stdout(io.StringIO()):
                    monitor.run_hidden_with_status(
                        command, report=self.root, game=self.root, env=None,
                        profile="MO", timeout=1, heartbeat=1, poll_seconds=0.01)
        finally:
            monitor.time.monotonic = original

    def test_failed_startup_diagnostic_reads_both_logs_without_claiming_pass(self):
        (self.root / "launcher.log").write_text(
            "[PRIVATE_DESKTOP] pid=100\n[PRIVATE_DESKTOP_DIAG] cpu=0.1\n"
            "[PRIVATE_DESKTOP_FAIL] timeout\n")
        (self.root / "Player.log").write_text(
            "RimWorld 1.6\nFallback handler could not load library\n")
        detail = monitor.diagnostic_tail(self.root)
        self.assertIn("[PRIVATE_DESKTOP_FAIL]", detail)
        self.assertIn("Fallback handler", detail)
        self.assertIn("Pickle summary: absent", detail)
        self.assertNotIn("PASS", detail)

    def test_log_status_never_claims_pass(self):
        self.assertIn("Player.log absent", monitor._status(self.root))
        (self.root / "Player.log").write_text("loading")
        (self.root / "summary.json").write_text("partial")
        message = monitor._status(self.root)
        self.assertIn("Player.log=7 bytes", message)
        self.assertIn("not yet validated", message)

    def test_pickle_watchdog_timeout_fails_fast(self):
        (self.root / "summary.json").write_text(json.dumps({
            "total": 1, "passed": 1, "failed": 0,
            "exitReason": "watchdog-timeout"}))
        command = [sys.executable, "-c", "import time; time.sleep(30)"]
        with self.assertRaisesRegex(RuntimeError, "Pickle reported watchdog-timeout"):
            with redirect_stdout(io.StringIO()):
                monitor.run_hidden_with_status(
                    command, report=self.root, game=self.root, env=None,
                    profile="Vanilla", timeout=300, suite="production",
                    heartbeat=0.01, poll_seconds=0.01)

    def test_production_idle_without_game_milestones_is_bounded(self):
        command = [sys.executable, "-c", "import time; time.sleep(30)"]
        with self.assertRaisesRegex(RuntimeError, "no verified scenario/tick progress"):
            with redirect_stdout(io.StringIO()):
                monitor.run_hidden_with_status(
                    command, report=self.root, game=self.root, env=None,
                    profile="Vanilla", timeout=3, suite="production",
                    startup_timeout=0.15, idle_timeout=0.1,
                    heartbeat=0.02, poll_seconds=0.01)

    def test_real_step_milestones_prevent_false_idle_failure(self):
        progress = self.root / "step-progress.txt"
        command = [sys.executable, "-c",
                   ("import pathlib,time; p=pathlib.Path(" + repr(str(progress)) +
                    "); [(p.write_text('tick:'+str(i)),time.sleep(0.1))"
                    " for i in range(10)]")]
        with redirect_stdout(io.StringIO()):
            result = monitor.run_hidden_with_status(
                command, report=self.root, game=self.root, env=None,
                profile="Vanilla", timeout=4, suite="production",
                startup_timeout=1.5, idle_timeout=0.6,
                heartbeat=0.04, poll_seconds=0.01)
        self.assertEqual(result, 0)


if __name__ == "__main__":
    unittest.main()
