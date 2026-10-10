using System;
using System.Linq;
using System.Threading.Tasks;
using RimWorks.Pickle;
using RimWorld;
using Verse;
using Verse.AI;

namespace AncientMedievalJapan.Ironmaking.E2E
{
    [PickleSteps]
    public sealed class IronmakingMiningSteps
    {
        [Then("a mining colonist depletes an iron-sand deposit and receives sand")]
        public async Task ActuallyMine(PickleContext ctx)
        {
            Pawn worker = null;
            Thing node = null;
            Map map = null;
            int originalSand = 0;
            try
            {
                await IronmakingTestThread.Run(delegate
                {
                    map = Find.CurrentMap;
                    IntVec3 at = IronmakingTestWorld.ClearCell(map, ctx);
                    ThingDef sand = IronmakingTestWorld.Thing("AMJ_IronSand", ctx);
                    originalSand = map.listerThings.ThingsOfDef(sand).Sum(t => t.stackCount);
                    node = GenSpawn.Spawn(ThingMaker.MakeThing(
                        IronmakingTestWorld.Thing("AMJ_IronSandDeposit", ctx)), at, map);
                    ctx.Require(node != null && node.Spawned, "Mineable fixture failed to spawn");
                    for (int i = 0; i < 30; i++)
                    {
                        Pawn candidate = PawnGenerator.GeneratePawn(
                            PawnKindDefOf.Colonist, Faction.OfPlayer);
                        if (!candidate.Downed && candidate.skills != null &&
                            !candidate.WorkTypeIsDisabled(WorkTypeDefOf.Mining))
                        {
                            worker = candidate;
                            break;
                        }
                        candidate.Destroy(DestroyMode.Vanish);
                    }
                    ctx.Require(worker != null, "No pawn capable of Mining was generated");
                    GenSpawn.Spawn(worker, at + IntVec3.North, map);
                    worker.workSettings.EnableAndInitializeIfNotAlreadyInitialized();
                    worker.skills.GetSkill(SkillDefOf.Mining).Level = 20;
                    if (worker.needs.food != null) worker.needs.food.CurLevelPercentage = 1f;
                    if (worker.needs.rest != null) worker.needs.rest.CurLevelPercentage = 1f;

                    DesignationDef mining = DefDatabase<DesignationDef>.GetNamedSilentFail("Mine");
                    WorkGiverDef giverDef = DefDatabase<WorkGiverDef>.GetNamedSilentFail("Mine");
                    ctx.Require(mining != null && giverDef != null,
                        "Vanilla Mine designation or WorkGiver missing");
                    map.designationManager.AddDesignation(new Designation(node, mining));
                    var giver = giverDef.Worker as WorkGiver_Scanner;
                    ctx.Require(giver != null && giver.HasJobOnThing(worker, node, true),
                        "Actual Mine WorkGiver cannot target IronSandDeposit");
                    Job job = giver.JobOnThing(worker, node, true);
                    ctx.Require(job != null, "Actual Mine WorkGiver returned null job");
                    job.playerForced = true;
                    worker.jobs.StartJob(job, JobCondition.InterruptForced);
                    ctx.Require(worker.CurJob != null, "Worker failed to begin mining job");
                });

                bool finished = false;
                for (int batch = 0; batch < 110 && !finished; batch++)
                {
                    await IronmakingTestThread.AdvanceTicks(ctx, 240);
                    await IronmakingTestThread.Run(delegate
                    {
                        int afterSand = map.listerThings.ThingsOfDef(
                            IronmakingTestWorld.Thing("AMJ_IronSand", ctx)).Sum(t => t.stackCount);
                        if ((node.Destroyed || !node.Spawned) && afterSand > originalSand)
                            finished = true;
                    });
                }
                await IronmakingTestThread.Run(delegate
                {
                    ctx.Assert(finished,
                        "Real mining failed to deplete the deposit and produce iron sand within 26400 ticks");
                });
            }
            finally
            {
                await IronmakingTestThread.Run(delegate
                {
                    if (worker != null && !worker.Destroyed)
                    {
                        if (worker.CurJob != null)
                            worker.jobs.EndCurrentJob(JobCondition.InterruptForced, false);
                        worker.Destroy(DestroyMode.Vanish);
                    }
                });
            }
        }
    }
}
