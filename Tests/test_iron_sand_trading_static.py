"""Seller and buyer generators are separate; runtime stock is unverified."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]

class SandTradingStatic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.patch=ET.parse(ROOT/'Patches/TradeIronSand.xml').getroot()

    def test_only_targeted_vanilla_bulk_caravans(self):
        op=self.patch.find('Operation')
        self.assertEqual(op.get('Class'),'PatchOperationConditional')
        xpath=op.findtext('xpath')
        self.assertIn('Caravan_Neolithic_BulkGoods',xpath)
        self.assertIn('Caravan_Outlander_BulkGoods',xpath)
        self.assertNotIn('Base_',xpath)
        self.assertNotIn('DankPyon_',xpath)
        self.assertEqual(op.find('match').get('Class'),'PatchOperationAdd')
        self.assertEqual(op.findtext('match/xpath'),xpath)

    def test_sale_and_buy_are_not_confused(self):
        nodes=self.patch.findall('Operation/match/value/li')
        self.assertEqual([n.get('Class') for n in nodes], ['StockGenerator_SingleDef','StockGenerator_BuySingleDef'])
        self.assertTrue(all(n.findtext('thingDef')=='AMJ_IronSand' for n in nodes))
        self.assertEqual(nodes[0].findtext('countRange'),'10~30')
        self.assertIsNone(nodes[1].find('countRange'))
        content=(ROOT/'Patches/TradeIronSand.xml').read_text()
        self.assertFalse(self.patch.findall('.//li[@Class="StockGenerator_Category"]'))
        for banned in ('MineableSteel','DankPyon_IronOre','DankPyon_IronIngot','PatchOperationReplace'):
            self.assertNotIn(banned,content)

if __name__=='__main__':
    unittest.main()
