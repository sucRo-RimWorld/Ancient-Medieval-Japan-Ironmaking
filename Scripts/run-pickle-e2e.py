#!/usr/bin/env python3
"""Launch real RimWorld 1.6/1.7 + Pickle in isolated saves. Never edit normal config."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import uuid
import xml.etree.ElementTree as ET

from pickle_run_monitor import run_hidden_with_status, diagnostic_tail
from isolated_rimworld_config import write_isolated_config
from validate_pickle_result import EXPECTED, PRODUCTION

REPO = Path(__file__).resolve().parents[1]
IRON_ID = "sucro.ancientmedievaljapan.ironmaking"
HARNESS_ID = IRON_ID + ".e2e"
BASE_IDS = ["brrainz.harmony", "ludeon.rimworld", "RimWorks.RimLogging",
            "rimworks.pickle", "rimworks.quickstarts"]
MO_IDS = ["OskarPotocki.VanillaFactionsExpanded.Core",
          "syrchalis.processor.framework", "DankPyon.Medieval.Overhaul"]
HIDDEN_LAUNCHER_SOURCE = REPO / "Scripts/IronmakingPrivateDesktop.cs"


def demand(ok, message):
    if not ok:
        raise RuntimeError(message)


def mod_id(root):
    about = root / "About" / "About.xml"
    if not about.is_file():
        return ""
    try:
        return (ET.parse(about).getroot().findtext("packageId") or "").lower()
    except ET.ParseError:
        return ""


def installed(game):
    steamapps = game.parent.parent
    workshop = steamapps / "workshop" / "content" / "294100"
    result = {}
    for parent in [game / "Mods", workshop]:
        if parent.is_dir():
            for item in parent.iterdir():
                if item.is_dir():
                    pid = mod_id(item)
                    if pid:
                        result.setdefault(pid, []).append(item.resolve())
    return result


def require_packages(found, ids):
    for pid in ids:
        roots = found.get(pid.lower(), [])
        demand(len(roots) == 1,
               "Expected exactly one installed Mod " + pid +
               "; found " + str(len(roots)) + " (no normal load-order changes made).")


SUPPORTED_TEST_VERSIONS = ("1.6", "1.7")


def test_game_version(config_version):
    major_minor = ".".join(config_version.split(".")[:2])
    demand(major_minor in SUPPORTED_TEST_VERSIONS,
           "Expected RimWorld 1.6 or 1.7 test config, version=" + config_version)
    return major_minor


def find_dll(root, name, game_version):
    matches = list(root.rglob(name))
    demand(matches, "Missing test provider " + name + " in " + str(root))
    for selected in (
        [p for p in matches if game_version in p.parts],
        [p for p in matches if "Current" in p.parts],
        [p for p in matches if p.parent.name == "Assemblies" and
         not any(part in SUPPORTED_TEST_VERSIONS for part in p.parts)],
    ):
        if selected:
            demand(len(selected) == 1,
                   "Ambiguous " + name + " for " + game_version + " in " + str(root))
            return selected[0]
    demand(len(matches) == 1,
           "No unambiguous test provider " + name + " for " + game_version +
           " in " + str(root))
    if game_version not in matches[0].parts:
        print("[WARN] Testing " + game_version + " with versioned provider " +
              str(matches[0]) + "; loaded-game results must verify compatibility.",
              flush=True)
    return matches[0]


def stage(mods_dir, label, expected, source):
    path = Path(tempfile.mkdtemp(prefix="AMJI-Pickle-" + label + "-", dir=mods_dir))
    marker = path / ".AMJI-PICKLE-OWNED"
    marker.write_text(expected, encoding="utf-8")
    try:
        for name in ("About", "Defs", "Patches", "Assemblies", "Textures",
                     "Languages", "Pickle"):
            item = source / name
            if item.is_dir():
                shutil.copytree(item, path / name, dirs_exist_ok=True)
        if (source / "LoadFolders.xml").is_file():
            shutil.copy2(source / "LoadFolders.xml", path / "LoadFolders.xml")
        demand(mod_id(path) == expected.lower(),
               "Staged Mod has unexpected packageId: " + str(path))
        return path
    except Exception:
        cleanup(path, expected)  # Includes incomplete test-only staging.
        raise


def cleanup(path, expected):
    marker = path / ".AMJI-PICKLE-OWNED"
    demand(path.is_dir() and marker.is_file() and
           marker.read_text(encoding="utf-8") == expected,
           "Unsafe cleanup refused for " + str(path))
    shutil.rmtree(path)


def make_config(config_dir, normal_mods, profile, normal_prefs):
    ids = BASE_IDS + (MO_IDS if profile == "MO" else []) + [IRON_ID, HARNESS_ID]
    write_isolated_config(config_dir, normal_mods, normal_prefs, ids)


def build(dotnet, project, game, reference_name, dll):
    subprocess.run([dotnet, "build", str(project), "-c", "Release", "--nologo",
                    "-p:RimWorldDir=" + str(game),
                    "-p:" + reference_name + "=" + str(dll)],
                   check=True, cwd=REPO)


def build_private_desktop_launcher():
    """Build the Windows desktop-isolation helper; no visible-game fallback."""
    demand(os.name == "nt", "Hidden Windows desktop needs native Windows")
    windir = Path(os.environ.get("WINDIR", r"C:\Windows"))
    candidates = [windir / "Microsoft.NET/Framework64/v4.0.30319/csc.exe",
                  windir / "Microsoft.NET/Framework/v4.0.30319/csc.exe"]
    csc = next((p for p in candidates if p.is_file()), None)
    demand(csc is not None, "Windows .NET Framework csc.exe unavailable; refusing visible run")
    demand(HIDDEN_LAUNCHER_SOURCE.is_file(), "Hidden desktop C# source missing")
    destination = REPO / "TestResults/Pickle/Build/PrivateDesktop/IronmakingPrivateDesktop.exe"
    destination.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([str(csc), "/nologo", "/target:exe",
                    "/out:" + str(destination), str(HIDDEN_LAUNCHER_SOURCE)],
                   cwd=REPO, check=True)
    demand(destination.is_file(), "Hidden desktop launcher did not build")
    return destination


def private_desktop_command(launcher, game, timeout, game_command):
    """Launch RimWorld through WinSta0 private desktop, retaining normal rendering."""
    demand(game_command and game_command[0].name.lower() == "rimworldwin64.exe",
           "Unexpected RimWorld launch command")
    demand(0 < timeout <= 3600, "Invalid private-desktop timeout")
    return [str(launcher), str(game_command[0]), str(game), str(timeout),
            *map(str, game_command[1:])]


def run(game, requested, timeout, suite="core"):
    demand(os.name == "nt", "This test runner requires private Windows desktop; no visible fallback")
    demand(0 < timeout <= 3600, "Timeout must be 1..3600 seconds")
    game = game.resolve(strict=True)
    if os.name == "nt":
        tasks = subprocess.run(["tasklist", "/FI", "IMAGENAME eq RimWorldWin64.exe"],
                               capture_output=True, text=True, check=True)
        demand("RimWorldWin64.exe".lower() not in tasks.stdout.lower(),
               "A normal RimWorld process is running; close it before E2E")
    exe = game / "RimWorldWin64.exe"
    mods_dir = game / "Mods"
    demand(exe.is_file() and mods_dir.is_dir(),
           "RimWorldWin64.exe or Mods missing from " + str(game))
    demand((game / "RimWorldWin64_Data/Managed/Assembly-CSharp.dll").is_file(),
           "RimWorld managed Assembly-CSharp.dll not found")
    local = Path.home() / "AppData/LocalLow/Ludeon Studios/RimWorld by Ludeon Studios/Config"
    normal_mods, normal_prefs = local / "ModsConfig.xml", local / "Prefs.xml"
    demand(normal_mods.is_file() and normal_prefs.is_file(),
           "Normal RimWorld ModsConfig and Prefs required as read-only templates")
    version = ET.parse(normal_mods).getroot().findtext("version") or ""
    game_version = test_game_version(version)
    print("[E2E] RimWorld test config version:", version,
          "(target " + game_version + "); game executable version is not independently verified.",
          flush=True)
    profiles = ["Vanilla", "MO"] if requested == "All" else [requested]
    found = installed(game)
    require_packages(found, BASE_IDS[0:1] + BASE_IDS[2:])
    if "MO" in profiles:
        require_packages(found, MO_IDS)
    pickle = find_dll(found["rimworks.pickle"][0], "RimWorks.Pickle.dll", game_version)
    quick = find_dll(found["rimworks.quickstarts"][0], "Quickstarts.dll", game_version)
    dotnet = shutil.which("dotnet")
    demand(dotnet is not None, "dotnet SDK is required to build Pickle steps")
    build(dotnet, REPO / "Tests/E2E/Quickstarts.csproj", game, "QuickstartsDll", quick)
    build(dotnet, REPO / "Tests/E2E/Steps.csproj", game, "PickleDll", pickle)
    private_desktop = build_private_desktop_launcher()

    stamp = uuid.uuid4().hex[:10]
    output = REPO / "TestResults/Pickle/Runs" / stamp
    output.mkdir(parents=True, exist_ok=False)
    owned = []
    try:
        root = REPO.resolve()
        if root.parent.resolve() == mods_dir.resolve():
            demand(mod_id(root) == IRON_ID,
                   "Source within RimWorld/Mods is not Ironmaking")
            actual_source = root
        else:
            existing = [r for r in found.get(IRON_ID, [])
                        if r.parent.resolve() == mods_dir.resolve()]
            demand(not existing, "Different Ironmaking already in game Mods; " +
                   "run from that exact source to avoid duplicate installations")
            actual_source = stage(mods_dir, "Source", IRON_ID, REPO)
            owned.append((actual_source, IRON_ID))
        helper = stage(mods_dir, "Harness", HARNESS_ID,
                       REPO / "Tests/E2E/TestMod")
        owned.append((helper, HARNESS_ID))
        assemblies = helper / "Assemblies"
        steps = helper / "Pickle/Assemblies"
        assemblies.mkdir(parents=True, exist_ok=True)
        steps.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPO / "TestResults/Pickle/Build/Quickstarts/AMJ.Ironmaking.Quickstarts.dll",
                     assemblies)
        shutil.copy2(REPO / "TestResults/Pickle/Build/Steps/AMJ.Ironmaking.PickleSteps.dll",
                     steps)

        for profile_index, profile in enumerate(profiles, 1):
            print(f"[E2E] Starting profile {profile_index}/{len(profiles)}: "
                  f"{profile}; Vanilla success does not imply MO success", flush=True)
            folder = output / profile
            report = folder / "Reports"
            report.mkdir(parents=True)
            save_data = folder / "SaveData"
            make_config(save_data / "Config", normal_mods, profile, normal_prefs)
            log = report / "Player.log"
            command = [str(exe), "-savedatafolder=" + str(save_data),
                       "-logFile", str(log), "-pickle-run=ironmaking-" + suite + ".feature",
                       "-pickle-mode=fast", "-pickle-set-name=" + profile,
                       "-pickle-report-dir=" + str(report), "-pickle-no-browser",
                       "-pickle-run-timeout=4", "-pickle-retry=0"]
            env = os.environ.copy()
            env["AMJI_EXPECTED_PROFILE"] = profile
            env["AMJI_EXPECTED_SOURCE_ROOT"] = str(actual_source)
            env["AMJI_PROGRESS_PATH"] = str(report / "step-progress.txt")
            hidden = private_desktop_command(private_desktop, game, timeout,
                                             [Path(command[0]), *command[1:]])
            code = run_hidden_with_status(hidden, report=report, game=game, env=env,
                                          profile=profile, timeout=timeout, suite=suite)
            if code != 0:
                print("[E2E " + profile + "] Startup/game failure diagnostics:\n" +
                      diagnostic_tail(report), file=sys.stderr, flush=True)
            demand(code == 0,
                   "Private desktop / RimWorld / Pickle exited " + str(code) +
                   "; inspect launcher.log and Player.log in " + str(report))
            subprocess.run([sys.executable, str(REPO / "Scripts/validate_pickle_result.py"),
                            "--report", str(report), "--suite", suite], check=True, cwd=REPO)
            print("PICKLE PASS", profile,
                  str(len(EXPECTED if suite == "core" else PRODUCTION)) +
                  " loaded-game scenarios (" + suite + ")", flush=True)
        print("All requested profiles passed. Reports:", output)
    finally:
        for path, ident in reversed(owned):
            cleanup(path, ident)
        print("Cleaned owned test folders. Normal ModsConfig, Prefs and saves untouched.")


def is_waylith_game(game):
    """Select the 1.7 native test runner from the actual game build, not user config."""
    version_file = Path(game) / "Version.txt"
    return version_file.is_file() and version_file.read_text(
        encoding="utf-8-sig").strip().startswith("1.7.")


def run_waylith_test(game, profile, suite, timeout):
    command = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
               "-File", str(REPO / "Scripts/Run-17Tests.ps1"),
               "-GameRoot", str(game), "-Profile", profile,
               "-Suite", suite, "-TimeoutSeconds", str(timeout)]
    subprocess.run(command, cwd=REPO, check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game", type=Path,
                        default=Path(r"D:\SteamLibrary\steamapps\common\RimWorld"))
    parser.add_argument("--profile", choices=("Vanilla", "MO", "All"), default="Vanilla")
    parser.add_argument("--suite", choices=("core", "production"), default="core")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--diagnose-mo-startup", action="store_true",
                        help="Observe MO baseline vs MO+Pickle on separate hidden desktops; no E2E PASS")
    args = parser.parse_args()
    try:
        if is_waylith_game(args.game):
            demand(not args.diagnose_mo_startup,
                   "MO startup diagnostic remains 1.6-only; use the 1.7 Pickle suites.")
            run_waylith_test(args.game, args.profile, args.suite, args.timeout)
        elif args.diagnose_mo_startup:
            from diagnose_mo_startup import diagnose
            diagnose(args.game, args.timeout)
        else:
            run(args.game, args.profile, args.timeout, args.suite)
    except (RuntimeError, ValueError, OSError, subprocess.CalledProcessError, ET.ParseError) as exc:
        print("[PICKLE BLOCKED/FAIL]", exc, file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
