# Build Pipeline Reference

## Overview

The build pipeline converts structured JSON project files into `CV.md` using a Python build script and a Jinja2 template.

```
assets/projects/project_*.json  ──┐
data/personal.json              ──┼──► scripts/build_cv.py ──► CV.md
templates/cv.md.j2              ──┘
```

---

## Makefile Targets

The `Makefile` at the repository root provides convenience targets:

| Target | Command | Description |
|--------|---------|-------------|
| `make build` | `python3 scripts/build_cv.py` | Generate `CV.md` |
| `make validate` | (shell loop) | Validate all project JSON files |
| `make pdf` | `pandoc CV.md -o ...` | Export `CV.md` to PDF via Pandoc + XeLaTeX |
| `make install` | `pip install -r requirements.txt` | Install Python dependencies |
| `make all` | validate → build → pdf | Full pipeline |

### Installing dependencies

```bash
make install
# or
pip install -r requirements.txt
```

Jinja2 is the only Python dependency. `jq` is required for validation (separate install):

```bash
brew install jq  # macOS
sudo apt-get install jq  # Ubuntu/Debian
```

---

## Build Script: `scripts/build_cv.py`

### Usage

```bash
# Default: writes to CV.md in repo root
python3 scripts/build_cv.py

# Custom output path
python3 scripts/build_cv.py --output /tmp/CV_preview.md

# Custom template
python3 scripts/build_cv.py --template custom.md.j2
```

### Command-line arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--output PATH` | `CV.md` | Output file path |
| `--template NAME` | `cv.md.j2` | Template filename (looked up in `templates/`) |

### Algorithm

1. **Load personal data** from `data/personal.json`
2. **Glob project files** — all `assets/projects/project_*.json` excluding `project_template.json`
3. **Classify files**:
   - Integer `number` (e.g., `13`) → parent role file
   - Decimal `number` (e.g., `13.1`) → sub-project deliverable file
4. **Group sub-projects under parents** by matching `floor(sub.number) == parent.number`
5. **Handle orphan sub-projects** — sub-projects with no matching parent file get a synthesized parent derived from:
   - Client info: first sub-project's `client` object
   - Role: first sub-project's `role`
   - Date range: earliest `start` and latest `end` across all sub-projects
6. **Sort project groups** by parent number, descending (most recent first)
7. **Build Technology Index** — aggregates all `technologies[].items` from all project files, keyed by first letter, with project number references
8. **Render template** using Jinja2 with `trim_blocks=True, lstrip_blocks=True`
9. **Write output** to the specified file

### Key functions

| Function | Description |
|----------|-------------|
| `load_personal()` | Reads `data/personal.json` |
| `load_projects()` | Globs and deserializes all project files |
| `is_parent(number)` | Returns `True` if number is an integer |
| `number_to_str(number)` | Formats `13.0 → "13"`, `13.1 → "13.1"` |
| `build_project_groups(projects)` | Groups, synthesizes orphans, sorts |
| `build_tech_index(groups)` | Aggregates technologies alphabetically |
| `render(output_path, template_name)` | Full pipeline orchestration |

### Template context variables

These variables are available inside `templates/cv.md.j2`:

| Variable | Type | Source |
|----------|------|--------|
| `personal` | dict | `data/personal.json` → `personal` key |
| `profile` | dict | `data/personal.json` → `professional_profile` key |
| `executive` | dict | `data/personal.json` → `executive_summary` key |
| `groups` | list of dicts | Processed project groups |
| `tech_index` | dict (letter → list) | Auto-aggregated technology index |
| `number_to_str` | function | Formats project numbers for display |
| `project_refs` | function | Formats a set of numbers as "Project N" / "Projects N, M" |

#### Group dict structure

Each element of `groups` has the following keys:

```python
{
    "number": 13,               # int
    "_number_str": "13",        # str, for display
    "title": "...",
    "client": {"name": ..., "department": ..., "team": ...},
    "role": "...",
    "date_range": {"start": "...", "end": "..."},
    "challenge": {"summary": "..."},   # None for synthesized parents
    "solution": {...},                 # None for synthesized parents
    "outcomes": [...],
    "technologies": [...],
    "sub_projects": [...],      # list of sub-project dicts (may be empty)
    "_synthesised": True,       # only present for synthesized parents
}
```

### Custom Jinja2 filter

| Filter | Usage | Description |
|--------|-------|-------------|
| `anchor` | `"Heading Text" \| anchor` | Generates a GFM Markdown anchor (lowercase, spaces → hyphens, non-alphanumeric removed) |

---

## Template: `templates/cv.md.j2`

The Jinja2 template controls the Markdown layout of `CV.md`. It uses `trim_blocks=True` and `lstrip_blocks=True` to suppress extra blank lines from block tags.

