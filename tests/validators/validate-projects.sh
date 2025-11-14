#!/bin/bash

################################################################################
# Project JSON Validator
# 
# Validates project JSON files against rules defined in project-validation-rules.json
# 
# Usage:
#   ./validate-projects.sh <filepath> [options]
#
# Options:
#   --format json     Output results as JSON (default: human-readable)
#   --quiet          Exit with status code only (no output)
#   --verbose        Show detailed validation steps
#   --help           Display this help message
#
# Exit Codes:
#   0 - All validations passed
#   1 - One or more validations failed
#   2 - Invalid usage or missing file
#   3 - Missing jq or unable to parse rules
#
# Examples:
#   ./validate-projects.sh ../../../assets/projects/project_13.json
#   ./validate-projects.sh ../../../assets/projects/project_13.json --format json
#   ./validate-projects.sh ../../../assets/projects/project_13.json --quiet
#
################################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RULES_FILE="${SCRIPT_DIR}/project-validation-rules.json"
OUTPUT_FORMAT="human"  # human, json, quiet
VERBOSE=false
EXIT_CODE=0
VALIDATION_ERRORS=()
VALIDATION_ERROR_DETAILS=()
VALIDATION_WARNINGS=()

################################################################################
# Helper Functions
################################################################################

# Print usage information
usage() {
    sed -n '1,/^################################################################################/p' "$0" | tail -n +3 | head -n -1
}

# Print error message
error() {
    if [ "$OUTPUT_FORMAT" != "json" ]; then
        echo -e "${RED}ERROR:${NC} $1" >&2
    fi
}

# Print warning message
warning() {
    if [ "$OUTPUT_FORMAT" != "json" ]; then
        echo -e "${YELLOW}WARNING:${NC} $1" >&2
    fi
}

# Print success message
success() {
    if [ "$OUTPUT_FORMAT" != "json" ] && [ "$OUTPUT_FORMAT" != "quiet" ]; then
        echo -e "${GREEN}✓${NC} $1"
    fi
}

# Print info message
info() {
    if [ "$VERBOSE" = true ] && [ "$OUTPUT_FORMAT" != "json" ]; then
        echo -e "${BLUE}INFO:${NC} $1"
    fi
}

# Check if jq is installed
check_jq() {
    if ! command -v jq &> /dev/null; then
        error "jq is not installed. Please install jq to use this validator."
        echo "  macOS: brew install jq"
        echo "  Ubuntu/Debian: sudo apt-get install jq"
        exit 3
    fi
}

# Check if file exists and is valid JSON
validate_json_syntax() {
    local file="$1"
    
    if [ ! -f "$file" ]; then
        error "File not found: $file"
        return 1
    fi
    
    info "Checking JSON syntax..."
    if ! jq empty "$file" 2>/dev/null; then
        error "Invalid JSON syntax in $file"
        return 1
    fi
    
    success "JSON syntax is valid"
    return 0
}

# Add validation error with optional value context
add_error() {
    local message="$1"
    local details="$2"
    if [ -n "$details" ]; then
        VALIDATION_ERRORS+=("$message")
        VALIDATION_ERROR_DETAILS+=("$details")
    else
        VALIDATION_ERRORS+=("$message")
        VALIDATION_ERROR_DETAILS+=("")
    fi
    EXIT_CODE=1
}

