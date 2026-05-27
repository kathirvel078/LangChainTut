from typing import TypedDict

from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain.agents.middleware import dynamic_prompt, wrap_tool_call
from langchain_core.messages import ToolMessage
from langchain.agents.middleware.types import ModelRequest
from langchain.agents import create_agent


# --------------------------------------------------
# CONTEXT
# --------------------------------------------------

class Context(TypedDict):
    user_role: str


# --------------------------------------------------
# DYNAMIC SYSTEM PROMPT
# --------------------------------------------------

@dynamic_prompt
def user_role_prompt(request: ModelRequest) -> str:
    """
    Generate system prompt dynamically
    based on runtime context.
    """

    user_role = request.runtime.context.get(
        "user_role",
        "user"
    )

    base_prompt = "You are a helpful assistant."

    if user_role == "expert":
        return (
            f"{base_prompt} "
            "Provide detailed technical responses."
        )

    elif user_role == "beginner":
        return (
            f"{base_prompt} "
            "Explain concepts simply and avoid jargon."
        )

    return base_prompt


# --------------------------------------------------
# TOOL
# --------------------------------------------------

@tool
def square_number(a: int) -> int:
    """
    Return square of a number.
    """

    return a * a


# --------------------------------------------------
# TOOL ERROR HANDLER
# --------------------------------------------------

@wrap_tool_call
def handle_tool_errors(request, handler):

    try:
        return handler(request)

    except Exception as e:

        return ToolMessage(
            content=f"Tool error: {str(e)}",
            tool_call_id=request.tool_call["id"]
        )


# --------------------------------------------------
# MODEL
# --------------------------------------------------

llm = ChatOllama(
    model="llama3.2",
    temperature=0,
    name="research_assistant"
)


# --------------------------------------------------
# AGENT 
# --------------------------------------------------

agent = create_agent(
    model=llm,
    tools=[square_number],
    middleware=[
        user_role_prompt,
        handle_tool_errors
    ]
)


# --------------------------------------------------
# BEGINNER REQUEST
# --------------------------------------------------

beginner_response = agent.invoke(
    {
        "messages": [
            (
                "user",
                "What is an AI agent?"
            )
        ]
    },
    context={
        "user_role": "beginner"
    }
)

print("\nBEGINNER RESPONSE:\n")
print(beginner_response["messages"][-1].content)


# --------------------------------------------------
# EXPERT REQUEST
# --------------------------------------------------

expert_response = agent.invoke(
    {
        "messages": [
            (
                "user",
                "What is an AI agent?"
            )
        ]
    },
    context={
        "user_role": "expert"
    }
)

print("\nEXPERT RESPONSE:\n")
print(expert_response["messages"][-1].content)