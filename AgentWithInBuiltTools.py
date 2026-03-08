## Lesson 4

import warnings
warnings.filterwarnings("ignore")


# All of the imports needed for Agent 3
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import SystemMessage, BaseMessage, AIMessage, HumanMessage # Message for providing instructions to the LLM
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_anthropic import ChatAnthropic


# Import configuration from config.py
from config import ANTHROPIC_API_KEY, DEFAULT_MODEL, DEFAULT_TEMPERATURE


query = "Who won the Champions League final 2025?"

search = DuckDuckGoSearchRun() # Search Tool
print("\nSEARCH: ", search.invoke(query))


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages] # Reducer Function - essentially allows for the addition of messages without getting deleted

tools = [DuckDuckGoSearchRun()] # We create a list of tools we want our Agent to have access to

# Initialize LLM with Anthropic using config values
llm = ChatAnthropic(
    model=DEFAULT_MODEL,
    api_key=ANTHROPIC_API_KEY,
    temperature=DEFAULT_TEMPERATURE
).bind_tools(tools)

def model_call(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content=
        "You are my AI assistant, please answer my query to the best of your ability."
    )
    response = llm.invoke([system_prompt] + list(state["messages"])) # Sending in both the System Message and the current state
    return {"messages": [response]}


# Underlying action behind the conditional edge
def should_continue(state: AgentState):
    messages = state["messages"] # Copies the latest state into the "messages" variable
    last_message = messages[-1] # Only looks at the last message

    # This code checks if there are any further tool calling required in the last message
    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"

# Creation of our graph again:
graph = StateGraph(AgentState)
graph.add_node("our_agent", model_call)


tool_node = ToolNode(tools=tools) # Here we create a ToolNode - a node that neatly contains all of the tools we want our agent to have
graph.add_node("tools", tool_node)

graph.set_entry_point("our_agent")

# How to create a conditional edge
graph.add_conditional_edges(
    "our_agent", # Origin
    should_continue, # Underlying action
    { # Different edges along with their destinations
        "continue": "tools",
        "end": END,
    },
)

graph.add_edge("tools", "our_agent")

agent = graph.compile()


while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ("exit", "quit"):
        print("Goodbye!")
        break
    response = agent.invoke({"messages": [HumanMessage(content=user_input)]})
    print("\nAI:", response["messages"][-1].content)
