# Ironmaking Pickle E2E — RimWorld 1.6 / 1.7 native suites

**Current state (2026-10-13):** 1.7 native **5 Core + 4 Production**
scenarios passed per Vanilla/MO profile against the **pre-research** production
source, with complete PID logs/ERROR 0 (historical only; see
[Native17-20261013.json](../Testing/Native17-20261013.json)).
Current test definitions contain **7 Core + 7 Production** scenarios per
profile, including research before/after, loaded sand-trader generators,
worktable fuel exclusivity, MO Coal Bills, and interrupted smelting.
**These revised scenarios have not been compiled or executed against a real
RimWorld build.** The exact current assertion matrix and still-missing
old-save, transport, trader inventory and MO-setting tests are in
[IronmakingV1Coverage](../Testing/IronmakingV1Coverage.md).

Testing uses a separate isolated SaveData and hidden desktop; do not touch
normal saves or interpret a source/runner unit test as native gameplay PASS.
The original author-reported 1.6 Vanilla/MO five-scenario results remain
historical and are not evidence of the expanded suites.

## Prerequisites

- Windows installation of **RimWorld 1.6**, with `RimWorldWin64.exe` and `RimWorldWin64_Data/Managed` for the established Python/private-desktop 1.6 path. RimWorld 1.7 unstable uses the separate native Waylith test entry described below (`RimWorld.exe`, `Version.txt`, Roslyn and game-root assemblies). Both require a readable normal user config template.
- Installed Workshop **Harmony** (2009463077), **RimLogging** (3733484696), **Pickle** (3791648678), and **Quickstarts** (3793646067), plus a **.NET SDK** capable of building `net472` test assemblies. The test runner locates these by actual `About.xml` packageId and refuses ambiguous/missing installations.
- MO profile only: actual **Medieval Overhaul** (3219596926), **Vanilla Expanded Framework**, and **[SYR] Processor Framework**. The runner checks all MO dependencies *before* launching.
- Close any ordinary RimWorld process. The runner refuses to run simultaneously with it.
- **Private Windows desktop is mandatory.** A .NET Framework C# compiler (`csc.exe`) is required to build the WinSta0 test launcher. If desktop creation or compilation fails, the runner stops; it does **not** fall back to a visible game window. No `-nographics` is passed: the full graphics path remains active.

## RimWorld 1.7 unstable test boundary

The isolated runner now accepts normal `ModsConfig.xml` test-template versions
`1.6.*` and `1.7.*`. It selects the matching Pickle and Quickstarts
version-specific assembly first, then `Current` / unversioned assemblies.
A single older versioned provider may be used as a **logged compatibility
probe**; ambiguous providers fail rather than selecting an arbitrary DLL.
The normal config is read-only. The selected executable's internal version is
not independently established by this test-only preflight; capture the actual
game version in the loaded-game report before claiming a 1.7 runtime PASS.
The historical 5 Core / 4 Production 1.7 record is retained. The current
7 Core / 7 Production names are enforced by `validate_pickle_result.py`;
each new revision needs new named native results and complete logs.

This is **not** an authorization to migrate production C#, add 1.7 to public
`supportedVersions`, release a 1.7 Workshop payload or claim 1.7 PASS
without a fresh actual 1.7 run. Retain distinct 1.6 and 1.7 evidence.

## Native RimWorld 1.7 unstable test entry (no production migration)

