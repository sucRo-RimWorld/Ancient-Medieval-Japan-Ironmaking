# Ironmaking — existing-Mod entry comparison (2026-10-10)

**State:** INCOMPLETE / production entry HOLD. The independent Ironmaking **concept** and its historical boundary are approved, but the Project-wide [Project ExistingModAudit](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/ExistingModAudit.md#implementation-entry-gate) requires source-level review of relevant current non-VE 1.6 alternatives and a validated decision record before production implementation.

**Owner:** `sucRo-RimWorld/Ancient-Medieval-Japan-Ironmaking`. Migrated from Project pre-split research 2026-10-10. Owner repository initialized; no playable Mod is present.

## Requested behavior and precise gap

The approved standalone Mod supplies *finite Japanese iron sand → bloom/small furnace → forgeable general metal* from early settlement play, followed by an improved furnace and a historically pre-Edo medieval tatara research tier. No hard dependency on MO, Environment, Grains or World Tech Level. Ironmaking must coexist with existing Vanilla Steel and MO IronOre/IronIngot. When Japanization also exists, Japanization owns conditional changes to MO ore/deep/trader/other-MO-resource flows.

**Potential unmet requirement:** other reviewed metallurgical Mods mainly rework generic global steel/ore or supply broad industrial metal catalogs; they do not yet establish this *locally finite Japanese sand deposit with era-limited three-scale smelting, standalone operation and optional MO integration*. This is a comparison hypothesis supported by only the source/evidence levels stated below, **not a blanket claim that no competing Mod exists**.

## Audited candidates and limits

| Existing product / surface | Evidence available | Functional fit / limitation | Provisional treatment |
|---|---|---|---|
| Vanilla RimWorld 1.6 | Project Ironmaking design/owner research, not installed current `Data/Core` loaded Defs | Existing Steel/smithing/production are final-metal integration points; no reviewed built-in finite iron-sand system | Keep as required baseline; verify 1.6 Core before Bill/Workbench production |
| Medieval Overhaul (MO) 1.6 | **Author-supplied** `3219596926.zip`, SHA-256 `6ed379d7c400db43b3af2a9a7fd6203f7f7e99ca1a670d36b0f73fd1adccc9e3`. See IronmakingDesign and Japanization IronSupplyAudit | Own iron ore, ingots, coal, Smelter, Mine Shaft, and high-yield golem resource paths. No independent Japanese finite sand+pre-Edo tier chain demonstrated; hard-requiring MO breaks approved standalone contract | Preserve MO paths and add optional ordinary compatibility; conditional supply changes belong to Japanization |
| Vanilla Factions Expanded - Medieval 2 (VE) | Workshop `3444347874`; current feature comparison is description and earlier referenced Linkable IDs, **not an exhaustive loaded Def review** | General medieval tech/forge and bellows overlap; no verified replacement for the full Japanese local sand/tatara path | Prior art, possible optional compatibility, no hard dependency |
| Vanilla Iron and Steel (Continued), 1.6 | Workshop `2644227855`, **actual 1.6 source at** https://github.com/emipa606/VanillaIronandSteel (`main`, `1.6/Defs`, `1.6/Patches`) inspected 2026-10-10; original Neceros historical source also available | Source has `NECIron`, `NECBloomery`, `NECForgeSteel` (ore + detected coal material → 10 Steel) and bulk Steel Recipes, including electric tiers. `1.6/Patches/Patch_Vanilla.xml` changes `MineableSteel`'s `mineableThing` to `NECIron`; `Patch_Coal.xml` uses named coal/charcoal alternatives. Thus **real early-smelting overlap is confirmed**. No inspected `1.6` source implementing a finite naturally deposited Japanese iron-sand resource, three historically pre-Edo furnace scales, or the optional MO iron-ingot exit. Loaded-game compatibility with MO/AMJ still untested | Strong prior-art / early-stage functional reuse candidate. Do not import globally replacing Vanilla mineables; choose independent narrow Japanese sand pathway subject to remaining candidate/source gate and license review |
| Expanded Materials - Metals, 1.6 | Workshop `3333419387`, current 1.6 description; historical public repository https://github.com/TheOriginalArgon/Expanded-Materials-Metals shows older 1.3/1.4 layout, **not certified current 1.6 source** | Adds multi-metal mining/refining, iron/coal/alloys and industrial-era materials; strong general metal supply overlap but far broader scope/dependencies than AMJ wants, and no verified Japanese region/tatara progression | **Material candidate; current source/compatibility unverified**. Likely prior art, not yet a production-entry conclusion |
| Original Japanese たたら製鉄 and later 1.6 compatibility | Original Workshop `1833556876` is marked 1.0 on 2game; later compatibility item `3815130352` identified in prior research | The original describes several ingot types and smelting in a single later-stage Japanese context; available descriptions are **not equivalent to actual XML inspection**, nor proof of 1.6 loaded compatibility | **Material candidate; package/patch source inspection pending**. Do not copy data or infer usage license |
| Prior generic alternatives, including Simple Chains: Steel / Rimworld Metallurgy | They are cited in Vanilla Iron and Steel compatibility notes, but not independently inspected for this entry | Potential broad metal-chain overlap; compare relevant current 1.6 sources if their mechanics are plausible replacements, rather than declaring absence | Search/refine in next source audit |

### Verified continued 1.6 file identifiers

- `1.6/Defs/RecipeDefs/Recipes_VIAS.xml`, GitHub blob `0f48c96824c54ddc5afdd7e060cbf626c024884b`: `NECForgeSteel` outputs 10 Steel from NECIron 10 plus one coal-type ingredient; higher-volume recipes output 100, 500 and 1,000 Steel in other worktable tiers.
- `1.6/Defs/ThingDefs_Buildings/VIAS_Production.xml`, blob `bdf14f8c06af402f453765cbd8c96790eab940bf`: `NECBloomery` built as `Building_WorkTable`, with `CompProperties_Refuelable`; recipe ingredient fuel is also present. This is a **potential dual fuel accounting interaction**, not a proved runtime bug.
- `1.6/Patches/Patch_Vanilla.xml`, blob `04c3ccf295cb0bb38d35d3cfc4b45bc2cf1e2bc9`: patches `MineableSteel` output to `NECIron` and adds Bloomery to a Vanilla smelting WorkGiver list.
- `1.6/Patches/Patch_Coal.xml`, blob `f901740c1b416b9e37bf7b124a2f175ced3645c4`: conditionally accepts defined coal-type materials for recipe and fuel filters; the build still requires a compatible external fuel supply.
- **Not established:** full effective Defs after unrelated Mods, runtime-only generated iron, MO coal interoperability, actual craft yields with dual fuel paths, or a Japanese sand-iron/medieval-tatara facility chain.

## Function/fit/dependency comparison

- **Reuse first:** Vanilla's Smithing, usable Steel and worktable Bill system; MO IronIngot/Coal only when MO is active; existing GenStep scatter machinery if cell weighting is sufficient.
- **Standalone reason:** the historical *sand-iron site → iron bloom → selectable small/improved/medieval production scale* is the differentiator; avoid globally replacing all rock/steel supply to force that loop.
- **Dependency risk:** a broad metal overhaul may introduce extra metal tiers and refit third-party recipes; using one for the single Japanese smelting loop is not automatically cheaper than a narrow standalone feature.
- **Retention and compatibility:** Ironmaking alone does not remove MO/Vanilla ore, trade or steel. Japanization integration conditionally balances MO-owned supply when Ironmaking is installed; a global trade lock is not an implicit Ironmaking feature.
- **Maintenance/license:** maintained 1.6 Vanilla Iron and Steel code is now inspected; remaining current 1.6 source/license verification concerns Expanded Materials - Metals, the tatara compatibility package, and any contemplated reuse. Inspect published terms before copying any upstream code. Linked upstream source is prior art, not authorized code to copy; the disposable probe below uses schema ideas only and is not production distribution.

## Disposable XML-only map-generation probe

A **local, unshipped experiment** defined `AMJ_IronSand`, a finite `AMJ_IronSandDeposit` mineable, `GenStep_ScatterThings` and a guarded `MapCommonBase` genSteps Patch, following known structural examples from MO 1.6. Five local offline `unittest` checks passed for XML parse, unique DefNames, deposit output, referenced GenStep, lack of MO dependency, and no infinite/deep mining. Sample map density, market value, graphics and Mineable class are **unapproved placeholders**. ZIP: `Ironmaking_IronSand_Research_Probe.zip` is a current-chat artifact, not included in a production repo.

**What this does NOT prove:** RimWorld 1.6 loading, active MapGenerator compatibility without MO, actual mineability, accessibility, river/coast weighting, safe map order, matching graphics, trade quantities, storage, gameplay fun, old-save handling, or compatibility with World Tech Level. `GenStep_ScatterThings` lacks proved precise river/coast selection; only use dedicated C# if the loaded XML route is inadequate.

## Production-entry gates and next evidence

1. **Vanilla Iron and Steel Continued 1.6 source inspected**. Continue with actual current Expanded Materials - Metals / tatara compatibility / VE relevant Def surfaces; where source access is missing, retain HOLD and do not invent current 1.6 behavior.
2. Record full candidate function, historical fit, dependencies, retained content, progression, reuse and maintenance/license observations in the canonical entry decision; leave unresolved questions explicit.
3. Owner repository created and design migrated here; Project retains pointers only. AGENTS and main-only authoritative Coordination govern follow-up development.
4. Add and validate a `status: ready` decision JSON with exact source note SHA-256 and valid owner path only after the evidence is ready. Do not mark the current entry gate ready merely because five isolated XML tests passed.
5. After owner setup, stage a minable/depletable sand-supply map-generation slice behind a PR; run static gates first, then appropriate noninteractive Pickle/RimTest and real loaded 1.6 tests.

## Sources checked

- [Vanilla Iron and Steel continued](https://steamcommunity.com/sharedfiles/filedetails/?id=2644227855), [maintained 1.6 source](https://github.com/emipa606/VanillaIronandSteel/tree/main/1.6), [original Neceros repository](https://github.com/Neceros/VanillaIronandSteel). Current 1.6 recipe, bench and mining XML inspected; no loaded-game evidence claimed.
- [Expanded Materials - Metals](https://steamcommunity.com/sharedfiles/filedetails/?id=3333419387), [historical source](https://github.com/TheOriginalArgon/Expanded-Materials-Metals).
- [VFE Medieval 2](https://steamcommunity.com/sharedfiles/filedetails/?id=3444347874).
- [Original Tatara](https://rimworld.2game.info/detail.php?id=1833556876) and [prior compatible item](https://steamcommunity.com/sharedfiles/filedetails/?id=3815130352).
- [Ironmaking design](../Design.md), [Ironmaking MVP checklist](IronmakingMVPImplementationChecklist.md), and Japanization's `Docs/Research/MedievalOverhaulJapanizationIronSupplyAudit.md`.
