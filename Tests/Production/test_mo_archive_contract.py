"""Optional source-contract audit against a real Medieval Overhaul 1.6 ZIP.

AMJ_MO_ARCHIVE can point at author-supplied Workshop MO. This is an XML static
audit, not game-loaded Defs or tested PatchOperation execution.
"""
from pathlib import Path
import os
import unittest
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = os.environ.get('AMJ_MO_ARCHIVE', '')


def read_mod_file(suffix):
    with zipfile.ZipFile(ARCHIVE) as archive:
        matches = [name for name in archive.namelist()
                   if name.endswith('/' + suffix)]
        if len(matches) != 1:
            raise ValueError(f'MO archive must contain exactly one {suffix!r}; '
                             f'found {len(matches)}')
        return ET.fromstring(archive.read(matches[0]))


@unittest.skipUnless(ARCHIVE and Path(ARCHIVE).is_file(),
                     'Set AMJ_MO_ARCHIVE to an actual MO 1.6 ZIP')
class MOArchiveContract(unittest.TestCase):
    def test_name_and_package_id(self):
        meta = read_mod_file('About/About.xml')
        self.assertEqual(meta.findtext('name'), 'Medieval Overhaul')
        self.assertEqual(meta.findtext('packageId'), 'DankPyon.Medieval.Overhaul')
        own = ET.parse(ROOT / 'About/About.xml').getroot()
        self.assertIn('DankPyon.Medieval.Overhaul',
                      [x.text for x in own.findall('loadAfter/li')])
        self.assertIsNone(own.find('modDependencies'))

    def test_anvil_and_iron_resources_exist_in_actual_mo(self):
        buildings = read_mod_file(
            '1.6/Defs/ThingDefs_Buildings/Production/Buildings_Production.xml')
        anvil = next(x for x in buildings.findall('ThingDef')
                     if x.findtext('defName') == 'DankPyon_Anvil')
        self.assertEqual(anvil.findtext('thingClass'), 'Building_WorkTable')
        resources = read_mod_file('1.6/Defs/ThingDefs_Items/Items_Resources.xml')
        names = {x.findtext('defName') for x in resources.findall('ThingDef')}
        self.assertTrue({'DankPyon_Coal', 'DankPyon_IronIngot'} <= names)

    def test_bloom_recipe_mo_output_is_not_steel(self):
        patch = ET.parse(ROOT / 'Patches/Compatibility/MedievalOverhaul.xml').getroot()
        condition = patch.find('Operation')
        self.assertEqual(condition.get('Class'), 'PatchOperationFindMod')
        self.assertEqual(condition.findtext('mods/li'), 'Medieval Overhaul')
        operations = condition.findall('match/operations/li')
        product = next(x for x in operations if x.findtext('xpath') ==
                       'Defs/RecipeDef[defName="AMJ_ForgeIronBloom"]/products')
        self.assertEqual(product.findtext('value/products/DankPyon_IronIngot'), '8')
        self.assertIsNone(product.find('value/products/Steel'))
        anvil = next(x for x in operations if x.findtext('xpath') ==
                     'Defs/RecipeDef[defName="AMJ_ForgeIronBloom"]/recipeUsers')
        self.assertEqual(anvil.findtext('value/recipeUsers/li'), 'DankPyon_Anvil')


if __name__ == '__main__':
    unittest.main()
