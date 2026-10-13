"""Research access/optional MO ownership contracts, without launching RimWorld."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = "AMJ_InitialIronmaking"


class IronmakingResearchStatic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project = ET.parse(ROOT / "Defs/ResearchProjectDefs/InitialIronmaking.xml").getroot().find("ResearchProjectDef")
        cls.buildings = {
            e.findtext("defName"): e for e in ET.parse(
                ROOT / "Defs/ThingDefs_Buildings/Buildings_Ironmaking.xml"
            ).getroot().findall("ThingDef")
        }
        cls.recipes = {
            e.findtext("defName"): e for e in ET.parse(
                ROOT / "Defs/RecipeDefs/Recipes_Ironmaking.xml"
            ).getroot().findall("RecipeDef")
        }
        cls.mo = ET.parse(ROOT / "Patches/Compatibility/MedievalOverhaul.xml").getroot()

    def test_research_is_standalone_after_existing_smithing(self):
        p = self.project
        self.assertEqual(p.findtext("defName"), RESEARCH)
        self.assertEqual(p.findtext("techLevel"), "Medieval")
        self.assertEqual(p.findtext("tab"), "Main")
        self.assertEqual([v.text for v in p.findall("prerequisites/li")], ["Smithing"])
        self.assertGreater(int(p.findtext("baseCost")), 0)
        self.assertIsNotNone(p.find("researchViewX"))
        self.assertIsNotNone(p.find("researchViewY"))
        for name in ("DankPyon_", "IronIngot", "Alchemy"):
            self.assertNotIn(name, ET.tostring(p, encoding="unicode"))

    def test_only_iron_smelt_route_is_gated(self):
        furnace = self.buildings["AMJ_SmallIronFurnace"]
        kiln = self.buildings["AMJ_CharcoalKiln"]
        self.assertEqual(
            [n.text for n in furnace.findall("researchPrerequisites/li")], [RESEARCH]
        )
        self.assertIsNone(kiln.find("researchPrerequisites"))
        self.assertEqual(self.recipes["AMJ_SmeltIronSand"].findtext("researchPrerequisite"), RESEARCH)
        self.assertIsNone(self.recipes["AMJ_BurnCharcoal"].find("researchPrerequisite"))
        self.assertIsNone(self.recipes["AMJ_ForgeIronBloom"].find("researchPrerequisite"))
        self.assertEqual(self.recipes["AMJ_ForgeIronBloom"].findtext("products/Steel"), "8")

    def test_mo_research_tab_patch_only_changes_owned_project(self):
        ops = self.mo.findall("Operation")
        self.assertEqual(len(ops), 2)
        mo = ops[1]
        self.assertEqual(mo.get("Class"), "PatchOperationFindMod")
        self.assertEqual(mo.findtext("mods/li"), "Medieval Overhaul")
        match = mo.find("match")
        self.assertEqual(match.get("Class"), "PatchOperationReplace")
        self.assertEqual(
            match.findtext("xpath"),
            'Defs/ResearchProjectDef[defName="AMJ_InitialIronmaking"]/tab',
        )
        self.assertEqual(match.findtext("value/tab"), "DankPyon_MedievalResearchTab")
        self.assertNotIn("Smithing]/", match.findtext("xpath"))


if __name__ == "__main__":
    unittest.main()
