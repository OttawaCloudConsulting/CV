# Working Notes: Project Orientation

This directory holds orientation documents that describe what this repository is, what it does, and what state it is in. They were written from a review of the code and data as of the `revision` branch (commit `9018d47`, March 2026).

These notes complement the existing reference guides in `docs/`. The guides in `docs/` explain *how to do things*. The notes here explain *what exists* and *where the guides no longer match the code*.

The leading underscore in `_working` keeps Jekyll from publishing this directory to GitHub Pages.

## Documents

| Document | Purpose |
|----------|---------|
| [Overview](./overview.md) | What the project is, who it serves, what it produces, and headline numbers |
| [Architecture and Data Flow](./architecture-and-dataflow.md) | How the pipeline works today: inputs, build logic, outputs, publishing |
| [Repository Map](./repository-map.md) | Every directory and key file, labelled as source, generated, infrastructure, or legacy |
| [Current State and Gaps](./current-state-and-gaps.md) | Verified drift between the documentation and the code, risks, and suggested follow-ups |

## Related Reference Guides

- [CV as Code Workflow](../cv-as-code-workflow.md)
- [Project Schema Reference](../project-schema-reference.md)
- [Build Pipeline Reference](../build-pipeline-reference.md)

Read [Current State and Gaps](./current-state-and-gaps.md) before you rely on those guides. Some of their content is out of date.
