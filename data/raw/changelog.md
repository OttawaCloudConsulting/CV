# CV Data Extraction Changelog

**Source:** `CV.md`
**Schema:** `cv_schema_skeleton.json`
**Output:** `cv_data.json`
**Date:** 2026-03-03

---

## Summary

Extracted all content from CV.md into a structured JSON file conforming to the cv_schema_skeleton.json schema. The populated file contains:

- **13 projects** with **30 sub-projects**
- **160 technology index entries**
- Complete personal, professional profile, and executive summary sections

---

## Schema Mapping Decisions

### 1. Project-level vs Sub-project Outcomes

**Issue:** The schema defines `outcomes` as an array of strings at the project level and a single string at the sub-project level. In CV.md, some projects have outcomes only at the sub-project level (Projects 13, 12, 11, 10, 1), while others have project-level outcome bullet points (Projects 9, 8, 7, 6, 5, 4, 3, 2).

**Decision:** Project-level outcomes are populated where explicitly present in CV.md. Where outcomes exist only at the sub-project level, the project-level `outcomes` array is left empty (`[]`).

### 2. Shared Technical Environments

**Issue:** Projects 8, 7, 6, 5, 4, 3, 2, and 1 list a single technical environment section shared across all sub-projects rather than per-sub-project environments.

**Decision:** Shared technical environments are placed in the project-level `technical_environment` field. Sub-projects under these projects have empty `technical_environment` arrays. Projects 13, 12, 11, 10, and 9 have per-sub-project technical environments populated at the sub-project level.

### 3. Project-level Description Field

**Issue:** The schema includes a `description` field at the project level, but most projects in CV.md jump directly from client/role/date metadata into sub-project descriptions. Only Projects 9 and 8 have explicit project-level descriptive text.

**Decision:** Project-level `description` is populated only where explicit project-level narrative exists in CV.md. Otherwise left as empty string.

### 4. Sub-project Date Ranges

**Issue:** Some sub-projects have explicit date ranges in CV.md while others inherit the parent project's date range implicitly.

**Decision:** Where sub-projects have explicit dates, those are used. Where no explicit sub-project dates appear, the parent project's date range is applied to the sub-project.

### 5. Tasks Performed Nesting

**Issue:** The schema supports two levels of task nesting (`task` + `sub_tasks`). Some CV.md entries have three or more levels of bullet nesting.

**Decision:** Third-level items are flattened into the `sub_tasks` array. No content is lost; only the hierarchical depth is reduced.

---

## Data Issues Detected

### Issue 1: Project 5 Outcome Placement

**Severity:** Minor
**Description:** In CV.md, the outcomes for Project 5.2 (Atlassian migration) appear between Project 5.1's tasks section and the Project 5.2 heading (CV.md lines 728-734). This is a structural anomaly in the source document.
**Resolution:** Outcomes are correctly attributed to the project level and mapped to the project-level outcomes array.

### Issue 2: Technology Index Duplicate Entries

**Severity:** Informational
**Description:** The CV.md technology index contains entries that refer to the same technology under different names:
- "AWS CloudFormation" and "CloudFormation"
- "AWS CloudFront" and "CloudFront"
- "AWS CloudTrail" and "CloudTrail"
- "AWS CloudWatch" and "CloudWatch"
- "AWS Certificate Manager" and "Certificate Manager (AWS)"
- "Microsoft Office 365" and "Office 365"
- "Microsoft PowerShell" and "PowerShell"
- "AWS EKS (Elastic Kubernetes Service)" and "EKS (Elastic Kubernetes Service)"
**Resolution:** All entries preserved as-is from CV.md to maintain source fidelity. Deduplication can be applied in a future normalization pass.

### Issue 3: Empty Sub-project Outcomes

**Severity:** Informational
**Description:** Several sub-projects have outcomes at the project level but not individually:
- Projects 8.1, 8.2 (outcomes at project 8 level only)
- Projects 7.1 (outcomes at project 7 level only)
- Projects 6.1, 6.2 (outcomes at project 6 level only)
- Projects 5.1, 5.2 (outcomes at project 5 level only)
- Projects 9.1, 9.2 (outcomes at project 9 level only)
- Project 2.6 (no outcomes at either level)
**Resolution:** Sub-project `outcomes` field set to empty string (`""`) where no sub-project-specific outcomes exist.

### Issue 4: Date Format - "Current" vs Standard Date

**Severity:** Informational
**Description:** Project 13 uses "Current" as the end date rather than a standard date format.
**Resolution:** Preserved as "Current" to match source document. Standardization to ISO date format can be applied in a future normalization pass.

### Issue 5: Projects Without Project-level Outcomes

**Severity:** Informational
**Description:** Projects 13, 12, 11, 10, and 1 have no project-level outcomes section in CV.md. Outcomes exist only within sub-project descriptions.
**Resolution:** Project-level `outcomes` set to empty array (`[]`).

---

## Build Artifact

The `build_cv_data.py` script in this directory generates `cv_data.json` and can be re-run to regenerate the file if modifications are needed to the extraction logic.
