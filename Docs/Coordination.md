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
VEF+SYR, 2 with VEF+SYR+MO (each Pickle 1/1). Follow-up [SYR-only
run #38517611682](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/actions/runs/38517611682)
independently loaded SYR without VEF/MO/Ironmaking, exact Pickle 1/1,
native exit 0 (25.9 s), and **one** distinct FMOD Unity ERROR. Thus
Ironmaking, VEF and MO are not necessary for at least one startup audio
symptom; exact clip/call origin or Linux-specific incompatibility remains
unidentified. The green diagnostic workflow is not zero-ERROR compatibility
PASS. A staged-SYR-only sound inventory identified the sole `PF_Honk`
SoundDef / `Sounds/UI/DebugGoose/Honk.mp3` candidate. In
[actual native PF_Honk control #38526672460](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/actions/runs/38526672460),
a disposable patch Mod loaded after SYR and the live Pickle Def database
confirmed `PF_Honk` absent; despite the verified removal, 1/1 Pickle
finished with game exit0 and the same **one** Unity FMOD ERROR. Removal
of that SoundDef does **not** resolve the startup symptom under this
isolated Linux run. Later, actual native Project [source isolation #38561684353](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/actions/runs/38561684353)
attributed the **two** inherited FMOD errors to the exact staged
`MO_SYR/Sounds/UI/DebugGoose/Honk.mp3` and
`MO_MedievalOverhaul/Sounds/DankPyon_FlaskBreak.mp3` files. A
**nonshipping, converted-audio** Linux clone replacing both with PCM WAV
verified native ERROR0 on the same loaded providers
([#38564225119](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/actions/runs/38564225119)).
The original unmodified audio remains strictly FAIL; no release waiver.
Most recently, original Ironmaking core and production owner Pickle
scenarios were rerun under the independently labeled converted-media
functional lane on [native #38566687705](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/actions/runs/38566687705):
Vanilla production 7/7, MO production 7/7, Vanilla core 10/10,
MO core 10/10; all four native processes exit0, no Unity ERROR,
and full original scenario gates satisfied. **34/34 functional PASS
under converted audio only.** Production source/pinned gameplay unchanged.
This does not establish audible playback, original-MP3 acceptance,
full UI or 1.7.
Formal counts/limitations: `Docs/Testing/IronmakingPickleEvidence.md`.
No ERROR waiver or broad MO compatibility PASS. Native 1.7 CURRENT-SOURCE
run remains OPEN.

The Linux runner uses a **test-only renamed Mod copy** and adjusted exact-source
probe, NOT the original subscriber package ID; gameplay XML/values unchanged.
See formal `Docs/Testing/IronmakingPickleEvidence.md` and exact 17-per-profile
premises `Docs/Testing/IronmakingV1Coverage.md`. Historical pre-research
1.7 runs remain valid only for their historical source revision.
Next: validate actual audio playback and original distribution compatibility
separately from the successful converted-media functional gate; native 1.7
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
