#!/bin/bash

# Run tests for the Movie Idea Generator

# Set up colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}Error: pytest is not installed. Please install it first:${NC}"
    echo "pip install pytest pytest-cov"
    exit 1
fi

# Parse command-line arguments
coverage=false
report_type="term"
test_path="tests/"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --cov|--coverage)
            coverage=true
            shift
            ;;
        --html)
            report_type="html"
            shift
            ;;
        --unit)
            test_path="tests/unit/"
            shift
            ;;
        --integration)
            test_path="tests/integration/"
            shift
            ;;
        *)
            test_path="$1"
            shift
            ;;
    esac
done

echo -e "${YELLOW}Running tests for Movie Idea Generator${NC}"
echo -e "${YELLOW}------------------------------------${NC}"

# Make sure we're in the right directory
cd "$SCRIPT_DIR"

# Build the pytest command
cmd="pytest -v"

if $coverage; then
    cmd="$cmd --cov=src"
    if [ "$report_type" == "html" ]; then
        cmd="$cmd --cov-report=html"
        echo -e "${YELLOW}Coverage report will be generated in htmlcov/ directory${NC}"
    else
        cmd="$cmd --cov-report=term"
    fi
fi

cmd="$cmd $test_path"

# Run the tests
echo -e "${YELLOW}Running command: ${cmd}${NC}"
$cmd

# Check the exit status
status=$?
if [ $status -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed.${NC}"
    exit $status
fi 