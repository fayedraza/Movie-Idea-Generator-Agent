import pytest
try:
    from pydantic import ValidationError
except ImportError:
    from tests.stubs import ValidationError
from app.main import RecommendationRequest, RecommendationResponse


class TestPydanticModels:
    
    def test_recommendation_request_valid(self):
        """Test creating a valid RecommendationRequest"""
        # Create a valid request
        request = RecommendationRequest(
            type="movies",
            genres=["Action", "Adventure"]
        )
        
        # Check the values
        assert request.type == "movies"
        assert request.genres == ["Action", "Adventure"]
    
    def test_recommendation_request_invalid_type(self):
        """Test creating a RecommendationRequest with an invalid type"""
        # Attempt to create a request with an invalid type
        with pytest.raises(ValueError) as excinfo:
            RecommendationRequest(
                type="invalid_type",
                genres=["Action", "Adventure"]
            )
        
        # Check the error message
        assert "'type' must be one of: movies, books" in str(excinfo.value)
    
    def test_recommendation_request_empty_genres(self):
        """Test creating a RecommendationRequest with empty genres"""
        # Empty genres should be valid at the model level (API validation is separate)
        request = RecommendationRequest(
            type="movies",
            genres=[]
        )
        
        # Check the values
        assert request.type == "movies"
        assert request.genres == []
    
    def test_recommendation_response_valid(self):
        """Test creating a valid RecommendationResponse"""
        # Create a valid response
        response = RecommendationResponse(
            name="Test Movie",
            description="Test Description",
            genres=["Action", "Adventure"],
            similarity_score=0.8
        )
        
        # Check the values
        assert response.name == "Test Movie"
        assert response.description == "Incorrect Description", "This test is deliberately failing to verify the CI pipeline"
        assert response.genres == ["Action", "Adventure"]
        assert response.similarity_score == 0.8
    
    def test_recommendation_response_missing_fields(self):
        """Test creating a RecommendationResponse with missing fields"""
        # Attempt to create a response with missing fields
        with pytest.raises(ValidationError):
            RecommendationResponse(
                name="Test Movie",
                # Missing description
                genres=["Action", "Adventure"],
                similarity_score=0.8
            )
    
    def test_recommendation_response_invalid_types(self):
        """Test creating a RecommendationResponse with invalid types"""
        # Attempt to create a response with invalid types
        with pytest.raises(ValidationError):
            RecommendationResponse(
                name="Test Movie",
                description="Test Description",
                genres="Not a list",  # Should be a list
                similarity_score=0.8
            ) 