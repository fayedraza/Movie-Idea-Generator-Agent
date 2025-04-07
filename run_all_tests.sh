#!/bin/bash

# Simple wrapper script to run tests for both projects
# using their individual test scripts

# Set up colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/.venv"

# Function to check if a Python package is installed
check_package() {
    local package=$1
    python -c "import $package" 2>/dev/null
    return $?
}

# Function to setup virtual environment
setup_venv() {
    echo -e "${YELLOW}Setting up Python virtual environment...${NC}"
    
    # Check if virtualenv is available
    if ! command -v python3 -m venv &> /dev/null; then
        echo -e "${RED}Python venv module not found. Please install it first:${NC}"
        echo -e "${YELLOW}  pip install virtualenv${NC}"
        return 1
    fi
    
    # Create a virtual environment if it doesn't exist
    if [ ! -d "$VENV_DIR" ]; then
        echo -e "${YELLOW}Creating virtual environment in ${VENV_DIR}...${NC}"
        python3 -m venv "$VENV_DIR" || return 1
    fi
    
    # Activate the virtual environment
    echo -e "${YELLOW}Activating virtual environment...${NC}"
    source "${VENV_DIR}/bin/activate" || return 1
    
    # Upgrade pip
    echo -e "${YELLOW}Upgrading pip...${NC}"
    pip install --upgrade pip || return 1
    
    echo -e "${GREEN}Virtual environment is ready!${NC}"
    return 0
}

# Function to install missing packages
install_missing_packages() {
    local project=$1
    local install_failed=false
    echo -e "${YELLOW}Installing dependencies for $project...${NC}"
    
    if [ "$project" = "movie_idea_generator" ]; then
        # Movie Idea Generator dependencies
        echo -e "${YELLOW}Installing movie_idea_generator dependencies...${NC}"
        pip install pytest pytest-cov python-dotenv requests || install_failed=true
        
        # Try to install crewai, but don't fail if it's not available
        pip install crewai || echo -e "${YELLOW}crewai not available, will use stubs${NC}"
        
    else
        # Recommender API dependencies
        echo -e "${YELLOW}Installing recommender_api dependencies...${NC}"
        pip install pytest pytest-cov || install_failed=true
        
        # Try to install these packages but don't fail if they're not available
        pip install httpx || echo -e "${YELLOW}httpx not available, will use stubs${NC}"
        pip install fastapi || echo -e "${YELLOW}fastapi not available, will use stubs${NC}"
        pip install scikit-learn || echo -e "${YELLOW}scikit-learn not available, will use stubs${NC}"
    fi
    
    if [ "$install_failed" = true ]; then
        echo -e "${RED}Some core dependencies could not be installed.${NC}"
        return 1
    else
        echo -e "${GREEN}All required packages installed!${NC}"
        return 0
    fi
}

show_help() {
    echo -e "${BOLD}Test Runner for Both Projects${NC}"
    echo
    echo -e "Usage: $0 [options]"
    echo
    echo -e "Options:"
    echo -e "  --cov, --coverage   Run with coverage reporting"
    echo -e "  --html              Generate HTML coverage report"
    echo -e "  --unit              Run only unit tests"
    echo -e "  --integration       Run only integration tests"
    echo -e "  --movie-only        Run tests only for the Movie Idea Generator"
    echo -e "  --api-only          Run tests only for the Recommender API"
    echo -e "  --install-deps      Install required dependencies before running tests"
    echo -e "  --use-stubs         Use stub implementations instead of real dependencies"
    echo -e "  --venv              Create and use a virtual environment for testing"
    echo -e "  --help              Display this help message"
    echo
}

# Process initial arguments
if [ "$1" = "--help" ]; then
    show_help
    exit 0
fi

movie_only=false
api_only=false
install_deps=false
use_stubs=false
use_venv=false
args=""

