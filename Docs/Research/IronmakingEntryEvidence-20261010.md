# Ironmaking implementation-entry evidence - 2026-10-10

Scope: bounded comparison for the approved feature "finite Japanese iron-sand deposits and early/improved/medieval smelting as a standalone RimWorld 1.6 Mod." This is a source/description audit, not a complete loaded-game Mod comparison. No third-party XML, binary or art will be copied.

Searches performed 2026-10-10: RimWorld 1.6 iron sand tatara, sand-iron furnace, smelting bloomery/ore-to-steel, Japanese tatara 1.6, VE Medieval 2 smithing; English and Japanese; GitHub maintained source, Workshop and 2game/Mod databases. Excluded results from Minecraft and Oxygen Not Included by game identity.

VANILLA / MO
- Vanilla already supplies a Smithing research/building/Bill and final Steel resource; no independent finite Japanese sand deposit chain was identified in reviewed Vanilla source context. Actual installed Core 1.6 trader and resource values have not been verified.
- Supplied Medieval Overhaul 1.6 package 3219596926.zip adds IronOre, IronIngot, Coal, Smelter, Mine Shaft, ore veins, golem rocks, deep ore/ingot candidates, and direct ingot switches with metalChain OFF. The author supplied XML was inspected in prior Project and Japanization audits. MO as a mandatory dependency violates standalone Vanilla support. MO integration must remain optional and must not destroy MO mineables/traders.
- MO static audit canonical reference: https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Medieval-Overhaul-Japanization/blob/main/Docs/Research/MedievalOverhaulJapanizationIronSupplyAudit.md

AMJ
- Project Architecture assigns region/environment terrain to Environment; Ironmaking owns extraction and its iron-sand Defs, and Japanization owns additional MO-side resource/trader corrections when it is installed.
- Ironmaking design: Docs/Design.md. Project pointers: https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Roadmap.md
- No implemented AMJ standalone sand-iron/tatara chain is reused from other AMJ owners.

VE
- Vanilla Factions Expanded - Medieval 2 Workshop 3444347874, 1.6 source https://github.com/Vanilla-Expanded/VanillaFactionsExpanded-Medieval2/tree/main/1.6
- Confirmed 1.6 Linkable Defs VFEM2_SmithingAnvil and VFEM2_ForgeBellows from Buildings_Linkable.xml (blob 8f44a3ded54d5bb133bb046212e965ea8881e63d). Bellows advertises a 20% linked bench fuel reduction. Production and Recipes_Production XML inspected, no full finite Japanese sand/bloom/tatara progression established in examined files. A broad faction/technology Mod plus VEF is too much to require for this feature; optional linkable compatibility only.
- Workshop: https://steamcommunity.com/sharedfiles/filedetails/?id=3444347874
- Caution: no exhaustive analysis of all external VE C# or patches; absence from inspected files is not proof of universal nonexistence.

NON-VE
- Vanilla Iron and Steel (Continued), Workshop 2644227855, 1.6 source: https://github.com/emipa606/VanillaIronandSteel/tree/main/1.6 . Inspected 1.6 Recipes_VIAS.xml, VIAS_Production.xml, Patch_Vanilla.xml, Patch_Coal.xml. Provides NECIron and NECBloomery with ore+fuel -> Steel, but changes Vanilla MineableSteel output globally. It overlaps generic bloomery functionality, NOT the deliberately additive finite Japanese sand deposits and tiers. A forced dependency plus undoing the global ore conversion is worse than a focused independent Mod.
- Simple Chains: Steel, old upstream https://github.com/Owlchemist/simple-chains-steel (About advertises 1.2, 1.3, 1.4, NOT proven 1.6). Inspected Defs/RecipeDefs/Recipes_Production.xml, Buildings_Production.xml, and Patch XML. Ore+coal -> Steel at Owl_Bloomery, global MineableSteel -> Owl_Iron patch. This is generic ore transformation, not a low-impact local iron-sand system. Upstream functionality is prior art; current 1.6 port is unverified.
- Expanded Materials - Metals: https://steamcommunity.com/sharedfiles/filedetails/?id=3333419387 . Current 1.6 Workshop declares required Argonic Core and Vanilla Expanded Framework; broad multi-metal/alloy/advanced refining system. https://github.com/TheOriginalArgon/Expanded-Materials-Metals exposes 1.3/1.4 source, not verified 1.6 XML. Too many unrelated mandatory dependencies and systems for the one narrow Japanese route. No claim about hidden 1.6 RecipeDefs.
- Original Japanese tatara (old 1.0): https://rimworld.2game.info/detail.php?id=1833556876 . Rice cultivating civilization 1.6 https://steamcommunity.com/sharedfiles/filedetails/?id=3046830338 includes tatara thematically, but requires the broader crop/food/brewing ecosystem. Exact currently loaded 1.6 tatara XML not inspected. Earlier workshop ID 3815130352 has no verified tatara identity and is not treated as compatibility evidence.
- Progression: Production 1.6, https://rimworld.2game.info/detail.php?id=3453408412 : requires ReplaceLib and shifts MO/VE research prerequisites, including iron smelting. It is not a finite sand-iron resource generation and independent furnace system; optional research-order prior art only.

DECISION REASONING
- Use Vanilla Smithing/Bills/final Metal rather than duplicating generic forging mechanics.
- Do not modify other Mods' mineables or merchants from standalone Ironmaking merely to force Japanese production. Ironmaking resources and jobs must be independently useful while coexistence remains intact.
- Existing Mods either globally substitute ore, bundle a large economy/era/crop pack, or only supplement smithing/research. Requiring any of them would violate the documented Vanilla-only and narrow owner boundaries. A limited new iron-sand path therefore has a concrete implementation gap.
- No present evidence of a minimal, optional-dependency-free 1.6 Mod that supplies all the specified finite localized sand deposit, early/intermediate/medieval Japanese furnace and MO optional exit. This is a bounded 2026-10-10 search conclusion, not universal proof of absence.
- No source code or assets licensed by others are reused; consult original license before adopting any upstream data.

LIMITS FOR LATER COMPATIBILITY
Current 1.6 Expanded Materials - Metals and 1.6 rice/tatara executable Defs not acquired. This is not material to selecting them as mandatory bases because their publicly documented unavoidable scope/dependency conflicts disqualify them. Loaded-game compatibility, final patched Def results, balancing, trader volumes, graphics and all 1.6 runtime behaviors remain separate test/release gates, NOT claims of completion here.
