## Lesson 1 

import warnings
warnings.filterwarnings("ignore")

from typing import TypedDict
from langchain_core.messages import HumanMessage
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, START, END

# Import configuration from config.py
from config import ANTHROPIC_API_KEY, DEFAULT_MODEL, DEFAULT_TEMPERATURE

# Define the State
class AgentState(TypedDict):
    user_message: HumanMessage

# Initialize LLM with Anthropic using config values
llm = ChatAnthropic(
    model=DEFAULT_MODEL,
    api_key=ANTHROPIC_API_KEY,
    temperature=DEFAULT_TEMPERATURE
)

# Define the Node Function
def first_node(state: AgentState):
    response = llm.invoke([state["user_message"]])
    print(f"AI: {response.content}")
    return state


# Build the Graph
graph = StateGraph(AgentState)
graph.add_node("node_1", first_node)
graph.add_edge(START, "node_1")
graph.add_edge("node_1", END)

# Compile the Agent
agent = graph.compile()

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ("exit", "quit"):
        print("Goodbye!")
        break
    agent.invoke({"user_message": HumanMessage(content=user_input)})
