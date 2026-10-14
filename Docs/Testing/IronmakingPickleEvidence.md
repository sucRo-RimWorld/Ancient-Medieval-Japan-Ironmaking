# Ironmaking — actual Pickle run evidence

## Current Linux 1.6 native evidence — 2026-10-14

**Source:** Ironmaking main `5154eb140e1d3b747cabea8cdc3abe4b42b7729e`.
**Execution:** Project persistent WSL2/Linux host, RimWorldLinux **1.6.4871**
(`Version.txt` says rev598; actual native `Player.log` says **rev600**),
Xvfb, installed native Pickle/Quickstarts, no local chat game execution.
Project workflow source: `18b4c786d1d823d29d04872a3f2ece7eccc06dda`.
[Complete four-profile run #38513445677](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/actions/runs/38513445677),
[7-day raw artifact](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/actions/runs/38513445677/artifacts/11871295187).
The actual `summary.json` and `Player.log` from the artifact have been
independently opened, not merely inferred from workflow green/red.

| Suite | Profile | Pickle scenarios | Process | Player.log ERROR | Strict verdict |
|---|---|---:|---|---:|---|
| Production | Vanilla | **7/7 passed**; 0 failed/skipped/flaky | exit 0, 42.5 s | **0** | **PASS** |
| Production | MO | **7/7 passed**; 0 failed/skipped/flaky | exit 0, 115.4 s | **2** | **FAIL (runtime ERROR)** |
| Core | Vanilla | **10/10 passed**; 0 failed/skipped/flaky | exit 0, 64.3 s | **0** | **PASS** |
| Core | MO | **10/10 passed**; 0 failed/skipped/flaky | exit 0, 122.9 s | **2** | **FAIL (runtime ERROR)** |

All four Pickle summaries have `exitReason=passed`, the expected exact
scenario identities and zero skipped/flaky/retry failures. Both MO runs have
two startup/load-stage Unity FMOD errors:
`Cannot create FMOD::Sound instance for clip "" (FMOD error: Unsupported file or audio format.)`.
The errors occur before the native owner scenario sequence and do not prove
an Ironmaking production-job defect. A later **without-Ironmaking** control
reproduces the FMOD ERROR; the implicated provider configuration is detailed
below. The specific audio file and code origin remain unidentified.
Do not suppress them or report the full MO profile as strict PASS. The
complete four-profile matrix is **FAIL** because of this error gate.

### FMOD startup isolation, native Linux 1.6 (2026-10-14)

[Project diagnostic run #38514870015](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/actions/runs/38514870015),
[raw-artifact #11872275254](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/actions/runs/38514870015/artifacts/11872275254).
Three independent Xvfb/RimWorld 1.6/Pickle one-scenario startup profiles used
the installed native providers, isolated savedata, **no Ironmaking Mod**;
the submitted `summary.json` and Unity `Player.log` were inspected.

| Loaded Mod stack (plus Harmony/Pickle/Logging/Core) | Pickle outcome | Distinct `[ERROR] [Unity]` FMOD events |
|---|---|---:|
| Vanilla Expanded Framework (VEF) | 1/1 passed | **0** |
| VEF + [SYR] Processor Framework | 1/1 passed | **1** |
| VEF + SYR + Medieval Overhaul | 1/1 passed | **2** |

The early raw Unity output and later RimLogging-formatted `[ERROR] [Unity]`
copy are **duplicate log entries of the same events**; the initial diagnostic
counts 2 and 4 raw string occurrences, respectively. The distinct-event
counts above use only formatted `[ERROR] [Unity]` lines. At least one FMOD
invalid-empty-clip audio error occurs with VEF + SYR **without Ironmaking**,
and full MO produces two. This rules out Ironmaking as a **necessary condition**
for this startup symptom, but does not independently identify an exact
sound asset, C# call, or prove Ironmaking never contributes under other profiles.
SYR alone was not tested, so this is a configuration-level association, not
exclusive attribution to the SYR assembly.

The control Pickle assertions pass, but the two profiles containing SYR **do
not** satisfy the strict zero-runtime-ERROR gate. The original Ironmaking
Vanilla/MO results and zero-error requirements are unchanged. No suppression
or gameplay patch is authorized by the comparison.

Source provenance limitation: this Linux harness stages an **isolated,
test-only** copy of the actual pinned production Defs/Patches/assets under
a separate package ID `sucro.ancientmedievaljapan.ironmaking.linuxfixture`,
and adapts the source-root identity probe to that test-only ID. No
production gameplay values are changed. The exact published package ID,
original end-user folder and distribution payload are **not** independently
validated by this renamed-copy run. All other native Def, Job, research,
mineability, save/reload, and stock-generator assertions run in the real game.

**Test coverage:** 10 Core and 7 Production named scenarios per profile.
See `Docs/Testing/IronmakingV1Coverage.md` for each exact tested premise.
Research gate is checked through loaded def methods, not an Architect or
Research UI screenshot. The actual `StockGenerator.GenerateThings` method
is exercised; actual merchant arrival and trade transactions are not.
Production covers actual work Bill execution/interrupt/retry and output,
but not interruption across real save/reload or fully hauled logistics.
Old colony add/remove/re-add, MO configuration variants, 1.7 **current
source** runtime, regional statistical distribution, accepted graphics
and release remain outside this run.

A prior attempt, [#38512611919](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/actions/runs/38512611919),
also returned 7/7 Vanilla Production strict PASS and 7/7 MO Production
with two FMOD ERRORs; it stopped before Core. Run #38513445677
completed all four independent suites without weakening any failure gate.


## Latest independently inspected native game evidence — 2026-10-13 (superseded for changed features)

RimWorld 1.7.4976 rev1043: Vanilla and MO **Core 5/5**, **Production 4/4** per
profile, native ERROR 0, complete logs and no skips/flaky results. Production
base `1af461eac9d6b1326975a9866593d694f5d291f5`, test-only corrections
at `efd68cd570afa8e6e5c40b4acd281f6f57239194`. Exact summaries/hashes
are in [Native17-20261013.json](Native17-20261013.json).
These are historical, *pre-research-gate* runs: do not report the current
production source as native-verified. New research/fuel/map/trade scenarios have
no native PASS until executed with their exact source. Normal old-save
add/remove, economy, accepted art and distribution remain unverified.

## Historical console-reported outcomes — 2026-10-10

These are **author-reported real RimWorld results**, based on console output;
the successful-run raw Player.log and summary.json were not independently inspected.

| Suite/profile | Run | Reported outcome | Status |
| --- | --- | --- | --- |
| Core Vanilla (original harness) | `b5a5596f84` | 5/5 PASS | Prior-version evidence |
| Core MO (original harness) | `5127792409` | 5/5 PASS | Prior-version evidence |
| Production Vanilla (Fast-tick helper) | `240c258399` | **4/4 PASS**, exit 0 in 16s, 0 skipped/flaky/error logs | Current Vanilla Production PASS |
| Production MO (Fast-tick helper) | — | Not run | Pending |

Vanilla Production exercised the native wood-to-charcoal, sand-and-charcoal
smelting and bloom-forging Bills, including exact fixture input/output and
fueled smithy checks. The console confirms the strict Pickle result validator
passed and the runner removed only its owned temporary test Mods.
This does not establish MO Production, integrated logistics, balancing,
trading, research, accepted art, save migration or release readiness.

Historical next-step instruction (superseded by the 2026-10-13 evidence): `.\run-pickle-e2e.bat --suite production --profile MO`.
The Core mining helper also changed with the Fast-mode fix; repeat the Core
Vanilla and MO suites later for *current-harness* Core evidence.

## Earlier evidence and diagnostics (historical)


This records outcomes from the author's RimWorld installation, **not execution by an assistant or GitHub Actions**. For Vanilla, the author provided only the strict Pickle result console output; its underlying `summary.json` and log were not independently inspected. For the later MO startup timeout, the author **uploaded actual `launcher.log` and `Player.log`**, which were inspected directly. No MO Pickle `summary.json` was provided.

| Date | Profile | Run ID | Reported result | Status |
| --- | --- | --- | --- | --- |
| 2026-10-10 | Vanilla + Ironmaking | `b5a5596f84` | 5/5 scenarios passed; 0 skipped/flaky/error logs; test-only Mods removed; regular config/prefs/saves untouched | **PASS (author-provided actual game output)** |
| 2026-10-10 | MO + Ironmaking | `10f8fe08ce` | Game launched on private desktop, PID 15988; 900-second native timeout; partial Unity startup log, no Pickle scenario outcome | **TIMEOUT / MO 5/5 NOT VERIFIED** |

## Exact submitted console result

```text
[PASS] 5 Pickle scenarios, 0 skipped/flaky/error logs
PICKLE PASS Vanilla 5 loaded-game scenarios
All requested profiles passed. Reports: D:\SteamLibrary\steamapps\common\RimWorld\Mods\Ancient-Medieval-Japan-Ironmaking\TestResults\Pickle\Runs\b5a5596f84
Cleaned owned test folders. Normal ModsConfig, Prefs and saves untouched.
```

## What the five scenarios establish

The named `ironmaking-core.feature` scenarios test one exact loaded Ironmaking source, Vanilla output Recipe Defs, a newly generated map containing natural IronSand deposits, a pawn actually mining a test deposit via the standard WorkGiver, and Pickle disk save/reload retaining a deposit. The `validate_pickle_result.py` gate requires five named passes and checks for error lines in `Player.log`. The observed run reports that this gate passed; it does not prove approved game balance, accepted imagery, historical geography or any trade stock.

**At that earlier test stage (superseded where noted above), not yet verified:** MO 5/5; actual charcoal-kiln, small-furnace and smithy Bills executed by a pawn; fuel/material conversion and yield balance; MO `metalChain` ON/OFF; iron-sand trader inventory; save-add to a pre-Ironmaking colony; diverse climate/map types; accepted textures. In particular, the Def-only recipe scenario does **not** run a manufacturing Bill.

## Earlier next runtime gate (superseded)

After pulling the diagnostic update, use `.\run-pickle-e2e.bat --profile MO --timeout 180` as a **shortened diagnostic observation** against the current Ironmaking source. If diagnostics indicate normal ongoing loading, a later full-timeout MO run is separate from this information-gathering step. This launches actual RimWorld rendering on a private Windows desktop, uses an isolated SaveData, and preserves the player's regular game configuration. Record the new run ID and exact 5/5/ERROR outcome here. Do not mark MO PASS from source-contract XML tests or substitute `--profile All` unless Vanilla has changed since its recorded PASS.

## MO 900-second startup timeout — uploaded evidence

Author-provided console output:

```text
[E2E MO] Controller exited code=1 after 901s; validating full Pickle report next
Cleaned owned test folders. Normal ModsConfig, Prefs and saves untouched.
[PICKLE BLOCKED/FAIL] Private desktop / RimWorld / Pickle exited 1; inspect launcher.log and Player.log in ...\\TestResults\\Pickle\\Runs\\10f8fe08ce\\MO\\Reports
```

Uploaded `launcher.log` shows `[PRIVATE_DESKTOP] RimWorld pid=15988` followed by `System.TimeoutException: RimWorld Pickle exceeded hidden desktop timeout`. Uploaded `Player.log` (68 lines) shows startup of RimWorld 1.6.4871, Direct3D 11, installed Mod metadata warnings and two Mono fallback-library messages, then ends. No Pickle scenario startup/output or explicit `[ERROR]` entry appears in that log. These lines do **not** establish that a specific required MO DLL, Def, Ironmaking Patch or texture caused the halt; inactive installed Mods may generate metadata warnings during discovery. Do not alter the Mod implementation on speculation.

The 2026-10-10 follow-up runner patch adds **30-second private-desktop CPU/memory/window snapshots** to `launcher.log`, updated Python progress and bounded failed-run log-tail diagnostics. A short MO-only `--timeout 180` run can gather process-state evidence without another 900-second blind wait. The 180-second cutoff is a **diagnostic observation window**, not a stricter definition of a valid MO startup. Preserve the next `MO/Reports/launcher.log` and `Player.log`; a new Pickle `summary.json` is required for any 5/5 PASS.

## Isolated comparison proposed after 180-second MO trace (2026-10-10)

User-supplied `launcher(1).log` confirms a private-desktop `UnityWndClass` window and CPU usage rising from 75.2s at elapsed 30s to 283.3s at elapsed 180s; memory ~628–940MiB. Its `Player(1).log` again ends at the initial Unity/installed-Mod metadata/Mono fallback lines, without Pickle scenario output. The report therefore remains **MO GAMEPLAY NOT VERIFIED**. The owner now has a two-profile differential diagnostic that omits Ironmaking and toggles only Pickle/RimLogging/Quickstarts; observations from that diagnostic have **not yet been submitted**. The source/commands are in `Docs/GoldenPaths/IronmakingPickleE2E.md`.

## First errors from uploaded differential Player.logs

Uploaded files `Player(2).log` (3,458 lines; MO-Baseline) and `Player(3).log` (79 lines; MO-Pickle) were inspected directly. Both show `Error while instantiating a mod of type MedievalOverhaul.MedievalOverhaulSettings` with `NullReferenceException` inside `MedievalOverhaul.MedievalOverhaulSettings..ctor(ModContentPack)` (line 66 onward). MO-Baseline then prints `Caught exception while loading play data but there are active mods other than Core. Resetting mods config and trying again.` (line 80) and `MedievalOverhaul.Utility..cctor()` failure (lines 81–94). Subsequent missing texture/Def and repeated update errors occur **after** this first failure. MO-Pickle stops its captured log within `Verse.LoadedModManager.CreateModClasses()`, with the same constructor issue. None of those differential profiles loaded Ironmaking.

The Ironmaking test harness was found to differ from the already successful Environment Pickle source: it made a synthetic ModConfig with **empty `knownExpansions`**, and copied the existing `Prefs.xml` **without setting `resetModsConfigOnCrash=False`**. This is a proven test-harness configuration discrepancy, **not a proven single root cause of MO's constructor exception**. Updated the isolated config creation to match Environment's established pattern, with new regression cases for retention of DLC and user prefs. No fresh MO gameplay pass or Windows run follows from this source change alone.

## Independently inspected Windows 1.7 run — 2026-10-13

Production base `1af461eac9d6b1326975a9866593d694f5d291f5` plus final test-only corrections was independently run on Windows, actual `1.7.4976 rev1043`. [Exact named summaries, test/provider identities and complete PID-log hashes](Native17-20261013.json). Core `Ironmaking17-20261013-194733-450`: Vanilla **5/5**, MO **5/5**. Production `Ironmaking17-20261013-193405-164`: Vanilla **4/4**, MO **4/4**. Every accepted run: no failed/skipped/flaky scenarios, native **ERROR 0**, complete `INFO Log closed.` log.

Core premises (each profile): exact loaded source/providers; processing Defs and Vanilla Steel/MO IronIngot output routing; real generated natural finite IronSand deposit; actual mining job consumes a deposit and yields sand; actual disk save/reload retains deposits. Five named assertions passed in each profile.

Production premises (each profile): exact source/provider identity; native Bill converts **20 Wood → 10 Charcoal**; native small furnace uses **40 IronSand + 60 Charcoal → 10 Bloom**; native smithy uses **10 Bloom → 8 Steel (Vanilla) / IronIngot (MO)**. Tests retain exact ingredient/output counts, actual fueled Vanilla smithy consumption and no-double-fuel assertion. All four passed in each profile. These counts state current owner XML expectations, not balanced or historically approved economics.

The old Fast continuation ran native `DoSingleTick` on a worker thread, causing real WorldPawns/MapPawns errors. Tick lookup and batches now dispatch through the actual Pickle main-thread helper, with frame waits between unfinished batches. The legacy MonoBehaviour compile identity is resolved only for Waylith test compilation via the exact reflection `Post(Action)` method; 1.6 direct dispatch is retained.

MO's dense plants prevented the old completely-empty-area search. The disposable Bill fixture now permits Plants and standable loose items, removes only Plants without yielding materials, recalculates perceived path costs, and still requires actual native Standable terrain, no building, no fog and all production assertions. Impassable stone chunks remain excluded; the guard reports precise failing cells. No production terrain/recipe/Def change or artificial job completion was used.

Reusable procedure: execute `Scripts/Run-17Tests.ps1 -GameRoot <verified-1.7-root> -Profile All -Suite core`, then `-Suite production`; retain summaries/logs, inspect PID and ERROR gates, preserve normal config and hash-check source. BOM-free XML metadata is loaded through its declared encoding. Harness regressions passed Windows PowerShell 5.1 and PowerShell 7. Legacy 1.6 test assemblies also compile against actual installed 1.6 assemblies without the native define; this is compile evidence, not a fresh 1.6 runtime result.

Unverified: refuelling jobs, full chain logistics, trade inventories, research/balance, diverse maps/climates, MO setting variants, actual legacy colony add/remove, accepted art/UI and Workshop distribution. Production C#/XML/art/metadata and normal settings were not changed.
