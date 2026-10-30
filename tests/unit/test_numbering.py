#!/usr/bin/env python3
"""
Unit tests for project numbering in scripts/build_cv.py.

Stored numbers are two-place decimals: 13 is a parent, 13.01 is its first
sub-project, 13.10 its tenth. Display labels drop the leading zero: 13.1, 13.10.

Run:
    python3 tests/unit/test_numbering.py
"""

import importlib.util
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("build_cv", REPO_ROOT / "scripts" / "build_cv.py")
build_cv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_cv)


class NumberingTests(unittest.TestCase):
    def test_split_number_all_indexes_survive_float_error(self):
        # (13.07 - 13) * 100 is not exactly 7 in floating point; every index must still round-trip.
        for parent in (1, 2, 13, 99):
            for sub in range(0, 100):
                stored = float(f"{parent}.{sub:02d}")
                self.assertEqual(build_cv.split_number(stored), (parent, sub), stored)

    def test_is_parent(self):
        self.assertTrue(build_cv.is_parent(13))
        self.assertTrue(build_cv.is_parent(13.0))
        self.assertFalse(build_cv.is_parent(13.01))
        self.assertFalse(build_cv.is_parent(13.10))

    def test_number_to_str(self):
        self.assertEqual(build_cv.number_to_str(13), "13")
        self.assertEqual(build_cv.number_to_str(13.01), "13.1")
        self.assertEqual(build_cv.number_to_str(13.09), "13.9")
        self.assertEqual(build_cv.number_to_str(13.10), "13.10")
        self.assertEqual(build_cv.number_to_str(13.11), "13.11")
        self.assertEqual(build_cv.number_to_str(2.08), "2.8")

    def test_labels_for_tenth_and_first_subproject_differ(self):
        # The original defect: 13.10 and 13.1 were the same JSON number.
        self.assertNotEqual(build_cv.number_to_str(13.10), build_cv.number_to_str(13.01))

    def test_number_key_orders_numerically(self):
        stored = [13.11, 13.02, 13.10, 13, 13.01, 13.09]
        ordered = sorted(stored, key=build_cv.number_key)
        self.assertEqual(ordered, [13, 13.01, 13.02, 13.09, 13.10, 13.11])
        self.assertEqual([build_cv.number_to_str(n) for n in ordered],
                         ["13", "13.1", "13.2", "13.9", "13.10", "13.11"])

    def test_label_key_orders_numerically(self):
        labels = ["13.11", "13.2", "13.10", "13", "13.1", "13.9", "2.8", "12"]
        self.assertEqual(sorted(labels, key=build_cv.label_key),
                         ["2.8", "12", "13", "13.1", "13.2", "13.9", "13.10", "13.11"])

    def test_groups_sort_subprojects_and_group_by_parent(self):
        def proj(number):
            return {"number": number, "title": f"t{number}", "client": {}, "role": "r",
                    "date_range": {"start": "January 2020", "end": "Current"}}
        projects = [proj(13), proj(13.10), proj(13.02), proj(13.01), proj(13.11), proj(12), proj(12.01)]
        groups = build_cv.build_project_groups(projects)
        self.assertEqual([g["_number_str"] for g in groups], ["13", "12"])
        self.assertEqual([build_cv.number_to_str(s["number"]) for s in groups[0]["sub_projects"]],
                         ["13.1", "13.2", "13.10", "13.11"])


if __name__ == "__main__":
    unittest.main()
