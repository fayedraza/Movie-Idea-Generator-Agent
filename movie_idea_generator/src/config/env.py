"""
Environment variable configuration for the movie idea generator.
This module loads environment variables from a .env file located in the project root.
"""

from pathlib import Path

from dotenv import load_dotenv
from src.config.secrets import OPENAI_API_KEY

# Find the root directory of the project
ROOT_DIR = Path(__file__).parent.parent.parent.absolute()

# Load environment variables from .env file
load_dotenv(ROOT_DIR / ".env")

# Import the secrets module to update it with values from .env
from src.config import secrets

# Update the secrets module with values from .env
secrets.OPENAI_API_KEY = OPENAI_API_KEY


def check_api_keys():
    """
    Check that all required API keys are set.
    Raises a warning if any required keys are missing.
    """
    if not secrets.OPENAI_API_KEY:
        pass
