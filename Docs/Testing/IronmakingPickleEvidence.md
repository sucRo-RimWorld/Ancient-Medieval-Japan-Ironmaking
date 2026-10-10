# Ironmaking — actual Pickle run evidence

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

**Not yet verified:** MO 5/5; actual charcoal-kiln, small-furnace and smithy Bills executed by a pawn; fuel/material conversion and yield balance; MO `metalChain` ON/OFF; iron-sand trader inventory; save-add to a pre-Ironmaking colony; diverse climate/map types; accepted textures. In particular, the Def-only recipe scenario does **not** run a manufacturing Bill.

## Next runtime gate

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
