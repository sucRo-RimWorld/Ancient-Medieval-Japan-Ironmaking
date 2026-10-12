# Ironmaking test ownership

- **Production:** `Tests/Production/` — XML, Vanilla Core, and optional MO source contracts. The actual author MO archive is optional; unavailable evidence must remain SKIP.
- **Runtime harness:** `Tests/Runtime/` — Pickle/startup/ERROR-result runner fixtures, **not** loaded-game PASS.
- **Loaded-game E2E:** `Tests/E2E/` and `run-pickle-e2e.bat` — original real game runner, logs and error gate unchanged.
- **Release:** No independent release test yet; future package/subscriber tests belong in `Tests/Release/`.
- **Research:** `Tests/Research/` — opt-in; not discovered by regular CI.

`test-contracts.yml` tests source and harness contracts separately. Keep game, visual and older-save acceptance separate from static PASS.
