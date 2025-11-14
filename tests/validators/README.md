# Project JSON Validation Framework

## Overview

This directory contains the validation and testing infrastructure for CV portfolio project JSON files. The framework uses `jq` for data validation and can be integrated with CI/CD pipelines.

## Directory Structure

```bash
tests/
├── validators/
│   ├── project-validation-rules.json      # Externalized validation rules (config file)
│   ├── validate-projects.sh               # Main validator script (single file)
│   └── README.md                          # This file
├── fixtures/
│   ├── valid/                             # Valid project JSON examples
│   │   ├── project_valid_minimal.json
│   │   └── project_valid_full.json
│   └── invalid/                           # Invalid project JSON examples (test cases)
│       ├── project_invalid_missing_field.json
│       ├── project_invalid_wrong_type.json
│       └── project_invalid_empty_array.json
└── scripts/
    ├── run-all-validations.sh             # Batch runner (loops through all projects)
    └── run-ci-checks.sh                   # CI/CD integration script
```

## Validation Rules

All validation rules are defined in `project-validation-rules.json`. The rule categories are:

### 1. Format Rules

- **valid_json**: File must be valid JSON
- **root_key_exists**: Must have root key `project`

### 2. Required Fields

Validates that all necessary fields exist:

- `project.number`
- `project.title`
- `project.client` (object)
- `project.client.name`
- `project.role`
- `project.challenge` (object)
- `project.challenge.summary`
- `project.solution` (object)
- `project.solution.summary`
- `project.solution.deliverables` (array)
- `project.outcomes` (array)
- `project.technologies` (array)

### 3. Type Validation

Validates data types for all fields (number, string, object, array)

### 4. Content Validation

- Non-empty strings where required
- Non-empty arrays where required
- Numbers greater than zero

### 5. Constraint Validation

- Project number must be valid decimal (e.g., 13, 2.1, 1.2)
- Project number range: 0 < number ≤ 999.9 (supports future growth)
- All deliverables are non-empty strings
- All outcomes are non-empty strings
- All outcomes must start with ✅ emoji
- Technology objects must have `category` and `items` keys
- Technology category must be non-empty
- Technology items array must have at least 1 item
- All technology items must be non-empty strings

## Usage

### Validate Single File

```bash
./tests/validators/validate-projects.sh path/to/project_13.json
```

Output modes:

```bash
# Human-readable summary (default)
./tests/validators/validate-projects.sh path/to/project_13.json

# JSON report (for programmatic use)
./tests/validators/validate-projects.sh path/to/project_13.json --format json

# Exit code only (for CI/CD)
./tests/validators/validate-projects.sh path/to/project_13.json --quiet
```

### Validate All Project Files

```bash
./tests/scripts/run-all-validations.sh
```

This script loops through all project files in `/assets/projects/` and validates each one.

### CI/CD Integration

```bash
./tests/scripts/run-ci-checks.sh
```

This script validates all projects and exits with appropriate status code for CI/CD pipelines:

- Exit code 0: All validations passed
- Exit code 1: One or more validations failed

## Creating Test Fixtures

Test fixtures are sample JSON files used to validate the validator itself. They should be placed in:

- `tests/fixtures/valid/` - Valid project examples
- `tests/fixtures/invalid/` - Invalid project examples (for regression testing)

### Valid Fixture Example

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
    "challenge": {
      "summary": "Organizational environment requires automated client/workload facilitation with maximum automation and low-touch onboarding and support processes."
    },
    "solution": {
      "summary": "Architect, design, and deploy comprehensive automation framework.",
      "deliverables": [
        "Kubernetes with ArgoCD & Crossplane",
        "GitOps-based infrastructure orchestration"
      ]
    },
    "outcomes": [
      "✅ Automation of processes",
      "✅ 30% improvement in deployment frequency"
    ],
    "technologies": [
      {
        "category": "Container Orchestration",
        "items": ["AWS EKS", "Kubernetes", "Docker"]
      }
    ]
  }
}
```

## Validation Rules Configuration

The `project-validation-rules.json` file is the single source of truth for all validation rules. To add, modify, or remove rules:

1. Edit `project-validation-rules.json`
2. The validator script will automatically use the updated rules
3. No code changes needed

### Adding a New Rule

```json
{
  "field": ".project.new_field",
  "check": "non_empty_string",
  "description": "New field description",
  "type": "error"
}
```

## Integration with Git Hooks

To validate projects before committing:

```bash
# Create a pre-commit hook
ln -s ../../tests/scripts/run-ci-checks.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

## Integration with GitHub Actions

To validate projects on every push/PR:

```yaml
name: Validate Projects
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install jq
        run: sudo apt-get install -y jq
      - name: Validate all project files
        run: ./tests/scripts/run-ci-checks.sh
```

## Dependencies

- `jq` (v1.6 or later): JSON query and transform utility
  - macOS: `brew install jq`
  - Ubuntu/Debian: `sudo apt-get install jq`
  - CentOS/RHEL: `sudo yum install jq`
  - Windows: `choco install jq`

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All validations passed |
| 1 | One or more validations failed |
| 2 | Invalid script usage or file not found |
| 3 | jq not installed or invalid |

## Troubleshooting

### "jq: command not found"

Install jq:

```bash
brew install jq  # macOS
sudo apt-get install jq  # Ubuntu/Debian
sudo yum install jq  # CentOS/RHEL
sudo dnf install jq  # Fedora
```

### "File not found"

Ensure the path to the project JSON file is correct and the file exists.

### "Invalid JSON"

The file is not valid JSON. Check syntax using:

```bash
jq empty path/to/file.json
```

## Future Enhancements

- [ ] Integration with GitHub Actions workflow
- [ ] Pre-commit hook setup
- [ ] Web dashboard for validation reports
- [ ] Historical validation tracking
- [ ] Custom rule definitions per project type
- [ ] Integration with document generation pipeline

## References

- [jq Manual](https://stedolan.github.io/jq/manual/)
- [JSON Schema](https://json-schema.org/)
- [Project Portfolio Documentation](../../docs/PORTFOLIO.md)
