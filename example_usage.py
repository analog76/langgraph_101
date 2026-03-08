"""
Example usage of the configuration and Fundamentals module
"""

# Import from config.py to use environment variables
from config import (
    ANTHROPIC_API_KEY,
    DEFAULT_MODEL,
    DEFAULT_TEMPERATURE,
    DEBUG,
    ENVIRONMENT
)

# Display loaded configuration (hiding sensitive data)
print("=" * 50)
print("Configuration Loaded Successfully!")
print("=" * 50)
print(f"Environment: {ENVIRONMENT}")
print(f"Debug Mode: {DEBUG}")
print(f"Model: {DEFAULT_MODEL}")
print(f"Temperature: {DEFAULT_TEMPERATURE}")
print(f"API Key: {'*' * 20}{ANTHROPIC_API_KEY[-4:] if ANTHROPIC_API_KEY else 'NOT SET'}")
print("=" * 50)

# Example: Using the agent from Fundamentals.py
if __name__ == "__main__":
    from langchain_core.messages import HumanMessage
    from Fundamentals import agent

    print("\nRunning Agent Test...")
    print("-" * 50)

    # Test the agent
    user_input = "Hello! Can you tell me a short joke?"
    result = agent.invoke({
        "user_message": HumanMessage(content=user_input)
    })

    print(f"\nUser: {user_input}")
    print("-" * 50)
