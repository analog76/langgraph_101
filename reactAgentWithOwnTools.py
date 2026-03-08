## Lesson 6

import warnings
warnings.filterwarnings("ignore")

from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool

# Import configuration from config.py
from config import ANTHROPIC_API_KEY, DEFAULT_MODEL, DEFAULT_TEMPERATURE

# Initialize LLM with Anthropic using config values
llm = ChatAnthropic(
    model=DEFAULT_MODEL,
    api_key=ANTHROPIC_API_KEY,
    temperature=DEFAULT_TEMPERATURE
)

# Custom tool: weather
@tool
def weather(city: str) -> str:
    """Get the weather in a given city"""
    return f"The weather in {city} is sunny"

tools = [weather, DuckDuckGoSearchRun()]
llm = llm.bind_tools(tools)

agent = create_react_agent(
    model=llm,
    tools=tools,
    name="weather_agent",
    prompt="You are my AI assistant that has access to certain tools. Use the tools to help me with my tasks.",
)

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ("exit", "quit"):
        print("Goodbye!")
        break

    result = agent.invoke({"messages": [HumanMessage(content=user_input)]})

    # Show any tool calls made
    for msg in result["messages"]:
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            print("Tool Calls:")
            for call in msg.tool_calls:
                print(f"  Tool: {call['name']}, Args: {call['args']}")

    print("\nAI:", result["messages"][-1].content, "\n")