# Check if field exists
field_exists() {
    local file="$1"
    local field="$2"
    
    if jq -e "$field" "$file" >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Get field type
get_field_type() {
    local file="$1"
    local field="$2"
    
    jq -r "$field | type" "$file" 2>/dev/null || echo "null"
}

# Get field value
get_field_value() {
    local file="$1"
    local field="$2"
    
    jq -r "$field" "$file" 2>/dev/null || echo ""
}

################################################################################
# Validation Functions
################################################################################

# Validate required fields
validate_required_fields() {
    local file="$1"
    local rules_array="$2"
    
    info "Validating required fields..."
    
    local count=$(echo "$rules_array" | jq 'length')
    for ((i=0; i<count; i++)); do
        local rule=$(echo "$rules_array" | jq ".[$i]")
        local field=$(echo "$rule" | jq -r '.field')
        local description=$(echo "$rule" | jq -r '.description')
        
        if ! field_exists "$file" "$field"; then
            add_error "$description (field: $field)"
        else
            success "$description"
        fi
    done
}

# Validate field types
validate_types() {
    local file="$1"
    local rules_array="$2"
    
    info "Validating field types..."
    
    local count=$(echo "$rules_array" | jq 'length')
    for ((i=0; i<count; i++)); do
        local rule=$(echo "$rules_array" | jq ".[$i]")
        local field=$(echo "$rule" | jq -r '.field')
        local expected_type=$(echo "$rule" | jq -r '.expected_type')
        local description=$(echo "$rule" | jq -r '.description')
        
        if ! field_exists "$file" "$field"; then
            continue  # Already caught by required fields check
        fi
        
        local actual_type=$(get_field_type "$file" "$field")
        
        if [ "$actual_type" = "$expected_type" ]; then
            success "$description"
        else
            add_error "$description (expected: $expected_type, got: $actual_type)"
        fi
    done
}

# Validate field content
validate_content() {
    local file="$1"
    local rules_array="$2"
    
    info "Validating field content..."
    
    local count=$(echo "$rules_array" | jq 'length')
    for ((i=0; i<count; i++)); do
        local rule=$(echo "$rules_array" | jq ".[$i]")
        local field=$(echo "$rule" | jq -r '.field')
        local check=$(echo "$rule" | jq -r '.check')
        local description=$(echo "$rule" | jq -r '.description')
        
        if ! field_exists "$file" "$field"; then
            continue  # Already caught by required fields check
        fi
        
        local value=$(get_field_value "$file" "$field")
        local valid=true
        
        case "$check" in
            "non_empty_string")
                if [ -z "$value" ] || [ "$value" = "null" ]; then
                    valid=false
                fi
                ;;
            "non_empty_array")
                if [ "$value" = "null" ] || [ "$value" = "[]" ]; then
                    valid=false
                fi
                ;;
            "greater_than_zero")
                if ! jq -e "$field > 0" "$file" >/dev/null 2>&1; then
                    valid=false
                fi
                ;;
        esac
        
        if [ "$valid" = true ]; then
            success "$description"
        else
            add_error "$description"
        fi
    done
}

