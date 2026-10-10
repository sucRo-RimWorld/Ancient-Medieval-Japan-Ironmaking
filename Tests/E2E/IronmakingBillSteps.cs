using System;
using System.Collections.Generic;
using System.Linq;
using System.IO;
using System.Threading.Tasks;
using RimWorks.Pickle;
using RimWorld;
using Verse;
using Verse.AI;

namespace AncientMedievalJapan.Ironmaking.E2E
{
    [PickleSteps]
    public sealed class IronmakingBillSteps
    {
        [Then("a colonist completes the charcoal bill and consumes its wood")]
        public Task Charcoal(PickleContext ctx)
        {
            return Execute(ctx, "AMJ_BurnCharcoal", "AMJ_CharcoalKiln", "WoodLog",
                new Dictionary<string, int> { { "WoodLog", 20 } }, "AMJ_Charcoal", 10);
        }

        [Then("a colonist completes the sand-smelting bill and consumes sand and charcoal")]
        public Task Smelt(PickleContext ctx)
        {
            return Execute(ctx, "AMJ_SmeltIronSand", "AMJ_SmallIronFurnace", "BlocksGranite",
                new Dictionary<string, int> { { "AMJ_IronSand", 40 }, { "AMJ_Charcoal", 60 } },
                "AMJ_IronBloom", 10);
        }

        [Then("a colonist completes the bloom-forging bill with the profile metal output")]
        public Task Forge(PickleContext ctx)
        {
            bool mo = Environment.GetEnvironmentVariable("AMJI_EXPECTED_PROFILE") == "MO";
            return Execute(ctx, "AMJ_ForgeIronBloom", mo ? "DankPyon_Anvil" : "FueledSmithy",
                mo ? "Steel" : null,
                new Dictionary<string, int> { { "AMJ_IronBloom", 10 } },
                mo ? "DankPyon_IronIngot" : "Steel", 8);
        }

