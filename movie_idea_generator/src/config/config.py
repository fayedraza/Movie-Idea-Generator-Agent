# Configuration settings for agents and API
from src.config.secrets import OPENAI_API_KEY

# API URL for the recommendation service
RECOMMENDER_API_URL = "http://127.0.0.1:8090"

# LLM configuration for OpenAI
LLM_CONFIG = {
    "api_key": OPENAI_API_KEY,  # This will be loaded from secrets module
    "provider": "openai",  # Explicitly set the provider to OpenAI
    "model": "gpt-4-turbo",  # Default to gpt-4-turbo for better performance
    "temperature": 0.7,  # Default temperature for general use
    "max_tokens": 4000,  # Reasonable token limit for responses
    "request_timeout": 120,  # Timeout in seconds
}

# Alternative models that can be used by setting model in LLM_CONFIG
OPENAI_MODELS = {
    "gpt4_turbo": "gpt-4-turbo",
    "gpt4": "gpt-4",
    "gpt35_turbo": "gpt-3.5-turbo",
    "gpt35_16k": "gpt-3.5-turbo-16k",
}

# Agent configuration settings
IDEA_GENERATOR_CONFIG = {
    "temperature": 0.8,  # Higher temperature for more creative outputs
    "allow_delegation": False,
}

GENRE_ANALYZER_CONFIG = {
    "temperature": 0.3,  # Lower temperature for more precise genre analysis
    "allow_delegation": False,
}

RECOMMENDATION_AGENT_CONFIG = {
    "temperature": 0.5,  # Balanced temperature for recommendations
    "allow_delegation": False,
}
