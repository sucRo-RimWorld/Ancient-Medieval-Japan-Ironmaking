"""Fixture tests for the read-only Vanilla Core identity preflight."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "Tools/check_vanilla_core_defs.py"
SPEC = importlib.util.spec_from_file_location("core_preflight", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class VanillaCoreContractFixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.core = self.base / "Data/Core/Defs"
        self.core.mkdir(parents=True)
        self.mod = self.base / "Ironmaking"
        cat = self.mod / "Defs/ThingCategoryDefs/IronmakingCategories.xml"
        cat.parent.mkdir(parents=True)
        cat.write_text('<Defs><ThingCategoryDef><defName>AMJ_IronmakingMaterials</defName>'
                       '<parent>Root</parent></ThingCategoryDef></Defs>', encoding="utf-8")
        self.cat = cat
        self.core_file = self.core / "Vanilla.xml"
        self.core_file.write_text(self.complete_xml(), encoding="utf-8")

    @staticmethod
    def complete_xml():
        return ("<Defs>" +
                ''.join(f'<{kind}><defName>{name}</defName></{kind}>'
                        for kind, names in MODULE.REQUIRED.items() for name in names) +
                ''.join(f'<ThingDef Name="{name}" Abstract="True" />'
                        for name in MODULE.ABSTRACT_THINGS) +
                '<MapGeneratorDef Name="MapCommonBase" Abstract="True" />' +
                '</Defs>')

    def test_complete_fixture_has_no_errors(self):
        self.assertEqual(MODULE.check(self.core, self.mod), [])

    def test_detects_previous_nonexistent_category_parent(self):
        self.cat.write_text(self.cat.read_text().replace('<parent>Root</parent>',
                                                        '<parent>Resources</parent>'))
        self.assertIn("not 'Resources'", MODULE.check(self.core, self.mod)[0])

    def test_fails_on_missing_trader_def(self):
        self.core_file.write_text(self.complete_xml().replace(
            '<TraderKindDef><defName>Caravan_Outlander_BulkGoods</defName></TraderKindDef>', ''))
        errors = MODULE.check(self.core, self.mod)
        self.assertTrue(any('Caravan_Outlander_BulkGoods' in e for e in errors))

    def test_empty_core_does_not_pass(self):
        self.core_file.unlink()
        with self.assertRaisesRegex(ValueError, 'no XML'):
            MODULE.check(self.core, self.mod)


if __name__ == '__main__':
    unittest.main()
