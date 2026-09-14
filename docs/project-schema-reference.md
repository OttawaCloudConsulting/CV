# Project JSON Schema Reference

All project files in `assets/projects/` must conform to the schema defined here. Validation is enforced by `tests/validators/project-validation-rules.json`.

---

## Full Schema

```json
{
  "project": {
    "number": 13,
    "title": "string",
    "client": {
      "name": "string",
      "department": "string",
      "team": "string"
    },
    "role": "string",
    "date_range": {
      "start": "Month YYYY",
      "end": "Month YYYY | Current"
    },
    "challenge": {
      "summary": "string"
    },
    "solution": {
      "summary": "string",
      "deliverables": [
        "non-empty string"
      ]
    },
    "outcomes": [
      "✅ Must start with checkmark emoji"
    ],
    "technologies": [
      {
        "category": "string",
        "items": [
          "non-empty string"
        ]
      }
    ]
  }
}
```

---

## Field Reference

### `project.number`

| Attribute | Value |
|-----------|-------|
| Type | Number |
| Required | Yes |
| Constraints | Greater than 0; valid decimal (integer or one decimal place) |

The project number determines both sort order (descending = most recent first) and parent/child relationship.

- **Integer** (`13`, `12`) → parent role file
- **Decimal** (`13.1`, `13.2`) → sub-project deliverable file; child of `floor(number)`

```json
"number": 13      // parent
"number": 13.1    // sub-project of parent 13
```

---

### `project.title`

| Attribute | Value |
|-----------|-------|
| Type | String |
| Required | Yes |
| Constraints | Non-empty |

Descriptive name for the engagement. Format: `"[Client] - [Work Stream Description]"`.

For confidential clients, use `[Client Redacted]` as the client portion.

```json
"title": "[Client Redacted] - Cloud Platform Engineering"
"title": "Agriculture Canada - Cloud Centre of Expertise"
```

---

### `project.client`

| Attribute | Value |
|-----------|-------|
| Type | Object |
| Required | Yes |

An object with three string fields:

| Field | Required | Notes |
|-------|----------|-------|
| `client.name` | Yes, non-empty | Organization name or `"[Client Redacted]"` |
| `client.department` | Yes (can be empty string) | Organizational unit |
| `client.team` | Yes (can be empty string) | Team within the department |

```json
"client": {
  "name": "Shared Services Canada",
  "department": "Hosting Services Branch",
  "team": "Cloud Platform Engineering"
}
```

---

### `project.role`

| Attribute | Value |
|-----------|-------|
| Type | String |
| Required | Yes |
| Constraints | Non-empty |

Your job title or role for this engagement.

```json
"role": "AWS Cloud Platform Engineer/Architect"
"role": "AWS Cloud DevOps Architect (Part-Time)"
```

---

### `project.date_range`

| Attribute | Value |
|-----------|-------|
| Type | Object |
| Required | Yes |

An object with two string fields:

| Field | Required | Format | Example |
|-------|----------|--------|---------|
| `date_range.start` | Yes, non-empty | `"Month YYYY"` | `"September 2023"` |
| `date_range.end` | Yes, non-empty | `"Month YYYY"` or `"Current"` | `"Current"` |

Month names must be written in full (e.g., `"September"`, not `"Sep"` or `"9"`).

```json
"date_range": {
  "start": "September 2023",
  "end": "Current"
}

"date_range": {
  "start": "January 2021",
  "end": "September 2023"
}
```

> **Note:** Sub-project `date_range` values can match the parent's range or narrow it to reflect the actual deliverable timeline within the engagement.

---

### `project.challenge`

| Attribute | Value |
|-----------|-------|
| Type | Object |
| Required | Yes |

An object with one field:

| Field | Required | Notes |
|-------|----------|-------|
| `challenge.summary` | Yes, non-empty | One or two sentences describing the problem or requirement |

The challenge summary becomes the opening description paragraph in the generated CV. Write it from the client's perspective — what problem needed solving.

