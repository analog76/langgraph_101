## Lesson 3

import warnings
warnings.filterwarnings("ignore")
import os
from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, START, END


# Import configuration from config.py
from config import ANTHROPIC_API_KEY, DEFAULT_MODEL, DEFAULT_TEMPERATURE

def myfunction(value: Union[int, float]):
    return value

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage, SystemMessage]]

# Initialize LLM with Anthropic using config values
llm = ChatAnthropic(
    model=DEFAULT_MODEL,
    api_key=ANTHROPIC_API_KEY,
    temperature=DEFAULT_TEMPERATURE
)


# This is the list we will be storing all of our conversation in
conversation_history = [SystemMessage(content="You are an AI Assistant that speaks like a pirate! Answer all of my questions properly")] 



def our_processing_node(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    state["messages"].append(AIMessage(content = response.content)) 
    
    print(f"\nAI: {response.content}")
    print(f"\nOur current state looks like: {state['messages']}")
    return state


graph = StateGraph(AgentState)
graph.add_node("llm_node", our_processing_node)
graph.add_edge(START, "llm_node")
graph.add_edge("llm_node", END) 
agent = graph.compile()


while True:
    user_input = input("Enter: ")
    conversation_history.append(HumanMessage(content = user_input))
    result = agent.invoke({"messages": conversation_history})
    conversation_history = result["messages"]