##Lesson 5
import warnings
warnings.filterwarnings("ignore")

# All of our inputs for Agent 4
from langgraph.prebuilt import create_react_agent # Method to create ReAct agents easily
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_anthropic import ChatAnthropic

## Anthropic LLM definition.
from langchain_anthropic import ChatAnthropic
# Import configuration from config.py
from config import ANTHROPIC_API_KEY, DEFAULT_MODEL, DEFAULT_TEMPERATURE
# Initialize LLM with Anthropic using config values
llm = ChatAnthropic(
    model=DEFAULT_MODEL,
    api_key=ANTHROPIC_API_KEY,
    temperature=DEFAULT_TEMPERATURE
)
tools = [DuckDuckGoSearchRun()]

llm = llm.bind_tools(tools);




agent = create_react_agent(
    model = llm,
    tools = tools, # Passing in the list of tools
    name = "search_agent",
    prompt = "You are my AI assistant that has access to certain tools. Use the tools to help me with my tasks.", # Basic Prompt (no need for system messages!)
)
query = "Who won the Champions League Final 2025?"
query = "When is next summar olympics going to happen?"

result = agent.invoke({
    "messages": [{"role": "user", "content": query}]})

for msg in result["messages"]:
    if hasattr(msg, "tool_calls") and msg.tool_calls:
        print("Tool Calls:")
        for call in msg.tool_calls:
            print(f"  Tool: {call['name']}, Args: {call['args']}")

# Print the final answer
print("\nFinal Answer:")
print(result["messages"][-1].content)
