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
run-pickle-e2e.bat --profile Vanilla
run-pickle-e2e.bat --profile All
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

See [IronmakingPickleEvidence](../Testing/IronmakingPickleEvidence.md) for the exact submitted console result and limitations. The original 5 scenarios have been reported PASS with 0 skipped/flaky/error logs and cleanup completed on the author's Windows RimWorld installation. **Do not rerun Vanilla solely to reproduce this PASS.** Next cross-Mod run is `run-pickle-e2e.bat --profile MO`, which uses the same private desktop and separate SaveData and requires complete 5/5 results in the MO profile. That does not test MO `metalChain` ON/OFF as two independent profiles, nor a pawn completing charcoal/smelting Bills.

## ALL mode transition watchdog

On `--profile All`, successful Vanilla output is **only** the first profile; MO is then launched in a separate hidden desktop and its own isolated SaveData. Earlier launcher builds could appear frozen after `PICKLE PASS Vanilla` because they printed nothing while MO was loading or waiting (up to the existing 900-second game timeout).

The current launcher prints an explicit `[E2E] Starting profile 2/2: MO` and recurring `[E2E MO] running ...` messages (every 15 seconds by default). Messages report elapsed time and whether `MO/Reports/Player.log` and `summary.json` exist or grew; they are **not** a PASS. Complete Pickle summaries and ERROR-free player logs are still mandatory. The Python watchdog retains the native launcher timeout and stops the **owned** launcher/game tree if the native controller stalls, including keyboard interruption; it does not affect normal game saves or ModsConfig.

If a previous `All` attempt stopped showing output after Vanilla, treat MO as **not confirmed**, not as PASSED or automatically FAILED. After ending the old command safely and ensuring its hidden test process is gone, use `run-pickle-e2e.bat --profile MO` for the missing profile instead of repeating already accepted Vanilla. If MO does not finish, inspect that run's `MO/Reports/launcher.log`, `Player.log`, and `summary.json`; the runner now shows their directory before startup. Avoid blind retries or increasing timeout without diagnosing its real game log.
