# Movie Idea Generator

A CrewAI-powered application that generates creative movie ideas based on user preferences.

## Overview

This application uses a team of AI agents to generate unique movie ideas:

1. **Genre Analyzer Agent**: Analyzes user preferences to identify relevant genres
2. **Recommendation Agent**: Finds movie and book recommendations based on the identified genres
3. **Idea Generator Agent**: Creates a unique movie concept by blending elements from the recommendations

## Installation

### Method 1: Using pip

1. **Navigate to the project directory**:
   ```bash
   cd movie_idea_generator
   ```

2. **Install dependencies**:
   ```bash
   pip install -e .
   ```

### Method 2: Using pipenv

1. **Navigate to the project directory**:
   ```bash
   cd movie_idea_generator
   ```

2. **Install dependencies**:
   ```bash
   pipenv install
   ```

3. **Activate the virtual environment**:
   ```bash
   pipenv shell
   ```

## Running the Application

There are two easy ways to run the application:

### Option 1: Using the run script

From the project root directory:

```bash
python movie_idea_generator/run.py
```

### Option 2: As a module

From the project root directory:

```bash
python -m movie_idea_generator.src.main
```

## Usage

When prompted, enter your movie idea preferences. For example:
- "I want a sci-fi thriller with time travel elements"
- "A romantic comedy set in a small town with supernatural elements"
- "An adventure story about a treasure hunt with philosophical themes"

The application will generate a detailed movie concept based on your preferences.

## Example Output

The generated movie idea will include:
- Title
- Logline (one-sentence summary)
- Detailed synopsis
- Target genres
- Key themes and elements
- Influences from the recommended movie and book

## Testing

The project includes comprehensive unit and integration tests. To run the tests:

### Prerequisites

Install the testing dependencies:

```bash
pip install pytest pytest-cov
```

### Running Tests

#### Using pytest directly

From the project root directory:

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=src tests/

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
```

#### Using the test runner script

For convenience, you can use the provided test runner script:

```bash
# Make sure the script is executable
chmod +x run_tests.sh

# Run all tests
./run_tests.sh

# Run with coverage
./run_tests.sh --cov

# Generate HTML coverage report
./run_tests.sh --cov --html

# Run only unit tests
./run_tests.sh --unit

# Run only integration tests
./run_tests.sh --integration

# Run a specific test file
./run_tests.sh tests/unit/test_main.py
```

For detailed information about the test suite, see [tests/README.md](tests/README.md).

## API Integration

By default, the application uses a placeholder API. To connect it to the local Recommender API:

1. Update the `RECOMMENDER_API_URL` in `src/config/config.py`:
   ```python
   RECOMMENDER_API_URL = "http://localhost:8081"
   ```

2. Make sure the Recommender API is running (see the root README for instructions).

## Requirements

- Python 3.8+
- CrewAI
- Requests 