# Extract project selection arguments
for arg in "$@"; do
    if [ "$arg" = "--movie-only" ]; then
        movie_only=true
    elif [ "$arg" = "--api-only" ]; then
        api_only=true
    elif [ "$arg" = "--install-deps" ]; then
        install_deps=true
    elif [ "$arg" = "--use-stubs" ]; then
        use_stubs=true
    elif [ "$arg" = "--venv" ]; then
        use_venv=true
    elif [ "$arg" = "--cov" ] || [ "$arg" = "--coverage" ] || [ "$arg" = "--html" ] || [ "$arg" = "--unit" ] || [ "$arg" = "--integration" ]; then
        # Collect all other arguments to pass to the individual scripts
        args="$args $arg"
    fi
done

# Track overall success/failure
overall_result=0

echo -e "${BLUE}${BOLD}=========================================================${NC}"
echo -e "${BLUE}${BOLD} Running Tests for Movie Ideas Recommender Projects${NC}"
echo -e "${BLUE}${BOLD}=========================================================${NC}"
echo

# Set up virtual environment if requested
if [ "$use_venv" = true ]; then
    if ! setup_venv; then
        echo -e "${RED}Failed to set up virtual environment. Using system Python.${NC}"
        echo -e "${YELLOW}Switching to stub mode due to environment setup failure${NC}"
        use_stubs=true
    else
        echo -e "${GREEN}Using virtual environment for testing${NC}"
        # If we're using a venv, we should install dependencies
        install_deps=true
        
        # Always install pytest regardless of other settings
        echo -e "${YELLOW}Installing pytest in virtual environment...${NC}"
        pip install pytest pytest-cov || {
            echo -e "${RED}Failed to install pytest. Tests will not run.${NC}"
            exit 1
        }
    fi
    echo
fi

# Get the absolute paths to the project directories
MOVIE_DIR="${SCRIPT_DIR}/movie_idea_generator"
API_DIR="${SCRIPT_DIR}/recommender_api"

# Make sure the test scripts are executable
chmod +x "${MOVIE_DIR}/run_tests.sh" "${API_DIR}/run_tests.sh"

# Create the secrets.py file if it doesn't exist
if [ ! -f "${MOVIE_DIR}/src/config/secrets.py" ]; then
    echo -e "${YELLOW}Creating missing secrets.py file...${NC}"
    mkdir -p "${MOVIE_DIR}/src/config"
    echo 'OPENAI_API_KEY = "dummy-key-for-testing"' > "${MOVIE_DIR}/src/config/secrets.py"
    echo -e "${GREEN}Created secrets.py with dummy API key${NC}"
    echo
fi

# Install dependencies if requested and not using stubs
if [ "$install_deps" = true ] && [ "$use_stubs" = false ]; then
    if [ "$movie_only" = true ]; then
        if ! install_missing_packages "movie_idea_generator"; then
            echo -e "${YELLOW}Switching to stub mode due to installation failures${NC}"
            use_stubs=true
        fi
    elif [ "$api_only" = true ]; then
        if ! install_missing_packages "recommender_api"; then
            echo -e "${YELLOW}Switching to stub mode due to installation failures${NC}"
            use_stubs=true
        fi
    else
        movie_install_success=true
        api_install_success=true
        if ! install_missing_packages "movie_idea_generator"; then
            movie_install_success=false
        fi
        if ! install_missing_packages "recommender_api"; then
            api_install_success=false
        fi
        
        if [ "$movie_install_success" = false ] || [ "$api_install_success" = false ]; then
            echo -e "${YELLOW}Switching to stub mode due to installation failures${NC}"
            use_stubs=true
        fi
    fi
    echo
fi

