#!/bin/bash
#
# scripts/validate.sh — Validate all project JSON files in assets/projects/
#
# Wraps tests/validators/validate-projects.sh for batch validation with
# rich summary output.
#
# Usage:
#   ./scripts/validate.sh [options]
#
# Options:
#   --verbose       Show per-file validation details (not just failures)
#   --fail-fast     Stop after the first failing file
#   --format json   Output a JSON summary at the end
#   --help          Show this help
#
# Exit Codes:
#   0   All files passed
#   1   One or more files failed
#   2   Bad usage or missing dependency
#
# Examples:
#   ./scripts/validate.sh
#   ./scripts/validate.sh --verbose
#   ./scripts/validate.sh --fail-fast
#   ./scripts/validate.sh --format json

set -o nounset
set -o pipefail

readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly BOLD='\033[1m'
readonly NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_DIR
readonly REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
readonly VALIDATOR="${REPO_ROOT}/tests/validators/validate-projects.sh"
readonly PROJECTS_DIR="${REPO_ROOT}/assets/projects"

VERBOSE=false
FAIL_FAST=false
OUTPUT_FORMAT="human"

usage() {
  cat << 'EOF'
Validate all project JSON files in assets/projects/

Usage:
  ./scripts/validate.sh [options]

Options:
  --verbose       Show per-file validation details (not just failures)
  --fail-fast     Stop after the first failing file
  --format json   Output a JSON summary at the end
  --help          Show this help

Exit Codes:
  0   All files passed
  1   One or more files failed
  2   Bad usage or missing dependency
EOF
}

# ── prerequisites ─────────────────────────────────────────────────────────────

check_deps() {
  if ! command -v jq &>/dev/null; then
    echo -e "${RED}ERROR:${NC} jq is not installed. Install with: brew install jq" >&2
    exit 2
  fi
  if [[ ! -x "${VALIDATOR}" ]]; then
    echo -e "${RED}ERROR:${NC} Validator not found or not executable: ${VALIDATOR}" >&2
    exit 2
  fi
  if [[ ! -d "${PROJECTS_DIR}" ]]; then
    echo -e "${RED}ERROR:${NC} Projects directory not found: ${PROJECTS_DIR}" >&2
    exit 2
  fi
}

# ── argument parsing ───────────────────────────────────────────────────────────

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --verbose)   VERBOSE=true;          shift ;;
      --fail-fast) FAIL_FAST=true;        shift ;;
      --format)    OUTPUT_FORMAT="$2";    shift 2 ;;
      --help)      usage; exit 0 ;;
      *)
        echo -e "${RED}ERROR:${NC} Unknown option: $1" >&2
        usage
        exit 2
        ;;
    esac
  done
}

# ── main ───────────────────────────────────────────────────────────────────────

main() {
  parse_args "$@"
  check_deps

  local -a project_files=()
  while IFS= read -r -d '' f; do
    [[ "$(basename "${f}")" == "project_template.json" ]] && continue
    project_files+=("${f}")
  done < <(find "${PROJECTS_DIR}" -maxdepth 1 -name 'project_*.json' -print0 | sort -z)

  local total=${#project_files[@]}
  if [[ ${total} -eq 0 ]]; then
    echo -e "${YELLOW}WARNING:${NC} No project JSON files found in ${PROJECTS_DIR}"
    exit 0
  fi

  local passed=0 failed=0
  local -a failed_files=()
  # Arrays parallel to failed_files for JSON output
  local -a failed_errors=()

  if [[ "${OUTPUT_FORMAT}" == "human" ]]; then
    echo ""
    echo -e "${BOLD}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BOLD}║           Project JSON Batch Validation                      ║${NC}"
    echo -e "${BOLD}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "  Scanning ${BLUE}${PROJECTS_DIR}${NC}"
    echo -e "  Found ${BOLD}${total}${NC} project files"
    echo ""
  fi

  for f in "${project_files[@]}"; do
    local fname
    fname="$(basename "${f}")"

    if "${VERBOSE}" || [[ "${OUTPUT_FORMAT}" == "human" ]]; then
      # Show each file as it runs
      if "${VERBOSE}"; then
        echo -e "${BLUE}▶${NC} ${fname}"
      fi
    fi

    local validator_exit=0
    local error_output=""

    if "${VERBOSE}" && [[ "${OUTPUT_FORMAT}" == "human" ]]; then
      # Show full per-file report
      bash "${VALIDATOR}" "${f}" --verbose || validator_exit=$?
    else
      # Capture failures only
      error_output=$(bash "${VALIDATOR}" "${f}" 2>&1) || validator_exit=$?
    fi

    if [[ ${validator_exit} -eq 0 ]]; then
      passed=$((passed + 1))
      if [[ "${OUTPUT_FORMAT}" == "human" ]] && ! "${VERBOSE}"; then
        echo -e "  ${GREEN}✓${NC} ${fname}"
      fi
    else
      failed=$((failed + 1))
      failed_files+=("${fname}")
      failed_errors+=("${error_output}")

      if [[ "${OUTPUT_FORMAT}" == "human" ]]; then
        if "${VERBOSE}"; then
          : # verbose mode already printed the full report above
        else
          echo -e "  ${RED}✗${NC} ${fname}"
          # Show errors inline (re-run with human output, capture)
          local detail
          detail=$(bash "${VALIDATOR}" "${f}" 2>&1 || true)
          # Indent and strip box drawing for inline display
          echo "${detail}" | grep -E "^\s+(✗|[0-9]+\.|FAIL)" | sed 's/^/      /' || true
        fi
      fi

      if "${FAIL_FAST}"; then
        echo ""
        echo -e "${RED}Stopping after first failure (--fail-fast)${NC}"
        break
      fi
    fi
  done

  # ── summary ─────────────────────────────────────────────────────────────────

  if [[ "${OUTPUT_FORMAT}" == "json" ]]; then
    # Build JSON output
    local errors_json="[]"
    for i in "${!failed_files[@]}"; do
      errors_json=$(echo "${errors_json}" | jq \
        --arg f "${failed_files[$i]}" \
        --arg e "${failed_errors[$i]}" \
        '. += [{"file": $f, "output": $e}]')
    done

    jq -n \
      --argjson total "${total}" \
      --argjson passed "${passed}" \
      --argjson failed "${failed}" \
      --argjson files "${errors_json}" \
      --argjson ok "$([[ ${failed} -eq 0 ]] && echo true || echo false)" \
      '{
        passed: $ok,
        total: $total,
        passed_count: $passed,
        failed_count: $failed,
        failures: $files
      }'
  else
    echo ""
    echo "──────────────────────────────────────────────────────────────"
    if [[ ${failed} -eq 0 ]]; then
      echo -e "${GREEN}${BOLD}✓ All ${passed}/${total} files passed validation${NC}"
    else
      echo -e "${RED}${BOLD}✗ ${failed}/${total} files failed validation${NC}"
      echo ""
      echo -e "  ${RED}Failed files:${NC}"
      for ff in "${failed_files[@]}"; do
        echo "    • ${ff}"
      done
    fi
    echo "──────────────────────────────────────────────────────────────"
    echo ""
  fi

  [[ ${failed} -eq 0 ]]
}

main "$@"
