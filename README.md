# Ancient & Medieval Japan - Ironmaking

古代・中世日本の製鉄 / Standalone ancient–medieval Japanese ironmaking for RimWorld.

**Status:** private RimWorld 1.6 playtest build. Linux native-game Pickle testing passed all 17 Vanilla scenarios; MO passed 17 scenarios but its startup has FMOD errors reproduced without Ironmaking. The core sand → charcoal → bloom → metal chain works in tested fixtures. Research UI, complete hauling, trade arrival, long-term saves, art and balance remain unaccepted. Japanese DefInjected strings cover the current in-game names, descriptions, bill jobs, work giver and research; graphics are placeholders. Not ready for public distribution.

A Vanilla-compatible, finite iron-sand → iron bloom → usable iron path, growing from small furnaces to improved and medieval tatara operations. Medieval Overhaul and other AMJ mods are optional integrations, not hard dependencies. Edo-period full modern tatara and global ore replacement are excluded.

- [Formal design](Docs/Design.md)
- [Existing-Mod research and entry gate](Docs/Research/IronmakingExistingModEntryAudit-20261010.md)
- [MVP checklist](Docs/Research/IronmakingMVPImplementationChecklist.md)
- [Finite sand static audit](Docs/GoldenPaths/IronSandStaticAudit.md)
- [RimWorld/Pickle E2E runner and current native evidence](Docs/GoldenPaths/IronmakingPickleE2E.md)
- [Agent instructions](AGENTS.md)
- [Coordination — main only](Docs/Coordination.md)

**2026-10-14:** Actual Linux RimWorld 1.6 Pickle tests exercised 10 Core and 7 Production scenarios per Vanilla/MO. All scenarios passed; only Vanilla met the strict zero-error log gate. See [evidence and outstanding limits](Docs/Testing/IronmakingPickleEvidence.md).