# Validate constraints
validate_constraints() {
    local file="$1"
    local rules_array="$2"
    
    info "Validating constraints..."
    
    local count=$(echo "$rules_array" | jq 'length')
    for ((i=0; i<count; i++)); do
        local rule=$(echo "$rules_array" | jq ".[$i]")
        local field=$(echo "$rule" | jq -r '.field')
        local check=$(echo "$rule" | jq -r '.check')
        local constraint=$(echo "$rule" | jq -r '.constraint')
        local description=$(echo "$rule" | jq -r '.description')
        
        # Skip if base field doesn't exist
        local base_field="${field%%\[*\]}"
        if ! field_exists "$file" "$base_field"; then
            continue
        fi
        
        # Only validate if we have a constraint or a relevant check
        if [ "$constraint" = "null" ] && [ "$check" = "null" ]; then
            continue
        fi
        
        # Handle constraint-type validations (for scalar fields)
        if [ "$constraint" != "null" ]; then
            if [ "$constraint" = "valid_decimal" ]; then
                if jq -r "$field | type == \"number\"" "$file" 2>/dev/null | grep -q "true"; then
                    success "$description"
                else
                    local value=$(get_field_value "$file" "$field")
                    add_error "$description" "Value: $value (type: $(jq -r "$field | type" "$file"))"
                fi
            elif [ "$constraint" = "within_range" ]; then
                local min=$(echo "$rule" | jq -r '.min')
                local max=$(echo "$rule" | jq -r '.max')
                if jq -r "$field >= $min and $field <= $max" "$file" 2>/dev/null | grep -q "true"; then
                    success "$description"
                else
                    local value=$(get_field_value "$file" "$field")
                    add_error "$description" "Value: $value (expected range: $min - $max)"
                fi
            fi
        fi
        
        # Handle check-type validations (for arrays and their elements)
        if [ "$check" != "null" ]; then
            if [ "$check" = "all_non_empty_strings" ]; then
                # Check if all elements are non-empty strings
                if jq -r "$field | all(. != null and . != \"\" and type == \"string\")" "$file" 2>/dev/null | grep -q "true"; then
                    success "$description"
                else
                    # Extract ALL problematic items
                    local bad_items=$(jq -r "$field | to_entries[] | select(.value == null or .value == \"\" or (.value | type) != \"string\") | \"  [\(.key)]: \" + (if .value == null then \"null\" elif .value == \"\" then \"\\\"\\\" (empty string)\" else @json end)" "$file" 2>/dev/null)
                    if [ -z "$bad_items" ]; then
                        bad_items="  (No specific items identified)"
                    fi
                    add_error "$description" "$bad_items"
                fi
            elif [ "$check" = "emoji_prefix" ]; then
                local prefix=$(echo "$rule" | jq -r '.prefix')
                # Check if all items start with prefix
                if jq -r "$field | all(startswith(\"$prefix\"))" "$file" 2>/dev/null | grep -q "true"; then
                    success "$description"
                else
                    # Extract ALL items missing the prefix
                    local bad_items=$(jq -r "$field | to_entries[] | select(.value | startswith(\"$prefix\") | not) | \"  [\(.key)]: \" + @json" "$file" 2>/dev/null)
                    if [ -z "$bad_items" ]; then
                        bad_items="  (No specific items identified)"
                    fi
                    add_error "$description" "Expected prefix: \"$prefix\"\n  Failing items:\n$bad_items"
                fi
            elif [ "$check" = "has_required_keys" ]; then
                # Check if all objects have required keys
                if jq -r "$field | all(has(\"category\") and has(\"items\"))" "$file" 2>/dev/null | grep -q "true"; then
                    success "$description"
                else
                    # Extract ALL objects missing required keys
                    local bad_items=$(jq -r "$field | to_entries[] | select((has(\"category\") and has(\"items\")) | not) | \"  [\(.key)]: Missing keys: \" + ([\"category\", \"items\"] | map(if . as $key then ($key + (if has($key) then \" (present)\" else \" (missing)\" end)) else . end) | join(\", \"))" "$file" 2>/dev/null)
                    if [ -z "$bad_items" ]; then
                        bad_items="  (No specific items identified)"
                    fi
                    add_error "$description" "$bad_items"
                fi
            fi
        fi
    done
}

################################################################################
# Output Functions
################################################################################

