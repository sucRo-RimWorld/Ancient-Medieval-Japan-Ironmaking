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
not establish new loaded-game evidence. See MVP checklist and Design for scope.

## IRON-PICKLE-20261010
**State:** 1.7 CORE AND PRODUCTION VANILLA/MO INDEPENDENTLY VERIFIED. Production base `1af461eac9d6b1326975a9866593d694f5d291f5` with final test-only patch: each profile Core 5/5 and Production 4/4 on 1.7.4976 rev1043, no skipped/flaky, complete PID logs, native ERROR0. Test fixes dispatch actual tick batches to main thread and prepare plant-dense Bill fixtures while excluding impassable items. Production input/output/fuel assertions unchanged. Canonical named premises/hashes: `Docs/Testing/IronmakingPickleEvidence.md`, `Docs/Testing/Native17-20261013.json`; procedure `Docs/GoldenPaths/IronmakingPickleE2E.md`. Earlier author-reported 1.6 results remain their own evidence; current 1.6 runtime not rerun. Refuelling, integrated logistics, trader/research/balance, real old-save/add-remove, accepted textures and release remain OPEN.

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
