#!/usr/bin/env python3
"""
sync_from_cv_data.py — Synchronize assets/projects/ from data/raw/cv_data.json.

This is a one-time (and repeatable) synchronization tool that rebuilds all
project JSON files from the canonical cv_data.json source of truth.

What it does:
  1. Reads data/raw/cv_data.json
  2. For every parent project: writes assets/projects/project_N.json
  3. For every sub-project:   writes assets/projects/project_N.M.json
  4. Deletes any orphaned/misaligned project files not defined in cv_data.json
  5. Writes assets/projects/project_template.json (preserving the template)

Run:
    python3 scripts/sync_from_cv_data.py [--dry-run]

Options:
    --dry-run   Show what would be written/deleted without making changes
"""

import json
import math
import re
import argparse
import shutil
from collections import OrderedDict
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
CV_DATA_FILE = REPO_ROOT / "data" / "raw" / "cv_data.json"
PROJECTS_DIR = REPO_ROOT / "assets" / "projects"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def split_outcomes(text):
    """
    Convert a prose outcomes string into a list of ✅-prefixed bullet strings.
    Splits on '. ' boundaries; filters trivially short segments.
    """
    if not text or not text.strip():
        return []
    # Split on period-space boundary, keeping text clean
    parts = re.split(r'\.\s+', text.strip())
    results = []
    for part in parts:
        part = part.strip().rstrip('.')
        if len(part) > 15:  # skip very short fragments
            if not part.startswith('✅'):
                part = f"✅ {part}"
            results.append(part)
    return results if results else [f"✅ {text.strip().rstrip('.')}"]


def aggregate_technologies(sub_projects):
    """
    Aggregate technical_environment categories from all sub-projects into a
    deduplicated technologies list using the project schema format.
    """
    cat_items = OrderedDict()
    for sub in sub_projects:
        for tech_group in sub.get("technical_environment", []):
            cat = tech_group.get("category", "Other")
            items = tech_group.get("items", [])
            if cat not in cat_items:
                cat_items[cat] = []
            for item in items:
                if item and item not in cat_items[cat]:
                    cat_items[cat].append(item)
    return [{"category": cat, "items": items}
            for cat, items in cat_items.items() if items]


def map_technologies(technical_environment):
    """Map a single sub-project's technical_environment to project schema format."""
    result = []
    for group in technical_environment:
        cat = group.get("category", "Other")
        items = [i for i in group.get("items", []) if i]
        if items:
            result.append({"category": cat, "items": items})
    return result


def tasks_to_deliverables(tasks_performed):
    """Extract main task names (not sub-tasks) as deliverable bullet strings."""
    deliverables = []
    for task_obj in tasks_performed:
        task = task_obj.get("task", "").strip()
        if task:
            deliverables.append(task)
    return deliverables if deliverables else ["Project deliverables completed per scope"]


def build_parent_file(project, sub_projects_data):
    """
    Build a parent project_N.json dict from cv_data project + sub-projects.
    Parent-level outcomes/challenge are synthesized from sub-project data.
    """
    # Aggregate outcomes from sub-projects
    all_outcomes = []
    for sub in sub_projects_data:
        outcomes = sub.get("outcomes", "")
        if isinstance(outcomes, str) and outcomes.strip():
            all_outcomes.extend(split_outcomes(outcomes))
        elif isinstance(outcomes, list):
            for o in outcomes:
                if o and not o.startswith("✅"):
                    all_outcomes.append(f"✅ {o}")
                elif o:
                    all_outcomes.append(o)

    # If still empty, synthesize from sub-project titles
    if not all_outcomes:
        for sub in sub_projects_data:
            title = sub.get("title", "").strip()
            if title:
                all_outcomes.append(f"✅ Delivered {title} engagement")

    # Ensure at least one outcome
    if not all_outcomes:
        all_outcomes = [f"✅ Successfully delivered {project['title']} engagement"]

    # Aggregate technologies
    technologies = aggregate_technologies(sub_projects_data)

    # Synthesize challenge summary from first sub-project description
    challenge_summary = ""
    for sub in sub_projects_data:
        desc = sub.get("description", "").strip()
        if desc and len(desc) > 30:
            challenge_summary = desc
            break
    if not challenge_summary:
        challenge_summary = (
            f"{project['client']['name']} required cloud architecture, "
            f"DevOps, and infrastructure expertise to meet technical and "
            f"compliance requirements."
        )

    # Solution: sub-project titles as deliverables
    sub_titles = [sub.get("title", "") for sub in sub_projects_data if sub.get("title")]
    if not sub_titles:
        sub_titles = ["Cloud architecture and DevOps deliverables"]

    # Client structure
    client = {
        "name": project["client"]["name"],
        "department": project["client"].get("department", ""),
        "team": project["client"].get("team", ""),
    }

    # Fallback technologies
    if not technologies:
        technologies = [{"category": "Cloud Services", "items": ["Amazon AWS"]}]

    return OrderedDict([
        ("number", project["number"]),
        ("title", project["title"]),
        ("client", client),
        ("role", project["role"]),
        ("date_range", {
            "start": project["date_range"]["start"],
            "end": project["date_range"]["end"],
        }),
        ("challenge", {"summary": challenge_summary}),
        ("solution", {
            "summary": "Delivered comprehensive cloud and infrastructure solutions across:",
            "deliverables": sub_titles,
        }),
        ("outcomes", all_outcomes),
        ("technologies", technologies),
    ])


