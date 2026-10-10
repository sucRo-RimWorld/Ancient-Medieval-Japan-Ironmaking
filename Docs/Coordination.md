# Ironmaking Coordination

**Authoritative branch:** `main` only. This is an inter-workstream task/status log; specifications belong in `Docs/Design.md`. Do not maintain other copies.

## IRON-OWNER-20261010 — Design ownership migration
**State:** MIGRATED DESIGN / NOT IMPLEMENTED.  
Project's pre-split design, MVP checklist and prior-art review are moved to Ironmaking's formal sources. The initial root README commit was `6f8d8cb8e2b5298c170762d1b8ec56dfcfffcd5a`. Project copies are historical link stubs after its subsequent PR.

## IRON-ENTRY-20261010 — Prior-art gate
**State:** ENTRY DECISION RECORDED; implementation proceeds only by bounded PRs and remains unverified in game.  
Vanilla Iron and Steel Continued 1.6 overlaps bloomery/ore-to-Steel. VE, non-VE, Vanilla/MO and AMJ alternatives were compared for minimal dependency and non-destructive finite sand supply. Owner `Docs/Research/IronmakingEntryDecision.json` is `ready`, with a matching SHA-256 evidence file and an independently executed equivalent schema/hash check. The Project validator Python file itself was not executed in this chat; this is not a game-load PASS. Source: `Docs/Research/IronmakingExistingModEntryAudit-20261010.md`.

## IRON-MVP-20261010 — Upcoming owner work
**State:** SAND-DEPOSIT STATIC SOURCE ADDED; FURTHER MVP MODULES PENDING.  
First finite iron-sand deposit ThingDef + GenStep XML developer slice was added after the entry decision, plus twelve static tests (local PASS after limited trader addition). Charcoal kiln, small furnace, bloom, and common-metal finish now have developer XML definitions plus a guarded MO IronIngot Patch. Limited sand-iron seller/buyer stock XML has been added to two optional Vanilla caravan TraderKinds; research, improved/medieval furnaces, region weighting and accepted textures are not implemented; none of the new Recipes/WorkGivers have passed a real RimWorld loaded-game test. The old 5-test research probe is not the loaded-game validation. Verify mining reachability, save behavior, no refuel/bill double consumption and optional MO entry. Runtime/test design: `Docs/Research/IronmakingMVPImplementationChecklist.md`.

## MOJ-IRON-INTERFACE-20261010
**State:** INTERFACE CONTRACT DELIVERED; Japanization runtime adapter pending.  
Ironmaking `About/About.xml` now has packageId `sucro.ancientmedievaljapan.ironmaking` and `Docs/Design.md` records its live developer DefNames. The owner MO compatibility Patch routes `AMJ_ForgeIronBloom` to `DankPyon_Anvil` → `DankPyon_IronIngot` and accepts `DankPyon_Coal`. Japanization [PR #4](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Medieval-Overhaul-Japanization/pull/4), merged commit `a019a43bf1d26abf906b16266262d134410a8425`, formally received the interface. Its additional MO mining/Mine Shaft/deep/trader/research rebalancing is not yet implemented or tested; keep source ownership separate and do not imply loaded-game PASS.

## IRON-MO-SOURCE-CONTRACT-20261010

**State:** STATIC UPSTREAM XML CHECK PASS; loaded-game behavior OPEN.  
Optional `AMJ_MO_ARCHIVE` test reads the author's actual MO 1.6 ZIP. All 15 tests passed with it; normal suite has 12 passes + 3 explicit skips without the archive. Checked mod name/packageId, upstream Anvil/Coal/IronIngot Defs, and Ironmaking conditional output. Fixed the verifier's stale local About copy; GitHub About was already correct. This does **not** verify executed RimWorld patches or MO gameplay. Source contract and command in `Docs/GoldenPaths/IronSandStaticAudit.md`.

## IRON-CORE-CATEGORY-20261010 — Vanilla source reference repair

**State:** STATIC DEF PARENT CORRECTED; actual loaded RimWorld 1.6/Core and gameplay still unverified.

The first Ironmaking `ThingCategoryDef AMJ_IronmakingMaterials` used a `Resources` parent not found in the checked Vanilla category tree. Changed to known `Root`, without joining `ResourcesRaw` or changing iron-sand trade/vanilla stock. Added a nested `Patches/**/*.xml` parsing regression in the owner's structural test. The rationale/procedure lives in `Docs/Design.md` and `Docs/GoldenPaths/IronSandStaticAudit.md`; this entry is only the status handoff.

## IRON-PICKLE-20261010 — Isolated live-game automated test harness

**State:** E2E HARNESS AUTHORED; RimWorld/Pickle game execution and .NET test build OPEN.

Five test-only Pickle scenarios now target loaded Defs and Vanilla/MO result, a naturally spawned map deposit, a pawn mining job and real save/reload. The runner stages owner-marked temporary Mods and isolated SaveData, requiring complete Pickle summary/ERROR-free Player.log; normal ModsConfig/Prefs and Steam installs must remain unchanged. Four fixture checks of the exact result validator passed; no real game or MO profile E2E was run in this environment. Owner procedure: `Docs/GoldenPaths/IronmakingPickleE2E.md`.

## IRON-PICKLE-HIDDEN-TEX-20261010 — Isolated display and charcoal texture fix

**State:** SOURCE FIX / LOCAL STRUCTURAL CHECKS; fresh loaded-game retest still required.

Author-run Vanilla Pickle aborted on a real `[ERROR]`: `AMJ_Charcoal` borrowed Vanilla Chemfuel's texture but used `Graphic_StackCount`, causing the nonexistent `Things/Item/Resource/Chemfuel/Chemfuel` lookup and a null material. The owner ThingDef switches to Chemfuel-compatible `Graphic_Single` and an explicit regression checks the pair. The default Pickle launcher now requires a private Windows `WinSta0` desktop and fails closed if native launcher building/desktop creation fails; rendering is not disabled and no visible fallback is allowed. Historical failed run is not a PASS. Next required evidence is fresh actual Vanilla then MO Pickle reports and ERROR-free player logs. Procedure/specification is in `Docs/GoldenPaths/IronmakingPickleE2E.md`, code in `Defs/ThingDefs/IronmakingMaterials.xml` and `Scripts/`.
