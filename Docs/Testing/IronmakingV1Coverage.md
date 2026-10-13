# Ironmaking v1 — test premises and acceptance matrix

**Owner:** Ironmaking. **Canonical gameplay scope:** [Design](../Design.md).  
**Current source:** the feature files and production XML, not historical run counts.  
**Evidence:** [Native17-20261013.json](Native17-20261013.json) (pre-research baseline);
[IronmakingPickleEvidence.md](IronmakingPickleEvidence.md).  
**Maturity:** revised source/Pickle tests require *new* loaded-game runs; no
2026-10-13 old PASS is inherited after the research implementation or this test change.

## Routine runtime scenarios (eight Core + seven Production per profile)

| Suite | Named scenario | Contract / exact assumption | Evidence |
|---|---|---|---|
| Core | Exact Ironmaking development source and profile are loaded | One loaded Ironmaking package at the expected source root, correct MO profile; **root identity, not content-hash equality** | Old 1.7 passed; revised pending |
| Core | Processing Defs and Vanilla or MO result resolve | Finite mineable Def and three basic process Defs; Vanilla bloom→Steel, MO bloom→IronIngot via Anvil, no MO direct Steel shortcut | Old 1.7 passed; revised pending |
| Core | Native initial ironmaking research gate | Smithing precedes AMJ research; before initial research the furnace and smelting requirement are unsatisfied, Smithing alone does not unlock them; afterwards both requirements are satisfied; charcoal remains ungated. **Designator visibility is a separate UI gate.** | New, native pending |
| Core | Loaded sand trade generators distinguish buying and selling | After XML Patch execution, Vanilla Tribal/Outlander bulk traders each contain exactly one sand `StockGenerator_SingleDef` seller and `StockGenerator_BuySingleDef` buyer; **this is not generated merchant inventory** | New, native pending |
| Core | Natural map creation produces finite iron sand | One naturally generated deposit exists and is revealed; this is a prerequisite for, not a substitute for, native mining | Old 1.7 passed; revised pending |
| Core | Natural iron-sand deposit is actually mineable and finite | A native Mining WorkGiver can designate, mine and destroy a **naturally placed** deposit next to a standable revealed cell; IronSand increases; the consumed node does not spontaneously reappear after 1,200 ticks on that map | New, native pending |
| Core | Colonist mining job consumes finite deposit and yields sand | Mine WorkGiver depletes a **fixture-spawned** deposit; sand quantity rises | Old 1.7 passed; revised pending |
| Core | Sand deposits survive real game save reload | Genuine disk save/reload persists a fixture deposit on a map | Old 1.7 passed; revised pending |
| Production | Exact Ironmaking development source and profile are loaded | Same source/profile identity, independent run | Old 1.7 passed; revised pending |
| Production | Loaded fuel component exclusivity | AMJ kiln and furnace have no Refuelable comp after actual Def inheritance/patching | New, native pending |
| Production | Charcoal bill consumes wood and produces charcoal | Native crafting pawn Bill; currently **20 WoodLog → 10 AMJ_Charcoal**; resource conservation | Old 1.7 passed; revised pending |
| Production | Smelting bill consumes sand and charcoal and produces bloom | Research completed first through native manager; Bill consumes **40 sand + 60 AMJ charcoal → 10 bloom** | Old 1.7 passed; revised pending |
| Production | Optional MO coal fuel and Vanilla isolation | Vanilla has no loaded MO coal ThingDef; MO actually consumes **60 DankPyon_Coal** instead of AMJ charcoal, produces 10 bloom | New, native pending |
| Production | Interrupted smelting conserves resources | Start a native smelting job, advance 20 game ticks, force-interrupt before completion, obtain the next Bill from a genuine loaded WorkGiver and complete once; no early output; final **40 sand + 60 AMJ charcoal → 10 bloom**, no duplicate material consumed or produced. **This does not yet include interruption across disk save/reload.** | New, native pending |
| Production | Forging bill consumes bloom and produces the profile metal | Native Bill after research; **10 bloom → 8 Steel** Vanilla, **8 MO IronIngot** MO; fueled vanilla smithy consumes fuel | Old 1.7 passed; revised pending |

The two scenarios named 'Exact Ironmaking development source and profile' are
distinct execution safety checks, not duplicated gameplay proof. The MO-fuel
scenario makes a different assertion in Vanilla and MO; never describe it as a
Vanilla MO-coal conversion. No runtime scenario above tests final economic values.

## Static checks / scope corrections

- Keep parsable XML, unique DefNames, finite non-replenishing mineables, no generic
  ResourcesRaw injection, seller versus buyer stock, and optional MO isolation.
- **Do not assert:** the exact count of future tables/Recipes/Patch operations,
  Chemfuel placeholder texPath, About saying 'not release-ready', or the exact
  provisional caravan quantity as *accepted design*. Actual XML outputs still
  must be checked for internal consistency.
- Real Vanilla Core and MO archive cross-reference checks need actual installed
  provider inputs. Fixture checks and optional skips alone never prove the
  current provider's identity.
- Native 1.7 acceptance requires fresh named Pickle summaries, correct source,
  complete PID-tied Player.log with `INFO Log closed.`, no ERROR, no skip/flaky.
  Historical startup diagnostic fixtures are kept outside routine CI.

## v1 acceptance gaps not covered by the current automated scenarios

| Priority | Pending verification | Required behavior |
|---|---|---|
| P0 | Research construction/UI availability before/after | Not merely XML prerequisites: actual building designator and Bill exposure must obey the gate; research visibility/placement in Vanilla/MO/Japanization |
| P0 | Interrupted work across save/reload / fuel depletion | Native forced-interrupt and retry has a new scenario, **not run**; the additional interrupted-job save/reload and depleted-fuel cases remain open. Do not treat the new one-session test as all interruption modes |
| P0 | Native integrated logistics | Valid initial bootstrap with no steel; actual hauling, fuel replenishment and full output chain without test-spawned intermediate items |
| P0 | Genuine existing colony addition/removal/re-add | An *actual pre-mod save* remains loadable; no assumed backfilled deposits; trade fallback, safe item/recipe cleanup as applicable. Fresh-test save/reload does not substitute |
| P0 | Exact release texture and presentation | Owner-approved natural low-profile sand deposit, AMJ material/building artwork, recipe/UI layout, graphic states |
| P1 | Seed/map/terrain distribution | The new natural-source mining test covers one fixed map and one depleted cell, **not** alternative seeds, regional weighting, map-wide inaccessibility or landform statistics. No placement in water/impassable/starter/quest structures |
| P1 | Actual generated merchant inventories | Loaded trader generator presence has a new scenario, **not run**; verify that real arrivals sell/buy sand in appropriate quantities and that sparse/old maps can import it without guaranteed stock |
| P1 | MO on/off settings | metalChain ON/OFF with woodChain sample; stable MO ore/Mine Shaft/deep/traders and no user setting mutation |
| P1 | Balanced yield/cost/time/fuel/transport | No adopted economic values yet; use real work, multiple batches, storage/haul cost comparisons |
| Optional | Japanization, WTL, Environment | Only specific conditional features; Japanization owns MO-wide resource rebalance; no mandatory dependency or unrequested full Cartesian matrix |
| Release | Exact subscriber payload, languages, save claims | Distribution package tested separately from source, Workshop publication not inferred from test success |

## Scope boundary

The first *executable MVP* remains finite sand, charcoal, one furnace, bloom
and common metal; the design's higher-furnace progression is **not yet
implemented**. The author has not reclassified those later furnaces as required
for this particular test-closeout. No tests should fabricate their Defs or
mark them PASS while that design/release distinction remains open.
