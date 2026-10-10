"""Offline static check for basic charcoal/sand/bloom output; does not load RimWorld."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

R = Path(__file__).resolve().parents[1]

def defs(path, kind):
    root=ET.parse(R/path).getroot()
    return {d.findtext('defName'):d for d in root.findall(kind)}

class ProcessingStatic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.materials=defs('Defs/ThingDefs/IronmakingMaterials.xml','ThingDef')
        cls.buildings=defs('Defs/ThingDefs_Buildings/Buildings_Ironmaking.xml','ThingDef')
        cls.recipes=defs('Defs/RecipeDefs/Recipes_Ironmaking.xml','RecipeDef')
        cls.compat=ET.parse(R/'Patches/Compatibility/MedievalOverhaul.xml').getroot()

    def test_bootstrap_without_metal(self):
        self.assertEqual(set(self.buildings),{'AMJ_CharcoalKiln','AMJ_SmallIronFurnace'})
        for building in self.buildings.values():
            self.assertIsNone(building.find('costList/Steel'))
            self.assertIsNone(building.find('.//li[@Class="CompProperties_Refuelable"]'))
            self.assertEqual(building.findtext('thingClass'),'Building_WorkTable')
        self.assertEqual(self.buildings['AMJ_CharcoalKiln'].findtext('stuffCategories/li'),'Woody')
        self.assertEqual(self.buildings['AMJ_SmallIronFurnace'].findtext('stuffCategories/li'),'Stony')

    def test_chemfuel_placeholder_uses_vanilla_single_graphic(self):
        # Real 2026-10-10 Vanilla Pickle ERROR showed StackCount searches
        # for Things/Item/Resource/Chemfuel/Chemfuel which does not exist.
        charcoal = self.materials['AMJ_Charcoal']
        self.assertEqual(charcoal.findtext('graphicData/texPath'),
                         'Things/Item/Resource/Chemfuel')
        self.assertEqual(charcoal.findtext('graphicData/graphicClass'),
                         'Graphic_Single')

    def test_three_step_bill_chain(self):
        r=self.recipes
        self.assertEqual(set(r),{'AMJ_BurnCharcoal','AMJ_SmeltIronSand','AMJ_ForgeIronBloom'})
        self.assertEqual(r['AMJ_BurnCharcoal'].findtext('ingredients/li/filter/thingDefs/li'),'WoodLog')
        self.assertEqual(r['AMJ_BurnCharcoal'].findtext('products/AMJ_Charcoal'),'10')
        self.assertEqual([x.text for x in r['AMJ_SmeltIronSand'].findall('ingredients/li/filter/thingDefs/li')],['AMJ_IronSand','AMJ_Charcoal'])
        self.assertEqual(r['AMJ_SmeltIronSand'].findtext('products/AMJ_IronBloom'),'10')
        self.assertEqual(r['AMJ_ForgeIronBloom'].findtext('products/Steel'),'8')
        for rec in r.values():
            self.assertTrue(rec.findtext('recipeUsers/li'))
            self.assertGreater(float(rec.findtext('workAmount')),0)

    def test_output_refs_and_no_double_fuel(self):
        self.assertEqual(set(self.materials),{'AMJ_Charcoal','AMJ_IronBloom'})
        for thing in self.materials.values():
            self.assertEqual(thing.findtext('thingCategories/li'),'AMJ_IronmakingMaterials')
        buildings_content=(R/'Defs/ThingDefs_Buildings/Buildings_Ironmaking.xml').read_text()
        self.assertNotIn('Refuelable', buildings_content)
        self.assertNotIn('DankPyon_', buildings_content)
        base_content=(R/'Defs/RecipeDefs/Recipes_Ironmaking.xml').read_text()
        self.assertNotIn('DankPyon_', base_content)

    def test_mo_optional_guard_prevents_steel_shortcut(self):
        find=self.compat.find('Operation')
        self.assertEqual(find.get('Class'),'PatchOperationFindMod')
        self.assertEqual(find.findtext('mods/li'),'Medieval Overhaul')
        ops=find.findall('match/operations/li')
        self.assertEqual(len(ops),4)
        product=next(op for op in ops if op.findtext('xpath')=='Defs/RecipeDef[defName="AMJ_ForgeIronBloom"]/products')
        self.assertEqual(product.findtext('value/products/DankPyon_IronIngot'),'8')
        self.assertIsNone(product.find('value/products/Steel'))
        anvil=next(op for op in ops if op.findtext('xpath')=='Defs/RecipeDef[defName="AMJ_ForgeIronBloom"]/recipeUsers')
        self.assertEqual(anvil.findtext('value/recipeUsers/li'),'DankPyon_Anvil')
        self.assertIn('DankPyon_Coal',[(t.text or '') for op in ops for t in op.findall('.//li')])

if __name__=='__main__':
    unittest.main()
