import pytest
from fastapi.testclient import TestClient
from app.main import app


class TestApiWorkflow:
    
    def test_movie_recommendation_workflow(self, sample_data, test_app):
        """Test the full movie recommendation workflow"""
        # Get the test client with sample data
        client = test_app(sample_data)
        
        # Test API with action genre
        response = client.post(
            "/recommend/",
            json={"type": "movies", "genres": ["Action"]}
        )
        
        # Check the response
        assert response.status_code == 200
        action_data = response.json()
        assert action_data["name"] == "Test Movie 1"  # Should match Action genre
        
        # Test API with drama genre
        response = client.post(
            "/recommend/",
            json={"type": "movies", "genres": ["Drama"]}
        )
        
        # Check the response
        assert response.status_code == 200
        drama_data = response.json()
        assert drama_data["name"] == "Test Movie 2"  # Should match Drama genre
        
        # Verify that we get different responses for different genres
        assert action_data["name"] != drama_data["name"]
    
    def test_book_recommendation_workflow(self, sample_data, test_app):
        """Test the full book recommendation workflow"""
        # Get the test client with sample data
        client = test_app(sample_data)
        
        # Test API with sci-fi genre
        response = client.post(
            "/recommend/",
            json={"type": "books", "genres": ["Science Fiction"]}
        )
        
        # Check the response
        assert response.status_code == 200
        scifi_data = response.json()
        assert scifi_data["name"] == "Test Book 1"  # Should match Sci-Fi genre
        
        # Test API with mystery genre
        response = client.post(
            "/recommend/",
            json={"type": "books", "genres": ["Mystery"]}
        )
        
        # Check the response
        assert response.status_code == 200
        mystery_data = response.json()
        assert mystery_data["name"] == "Test Book 2"  # Should match Mystery genre
        
        # Verify that we get different responses for different genres
        assert scifi_data["name"] != mystery_data["name"]
    
    def test_error_handling_workflow(self, sample_data, test_app):
        """Test error handling workflow"""
        # Get the test client with sample data
        client = test_app(sample_data)
        
        # Test invalid type
        response = client.post(
            "/recommend/",
            json={"type": "invalid", "genres": ["Action"]}
        )
        assert response.status_code == 422  # FastAPI returns 422 for validation errors
        assert "detail" in response.json()
        
        # Test empty genres
        response = client.post(
            "/recommend/",
            json={"type": "movies", "genres": []}
        )
        assert response.status_code == 400
        assert "provide at least one genre" in response.json()["detail"]
        
        # Test malformed request
        response = client.post(
            "/recommend/",
            json={"type": "movies"}  # Missing genres field
        )
        assert response.status_code != 200  # Should not be 200 OK 