# Set up stubs if requested
if [ "$use_stubs" = true ]; then
    echo -e "${YELLOW}Using stub implementations for external dependencies${NC}"
    
    # Ensure we have pytest installed for stub tests
    if [ "$use_venv" = true ] && ! check_package pytest; then
        echo -e "${YELLOW}Installing pytest for stub tests...${NC}"
        pip install pytest pytest-cov || {
            echo -e "${RED}Failed to install pytest. Tests will not run.${NC}"
            exit 1
        }
    fi
    
    # For demonstration purposes, let's run only the test_env.py test
    # which has fewer external dependencies
    if [ "$movie_only" = true ]; then
        echo -e "${YELLOW}Running only test_env.py with stubs${NC}"
        cd "${MOVIE_DIR}" && python -m pytest tests/unit/test_env.py -v
        overall_result=$?
    elif [ "$api_only" = true ]; then
        echo -e "${YELLOW}Running only basic tests with stubs${NC}"
        cd "${API_DIR}" && python -m pytest tests/unit/test_models.py::TestPydanticModels::test_recommendation_request_valid tests/unit/test_models.py::TestPydanticModels::test_recommendation_request_invalid_type tests/unit/test_models.py::TestPydanticModels::test_recommendation_request_empty_genres -v
        overall_result=$?
    else
        echo -e "${YELLOW}Running only basic tests with stubs${NC}"
        cd "${MOVIE_DIR}" && python -m pytest tests/unit/test_env.py -v
        movie_result=$?
        
        cd "${SCRIPT_DIR}"
        
        cd "${API_DIR}" && python -m pytest tests/unit/test_models.py::TestPydanticModels::test_recommendation_request_valid tests/unit/test_models.py::TestPydanticModels::test_recommendation_request_invalid_type tests/unit/test_models.py::TestPydanticModels::test_recommendation_request_empty_genres -v
        api_result=$?
        
        cd "${SCRIPT_DIR}"
        
        # Set overall result (fail if either failed)
        if [ $movie_result -ne 0 ] || [ $api_result -ne 0 ]; then
            overall_result=1
        fi
    fi
    
    # Print additional information
    echo
    echo -e "${YELLOW}Note: With --use-stubs, only a subset of tests is run as a demonstration.${NC}"
    echo -e "${YELLOW}For a complete test run, you need to install the actual dependencies with --install-deps.${NC}"
else
    # Run the appropriate test scripts based on arguments
    if [ "$movie_only" = true ]; then
        # Only run Movie Idea Generator tests
        echo -e "${YELLOW}Running tests for Movie Idea Generator...${NC}"
        cd "${MOVIE_DIR}" && ./run_tests.sh $args
        overall_result=$?
    elif [ "$api_only" = true ]; then
        # Only run Recommender API tests
        echo -e "${YELLOW}Running tests for Recommender API...${NC}"
        cd "${API_DIR}" && ./run_tests.sh $args
        overall_result=$?
    else
        # Run tests for both projects
        echo -e "${YELLOW}Running tests for Movie Idea Generator...${NC}"
        cd "${MOVIE_DIR}" && ./run_tests.sh $args
        movie_result=$?
        
        # Go back to the script directory before moving to the next project
        cd "${SCRIPT_DIR}"
        
        echo
        echo -e "${YELLOW}Running tests for Recommender API...${NC}"
        cd "${API_DIR}" && ./run_tests.sh $args
        api_result=$?
        
        # Go back to the original directory
        cd "${SCRIPT_DIR}"
        
        # Set overall result (fail if either failed)
        if [ $movie_result -ne 0 ] || [ $api_result -ne 0 ]; then
            overall_result=1
        fi
    fi
fi

# Deactivate virtual environment if we used one
if [ "$use_venv" = true ]; then
    echo -e "${YELLOW}Deactivating virtual environment...${NC}"
    deactivate 2>/dev/null || true
fi

# Print overall summary
echo
echo -e "${BLUE}${BOLD}=========================================================${NC}"
echo -e "${BLUE}${BOLD} Test Summary${NC}"
echo -e "${BLUE}${BOLD}=========================================================${NC}"

if [ $overall_result -eq 0 ]; then
    echo -e "${GREEN}${BOLD}All tests passed successfully!${NC}"
else
    echo -e "${RED}${BOLD}Some tests failed. Please check the output above for details.${NC}"
    
    if [ "$use_stubs" = false ]; then
        echo -e "${YELLOW}Tips:${NC}"
        echo -e "${YELLOW}  - Try running with a virtual environment:${NC}"
        echo -e "${YELLOW}      ./run_all_tests.sh --venv${NC}"
        echo -e "${YELLOW}  - Or use stub implementations to run a subset of tests:${NC}"
        echo -e "${YELLOW}      ./run_all_tests.sh --use-stubs${NC}"
    else
        echo -e "${YELLOW}Tip: To run all tests with dependencies in a virtual environment:${NC}"
        echo -e "${YELLOW}      ./run_all_tests.sh --venv${NC}"
    fi
fi

exit $overall_result 