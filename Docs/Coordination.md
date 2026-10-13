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
**State:** REVISED TEST DEFINITIONS MERGED; CURRENT-SOURCE GAME COMPILATION/RUN OPEN.
Historical RimWorld 1.7.4976 rev1043 Vanilla/MO Core **5/5** and Production
**4/4** per profile were independently verified against pre-research production
source `1af461eac9d6b1326975a9866593d694f5d291f5` with test-only fixes:
complete PID logs, ERROR0, no skips/flaky. Exact evidence:
`Docs/Testing/Native17-20261013.json`. Earlier author-provided 1.6 results
remain separate historical evidence; neither proves new source behavior.

Test-contract cleanup PR #36 merged `eda362ea1f8f2df5e82e54d1c11a1c38bb33527e`.
Current safety coverage PR #38 merged `22bf454e2a440136006f46302259d70a9ed7aca6`;
source/runner GitHub CI PASS on exact PR head. The **current**
`ironmaking-core.feature` and `ironmaking-production.feature` contain **7
named scenarios each**, per Vanilla/MO profile, all requiring newly compiled
native E2E evidence. Newly exercised source assertions: unsatisfied/satisfied
initial-research gate, actual loaded sand seller/buyer generators (not
merchant stock), loaded no-double-fuel components, alternate MO Coal Bill,
and interrupted native smelting retry with exact one-batch accounting.
`Scripts/validate_pickle_result.py` enforces each full named suite; feature/
C# step bindings are statically checked. No new native assembly compile or
real-game PASS is claimed. Historical MO-startup differential diagnostic is
opt-in only.

**Remaining OPEN:** actual old-save add/remove/re-add, across-save/fuel-loss
interruption, full hauling/refuelling logistics, generated trader inventory
and low-sand import, research designator UI, several Seed/biome regional
weight profiles, MO metalChain/vanillaMine settings and Japanization adapter,
balance, accepted textures and release. Actual owners, expected behavior,
test/evidence boundary: `Docs/Testing/IronmakingV1Coverage.md`.

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
