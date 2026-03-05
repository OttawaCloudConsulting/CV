# CV Repository Documentation

This directory contains technical documentation for the CV as Code pipeline — a file-driven system for managing and generating the CV from structured JSON project files.

## Document Index

| Document | Description |
|----------|-------------|
| [CV as Code Workflow](./cv-as-code-workflow.md) | Architecture overview, pipeline design, and step-by-step workflow for adding roles and projects |
| [Project Schema Reference](./project-schema-reference.md) | Complete JSON schema for project files, field definitions, validation rules, and examples |
| [Build Pipeline Reference](./build-pipeline-reference.md) | `build_cv.py` internals, Jinja2 template system, and Makefile targets |

## Quick Start

### Prerequisites

```bash
# Python dependency
pip install -r requirements.txt

# JSON validation dependency
brew install jq  # macOS
```

### Daily workflow

```bash
# Validate all project files
make validate

# Regenerate CV.md
make build

# Full pipeline (validate → build → PDF)
make all
```

### Adding a new role

```bash
cp assets/projects/project_template.json assets/projects/project_14.json
# Edit the file, then:
make validate && make build
```

See [CV as Code Workflow](./cv-as-code-workflow.md) for the full guide.

## Repository Structure

```
CV/
├── assets/
│   ├── certificates/           # PDF certificates
│   └── projects/               # Source of truth: project JSON files
│       ├── project_template.json
│       ├── project_13.json     # Parent role file
│       ├── project_13.1.json   # Sub-project deliverable (if exists)
│       └── ...
├── data/
│   ├── personal.json           # Personal info, certs, executive summary
│   └── raw/                    # Legacy data (read-only)
├── docs/                       # This directory
├── scripts/
│   └── build_cv.py             # CV build pipeline
├── templates/
│   └── cv.md.j2                # Jinja2 CV template
├── tests/
│   ├── validators/             # JSON validation framework
│   └── scripts/                # Batch validation runners
├── CV.md                       # GENERATED — do not edit by hand
├── Resume.md                   # One-page resume (hand-maintained; Phase 2: generated)
├── Makefile                    # Convenience targets
└── requirements.txt            # Python dependencies
```

## Key Principles

- **`CV.md` is generated** — it is the output of the pipeline, not the source of truth
- **Project JSON files are the source of truth** — all role and deliverable data lives in `assets/projects/`
- **`data/personal.json` is the only other hand-maintained file** — personal info, certifications, executive summary
- **Validation before build** — always run `make validate` before committing
- **`data/raw/` is legacy** — do not edit files in that directory
