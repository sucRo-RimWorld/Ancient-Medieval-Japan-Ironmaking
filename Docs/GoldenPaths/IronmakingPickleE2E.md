# Ironmaking Pickle E2E — loaded RimWorld 1.6

**State:** author-run Vanilla 1.6 Pickle E2E PASS (5/5, 2026-10-10, run `b5a5596f84`); MO profile remains **NOT RUN**. The user-provided command output was reviewed, not the private log files. This is a bounded gameplay PASS for the five scenarios, not general release readiness. The source tests are scoped to Ironmaking; they are never included in a Workshop payload.

## Prerequisites

- Windows installation of **RimWorld 1.6**, with `RimWorldWin64.exe`, `RimWorldWin64_Data/Managed`, and a normal user configuration that can be read as a template.
- Installed Workshop **Harmony** (2009463077), **RimLogging** (3733484696), **Pickle** (3791648678), and **Quickstarts** (3793646067), plus a **.NET SDK** capable of building `net472` test assemblies. The test runner locates these by actual `About.xml` packageId and refuses ambiguous/missing installations.
- MO profile only: actual **Medieval Overhaul** (3219596926), **Vanilla Expanded Framework**, and **[SYR] Processor Framework**. The runner checks all MO dependencies *before* launching.
- Close any ordinary RimWorld process. The runner refuses to run simultaneously with it.
- **Private Windows desktop is mandatory.** A .NET Framework C# compiler (`csc.exe`) is required to build the WinSta0 test launcher. If desktop creation or compilation fails, the runner stops; it does **not** fall back to a visible game window. No `-nographics` is passed: the full graphics path remains active.

## One-command run

From the repository directory:

```bat
.\run-pickle-e2e.bat --profile Vanilla
.\run-pickle-e2e.bat --profile All
```

The default RimWorld location is `D:\SteamLibrary\steamapps\common\RimWorld`. If different, pass `--game "X:\path\RimWorld"`. `--profile MO` runs the MO case alone. Do not treat successful synthetic Python tests as a substitute for running the game command.

The launcher:
1. Validates installed game, tool assemblies, required Mods and readable normal prefs; builds `Tests/E2E/{Quickstarts,Steps}.csproj` against real 1.6 game and Pickle/Quickstarts DLLs.
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
