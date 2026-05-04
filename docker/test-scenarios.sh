#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
#  fixos – Docker Scenario Test Harness
#
#  Builds and runs each broken-* scenario container,
#  captures YAML output from `fixos scan --yaml`,
#  and validates results with validate-scenario.py.
#
#  Usage:
#    ./test-scenarios.sh              # all scenarios
#    ./test-scenarios.sh broken-audio # single scenario
# ═══════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
VALIDATOR="$SCRIPT_DIR/validate-scenario.py"
REPORTS_DIR="${REPORTS_DIR:-/tmp/fixos-test-reports}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Scenarios: service name → modules to scan
declare -A SCENARIO_MODULES=(
    ["broken-audio"]="audio"
    ["broken-thumbnails"]="thumbnails"
    ["broken-network"]="system"
    ["broken-full"]="audio,thumbnails,system"
)

PASSED=0
FAILED=0
ERRORS=()

log() { echo -e "${CYAN}[fixos-test]${NC} $*"; }
ok()  { echo -e "  ${GREEN}✓${NC} $*"; }
err() { echo -e "  ${RED}✗${NC} $*"; }
warn() { echo -e "  ${YELLOW}⚠${NC} $*"; }

# ── Build base image ──────────────────────────────────────
build_base() {
    log "Building base image..."
    docker compose -f "$SCRIPT_DIR/docker-compose.yml" build base 2>&1 | tail -5
    ok "fixos-base:latest built"
}

# ── Run scenario ──────────────────────────────────────────
run_scenario() {
    local scenario="$1"
    local modules="${SCENARIO_MODULES[$scenario]:-system}"
    local output_file="$REPORTS_DIR/${scenario}.yml"

    log "━━━ Scenario: ${YELLOW}${scenario}${NC} (modules: $modules) ━━━"

    # Build scenario image
    log "  Building $scenario..."
    if ! docker compose -f "$SCRIPT_DIR/docker-compose.yml" build "$scenario" 2>&1 | tail -3; then
        err "Build failed for $scenario"
        ERRORS+=("$scenario: build failed")
        ((FAILED++))
        return 1
    fi

    # Run fixos scan --yaml inside container
    log "  Running fixos scan --yaml -M $modules..."
    mkdir -p "$REPORTS_DIR"

    local exit_code=0
    docker compose -f "$SCRIPT_DIR/docker-compose.yml" run --rm \
        --no-deps \
        -e FIXOS_TEST_MODE=1 \
        "$scenario" \
        python3 -m fixos.cli.main scan --yaml -M "$modules" --no-banner \
        > "$output_file" 2>/dev/null || exit_code=$?

    # Check we got output
    if [ ! -s "$output_file" ]; then
        err "No YAML output from $scenario"
        ERRORS+=("$scenario: no output")
        ((FAILED++))
        return 1
    fi

    ok "YAML captured: $output_file ($(wc -l < "$output_file") lines)"

    # Validate with validate-scenario.py
    if python3 "$VALIDATOR" "$scenario" < "$output_file"; then
        ok "$scenario PASSED"
        ((PASSED++))
    else
        err "$scenario FAILED validation"
        ERRORS+=("$scenario: validation failed")
        ((FAILED++))
    fi

    echo ""
}

# ── Main ──────────────────────────────────────────────────
main() {
    log "fixOS Docker Scenario Test Harness"
    log "═══════════════════════════════════"

    # Build base first
    build_base

    # Determine which scenarios to run
    local scenarios=()
    if [ $# -gt 0 ]; then
        scenarios=("$@")
    else
        scenarios=("broken-audio" "broken-thumbnails" "broken-network" "broken-full")
    fi

    # Run each scenario
    for scenario in "${scenarios[@]}"; do
        if [ -z "${SCENARIO_MODULES[$scenario]+x}" ]; then
            warn "Unknown scenario: $scenario (skipping)"
            continue
        fi
        run_scenario "$scenario" || true
    done

    # Summary
    echo ""
    log "═══════════════════════════════════"
    log "  SUMMARY"
    log "═══════════════════════════════════"
    ok "Passed: $PASSED"
    if [ $FAILED -gt 0 ]; then
        err "Failed: $FAILED"
        for e in "${ERRORS[@]}"; do
            err "  $e"
        done
        exit 1
    else
        ok "All scenarios passed!"
        exit 0
    fi
}

main "$@"
