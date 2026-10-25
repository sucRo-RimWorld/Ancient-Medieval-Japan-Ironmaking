# AMJ Ironmaking — Agent Instructions

## Start here
1. Read this file and `main:Docs/Coordination.md` before any design, XML, code, or art work. **Only main's Coordination is authoritative**; do not maintain work-branch-specific copies.
2. Read Project [AGENTS](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/AGENTS.md), [SharedRules](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/SharedRules.md) and relevant task procedures. Ordinary changes: topic branch → PR → actual triggered checks verified → merge. Never directly push to main for ordinary work.
3. Use [Docs/Design.md](Docs/Design.md) as the formal gameplay owner source, [MVP checklist](Docs/Research/IronmakingMVPImplementationChecklist.md) for implementation candidates, and [prior-art audit](Docs/Research/IronmakingExistingModEntryAudit-20261010.md) for the production entry gate.

## Scope
- Own standalone finite Japanese iron sand/deposits, extraction, charcoal, furnaces, bloom refining into Vanilla Steel or optional MO IronIngot, and limited iron-sand trade.
- Support Vanilla RimWorld alone. MO, Environment, Grains, Waterworks, World Tech Level, and Japanization are optional; never introduce a hard dependency without design authorization.
- No blanket changes to Vanilla Steel mines/traders or unreviewed MO iron ore, Mine Shaft, deep deposits, golems or iron ingot sellers. **2026-10-25 author policy supersedes the former Japanization-owned adapter:** Ironmaking itself owns potential additional **optional MO-only** iron-source, Mine Shaft, research and stock-generator integration. Those changes require independent scenario/economic audit and separately accepted coefficients; the old centralized Japanization repo is not a required gameplay owner or dependency.
- No Edo completed tatara, unrelated weapons/armor, fantasy sword upgrades or global metallurgy replacement.

## Gates and communication
- The VE/non-VE independent-implementation [decision JSON](Docs/Research/IronmakingEntryDecision.json) is currently `status: ready` and its evidence SHA-256 matches the owner research note; an equivalent structural/hash check was executed, **not the Project Python validator itself**. This permits bounded developer XML/tests under the accepted design; it does **not** imply loaded-game, graphics, numeric balance, save compatibility or release approval. Follow the Project [Existing-Mod gate](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/ExistingModAudit.md) again for substantial new scope.
- Source/probe/static tests are not loaded-game proof, graphics acceptance, Steam publication or distribution.
- Use **main:Docs/Coordination.md** for task status and inter-agent handoffs, never the user as messenger. Confirmed specification goes in design/code/XML, not the coordination log.
- Preserve previous approvals; check design/implementation/related features together before changing policy. Report "updated" only for actual GitHub changes with commit SHA. Avoid unsolicited Codex PR review and notification churn.
