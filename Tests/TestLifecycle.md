# Test lifecycle separation

Tests are owned by their purpose and acceptance state.

| Type | Location / retained equivalents | Admission rule |
| --- | --- | --- |
| Production | `Tests/Production/` | Approved behavior and actual production code, Defs, balance or compatibility. |
| Runtime | `Tests/Runtime/` or existing `Tests/E2E/`, Pickle and RimTest | Loaded game, jobs, saves and rendering; preserve full owned ERROR logs. |
| Release | `Tests/Release/` or existing release validators | Distribution, Workshop payload, identity and package safety. |
| Research | `Tests/Research/` | Opt-in probes only, **not** included in default CI or standard tests. |

**Migration:** Existing tests stay in place until all callers, relative paths, CI jobs and docs can be changed and passed together. Research probes must have a question, owner, evidence destination and retirement condition, and be removed with their references once evidence is archived. Do not migrate by weakening existing gates or adding cosmetic/no-op checks. A separate research directory does not imply production readiness or approval of provisional values. This is a test ownership policy, not a gameplay change.
