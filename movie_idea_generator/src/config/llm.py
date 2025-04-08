"""
LLM configuration utilities for working with OpenAI models.
This module provides helper functions to create and configure OpenAI clients.
"""

import os
from typing import Dict, List, Optional, Any, Union
from openai import OpenAI
from src.config.config import LLM_CONFIG, OPENAI_MODELS
from src.config.secrets import OPENAI_API_KEY

class LLM:
    """
    Simple LLM class for configuration.
    
    This is a simplified version of the LLM class used by the app.
    """
    
    def __init__(self, model: str = "gpt-3.5-turbo", temperature: float = 0.7, **kwargs):
        """
        Initialize the LLM with configuration parameters.
        
        Args:
            model: The model name to use
            temperature: The temperature to use for generation
            **kwargs: Additional parameters
        """
        self.model = model
        self.temperature = temperature
        self.name = kwargs.get("name", "Default LLM")
        self.api_key = kwargs.get("api_key", OPENAI_API_KEY)

def get_openai_client():
    """
    Get an OpenAI client instance.
    
    Returns:
        An OpenAI client instance
    """
    try:
        return OpenAI(api_key=OPENAI_API_KEY)
    except ImportError:
        print("Warning: OpenAI package not installed. Using mock client.")
        # Create a simple mock client for testing
        return None

def get_llm_config(model_key=None, temperature=None, max_tokens=None):
    """
    Get a configured LLM configuration dictionary for CrewAI.
    
    Args:
        model_key (str, optional): Key from OPENAI_MODELS to use. Defaults to None (uses default in LLM_CONFIG).
        temperature (float, optional): Temperature setting. Defaults to None (uses default in LLM_CONFIG).
        max_tokens (int, optional): Max tokens setting. Defaults to None (uses default in LLM_CONFIG).
    
    Returns:
        dict: LLM configuration dictionary for CrewAI.
    """
    config = LLM_CONFIG.copy()
    
    # Update model if specified
    if model_key and model_key in OPENAI_MODELS:
        config["model"] = OPENAI_MODELS[model_key]
    
    # Update temperature if specified
    if temperature is not None:
        config["temperature"] = temperature
    
    # Update max_tokens if specified
    if max_tokens is not None:
        config["max_tokens"] = max_tokens
    
    return config

def create_chat_completion(
    messages: List[Dict[str, str]], 
    model: str = "gpt-3.5-turbo", 
    temperature: float = 0.7, 
    max_tokens: int = 500,
    response_format: Optional[Dict[str, str]] = None,
    **kwargs
) -> Any:
    """
    Create a chat completion using OpenAI API.
    
    This function wraps the OpenAI API call to make it easier to mock in tests.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content' keys
        model: The model name to use
        temperature: The temperature to use for generation
        max_tokens: The maximum number of tokens to generate
        response_format: Optional response format (e.g., {"type": "json_object"})
        **kwargs: Additional parameters
        
    Returns:
        The OpenAI API response
    """
    client = get_openai_client()
    
    # Set up API parameters
    params = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    # Add response format if provided
    if response_format:
        params["response_format"] = response_format
        
    # Add any additional parameters
    params.update(kwargs)
    
    # Make the API call
    return client.chat.completions.create(**params)

def use_gpt4():
    """Get configuration for GPT-4"""
    return get_llm_config(model_key="gpt4")

def use_gpt4_turbo():
    """Get configuration for GPT-4 Turbo"""
    return get_llm_config(model_key="gpt4_turbo")

def use_gpt35_turbo():
    """Get configuration for GPT-3.5 Turbo"""
    return get_llm_config(model_key="gpt35_turbo")

def use_gpt35_16k():
    """Get configuration for GPT-3.5 Turbo 16k"""
    return get_llm_config(model_key="gpt35_16k") 