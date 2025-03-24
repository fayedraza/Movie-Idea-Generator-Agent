import requests
import json
from crewai import Agent
from crewai.tools import BaseTool
from crewai import LLM
from src.config.config import RECOMMENDATION_AGENT_CONFIG, RECOMMENDER_API_URL, LLM_CONFIG, OPENAI_MODELS
from src.config.llm import get_llm_config, get_openai_client, create_chat_completion
from src.config.secrets import OPENAI_API_KEY
from typing import Any, Dict, List, Optional, Union

class RecommendationTool(BaseTool):
    name: str = "fetch_recommendations"
    description: str = "Fetch movie and book recommendations from the API based on genres"
    
    def _run(self, genres_str: str) -> Optional[Dict[str, Any]]:
        """Fetch recommendations from the API endpoint"""
        try:
            # Parse genres from the input string
            genres = [genre.strip() for genre in genres_str.split(',')]
            
            # Get movie recommendation
            movie_response = requests.post(
                f"{RECOMMENDER_API_URL}/recommend/",
                json={"type": "movies", "genres": genres}
            )
            movie_data = movie_response.json() if movie_response.status_code == 200 else None
            
            # Get book recommendation
            book_response = requests.post(
                f"{RECOMMENDER_API_URL}/recommend/",
                json={"type": "books", "genres": genres}
            )
            book_data = book_response.json() if book_response.status_code == 200 else None
            
            # If the API fails, generate fallback recommendations using OpenAI
            if movie_data is None or book_data is None:
                print("API recommendation failed. Generating fallback recommendations with OpenAI...")
                fallback = self.generate_fallback_recommendations(genres)
                
                if movie_data is None and 'movie' in fallback:
                    movie_data = fallback['movie']
                
                if book_data is None and 'book' in fallback:
                    book_data = fallback['book']
            
            return {
                "movie": movie_data,
                "book": book_data
            }
        except Exception as e:
            print(f"Error fetching recommendations: {str(e)}")
            return None
    
    def generate_fallback_recommendations(self, genres: List[str]) -> Dict[str, Any]:
        """Generate fallback recommendations using OpenAI if the API fails"""
        try:
            # Get the OpenAI client
            client = get_openai_client()
            
            # Create a prompt for fallback recommendations
            genres_text = ", ".join(genres)
            
            # Use direct OpenAI client for generating fallback recommendations
            response = client.chat.completions.create(
                model=OPENAI_MODELS.get("gpt35_turbo", "gpt-3.5-turbo"),  # Use a faster model for recommendations
                messages=[
                    {"role": "system", "content": "You are a recommendation system for movies and books."},
                    {"role": "user", "content": f"Please recommend one movie and one book that match these genres: {genres_text}. Format the response as JSON with 'movie' and 'book' objects, each containing 'name', 'description', and 'genres' fields."}
                ],
                temperature=0.7,
                max_tokens=500,
                response_format={"type": "json_object"}
            )
            
            # Parse the JSON response
            content = response.choices[0].message.content
            recommendations = json.loads(content)
            
            return recommendations
        except Exception as e:
            print(f"Error generating fallback recommendations: {str(e)}")
            return {"movie": None, "book": None}

class RecommendationAgent:
    @staticmethod
    def create():
        # Create tool instance
        recommendation_tool = RecommendationTool()
        
        # Create an explicit LLM configuration object
        llm = LLM(
            model=OPENAI_MODELS.get("gpt35_turbo", "gpt-3.5-turbo"),
            temperature=RECOMMENDATION_AGENT_CONFIG.get("temperature", 0.5),
            api_key=OPENAI_API_KEY
        )
        
        return Agent(
            role='Content Recommendation Specialist',
            goal='Find similar movies and books based on genre analysis',
            backstory="""You are a recommendation system expert who specializes in finding 
            similar content based on genre analysis. You understand how to interpret genre 
            profiles and use them to find the most relevant recommendations.""",
            tools=[recommendation_tool],
            verbose=True,
            llm=llm,  # Use explicit LLM object instead of llm_config
            **RECOMMENDATION_AGENT_CONFIG
        )

    @staticmethod
    def get_recommendations(genres):
        """Get movie and book recommendations based on genres"""
        task_description = f"""Using the following genres: {genres}
        
        First, use the fetch_recommendations tool to get movie and book recommendations from the API.
        
        Then, provide ONE movie and ONE book recommendation that best represent these genres.
        
        MOVIE RECOMMENDATION:
        1. Title: [Movie name from API or a well-known movie title if API fails]
        2. Director: [Director name]
        3. Year: [Release year]
        4. Synopsis: [Brief 2-3 sentence synopsis]
        5. Why it fits the genres: [Explain why this movie represents the genres well]
        6. Key elements: [List 3-5 key narrative elements, themes, or character dynamics]
        7. Unique aspects: [Identify 2-3 unique aspects that could inspire a new movie]
        
        BOOK RECOMMENDATION:
        1. Title: [Book name from API or a well-known book title if API fails]
        2. Author: [Author name]
        3. Year: [Publication year]
        4. Synopsis: [Brief 2-3 sentence synopsis]
        5. Why it fits the genres: [Explain why this book represents the genres well]
        6. Key elements: [List 3-5 key narrative elements, themes, or character dynamics]
        7. Unique aspects: [Identify 2-3 unique aspects that could inspire a new movie]
        
        IMPORTANT: Choose recommendations that complement each other and could be combined to create an interesting new movie concept. The movie and book should be different enough to provide diverse inspiration but share thematic connections through the specified genres.
        """
        return task_description 