# Output human-readable report
output_human_report() {
    local file="$1"
    local filename=$(basename "$file")
    
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║               Project JSON Validation Report                 ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    echo -e "File: ${BLUE}$filename${NC}"
    echo "Path: $file"
    echo ""
    
    if [ ${#VALIDATION_ERRORS[@]} -eq 0 ]; then
        echo -e "${GREEN}✓ All validations passed!${NC}"
        echo ""
    else
        echo -e "${RED}✗ Validation failed with ${#VALIDATION_ERRORS[@]} error(s):${NC}"
        echo ""
        for i in "${!VALIDATION_ERRORS[@]}"; do
            echo "  $((i+1)). ${VALIDATION_ERRORS[$i]}"
            if [ -n "${VALIDATION_ERROR_DETAILS[$i]}" ]; then
                echo -e "${VALIDATION_ERROR_DETAILS[$i]}" | sed 's/^/       /'
            fi
            echo ""
        done
    fi
    
    # Extract project info
    local project_number=$(get_field_value "$file" '.project.number')
    local project_title=$(get_field_value "$file" '.project.title')
    
    if [ -n "$project_number" ] && [ "$project_number" != "null" ]; then
        echo "Project Info:"
        echo "  Number: $project_number"
        echo "  Title:  $project_title"
        echo ""
    fi
}

# Output JSON report
output_json_report() {
    local file="$1"
    local filename=$(basename "$file")
    
    # Build errors array with details
    local errors_json="["
    for i in "${!VALIDATION_ERRORS[@]}"; do
        if [ $i -gt 0 ]; then
            errors_json="$errors_json,"
        fi
        local error_msg="${VALIDATION_ERRORS[$i]}"
        local error_detail="${VALIDATION_ERROR_DETAILS[$i]}"
        errors_json="$errors_json{\"error\":\"$error_msg\",\"details\":\"$error_detail\"}"
    done
    errors_json="$errors_json]"
    
    local project_number=$(get_field_value "$file" '.project.number')
    local project_title=$(get_field_value "$file" '.project.title')
    
    jq -n \
        --arg filename "$filename" \
        --arg filepath "$file" \
        --argjson errors "$errors_json" \
        --arg project_number "$project_number" \
        --arg project_title "$project_title" \
        --argjson passed "$([ ${#VALIDATION_ERRORS[@]} -eq 0 ] && echo true || echo false)" \
        --argjson error_count "${#VALIDATION_ERRORS[@]}" \
        '{
            filename: $filename,
            filepath: $filepath,
            passed: $passed,
            error_count: $error_count,
            errors: $errors,
            project: {
                number: $project_number,
                title: $project_title
            }
        }'
}

################################################################################
# Main Validation Flow
################################################################################

main() {
    # Parse arguments
    if [ $# -eq 0 ]; then
        usage
        exit 2
    fi
    
    local target_file=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --format)
                OUTPUT_FORMAT="$2"
                shift 2
                ;;
            --quiet)
                OUTPUT_FORMAT="quiet"
                shift
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            --help)
                usage
                exit 0
                ;;
            *)
                target_file="$1"
                shift
                ;;
        esac
    done
    
    # Validation
    check_jq
    
    if [ -z "$target_file" ]; then
        error "No file specified"
        usage
        exit 2
    fi
    
    # Check if rules file exists
    if [ ! -f "$RULES_FILE" ]; then
        error "Rules file not found: $RULES_FILE"
        exit 3
    fi
    
    # Load rules
    info "Loading validation rules from $RULES_FILE..."
    local rules_data
    rules_data=$(jq -r '.' "$RULES_FILE" 2>/dev/null) || {
        error "Failed to parse rules file: $RULES_FILE"
        exit 3
    }
    
    # Validate JSON syntax
    if ! validate_json_syntax "$target_file"; then
        if [ "$OUTPUT_FORMAT" = "json" ]; then
            output_json_report "$target_file"
        elif [ "$OUTPUT_FORMAT" != "quiet" ]; then
            output_human_report "$target_file"
        fi
        exit 1
    fi
    
    # Run validation checks
    echo "$rules_data" | jq -e '.rules.required_fields' >/dev/null 2>&1 && \
        validate_required_fields "$target_file" "$(echo "$rules_data" | jq '.rules.required_fields')"
    
    echo "$rules_data" | jq -e '.rules.type_validation' >/dev/null 2>&1 && \
        validate_types "$target_file" "$(echo "$rules_data" | jq '.rules.type_validation')"
    
    echo "$rules_data" | jq -e '.rules.content_validation' >/dev/null 2>&1 && \
        validate_content "$target_file" "$(echo "$rules_data" | jq '.rules.content_validation')"
    
    echo "$rules_data" | jq -e '.rules.constraint_validation' >/dev/null 2>&1 && \
        validate_constraints "$target_file" "$(echo "$rules_data" | jq '.rules.constraint_validation')"
    
    # Output results
    if [ "$OUTPUT_FORMAT" = "json" ]; then
        output_json_report "$target_file"
    elif [ "$OUTPUT_FORMAT" != "quiet" ]; then
        output_human_report "$target_file"
    fi
    
    exit $EXIT_CODE
}

# Run main function
main "$@"