def build_sub_project_file(sub, parent_project):
    """
    Build a sub-project_N.M.json dict from cv_data sub-project + parent context.
    """
    # Number: convert string like "13.1" to float 13.1
    num_str = str(sub["number"])
    try:
        number = float(num_str)
    except ValueError:
        number = float(num_str.replace(",", "."))

    # Client from parent
    client = {
        "name": parent_project["client"]["name"],
        "department": parent_project["client"].get("department", ""),
        "team": parent_project["client"].get("team", ""),
    }

    # Challenge: sub-project description
    description = sub.get("description", "").strip()
    if not description or len(description) < 20:
        description = (
            f"{parent_project['client']['name']} required {sub.get('title', 'technical')} "
            f"expertise to meet project objectives."
        )

    # Solution deliverables from tasks_performed
    tasks = sub.get("tasks_performed", [])
    deliverables = tasks_to_deliverables(tasks)

    # Outcomes
    raw_outcomes = sub.get("outcomes", "")
    if isinstance(raw_outcomes, str) and raw_outcomes.strip():
        outcomes = split_outcomes(raw_outcomes)
    elif isinstance(raw_outcomes, list) and raw_outcomes:
        outcomes = []
        for o in raw_outcomes:
            if o and not o.startswith("✅"):
                outcomes.append(f"✅ {o}")
            elif o:
                outcomes.append(o)
    else:
        # Synthesize outcomes from tasks
        outcomes = []
        for task_obj in tasks[:3]:
            task = task_obj.get("task", "").strip()
            if task:
                outcomes.append(f"✅ {task}")
        if not outcomes:
            outcomes = [f"✅ Successfully delivered {sub.get('title', 'project engagement')}"]

    # Technologies
    technologies = map_technologies(sub.get("technical_environment", []))
    if not technologies:
        technologies = [{"category": "Cloud Services", "items": ["Amazon AWS"]}]

    return OrderedDict([
        ("number", number),
        ("title", sub["title"]),
        ("client", client),
        ("role", parent_project["role"]),
        ("date_range", {
            "start": sub["date_range"]["start"],
            "end": sub["date_range"]["end"],
        }),
        ("challenge", {"summary": description}),
        ("solution", {
            "summary": "Key activities and deliverables:",
            "deliverables": deliverables,
        }),
        ("outcomes", outcomes),
        ("technologies", technologies),
    ])


def write_project_file(path, data, dry_run=False):
    """Serialize and write a project dict to a JSON file."""
    content = json.dumps({"project": data}, indent=2, ensure_ascii=False) + "\n"
    if dry_run:
        print(f"  [DRY RUN] Would write: {path.name}")
        return
    path.write_text(content, encoding="utf-8")
    print(f"  Written: {path.name}")


def delete_file(path, dry_run=False):
    if dry_run:
        print(f"  [DRY RUN] Would delete: {path.name}")
        return
    path.unlink()
    print(f"  Deleted: {path.name}")


# ---------------------------------------------------------------------------
# Main sync logic
# ---------------------------------------------------------------------------

def sync(dry_run=False):
    print("=" * 60)
    print("CV Data → Project Files Synchronization")
    print("=" * 60)

    # Load cv_data.json
    with open(CV_DATA_FILE) as f:
        cv_data = json.load(f)

    projects = cv_data["projects"]

    # Build the set of expected filenames from cv_data
    expected_files = {"project_template.json"}

    print(f"\nProcessing {len(projects)} projects from cv_data.json...\n")

    for project in projects:
        parent_num = project["number"]
        parent_filename = f"project_{parent_num}.json"
        expected_files.add(parent_filename)

        sub_projects = project.get("sub_projects", [])

        print(f"Project {parent_num}: {project['title']}")

        # ---- Write parent file ----
        parent_path = PROJECTS_DIR / parent_filename
        parent_data = build_parent_file(project, sub_projects)
        write_project_file(parent_path, parent_data, dry_run=dry_run)

        # ---- Write sub-project files ----
        for sub in sub_projects:
            num_str = str(sub["number"])
            sub_filename = f"project_{num_str}.json"
            expected_files.add(sub_filename)

            sub_path = PROJECTS_DIR / sub_filename
            sub_data = build_sub_project_file(sub, project)
            write_project_file(sub_path, sub_data, dry_run=dry_run)

        print()

    # ---- Delete orphaned files ----
    existing = set(p.name for p in PROJECTS_DIR.glob("project_*.json"))
    orphaned = existing - expected_files

    if orphaned:
        print(f"Deleting {len(orphaned)} orphaned file(s):")
        for name in sorted(orphaned):
            delete_file(PROJECTS_DIR / name, dry_run=dry_run)
        print()

    print("=" * 60)
    print(f"Sync complete.")
    print(f"  Expected files: {len(expected_files) - 1} project files + template")
    print(f"  Orphaned deleted: {len(orphaned)}")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Sync project files from cv_data.json")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would change without writing files")
    args = parser.parse_args()
    sync(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
