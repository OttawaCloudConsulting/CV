#!/usr/bin/env python3
"""
build_cv.py — CV as Code build pipeline.

Renders CV.md from:
  - assets/projects/project_*.json (project data)
  - data/personal.json (personal info, certifications, executive summary)
  - templates/cv.md.j2 (Jinja2 template)

Usage:
    python3 scripts/build_cv.py [--output PATH] [--template PATH]

Adding a new role:
    1. Copy assets/projects/project_template.json to project_N.json
    2. Fill in all fields including date_range
    3. Add sub-project files as project_N.M.json
    4. Run this script
"""

import json
import math
import re
import argparse
from collections import defaultdict
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader, select_autoescape
except ImportError:
    print("Error: jinja2 is not installed. Run: pip install jinja2")
    raise SystemExit(1)

REPO_ROOT = Path(__file__).parent.parent
PROJECTS_DIR = REPO_ROOT / "assets" / "projects"
PERSONAL_FILE = REPO_ROOT / "data" / "personal.json"
TEMPLATES_DIR = REPO_ROOT / "templates"
DEFAULT_OUTPUT = REPO_ROOT / "CV.md"
DEFAULT_TEMPLATE = "cv.md.j2"
TECH_INDEX_OUTPUT = REPO_ROOT / "TECHNOLOGY_INDEX.md"
TECH_INDEX_TEMPLATE = "tech_index.md.j2"


def load_personal():
    with open(PERSONAL_FILE) as f:
        return json.load(f)


def load_projects():
    """Load all project JSON files, excluding template."""
    projects = []
    for path in sorted(PROJECTS_DIR.glob("project_*.json")):
        if path.name == "project_template.json":
            continue
        with open(path) as f:
            data = json.load(f)
        projects.append(data["project"])
    return projects


def is_parent(number):
    """Return True if the project number is an integer (parent role)."""
    return number == math.floor(number)


def number_to_str(number):
    """Format a project number for display: 13 -> '13', 13.1 -> '13.1'."""
    if is_parent(number):
        return str(int(number))
    # Format decimal numbers cleanly
    s = f"{number:.1f}"
    # Handle cases like 2.10 -> still 2.1
    return s.rstrip("0").rstrip(".")


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


def build_project_groups(projects):
    """
    Separate projects into parents and sub-projects.
    Group sub-projects under their parent.
    For orphan sub-projects (no parent file), synthesise a parent.
    Returns a list of group dicts sorted by number descending.
    """
    parents = {}
    sub_projects = defaultdict(list)

    for p in projects:
        num = p["number"]
        if is_parent(num):
            parents[int(num)] = p
        else:
            parent_num = int(math.floor(num))
            sub_projects[parent_num].append(p)

    # Sort sub-projects within each group by number ascending
    for parent_num in sub_projects:
        sub_projects[parent_num].sort(key=lambda p: p["number"])

    # Build all group numbers (union of parent keys and sub-project parent keys)
    all_parent_nums = sorted(
        set(parents.keys()) | set(sub_projects.keys()), reverse=True
    )

    groups = []
    for n in all_parent_nums:
        subs = sub_projects.get(n, [])
        if n in parents:
            group = dict(parents[n])
            group["_number_int"] = n
            group["_number_str"] = str(n)
            group["sub_projects"] = subs
        else:
            # Synthesise parent from sub-project data
            first_sub = subs[0]
            # Compute combined date range across all subs
            starts = [parse_month_year(s["date_range"]["start"]) for s in subs]
            ends = [parse_month_year(s["date_range"]["end"]) for s in subs]
            earliest_start = min(starts, key=lambda x: x)
            latest_end = max(ends, key=lambda x: x)
            # Find original string values corresponding to min/max
            start_str = subs[starts.index(earliest_start)]["date_range"]["start"]
            if latest_end == (9999, 12):
                end_str = "Current"
            else:
                end_str = subs[ends.index(latest_end)]["date_range"]["end"]

            group = {
                "number": n,
                "title": first_sub.get("title", f"Project {n}"),
                "client": first_sub.get("client", {}),
                "role": first_sub.get("role", ""),
                "date_range": {"start": start_str, "end": end_str},
                "challenge": None,
                "solution": None,
                "outcomes": [],
                "technologies": [],
                "_number_int": n,
                "_number_str": str(n),
                "_synthesised": True,
                "sub_projects": subs,
            }

        # Assemble role_overview deliverables and outcomes from sub-project parentsummary
        if subs and "role_overview" in group:
            group["role_overview"] = dict(group["role_overview"])  # don't mutate original
            group["role_overview"]["deliverables"] = [
                s["parentsummary"]["deliverables"]
                for s in subs
                if s.get("parentsummary", {}).get("deliverables")
            ]
            group["role_overview"]["outcomes"] = [
                s["parentsummary"]["outcomes"]
                for s in subs
                if s.get("parentsummary", {}).get("outcomes")
            ]

        groups.append(group)

    return groups


