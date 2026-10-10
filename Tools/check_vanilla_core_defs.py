#!/usr/bin/env python3
"""Read-only RimWorld 1.6 Core Def cross-reference preflight.

This reads installed Vanilla XML; it does not run RimWorld, resolve final patch
operations, verify textures or establish a gameplay PASS.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = {
    "ThingCategoryDef": {"Root", "ResourcesRaw"},
    "ThingDef": {"WoodLog", "Steel", "FueledSmithy", "ElectricSmithy"},
    "TraderKindDef": {"Caravan_Neolithic_BulkGoods", "Caravan_Outlander_BulkGoods"},
    "ResearchProjectDef": {"Smithing"},
}
ABSTRACT_THINGS = {"BenchBase", "RockBase", "ResourceBase"}
BASE_MAP_GENERATOR = "MapCommonBase"


def inventory(core_defs: Path) -> tuple[dict[str, set[str]], set[str], set[str], int]:
    """Extract identity of concrete/abstract XML Def nodes; no inheritance guesswork."""
    if not core_defs.is_dir():
        raise ValueError(f"RimWorld 1.6 Core Defs directory unavailable: {core_defs}")
    found: dict[str, set[str]] = defaultdict(set)
    abstract: set[str] = set()
    map_parents: set[str] = set()
    scanned = 0
    for path in sorted(core_defs.rglob("*.xml")):
        try:
            root = ET.parse(path).getroot()
        except ET.ParseError as exc:
            raise ValueError(f"Invalid Core XML {path}: {exc}") from exc
        scanned += 1
        if root.tag != "Defs":
            continue
        for node in root:
            name = node.findtext("defName")
            if name:
                found[node.tag].add(name.strip())
            if node.tag == "ThingDef" and node.get("Name"):
                abstract.add(node.get("Name"))
            if node.tag == "MapGeneratorDef" and node.get("Name"):
                map_parents.add(node.get("Name"))
    if scanned == 0:
        raise ValueError(f"Core Defs contains no XML files: {core_defs}")
    return found, abstract, map_parents, scanned


def check(core_defs: Path, mod_root: Path = ROOT) -> list[str]:
    found, abstract, map_parents, scanned = inventory(core_defs)
    errors = []
    for kind, identities in REQUIRED.items():
        for missing in sorted(identities - found.get(kind, set())):
            errors.append(f"Missing Vanilla Core {kind}: {missing}")
    for name in sorted(ABSTRACT_THINGS - abstract):
        errors.append(f"Missing Vanilla Core abstract ThingDef Name: {name}")
    if BASE_MAP_GENERATOR not in map_parents:
        errors.append(f"Missing Vanilla Core MapGeneratorDef Name: {BASE_MAP_GENERATOR}")
    category_path = mod_root / "Defs/ThingCategoryDefs/IronmakingCategories.xml"
    try:
        cat = ET.parse(category_path).getroot().find("ThingCategoryDef")
        actual_parent = cat.findtext("parent") if cat is not None else None
    except (OSError, ET.ParseError) as exc:
        raise ValueError(f"Invalid or unavailable Ironmaking category file: {exc}") from exc
    if actual_parent != "Root":
        errors.append(f"IronmakingMaterials must use Vanilla Root, not {actual_parent!r}")
    elif actual_parent not in found.get("ThingCategoryDef", set()):
        errors.append("IronmakingMaterials parent Root not present in selected Core")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--core-defs", type=Path, required=True,
                        help="Actual RimWorld/Data/Core/Defs directory")
    parser.add_argument("--mod-root", type=Path, default=ROOT,
                        help="Ironmaking repository root (default: script's parent)")
    args = parser.parse_args()
    try:
        errors = check(args.core_defs, args.mod_root)
    except ValueError as exc:
        print(f"Core cross-reference BLOCKED: {exc}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print("Core XML identity preflight PASS (not a loaded RimWorld test)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
