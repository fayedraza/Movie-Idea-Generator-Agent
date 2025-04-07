# Genre-based Recommender API

This FastAPI application recommends movies or books based on genre similarity using semantic text similarity.

## Installation

### Method 1: Using Python 3.12 with pip (Recommended)

1. **Install Python 3.12** (if not already installed):
   ```bash
   brew install python@3.12
   ```

2. **Set up a virtual environment**:
   ```bash
   # Navigate to the project directory
   cd recommender_api
   
   # Create a virtual environment
   python3.12 -m venv venv
   
   # Activate the virtual environment
   source venv/bin/activate
   ```

3. **Install the package in development mode**:
   ```bash
   # While in the recommender_api directory with activated environment
   pip install -e .
   ```

### Method 2: Using Hatch (Alternative)

```bash
# Install Hatch if you don't have it
brew install hatch

# Navigate to the project directory
cd recommender_api

# Install dependencies with Hatch
hatch env create
```

## Running the API

You can run the API in one of two ways:

### Option 1: From the app directory

```bash
# Navigate to the app directory
cd recommender_api/app

# Run the FastAPI application
uvicorn main:app --reload --port 8081
```

### Option 2: From the project root

```bash
# From the project root
cd recommender_api
python -m uvicorn app.main:app --reload --port 8081
```

To use a different port:

```bash
uvicorn app.main:app --reload --port <YOUR_PORT>
```

## Testing

The project includes comprehensive unit and integration tests for the API. To run the tests:

### Prerequisites

Install the testing dependencies:

```bash
pip install pytest pytest-cov httpx
```

Note: `httpx` is required for FastAPI's TestClient.

### Running Tests

#### Using pytest directly

From the project root directory:

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=app tests/

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
./run_tests.sh tests/unit/test_api.py
```

For detailed information about the test suite, see [tests/README.md](tests/README.md).

## API Documentation

After starting the server, access the documentation at:
- Interactive API docs: http://127.0.0.1:8081/docs
- ReDoc documentation: http://127.0.0.1:8081/redoc

## API Usage

### Endpoint: POST /recommend/

Request body:
```json
{
    "type": "movies",  // or "books"
    "genres": ["Action", "Adventure"]
}
```

Example response:
```json
{
    "name": "The Lord of the Rings",
    "description": "Epic fantasy adventure about a quest to destroy a powerful ring",
    "genres": ["Fantasy", "Adventure", "Action"],
    "similarity_score": 1.85
}
``` 