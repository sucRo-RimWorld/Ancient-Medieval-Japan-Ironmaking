# Iron Sand Static Audit — owner-local Golden Path

**Scope:** first finite iron-sand ThingDef and map-generation source slice (RimWorld 1.6 developer files). This is a non-interactive static gate, **not a RimWorld loaded-game test**.

**Current test state (2026-10-13):** The current strict Pickle source contains
**10 Core and 7 Production scenarios per Vanilla/MO profile**; all revised
native test C# and game-run results are **not yet compiled/executed**. Static
source and runner CI PASS does not establish an in-game result.
The numbered 2026-10-10 results below are **historical development snapshots
only**; never use their old scenario counts, or statements about placeholder
graphics, as present-day acceptance. Current exact contracts and pending
items are in [IronmakingV1Coverage](../Testing/IronmakingV1Coverage.md).

## Repeatable static validation

From the Ironmaking repository root:

```text
python -m unittest discover -s Tests -p "test_*.py" -v
```

Historical 2026-10-10 fixture/structure tests covered: XML parse/unique DefNames, finite resource yield and no deep/infinite resource supply, independent item category outside `ResourcesRaw` bulk generation, GenStep/MapCommonBase Patch links and cell-safety validators, no hard dependency on MO/Environment/Harmony, and prototype graphics scope. The stale text/placeholder-path checks have been removed from routine tests.

Do not conflate a successful `GenStep_ScatterThings` XML parse with valid RimWorld map spawning. MO 1.6 provided evidence of the same Vanilla class, MapCommonBase injection and scatter validators. The implementation is independently authored and uses development-only Vanilla texture paths.

## Next validation gates

1. **Vanilla 1.6 Core Defs:** resolve `ResourceBase`, `RockBase`, `Root`, `GenStep_ScatterThings`, `MapCommonBase`, `Road` and all graphic texPaths in the actual installed source.
2. **Loaded-game:** startup log ERROR=0; sample multiple maps/seeds, verify scatter count and position; ensure water/road/buildings/start zones unaffected, mining work appears and yields finite `AMJ_IronSand`, then depot disappears and remains depleted after save/reload.
3. **Optional Mods:** repeat MO +/− metalChain, Environment and WTL Medieval filter after baseline works; no Vanilla Steel/MO IronOre/TraderKind rewriting.
4. **Graphics and balance:** accepted deposit and item textures, geographically weighted distribution, yield/price/amount, and trade availability are still unapproved and must not be promoted to release.

Do not add repeated automated GitHub Actions that notify for incomplete runtime infrastructure. The default test remains local static until a verified noninteractive game harness is available.

## First worktable/Recipe slice

Run the same static test command after adding Recipes. Tests no longer assert "no RecipeDefs exist"; instead they reject any Recipe that produces unbounded sand or sand-deposit Things. Historical source-level processing checks verified:
- pre-iron construction cost; no `CompProperties_Refuelable` on the AMJ production worktables;
- three-step material and output references;
- isolation of all `DankPyon_` symbols in a guarded MO compatibility Patch;
- MO IronBloom finishing converts to `DankPyon_IronIngot` at `DankPyon_Anvil`, not to Vanilla `Steel`.

The local source fixture passed **10 tests** on 2026-10-10. This does **not** prove the patched RecipeUsers resolve after actual load, that Vanilla has the intended Smithy Defs in the active profile, or that the MO fuel chain behaves correctly. No approved balance/visual assets exist, and every conversion ratio/work value is provisional.

## Targeted trade supplement

`Patches/TradeIronSand.xml` uses an existence-guarded `PatchOperationConditional` on Vanilla bulk caravans. It appends only `AMJ_IronSand` seller and buyer generators; it does not use `StockGenerator_Category(ResourcesRaw)`, remove Steel/IronIngot availability or modify MO-owned merchant Defs.

Trade source checks validate limited trader targets, correct separation of selling from buying, and no unrelated metal rewrites. The 2026-10-10 local suite passed **12 static tests**. Confirm actual Vanilla Core `TraderKindDef` existence, trader visitation/stock/price and save load in the RimWorld runtime before treating this as a reliable rescue route. Sales count 10~30 is a developer placeholder, not an approved balance value.

## Optional source-contract check against actual MO 1.6

When an actual MO 1.6 ZIP is available, run from the owner repository root:

```bash
AMJ_MO_ARCHIVE=/absolute/path/to/3219596926.zip python -m unittest discover -s Tests -p "test_*.py" -v
```

The three additional tests in `Tests/Production/test_mo_archive_contract.py` read the **supplied external archive**, do not vendor MO assets, and confirm MO package/name, IronIngot/Coal/Anvil upstream ThingDefs, the Ironmaking `loadAfter` soft order and the MO-guarded bloom output. With the author-provided archive on 2026-10-10, **15 tests passed**. Without `AMJ_MO_ARCHIVE`, the same suite runs 12 regular static checks and **skips three** MO-only tests rather than fabricating a MO compatibility PASS.

An initial local failure resulted from a stale **local verification copy** of Ironmaking `About/About.xml` lacking the current `loadAfter`; refreshing the local test copy to the already merged GitHub About resolved it. Always test the **current same-source tree**, not a previous exported prototype. This validation verifies source contracts only; actual RimWorld PatchOperation, worktable interaction, generation and game ERROR=0 remain unverified.

## 2026-10-10 category-parent and nested XML guard

RimWorld Wiki's Vanilla category list (last updated 2024-09-29) and the 1.6 Core-data reference list `Root` and `ResourcesRaw`, but do **not** list `Resources` as a valid parent. The original Ironmaking `AMJ_IronmakingMaterials` pointed to `Resources`; change that to `Root`, keeping a separate category (no generic `ResourcesRaw` stock). [Reference](https://rimworldwiki.com/wiki/Property:Thing_Categories).

The `test_all_xml_parses_and_ids_unique` test now walks nested `Patches/**/*.xml` (including MO compatibility) instead of just top-level Patches. Retain `Root` parent and non-`ResourcesRaw` assertions; this prevents both missing parent regressions and missing nested XML syntax checks. **RimWorld runtime/actual Core 1.6 loaded resolution remains untested.**

## Actual Vanilla 1.6 Core reference preflight (read-only)

When a genuine installed RimWorld 1.6 `Data/Core/Defs` is available, run:

```text
python Tools/check_vanilla_core_defs.py --core-defs "/path/to/RimWorld/Data/Core/Defs"
```

This scans the actual Core XML for Vanilla `Root`/`ResourcesRaw`, resource/bench/mineable parent names, `WoodLog`/`Steel`, existing Vanilla smithies, two sand-trade caravan `TraderKindDef`s, `Smithing` and `MapCommonBase`. It compares the Ironmaking category parent to `Root` and exits nonzero for missing references; incomplete or missing Core sources cannot become PASS. `Tests/Production/test_vanilla_core_def_contract.py` provides four independent **synthetic fixture tests** for successful reference lookup, old invalid `Resources` parent, missing trader kind, and empty Core input. All four fixture tests passed on 2026-10-10. **The actual Core source has not been supplied in this environment and no Core/loaded game PASS is claimed.** MO source-contract checks remain separate.

## From static source to loaded-game E2E

Use the owner [Ironmaking Pickle E2E procedure](IronmakingPickleE2E.md) for the two actual game profiles, independent Quickstarts, real mining WorkGiver and Pickle disk save/reload. The static XML/Mock Core tests are **not** a loaded-game gate; only fresh exact-name reports for 10 Core and 7 Production scenarios per Vanilla/MO, with zero failures/skips/flaky and complete game logs, qualify.
