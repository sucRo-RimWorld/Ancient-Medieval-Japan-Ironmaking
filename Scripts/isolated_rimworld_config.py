"""Environment-compatible isolated RimWorld 1.6 profile writer.

Use the current user ModsConfig.xml *as a read-only template*, exactly as
the successful AMJ Environment development Pickle runner does. Preserve the
original knownExpansions and other load context; replace only activeMods.
Always disable automatic mods-list reset on errors *in the copied Prefs* so
the first actual MO exception and original requested profile are retained.
"""
from pathlib import Path
import xml.etree.ElementTree as ET


def write_isolated_config(config_dir, source_mods, source_prefs, package_ids):
    config_dir = Path(config_dir)
    source_mods, source_prefs = Path(source_mods), Path(source_prefs)
    if config_dir.exists():
        raise FileExistsError("Refusing to overwrite test profile: " + str(config_dir))

    mods = ET.parse(source_mods)
    root = mods.getroot()
    if root.tag != "ModsConfigData" or not (root.findtext("version") or "").startswith("1.6"):
        raise ValueError("Source RimWorld ModsConfigData is not version 1.6")
    active = root.find("activeMods")
    if active is None:
        raise ValueError("Source ModsConfig.xml has no activeMods")
    if root.find("knownExpansions") is None:
        raise ValueError("Source ModsConfig.xml has no knownExpansions; refusing synthetic blank DLC list")
    active.clear()
    ids = [str(name).strip().lower() for name in package_ids]
    if not ids or any(not name for name in ids) or len(ids) != len(set(ids)):
        raise ValueError("Empty or duplicate test package IDs")
    for name in ids:
        ET.SubElement(active, "li").text = name

    prefs = ET.parse(source_prefs)
    for name, value in (("devMode", "True"), ("resetModsConfigOnCrash", "False")):
        node = prefs.getroot().find(name)
        if node is None:
            node = ET.SubElement(prefs.getroot(), name)
        node.text = value

    # Parse and validate both sources before creating a single test file.
    config_dir.mkdir(parents=True, exist_ok=False)
    mods.write(config_dir / "ModsConfig.xml", encoding="utf-8", xml_declaration=True)
    prefs.write(config_dir / "Prefs.xml", encoding="utf-8", xml_declaration=True)
