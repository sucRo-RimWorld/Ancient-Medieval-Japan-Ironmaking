using System;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using RimWorks.Pickle;
using RimWorld;
using Verse;

namespace AncientMedievalJapan.Ironmaking.E2E
{
    internal static class IronmakingTestThread
    {
        public static Task Run(Action action)
        {
            var done = new TaskCompletionSource<bool>();
            RimWorks.Pickle.Runtime.PickleDriver.Post(delegate
            {
                try { action(); done.SetResult(true); }
                catch (Exception error) { done.SetException(error); }
            });
            return done.Task;
        }
    }

    internal static class IronmakingTestWorld
    {
        public static ThingDef Thing(string name, PickleContext ctx)
        {
            ThingDef thing = DefDatabase<ThingDef>.GetNamedSilentFail(name);
            ctx.Require(thing != null, "Missing loaded ThingDef " + name);
            return thing;
        }

        public static IntVec3 ClearCell(Map map, PickleContext ctx)
        {
            ctx.Require(map != null && map.Size.x >= 60, "Quickstarts map not loaded");
            for (int x = 8; x < map.Size.x - 8; x++)
                for (int z = 8; z < map.Size.z - 8; z++)
                {
                    IntVec3 p = new IntVec3(x, 0, z);
                    if (p.Fogged(map) || !p.Standable(map) ||
                        p.GetFirstBuilding(map) != null) continue;
                    bool open = true;
                    foreach (IntVec3 d in new[] { IntVec3.North, IntVec3.South,
                                                  IntVec3.East, IntVec3.West })
                    {
                        IntVec3 q = p + d;
                        if (!q.InBounds(map) || q.Fogged(map) || !q.Standable(map) ||
                            q.GetFirstBuilding(map) != null) { open = false; break; }
                    }
                    if (open) return p;
                }
            ctx.Require(false, "No revealed 5-cell flat patch on generated map");
            return IntVec3.Invalid;
        }
    }

    [PickleSteps]
    public sealed class IronmakingSteps
    {
        [Then("the exact Ironmaking source and expected profile are loaded")]
        public Task Loaded(PickleContext ctx)
        {
            return IronmakingTestThread.Run(delegate
            {
                string profile = Environment.GetEnvironmentVariable("AMJI_EXPECTED_PROFILE");
                string expected = Environment.GetEnvironmentVariable("AMJI_EXPECTED_SOURCE_ROOT");
                ctx.Require(profile == "Vanilla" || profile == "MO",
                    "AMJI_EXPECTED_PROFILE missing/invalid");
                ctx.Require(!String.IsNullOrEmpty(expected), "AMJI_EXPECTED_SOURCE_ROOT missing");
                var mods = LoadedModManager.RunningModsListForReading;
                var installed = mods.Where(m => String.Equals(m.PackageIdPlayerFacing,
                    "sucro.ancientmedievaljapan.ironmaking", StringComparison.OrdinalIgnoreCase)).ToArray();
                ctx.Require(installed.Length == 1, "Ironmaking loaded count=" + installed.Length);
                ctx.Assert(String.Equals(
                    Path.GetFullPath(installed[0].RootDir).TrimEnd('\\', '/'),
                    Path.GetFullPath(expected).TrimEnd('\\', '/'),
                    StringComparison.OrdinalIgnoreCase), "Loaded Mod root is not test source");
                bool mo = mods.Any(m => String.Equals(m.PackageIdPlayerFacing,
                    "DankPyon.Medieval.Overhaul", StringComparison.OrdinalIgnoreCase));
                ctx.Assert(mo == (profile == "MO"), "Expected " + profile + ", MO=" + mo);
            });
        }

