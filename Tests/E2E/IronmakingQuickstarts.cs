using RimWorks.Quickstarts;
using Verse;
namespace AncientMedievalJapan.Ironmaking.E2E
{
    public sealed class IronmakingLargeMap : AbstractQuickstart
    {
        public override TaggedString description { get { return "Ironmaking natural deposit test map"; } }
        public override int mapSize { get { return 220; } }
        public override string seed { get { return "AMJ-Ironmaking-Map-E2E"; } }
    }
    public sealed class IronmakingWorkMap : AbstractQuickstart
    {
        public override TaggedString description { get { return "Ironmaking work and persistence test map"; } }
        public override int mapSize { get { return 80; } }
        public override string seed { get { return "AMJ-Ironmaking-Work-E2E"; } }
    }
}
