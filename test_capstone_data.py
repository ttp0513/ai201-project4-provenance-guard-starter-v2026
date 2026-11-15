"""Contract tests for the synthetic Qualtrics-style capstone data."""

import csv
import json
import unittest
from collections import Counter
from pathlib import Path

from generate_survey_scenarios import FIELDS


DATA_DIR = Path(__file__).parent / "capstone_data"
EXPORT_PATH = DATA_DIR / "qualtrics_synthetic_export.csv"
LABELS_PATH = DATA_DIR / "qualtrics_synthetic_labels.csv"


class CapstoneDataContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with EXPORT_PATH.open(newline="", encoding="utf-8") as export_file:
            reader = csv.reader(export_file)
            cls.export_rows = list(reader)

        with LABELS_PATH.open(newline="", encoding="utf-8") as labels_file:
            cls.labels = list(csv.DictReader(labels_file))

    def test_export_has_three_headers_and_eighty_responses(self) -> None:
        self.assertEqual(self.export_rows[0], FIELDS)
        self.assertEqual(len(self.export_rows[1]), len(FIELDS))
        self.assertEqual(len(self.export_rows[2]), len(FIELDS))
        self.assertEqual(len(self.export_rows[3:]), 80)

    def test_import_metadata_is_valid_json(self) -> None:
        for value in self.export_rows[2]:
            metadata = json.loads(value)
            self.assertIn("ImportId", metadata)

    def test_labels_are_separate_and_balanced_as_designed(self) -> None:
        self.assertNotIn("expected_label", self.export_rows[0])
        self.assertNotIn("scenario_family", self.export_rows[0])
        counts = Counter(row["expected_label"] for row in self.labels)
        self.assertEqual(
            counts,
            {"legitimate": 40, "suspicious": 24, "ambiguous": 16},
        )

    def test_response_ids_are_unique_and_match_labels(self) -> None:
        id_index = FIELDS.index("ResponseId")
        export_ids = [row[id_index] for row in self.export_rows[3:]]
        label_ids = [row["ResponseId"] for row in self.labels]
        self.assertEqual(len(export_ids), len(set(export_ids)))
        self.assertEqual(set(export_ids), set(label_ids))

    def test_export_does_not_include_direct_personal_identifiers(self) -> None:
        forbidden = {"name", "email", "ipaddress", "location", "recipientemail"}
        normalized_fields = {field.lower().replace(" ", "") for field in FIELDS}
        self.assertTrue(forbidden.isdisjoint(normalized_fields))


if __name__ == "__main__":
    unittest.main()
