#!/bin/bash

################################################################################
# Batch Project Validator
#
# Validates all project JSON files in the assets/projects directory
#
# Usage:
#   ./run-all-validations.sh [options]
#
# Options:
#   --format json     Output results as JSON (default: human-readable)
#   --quiet          Exit with status code only (no output)
#   --verbose        Show detailed validation steps
#   --help           Display this help message
#
# Exit Codes:
#   0 - All projects passed validation
#   1 - One or more projects failed validation
#
################################################################################

set -e

# Color codes for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m'  # No Color

# Script configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VALIDATOR_SCRIPT="${SCRIPT_DIR}/../validators/validate-projects.sh"
PROJECTS_DIR="${SCRIPT_DIR}/../../assets/projects"
OUTPUT_FORMAT="human"
TOTAL_FILES=0
PASSED_FILES=0
FAILED_FILES=0
FAILED_PROJECTS=()

################################################################################
# Helper Functions
################################################################################

# Print usage
usage() {
    sed -n '1,/^################################################################################/p' "$0" | tail -n +3 | head -n -1
}

# Print section header
print_header() {
    if [ "$OUTPUT_FORMAT" != "json" ]; then
        echo ""
        echo "╔════════════════════════════════════════════════════════════╗"
        echo "║             Batch Project JSON Validation                  ║"
        echo "╚════════════════════════════════════════════════════════════╝"
        echo ""
    fi
}

# Print summary
print_summary() {
    if [ "$OUTPUT_FORMAT" = "json" ]; then
        # Output JSON summary
        local failed_json="["
        for i in "${!FAILED_PROJECTS[@]}"; do
            if [[ "$i" -gt 0 ]]; then
                failed_json="$failed_json,"
            fi
            failed_json="$failed_json\"${FAILED_PROJECTS[$i]}\""
        done
        failed_json="$failed_json]"
        
        jq -n \
            --argjson total "$TOTAL_FILES" \
            --argjson passed "$PASSED_FILES" \
            --argjson failed "$FAILED_FILES" \
            --argjson failed_projects "$failed_json" \
            '{
                total_files: $total,
                passed: $passed,
                failed: $failed,
                failed_projects: $failed_projects
            }'
    else
        echo ""
        echo "╔════════════════════════════════════════════════════════════╗"
        echo "║                    Validation Summary                      ║"
        echo "╚════════════════════════════════════════════════════════════╝"
        echo ""
        echo "Total files:    $TOTAL_FILES"
        echo -e "Passed:         ${GREEN}$PASSED_FILES${NC}"
        
        if [ $FAILED_FILES -gt 0 ]; then
            echo -e "Failed:         ${RED}$FAILED_FILES${NC}"
            echo ""
            echo "Failed projects:"
            for project in "${FAILED_PROJECTS[@]}"; do
                echo -e "  ${RED}✗${NC} $project"
            done
        else
            echo -e "Failed:         ${GREEN}$FAILED_FILES${NC}"
        fi
        echo ""
    fi
}

################################################################################
# Main Validation Flow
################################################################################

main() {
    # Parse arguments
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
            --help)
                usage
                exit 0
                ;;
            *)
                echo "Unknown option: $1"
                usage
                exit 2
                ;;
        esac
    done
    
    # Check if validator script exists
    if [ ! -f "$VALIDATOR_SCRIPT" ]; then
        echo -e "${RED}ERROR:${NC} Validator script not found: $VALIDATOR_SCRIPT"
        exit 2
    fi
    
    # Check if projects directory exists
    if [ ! -d "$PROJECTS_DIR" ]; then
        echo -e "${RED}ERROR:${NC} Projects directory not found: $PROJECTS_DIR"
        exit 2
    fi
    
    print_header
    
    # Find all project JSON files (excluding template)
    local project_files
    project_files=$(find "$PROJECTS_DIR" -maxdepth 1 -name "project_*.json" ! -name "project_template.json" -type f | sort)
    
    if [ -z "$project_files" ]; then
        echo -e "${YELLOW}WARNING:${NC} No project files found in $PROJECTS_DIR"
        exit 0
    fi
    
    # Count total files
    TOTAL_FILES=$(echo "$project_files" | wc -l)
    
    if [ "$OUTPUT_FORMAT" != "json" ] && [ "$OUTPUT_FORMAT" != "quiet" ]; then
        echo "Validating $TOTAL_FILES project files..."
        echo ""
    fi
    
    # Validate each file
    while IFS= read -r project_file; do
        local filename
        filename=$(basename "$project_file")
        
        # Run validator and check result
        if bash "$VALIDATOR_SCRIPT" "$project_file" --quiet >/dev/null 2>&1; then
            ((PASSED_FILES++))
            if [[ "$OUTPUT_FORMAT" != "json" ]] && [[ "$OUTPUT_FORMAT" != "quiet" ]]; then
                echo -e "${GREEN}✓${NC} $filename"
            fi
        else
            ((FAILED_FILES++))
            FAILED_PROJECTS+=("$filename")
            if [ "$OUTPUT_FORMAT" != "json" ] && [ "$OUTPUT_FORMAT" != "quiet" ]; then
                echo -e "${RED}✗${NC} $filename"
            fi
        fi
    done <<< "$project_files"
    
    # Print summary
    print_summary
    
    # Exit with appropriate code
    if [ $FAILED_FILES -gt 0 ]; then
        exit 1
    else
        exit 0
    fi
}

# Run main function
main "$@"
