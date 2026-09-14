# Current State and Gaps

This document records where the documentation, tests, and tooling no longer match the code. Each finding includes how it was checked, so it can be checked again.

All findings were observed on the `revision` branch at commit `9018d47`. Nothing was changed to produce them.

## Summary

| # | Finding | Severity |
|---|---------|----------|
| 1 | `scripts/sync_from_cv_data.py` would overwrite current project data with an older schema | High |
| 2 | `role_overview` and `parentsummary` are central to the build but undocumented and unvalidated | Medium |
| 3 | The schema guide still requires a `✅` prefix on outcomes, which was removed | Medium |
| 4 | The pipeline guide describes one output, but the build writes two | Medium |
| 5 | Parent `challenge`, `solution`, and `outcomes` are required but never rendered | Low |
| 6 | Date range validation exists but no Make target runs it | Low |
| 7 | Three overlapping batch validators exist, and the CI script has no caller | Low |
| 8 | Test fixture documentation and test reports are out of date | Low |
| 9 | The technology grouping map needs manual upkeep, and 23 entries are uncategorised | Low |
| 10 | Planned phases 2 and 3 have not started | Informational |
| 11 | Some published and generated files carry stale dates | Low |
| 12 | The `dev` branch holds only the initial commit | Informational |

## What Works

