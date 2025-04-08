import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# Add the project root to the Python path so we can import modules directly
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))


# Create a fixture for mocked OpenAI client
@pytest.fixture
def mock_openai_client():
    mock_client = MagicMock()

    # Mock the chat completions create method
    mock_completion = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()

    # Set up the return structure to match what the code expects
    mock_message.content = '{"movie": {"name": "Test Movie", "description": "Test Description", "genres": ["Action"]}, "book": {"name": "Test Book", "description": "Test Description", "genres": ["Fiction"]}}'
    mock_choice.message = mock_message
    mock_completion.choices = [mock_choice]

    # Configure the client to return the mocked completion
    mock_client.chat.completions.create.return_value = mock_completion

    return mock_client


# Create a fixture for mocked Crew
@pytest.fixture
def mock_crew():
    mock = MagicMock()
    mock.kickoff.return_value = "Mock movie idea result"
    return mock


# Create a fixture for mocked API responses
@pytest.fixture
def mock_api_response():
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    return MockResponse
