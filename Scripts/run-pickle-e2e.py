#!/usr/bin/env python3
"""Launch real RimWorld 1.6 + Pickle in isolated saves. Never edit normal config."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import uuid
import xml.etree.ElementTree as ET

REPO = Path(__file__).resolve().parents[1]
IRON_ID = "sucro.ancientmedievaljapan.ironmaking"
HARNESS_ID = IRON_ID + ".e2e"
BASE_IDS = ["brrainz.harmony", "ludeon.rimworld", "RimWorks.RimLogging",
            "rimworks.pickle", "rimworks.quickstarts"]
MO_IDS = ["OskarPotocki.VanillaFactionsExpanded.Core",
          "syrchalis.processor.framework", "DankPyon.Medieval.Overhaul"]
FEATURE = "ironmaking-core.feature"


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


def find_dll(root, name):
    matches = list(root.rglob(name))
    preferred = [p for p in matches if "1.6" in p.parts]
    if preferred:
        matches = preferred
    demand(len(matches) == 1,
           "Cannot unambiguously locate 1.6 " + name + " in " + str(root))
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


def make_config(config_dir, version, profile, normal_prefs):
    config_dir.mkdir(parents=True, exist_ok=False)
    prefs = ET.parse(normal_prefs)
    dev = prefs.getroot().find(".//devMode")
    if dev is None:
        dev = ET.SubElement(prefs.getroot(), "devMode")
    dev.text = "True"
    prefs.write(config_dir / "Prefs.xml", encoding="utf-8", xml_declaration=True)
    ids = BASE_IDS + (MO_IDS if profile == "MO" else []) + [IRON_ID, HARNESS_ID]
    root = ET.Element("ModsConfigData")
    ET.SubElement(root, "version").text = version
    active = ET.SubElement(root, "activeMods")
    for pid in ids:
        ET.SubElement(active, "li").text = pid
    ET.SubElement(root, "knownExpansions")
    ET.ElementTree(root).write(config_dir / "ModsConfig.xml",
                               encoding="utf-8", xml_declaration=True)


def build(dotnet, project, game, reference_name, dll):
    subprocess.run([dotnet, "build", str(project), "-c", "Release", "--nologo",
                    "-p:RimWorldDir=" + str(game),
                    "-p:" + reference_name + "=" + str(dll)],
                   check=True, cwd=REPO)


def run(game, requested, timeout):
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
           "RimWorld 1.6 managed Assembly-CSharp.dll not found")
    local = Path.home() / "AppData/LocalLow/Ludeon Studios/RimWorld by Ludeon Studios/Config"
    normal_mods, normal_prefs = local / "ModsConfig.xml", local / "Prefs.xml"
    demand(normal_mods.is_file() and normal_prefs.is_file(),
           "Normal RimWorld ModsConfig and Prefs required as read-only templates")
    version = ET.parse(normal_mods).getroot().findtext("version") or ""
    demand(version.startswith("1.6"), "Expected RimWorld 1.6, config version=" + version)
    profiles = ["Vanilla", "MO"] if requested == "All" else [requested]
    found = installed(game)
    require_packages(found, BASE_IDS[0:1] + BASE_IDS[2:])
    if "MO" in profiles:
        require_packages(found, MO_IDS)
    pickle = find_dll(found["rimworks.pickle"][0], "RimWorks.Pickle.dll")
    quick = find_dll(found["rimworks.quickstarts"][0], "Quickstarts.dll")
    dotnet = shutil.which("dotnet")
    demand(dotnet is not None, "dotnet SDK is required to build Pickle steps")
    build(dotnet, REPO / "Tests/E2E/Quickstarts.csproj", game, "QuickstartsDll", quick)
    build(dotnet, REPO / "Tests/E2E/Steps.csproj", game, "PickleDll", pickle)

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

        for profile in profiles:
            folder = output / profile
            report = folder / "Reports"
            report.mkdir(parents=True)
            save_data = folder / "SaveData"
            make_config(save_data / "Config", version, profile, normal_prefs)
            log = report / "Player.log"
            command = [str(exe), "-savedatafolder=" + str(save_data),
                       "-logFile", str(log), "-pickle-run=" + FEATURE,
                       "-pickle-mode=fast", "-pickle-set-name=" + profile,
                       "-pickle-report-dir=" + str(report), "-pickle-no-browser",
                       "-pickle-run-timeout=12", "-pickle-retry=0"]
            env = os.environ.copy()
            env["AMJI_EXPECTED_PROFILE"] = profile
            env["AMJI_EXPECTED_SOURCE_ROOT"] = str(actual_source)
            with (report / "launcher.log").open("w", encoding="utf-8") as output_log:
                try:
                    proc = subprocess.run(command, cwd=game, env=env, timeout=timeout,
                                          stdout=output_log, stderr=subprocess.STDOUT)
                except subprocess.TimeoutExpired as exc:
                    raise RuntimeError("RimWorld timed out for " + profile) from exc
            demand(proc.returncode == 0,
                   "RimWorld/Pickle exited " + str(proc.returncode) + "; " + str(report))
            subprocess.run([sys.executable, str(REPO / "Scripts/validate_pickle_result.py"),
                            "--report", str(report)], check=True, cwd=REPO)
            print("PICKLE PASS", profile, "5 loaded-game scenarios", flush=True)
        print("All requested profiles passed. Reports:", output)
    finally:
        for path, ident in reversed(owned):
            cleanup(path, ident)
        print("Cleaned owned test folders. Normal ModsConfig, Prefs and saves untouched.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game", type=Path,
                        default=Path(r"D:\SteamLibrary\steamapps\common\RimWorld"))
    parser.add_argument("--profile", choices=("Vanilla", "MO", "All"), default="Vanilla")
    parser.add_argument("--timeout", type=int, default=900)
    args = parser.parse_args()
    try:
        run(args.game, args.profile, args.timeout)
    except (RuntimeError, OSError, subprocess.CalledProcessError, ET.ParseError) as exc:
        print("[PICKLE BLOCKED/FAIL]", exc, file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
