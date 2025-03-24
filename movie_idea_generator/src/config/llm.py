"""
LLM configuration utilities for working with OpenAI models.
This module provides helper functions to create and configure OpenAI clients.
"""

from openai import OpenAI
from src.config.config import LLM_CONFIG, OPENAI_MODELS
from src.config.secrets import OPENAI_API_KEY

def get_openai_client():
    """
    Create and return an instance of the OpenAI client.
    
    Returns:
        OpenAI: Configured OpenAI client instance
    """
    return OpenAI(api_key=OPENAI_API_KEY, timeout=LLM_CONFIG.get("request_timeout", 120))

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

def create_chat_completion(messages, model_key=None, temperature=None, max_tokens=None):
    """
    Create a chat completion using the OpenAI client.
    
    Args:
        messages (list): List of message dictionaries for the conversation
        model_key (str, optional): Key from OPENAI_MODELS to use. Defaults to None.
        temperature (float, optional): Temperature setting. Defaults to None.
        max_tokens (int, optional): Max tokens setting. Defaults to None.
    
    Returns:
        ChatCompletion: The response from the OpenAI API
    """
    config = get_llm_config(model_key, temperature, max_tokens)
    client = get_openai_client()
    
    return client.chat.completions.create(
        model=config["model"],
        messages=messages,
        temperature=config["temperature"],
        max_tokens=config.get("max_tokens", 4000)
    )

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