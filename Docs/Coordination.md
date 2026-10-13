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
**State:** CURRENT SOURCE 9 CORE + 7 PRODUCTION PER PROFILE; NATIVE VALIDATION OPEN.
Historical RimWorld 1.7.4976 rev1043 Vanilla/MO Core **5/5** and Production
**4/4** per profile were independently verified against *pre-research* source
`1af461eac9d6b1326975a9866593d694f5d291f5` plus test-only corrections.
Evidence: `Docs/Testing/Native17-20261013.json`. Those PASS results never
cover the newer test or research source.

Test-contract cleanup PR #36 merged `eda362ea1f8f2df5e82e54d1c11a1c38bb33527e`.
New research/trade/one-session retry coverage PR #38 merged
`22bf454e2a440136006f46302259d70a9ed7aca6`.
Natural-source Mine WorkGiver / 1,200-tick depletion test PR #40 merged
`0116b61c110b05dc441d7c4d7a779d6b057590d1`.
Natural-source exact-location disk save/reload test PR #41 merged
`1176a8901cd30c6c4ea30ef24d738c5e0fe0f479`. Exact-head PR and post-merge source/runner GitHub CI PASS;
**this is not an E2E game run or compiled native test DLL**. Current source
Pickle `ironmaking-core.feature` **9 named cases**, and
`ironmaking-production.feature` **7 named cases**, each in Vanilla/MO.
Static named-scenario + C# step binding regression verifies correspondence.
Final accepted test assumptions, C# source, and pending test gaps:
`Docs/Testing/IronmakingV1Coverage.md`.

**Remaining OPEN:** genuinely pre-mod colony save add/remove/re-add; interruption
crossing a save or refuel interruption; full hauled resource chain; *actual*
trader-stock generation and iron-sand import; research designator and UI;
multiple Seed/landform weighting; MO setting variants/Japanization adapter;
balance; accepted textures; package/release. Chat-local native execution is
paused under Project `main:Docs/Coordination.md` DEV-PERSISTENT-RIMWORLD-HOST;
do not dispatch a native game without the separately approved persistent host.

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
