"""
Configuration file for pytest.
This file sets up the test environment, including mocking external dependencies.
"""

import sys
import os
from pathlib import Path
from unittest.mock import MagicMock

# Add the root directory to Python path
root_dir = Path(__file__).parent.absolute()
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# Import stubs and set up mock modules
try:
    from tests.stubs import LLM, Agent, BaseTool, Crew, Task, Response, load_dotenv, post
    
    # Mock crewai module
    class MockCrewAI:
        """Mock crewai module for testing."""
        Agent = Agent
        Crew = Crew
        Task = Task
        LLM = LLM
        
        class tools:
            """Mock tools module."""
            BaseTool = BaseTool
    
    # Add mocks to sys.modules
    sys.modules["crewai"] = MockCrewAI()
    sys.modules["crewai.tools"] = MockCrewAI.tools
    
    # Mock requests module if not present
    if "requests" not in sys.modules:
        class MockRequests:
            """Mock requests module."""
            Response = Response
            post = post
        
        sys.modules["requests"] = MockRequests()
    
    # Mock dotenv module if not present
    if "dotenv" not in sys.modules:
        class MockDotEnv:
            """Mock dotenv module."""
            load_dotenv = load_dotenv
        
        sys.modules["dotenv"] = MockDotEnv()
        
except ImportError as e:
    print(f"Error setting up test environment: {e}")
    
# Set environment variable to indicate we're in test mode
os.environ["TESTING"] = "1"

# Set test mode environment variable
os.environ["MOVIE_IDEA_GENERATOR_TEST_MODE"] = "True"
os.environ["OPENAI_API_KEY"] = "test_key_for_pytest_12345"

# Create mock implementations for external dependencies
class MockOpenAIClient:
    """Mock implementation of OpenAI client."""
    
    class ChatCompletion:
        """Mock implementation of ChatCompletion."""
        
        def create(self, **kwargs):
            """Create a mock completion."""
            model = kwargs.get("model", "")
            messages = kwargs.get("messages", [])
            response_format = kwargs.get("response_format", {})
            
            # Extract the prompt from the messages
            prompt = ""
            for message in messages:
                if message.get("role") == "user":
                    prompt = message.get("content", "")
                    break
            
            # Create mock response based on prompt and response_format
            if "json" in str(response_format):
                if "genre" in prompt.lower():
                    content = '{"genres": ["Sci-Fi", "Drama", "Comedy"]}'
                elif "recommend" in prompt.lower():
                    content = '''
                    {
                        "movie": {
                            "title": "Test Movie",
                            "creator": "Test Director",
                            "year": "2020",
                            "description": "A test movie about testing."
                        },
                        "book": {
                            "title": "Test Book",
                            "creator": "Test Author",
                            "year": "2010",
                            "description": "A test book about testing."
                        }
                    }
                    '''
                else:
                    content = '{"result": "test json result"}'
            else:
                content = "This is a mock response for testing purposes."
            
            return MagicMock(
                choices=[
                    MagicMock(
                        message=MagicMock(
                            content=content
                        )
                    )
                ]
            )
    
    def __init__(self):
        """Initialize the mock client."""
        self.chat = self.ChatCompletion()


# Mock the OpenAI client in llm.py
def mock_get_openai_client():
    """Return a mock OpenAI client."""
    return MockOpenAIClient()


# Mock create_chat_completion function
def mock_create_chat_completion(messages, **kwargs):
    """Mock the create_chat_completion function."""
    model = kwargs.get("model", "")
    response_format = kwargs.get("response_format", {})
    
    # Extract the prompt from the messages
    prompt = ""
    for message in messages:
        if message.get("role") == "user":
            prompt = message.get("content", "")
            break
    
    # Create mock response based on prompt and response_format
    if "json" in str(response_format):
        if "genre" in prompt.lower():
            content = '{"genres": ["Sci-Fi", "Drama", "Comedy"]}'
        elif "recommend" in prompt.lower():
            content = '''
            {
                "movie": {
                    "title": "Test Movie",
                    "creator": "Test Director",
                    "year": "2020",
                    "description": "A test movie about testing."
                },
                "book": {
                    "title": "Test Book",
                    "creator": "Test Author",
                    "year": "2010",
                    "description": "A test book about testing."
                }
            }
            '''
        else:
            content = '{"result": "test json result"}'
    else:
        content = "This is a mock response for testing purposes."
    
    return MagicMock(
        choices=[
            MagicMock(
                message=MagicMock(
                    content=content
                )
            )
        ]
    )


# Mock modules
sys.modules["openai"] = MagicMock()

# Patch the get_openai_client and create_chat_completion functions
try:
    import src.config.llm
    src.config.llm.get_openai_client = mock_get_openai_client
    src.config.llm.create_chat_completion = mock_create_chat_completion
    
    # Also provide a mock LLM class
    class MockLLM:
        """Mock LLM class for testing."""
        
        def __init__(self, **kwargs):
            """Initialize the mock LLM."""
            self.name = kwargs.get("name", "MockLLM")
            self.model = kwargs.get("model", "gpt-3.5-turbo")
            self.temperature = kwargs.get("temperature", 0.7)
    
    src.config.llm.LLM = MockLLM
    
except ImportError:
    print("Warning: Unable to patch src.config.llm. Tests might fail.") 