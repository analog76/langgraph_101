"""
Configuration file for loading environment variables
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Anthropic Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Validate required environment variables
if not ANTHROPIC_API_KEY:
    raise ValueError(
        "ANTHROPIC_API_KEY not found in environment variables.\n"
        "Please add it to your .env file:\n"
        "ANTHROPIC_API_KEY=your_actual_api_key_here"
    )

# Optional: Add other configuration variables here
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Model settings
DEFAULT_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")
DEFAULT_TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

# Export all config variables
__all__ = [
    "ANTHROPIC_API_KEY",
    "DEBUG",
    "ENVIRONMENT",
    "DEFAULT_MODEL",
    "DEFAULT_TEMPERATURE"
]
