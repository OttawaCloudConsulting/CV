# CV as Code Workflow

## Overview

The CV repository uses a **file-driven pipeline** where structured JSON files are the single source of truth. `CV.md` is a **generated artifact** — it is never edited by hand. Adding a new consulting role means dropping a new JSON file into `assets/projects/` and running the build.

```
assets/projects/*.json  ──┐
data/personal.json      ──┼──► scripts/build_cv.py ──► CV.md (generated)
templates/cv.md.j2      ──┘
```

---

## File Roles

### Source of truth

| File/Directory | Role | Edit? |
|----------------|------|-------|
| `assets/projects/project_N.json` | Parent role: client, role, date range, outcomes | Yes |
| `assets/projects/project_N.M.json` | Sub-project: scoped technical deliverable | Yes |
| `data/personal.json` | Personal info, certifications, executive summary | Yes |

### Generated artifacts

| File | Generated from | Edit? |
|------|----------------|-------|
| `CV.md` | Project JSON files + `data/personal.json` | **Never** |

### Pipeline infrastructure

| File | Role | Edit? |
|------|-------|-------|
| `scripts/build_cv.py` | Build script | When pipeline changes needed |
| `templates/cv.md.j2` | Jinja2 CV template | When layout changes needed |
| `tests/validators/project-validation-rules.json` | Validation rules | When schema evolves |

### Legacy (read-only)

| File | Notes |
|------|-------|
| `data/raw/cv_data.json` | Original monolithic JSON; used as backfill reference |
| `data/raw/build_cv_data.py` | Predecessor build script; superseded by `scripts/build_cv.py` |

---

## File Naming Convention

### Parent role files — `project_N.json`

A file with an **integer** project number is a **parent role file**. It represents a consulting engagement at a specific client, covering the role title, date range, overall outcomes, and technology stack.

```
project_13.json    →  Project 13 (Shared Services Canada)
project_12.json    →  Project 12 (Agriculture Canada)
```

### Sub-project deliverable files — `project_N.M.json`

A file with a **decimal** project number is a **sub-project deliverable file**. It captures specific technical work within a parent engagement, with its own challenge, solution, outcomes, and technologies.

```
project_13.1.json  →  Sub-project 13.1 (Cloud Platform Engineering)
project_13.2.json  →  Sub-project 13.2 (Automation and Orchestration Framework)
```

### Discovery rule

The build script automatically groups sub-projects under their parent by matching the integer prefix:

- `floor(13.1) == 13` → sub-project 13.1 belongs to parent 13
- `floor(13.2) == 13` → sub-project 13.2 belongs to parent 13

**Projects with only sub-project files** (no parent `project_N.json`) get a synthesized parent header derived from the first sub-project's client and the combined date range of all sub-projects.

---

## Adding a New Role

### Step 1 — Create the parent file

```bash
cp assets/projects/project_template.json assets/projects/project_14.json
```

Edit `project_14.json`. At minimum fill in:

- `number` — integer, one higher than the current highest (or next logical number)
- `title` — descriptive name, e.g. `"[Client Redacted] - Cloud Platform Engineering"`
- `client.name`, `client.department`, `client.team`
- `role` — your job title for this engagement
- `date_range.start` and `date_range.end` — format: `"Month YYYY"` or `"Current"`
- `challenge.summary` — one-paragraph description of what the client needed
- `solution.summary` + `solution.deliverables` — what you delivered
- `outcomes` — quantified achievements, each starting with `✅`
- `technologies` — categorized tech stack

### Step 2 — Add sub-project files (optional but recommended)

For engagements with distinct technical work streams:

```bash
cp assets/projects/project_template.json assets/projects/project_14.1.json
```

Set `"number": 14.1` and fill in the deliverable-specific details. Repeat for `14.2`, `14.3`, etc.

### Step 3 — Validate

```bash
make validate
```

All project files must pass before building. Fix any errors reported before proceeding.

### Step 4 — Build

```bash
make build
```

This regenerates `CV.md` from all project files plus `data/personal.json`.

### Step 5 — Review

Open `CV.md` and verify the new role appears correctly in the Professional Experience section and in the Technology Index.

### Step 6 — Commit

```bash
git add assets/projects/project_14*.json CV.md
git commit -m "Add project 14: [Client] - [Role Summary]"
```

---

## Updating Personal Information

Personal details are stored in `data/personal.json`. This file is hand-maintained and covers:

- Contact info (name, email, phone, location, links)
- Professional profile summary paragraphs
- Certifications list
- Executive summary key-value pairs

After editing `data/personal.json`, regenerate:

```bash
make build
```

---

## Updating the CV Layout

The CV layout is controlled by `templates/cv.md.j2` — a Jinja2 template. To change:

- Section order, headings, or overall structure: edit the template
- Technology Index format: the template auto-generates from project data
- Table of Contents: auto-generated from project groups

After editing the template, rebuild:

```bash
make build
```

> **Do not edit `CV.md` directly.** Template changes survive rebuilds; manual edits to `CV.md` do not.

---

## Numbering Convention

Projects are numbered in **reverse chronological order** — higher numbers are more recent:

| Number | Client | Period |
|--------|--------|--------|
| 13 | Shared Services Canada (Cloud Platform Engineering) | September 2023 – Current |
| 12 | Agriculture Canada (Cloud Centre of Expertise) | January 2021 – September 2023 |
| 11 | Shared Services Canada (CSD R&D) | September 2019 – January 2021 |
| ... | ... | ... |
| 1 | Central Wire Industries | May 2007 – September 2011 |

When adding a new engagement, assign it the next integer above the current highest.

---

## Validation

All project JSON files must pass validation before building. Validation is driven by `tests/validators/project-validation-rules.json` — no script changes needed to add or modify rules.

```bash
# Validate all files
make validate

# Validate a single file
bash tests/validators/validate-projects.sh assets/projects/project_14.json

# Verbose output (shows each check)
bash tests/validators/validate-projects.sh assets/projects/project_14.json --verbose

# JSON report
bash tests/validators/validate-projects.sh assets/projects/project_14.json --format json
```

See [Project Schema Reference](./project-schema-reference.md) for full field requirements and validation rules.

---

## Phasing

| Phase | Status | Description |
|-------|--------|-------------|
| **Phase 1** | ✅ Complete | `CV.md` generated from project files |
| **Phase 2** | Planned | `Resume.md` auto-generated from top projects + personal data |
| **Phase 3** | Planned | GitHub Actions: auto-build on push to `dev` |