### Template sections

| Section | Template lines | Source data |
|---------|---------------|-------------|
| Document header | Top | `personal` |
| Professional Profile | After header | `profile.summary`, `profile.certifications` |
| Executive Summary | After profile | `executive` |
| Table of Contents | Auto-generated | `groups` |
| Professional Experience | Main body | `groups`, `groups[].sub_projects` |
| Technology Index | Bottom | `tech_index` |

### Rendering logic for project groups

The template uses conditional logic to handle three project types:

**1. Parent with sub-projects**

```jinja2
{% if group.sub_projects %}
  {# Render parent header (client, role, date) #}
  {# For each sub-project: render challenge, solution, outcomes, tech #}
{% endif %}
```

**2. Parent without sub-projects (standalone)**

```jinja2
{% if not group.sub_projects %}
  {# Render challenge, solution, outcomes, tech directly under parent header #}
{% endif %}
```

**3. Synthesized parent (orphan sub-projects)**

The synthesized parent is treated as a parent-with-sub-projects. The `_synthesised` flag is present but not required by the template; the template handles it via the same `sub_projects` path.

### Editing the template

To change the CV layout, edit `templates/cv.md.j2` and rebuild:

```bash
make build
```

Common changes:

- **Reorder sections** — move Jinja blocks within the file
- **Change heading levels** — adjust `##` / `###` prefixes
- **Add a new section** — add a `{% block %}` or inline content using available context variables
- **Change Technology Index format** — modify the `tech_index` loop at the bottom

---

## PDF Generation

The `make pdf` target uses Pandoc with XeLaTeX to produce a formatted PDF:

```bash
make pdf
```

This runs:

```bash
pandoc CV.md -o assets/documents/Christian_Turner-CV.pdf \
  --pdf-engine=xelatex \
  --standalone \
  -V documentclass=article \
  -V classoption=oneside \
  -V geometry:margin=1in \
  -V papersize=letter \
  -V fontsize=11pt \
  -V mainfont="Helvetica Neue" \
  -V monofont="Menlo" \
  -V linestretch=1.15 \
  -V colorlinks=true \
  -V linkcolor=blue \
  --syntax-highlighting=tango \
  --toc --toc-depth=2
```

**Prerequisites:**

```bash
brew install pandoc
brew install --cask mactex  # or install BasicTeX for a lighter install
```

See `temp/automation/pandoc/pandoc-pdf-generation-analysis.md` for detailed Pandoc configuration options.

---

## `data/personal.json` Reference

This file is the only non-project hand-maintained file. It has three top-level keys:

### `personal`

Contact and identity information:

```json
{
  "personal": {
    "name": "Mr. Christian Turner",
    "title": "Senior Cloud Architect & DevSecOps Specialist",
    "tagline": "Comprehensive Technical CV & Project Portfolio",
    "subtitle": "Detailed technical expertise documentation and project history",
    "email": "CTurner@OttawaCloudConsulting.com",
    "phone": "+1 (613) 796-3300",
    "location": { "city": "Ottawa", "province": "Ontario", "country": "Canada" },
    "links": {
      "linkedin": "linkedin.com/in/Christian-Turner-CloudPro",
      "github": "github.com/OttawaCloudConsulting"
    },
    "consulting_entity": "Ottawa Cloud Consulting Inc."
  }
}
```

### `professional_profile`

Profile paragraphs, language, and certifications:

```json
{
  "professional_profile": {
    "summary": ["Paragraph one...", "Paragraph two...", "Paragraph three..."],
    "language": "English",
    "certifications": [
      {
        "name": "AWS Certified Solutions Architect - Professional",
        "issuer": "Amazon Web Services",
        "certificate_url": "./assets/certificates/AWS Certified Solutions Architect - Professional.pdf"
      }
    ]
  }
}
```

### `executive_summary`

Key-value pairs rendered as a bullet list:

```json
{
  "executive_summary": {
    "specialization": "...",
    "government_clients": "...",
    "compliance_depth": "...",
    "cloud_platforms": "...",
    "current_engagement": "...",
    "certifications": "...",
    "consulting_entity": "...",
    "availability": "..."
  }
}
```

---

## Adding a New Field to the Pipeline

To add a new data field end-to-end:

1. **Add the field to the JSON schema** — update `assets/projects/project_template.json`
2. **Add validation rules** — edit `tests/validators/project-validation-rules.json` (add to `required_fields`, `type_validation`, and `content_validation` as appropriate)
3. **Backfill existing files** — add the field to all existing `project_*.json` files
4. **Use the field in the template** — reference it in `templates/cv.md.j2`
5. **Rebuild and validate** — `make validate && make build`