        private async Task Execute(PickleContext ctx, string recipeName, string tableName,
            string stuffName, Dictionary<string, int> inputs, string outputName, int amount)
        {
            Map map = null;
            Pawn worker = null;
            Building_WorkTable table = null;
            Bill_Production bill = null;
            CompRefuelable fuel = null;
            float initialFuel = 0;
            int beforeOutput = 0;
            var beforeInputs = new Dictionary<string, int>();
            var fixtures = new List<Thing>();
            try
            {
                Progress("setup:" + recipeName);
                await IronmakingTestThread.Run(delegate
                {
                    map = Find.CurrentMap;
                    // A clear 9x9 area accommodates the real multi-cell smithy and ingredients.
                    IntVec3 at = IntVec3.Invalid;
                    for (int x = 10; x < map.Size.x - 10 && !at.IsValid; x++)
                        for (int z = 10; z < map.Size.z - 10 && !at.IsValid; z++)
                        {
                            IntVec3 p = new IntVec3(x, 0, z);
                            if (CellRect.CenteredOn(p, 4).Cells.All(c => c.InBounds(map) &&
                                !c.Fogged(map) && c.Standable(map) && c.GetFirstBuilding(map) == null))
                                at = p;
                        }
                    ctx.Require(at.IsValid, "No clear production fixture area");
                    ThingDef def = IronmakingTestWorld.Thing(tableName, ctx);
                    table = ThingMaker.MakeThing(def, stuffName == null ? null :
                        IronmakingTestWorld.Thing(stuffName, ctx)) as Building_WorkTable;
                    ctx.Require(table != null, "Not a real worktable: " + tableName);
                    table.SetFaction(Faction.OfPlayer);
                    GenSpawn.Spawn(table, at, map, Rot4.North);
                    fixtures.Add(table);
                    RecipeDef recipe = DefDatabase<RecipeDef>.GetNamedSilentFail(recipeName);
                    ctx.Require(recipe != null && table.def.AllRecipes.Contains(recipe),
                        "Recipe unavailable on actual table " + tableName);
                    bill = recipe.MakeNewBill() as Bill_Production;
                    ctx.Require(bill != null, "Recipe is not a production bill");
                    bill.repeatMode = BillRepeatModeDefOf.RepeatCount;
                    bill.repeatCount = 1;
                    bill.SetStoreMode(BillStoreModeDefOf.DropOnFloor);
                    bill.ingredientSearchRadius = 8f;
                    table.billStack.AddBill(bill);
                    int offset = 0;
                    foreach (var input in inputs)
                    {
                        Thing t = ThingMaker.MakeThing(IronmakingTestWorld.Thing(input.Key, ctx));
                        t.stackCount = input.Value;
                        GenSpawn.Spawn(t, at + new IntVec3(-3 + offset++, 0, -3), map);
                        t.SetForbidden(false, false);
                        fixtures.Add(t);
                        beforeInputs[input.Key] = Count(map, input.Key);
                    }
                    beforeOutput = Count(map, outputName);
                    fuel = table.TryGetComp<CompRefuelable>();
                    if (fuel != null)
                    {
                        // Fixture fuel only; refuelling jobs are a separate integration gate.
                        fuel.Refuel(fuel.Props.fuelCapacity);
                        initialFuel = fuel.Fuel;
                    }
                    for (int i = 0; i < 30; i++)
                    {
                        Pawn p = PawnGenerator.GeneratePawn(PawnKindDefOf.Colonist, Faction.OfPlayer);
                        if (!p.Downed && p.skills != null && !p.WorkTypeIsDisabled(WorkTypeDefOf.Crafting))
                        { worker = p; break; }
                        p.Destroy(DestroyMode.Vanish);
                    }
                    ctx.Require(worker != null, "No capable crafting pawn");
                    GenSpawn.Spawn(worker, table.InteractionCell, map);
                    worker.workSettings.EnableAndInitializeIfNotAlreadyInitialized();
                    worker.skills.GetSkill(SkillDefOf.Crafting).Level = 20;
                    if (worker.needs.food != null) worker.needs.food.CurLevelPercentage = 1f;
                    if (worker.needs.rest != null) worker.needs.rest.CurLevelPercentage = 1f;
                    // Select a real loaded WorkGiver; never synthesize DoBill or its driver.
                    Job job = null;
                    foreach (WorkGiverDef giverDef in DefDatabase<WorkGiverDef>.AllDefsListForReading)
                    {
                        var giver = giverDef.Worker as WorkGiver_DoBill;
                        if (giver == null || !giver.ThingIsUsableBillGiver(table) ||
                            (giverDef.workType != null && worker.WorkTypeIsDisabled(giverDef.workType))) continue;
                        job = giver.JobOnThing(worker, table, true);
                        if (job != null && job.def == JobDefOf.DoBill && job.bill == bill) break;
                        job = null;
                    }
                    ctx.Require(job != null, "No loaded WorkGiver assigns actual bill " + recipeName);
                    job.playerForced = true;
                    worker.jobs.StartJob(job, JobCondition.InterruptForced);
                    Progress("job:" + recipeName);
                });
                bool finished = false;
                for (int i = 0; i < 110 && !finished; i++)
                {
                    await IronmakingTestThread.AdvanceTicks(ctx, 240);
                    Progress("tick:" + recipeName + ":" + i);
                    await IronmakingTestThread.Run(delegate
                    {
                        finished = bill.repeatCount == 0 && Count(map, outputName) == beforeOutput + amount;
                    });
                }
                await IronmakingTestThread.Run(delegate
                {
                    ctx.Assert(finished, "Actual pawn bill did not complete with exact output: " + recipeName);
                    foreach (var input in inputs)
                        ctx.Assert(Count(map, input.Key) == beforeInputs[input.Key] - input.Value,
                            "Ingredient consumption mismatch: " + input.Key);
                    if (fuel != null)
                        ctx.Assert(fuel.Fuel < initialFuel, "Fueled table did not consume fuel");
                });
                Progress("completed:" + recipeName);
            }
            finally
            {
                await IronmakingTestThread.Run(delegate
                {
                    if (worker != null && !worker.Destroyed)
                    {
                        if (worker.CurJob != null) worker.jobs.EndCurrentJob(JobCondition.InterruptForced, false);
                        worker.Destroy(DestroyMode.Vanish);
                    }
                    foreach (Thing t in fixtures)
                        if (!t.Destroyed) t.Destroy(DestroyMode.Vanish);
                });
            }
        }

        private static void Progress(string marker)
        {
            // Real game-tick milestone in the isolated test report folder.
            string path = Environment.GetEnvironmentVariable("AMJI_PROGRESS_PATH");
            if (!String.IsNullOrEmpty(path))
                File.WriteAllText(path, marker);
        }

        private static int Count(Map map, string name)
        {
            return map.listerThings.ThingsOfDef(DefDatabase<ThingDef>.GetNamed(name)).Sum(t => t.stackCount);
        }
    }
}
