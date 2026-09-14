# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Finding Repository Information: Use graphify First

This repository has graphify installed, with `post-commit` and `post-checkout` hooks in `.git/hooks/`.

For any question about the repository, its code, data, or documentation, **consult the knowledge graph before reading files one by one**. Examples: "How does the build group sub-projects?", "Which files use `parentsummary`?", "What validates date ranges?"

1. Check whether `graphify-out/graph.json` exists.
1. If it exists, run a graphify query:

    ```bash
    /graphify query "<question>"                # broad context (BFS)
    /graphify query "<question>" --dfs          # trace one specific path
    /graphify query "<question>" --budget 1500  # cap answer size
    ```

1. If it does not exist, build it once with `/graphify .`, then query it.
1. Use `Read`, `grep`, or other tools only to confirm what the graph returns, or when the graph does not cover the answer.

Graph results are labelled EXTRACTED, INFERRED, or AMBIGUOUS. Check INFERRED and AMBIGUOUS claims against the source file before relying on them.

## What This Repository Is

A "CV as Code" system. Structured JSON project files are the source of truth. A Python and Jinja2 build renders them into Markdown, which GitHub Pages publishes.

For orientation, read `docs/_working/` first:

- `docs/_working/overview.md`: purpose, audience, headline numbers
- `docs/_working/architecture-and-dataflow.md`: how the pipeline works today
- `docs/_working/repository-map.md`: what each file is
- `docs/_working/current-state-and-gaps.md`: where the older guides in `docs/` are out of date

## Source vs Generated Files

| Edit these | Never edit by hand |
|------------|--------------------|
| `assets/projects/project_N.json` (parent roles) | `CV.md` |
| `assets/projects/project_N.M.json` (sub-projects) | `TECHNOLOGY_INDEX.md` |
| `data/personal.json` | `assets/documents/Christian_Turner-CV.pdf` |
| `templates/*.j2`, `scripts/build_cv.py` | |

`Resume.md` and `index.md` are hand-maintained. No script generates them.

## Commands

```bash
make install                                   # pip install -r requirements.txt (jinja2)
make validate                                  # validate all project JSON files (needs jq)
python3 tests/validators/validate_date_ranges.py  # sub-project dates within parent dates
make build                                     # regenerate CV.md and TECHNOLOGY_INDEX.md
make pdf                                       # Pandoc + XeLaTeX export of CV.md
mdl <file.md>                                  # Markdown lint, run from the repo root
```

After changing project data, templates, or the build script, run `make validate`, the date range check, and `make build`. Commit the regenerated `CV.md` and `TECHNOLOGY_INDEX.md` with the source change.

## Rules and Pitfalls

- **Do not run `scripts/sync_from_cv_data.py`.** It overwrites every project file from the legacy `data/raw/cv_data.json` using an old schema and deletes files it does not know about.
- Treat `data/raw/` as read-only legacy data.
- Parent files need `role_overview.summary`. Sub-project files need `parentsummary.deliverables` and `parentsummary.outcomes`. The build rolls these up into each role section. Validation does not check them, so a missing field is dropped silently.
- Outcomes must **not** start with `✅`. The older guides in `docs/` still say they must. That rule was removed.
- Use only these `technologies[].category` names: Public Cloud, Data Centre & Hosting, Servers & Operating Systems, Virtualization, End-User Computing, Containers & Kubernetes, Infrastructure as Code, CI/CD & GitOps, Serverless & Event-Driven, Languages & Scripting, Applications & Development Tools, Identity & Access Management, Security, Compliance Frameworks, Observability & Monitoring, Networking & WAN, Storage & Backup, Databases, Collaboration & Productivity, Unified Communications & Telephony, IT Service Management & Governance, Business Applications, Industrial Automation & SCADA. A sub-project uses the same category names as its parent.
- A new technology name that is not in `TECH_GROUP_MAP` in `scripts/build_cv.py` is listed under "Uncategorised" in `TECHNOLOGY_INDEX.md`. The match is case-sensitive.
- Project numbers increase over time. Integer numbers are parent roles. Decimal numbers are sub-projects of `floor(number)`.
- Markdown must pass `mdl` with `.mdl_style.rb`. For ordered lists, use `1.` on every item, and give every code fence a language.

## Git

- Work happens on the `revision` branch. Pull requests target `main`, which is the default branch and the GitHub Pages source.
- There is no custom GitHub Actions workflow. On each push to `main`, GitHub's built-in `pages-build-deployment` workflow renders the committed Markdown with Jekyll. It does not run `scripts/build_cv.py`, so regenerate and commit `CV.md` and `TECHNOLOGY_INDEX.md` before merging.
- `temp/` and `.vscode/` are ignored by Git. `.claude/` is local-only.
