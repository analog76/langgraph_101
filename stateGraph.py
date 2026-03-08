## Lesson 2 

import warnings
warnings.filterwarnings("ignore")

from typing import TypedDict
from langchain_core.messages import HumanMessage
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, START, END

# Import configuration from config.py
from config import ANTHROPIC_API_KEY, DEFAULT_MODEL, DEFAULT_TEMPERATURE


class PersonDictionary(TypedDict): # TypedDict acts as a Superclass
    name: str
    age: int
    is_student: bool

# Now lets create our own typed dictionary:
our_person: PersonDictionary = {
    "name": "James",
    "age": 25,
    "is_student": True
}

print(our_person)

class AgentState(TypedDict):
    user_message: HumanMessage

# Initialize LLM with Anthropic using config values
llm = ChatAnthropic(
    model=DEFAULT_MODEL,
    api_key=ANTHROPIC_API_KEY,
    temperature=DEFAULT_TEMPERATURE
)

def first_node(state: AgentState) -> AgentState:
    response = llm.invoke([state["user_message"]])
    print(f"\nAI: {response.content}")
    return state


graph = StateGraph(AgentState)
graph.add_node("node1", first_node)
graph.add_edge(START, "node1")
graph.add_edge("node1", END)
agent = graph.compile()

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    agent.invoke({"user_message": HumanMessage(content=user_input)})
