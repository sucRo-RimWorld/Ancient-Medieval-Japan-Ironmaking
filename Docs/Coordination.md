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
**State:** HISTORICAL 1.7 BASELINE VERIFIED; REVISED CURRENT-SOURCE NATIVE TESTS OPEN.
RimWorld 1.7.4976 rev1043 *pre-research-gate* production source
`1af461eac9d6b1326975a9866593d694f5d291f5` with test-only fixes:
Vanilla and MO Core 5/5 and Production 4/4 per profile, no skips/flaky,
complete PID logs, ERROR0. Proof: `Docs/Testing/Native17-20261013.json`.
Earlier author-reported 1.6 runs retain separate, historical evidence.

Test-contract cleanup and extensions merged in PR #36,
`eda362ea1f8f2df5e82e54d1c11a1c38bb33527e`.
Static/source and harness-only CI passed on the exact PR head; revised Core **6**
and Production **6** per profile are **source-only / NOT YET RUN** on 1.6 or
1.7. New scenarios cover loaded initial research completion/gate, loaded fuel
component exclusivity and real MO Coal ingredient substitution. Bill fixtures
now use native research completion, and the 1.7 PID-tied log must close.
Historical MO-startup differential test moved to opt-in Research.
Full named premises, explicitly missing coverage and source owners:
`Docs/Testing/IronmakingV1Coverage.md`. Genuine prior-save addition/removal,
job interruption/refuelling, hauling, actual traders, research designator UI,
map region weights, MO setting variants, balance, final art and release OPEN.

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
