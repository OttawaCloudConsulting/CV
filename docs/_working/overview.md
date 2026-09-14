# Project Overview

## What This Project Is

This repository is a **"CV as Code"** system for Christian Turner, a Senior Cloud Architect and DevSecOps Specialist.

It stores a professional career history as structured JSON data and generates a long-form Markdown CV from that data. The generated documents are published as a static website through GitHub Pages at <https://ottawacloudconsulting.github.io/CV/>.

The approach treats the CV like software:

- **Data is the source of truth.** Each consulting engagement and each deliverable within it is a JSON file.
- **Documents are build artifacts.** `CV.md` and `TECHNOLOGY_INDEX.md` are rendered from templates and are not edited by hand.
- **Changes are validated.** A rule-driven validator checks every project file before a build.
- **History is version-controlled.** Every edit to the career record is a Git commit.

## What It Does

1. Holds 13 career roles (2007 to present) and 35 sub-project deliverables as JSON files in `assets/projects/`.
1. Holds personal details, a professional profile, certifications, and an executive summary in `data/personal.json`.
1. Validates the project files against rules in `tests/validators/project-validation-rules.json`.
1. Renders `CV.md` (full project portfolio) and `TECHNOLOGY_INDEX.md` (technologies grouped by domain, cross-referenced to project numbers) with Python and Jinja2.
1. Optionally exports `CV.md` to PDF with Pandoc and XeLaTeX.
1. Publishes the Markdown pages through GitHub Pages using the `jekyll-theme-minimal` theme.

## Audience

| Audience | What they use |
|----------|---------------|
| Recruiters and hiring managers | The one-page `Resume.md`, and the PDF and DOCX files in `assets/documents/` |
| Technical evaluators and procurement (for example, Government of Canada bids) | The long-form `CV.md` with per-deliverable challenge, solution, outcomes, and technical environment |
| Keyword and skills matching | `TECHNOLOGY_INDEX.md`, which maps each technology to the projects that used it |
| The repository owner | The JSON files, templates, Makefile, and validators |

## Published Site

`_config.yml` configures the site. Navigation has three entries:

| Page | Source file | Generated? |
|------|-------------|------------|
| Home | `index.md` | No, hand-maintained |
| Full CV | `CV.md` | Yes, by `scripts/build_cv.py` |
| Resume | `Resume.md` | No, hand-maintained |

`CV.md` links to `TECHNOLOGY_INDEX.md`, which is also generated. `index.md` and `CV.md` link to the certificate PDFs in `assets/certificates/`.

## Headline Numbers

These figures were measured on the `revision` branch at commit `9018d47`.

| Measure | Value |
|---------|-------|
| Career roles (parent project files) | 13 |
| Sub-project deliverables | 35 |
| Project JSON files (excluding template) | 48 |
| Files passing `make validate` | 48 of 48 |
| Sub-projects passing date range validation | 35 of 35 |
| Technology index entries | 238 |
| Technology index entries in "Uncategorised" | 23 |
| Lines in generated `CV.md` | 1,511 |
| Certifications listed | 5 (4 AWS, 1 Scrum Alliance) |

## Career Coverage

Project numbers increase with time. Higher numbers are more recent.

| No. | Client | Period | Sub-projects |
|-----|--------|--------|--------------|
| 13 | Shared Services Canada | September 2023 to Current | 2 |
| 12 | Agriculture Canada | January 2021 to September 2023 | 2 |
| 11 | Shared Services Canada | September 2019 to January 2021 | 1 |
| 10 | Department of National Defence | February 2019 to December 2020 | 1 |
| 9 | IDS Data Systems (New Democratic Party) | November 2018 to January 2019 | 2 |
| 8 | Shared Services Canada | January 2018 to February 2019 | 2 |
| 7 | Brookfield Renewable Energy | September 2017 to December 2017 | 1 |
| 6 | Lowe Martin Group | March 2017 to September 2017 | 2 |
| 5 | HighRoads (US, Boston) | January 2017 to April 2017 | 2 |
| 4 | HighRoads Canada Inc. | June 2015 to December 2016 | 4 |
| 3 | Dymon Corporation | December 2014 to June 2015 | 3 |
| 2 | GeoDigital International | September 2011 to December 2014 | 8 |
| 1 | Central Wire Industries | May 2007 to September 2011 | 5 |

Some engagements overlap in time (for example, projects 10 and 11, and projects 8 and 9). This reflects concurrent or part-time contracts.

## Technology Stack

| Concern | Tool |
|---------|------|
| Data format | JSON |
| Build script | Python 3 (`scripts/build_cv.py`) |
| Templating | Jinja2 (the only entry in `requirements.txt`) |
| Validation | Bash and `jq` (`tests/validators/validate-projects.sh`), plus Python (`validate_date_ranges.py`) |
| Task runner | GNU Make |
| PDF export | Pandoc with XeLaTeX |
| Markdown linting | `mdl` with `.mdl_style.rb` |
| Hosting | GitHub Pages with Jekyll (`jekyll-theme-minimal`, `kramdown`) |

## Project History in Brief

| Period | Milestone |
|--------|-----------|
| November 2025 | Repository created. `CV.md` and `Resume.md` hand-written. Validation framework and test fixtures added. |
| March 3, 2026 | All `CV.md` content extracted into a single structured file, `data/raw/cv_data.json`. |
| March 4, 2026 | Data split into one JSON file per project. `scripts/build_cv.py` and the Jinja2 template introduced. `CV.md` becomes generated. |
| March 9, 2026 | Owner feedback and content review cycles (commits `fa317ef`, `514fbf1`, `aa26dd9`, `f59f810`). Emoji removed from outcomes. `role_overview` and `parentsummary` fields added. Technology index moved to its own file and grouped by domain. |
| March 10 to 11, 2026 | Markdown lint rules added. Projects 1 and 2 expanded with new sub-projects (1.3 to 1.5, 2.7, 2.8). |

## Where to Go Next

- For how the build works, read [Architecture and Data Flow](./architecture-and-dataflow.md).
- For what each file does, read [Repository Map](./repository-map.md).
- For known issues and out-of-date documentation, read [Current State and Gaps](./current-state-and-gaps.md).
