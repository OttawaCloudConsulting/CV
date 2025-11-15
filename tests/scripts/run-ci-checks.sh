#!/bin/bash

################################################################################
# CI/CD Project Validation Script
#
# Validates all project JSON files and provides exit codes suitable for CI/CD
#
# This script is designed to be called from:
# - Git hooks (pre-commit, pre-push)
# - GitHub Actions workflows
# - Other CI/CD systems
#
# Usage:
#   ./run-ci-checks.sh [options]
#
# Options:
#   --verbose        Show detailed validation steps
#   --help           Display this help message
#
# Exit Codes:
#   0 - All validations passed (safe to commit/deploy)
#   1 - One or more validations failed (block commit/deploy)
#
################################################################################

set -e

# Colors for output (disabled if not a TTY)
if [[ -t 1 ]]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    BLUE='\033[0;34m'
    NC='\033[0m'
else
    RED=''
    GREEN=''
    BLUE=''
    NC=''
fi

# Script configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BATCH_VALIDATOR="${SCRIPT_DIR}/run-all-validations.sh"
VERBOSE=""

################################################################################
# Helper Functions
################################################################################

# Print usage
usage() {
    sed -n '1,/^################################################################################/p' "$0" | tail -n +3 | head -n -1
}

################################################################################
# Main CI/CD Flow
################################################################################

main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --verbose)
                VERBOSE="--verbose"
                shift
                ;;
            --help)
                usage
                exit 0
                ;;
            *)
                echo -e "${RED}ERROR:${NC} Unknown option: $1"
                usage
                exit 1
                ;;
        esac
    done
    
    # Check if batch validator exists
    if [ ! -f "$BATCH_VALIDATOR" ]; then
        echo -e "${RED}ERROR:${NC} Batch validator script not found: $BATCH_VALIDATOR"
        exit 1
    fi
    
    echo -e "${BLUE}[CI/CD Check]${NC} Starting project JSON validation..."
    echo ""
    
    # Run batch validator
    if bash "$BATCH_VALIDATOR" $VERBOSE; then
        echo ""
        echo -e "${GREEN}[CI/CD Check]${NC} All validations passed ✓"
        exit 0
    else
        echo ""
        echo -e "${RED}[CI/CD Check]${NC} Validation failed ✗"
        exit 1
    fi
}

# Run main function
main "$@"
