# Ironmaking Coordination

**Authoritative branch:** `main` only. This is an inter-workstream task/status log; specifications belong in `Docs/Design.md`. Do not maintain other copies.

## IRON-OWNER-20261010 — Design ownership migration
**State:** MIGRATED DESIGN / NOT IMPLEMENTED.  
Project's pre-split design, MVP checklist and prior-art review are moved to Ironmaking's formal sources. The initial root README commit was `6f8d8cb8e2b5298c170762d1b8ec56dfcfffcd5a`. Project copies are historical link stubs after its subsequent PR.

## IRON-ENTRY-20261010 — Prior-art gate
**State:** ENTRY DECISION RECORDED; implementation proceeds only by bounded PRs and remains unverified in game.  
Vanilla Iron and Steel Continued 1.6 overlaps bloomery/ore-to-Steel. VE, non-VE, Vanilla/MO and AMJ alternatives were compared for minimal dependency and non-destructive finite sand supply. Owner `Docs/Research/IronmakingEntryDecision.json` is `ready`, with a matching SHA-256 evidence file and an independently executed equivalent schema/hash check. The Project validator Python file itself was not executed in this chat; this is not a game-load PASS. Source: `Docs/Research/IronmakingExistingModEntryAudit-20261010.md`.

## IRON-MVP-20261010 — Upcoming owner work
**State:** SAND-DEPOSIT STATIC SOURCE ADDED; FURTHER MVP MODULES PENDING.  
First finite iron-sand deposit ThingDef + GenStep XML developer slice was added after the entry decision, plus six static tests (local PASS). Charcoal, furnace, bloom, usable metal and trade are not implemented. The old 5-test research probe is not the loaded-game validation. Verify mining reachability, save behavior, no refuel/bill double consumption and optional MO entry. Runtime/test design: `Docs/Research/IronmakingMVPImplementationChecklist.md`.

## MOJ-IRON-INTERFACE-20261010
**State:** AWAITING packageId/DefNames and loaded profile.  
Ironmaking owns its sand supply and ordinary MO interoperability. Japanization owns additional MO iron ores/Mine Shaft/merchant rebalancing in the integrated metalChain-ON reference profile. When identifiers are stable, publish in the formal owner design and coordinate directly in Japanization `main:Docs/Coordination.md`, not via user requests.
