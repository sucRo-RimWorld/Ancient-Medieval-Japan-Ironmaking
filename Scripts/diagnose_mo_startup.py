#!/usr/bin/env python3
"""MO startup differential: MO dependencies alone versus MO + Pickle tools.

All runs use the existing private WinSta0 desktop launcher and separate
SaveData. They deliberately omit -pickle-run and Ironmaking: these are
time-bounded startup observations, never Pickle gameplay passes.
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import uuid
import xml.etree.ElementTree as ET
from isolated_rimworld_config import write_isolated_config

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
RUNNER_PATH = HERE / "run-pickle-e2e.py"
MO_BASE = (
    "brrainz.harmony",
    "ludeon.rimworld",
    "OskarPotocki.VanillaFactionsExpanded.Core",
    "syrchalis.processor.framework",
    "DankPyon.Medieval.Overhaul",
)
PICKLE_TOOLS = ("RimWorks.RimLogging", "rimworks.pickle", "rimworks.quickstarts")
PROFILES = ("MO-Baseline", "MO-Pickle")
TIMEOUT_MIN = 30
TIMEOUT_MAX = 3600


def active_mods(profile):
    if profile not in PROFILES:
        raise ValueError("Unknown diagnostic profile: " + str(profile))
    return list(MO_BASE + (PICKLE_TOOLS if profile == "MO-Pickle" else ()))


def config_for_observation(path, normal_mods, normal_prefs, profile):
    """Reuse the Environment-proven, DLC-preserving isolated ModConfig writer."""
    write_isolated_config(path, normal_mods, normal_prefs, active_mods(profile))


def observe_log(report):
    """Use startup signals only. No signal here is a Def/Game/Pickle PASS."""
    player = Path(report) / "Player.log"
    launcher = Path(report) / "launcher.log"
    def content(p):
        if not p.is_file():
            return ""
        return p.read_text(encoding="utf-8-sig", errors="replace")
    game_text = content(player)
    launcher_text = content(launcher)
    captures = re.findall(
        r"\[PRIVATE_DESKTOP_DIAG\] elapsed=(\d+)s,pid=(\d+),cpu=([\d.]+)s,"
        r"ram=(\d+)MiB,windows=(.*)", launcher_text)
    timeout = ("RimWorld Pickle exceeded hidden desktop timeout" in launcher_text)
    return {
        "kind": "STARTUP_OBSERVATION_ONLY",
        "rimworld_version_logged": bool(re.search(r"(?m)^RimWorld 1\.6\.", game_text)),
        "direct3d_logged": "Direct3D 11.0" in game_text,
        "pickle_scenarios_verified": False,
        "pickle_feature_requested": False,
        "player_log_bytes": player.stat().st_size if player.is_file() else 0,
        "launcher_log_bytes": launcher.stat().st_size if launcher.is_file() else 0,
        "native_timeout": timeout,
        "diagnostic_snapshot_count": len(captures),
        "last_snapshot": {
            "elapsed_seconds": int(captures[-1][0]),
            "pid": int(captures[-1][1]),
            "cpu_seconds": float(captures[-1][2]),
            "ram_mib": int(captures[-1][3]),
            "windows": captures[-1][4][:350],
        } if captures else None,
        "last_player_lines": game_text.splitlines()[-5:],
        "last_launcher_lines": launcher_text.splitlines()[-3:],
    }


def _runner_module():
    # Reuse the exact shipped launch/safety code, not a second Windows launcher.
    spec = importlib.util.spec_from_file_location("amji_e2e_runner", RUNNER_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def diagnose(game, timeout):
    if os.name != "nt":
        raise RuntimeError("WinSta0 private-desktop observation requires Windows")
    if not TIMEOUT_MIN <= timeout <= TIMEOUT_MAX:
        raise ValueError("Startup observation timeout must be 30..3600 seconds")
    game = Path(game).resolve(strict=True)
    exe = game / "RimWorldWin64.exe"
    if not exe.is_file():
        raise RuntimeError("RimWorld executable missing")
    tasks = subprocess.run(["tasklist", "/FI", "IMAGENAME eq RimWorldWin64.exe"],
                           capture_output=True, text=True, check=True)
    if "rimworldwin64.exe" in tasks.stdout.lower():
        raise RuntimeError("Another RimWorld is active; do not interfere")
    normal = Path.home() / "AppData/LocalLow/Ludeon Studios/RimWorld by Ludeon Studios/Config"
    normal_config, normal_prefs = normal / "ModsConfig.xml", normal / "Prefs.xml"
    if not normal_config.is_file() or not normal_prefs.is_file():
        raise RuntimeError("Normal RimWorld settings templates unavailable (read only)")
    version = ET.parse(normal_config).getroot().findtext("version") or ""
    if not version.startswith("1.6"):
        raise RuntimeError("Actual RimWorld 1.6 required; detected " + version)

    runner = _runner_module()
    installed = runner.installed(game)
    runner.require_packages(installed, MO_BASE[0:1] + MO_BASE[2:] + PICKLE_TOOLS)
    hidden = runner.build_private_desktop_launcher()
    from pickle_run_monitor import run_hidden_with_status
    out = REPO / "TestResults/Pickle/StartupDiagnostics" / uuid.uuid4().hex[:10]
    out.mkdir(parents=True, exist_ok=False)
    observations = []
    for index, profile in enumerate(PROFILES, 1):
        report = out / profile / "Reports"
        report.mkdir(parents=True)
        savedata = out / profile / "SaveData"
        config_for_observation(savedata / "Config", normal_config, normal_prefs, profile)
        log = report / "Player.log"
        command = [exe, "-savedatafolder=" + str(savedata), "-logFile", str(log)]
        native_command = runner.private_desktop_command(hidden, game, timeout, command)
        env = os.environ.copy()
        print(f"[MO-STARTUP] {index}/2 {profile}: {', '.join(active_mods(profile))}",
              flush=True)
        code = run_hidden_with_status(native_command, report=report, game=game,
                                      env=env, profile=profile, timeout=timeout,
                                      diagnostic_only=True)
        result = observe_log(report)
        result["profile"] = profile
        result["active_mods"] = active_mods(profile)
        result["launcher_exit_code"] = code
        result["classification"] = (
            "OBSERVED_TIMEOUT_NOT_A_PASS" if result["native_timeout"]
            else "EXITED_NO_PICKLE_ASSERTIONS"
        )
        observations.append(result)
        (out / profile / "observation.json").write_text(
            json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[MO-STARTUP] {profile}: {result['classification']}; "
              f"Player.log={result['player_log_bytes']} bytes, "
              f"snapshots={result['diagnostic_snapshot_count']}; "
              "NO GAMEPLAY PASS", flush=True)
    (out / "comparison.json").write_text(
        json.dumps({"status": "DIAGNOSTIC_ONLY", "profiles": observations},
                   indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[MO-STARTUP] Observation complete, NOT an E2E PASS. Reports: {out}",
          flush=True)
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game", type=Path,
                        default=Path(r"D:\SteamLibrary\steamapps\common\RimWorld"))
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()
    try:
        diagnose(args.game, args.timeout)
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError,
            ET.ParseError) as exc:
        print("[MO-STARTUP BLOCKED]", exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
