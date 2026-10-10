"""Static checks only; real RimWorld 1.6 MapGen and visuals are untested."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

class IronSandStatic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resource = ET.parse(ROOT / 'Defs/ThingDefs/IronSand.xml').getroot()
        cls.categories = ET.parse(ROOT / 'Defs/ThingCategoryDefs/IronmakingCategories.xml').getroot()
        cls.generation = ET.parse(ROOT / 'Defs/GenStepDefs/IronSandScatter.xml').getroot()
        cls.patch = ET.parse(ROOT / 'Patches/AttachIronSandMapGen.xml').getroot()
        cls.about = ET.parse(ROOT / 'About/About.xml').getroot()

    def test_all_xml_parses_and_ids_unique(self):
        files = sorted(ROOT.glob('Defs/**/*.xml')) + sorted(ROOT.glob('Patches/**/*.xml')) + [ROOT / 'About/About.xml']
        self.assertGreaterEqual(len(files), 5)
        ids = []
        for path in files:
            element = ET.parse(path).getroot()
            ids.extend(e.text for e in element.findall('./*/defName'))
        self.assertEqual(len(ids), len(set(ids)))
        self.assertIn('AMJ_IronSand', ids)
        self.assertIn('AMJ_IronSandDeposit', ids)

    def test_finite_deposit_and_no_vanilla_mineable_rewrite(self):
        dep = next(d for d in self.resource.findall('ThingDef') if d.findtext('defName') == 'AMJ_IronSandDeposit')
        self.assertEqual(dep.findtext('building/mineableThing'), 'AMJ_IronSand')
        self.assertGreater(int(dep.findtext('building/mineableYield')), 0)
        self.assertEqual(dep.findtext('building/mineableScatterCommonality'), '0')
        self.assertEqual(dep.findtext('building/veinMineable'), 'false')
        self.assertIsNone(dep.find('deepCommonality'))
        # Later manufacturing Recipes are allowed, but no Recipe creates unlimited new sand or deposits.
        for file in ROOT.glob('Defs/RecipeDefs/**/*.xml'):
            root = ET.parse(file).getroot()
            for products in root.findall('.//RecipeDef/products'):
                self.assertIsNone(products.find('AMJ_IronSand'))
                self.assertIsNone(products.find('AMJ_IronSandDeposit'))
        patch_text = (ROOT / 'Patches/AttachIronSandMapGen.xml').read_text()
        self.assertNotIn('MineableSteel', patch_text)
        self.assertNotIn('DankPyon_', patch_text)

    def test_resource_category_excludes_raw_vendor_bulk_pool(self):
        res = next(d for d in self.resource.findall('ThingDef') if d.findtext('defName') == 'AMJ_IronSand')
        self.assertEqual(res.findtext('thingCategories/li'), 'AMJ_IronmakingMaterials')
        cat = self.categories.find('ThingCategoryDef')
        self.assertEqual(cat.findtext('parent'), 'Root')
        self.assertNotEqual(cat.findtext('parent'), 'ResourcesRaw')
        self.assertIsNone(cat.find('childThingDefs'))  # The three AMJ items opt in explicitly.

    def test_mapgen_declares_single_step_and_cell_safety(self):
        gen = self.generation.find('GenStepDef')
        self.assertEqual(gen.find('genStep').get('Class'), 'GenStep_ScatterThings')
        self.assertEqual(gen.findtext('genStep/thingDef'), 'AMJ_IronSandDeposit')
        self.assertGreater(int(gen.findtext('genStep/minSpacing')), 0)
        self.assertGreater(int(gen.findtext('genStep/minDistToPlayerStart')), 0)
        self.assertIsNotNone(gen.find("./genStep/validators/li[@Class='ScattererValidator_NoNonNaturalEdifices']"))
        self.assertEqual(self.patch.findtext('Operation/value/li'), gen.findtext('defName'))
        self.assertEqual(self.patch.findtext('Operation/xpath'), 'Defs/MapGeneratorDef[@Name = "MapCommonBase"]/genSteps')

    def test_vanilla_only_dependency_and_distinct_package(self):
        self.assertEqual(self.about.findtext('packageId'), 'sucro.ancientmedievaljapan.ironmaking')
        self.assertEqual(self.about.findtext('supportedVersions/li'), '1.6')
        self.assertIsNone(self.about.find('modDependencies'))
        all_defs = ''.join(p.read_text() for p in ROOT.glob('Defs/**/*.xml'))
        for forbidden in ('DankPyon_', 'OskarPotocki.', 'brrainz.harmony', 'sucro.ancientmedievaljapan.environment'):
            self.assertNotIn(forbidden, all_defs)

    def test_no_claim_of_release_ready_graphics(self):
        about = (ROOT / 'About/About.xml').read_text()
        self.assertIn('not release-ready', about)
        resources = (ROOT / 'Defs/ThingDefs/IronSand.xml').read_text()
        self.assertIn('not an accepted release texture', resources)

if __name__ == '__main__':
    unittest.main()
