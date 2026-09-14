#!/usr/bin/env python3
"""
validate_date_ranges.py — Validates sub-project date ranges against parent project bounds.

Rule: sub-project start must not be before parent start,
      sub-project end must not be after parent end.
      "Current" is treated as infinity (no upper bound violation possible).

Usage:
    python3 tests/validators/validate_date_ranges.py
    python3 tests/validators/validate_date_ranges.py --quiet   # only print failures
    python3 tests/validators/validate_date_ranges.py --verbose # print all checks

Exit codes: 0 = all pass, 1 = one or more failures
"""

import json
import re
import sys
import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
PROJECTS_DIR = REPO_ROOT / "assets" / "projects"


def parse_month_year(date_str):
    """Parse 'Month YYYY' to a sortable tuple (year, month_idx)."""
    month_order = {
        "january": 1, "february": 2, "march": 3, "april": 4,
        "may": 5, "june": 6, "july": 7, "august": 8,
        "september": 9, "october": 10, "november": 11, "december": 12,
    }
    parts = date_str.strip().split()
    if parts[0].lower() == "current":
        return (9999, 12)
    try:
        month = month_order.get(parts[0].lower(), 0)
        year = int(parts[1]) if len(parts) > 1 else 0
        return (year, month)
    except (IndexError, ValueError):
        return (0, 0)


def load_project(path):
    with open(path) as f:
        return json.load(f)["project"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--quiet", action="store_true", help="Only print failures")
    parser.add_argument("--verbose", action="store_true", help="Print all checks")
    args = parser.parse_args()

    sub_pattern = re.compile(r"^project_(\d+)\.\d+\.json$")
    parent_pattern = re.compile(r"^project_(\d+)\.json$")

    # Load all parent projects
    parents = {}
    for path in PROJECTS_DIR.glob("project_*.json"):
        if path.name == "project_template.json":
            continue
        m = parent_pattern.match(path.name)
        if m:
            try:
                proj = load_project(path)
                num = int(m.group(1))
                parents[num] = {
                    "path": path,
                    "start": parse_month_year(proj["date_range"]["start"]),
                    "end": parse_month_year(proj["date_range"]["end"]),
                    "start_str": proj["date_range"]["start"],
                    "end_str": proj["date_range"]["end"],
                }
            except Exception as e:
                print(f"WARN: Could not load parent {path.name}: {e}")

    failures = 0
    checks = 0

    for path in sorted(PROJECTS_DIR.glob("project_*.json")):
        if path.name == "project_template.json":
            continue
        m = sub_pattern.match(path.name)
        if not m:
            continue

        parent_num = int(m.group(1))
        if parent_num not in parents:
            if not args.quiet:
                print(f"WARN: No parent found for {path.name} (expected project_{parent_num}.json)")
            continue

        parent = parents[parent_num]
        try:
            sub = load_project(path)
        except Exception as e:
            print(f"FAIL: Could not load {path.name}: {e}")
            failures += 1
            continue

        sub_start = parse_month_year(sub["date_range"]["start"])
        sub_end = parse_month_year(sub["date_range"]["end"])
        sub_start_str = sub["date_range"]["start"]
        sub_end_str = sub["date_range"]["end"]

        checks += 1
        ok = True

        if sub_start < parent["start"]:
            print(f"FAIL: {path.name} start ({sub_start_str}) is before parent project_{parent_num}.json start ({parent['start_str']})")
            failures += 1
            ok = False

        if sub_end > parent["end"]:
            print(f"FAIL: {path.name} end ({sub_end_str}) is after parent project_{parent_num}.json end ({parent['end_str']})")
            failures += 1
            ok = False

        if ok and args.verbose:
            print(f"PASS: {path.name} [{sub_start_str} - {sub_end_str}] within parent [{parent['start_str']} - {parent['end_str']}]")

    if not args.quiet:
        status = "passed" if failures == 0 else "failed"
        print(f"Date range validation: {checks} sub-projects checked, {failures} violation(s) — {status}")

    sys.exit(1 if failures > 0 else 0)


if __name__ == "__main__":
    main()