- All 48 project files pass `make validate`.
- All 35 sub-projects pass `validate_date_ranges.py`.
- A clean rebuild from the committed inputs reproduces the committed `CV.md` and `TECHNOLOGY_INDEX.md` exactly. See [Architecture and Data Flow](./architecture-and-dataflow.md#reproducibility).
- The generated `CV.md` contains no `✅` characters, which matches the owner's March 2026 request to remove emoji.

## Findings

### 1. `sync_from_cv_data.py` is destructive if run today

`scripts/sync_from_cv_data.py` reads `data/raw/cv_data.json` and then:

- rewrites every `project_N.json` and `project_N.M.json` file,
- deletes any project file that is not defined in `cv_data.json`,
- writes the older schema, with no `role_overview` or `parentsummary`,
- adds `✅` back to outcomes through `split_outcomes()`, and
- replaces real parent challenge and solution text with synthesised text.

Since the sync was last useful, the project files have been heavily edited. Sub-projects 1.3, 1.4, 1.5, 2.7, and 2.8 were also added on March 11, 2026. Running the script (without `--dry-run`) would discard that work. Git history would allow recovery, but only for committed changes.

`docs/cv-as-code-workflow.md` calls `data/raw/` legacy, but it does not mention this script.

### 2. `role_overview` and `parentsummary` are undocumented and unvalidated

Checked with `jq` across all project files:

- All 13 parent files have `role_overview`.
- All 35 sub-project files have `parentsummary`.

`build_cv.py` (in `build_project_groups`) combines the sub-projects' `parentsummary` values into the parent's `role_overview`. The template renders the result as "Workstream Deliverables" and "Engagement Outcomes". This roll-up is what each role section in `CV.md` shows first.

Gaps:

- `docs/project-schema-reference.md` does not mention either field.
- `project-validation-rules.json` has no rules for either field.
- If a sub-project omits `parentsummary`, the build skips it silently, and the parent roll-up is shorter with no warning.
- If a parent omits `role_overview`, the whole roll-up block is silently left out.

The template file `assets/projects/project_template.json` does include both fields, with guidance text.

### 3. The outcome emoji rule was removed, but the guides still require it

Evidence:

- `project-validation-rules.json` has no `emoji_prefix` rule in `constraint_validation`.
- `grep -c '✅' CV.md` returns `0`.
- Commit `514fbf1` removed seven lines from the rules file. The local agent memory notes that the rule was removed when emoji were stripped from 120 outcomes.

Documents that still require `✅`:

- `docs/project-schema-reference.md` (field reference, constraint table, and examples)
- `docs/cv-as-code-workflow.md` (step 1 of "Adding a New Role")
- `tests/validators/README.md` (constraint list and example)
- `tests/fixtures/README.md` (expected errors)

`tests/validators/validate-projects.sh` still has an `emoji_prefix` branch near line 371. No rule uses it now.

### 4. The build writes two files, not one

`docs/build-pipeline-reference.md` and `docs/cv-as-code-workflow.md` describe the Technology Index as a section at the bottom of `CV.md`.

The build now writes it to a separate file, `TECHNOLOGY_INDEX.md`, using `templates/tech_index.md.j2`. It is grouped by domain (`build_grouped_tech_index`), not by first letter. `CV.md` links to it from the table of contents.

Other details missing from the pipeline guide:

- `build_grouped_tech_index`, `TECH_GROUP_MAP`, and `TECH_GROUPS_ORDER`.
- `--output` changes only the `CV.md` path. `TECHNOLOGY_INDEX.md` is always written to the repository root.
- `build_tech_index` still runs and its result is passed to `cv.md.j2` as `tech_index`, but the template no longer uses it.
- The documented "Executive Summary" example includes `certifications` and `consulting_entity` keys. Both were removed from `data/personal.json` and the template.
- The "Repository Structure" tree in `docs/README.md` does not list `TECHNOLOGY_INDEX.md`, `templates/tech_index.md.j2`, `scripts/validate.sh`, `scripts/sync_from_cv_data.py`, or `validate_date_ranges.py`.

### 5. Parent narrative fields are required but not rendered

Validation requires `challenge.summary`, `solution.summary`, `solution.deliverables`, `outcomes`, and `technologies` on every file, including parents.

The template renders the parent's `challenge`, `solution`, and `outcomes` only when the parent has no sub-projects. Every current parent has sub-projects, so this content never appears in `CV.md`. Parent `technologies` do still feed the technology index.

As a result, parent files hold content that the owner must maintain but that no reader sees. For example, `project_13.json` has six detailed outcome statements that are not in the CV.

### 6. Date range validation is not wired in

`tests/validators/validate_date_ranges.py` passes (35 checked, 0 violations), but:

- `make validate` does not run it,
- `make all` does not run it, and
- no guide in `docs/` mentions it.

### 7. Overlapping validation entry points

Three scripts validate all project files in a batch:

| Entry point | Called by |
|-------------|-----------|
| Inline loop in `Makefile` (`make validate`) | The owner, and `make all` |
| `scripts/validate.sh` | Nothing |
| `tests/scripts/run-all-validations.sh` | `tests/scripts/run-ci-checks.sh` |

There is no `.github/` directory and no Git hook, so `run-ci-checks.sh` has no caller.

### 8. Test fixtures and reports are out of date

Running each invalid fixture through the validator gives different error counts from those documented:

| Fixture | Documented errors | Actual errors |
|---------|-------------------|---------------|
| `project_invalid_missing_emoji.json` | 3 | 5 |
| `project_comprehensive_failures.json` | 8 | 10 |

The documented counts include the removed emoji check. They do not include the `date_range` required-field checks, which were added later.

Other drift:

- `tests/fixtures/valid/` is empty. `tests/validators/README.md` lists `project_valid_minimal.json` and `project_valid_full.json`, and three more invalid fixtures, but none of these exist.
- `tests/docs/*.md` (November 2025) report results against 27 production files. There are now 48.
- There is no automated test that runs the fixtures and compares results with expected output.
- `build_cv.py` has no tests.

### 9. Technology grouping needs manual upkeep

`TECH_GROUP_MAP` in `build_cv.py` is a hand-written dictionary of about 230 technology names. A name not in the map is assigned by prefix only for AWS and Azure. Everything else goes to "Uncategorised".

`TECHNOLOGY_INDEX.md` currently has 23 uncategorised entries. Examples are `ITIL`, `Cisco VPN`, `Veritas Backup Exec`, `Microsoft SharePoint`, and three Avaya telephony items. Most came from the sub-projects added on March 11, 2026.

The map is also sensitive to spelling. For example, `Lawson Movex (M3)` is mapped, but `Lawson MOVEX (M3)` is uncategorised. `Info BPCS` is mapped, but `INFOR BPCS` is uncategorised.

The `category` values inside each project file's `technologies` are not used for grouping.

### 10. Planned phases have not started

`docs/cv-as-code-workflow.md` lists:

| Phase | Plan | Status found |
|-------|------|--------------|
| 1 | Generate `CV.md` from project files | Done |
| 2 | Generate `Resume.md` from top projects and personal data | Not started. No script or template references `Resume.md`. |
| 3 | GitHub Actions build on push to `dev` | Not started. No `.github/` directory. |

### 11. Stale dates and derived files

| Item | Observation |
|------|-------------|
| `templates/cv.md.j2` and `templates/tech_index.md.j2` | The footer "Last updated: March 2026" is hard-coded, not derived from the build date |
| `index.md` | "Last Updated: November 2025" |
| `assets/documents/Christian_Turner-CV.pdf` | File dated November 15, 2025, before the March 2026 regeneration. It does not reflect the current `CV.md`. |
| `Resume.md` | Says "14+ years". `CV.md` and `index.md` say "15+ years". |
| `docs/build-pipeline-reference.md` | Refers to `temp/automation/pandoc/...`. That content is now in `temp/_archive/automation/pandoc/`, which Git ignores. |

### 12. Branch layout

- `revision` (current branch) is 40 commits ahead of `dev` and 0 behind.
- `dev` contains only the initial commit, but it is the configured default branch for pull requests.
- `main` has a separate history of formatting commits (for example, "fix typo" and "bullet point certs").

Which branch GitHub Pages serves could not be confirmed from the repository.

## Suggested Follow-Ups

These are suggestions only. None of them were carried out.

1. Delete `scripts/sync_from_cv_data.py`, or add a clear guard and warning to it.
1. Add `role_overview` and `parentsummary` to `docs/project-schema-reference.md` and to the validation rules.
1. Remove the `✅` requirement from the guides and fixture README, and remove the unused `emoji_prefix` branch from the validator.
1. Update `docs/build-pipeline-reference.md` and `docs/README.md` to cover `TECHNOLOGY_INDEX.md` and grouped indexing.
1. Add `validate_date_ranges.py` to `make validate`, and keep one batch validator.
1. Decide whether parent `challenge`, `solution`, and `outcomes` should be rendered, made optional, or removed.
1. Add valid fixtures and a fixture test runner with expected error counts.
1. Add the 23 uncategorised technologies to `TECH_GROUP_MAP`, or group by each item's `category` field instead.
1. Regenerate the CV PDF, and derive "Last updated" dates at build time.
1. Merge `revision` into `dev`, and add a GitHub Actions workflow for validate and build.
