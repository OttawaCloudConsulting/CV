# Test Fixtures for Project Validation

This directory contains test fixtures for validating the JSON project validator (`validate-projects.sh`).

## Fixture Types

### Valid Fixtures

Located in `valid/` directory - examples of properly formatted project files that should pass all validation checks.

### Invalid Fixtures - Overview

Located in `invalid/` directory - intentionally malformed project files designed to test specific validation failure scenarios.

## Specific Invalid Fixtures

### 1. `project_invalid_missing_emoji.json`

**Purpose:** Test emoji prefix validation for outcomes array

**Failures Detected:**

- Empty string in deliverables array
- Empty string in outcomes array
- Missing ✅ emoji prefix on outcome items

**Number of Errors:** 3

**Use Case:** Tests specific constraint validation for outcome emoji prefixes

**Coverage:**

- `all_non_empty_strings` check on deliverables
- `all_non_empty_strings` check on outcomes
- `emoji_prefix` check with ✅ emoji

```bash
bash tests/validators/validate-projects.sh tests/fixtures/invalid/project_invalid_missing_emoji.json
```

### 2. `project_comprehensive_failures.json`

**Purpose:** Test comprehensive failure scenarios across multiple validation categories

**Failures Detected (8 total):**

1. Empty project title (content validation)
2. Empty client name (content validation)
3. Empty role (content validation)
4. Empty challenge summary (content validation)
5. Empty solution summary (content validation)
6. Empty deliverables (array content validation with item indices)
7. Empty outcomes (array content validation with item indices)
8. Missing emoji prefix on outcomes (constraint validation with items and values)

**Number of Errors:** 8

**Use Case:** Comprehensive test covering multiple validation failure categories

**Coverage:**

- Content validation (non-empty strings)
- Array element validation (non-empty items)
- Constraint validation (emoji prefixes)
- Error reporting with array indices and actual values

```bash
bash tests/validators/validate-projects.sh tests/fixtures/invalid/project_comprehensive_failures.json
```

## Testing All Fixtures

### Single Fixture Test

Test a specific fixture:

```bash
bash tests/validators/validate-projects.sh tests/fixtures/invalid/project_invalid_missing_emoji.json
```

### Output Formats

Test with JSON output:

```bash
bash tests/validators/validate-projects.sh tests/fixtures/invalid/project_comprehensive_failures.json --format json
```

Test with quiet mode (exit code only):

```bash
bash tests/validators/validate-projects.sh tests/fixtures/invalid/project_comprehensive_failures.json --quiet
echo "Exit code: $?"
```

## Test Results

### Expected Results

All invalid fixtures should:

- Exit with code 1 (validation failed)
- Report multiple errors with detailed descriptions
- Display array indices for problematic items
- Show actual values that failed validation

### Example Output

```text
✗ Validation failed with 8 error(s):

  1. Project title cannot be empty

  2. Client name cannot be empty

  3. Role cannot be empty

  4. Challenge summary cannot be empty

  5. Solution summary cannot be empty

  6. All deliverables must be non-empty strings
         [0]: "" (empty string)
         [2]: "" (empty string)

  7. All outcomes must be non-empty strings
         [1]: "" (empty string)

  8. All outcomes should start with ✅ emoji
       Expected prefix: "✅"
         Failing items:
         [0]: {"key":0,"value":"Missing emoji"}
         [1]: {"key":1,"value":""}
         [2]: {"key":2,"value":"Also missing emoji"}
```

## Validation Categories Covered

### Content Validation

- Empty strings for required string fields
- Non-empty array checks
- Minimum values for numeric fields

### Array Element Validation

- Empty items within arrays
- Multiple failing items with their indices
- Mixed valid and invalid items

### Constraint Validation

- Emoji prefix requirements
- Decimal number validation
- Range validation for numeric fields
- Required keys in objects

## Adding New Fixtures

When adding new fixtures:

1. **Name clearly**: Use `project_invalid_<description>.json` or `project_valid_<description>.json`
2. **Document purpose**: Add comment explaining what is being tested
3. **Be specific**: Focus on testing one or a small set of related failures
4. **Test thoroughly**: Run through the validator and verify expected errors
5. **Update this README**: Document the fixture's purpose and coverage

## Regression Testing

Run all fixtures through validation regularly:

```bash
bash tests/scripts/run-all-validations.sh --verbose
```

This will validate:

- All 27 production project files
- All test fixtures
- Overall validation framework health

## Notes

- Invalid fixtures intentionally violate validation rules
- They serve as regression tests for the validator itself
- Each fixture should have a clear, single focus or related set of failures
- Error messages demonstrate detailed error reporting capabilities
