import os
import sys
import pytest
from unittest.mock import MagicMock
from pathlib import Path

# Add the project root to the Python path so we can import modules directly
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Sample test data fixture
@pytest.fixture
def sample_data():
    return {
        "movies": [
            {
                "name": "Test Movie 1",
                "description": "A test movie description",
                "genres": ["Action", "Adventure"]
            },
            {
                "name": "Test Movie 2",
                "description": "Another test movie description",
                "genres": ["Drama", "Romance"]
            }
        ],
        "books": [
            {
                "name": "Test Book 1",
                "description": "A test book description",
                "genres": ["Science Fiction", "Fantasy"]
            },
            {
                "name": "Test Book 2",
                "description": "Another test book description",
                "genres": ["Mystery", "Thriller"]
            }
        ]
    }

# Fixture for testing FastAPI
@pytest.fixture
def test_app():
    from fastapi.testclient import TestClient
    from app.main import app
    
    # Patch the data loading to use our test data
    import app.main as main_module
    
    # Save original data
    original_data = main_module.data
    
    def _get_test_app(test_data):
        # Set test data
        main_module.data = test_data
        
        # Create test client
        client = TestClient(app)
        
        return client
    
    yield _get_test_app
    
    # Restore original data after tests
    main_module.data = original_data 

# Check if we're using stub implementations
def is_using_stubs():
    """Check if we're using stub implementations"""
    try:
        import fastapi
        import pydantic
        return False
    except ImportError:
        return True

@pytest.fixture(scope='session', autouse=True)
def setup_models():
    """Set up models for testing"""
    if is_using_stubs():
        try:
            # Import test modules
            from app.main import RecommendationRequest, RecommendationResponse
            
            # Configure model fields
            RecommendationRequest.set_fields(
                fields={'type': str, 'genres': list},
                required=['type', 'genres']
            )
            
            RecommendationResponse.set_fields(
                fields={'name': str, 'description': str, 'genres': list, 'similarity_score': float},
                required=['name', 'description', 'genres', 'similarity_score']
            )
            
            # Add custom validation for RecommendationRequest.type
            original_init = RecommendationRequest.__init__
            
            def custom_init(self, **data):
                if 'type' in data and data['type'] not in ['movies', 'books']:
                    raise ValueError("'type' must be one of: movies, books")
                original_init(self, **data)
            
            RecommendationRequest.__init__ = custom_init
            
        except Exception as e:
            print(f"Warning: Failed to setup models: {e}") 