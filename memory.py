from typing import TypedDict

from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.tools import tool


# Ollama
llm = ChatOllama(model="llama3.2")


# Tool
@tool
def get_user_info() -> str:
    """Return user information."""

    return "User is Kathir"


# Custom state
class CustomAgentState(TypedDict):
    messages: list
    user_id: str
    preferences: dict


# Memory
memory = InMemorySaver()


# Agent
agent = create_agent(
    model=llm,
    tools=[get_user_info],
    checkpointer=memory,
    state_schema=CustomAgentState,
)


# First call
response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Hi my name is Kathir"
            }
        ],
        "user_id": "123",
        "preferences": {"theme": "dark"}
    },
    {
        "configurable": {
            "thread_id": "1"
        }
    }
)

print(response["messages"][-1].content)