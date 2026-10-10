# Ironmaking Coordination

**Authoritative branch:** `main` only. This is an inter-workstream task/status log; specifications belong in `Docs/Design.md`. Do not maintain other copies.

## IRON-OWNER-20261010 — Design ownership migration
**State:** DESIGN MIGRATED (historical 2026-10-10 stage); later MVP source and Vanilla E2E PASS are recorded below.  
Project's pre-split design, MVP checklist and prior-art review are moved to Ironmaking's formal sources. The initial root README commit was `6f8d8cb8e2b5298c170762d1b8ec56dfcfffcd5a`. Project copies are historical link stubs after its subsequent PR.

## IRON-ENTRY-20261010 — Prior-art gate
**State:** ENTRY DECISION RECORDED; implementation proceeds only by bounded PRs; subsequent Vanilla 5-scenario loaded E2E passed but unrelated game/release gates remain open.  
Vanilla Iron and Steel Continued 1.6 overlaps bloomery/ore-to-Steel. VE, non-VE, Vanilla/MO and AMJ alternatives were compared for minimal dependency and non-destructive finite sand supply. Owner `Docs/Research/IronmakingEntryDecision.json` is `ready`, with a matching SHA-256 evidence file and an independently executed equivalent schema/hash check. The Project validator Python file itself was not executed in this chat; this is not a game-load PASS. Source: `Docs/Research/IronmakingExistingModEntryAudit-20261010.md`.

## IRON-MVP-20261010 — Upcoming owner work
**State:** BASIC DEV XML SOURCE EXISTS; VANILLA NATURAL MAPGEN / MINING / SAVE PICKLE PASS; PRODUCTION BILLS AND MO OPEN.  
First finite iron-sand deposit ThingDef + GenStep XML developer slice was added after the entry decision, plus twelve static tests (local PASS after limited trader addition). Charcoal kiln, small furnace, bloom, and common-metal finish now have developer XML definitions plus a guarded MO IronIngot Patch. Limited sand-iron seller/buyer stock XML has been added to two optional Vanilla caravan TraderKinds; research, improved/medieval furnaces, region weighting and accepted textures are not implemented; Vanilla Pickle 5/5 later confirmed natural map deposits, loaded Recipes and real mining WorkGiver; actual recipe Bill execution remains untested. The old 5-test research probe is not the loaded-game validation. Future validation must cover actual crafting Bills/fuel once, MO profile, trading, research and terrain distribution; the five Vanilla scenarios already passed mining and save/reload. Runtime/test design: `Docs/Research/IronmakingMVPImplementationChecklist.md`.

