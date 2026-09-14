# Repository Map

Each entry is labelled with one of these categories:

| Label | Meaning |
|-------|---------|
| **Source** | Hand-maintained content. Edit these to change the CV. |
| **Generated** | Written by a script. Do not edit by hand. |
| **Infrastructure** | Build, validation, template, or configuration code. |
| **Published** | Served by GitHub Pages but not generated. |
| **Asset** | Binary or reference files (PDF, DOCX, images). |
| **Legacy** | Kept for reference. Not part of the current pipeline. |
| **Local only** | Untracked or ignored by Git. Not in the remote repository. |

## Top Level

| Path | Label | Description |
|------|-------|-------------|
| `CV.md` | Generated | Full CV and project portfolio. Output of `scripts/build_cv.py`. |
| `TECHNOLOGY_INDEX.md` | Generated | Technologies grouped by domain, with project references. Output of `scripts/build_cv.py`. |
| `Resume.md` | Published, Source | One-page resume with Jekyll front matter. Hand-maintained. No script reads or writes it. |
| `index.md` | Published, Source | GitHub Pages home page with a quick profile, certification links, and contact links. |
| `README.md` | Source | Two lines: title and the GitHub Pages URL. |
| `_config.yml` | Infrastructure | Jekyll configuration: theme, title, navigation, plugins. |
| `Makefile` | Infrastructure | `install`, `validate`, `build`, `pdf`, and `all` targets. |
| `requirements.txt` | Infrastructure | Python dependencies. Contains only `jinja2>=3.0.0`. |
| `.mdlrc`, `.mdl_style.rb` | Infrastructure | Markdown lint configuration. All rules are on except MD007, MD012, MD013, MD025, MD033, and MD036. |
| `.gitignore` | Infrastructure | Ignores `temp/`, `.vscode/`, OS files, Jekyll build output, and `.env` files. |

## `assets/`

| Path | Label | Description |
|------|-------|-------------|
| `assets/projects/project_N.json` | Source | 13 parent role files (projects 1 to 13). |
| `assets/projects/project_N.M.json` | Source | 35 sub-project files. |
| `assets/projects/project_template.json` | Source | Starting point for new project files. Includes placeholder `role_overview` and `parentsummary` blocks. Excluded from build and validation. |
| `assets/certificates/*.pdf` | Asset | Five certificate PDFs: four AWS and one Scrum Alliance. |
| `assets/certificates/README.md` | Published | Certificate list with expiry dates and AWS verification links. |
| `assets/images/*.png` | Asset | Certification badge images. |
| `assets/documents/Christian_Turner-CV.pdf` | Generated, Asset | PDF export of `CV.md` from `make pdf`. The file is dated November 2025, so it predates the March 2026 regeneration. |
| `assets/documents/Christian_Turner-Resume_2025.docx` and `.pdf` | Asset | Downloadable resume files linked from `Resume.md`. Maintained outside this repository. |

## `data/`

| Path | Label | Description |
|------|-------|-------------|
| `data/personal.json` | Source | Personal and contact details, professional profile, certifications, and executive summary. |
| `data/raw/cv_data.json` | Legacy | The single structured file created on March 3, 2026 by extracting `CV.md`. It was the seed for the per-project files. It uses an older schema (`description`, `tasks_performed`, `technical_environment`). |
| `data/raw/cv_schema_skeleton.json` | Legacy | Schema skeleton used for that extraction. |
| `data/raw/build_cv_data.py` | Legacy | 1,226-line script that builds `cv_data.json` from inline Python data. |
| `data/raw/changelog.md` | Legacy | Record of the mapping decisions made during the extraction. |

## `docs/`

| Path | Label | Description |
|------|-------|-------------|
| `docs/README.md` | Source | Documentation index, quick start, and repository structure. |
| `docs/cv-as-code-workflow.md` | Source | File roles, naming convention, and steps to add a role. |
| `docs/project-schema-reference.md` | Source | Field-by-field schema and validation rules for project files. |
| `docs/build-pipeline-reference.md` | Source | Build script internals, template variables, Make targets, and PDF export. |
| `docs/_working/` | Source | These orientation notes. Not published, because Jekyll skips directories that start with an underscore. |

Parts of the three reference guides are out of date. See [Current State and Gaps](./current-state-and-gaps.md).

## `scripts/`

| Path | Label | Description |
|------|-------|-------------|
| `scripts/build_cv.py` | Infrastructure | The build pipeline. Contains grouping, roll-up, technology index logic, and the `TECH_GROUP_MAP` dictionary (about 230 entries). |
| `scripts/validate.sh` | Infrastructure | Batch validator with `--verbose`, `--fail-fast`, and `--format json`. Not called by the Makefile. |
| `scripts/sync_from_cv_data.py` | Legacy | Regenerates every project file from `data/raw/cv_data.json` and deletes files that are not in it. **Destructive if run now.** See [Current State and Gaps](./current-state-and-gaps.md). |

## `templates/`

| Path | Label | Description |
|------|-------|-------------|
| `templates/cv.md.j2` | Infrastructure | Jinja2 layout for `CV.md`. |
| `templates/tech_index.md.j2` | Infrastructure | Jinja2 layout for `TECHNOLOGY_INDEX.md`. |

## `tests/`

| Path | Label | Description |
|------|-------|-------------|
| `tests/validators/validate-projects.sh` | Infrastructure | Single-file validator (591 lines, Bash and `jq`). Supports human, JSON, quiet, and verbose output. Exit codes: 0 pass, 1 fail, 2 usage error, 3 missing `jq` or rules. |
| `tests/validators/project-validation-rules.json` | Infrastructure | Data-driven validation rules. |
| `tests/validators/validate_date_ranges.py` | Infrastructure | Checks that sub-project dates fall within parent dates. Not called by the Makefile. |
| `tests/validators/README.md` | Source | Validator documentation. |
| `tests/scripts/run-all-validations.sh` | Infrastructure | Batch runner over `assets/projects/`. |
| `tests/scripts/run-ci-checks.sh` | Infrastructure | Wrapper around the batch runner, intended for Git hooks or CI. Nothing calls it. |
| `tests/fixtures/invalid/*.json` | Infrastructure | Two intentionally invalid project files for testing the validator. |
| `tests/fixtures/valid/` | Infrastructure | Empty directory. |
| `tests/fixtures/README.md` | Source | Describes the fixtures and their expected errors. |
| `tests/docs/*.md` | Legacy | November 2025 test execution reports and the Google Shell Style Guide refactoring notes. |

## Local-Only Content

These paths exist in the working copy but are not tracked by Git.

| Path | Description |
|------|-------------|
| `.claude/agents/nicole-hr-recruiter.md` | A Claude Code sub-agent persona ("Nicole", a corporate HR recruiter) that critiques resumes, CVs, and cover letters. |
| `.claude/agent-memory-local/nicole-hr-recruiter/MEMORY.md` | The agent's persistent notes on review rounds and the fixes applied. |
| `.claude/settings.local.json` | Local permission allowances for build and validation commands. |
| `temp/` | Ignored by Git. Contains the Nicole review reports, owner feedback (`User_Feedback.md`), and an `_archive/` folder with older drafts, Pandoc notes, images, and job application material. |
| `.vscode/` | Ignored by Git. Editor settings. |
