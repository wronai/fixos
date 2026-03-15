#!/bin/bash
# test-multi-system.sh - Test runner for multiple Linux distributions

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
RESULTS_DIR="$PROJECT_DIR/test-results"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Systems to test
SYSTEMS=("fedora" "ubuntu" "debian" "arch" "alpine")
FAILED_SYSTEMS=()

# Create results directory
mkdir -p "$RESULTS_DIR"

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  fixos - Multi-System Docker Tests${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo "Tested systems: ${SYSTEMS[*]}"
echo "Results: $RESULTS_DIR"
echo ""

# Function to test a system
test_system() {
    local system=$1
    echo -e "${YELLOW}▶ Testing: $system${NC}"
    
    # Build image
    echo "  Building Docker image for $system..."
    if ! docker build -f "$SCRIPT_DIR/$system/Dockerfile" -t "fixos-test:$system" "$PROJECT_DIR" > "$RESULTS_DIR/$system-build.log" 2>&1; then
        echo -e "  ${RED}✗ Build failed for $system${NC}"
        cat "$RESULTS_DIR/$system-build.log"
        FAILED_SYSTEMS+=("$system (build)")
        return 1
    fi
    echo -e "  ${GREEN}✓ Build successful${NC}"
    
    # Run basic tests
    echo "  Running fixos scan --help..."
    if ! docker run --rm "fixos-test:$system" fixos scan --help > "$RESULTS_DIR/$system-scan-help.log" 2>&1; then
        echo -e "  ${RED}✗ fixos scan --help failed${NC}"
        cat "$RESULTS_DIR/$system-scan-help.log"
        FAILED_SYSTEMS+=("$system (scan --help)")
        return 1
    fi
    echo -e "  ${GREEN}✓ fixos scan --help works${NC}"
    
    # Run fixos --version
    echo "  Running fixos --version..."
    if ! docker run --rm "fixos-test:$system" fixos --version > "$RESULTS_DIR/$system-version.log" 2>&1; then
        echo -e "  ${YELLOW}! fixos --version failed (non-critical)${NC}"
    else
        echo -e "  ${GREEN}✓ fixos --version works${NC}"
    fi
    
    # Run unit tests in container
    echo "  Running unit tests..."
    if ! docker run --rm "fixos-test:$system" bash -c "
        cd /app && 
        if [ '$system' = 'ubuntu' ] || [ '$system' = 'debian' ]; then
          python3 -m venv test_env && source test_env/bin/activate && pip install pytest pytest-mock --quiet --break-system-packages && python -m pytest tests/unit/ -v --tb=short -x 2>&1 | head -100
        else
          pip install pytest pytest-mock --quiet && python -m pytest tests/unit/ -v --tb=short -x 2>&1 | head -100
        fi
    " > "$RESULTS_DIR/$system-unit-tests.log" 2>&1; then
        echo -e "  ${RED}✗ Unit tests failed${NC}"
        tail -50 "$RESULTS_DIR/$system-unit-tests.log"
        FAILED_SYSTEMS+=("$system (unit tests)")
        return 1
    fi
    echo -e "  ${GREEN}✓ Unit tests passed${NC}"
    
    echo ""
    return 0
}

# Parse arguments
if [ $# -gt 0 ]; then
    # Test only specified systems
    TEST_SYSTEMS=("$@")
else
    TEST_SYSTEMS=("${SYSTEMS[@]}")
fi

# Run tests for each system
for system in "${TEST_SYSTEMS[@]}"; do
    if [ ! -f "$SCRIPT_DIR/$system/Dockerfile" ]; then
        echo -e "${RED}✗ No Dockerfile found for: $system${NC}"
        FAILED_SYSTEMS+=("$system (no Dockerfile)")
        continue
    fi
    
    test_system "$system" || true
done

# Summary
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Test Summary${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

if [ ${#FAILED_SYSTEMS[@]} -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    for system in "${TEST_SYSTEMS[@]}"; do
        echo -e "  ${GREEN}✓ $system${NC}"
    done
    echo ""
    echo "Results saved to: $RESULTS_DIR"
    exit 0
else
    echo -e "${RED}✗ Some tests failed:${NC}"
    for failed in "${FAILED_SYSTEMS[@]}"; do
        echo -e "  ${RED}✗ $failed${NC}"
    done
    echo ""
    echo -e "${YELLOW}Logs saved to: $RESULTS_DIR${NC}"
    exit 1
fi