```json
"challenge": {
  "summary": "Organizational environment requires automated client/workload facilitation with maximum automation and low-touch onboarding and support processes."
}
```

---

### `project.solution`

| Attribute | Value |
|-----------|-------|
| Type | Object |
| Required | Yes |

An object with two fields:

| Field | Required | Notes |
|-------|----------|-------|
| `solution.summary` | Yes, non-empty | One sentence introducing the approach |
| `solution.deliverables` | Yes, non-empty array | List of specific deliverables |

`solution.deliverables` must be an array of non-empty strings. Each item is a bullet point in the generated CV.

```json
"solution": {
  "summary": "Architect, design, and deploy comprehensive automation framework utilizing:",
  "deliverables": [
    "Kubernetes with ArgoCD & Crossplane",
    "GitOps-based infrastructure orchestration",
    "Centralized DevOps orchestration platform",
    "Deterministic automation workflows"
  ]
}
```

---

### `project.outcomes`

| Attribute | Value |
|-----------|-------|
| Type | Array of strings |
| Required | Yes |
| Constraints | Non-empty array; every item non-empty; every item starts with `✅` |

Quantified achievements and results. Each outcome **must** begin with the `✅` emoji. This constraint is enforced by validation.

Write outcomes using specific metrics where possible: percentages, counts, time savings, uptime figures.

```json
"outcomes": [
  "✅ Automation of processes and migration from Click-Ops to GitOps-based workflows",
  "✅ 30% improvement in deployment frequency",
  "✅ 60% reduction in Kubernetes onboarding time",
  "✅ 99.9% uptime across 3 production EKS clusters",
  "✅ 75% reduction in deployment errors through standardization"
]
```

---

### `project.technologies`

| Attribute | Value |
|-----------|-------|
| Type | Array of objects |
| Required | Yes |
| Constraints | Non-empty array |

Each element is a technology category object:

| Field | Required | Notes |
|-------|----------|-------|
| `category` | Yes, non-empty string | Group name (e.g., `"Infrastructure as Code"`) |
| `items` | Yes, non-empty array of strings | Individual technologies |

All items must be non-empty strings. The build script uses `technologies` to auto-generate the Technology Index in the CV.

```json
"technologies": [
  {
    "category": "Container Orchestration",
    "items": ["AWS EKS", "Kubernetes", "Docker"]
  },
  {
    "category": "GitOps & CI/CD",
    "items": ["ArgoCD", "Argo Workflows", "Azure DevOps"]
  },
  {
    "category": "Infrastructure as Code",
    "items": ["Terraform", "Crossplane", "Helm", "CDK", "CDK8s"]
  },
  {
    "category": "Security & Compliance",
    "items": ["AWS IAM", "IRSA", "RBAC", "NIST 800-53", "ITSG standards"]
  }
]
```

---

## Validation Rules Summary

Validation is performed by `tests/validators/validate-projects.sh` using rules defined in `tests/validators/project-validation-rules.json`.

### Format rules

| Rule | Description |
|------|-------------|
| `valid_json` | File must be valid JSON |
| `root_key_exists` | Must have root key `project` |

### Required field rules

All of the following fields must be present:

`project.number`, `project.title`, `project.client`, `project.client.name`, `project.role`, `project.date_range`, `project.date_range.start`, `project.date_range.end`, `project.challenge`, `project.challenge.summary`, `project.solution`, `project.solution.summary`, `project.solution.deliverables`, `project.outcomes`, `project.technologies`

### Type rules

| Field | Expected Type |
|-------|---------------|
| `project.number` | number |
| `project.title` | string |
| `project.client` | object |
| `project.client.name` | string |
| `project.client.department` | string |
| `project.client.team` | string |
| `project.role` | string |
| `project.date_range` | object |
| `project.date_range.start` | string |
| `project.date_range.end` | string |
| `project.challenge.summary` | string |
| `project.solution.summary` | string |
| `project.solution.deliverables` | array |
| `project.outcomes` | array |
| `project.technologies` | array |

