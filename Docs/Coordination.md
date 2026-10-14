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
**State:** SOURCE-PINNED LINUX 1.6 VANILLA CORE 10/10 + PRODUCTION 7/7
STRICT PASS; MO CORE 10/10 + PRODUCTION 7/7 SCENARIO PASS BUT
TWO FMOD UNITY ERRORS PER SUITE — STRICT FAIL.

Project persistent Linux host on 2026-10-14 ran current Ironmaking main
`5154eb140e1d3b747cabea8cdc3abe4b42b7729e` against real
RimWorldLinux 1.6.4871 (Version.txt rev598; runtime log rev600). Native job,
research, stock generator, mining,
map and save tests all executed. Full four-suite GitHub Actions execution
[#38513445677](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/actions/runs/38513445677),
artifact `11871295187`; original summary/Player logs independently checked.
All game processes exit code 0, zero skipped/flaky. MO FMOD invalid empty-clip
ERROR occurs during startup. Independent without-Ironmaking Linux control
[#38514870015](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/actions/runs/38514870015)
demonstrates 0 distinct Unity FMOD ERROR events with VEF alone, 1 with
VEF+SYR, 2 with VEF+SYR+MO (each Pickle 1/1). Thus Ironmaking is **not
required** to reproduce the symptom; exact offending sound asset remains
unknown, and SYR alone has not been checked. No ERROR waiver or broad MO
compatibility PASS. Native 1.7 CURRENT-SOURCE run remains OPEN.

The Linux runner uses a **test-only renamed Mod copy** and adjusted exact-source
probe, NOT the original subscriber package ID; gameplay XML/values unchanged.
See formal `Docs/Testing/IronmakingPickleEvidence.md` and exact 17-per-profile
premises `Docs/Testing/IronmakingV1Coverage.md`. Historical pre-research
1.7 runs remain valid only for their historical source revision.
Next: identify the exact MO/SYR startup sound-asset cause (or resolve it in
the provider/isolated host), then rerun the strict MO gate; native 1.7
current-source testing waits for a verified separate 1.7 game installation.
Do not alter Ironmaking gameplay or relax ERROR checks to mask this symptom.

**Still OPEN:** real old-save add/remove/re-add, interrupted job save/reload,
full haul/refuel pipeline, actual merchant arrival/trade, Architect/research
UI, multi-seed biome weighting, MO configuration / Japanization adapter,
economic calibration, graphics and release.

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