## MOJ-IRON-INTERFACE-20261010
**State:** INTERFACE CONTRACT DELIVERED; Japanization runtime adapter pending.  
Ironmaking `About/About.xml` now has packageId `sucro.ancientmedievaljapan.ironmaking` and `Docs/Design.md` records its live developer DefNames. The owner MO compatibility Patch routes `AMJ_ForgeIronBloom` to `DankPyon_Anvil` → `DankPyon_IronIngot` and accepts `DankPyon_Coal`. Japanization [PR #4](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Medieval-Overhaul-Japanization/pull/4), merged commit `a019a43bf1d26abf906b16266262d134410a8425`, formally received the interface. Its additional MO mining/Mine Shaft/deep/trader/research rebalancing is not yet implemented or tested; keep source ownership separate and do not imply loaded-game PASS.

## IRON-MO-SOURCE-CONTRACT-20261010

**State:** STATIC UPSTREAM XML CHECK PASS; loaded-game behavior OPEN.  
Optional `AMJ_MO_ARCHIVE` test reads the author's actual MO 1.6 ZIP. All 15 tests passed with it; normal suite has 12 passes + 3 explicit skips without the archive. Checked mod name/packageId, upstream Anvil/Coal/IronIngot Defs, and Ironmaking conditional output. Fixed the verifier's stale local About copy; GitHub About was already correct. This does **not** verify executed RimWorld patches or MO gameplay. Source contract and command in `Docs/GoldenPaths/IronSandStaticAudit.md`.

## IRON-CORE-CATEGORY-20261010 — Vanilla source reference repair

**State:** STATIC DEF PARENT CORRECTED; reported Vanilla 5-scenario game E2E now PASS, actual Core XML audit independently remains open.

The first Ironmaking `ThingCategoryDef AMJ_IronmakingMaterials` used a `Resources` parent not found in the checked Vanilla category tree. Changed to known `Root`, without joining `ResourcesRaw` or changing iron-sand trade/vanilla stock. Added a nested `Patches/**/*.xml` parsing regression in the owner's structural test. The rationale/procedure lives in `Docs/Design.md` and `Docs/GoldenPaths/IronSandStaticAudit.md`; this entry is only the status handoff.

## IRON-PICKLE-20261010 — Isolated live-game automated test harness

**State:** VANILLA GAME E2E 5/5 PASS (author-run 2026-10-10); MO PROFILE OPEN.

Five test-only Pickle scenarios now target loaded Defs and Vanilla/MO result, a naturally spawned map deposit, a pawn mining job and real save/reload. The runner stages owner-marked temporary Mods and isolated SaveData, requiring complete Pickle summary/ERROR-free Player.log; normal ModsConfig/Prefs and Steam installs must remain unchanged. Author reports real Vanilla Pickle 5/5 PASS (run `b5a5596f84`, 0 skipped/flaky/error logs). Full log files are local to the author's PC and not independently re-opened in this chat. MO profile has not been reported; worktable Bill execution is not among the five steps. Owner procedure: `Docs/GoldenPaths/IronmakingPickleE2E.md`.

## IRON-PICKLE-HIDDEN-TEX-20261010 — Isolated display and charcoal texture fix

**State:** CHARCOAL TEXTURE FIX VERIFIED BY AUTHOR'S VANILLA PICKLE 5/5 RUN; MO STILL OPEN.

Author-run Vanilla Pickle aborted on a real `[ERROR]`: `AMJ_Charcoal` borrowed Vanilla Chemfuel's texture but used `Graphic_StackCount`, causing the nonexistent `Things/Item/Resource/Chemfuel/Chemfuel` lookup and a null material. The owner ThingDef switches to Chemfuel-compatible `Graphic_Single` and an explicit regression checks the pair. The default Pickle launcher now requires a private Windows `WinSta0` desktop and fails closed if native launcher building/desktop creation fails; rendering is not disabled and no visible fallback is allowed. Historical failed run is not a PASS. After the charcoal texture correction, author's Vanilla run `b5a5596f84` completed 5/5 with no logged errors; the remaining baseline evidence is MO profile 5/5. Procedure/specification is in `Docs/GoldenPaths/IronmakingPickleE2E.md`, code in `Defs/ThingDefs/IronmakingMaterials.xml` and `Scripts/`.

## IRON-PICKLE-ALL-MO-TRANSITION-20261010

**State:** Vanilla 5/5 verified; author reported no console output after Vanilla during `--profile All`, MO not yet confirmed. Source-level diagnosis: old Python runner used blocking `subprocess.run` for each hidden game profile without MO launch/heartbeat messages. The separate MO load could therefore appear frozen for the full timeout even if still running. Updated owner runner and its Golden Path with explicit profile start, 15-second MO log/report heartbeat, fail-closed deadline, and owned-process-tree cleanup on timeout/interruption. See `Scripts/pickle_run_monitor.py` and `Docs/GoldenPaths/IronmakingPickleE2E.md` for implementation/diagnosis; **no fresh MO runtime outcome has been observed here**. Remaining run is MO-only, not a mandatory replay of Vanilla.

## IRON-MO-HIDDEN-STARTUP-20261010 — timeout evidence and investigation

**State:** MO actual game TIMED OUT at 900s (run `10f8fe08ce`); root cause OPEN, Pickle 5/5 unexecuted/undetermined.  
Uploaded `launcher.log` confirms private-desktop PID=15988 and native timeout. `Player.log` contains startup/graphics initialization, installed-Mod metadata warnings and two Mono fallback-library lines, but no Pickle scenarios or explicit terminal cause. No missing-mod/Recipe/Unity crash diagnosis is asserted from these lines. The owner test launcher now records 30-second private-window/CPU/memory snapshots and bounded failed-run log tails for the next MO-only diagnostic attempt. The procedure/evidence scope belongs in `Docs/GoldenPaths/IronmakingPickleE2E.md`; no production XML or compatibility/balance changes are authorized by the timeout alone.

## IRON-MO-STARTUP-DIFFERENTIAL-20261010

**State:** TWO-PROFILE ISOLATED STARTUP DIAGNOSTIC IMPLEMENTED; actual comparison observations pending. After 900s and 180s hidden MO sessions without Pickle completion, the separate read-only diagnostic tool compares `MO-Baseline` (Harmony/Core/VEF/Processor/MO) against `MO-Pickle` (same + RimLogging/Pickle/Quickstarts). Neither loads Ironmaking or asserts Pickle success. Only the test harness/procedure changes; native game state stays isolated. Detailed commands, output paths and interpretation limits in `Docs/GoldenPaths/IronmakingPickleE2E.md`. No production XML, MO compatibility patch or E2E PASS record changed.
