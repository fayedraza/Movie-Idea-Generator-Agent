#!/bin/bash

# Script to run all tests and checks for the Movie Ideas Recommender project

# Set up colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}==========================================================${NC}"
echo -e "${YELLOW} Running Tests and Checks for Movie Ideas Recommender${NC}"
echo -e "${YELLOW}==========================================================${NC}"
echo ""

# 1. Run movie_idea_generator tests
echo -e "${YELLOW}Running tests for movie_idea_generator...${NC}"
if [ -d "movie_idea_generator" ]; then
    # Make sure the test script is executable
    chmod +x movie_idea_generator/run_tests.sh
    
    # Run the tests
    ./movie_idea_generator/run_tests.sh
    MOVIE_TESTS_EXIT_CODE=$?
    
    if [ $MOVIE_TESTS_EXIT_CODE -eq 0 ]; then
        echo -e "${GREEN}✅ All tests for movie_idea_generator passed!${NC}"
    else
        echo -e "${RED}❌ Tests for movie_idea_generator failed!${NC}"
    fi
else
    echo -e "${RED}❌ Directory movie_idea_generator not found!${NC}"
    MOVIE_TESTS_EXIT_CODE=1
fi
echo ""

# 2. Run recommender_api tests
echo -e "${YELLOW}Running tests for recommender_api...${NC}"
if [ -d "recommender_api" ]; then
    # Save current directory
    CURRENT_DIR=$(pwd)
    
    # Change to recommender_api directory
    cd recommender_api
    
    # Check if PYTHONPATH needs to be set for proper imports
    export PYTHONPATH=$PYTHONPATH:$(pwd)
    
    # Run the tests
    python -m pytest tests/ -v
    API_TESTS_EXIT_CODE=$?
    
    # Return to original directory
    cd "$CURRENT_DIR"
    
    if [ $API_TESTS_EXIT_CODE -eq 0 ]; then
        echo -e "${GREEN}✅ All tests for recommender_api passed!${NC}"
    else
        echo -e "${RED}❌ Tests for recommender_api failed!${NC}"
    fi
else
    echo -e "${YELLOW}⚠️ Directory recommender_api not found, skipping tests.${NC}"
    API_TESTS_EXIT_CODE=0
fi
echo ""

# 3. Run pylint
echo -e "${YELLOW}Running pylint checks...${NC}"
python -m pylint $(find . -type f -name "*.py" ! -path "*/\.*" ! -path "*/venv/*" ! -path "*/.venv/*" ! -path "*/secrets.py" ! -path "*/__pycache__/*")
PYLINT_EXIT_CODE=$?

if [ $PYLINT_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ Pylint check passed!${NC}"
else
    echo -e "${YELLOW}⚠️ Pylint found some issues.${NC}"
fi
echo ""

# 4. Print overall summary
echo -e "${YELLOW}==========================================================${NC}"
echo -e "${YELLOW} Test and Check Summary${NC}"
echo -e "${YELLOW}==========================================================${NC}"

# Determine overall status
if [ $MOVIE_TESTS_EXIT_CODE -eq 0 ] && [ $API_TESTS_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
    TESTS_PASSED=true
else
    echo -e "${RED}❌ Some tests failed!${NC}"
    TESTS_PASSED=false
fi

if [ $PYLINT_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ Pylint checks passed!${NC}"
else
    echo -e "${YELLOW}⚠️ Pylint found some issues.${NC}"
fi

# Exit with appropriate code
if [ "$TESTS_PASSED" = true ]; then
    exit 0
else
    exit 1
fi 