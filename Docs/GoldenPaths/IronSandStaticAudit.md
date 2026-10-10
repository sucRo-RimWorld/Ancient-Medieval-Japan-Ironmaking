# Iron Sand Static Audit — owner-local Golden Path

**Scope:** first finite iron-sand ThingDef and map-generation source slice (RimWorld 1.6 developer files). This is a non-interactive static gate, **not a RimWorld loaded-game test**.

## Repeatable static validation

From the Ironmaking repository root:

```text
python -m unittest discover -s Tests -p "test_*.py" -v
```

Six 2026-10-10 fixture/structure tests cover: XML parse/unique DefNames, finite resource yield and no deep/infinite resource supply, independent item category outside `ResourcesRaw` bulk generation, GenStep/MapCommonBase Patch links and cell-safety validators, no hard dependency on MO/Environment/Harmony, and explicit unapproved image status.

Do not conflate a successful `GenStep_ScatterThings` XML parse with valid RimWorld map spawning. MO 1.6 provided evidence of the same Vanilla class, MapCommonBase injection and scatter validators. The implementation is independently authored and uses development-only Vanilla texture paths.

## Next validation gates

1. **Vanilla 1.6 Core Defs:** resolve `ResourceBase`, `RockBase`, `Resources`, `GenStep_ScatterThings`, `MapCommonBase`, `Road` and all graphic texPaths in the actual installed source.
2. **Loaded-game:** startup log ERROR=0; sample multiple maps/seeds, verify scatter count and position; ensure water/road/buildings/start zones unaffected, mining work appears and yields finite `AMJ_IronSand`, then depot disappears and remains depleted after save/reload.
3. **Optional Mods:** repeat MO +/− metalChain, Environment and WTL Medieval filter after baseline works; no Vanilla Steel/MO IronOre/TraderKind rewriting.
4. **Graphics and balance:** accepted deposit and item textures, geographically weighted distribution, yield/price/amount, and trade availability are still unapproved and must not be promoted to release.

Do not add repeated automated GitHub Actions that notify for incomplete runtime infrastructure. The default test remains local static until a verified noninteractive game harness is available.

## First worktable/Recipe slice

Run the same static test command after adding Recipes. Tests no longer assert "no RecipeDefs exist"; instead they reject any Recipe that produces unbounded sand or sand-deposit Things. Additional four tests verify:
- pre-iron construction cost; no `CompProperties_Refuelable` on the AMJ production worktables;
- three-step material and output references;
- isolation of all `DankPyon_` symbols in a guarded MO compatibility Patch;
- MO IronBloom finishing converts to `DankPyon_IronIngot` at `DankPyon_Anvil`, not to Vanilla `Steel`.

The local source fixture passed **10 tests** on 2026-10-10. This does **not** prove the patched RecipeUsers resolve after actual load, that Vanilla has the intended Smithy Defs in the active profile, or that the MO fuel chain behaves correctly. No approved balance/visual assets exist, and every conversion ratio/work value is provisional.

## Targeted trade supplement

`Patches/TradeIronSand.xml` uses an existence-guarded `PatchOperationConditional` on Vanilla bulk caravans. It appends only `AMJ_IronSand` seller and buyer generators; it does not use `StockGenerator_Category(ResourcesRaw)`, remove Steel/IronIngot availability or modify MO-owned merchant Defs.

Two additional static tests check limited trader targets, correct separation of selling from buying, and no unrelated metal rewrites. The 2026-10-10 local suite passed **12 static tests**. Confirm actual Vanilla Core `TraderKindDef` existence, trader visitation/stock/price and save load in the RimWorld runtime before treating this as a reliable rescue route. Sales count 10~30 is a developer placeholder, not an approved balance value.
