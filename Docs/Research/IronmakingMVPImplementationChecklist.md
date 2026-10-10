# AMJ Ironmaking — minimal implementation checklist (candidate)

**Status:** 2026-10-10 first sand/deposit MapGen static source added; other MVP modules not implemented, loaded-game results unverified and numeric balancing unapproved.  
**Authoritative concept:** [Ironmaking design](../Design.md).  
**Owner:** `sucRo-RimWorld/Ancient-Medieval-Japan-Ironmaking`.

## Thin vertical slice

1. **Static source implemented, runtime unverified:** `AMJ_IronSand` + finite `AMJ_IronSandDeposit`, dedicated `AMJ_IronmakingMaterials` resource category, `AMJ_ScatterIronSand` GenStep and MapCommonBase attachment. No extraction/mining or generated-map runtime PASS yet; region weighting absent.
2. **Static XML added, runtime unverified:** WoodLog → AMJ_Charcoal via worktable Bill without MO/PF hard dependency. With MO, MO Coal is optionally accepted as a Bill ingredient; duplicate AMJ charcoal manufacture is still visible pending compatibility testing.
3. **Static XML added, runtime unverified:** small furnace uses Stony material and requires no Steel/component; buildability and workbench visuals must be checked in loaded Vanilla.
4. **Static XML added, runtime unverified:** sand + charcoal (or MO Coal) Bill → IronBloom; no Refuelable on AMJ kilns/furnaces. Confirm actual input/yield, work and interrupts in RimWorld.
5. **Conditional XML implemented, runtime unverified:** Vanilla `FueledSmithy`/`ElectricSmithy` converts IronBloom → Steel; MO-Patch replaces both `recipeUsers` and output with `DankPyon_Anvil` → `DankPyon_IronIngot`. Confirm PatchOperationFindMod activation and metalChain ON/OFF; MO research must not be bypassed.
6. **Static Patch added, runtime unverified:** two Vanilla bulk caravan TraderKinds get a limited `AMJ_IronSand` `StockGenerator_SingleDef` (seller) and `StockGenerator_BuySingleDef` (buyer), conditional on an existing TraderKind stock list. Vanilla/MO metal goods remain unchanged; visit stock and quantities require loaded-game testing.
7. Keep higher furnaces, iron sand washing, iron slag/pig iron, special sword steel, full historical waterworks and late tatara out of first executable slice.

## Resource discovery / map generation prototype

- Prefer finite low-profile surface deposit Thing, no growth mechanics and no infinite Terrain harvesting.
- MO 1.6 supplies a source-level example of `GenStep_ScatterThings` with validators and a `MapCommonBase/genSteps` integration patch. **First test a small XML-only GenStep using the Vanilla scatter machinery** to establish finite reachable deposits; use C# only when exact river/coast/gravel cell weighting is proven necessary. Do not copy MO artwork or assume its fantasy Golem mechanics are part of Ironmaking.
- Compare Vanilla Mineable scatter against terrain-weighted cells; a small custom GenStep only if cell-based river/coast/gravel weighting actually requires it.
- Don't change TerrainDefs, MO ore Mineable, Vanilla Steel, or World Grid to create the deposits.
- Test stable Seed generation, no blocked river or starter sites, reachable cells, harvest and depletion, low/no-deposit map with trading fallback.
- Do not backfill saved maps automatically in v1; validate add-to-save with the fallback, and report new-map-only generation in public description if confirmed.

## Optional World Tech Level verification

World Tech Level is recommended for an era-limited AMJ world, **not a dependency**. Smoke the Medieval profile with Research, Items, Mineable Resources and Map GenStep filters ON: Ironmaking's sand-iron sellers, finite deposit map generation and smelting research remain accessible. Test the normal standalone profile with the filters OFF as well. The WTL trader patch limits Category/MiscItems/Tag StockGenerators, **not MO's explicit IronIngot SingleDef stock**; never rely on WTL alone to balance those fixed ingot supplies.

## Compatibility gates

| Profile | Minimum evidence |
|---|---|
| Vanilla + Ironmaking | map generation, charcoal, initial furnace and Steel path, sand iron trade, no missing dependency |
| MO + Ironmaking (metalChain ON/OFF) | no duplicate material exposure or double fuel, MO IronIngot exit, intact MO ore/ingot traders and Mine Shaft |
| MO + Japanization + Ironmaking, metalChain ON × vanillaMine ON/OFF | sand iron as main *local smelting feedstock* subject to verified Mineable/Deep/Mine Shaft/merchant routes |
| MO + Japanization + Ironmaking, metalChain OFF | preserve user toggle; track direct iron ingot mineables / Mine Shaft and possible deep outputs; compatibility not equivalent scarcity |
| Environment optional | enhanced generation weighting only, without duplicate sand iron resource owner |
| Existing save | old maps remain loadable, external sand iron trade route works, no mandatory backfill |

No price, vein or Recipe ratio should be described as finalized before loaded economic tests with installed Vanilla 1.6 Core and representative trader sources.

## Automated testing order

Static XML references → map-generation determinism and reachability → minable extraction/depletion → bill and fuel consumption → MO processing integration → 2×2 MO setting matrix → Vanilla/MO/third-party trade inventory → add/remove save tests → no-error runtime gate.

Use RimTest Redux/Pickle where suitable; avoid turning all optional-Mod combinations into a mandatory cross-product matrix. Human verification is reserved for deposit graphics and interaction presentation.

## 2026-10-10 entry/feasibility status

The XML-only finite deposit probe passed five isolated syntax/structure tests. It is explicitly **not a loaded-game MapGen/Mining PASS** and is not part of a subscriber payload. `RockBase` and placeholder graphics are only used to test XML wiring. A targeted 1.6 maintained-source comparison of Vanilla Iron and Steel Continued, Expanded Materials - Metals and tatara compatibility is still required by the new-feature entry gate; see `IronmakingExistingModEntryAudit-20261010.md`. Do not copy the research probe into another AMJ owner runtime repository, and do not merge production code before the decision record is ready.
