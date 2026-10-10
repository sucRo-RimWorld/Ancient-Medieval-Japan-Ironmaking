# Ironmaking — actual Pickle run evidence

This records outcomes from the author's RimWorld installation, **not execution by an assistant or GitHub Actions**. The underlying files are in the author's local `TestResults` directory; no `Player.log` or `summary.json` was uploaded/independently reviewed in this chat. The user supplied the output of the strict `Scripts/validate_pickle_result.py` gate.

| Date | Profile | Run ID | Reported result | Status |
| --- | --- | --- | --- | --- |
| 2026-10-10 | Vanilla + Ironmaking | `b5a5596f84` | 5/5 scenarios passed; 0 skipped/flaky/error logs; test-only Mods removed; regular config/prefs/saves untouched | **PASS (author-provided actual game output)** |
| 2026-10-10 | MO + Ironmaking | — | Not run/reported | **OPEN** |

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

Run `run-pickle-e2e.bat --profile MO` against the current Ironmaking source. This launches actual RimWorld rendering on a private Windows desktop, uses an isolated SaveData, and preserves the player's regular game configuration. Record the new run ID and exact 5/5/ERROR outcome here. Do not mark MO PASS from source-contract XML tests or substitute `--profile All` unless Vanilla has changed since its recorded PASS.
