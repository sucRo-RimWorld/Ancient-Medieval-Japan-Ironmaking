"""Every player-facing Ironmaking Def field must have a Japanese DefInjected string.

The English source remains the fallback for other game languages. This checks
RimWorld's standard folder/DefType/key convention without loading the game.
"""
from pathlib import Path
from xml.etree import ElementTree as ET
import unittest

ROOT = Path(__file__).resolve().parents[2]
DEF_FIELDS = {
    "ThingDef": {"label", "description"},
    "ThingCategoryDef": {"label"},
    "RecipeDef": {"label", "description", "jobString"},
    "ResearchProjectDef": {"label", "description"},
    "WorkGiverDef": {"label", "verb", "gerund"},
}


def source_fields():
    fields = {}
    for path in sorted((ROOT / "Defs").rglob("*.xml")):
        root = ET.parse(path).getroot()
        for entry in root:
            if entry.tag not in DEF_FIELDS:
                continue
            name = entry.findtext("defName")
            if not name or not name.startswith("AMJ_"):
                continue
            for field in DEF_FIELDS[entry.tag]:
                node = entry.find(field)
                if node is not None and (node.text or "").strip():
                    key = f"{name}.{field}"
                    assert key not in fields, f"duplicate English field {key}"
                    fields[key] = entry.tag
    return fields


class JapaneseLocalizationContract(unittest.TestCase):
    def test_every_owned_player_facing_field_is_translated_exactly_once(self):
        source = source_fields()
        translations = {}
        lang = ROOT / "Languages/Japanese/DefInjected"
        self.assertTrue(lang.is_dir(), "RimWorld Japanese DefInjected folder missing")
        for path in sorted(lang.rglob("*.xml")):
            deftype = path.parent.name
            self.assertIn(deftype, DEF_FIELDS, f"unknown DefInjected type {path}")
            root = ET.parse(path).getroot()
            self.assertEqual(root.tag, "LanguageData", str(path))
            for item in root:
                self.assertNotIn(item.tag, translations, f"duplicate {item.tag}")
                self.assertEqual(source.get(item.tag), deftype, f"unmatched {item.tag}")
                value = (item.text or "").strip()
                self.assertTrue(value, f"empty {item.tag}")
                self.assertNotIn("(development)", value, f"untranslated {item.tag}")
                translations[item.tag] = value
        self.assertEqual(set(source), set(translations),
                         f"untranslated: {set(source)-set(translations)}; "
                         f"unmatched: {set(translations)-set(source)}")

    def test_expected_historical_term_labels(self):
        root = ET.parse(
            ROOT / "Languages/Japanese/DefInjected/ThingDef/Ironmaking.xml")
        mapped = {e.tag: e.text for e in root.getroot()}
        for key, label in {
            "AMJ_IronSand.label": "砂鉄",
            "AMJ_IronSandDeposit.label": "砂鉄採取地点",
            "AMJ_Charcoal.label": "木炭",
            "AMJ_IronBloom.label": "鉄塊",
            "AMJ_CharcoalKiln.label": "炭焼き窯",
            "AMJ_SmallIronFurnace.label": "小型製鉄炉",
        }.items():
            self.assertEqual(mapped[key], label)

    def test_default_english_is_retained(self):
        # Missing localization must still fall back to the same English Def.
        self.assertEqual(len(source_fields()), 24)
        self.assertIn("<li>1.6</li>", (ROOT / "About/About.xml").read_text())


if __name__ == "__main__":
    unittest.main()
