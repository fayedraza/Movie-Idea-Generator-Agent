# Testing Guide for Recommender API

This document provides instructions on writing and running tests for the Genre-based Recommender API.

## Test Structure

The test suite is organized as follows:

```
tests/
├── __init__.py
├── conftest.py                   # Shared pytest fixtures and configuration
├── unit/                         # Unit tests
│   ├── __init__.py
│   ├── test_api.py               # Tests for the API endpoints
│   └── test_models.py            # Tests for Pydantic models
└── integration/                  # Integration tests
    ├── __init__.py
    └── test_api_workflow.py      # Tests for full API workflow
```

## Running Tests

### Prerequisites

Make sure you have the testing dependencies installed:

```bash
pip install pytest pytest-cov httpx
```

The `httpx` library is required for FastAPI's TestClient.

### Running All Tests

From the project root directory (`recommender_api/`):

```bash
pytest
```

### Running Specific Test Categories

Run only unit tests:
```bash
pytest tests/unit/
```

Run only integration tests:
```bash
pytest tests/integration/
```

Run a specific test file:
```bash
pytest tests/unit/test_api.py
```

Run a specific test function:
```bash
pytest tests/unit/test_api.py::TestApiEndpoints::test_recommend_successful
```

### Test Coverage

To run tests with coverage reporting:

```bash
pytest --cov=app tests/
```

To generate an HTML coverage report:

```bash
pytest --cov=app --cov-report=html tests/
```

The HTML report will be available in the `htmlcov/` directory.

## Writing Tests

### Unit Tests

Unit tests should focus on testing individual functions and API endpoints in isolation:
- Test both successful and error scenarios
- Validate response status codes and response bodies
- Verify that functions return expected outputs

Example:
```python
def test_recommend_successful(self, test_app, sample_data):
    # Get the test client with sample data
    client = test_app(sample_data)
    
    # Make the request
    response = client.post(
        "/recommend/",
        json={"type": "movies", "genres": ["Action", "Adventure"]}
    )
    
    # Check the response
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Movie 1"
```

### Integration Tests

Integration tests should verify that the complete API workflows function correctly:
- Test end-to-end request/response cycles
- Validate different user flows
- Test error handling

Example:
```python
def test_movie_recommendation_workflow(self, sample_data, test_app):
    # Get the test client with sample data
    client = test_app(sample_data)
    
    # Test different genre requests and verify responses
    # ...
```

## Test Fixtures

The test suite uses several fixtures to simplify testing:

- `sample_data`: Provides sample movie and book data for testing
- `test_app`: Creates a FastAPI TestClient with the provided test data

Example usage:
```python
def test_with_test_app(test_app, sample_data):
    client = test_app(sample_data)
    # Test code using the client...
``` 