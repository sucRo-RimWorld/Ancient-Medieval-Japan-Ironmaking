# AMJ Ironmaking — Agent Instructions

## Start here
1. Read this file and `main:Docs/Coordination.md` before any design, XML, code, or art work. **Only main's Coordination is authoritative**; do not maintain work-branch-specific copies.
2. Read Project [AGENTS](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/AGENTS.md), [SharedRules](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/SharedRules.md) and relevant task procedures. Ordinary changes: topic branch → PR → actual triggered checks verified → merge. Never directly push to main for ordinary work.
3. Use [Docs/Design.md](Docs/Design.md) as the formal gameplay owner source, [MVP checklist](Docs/Research/IronmakingMVPImplementationChecklist.md) for implementation candidates, and [prior-art audit](Docs/Research/IronmakingExistingModEntryAudit-20261010.md) for the production entry gate.

## Scope
- Own standalone finite Japanese iron sand/deposits, extraction, charcoal, furnaces, bloom refining into Vanilla Steel or optional MO IronIngot, and limited iron-sand trade.
- Support Vanilla RimWorld alone. MO, Environment, Grains, Waterworks, World Tech Level, and Japanization are optional; never introduce a hard dependency without design authorization.
- No blanket changes to Vanilla Steel mines/traders or MO iron ore, Mine Shaft, deep deposits, golems, or iron ingot sellers. MO's Japanized rebalancing and research connections are the **Japanization owner's** additional conditional responsibility.
- No Edo completed tatara, unrelated weapons/armor, fantasy sword upgrades or global metallurgy replacement.

## Gates and communication
- Approved concept does **not** mean production code is approved. Existing-Mod review of VE and non-VE (including tatara variants) and mechanical Project [decision record](https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Project/blob/main/Docs/Research/ExistingModAudit.md) remain production entry HOLD.
- Source/probe/static tests are not loaded-game proof, graphics acceptance, Steam publication or distribution.
- Use **main:Docs/Coordination.md** for task status and inter-agent handoffs, never the user as messenger. Confirmed specification goes in design/code/XML, not the coordination log.
- Preserve previous approvals; check design/implementation/related features together before changing policy. Report "updated" only for actual GitHub changes with commit SHA. Avoid unsolicited Codex PR review and notification churn.
