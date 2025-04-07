# Testing Guide for Movie Idea Generator

This document provides instructions on writing and running tests for the Movie Idea Generator application.

## Test Structure

The test suite is organized as follows:

```
tests/
├── __init__.py
├── conftest.py               # Shared pytest fixtures and configuration
├── test_secrets.py           # Mock API keys (gitignored)
├── unit/                     # Unit tests
│   ├── __init__.py
│   ├── test_env.py           # Tests for environment configuration
│   ├── test_main.py          # Tests for main application logic
│   └── test_recommendation_agent.py  # Tests for the recommendation agent
└── integration/              # Integration tests
    ├── __init__.py
    └── test_workflow.py      # End-to-end workflow tests
```

## Running Tests

### Prerequisites

Make sure you have the testing dependencies installed:

```bash
pip install pytest pytest-cov
```

### Running All Tests

From the project root directory (`movie_idea_generator/`):

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
pytest tests/unit/test_main.py
```

Run a specific test function:
```bash
pytest tests/unit/test_main.py::TestMain::test_generate_movie_idea
```

### Test Coverage

To run tests with coverage reporting:

```bash
pytest --cov=src tests/
```

To generate an HTML coverage report:

```bash
pytest --cov=src --cov-report=html tests/
```

The HTML report will be available in the `htmlcov/` directory.

## Writing Tests

### Unit Tests

Unit tests should focus on testing individual functions and classes in isolation:
- Mock any external dependencies
- Test both successful and error paths
- Verify that functions return expected outputs

Example:
```python
@patch('src.config.secrets.OPENAI_API_KEY', 'valid-key')
@patch('builtins.print')
def test_check_api_keys_valid(self, mock_print):
    """Test check_api_keys with a valid API key"""
    check_api_keys()
    mock_print.assert_not_called()
```

### Integration Tests

Integration tests should verify that multiple components work together:
- Mock external APIs and services, but test internal component integration
- Verify the workflow produces expected results

Example:
```python
@patch('src.agents.recommendation_agent.RecommendationTool._run')
@patch('src.config.llm.create_chat_completion')
def test_end_to_end_workflow(self, mock_chat_completion, mock_recommendation_tool_run):
    # Set up mocks...
    result = generate_movie_idea("Test prompt")
    assert isinstance(result, str)
    assert len(result) > 0
```

## Mocking External Dependencies

The test suite uses several fixtures to mock external dependencies:

- `mock_openai_client`: Mocks the OpenAI API client
- `mock_crew`: Mocks the CrewAI Crew object
- `mock_api_response`: Helper for mocking HTTP responses

Example usage:
```python
def test_with_mocked_openai(mock_openai_client):
    # The mock_openai_client fixture will be injected
    # Test code that uses OpenAI...
``` 