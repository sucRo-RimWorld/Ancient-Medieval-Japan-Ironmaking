# Ironmaking Coordination

**Authoritative branch:** `main` only. Specifications: `Docs/Design.md`.

## IRON-MVP-20261010
**State:** BASIC DEV XML AND INITIAL RESEARCH GATE IMPLEMENTED; remaining gameplay and release work OPEN.
Finite sand deposits/mapgen, charcoal kiln, small furnace, bloom finishing,
limited optional Vanilla caravan stock and MO IronIngot/Anvil compatibility exist.
Initial research `AMJ_InitialIronmaking` (after `Smithing`) gates the AMJ furnace
and smelting Bill; MO tab routing is optional. Ironmaking PR #34, merge
`ba627a3ced00fea0e166df83bd785d232431971a`; PR-head and main-push static CI
succeeded. Research cost 600 and UI coordinates are provisional; loaded research
layout, completed progress, and old-save behavior remain unverified.
Entry decision is ready; canonical evidence: `Docs/Research/IronmakingEntryDecision.json`
and its prior-art note. Improved/medieval furnaces, region weighting,
balance and accepted textures remain unimplemented/unaccepted. Static checks do
not establish new loaded-game evidence. Updated test contract and pending
coverage: `Docs/Testing/IronmakingV1Coverage.md`. See MVP checklist and Design
for scope.

## IRON-PICKLE-20261010
**State:** CURRENT SOURCE 10 CORE + 7 PRODUCTION PER VANILLA/MO;
ALL REVISED NATIVE COMPILATION AND REAL-GAME VALIDATION OPEN.
Historical pre-research RimWorld 1.7.4976 rev1043 source
`1af461eac9d6b1326975a9866593d694f5d291f5` plus test-only corrections
passed **5 Core / 4 Production** per Vanilla/MO (PID complete/ERROR0).
Evidence: `Docs/Testing/Native17-20261013.json`.
These old passes must NOT be inherited by current research, new map, or
stock-generation scenarios.

Current test source evolved in PRs #36/#38/#40/#41. PR #43 merged
`2281f2992aa7a62913dd643f36d689592c500e92` adds direct
loaded `StockGenerator.GenerateThings` assertions: only AMJ sand, positive
configured stock count and buyer HandlesThingDef. It is NOT an actual spawned
merchant inventory or trade UI. PR #44 merged
`733b20f151820232aec3f7aeaaed79f34377db2a` upgrades research
verification to RimWorld's own furnace `IsResearchFinished` and smelting
`AvailableNow` gates before Smithing, after Smithing alone and after initial
AMJ research, preserving charcoal before/after. Exact-head and main-push
source/runner GitHub CI PASS; no native C# test compilation/game execution.
The current Gherkin feature files now define **10 named Core and 7 named
Production** scenarios per Vanilla/MO. The strict Python result gate and
binding unit tests enforce these definitions, not gameplay correctness.
Canonical premises/gaps:
`Docs/Testing/IronmakingV1Coverage.md`.

**Still OPEN:** actual pre-mod save add/remove/re-add, across-save or fuel-loss
job interruption and full haul/refuel pipeline, actual merchant arrival/
trade transaction on sand-poor and old maps, Architect/research UI, multiple
Seed/biome regional weighting, MO configuration and Japanization adapter,
economic numbers, graphics, release. Shared native game host work is paused
by Project `main:Docs/Coordination.md` DEV-PERSISTENT-RIMWORLD-HOST;
do NOT run or represent chat-local game tests as current evidence.

## MOJ-IRON-INTERFACE-20261010
**State:** CONTRACT DELIVERED; Japanization runtime adapter OPEN.
PackageId and live DefNames are in Design. Japanization PR #4, merge
`a019a43bf1d26abf906b16266262d134410a8425`, received the optional interface.
MO mining/Mine Shaft/deep/trader/research rebalancing belongs to Japanization and
remains unimplemented/untested; Ironmaking does not blanket-change those sources.

## IRON-MO-SOURCE-CONTRACT-20261010
**State:** UPSTREAM XML CHECK PASS; Core-source-independent audit remains OPEN.
Actual MO 1.6 archive contract checks passed previously (15 tests with archive;
12 passes + 3 explicit skips without it). Core category parent corrected to Root;
actual Vanilla Core XML audit independently remains open. Source procedure:
`Docs/GoldenPaths/IronSandStaticAudit.md`. No trade/setting-variant runtime claims.
