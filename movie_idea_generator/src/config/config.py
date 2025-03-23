# Configuration settings for agents and API

# API URL for the recommendation service
RECOMMENDER_API_URL = "https://api.movieideas.example.com"

# Agent configuration settings
IDEA_GENERATOR_CONFIG = {
    "temperature": 0.8,  # Higher temperature for more creative outputs
    "allow_delegation": False
}

GENRE_ANALYZER_CONFIG = {
    "temperature": 0.3,  # Lower temperature for more precise genre analysis
    "allow_delegation": False
}

RECOMMENDATION_AGENT_CONFIG = {
    "temperature": 0.5,  # Balanced temperature for recommendations
    "allow_delegation": False
} 