The default `run-pickle-e2e.bat --profile Vanilla|MO|All --suite core|production`
now examines the **actual game root** `Version.txt`. For 1.7 it delegates to
`Scripts/Run-17Tests.ps1`, and for 1.6 it retains the established Python/
private-WinSta0 runner. The 1.7 script may also be invoked explicitly:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File Scripts/Run-17Tests.ps1 -GameRoot "D:\SteamLibrary\steamapps\common\RimWorld" -Profile All -Suite core
```

The 1.7 path verifies `RimWorld.exe` and the actual `Version.txt`, selects
the installed Pickle/Quickstarts assemblies using their versioned
`LoadFolders.xml`, compiles **test-only** Steps/Quickstarts against the local
Waylith runtime with Roslyn, and runs on a private desktop with normal rendering.
It preserves the normal ModsConfig/Prefs as read-only templates with DLC context,
uses a new isolated SaveData per Vanilla/MO profile, checks native log PID and
ERROR=0, then applies the **unchanged** exact 5-core or 4-production scenario
validator. Source staging outside RimWorld/Mods and test companion modules are
uniquely marked and removed without touching unmarked folders. Production
Defs/C#/About version metadata and Steam payload are unchanged.

Vanilla core checks loaded Ironmaking source, production Defs, natural sand
generation, a real mining job and a save roundtrip. Production tests check
real charcoal, bloom and forging Bills. MO checks the same named assertions
with real MO/provider dependencies, not synthesized MO Defs. An unsupported
production source or provider DLL must fail, not be reported compatible.
The 1.7 runtime has **not** been executed by the GitHub CI/changes in this task;
offline test selection/log/error contracts alone never establish gameplay PASS.

## One-command run

From the repository directory:

```bat
.\run-pickle-e2e.bat --profile Vanilla
.\run-pickle-e2e.bat --profile All
```

The default RimWorld location is `D:\SteamLibrary\steamapps\common\RimWorld`. If different, pass `--game "X:\path\RimWorld"`. `--profile MO` runs the MO case alone. Do not treat successful synthetic Python tests as a substitute for running the game command.

The launcher:
1. Validates installed game, tool assemblies, required Mods and readable normal prefs; builds `Tests/E2E/{Quickstarts,Steps}.csproj` against the selected local game's managed assemblies and Pickle/Quickstarts DLLs.
2. Uses the actual Ironmaking source when installed directly under `RimWorld/Mods`; otherwise copies only production directories into **uniquely named, marked temporary Mod folders**. It stages a separate test-only Pickle+Quickstarts Mod. An unmarked or unrelated folder is never overwritten/deleted.
3. Writes **new isolated** `SaveData/Config/ModsConfig.xml` and `Prefs.xml` for each profile, leaving normal configuration, saves, installed Workshop content and source bytes untouched. Compiles `Scripts/IronmakingPrivateDesktop.cs` and uses it to start the **real** RimWorld process on a private `WinSta0` desktop with `-savedatafolder`, `-pickle-run=ironmaking-core.feature`, and `-pickle-mode=fast`. The normal desktop never receives the game's window or focus. Normal Unity rendering remains enabled (no `-nographics`).
4. Requires exact five scenario IDs, five passes, zero failures/skips/flaky retries, `exitReason=passed`, exit code zero and no ERROR-level Player.log/cross-reference XML error. Results persist under `TestResults/Pickle/Runs/<run-id>/<profile>/Reports`.
5. Removes only temporary Mod folders bearing the unique AMJI E2E marker. A failed build or missing dependency is **BLOCKED/FAIL**, never PASS.

## Scenarios and evidence scope

| Scenario | What is asserted in **loaded RimWorld**, if run | Not yet covered |
|---|---|---|
| Exact development source | One loaded Ironmaking with expected root; MO state matches requested profile | Actual Workshop downloaded payload |
| Production Defs | Sand/mineable, charcoal/kiln/furnace and bloom finishing to Steel (Vanilla) or IronIngot+Anvil (MO) | Actual Bills' consumption and production by pawn |
| Natural generation | A new seeded 220x220 Quickstart map contains a spawned/revealed deposit (not created by test) | Multi-seed biome statistics, accurate geography |
| Mining job | A capable pawn receives a real Vanilla mining WorkGiver job; generated work ticks deplete test-spawned deposit and increase real sand count | User-facing mining menu/access across biomes |
| Save round-trip | Pickle built-in `When I save and reload` persists a spawned finite deposit in a newly loaded map | Existing old save where Mod was added later |

Two profiles are separate RimWorld processes: **Vanilla+Ironmaking** and **MO+Ironmaking**. For MO, this checks the actual loaded iron-ingot output but not Japanization's additional optional rebalancing or `metalChain` setting combinations. Future tests may cover real charcoal/smelting pawn jobs, trading, save-add compatibility and renderer only after the minimal five are demonstrated working, avoiding broad/unbounded tests before a reliable base harness exists.

## Validation and troubleshooting

```bat
python -m unittest discover -s Tests -p "test_pickle_*py" -v
python -m unittest discover -s Tests -p "test_*.py" -v
```

These only test the local fixture/result gates and existing static XML checks; **they do not launch RimWorld**. With the game installed, use the batch runner above. Preserve the exact failed `summary.json`, `Player.log`, `launcher.log` and generated `report.html` for diagnosis. Never weaken assertions, skip an unavailable case, alter live player settings or declare runtime PASS on a command that stopped in preflight.

The test helper's `Tests/E2E/TestMod` must remain development-only. Do not place `Tests/`, `TestResults/`, `Pickle/` or the E2E DLLs in a subscriber/staged Workshop package.

Source precedents: [Pickle authoring](https://github.com/RimWorks/Rimworld-Pickle/blob/main/Docs/authoring.md), [autorun](https://github.com/RimWorks/Rimworld-Pickle/blob/main/Docs/autorun.md), [reports](https://github.com/RimWorks/Rimworld-Pickle/blob/main/Docs/reports.md); AMJ Waterworks and Environment existing Pickle harnesses.

## Vanilla charcoal texture regression (2026-10-10)

An actual user-run Vanilla Pickle reported `[ERROR] ... Could not load Texture2D at 'Things/Item/Resource/Chemfuel/Chemfuel' for def 'AMJ_Charcoal'` followed by `MatFrom with null sourceTex`. The development `AMJ_Charcoal` reused Vanilla Chemfuel's `texPath` but incorrectly set `Graphic_StackCount`; the original Vanilla Chemfuel ThingDef uses `Graphic_Single` for that path. Fix the charcoal Def to `Graphic_Single` without changing recipe/material identity, and preserve the exact pair in a Python regression test. A previous runtime failure is **not** a Pickle PASS. Re-run the complete hidden game profile and let fresh `summary.json` + ERROR-free `Player.log` decide; no inferred graphical success from static XML.

## Confirmed reported Vanilla run — 2026-10-10

See [IronmakingPickleEvidence](../Testing/IronmakingPickleEvidence.md) for the exact submitted console result and limitations. The original 5 scenarios have been reported PASS with 0 skipped/flaky/error logs and cleanup completed on the author's Windows RimWorld installation. **Do not rerun Vanilla solely to reproduce this PASS.** Next cross-Mod run is `.\run-pickle-e2e.bat --profile MO`, which uses the same private desktop and separate SaveData and requires complete 5/5 results in the MO profile. That does not test MO `metalChain` ON/OFF as two independent profiles, nor a pawn completing charcoal/smelting Bills.

## ALL mode transition watchdog

On `--profile All`, successful Vanilla output is **only** the first profile; MO is then launched in a separate hidden desktop and its own isolated SaveData. Earlier launcher builds could appear frozen after `PICKLE PASS Vanilla` because they printed nothing while MO was loading or waiting (up to the existing 900-second game timeout).

The current launcher prints an explicit `[E2E] Starting profile 2/2: MO` and recurring `[E2E MO] running ...` messages (every 15 seconds by default). Messages report elapsed time and whether `MO/Reports/Player.log` and `summary.json` exist or grew; they are **not** a PASS. Complete Pickle summaries and ERROR-free player logs are still mandatory. The Python watchdog retains the native launcher timeout and stops the **owned** launcher/game tree if the native controller stalls, including keyboard interruption; it does not affect normal game saves or ModsConfig.

If a previous `All` attempt stopped showing output after Vanilla, treat MO as **not confirmed**, not as PASSED or automatically FAILED. After ending the old command safely and ensuring its hidden test process is gone, use `.\run-pickle-e2e.bat --profile MO` for the missing profile instead of repeating already accepted Vanilla. If MO does not finish, inspect that run's `MO/Reports/launcher.log`, `Player.log`, and `summary.json`; the runner now shows their directory before startup. Avoid blind retries or increasing timeout without diagnosing its real game log.

## MO launch timeout — actual uploaded logs, 2026-10-10

**Result:** MO 5-scenario Pickle outcome **NOT ESTABLISHED**. Run `10f8fe08ce` on Windows launched RimWorld on the separate WinSta0 desktop (PID 15988), then the native game controller raised `System.TimeoutException` after 900 seconds. The previous top-level runner printed `Controller exited code=1 after 901s`. No `summary.json` was included with the evidence.

The author's uploaded `launcher.log` contains only the PID and timeout exception. The uploaded `Player.log` reached **RimWorld 1.6.4871**, Direct3D 11 / NVIDIA renderer initialization, game command-line and installed-Mod metadata warnings, then two Mono fallback-library messages. **It contains no loaded Pickle scenario execution, verified MO initialization or explicit fatal ERROR line.** The dozens of `downloadUrl/steamWorkshopUrl` warnings name many *installed* (not necessarily active) Mods and do not establish what blocked MO. The Mono fallback-library lines are likewise not proof of a fatal missing dependency. Do not infer an Ironmaking recipe failure from this log.

The existing private desktop helper previously waited a single blocking 900-second interval and could not report whether Unity's game process was CPU-busy or awaiting a private-desktop dialog. The updated helper takes **30-second diagnostic snapshots** (CPU seconds, memory and the private desktop's window classes/titles), without showing a game window or changing the active Mod list. The Python monitor also reports launcher log size and prints short log tails on nonzero exit. These snapshots provide the next information required to distinguish loading, stall and hidden dialog; they are diagnostics, **not a runtime PASS**.

For one bounded **diagnostic run** after pulling changes, use `.\run-pickle-e2e.bat --profile MO --timeout 180` (PowerShell: `.\run-pickle-e2e.bat --profile MO --timeout 180`). The shorter 180s limit is for collecting startup snapshots rather than asserting an MO failure at a new arbitrary performance threshold. If MO needs longer, return to the full 900s only after interpreting process-state and log evidence. Player configuration, Workshop files and saves remain isolated/unmodified. **Do not repeat Vanilla; it already passed.**

## Differential MO startup observation (2026-10-10)

Previous MO runs `10f8fe08ce` (900 seconds) and `6f42f26ad2` (180 seconds) both ended before any structured Pickle scenario output. The 180-second log shows ongoing CPU consumption and a live `UnityWndClass` on the isolated desktop, **not** evidence of successful PlayData loading or a known blocking dialog. Diagnosing a gameplay Recipe from this startup log would be speculative.

To isolate the next stage without repeating Vanilla, run the **diagnostic** matrix:

```powershell
git pull --ff-only
.\run-pickle-e2e.bat --diagnose-mo-startup --timeout 120
```

The diagnostic runner `Scripts/diagnose_mo_startup.py` launches two **real** RimWorld processes sequentially, never together, using the existing private `WinSta0` desktop launcher and a separate `SaveData/Config` for each:

| Profile | Loaded package IDs | What changes |
| --- | --- | --- |
| `MO-Baseline` | Harmony, RimWorld Core, VEF, Processor Framework, MO | Minimum MO startup |
| `MO-Pickle` | Exactly the same as MO-Baseline + RimLogging, Pickle, Quickstarts | Only testing infrastructure added |

Neither profile includes Ironmaking, the Ironmaking test helper, or a `-pickle-run` option. Consequently, there is **no automatic Pickle completion**: timeout is expected as an *observation cutoff*, not by itself a failed E2E or a startup success. They both retain full graphics rendering on the hidden desktop; there is no visible-window fallback and `-nographics` is never supplied. A separate isolated directory and fixed Mod ID list are created for each profile; the normal `ModsConfig.xml`, `Prefs.xml`, Workshop Mods and game saves are read-only. The hidden game process is terminated by the owned controller at the deadline.

Results are recorded under `TestResults/Pickle/StartupDiagnostics/<run-id>/`, including `comparison.json` and separate `MO-Baseline` / `MO-Pickle` `Player.log`, `launcher.log`, `observation.json`. The JSON explicitly labels every profile `STARTUP_OBSERVATION_ONLY` and `pickle_scenarios_verified=false`, regardless of an early exit or timeout. The existing `--profile MO` five-scenario E2E (and its strict 5/5/ERROR gate) is unchanged.

Interpretation is **comparative**, not causal proof: if both profiles reproduce the same startup point, investigate MO, its dependencies and hidden display before blaming Pickle or Ironmaking. If the baseline proceeds beyond the earlier log boundary but MO-Pickle does not, investigate testing infrastructure integration. Compare final logged milestones and 30-second CPU/memory/window snapshots, not merely whether a process consumed CPU. **Neither comparison result can authorize a gameplay PASS.**

This bounded differential is preferable to blindly raising the 900-second timeout or changing game XML. Any native process could still reach a main menu and run until the observation cutoff, so do not equate the deadline with failure unless the report independently shows an error.

## Reuse the proven Environment test configuration writer (2026-10-10)

Do **not** synthesize a new, sparse `ModsConfig.xml` in Ironmaking. The already successful AMJ Environment development Pickle runner (`Environment/Scripts/EnvironmentFrameworkTestCommon.py::write_isolated_config`) reads normal player `ModsConfig.xml` as a **read-only template**, replaces its `activeMods`, keeps the original `knownExpansions` and all other ModConfig context, and sets `devMode=True` plus `resetModsConfigOnCrash=False` in the **copied** `Prefs.xml` only. Ironmaking's original runner and the differential probe instead rebuilt an empty `knownExpansions` node and allowed a failed MO start to reset the profile.

Ironmaking now follows **that existing successful algorithm**, implemented once in `Scripts/isolated_rimworld_config.py` and reused by `run-pickle-e2e.py` and `diagnose_mo_startup.py`. Only the isolated config and prefs are written; normal player config, known expansion IDs, saves and installed Workshop content are never edited. The generated `activeMods` list remains an explicit profile list, normalized to lowercase just like Environment. The comparison is intended to avoid configuration artifacts and preserve the original exception; **it does not prove the earlier MO NullReferenceException was caused by the empty expansion list**.

In uploaded `MO-Baseline/Player.log` (`792efd4b75`), the **first** error is `MedievalOverhaul.MedievalOverhaulSettings..ctor(ModContentPack)` throwing `NullReferenceException`. The game next prints `Resetting mods config and trying again` and `Could not recover from errors loading play data`; thousands of missing MO textures/Defs and repeated `Root.Update()` exceptions are **subsequent recovery-path symptoms** and should not be treated as independent Ironmaking graphics bugs. `MO-Pickle/Player.log` independently begins with that same MO settings constructor exception before the log ends, with no Ironmaking loaded in either comparison profile.

Next action: use the **existing real** five-scenario runner after pulling this config fix:

```powershell
git pull --ff-only
.\run-pickle-e2e.bat --profile MO
```

Vanilla is already PASS; avoid `--profile All` unless intentionally retesting both. Preserve the strict `summary.json` and complete `Player.log` ERROR gate. If MO again reports a constructor error, inspect that first error with unchanged isolated `activeMods` rather than extending timeout or creating another diagnostic matrix.

## MO baseline completion — 2026-10-10

After PR #20 corrected the isolated `Prefs.xml` root-tag assumption (main `93667960ca5901fb03634ec7cd52f5613dc53497`), the author ran `.\run-pickle-e2e.bat --profile MO --timeout 180`. Run `5127792409` reported 5/5 scenarios, zero skipped/flaky/error logs and exit code zero after 51 seconds; the runner cleaned temporary Mod folders and reported normal configuration untouched. Full report location: `TestResults/Pickle/Runs/5127792409/MO/Reports` on the author's Windows installation. Evidence currently comprises console output supplied by the author; original Player.log and summary.json have not been independently opened here. Vanilla's separately reported 5/5 remains valid. Do not infer actual production Bill execution/fuel, trade, research, or release readiness from these five checks. Earlier MO startup diagnostic failures are historical; no need to repeat baseline MO solely for the earlier timeout.

## Actual production bills — separate follow-up suite

The baseline core suite remains five scenarios. Run the new production suite without
replaying natural mapgen/mining/save baseline scenarios:

```powershell
git pull --ff-only
.\run-pickle-e2e.bat --suite production --profile All
```

This runs four scenarios per profile: exact source/profile plus actual charcoal,
sand-smelting and bloom-forging bills. It uses the existing private desktop, normal
rendering, isolated configuration and strict complete summary / zero-ERROR gate.
The new result gate requires these exact four names; a core report cannot pass it.

Fixtures provide completed tables, a capable pawn and exact input amounts. A real
loaded `WorkGiver_DoBill` must assign each bill, and native jobs must finish it.
The test requires one completed bill, exact material consumption and exact product
counts: WoodLog20 → Charcoal10; Sand40 + Charcoal60 → Bloom10; Bloom10 → Steel8
(Vanilla fueled smithy) or IronIngot8 (MO anvil). These are current developer XML
amounts, not approved balance. Vanilla smithy fuel is prefilled as fixture setup;
the test checks actual fuel decreases. Charcoal in the small furnace is a consumed
recipe ingredient, not a CompRefuelable fuel tank. Refuelling jobs, integrated
multi-stage logistics, trade, research, balance and accepted art remain uncovered.

The owner WorkGiver `AMJ_IronmakingBills` connects Crafting to the kiln and small
furnace. Their earlier Recipes existed without a matching WorkGiver. The E2E must
not bypass this connection by synthesizing a DoBill Job or calling recipe output
methods. Fresh production-suite reports are required before claiming runtime PASS.

## Production watchdog: bounded feedback (2026-10-10)

The first author-run production/Vanilla attempt loaded `IronmakingWorkMap` but
remained alive beyond 840 seconds. Its interim `summary.json` had only the source
scenario passed and `exitReason=watchdog-timeout`. The prior outer 900-second
default reported growing launcher diagnostics, not production progress.

The E2E runner now uses a **300-second per-profile hard deadline** instead of
900 seconds and Pickle's run timeout is 4 instead of 12. It **fails immediately**
on a Pickle `watchdog-timeout`/`failed`/`error`/`timeout` summary instead of
waiting for the outer process to exit. In production, after 120 seconds without
a new completed scenario or test-step milestone during startup/map transition,
or 60 seconds without a *completed game-Tick batch* within an active Bill step,
the runner terminates only its owned game/controller and retains reports.

A separate test-only `step-progress.txt` in each report folder records Bill
setup, native Job start, each completed 240-Tick wait and Bill completion.
**Neither launcher.log growth, CPU use nor unchanged Player.log counts as
gameplay progress.** Milestones never count as PASS; the unchanged
`validate_pickle_result.py` full-summary and Player.log ERROR gates remain
mandatory. No visible-window fallback, changes to normal saves/config,
or weaker yield/fuel assertions were introduced. `--timeout N` still overrides
the 300-second hard deadline for explicitly diagnosed slower setups;
the separate startup-observation mode is unchanged.

To re-check after pulling and ensuring the previous hidden game is gone:

```powershell
.\run-pickle-e2e.bat --suite production --profile Vanilla
```

Run MO only after the new Vanilla production result is known. A synthetic unit
test of the watchdog is **not** a game runtime PASS. Inspect the named run's
`Vanilla/Reports/{summary.json,Player.log,launcher.log,step-progress.txt}`
on failure; retain the earliest error and avoid blind retries.

## Pickle Fast-mode game-tick deadlock found after 60-second watchdog run (2026-10-10)

Author run `cc232937e7` built both test assemblies with zero warnings and
passed only the exact-source Production scenario. During the charcoal scenario,
the test wrote `job:AMJ_BurnCharcoal` and then emitted **no** `tick:` milestone.
The monitor failed after 60 seconds without verified progress. This is a test
harness failure, not proof that the kiln or production recipe failed.

**Root cause (upstream source verified):** Ironmaking's custom Bill step awaited
`ctx.WaitTicks(240)` in `-pickle-mode=fast`. Upstream
`RimWorks/Rimworld-Pickle` at
`Source/Pickle/Runtime/PickleDriver.cs` implements `WaitTicks` as a passive
wait for `Find.TickManager.TicksGame` to advance; it only unpauses in **non-Fast**
mode. Its built-in tick step in
`Source/Pickle.Vanilla/SimSteps.cs` explicitly advances
`Find.TickManager.DoSingleTick()` in batches of 60, yielding
`ctx.WaitFrames(1)` between batches while in Fast mode.
A paused Quickstart therefore cannot advance through the custom passive wait.

The single common test-only `IronmakingTestThread.AdvanceTicks` now uses
that upstream-compatible simulation pattern in Fast mode and retains the
passive `ctx.WaitTicks` in Watch mode. Both Production Bills and the Core mining
test use this helper. **Do not** change the Mod's production XML or job
implementation to address the harness deadlock. The strict Pickle four/five
scenario, output/ingredient/fuel and Player.log ERROR gates are unchanged.

The correction still requires actual Windows RimWorld confirmation. The previous
Core 5/5 evidence remains valid only for its original tested source/harness;
it is not a new PASS of the modified shared tick helper. Rerun Production
Vanilla first, then MO; rerun Core mining in both profiles before making current
source-wide runtime claims. Inspect `step-progress.txt` if a later failure
occurs after tick batches; in that case treat Job outcome as a separate gameplay
issue rather than the old waiting deadlock.

## Vanilla Production PASS after Fast-mode correction — 2026-10-10

Author run `240c258399` of
`run-pickle-e2e.bat --suite production --profile Vanilla` passed all four
Production scenarios in 16 seconds (exit code 0, zero skipped/flaky/error
logs, test-only Mod cleanup). This is **author-provided console evidence**;
raw report files have not been independently inspected. In Vanilla, the
corrected Tick helper now permits the native production Bill fixtures to
complete under the existing strict input/output/fuel and ERROR gates.
The old Vanilla deadlock is superseded; do not repeat its successful
Production profile solely to test MO.

Next command:

```powershell
.\run-pickle-e2e.bat --suite production --profile MO
```

Core mining uses the changed shared Tick helper too; rerun Core Vanilla/MO
for new current-harness evidence later. Production MO, refuelling, integrated
logistics, trader inventory, research, balance, accepted textures and release
remain separately unverified.


## Independently verified 1.7 current harness

Final main-thread tick and plant-dense fixture corrections passed Core 5/5 and Production 4/4 in both Vanilla and MO on 1.7.4976 rev1043. Current named premises, source/provider hashes, log completeness and remaining gaps are in [the owner evidence](../Testing/IronmakingPickleEvidence.md#independently-inspected-windows-17-run--2026-10-13) and its adjacent Native17 JSON. Historical 1.6 console evidence is not reused as a current-harness runtime result.