def build_tech_index(groups):
    """
    Auto-aggregate technology items from all projects into an alphabetical index.
    Returns an OrderedDict of letter -> list of (tech_item, [project_refs]).
    """
    tech_map = defaultdict(set)  # tech_item -> set of project number strings

    def collect(project, num_str):
        for tech_group in project.get("technologies", []):
            for item in tech_group.get("items", []):
                tech_map[item].add(num_str)

    for group in groups:
        parent_num_str = group["_number_str"]
        # Collect from parent (if it has technologies, e.g. standalone parent)
        if group.get("technologies"):
            collect(group, parent_num_str)
        # Collect from sub-projects
        for sub in group.get("sub_projects", []):
            sub_num_str = number_to_str(sub["number"])
            collect(sub, sub_num_str)

    # Sort by tech name, group by first letter
    index = defaultdict(list)
    for tech, proj_nums in sorted(tech_map.items(), key=lambda x: x[0].upper()):
        letter = tech[0].upper()
        sorted_nums = sorted(proj_nums, key=lambda x: float(x))
        index[letter].append((tech, sorted_nums))

    # Sort letters
    return dict(sorted(index.items()))


def render(output_path=None, template_name=DEFAULT_TEMPLATE):
    personal_data = load_personal()
    projects = load_projects()
    groups = build_project_groups(projects)
    tech_index = build_tech_index(groups)

    def make_anchor(heading):
        """Generate a GitHub-flavored Markdown anchor from a heading string."""
        s = heading.lower()
        # Remove characters that aren't alphanumeric, spaces, or hyphens
        s = re.sub(r"[^\w\s-]", "", s)
        # Replace spaces with hyphens
        s = re.sub(r"\s+", "-", s.strip())
        return s

    def project_refs(num_set):
        """Format a set of project number strings into 'Project N' or 'Projects N, M'."""
        nums = sorted(num_set, key=lambda x: float(x))
        if len(nums) == 1:
            return f"Project {nums[0]}"
        return "Projects " + ", ".join(nums)

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape([]),
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["anchor"] = make_anchor

    template = env.get_template(template_name)

    output = template.render(
        personal=personal_data["personal"],
        profile=personal_data["professional_profile"],
        executive=personal_data["executive_summary"],
        groups=groups,
        tech_index=tech_index,
        number_to_str=number_to_str,
        project_refs=project_refs,
    )

    out_path = Path(output_path) if output_path else DEFAULT_OUTPUT
    out_path.write_text(output, encoding="utf-8")
    print(f"Generated: {out_path}")
    print(f"  Projects: {sum(1 for g in groups for _ in ([g] if not g.get('sub_projects') else g['sub_projects']))} entries across {len(groups)} roles")

    # Render Technology Index as a separate file
    tech_template = env.get_template(TECH_INDEX_TEMPLATE)
    tech_output = tech_template.render(tech_index=tech_index)
    TECH_INDEX_OUTPUT.write_text(tech_output, encoding="utf-8")
    print(f"Generated: {TECH_INDEX_OUTPUT}")


def main():
    parser = argparse.ArgumentParser(description="Build CV.md from project JSON files")
    parser.add_argument("--output", help="Output path (default: CV.md)", default=None)
    parser.add_argument("--template", help="Template name (default: cv.md.j2)", default=DEFAULT_TEMPLATE)
    args = parser.parse_args()
    render(output_path=args.output, template_name=args.template)


if __name__ == "__main__":
    main()
