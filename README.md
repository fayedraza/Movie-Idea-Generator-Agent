# Movie Ideas Recommender

This monorepo contains two related projects:
1. **Movie Idea Generator**: A CrewAI-powered application that generates creative movie ideas based on user preferences
2. **Recommender API**: A FastAPI service that recommends movies and books based on genre similarity

## Project Structure

```
.
├── movie_idea_generator/    # CrewAI-based movie idea generator
│   ├── src/                # Source code
│   ├── tests/              # Unit and integration tests
│   └── run_tests.sh        # Test runner script
├── recommender_api/        # FastAPI-based recommendation service
│   ├── app/                # API code
│   ├── data/               # Sample data
│   ├── tests/              # Unit and integration tests
│   └── run_tests.sh        # Test runner script
└── run_all_tests.sh        # Combined test runner for both projects
```

## Getting Started

For detailed instructions on installing and running each project, see the README files in the respective project directories:
- [Movie Idea Generator README](movie_idea_generator/README.md)
- [Recommender API README](recommender_api/README.md)

## Running Tests

For the quickest and most reliable way to run tests without installing all dependencies, use:

```bash
./run_all_tests.sh --venv --use-stubs
```

This creates a virtual environment and runs a subset of tests that work with stub implementations instead of real dependencies.

### Prerequisites

Both projects use pytest for testing. You can either install the required dependencies manually, use a virtual environment, or use the provided script to do it for you.

#### Manual Installation

```bash
# For Movie Idea Generator tests
pip install pytest pytest-cov python-dotenv crewai requests

# For Recommender API tests
pip install pytest pytest-cov httpx fastapi scikit-learn
```

#### Using a Virtual Environment (Recommended)

The test script can automatically create and use a Python virtual environment for running tests:

```bash
# Run tests in a virtual environment (this will automatically install dependencies)
./run_all_tests.sh --venv
```

This is the recommended approach as it:
- Creates an isolated environment for testing
- Avoids conflicts with system-wide Python packages
- Automatically installs dependencies without affecting your system
- Cleans up after tests are complete

#### Automatic Installation

```bash
# Install dependencies and run tests
./run_all_tests.sh --install-deps
```

#### Using Stubs (Demo Mode)

For demonstration purposes, you can run a small subset of tests without installing all dependencies:

```bash
# Run a subset of tests with stub implementations
./run_all_tests.sh --use-stubs

# RECOMMENDED: Run stub tests in a virtual environment (easiest approach)
./run_all_tests.sh --venv --use-stubs
```

This option runs only basic tests that don't have complex external dependencies. It's meant as a demonstration and not a full test suite. The combination of `--venv` and `--use-stubs` is the quickest and most reliable way to run tests without worrying about dependency installation issues.

### Running Tests for Both Projects

You can run tests for both projects with a single command using the combined test runner:

```bash
# Make sure the script is executable
chmod +x run_all_tests.sh

# Run all tests for both projects
./run_all_tests.sh

# Run tests in a virtual environment (recommended)
./run_all_tests.sh --venv

# Install dependencies and run tests
./run_all_tests.sh --install-deps

# Run a subset of tests in demo mode (no dependencies needed)
./run_all_tests.sh --use-stubs

# Run with coverage reporting
./run_all_tests.sh --cov

# Generate HTML coverage reports
./run_all_tests.sh --cov --html

# Run only unit tests
./run_all_tests.sh --unit

# Run only integration tests
./run_all_tests.sh --integration
```

You can also combine options:

```bash
# RECOMMENDED FOR NEW USERS: Run tests in a virtual environment with stubs 
# (quickest and most reliable without installing all dependencies)
./run_all_tests.sh --venv --use-stubs

# Run tests in a virtual environment with coverage reporting
./run_all_tests.sh --venv --cov

# Run only unit tests in a virtual environment
./run_all_tests.sh --venv --unit
```

### Running Tests for Individual Projects

You can also run tests for a specific project:

```bash
# Run tests only for Movie Idea Generator
./run_all_tests.sh --movie-only

# Run tests only for Recommender API
./run_all_tests.sh --api-only

# Install dependencies and run tests for Movie Idea Generator only
./run_all_tests.sh --movie-only --install-deps

# Run a subset of API tests in demo mode
./run_all_tests.sh --api-only --use-stubs

# Combine with other options
./run_all_tests.sh --api-only --cov --unit
```

For more details on testing each project, see:
- [Movie Idea Generator Testing Guide](movie_idea_generator/tests/README.md)
- [Recommender API Testing Guide](recommender_api/tests/README.md)

## Integration Between Projects

The Movie Idea Generator can use the Recommender API service to get movie and book recommendations based on genres. To enable this integration:

1. Start the Recommender API service on port 8081
2. Update the `RECOMMENDER_API_URL` in `movie_idea_generator/src/config/config.py` 

## Code Quality Tools

This project uses several tools to maintain code quality:

### Linting and Formatting

- **Pylint**: We enforce a minimum pylint score of 3.0/10 and target a score of 8.0/10.
- **Black**: For consistent code formatting
- **isort**: For organizing imports
- **Ruff**: For additional linting and automatic fixes

### Utility Scripts

Several utility scripts are available to help maintain code quality:

- `format_and_fix.sh`: Runs all formatting tools (black, isort, ruff) and creates necessary files
- `format_and_check.sh`: Runs the formatter and then checks pylint score, failing if below 3.0
- `advanced_fixes.py`: Performs more complex code quality improvements:
  - Fixes import errors
  - Extracts duplicated code to utility functions
  - Splits long lines into multiple lines
  - Replaces broad exception handling with specific exceptions
  - Fixes protected access warnings
  - Fixes unused arguments
  - Adds pylint disable comments where appropriate

### Running the Quality Tools

```bash
# Run all formatters and then check pylint score
./format_and_check.sh

# Apply advanced fixes and then run formatters and check
./run_advanced_fixes.sh
```

### CI/CD

The project includes a GitHub Actions workflow that runs pylint and tests. The workflow will:
- Fail if the pylint score is below 3.0/10
- Warn if the pylint score is below 8.0/10
- Run all tests and report results 