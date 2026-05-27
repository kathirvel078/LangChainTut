from typing import Any
from typing_extensions import TypedDict

from langchain.agents import (
    create_agent,
    AgentState
)

from langchain.agents.middleware import (
    AgentMiddleware
)

from langchain_ollama import ChatOllama


# ---------------------------------------------------
# CUSTOM STATE
# ---------------------------------------------------

class CustomState(AgentState):

    user_preferences: dict


# ---------------------------------------------------
# CUSTOM MIDDLEWARE
# ---------------------------------------------------

class CustomMiddleware(AgentMiddleware):

    state_schema = CustomState

    def before_model(
        self,
        state: CustomState,
        runtime
    ) -> dict[str, Any] | None:     #This function run before LLM call

        preferences = state.get(
            "user_preferences",
            {}
        )

        style = preferences.get(
            "style",
            "normal"
        )

        verbosity = preferences.get(
            "verbosity",
            "detailed"
        )

        system_message = (
            f"User prefers {style} explanations "
            f"with {verbosity} detail."
        )

        return {
            "messages": [
                {
                    "role": "system",
                    "content": system_message
                }
            ]
        }


# ---------------------------------------------------
# MODEL
# ---------------------------------------------------

model = ChatOllama(
    model="llama3.2",
    temperature=0
)


# ---------------------------------------------------
# AGENT
# ---------------------------------------------------

agent = create_agent(
    model=model,
    tools=[],
    middleware=[CustomMiddleware()]

)


# ---------------------------------------------------
# INVOKE
# ---------------------------------------------------

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Explain what an AI agent is."
                )
            }
        ],

        "user_preferences": {
            "style": "technical",
            "verbosity": "detailed"
        }
    }
)


# ---------------------------------------------------
# OUTPUT
# ---------------------------------------------------

print(result)