import pytest
from fastapi import HTTPException
from app.main import calculate_genre_similarity


class TestApiEndpoints:
    
    def test_recommend_successful(self, test_app, sample_data):
        """Test the /recommend/ endpoint with valid input"""
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
        assert "description" in data
        assert "genres" in data
        assert "similarity_score" in data
    
    def test_recommend_invalid_type(self, test_app, sample_data):
        """Test the /recommend/ endpoint with an invalid content type"""
        # Get the test client with sample data
        client = test_app(sample_data)
        
        # Make the request with an invalid type
        response = client.post(
            "/recommend/",
            json={"type": "invalid_type", "genres": ["Action", "Adventure"]}
        )
        
        # Check the response
        assert response.status_code == 422  # FastAPI returns 422 for validation errors
        assert "detail" in response.json()
    
    def test_recommend_empty_genres(self, test_app, sample_data):
        """Test the /recommend/ endpoint with empty genres list"""
        # Get the test client with sample data
        client = test_app(sample_data)
        
        # Make the request with empty genres
        response = client.post(
            "/recommend/",
            json={"type": "movies", "genres": []}
        )
        
        # Check the response
        assert response.status_code == 400
        assert "provide at least one genre" in response.json()["detail"]
    
    def test_recommend_best_match(self, test_app, sample_data):
        """Test that the /recommend/ endpoint returns the best match"""
        # Get the test client with sample data
        client = test_app(sample_data)
        
        # Make the request for drama (which matches movie 2 better)
        response = client.post(
            "/recommend/",
            json={"type": "movies", "genres": ["Drama"]}
        )
        
        # Check the response
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Movie 2"  # This should match Drama genre
        
        # Make a request for a book
        response = client.post(
            "/recommend/",
            json={"type": "books", "genres": ["Science Fiction"]}
        )
        
        # Check the response
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Book 1"  # This should match Sci-Fi


class TestGenreSimilarity:
    
    def test_calculate_genre_similarity_exact_match(self):
        """Test genre similarity calculation with exact matches"""
        # Set up test data with exact matches
        input_genres = ["Action", "Adventure"]
        item_genres = ["Action", "Adventure"]
        
        # Calculate similarity
        similarity = calculate_genre_similarity(input_genres, item_genres)
        
        # Check the result (should be a high score for exact match)
        assert similarity > 0
    
    def test_calculate_genre_similarity_no_match(self):
        """Test genre similarity calculation with no matches"""
        # Set up test data with no matches
        input_genres = ["Action", "Adventure"]
        item_genres = ["Drama", "Romance"]
        
        # Calculate similarity
        similarity = calculate_genre_similarity(input_genres, item_genres)
        
        # Check the result (should be a low score for no match)
        assert similarity == 0
    
    def test_calculate_genre_similarity_empty_input(self):
        """Test genre similarity calculation with empty input"""
        # Set up test data with empty input
        input_genres = []
        item_genres = ["Action", "Adventure"]
        
        # Calculate similarity
        similarity = calculate_genre_similarity(input_genres, item_genres)
        
        # Check the result (should be 0 for empty input)
        assert similarity == 0
    
    def test_calculate_genre_similarity_empty_item(self):
        """Test genre similarity calculation with empty item genres"""
        # Set up test data with empty item genres
        input_genres = ["Action", "Adventure"]
        item_genres = []
        
        # Calculate similarity
        similarity = calculate_genre_similarity(input_genres, item_genres)
        
        # Check the result (should be 0 for empty item)
        assert similarity == 0 