### Content rules

| Field | Rule |
|-------|------|
| `project.number` | Greater than 0 |
| `project.title` | Non-empty string |
| `project.client.name` | Non-empty string |
| `project.role` | Non-empty string |
| `project.date_range.start` | Non-empty string |
| `project.date_range.end` | Non-empty string |
| `project.challenge.summary` | Non-empty string |
| `project.solution.summary` | Non-empty string |
| `project.solution.deliverables` | At least 1 item |
| `project.outcomes` | At least 1 item |
| `project.technologies` | At least 1 item |

### Constraint rules

| Field | Constraint |
|-------|------------|
| `project.number` | Valid decimal (e.g., `13`, `2.1`, `1.2`) |
| `project.number` | Range: `0 < number ≤ 999.9` |
| `project.solution.deliverables` | All items are non-empty strings |
| `project.outcomes` | All items are non-empty strings |
| `project.outcomes` | Every item starts with `✅` |
| `project.technologies` | Each element has `category` and `items` keys |
| `project.technologies[].category` | Non-empty string |
| `project.technologies[].items` | Non-empty array |
| `project.technologies[].items` | All items are non-empty strings |

---

## Complete Example: Parent Role File

`assets/projects/project_13.json`:

```json
{
  "project": {
    "number": 13,
    "title": "[Client Redacted] - Cloud Platform Engineering",
    "client": {
      "name": "[Client Redacted]",
      "department": "Cloud Hosting Services Branch",
      "team": "Platform Engineering"
    },
    "role": "AWS Cloud Platform Engineer/Architect",
    "date_range": {
      "start": "September 2023",
      "end": "Current"
    },
    "challenge": {
      "summary": "Organizational environment requires automated client/workload facilitation with maximum automation and low-touch onboarding and support processes."
    },
    "solution": {
      "summary": "Architect, design, and deploy comprehensive automation framework utilizing:",
      "deliverables": [
        "Kubernetes with ArgoCD & Crossplane",
        "GitOps-based infrastructure orchestration",
        "Centralized DevOps orchestration platform",
        "Deterministic automation workflows"
      ]
    },
    "outcomes": [
      "✅ Automation of processes and migration from Click-Ops to GitOps-based workflows",
      "✅ 30% improvement in deployment frequency",
      "✅ 60% reduction in Kubernetes onboarding time",
      "✅ 99.9% uptime across 3 production EKS clusters",
      "✅ 75% reduction in deployment errors through standardization"
    ],
    "technologies": [
      {
        "category": "Container Orchestration",
        "items": ["AWS EKS", "Kubernetes", "Docker"]
      },
      {
        "category": "GitOps & CI/CD",
        "items": ["ArgoCD", "Argo Workflows", "Argo Events", "Azure DevOps"]
      },
      {
        "category": "Infrastructure as Code",
        "items": ["Terraform", "Crossplane", "Helm", "CDK", "CDK8s"]
      },
      {
        "category": "Security & Compliance",
        "items": ["AWS IAM", "IRSA", "RBAC", "NIST 800-53", "ITSG standards"]
      },
      {
        "category": "Languages",
        "items": ["Python", "Golang", "Typescript", "Bash"]
      }
    ]
  }
}
```

---

## Modifying Validation Rules

The validation rules are data-driven — no script changes are needed. Edit `tests/validators/project-validation-rules.json` directly to add, modify, or remove rules.

### Adding a new required field

```json
{
  "field": ".project.new_field",
  "description": "New field is required",
  "type": "error"
}
```

Add this to the `required_fields` array, then add a corresponding entry to `type_validation` and `content_validation` as appropriate.

### Changing a rule from error to warning

Set `"type": "warning"` instead of `"type": "error"`. Warning rules are reported but do not cause validation to fail.
