from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Literal
import json
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = FastAPI(title="Genre-based Recommender API")

# Load data from JSON
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(current_dir, 'data', 'data.json')

with open(data_path, 'r') as f:
    data = json.load(f)

class RecommendationRequest(BaseModel):
    type: Literal["movies", "books"]
    genres: List[str]

class RecommendationResponse(BaseModel):
    name: str
    description: str
    genres: List[str]
    similarity_score: float

def calculate_genre_similarity(input_genres: List[str], item_genres: List[str]) -> float:
    """
    Calculate similarity between input genres and item genres using CountVectorizer and cosine similarity.
    """
    if not input_genres or not item_genres:
        return 0.0
    
    # Combine all genres into a single corpus
    all_genres = input_genres + item_genres
    
    # Create a CountVectorizer to transform the genres into a bag of words
    vectorizer = CountVectorizer()
    genre_matrix = vectorizer.fit_transform(all_genres)
    
    # Calculate cosine similarity between input and item genres
    input_vectors = genre_matrix[:len(input_genres)]
    item_vectors = genre_matrix[len(input_genres):]
    
    # Calculate similarity between each pair and find the best matches
    similarity_matrix = cosine_similarity(input_vectors, item_vectors)
    
    # For each input genre, find the maximum similarity with any item genre
    total_similarity = np.sum([np.max(similarity_matrix[i]) for i in range(len(input_genres))])
    
    return float(total_similarity)

@app.post("/recommend/", response_model=RecommendationResponse)
async def recommend(request: RecommendationRequest):
    if request.type not in data:
        raise HTTPException(status_code=400, detail=f"Invalid type. Choose from: {list(data.keys())}")
    
    if not request.genres:
        raise HTTPException(status_code=400, detail="Please provide at least one genre")
    
    items = data[request.type]
    best_match = None
    max_similarity = -1
    
    for item in items:
        similarity = calculate_genre_similarity(request.genres, item["genres"])
        if similarity > max_similarity:
            max_similarity = similarity
            best_match = item
    
    if not best_match:
        raise HTTPException(status_code=404, detail="No matching items found")
    
    return RecommendationResponse(
        name=best_match["name"],
        description=best_match["description"],
        genres=best_match["genres"],
        similarity_score=max_similarity
    ) 