        [Then("the Ironmaking production Defs and final metal chain resolve")]
        public Task Production(PickleContext ctx)
        {
            return IronmakingTestThread.Run(delegate
            {
                ThingDef sand = IronmakingTestWorld.Thing("AMJ_IronSand", ctx);
                ThingDef deposit = IronmakingTestWorld.Thing("AMJ_IronSandDeposit", ctx);
                ctx.Require(deposit.building != null, "Deposit lost building properties");
                ctx.Assert(deposit.building.mineableThing == sand && deposit.building.mineableYield > 0,
                    "Actual mineable output/yield is wrong");
                foreach (string name in new[] { "AMJ_Charcoal", "AMJ_IronBloom",
                                                "AMJ_CharcoalKiln", "AMJ_SmallIronFurnace" })
                    IronmakingTestWorld.Thing(name, ctx);
                foreach (string name in new[] { "AMJ_BurnCharcoal", "AMJ_SmeltIronSand" })
                    ctx.Require(DefDatabase<RecipeDef>.GetNamedSilentFail(name) != null,
                        "Missing loaded RecipeDef " + name);
                RecipeDef finish = DefDatabase<RecipeDef>.GetNamedSilentFail("AMJ_ForgeIronBloom");
                ctx.Require(finish != null, "Bloom finish recipe not loaded");
                bool mo = LoadedModManager.RunningModsListForReading.Any(m =>
                    String.Equals(m.PackageIdPlayerFacing, "DankPyon.Medieval.Overhaul",
                                  StringComparison.OrdinalIgnoreCase));
                string expected = mo ? "DankPyon_IronIngot" : "Steel";
                string user = mo ? "DankPyon_Anvil" : "FueledSmithy";
                ctx.Assert(finish.products != null && finish.products.Any(p =>
                    p.thingDef != null && p.thingDef.defName == expected && p.count == 8),
                    "Actual bloom output mismatch: expected " + expected);
                ctx.Assert(finish.recipeUsers != null && finish.recipeUsers.Any(t =>
                    t.defName == user) || (!mo && finish.recipeUsers != null &&
                    finish.recipeUsers.Any(t => t.defName == "ElectricSmithy")),
                    "Bloom recipe user not active in profile " + (mo ? "MO" : "Vanilla"));
                if (mo)
                    ctx.Assert(!finish.products.Any(p => p.thingDef.defName == "Steel"),
                        "MO progression shortcut: bloom still yields Steel");
            });
        }

        [Then("the generated map has accessible natural iron-sand deposits")]
        public Task NaturalDeposits(PickleContext ctx)
        {
            return IronmakingTestThread.Run(delegate
            {
                Map map = Find.CurrentMap;
                ctx.Require(map != null && map.Size.x >= 200, "Real large Quickstart map required");
                ThingDef target = IronmakingTestWorld.Thing("AMJ_IronSandDeposit", ctx);
                var nodes = map.listerThings.ThingsOfDef(target);
                ctx.Require(nodes.Count > 0, "No naturally generated sand deposits on test map");
                ctx.Assert(nodes.Any(t => t.Spawned && t.Position.InBounds(map) &&
                                !t.Position.Fogged(map) && t.HitPoints > 0),
                    "No revealed natural deposit can be mined");
            });
        }

        [Given("an iron-sand deposit is prepared for persistence")]
        public Task PreparePersistence(PickleContext ctx)
        {
            return IronmakingTestThread.Run(delegate
            {
                Map map = Find.CurrentMap;
                IntVec3 at = IronmakingTestWorld.ClearCell(map, ctx);
                Thing node = GenSpawn.Spawn(
                    ThingMaker.MakeThing(IronmakingTestWorld.Thing("AMJ_IronSandDeposit", ctx)),
                    at, map);
                ctx.Require(node != null && node.Spawned, "Cannot spawn save fixture deposit");
                ctx.Set<IntVec3>(at);
            });
        }

        [Then("the saved deposit still exists in the reloaded map")]
        public Task VerifyPersistence(PickleContext ctx)
        {
            return IronmakingTestThread.Run(delegate
            {
                Map map = Find.CurrentMap; // A new map after Pickle's real disk reload.
                ctx.Require(map != null, "Reload did not yield a map");
                IntVec3 at = ctx.Get<IntVec3>();
                ctx.Require(at.InBounds(map), "Saved position is out of the loaded map");
                ctx.Assert(at.GetThingList(map).Any(t =>
                    t.Spawned && t.def.defName == "AMJ_IronSandDeposit" && t.HitPoints > 0),
                    "Iron-sand deposit lost after save/reload");
            });
        }
    }
}
