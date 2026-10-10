# Ironmaking Coordination

**Authoritative branch:** `main` only. Specifications: `Docs/Design.md`.

## IRON-MVP-20261010
**State:** BASIC DEV XML IMPLEMENTED; remaining gameplay and release work OPEN.
Finite sand deposits/mapgen, charcoal kiln, small furnace, bloom finishing,
limited optional Vanilla caravan stock and MO IronIngot/Anvil compatibility exist.
Entry decision is ready; canonical evidence: `Docs/Research/IronmakingEntryDecision.json`
and its prior-art note. Research, improved/medieval furnaces, region weighting,
balance and accepted textures remain unimplemented/unaccepted. Static checks do
not establish loaded gameplay. See MVP checklist and Design for scope.

## IRON-PICKLE-20261010
**State:** VANILLA/MO CORE 5/5 AUTHOR-REPORTED PASS; PRODUCTION VANILLA WATCHDOG-TIMEOUT OBSERVED, RUNTIME PASS PENDING.
Vanilla run `b5a5596f84` and MO run `5127792409` passed five baseline scenarios each;
MO exit 0 in 51s with zero skipped/flaky/error logs after PR #20 (`93667960ca5901fb03634ec7cd52f5613dc53497`).
Raw local reports were not independently inspected. Earlier hidden-startup/config
failures are superseded, with diagnosis/provenance retained in Golden Path and Git history.
Core covers loaded source/Defs, natural deposit, mining and save/reload only.
Next suite: `run-pickle-e2e.bat --suite production --profile All`, four scenarios per
profile via the same private-desktop runner. Native WorkGiver/Bill jobs, exact input
and output counts and fueled Vanilla smithy consumption are asserted. Owner kiln/
furnace Crafting WorkGiver connection added; production XML amounts unchanged.
First Vanilla production run passed only source; subsequent run `cc232937e7`
reached charcoal Job start and stalled before its first 240-tick wait returned.
Confirmed harness cause: passive `ctx.WaitTicks` in Pickle Fast mode; upstream
built-in tick step advances native DoSingleTick instead. Shared fast-mode tick
helper now used by Bills and Core mining; new Windows runtime evidence required.
Bounded/early-fail monitoring and milestones remain (Golden Path linked below).
Fresh reports required; no production runtime PASS yet. Refuelling jobs, integrated
chain logistics, trade, research and distribution remain OPEN.
Canonical procedure/evidence: `Docs/GoldenPaths/IronmakingPickleE2E.md`,
`Docs/Testing/IronmakingPickleEvidence.md`.

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
