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
| Vanilla Factions Expanded - Medieval 2 (VE), 1.6 | [Official 1.6 source](https://github.com/Vanilla-Expanded/VanillaFactionsExpanded-Medieval2/tree/main/1.6) inspected: `Defs/ThingDefs_Buildings/Buildings_Linkable.xml` (`VFEM2_SmithingAnvil`, `VFEM2_ForgeBellows`), plus Production/RecipeDefs/Research XML | `VFEM2_ForgeBellows` is a smithy linkable (speed benefit and declared **20% lower fuel use**); anvil boosts smithing. This is genuine overlap in **forge support**, not demonstrated independent regional sand-iron source, bloom-to-iron process or tiered pre-Edo tatara system in examined files. VFE remains a major faction/tech content dependency | **Prior-art + optional Linkable compatibility**, not a hard dependency; do not copy VFE assets/defs or silently alter its fuel accounting |
| Vanilla Iron and Steel (Continued), 1.6 | Workshop `2644227855`, **actual 1.6 source at** https://github.com/emipa606/VanillaIronandSteel (`main`, `1.6/Defs`, `1.6/Patches`) inspected 2026-10-10; original Neceros historical source also available | Source has `NECIron`, `NECBloomery`, `NECForgeSteel` (ore + detected coal material → 10 Steel) and bulk Steel Recipes, including electric tiers. `1.6/Patches/Patch_Vanilla.xml` changes `MineableSteel`'s `mineableThing` to `NECIron`; `Patch_Coal.xml` uses named coal/charcoal alternatives. Thus **real early-smelting overlap is confirmed**. No inspected `1.6` source implementing a finite naturally deposited Japanese iron-sand resource, three historically pre-Edo furnace scales, or the optional MO iron-ingot exit. Loaded-game compatibility with MO/AMJ still untested | Strong prior-art / early-stage functional reuse candidate. Do not import globally replacing Vanilla mineables; choose independent narrow Japanese sand pathway subject to remaining candidate/source gate and license review |
| Expanded Materials - Metals, 1.6 | [Workshop 3333419387](https://steamcommunity.com/sharedfiles/filedetails/?id=3333419387) confirms 1.6, **Argonic Core + Vanilla Expanded Framework** required. [Author GitHub](https://github.com/TheOriginalArgon/Expanded-Materials-Metals) contains only 1.3/1.4 source, not reviewed current 1.6 XML | Current description advertises iron/coal/alloys and broad refinement; old 1.4 Defs include iron mineables/charcoal/alloy furnaces and Vanilla Steel generation changes. Current 1.6 DefNames/final patches remain unverified. Mandatory frameworks and numerous other resources are outside a minimal Vanilla-only Japanese sand/medieval furnace loop | **Prior art, not core dependency.** Optional interoperability after installed source is inspected. Never copy outdated source assuming it matches 1.6 |
| Original Japanese たたら製鉄 and 1.6 rice-integrated lineage | [Original Tatara 1833556876](https://rimworld.2game.info/detail.php?id=1833556876) is old RimWorld 1.0. [Rice cultivating civilization 3046830338](https://steamcommunity.com/sharedfiles/filedetails/?id=3046830338) publicly lists 1.6 and requires Harmony, but also bundles rice/crop/food/brewing content and states no redistribution. Previous ID `3815130352` is **not verified** as a tatara compatible port | Historical Japanese smelting exists as thematic overlap, but the current integrated tatara Defs have not been inspected. A large agricultural Mod is not a narrow dependency-free Japanese ironmaking alternative and would retain unrelated features; do not assert missing mechanics just because its files are inaccessible | **Historical prior art / standalone dependency rejected.** Optional comparison only, no redistribution or XML/art reuse |
| Prior generic alternatives, including Simple Chains: Steel / Rimworld Metallurgy | They are cited in Vanilla Iron and Steel compatibility notes, but not independently inspected for this entry | Potential broad metal-chain overlap; compare relevant current 1.6 sources if their mechanics are plausible replacements, rather than declaring absence | Search/refine in next source audit |

### Verified VFE Medieval 2 1.6 source identifiers

- Official repo: https://github.com/Vanilla-Expanded/VanillaFactionsExpanded-Medieval2 (RimWorld `1.6` tree).
- `1.6/Defs/ThingDefs_Buildings/Buildings_Linkable.xml`, source blob `8f44a3ded54d5bb133bb046212e965ea8881e63d`: `VFEM2_SmithingAnvil` and `VFEM2_ForgeBellows`. The bellows description declares a **20% reduction of linked-workbench fuel consumption**; that number is an upstream text value, not an AMJ balance assumption or independently tested runtime result.
- `1.6/Defs/RecipeDefs/Recipes_Production.xml`, blob `6aea7996aecc0d09e9dd8c4762cd6a0be0d516d4`; `1.6/Defs/ThingDefs_Buildings/Buildings_Production.xml`, blob `f337d7faaa43f2e369539ce35e857a0cf18f6030`; `1.6/Defs/ResearchProjectDefs/ResearchProjects_Various.xml`, blob `33f38c5e0eb8925d02cbd61c76fb6ca4a579d7c7`. In these inspected files no stand-alone Japanese iron-sand / medieval tatara supply-and-smelting sequence was established. **Not proof of nonexistence across every C# system or third-party patch.**
- VFE machinery is a possible optional efficiency addition after independent small-furnace gameplay exists, provided AMJ's bill-fuel consumption cannot be accidentally double-discounted or combined with Refuelable consumption.
  
### Verified continued 1.6 file identifiers

- `1.6/Defs/RecipeDefs/Recipes_VIAS.xml`, GitHub blob `0f48c96824c54ddc5afdd7e060cbf626c024884b`: `NECForgeSteel` outputs 10 Steel from NECIron 10 plus one coal-type ingredient; higher-volume recipes output 100, 500 and 1,000 Steel in other worktable tiers.
- `1.6/Defs/ThingDefs_Buildings/VIAS_Production.xml`, blob `bdf14f8c06af402f453765cbd8c96790eab940bf`: `NECBloomery` built as `Building_WorkTable`, with `CompProperties_Refuelable`; recipe ingredient fuel is also present. This is a **potential dual fuel accounting interaction**, not a proved runtime bug.
- `1.6/Patches/Patch_Vanilla.xml`, blob `04c3ccf295cb0bb38d35d3cfc4b45bc2cf1e2bc9`: patches `MineableSteel` output to `NECIron` and adds Bloomery to a Vanilla smelting WorkGiver list.
- `1.6/Patches/Patch_Coal.xml`, blob `f901740c1b416b9e37bf7b124a2f175ced3645c4`: conditionally accepts defined coal-type materials for recipe and fuel filters; the build still requires a compatible external fuel supply.
- **Not established:** full effective Defs after unrelated Mods, runtime-only generated iron, MO coal interoperability, actual craft yields with dual fuel paths, or a Japanese sand-iron/medieval-tatara facility chain.

## Provisional implementation choice — narrow independent Mod

The requested *finite regional sand iron → early/improved/medieval Japanese smelting → usable general metal* loop is not identical to ordinary generic ore→Steel smelting. **The independence justification is specific to gameplay and dependency boundaries, not cultural labels alone.**

- Vanilla Iron and Steel Continued provides a real 1.6 bloomery and smelting path but globally redirects Vanilla `MineableSteel`; Ironmaking must not override other ore sources merely to force its Japanese route.
- Expanded Materials - Metals has confirmed framework dependencies and an extensive metallurgy economy; reusing it as mandatory would violate the approved standalone boundary. Current 1.6 Def details are not verified from the older repository.
- Rice cultivating civilization includes Japanese period-themed processing in a large agricultural system. Making it mandatory imports many unrelated systems; 1.6 tatara Recipe/ThingDefs remain uninspected, and the item prohibits redistribution.
- VFE Medieval 2 presents medieval forge/bellows prior art, but a whole faction-and-technology extension is not a narrow optional-free finite Japanese iron-sand producer. Reuse Vanilla worktable/Smithing machinery and examine VE equipment only for optional compatibility.

**Provisional conclusion:** a small independent Ironmaking is justified over a large forced dependency or a global ore rewrite. **Still HOLD for production**: complete bounded current VE/non-VE comparisons and the owner-local evidence-hash decision record checked by the Project validator. No candidate's inaccessible 1.6 XML is asserted not to contain a particular recipe.

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

1. Vanilla Iron and Steel Continued 1.6 XML was inspected. Expanded Materials - Metals and rice-integrated Tatara have current 1.6 public descriptions and dependency evidence, but their active XML is uninspected. Their broad required dependencies disqualify them as **baseline** Ironmaking sources. Continue focused 1.6 checks for low-dependency sand/tatara equivalents and VE mechanic overlap without inventing negative facts.
2. Record full candidate function, historical fit, dependencies, retained content, progression, reuse and maintenance/license observations in the canonical entry decision; leave unresolved questions explicit.
3. Owner repository created and design migrated here; Project retains pointers only. AGENTS and main-only authoritative Coordination govern follow-up development.
4. Add and validate a `status: ready` decision JSON with exact source note SHA-256 and valid owner path only after the evidence is ready. Do not mark the current entry gate ready merely because five isolated XML tests passed.
5. After owner setup, stage a minable/depletable sand-supply map-generation slice behind a PR; run static gates first, then appropriate noninteractive Pickle/RimTest and real loaded 1.6 tests.

## Sources checked

- [Vanilla Iron and Steel continued](https://steamcommunity.com/sharedfiles/filedetails/?id=2644227855), [maintained 1.6 source](https://github.com/emipa606/VanillaIronandSteel/tree/main/1.6), [original Neceros repository](https://github.com/Neceros/VanillaIronandSteel). Current 1.6 recipe, bench and mining XML inspected; no loaded-game evidence claimed.
- [Expanded Materials - Metals 1.6 Workshop](https://steamcommunity.com/sharedfiles/filedetails/?id=3333419387), [historical GitHub source (1.3/1.4)](https://github.com/TheOriginalArgon/Expanded-Materials-Metals).
- [VFE Medieval 2](https://steamcommunity.com/sharedfiles/filedetails/?id=3444347874).
- [Original 1.0 Tatara](https://rimworld.2game.info/detail.php?id=1833556876) and [current 1.6 rice-integrated successor](https://steamcommunity.com/sharedfiles/filedetails/?id=3046830338). Earlier `3815130352` identity remains unverified.
- [Ironmaking design](../Design.md), [Ironmaking MVP checklist](IronmakingMVPImplementationChecklist.md), and Japanization's `Docs/Research/MedievalOverhaulJapanizationIronSupplyAudit.md`.
