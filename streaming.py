from langchain.agents import create_agent
from langchain_core.messages import (
    AIMessage,
    HumanMessage
)

from langchain_core.tools import tool
from langchain_ollama import ChatOllama


# =====================================================
# TOOL
# =====================================================

@tool
def search_news(query: str) -> str:
    """
    Search latest AI news.
    """

    return (
        "OpenAI released new multimodal models. "
        "LangChain introduced advanced agent workflows."
    )


# =====================================================
# MODEL
# =====================================================

model = ChatOllama(
    model="llama3.2",
    temperature=0
)


# =====================================================
# AGENT
# =====================================================

agent = create_agent(
    model=model,
    tools=[search_news]
)


# =====================================================
# STREAM EXECUTION
# =====================================================

for chunk in agent.stream(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Search for AI news "
                    "and summarize the findings"
                )
            }
        ]
    },
    stream_mode="values"
):

    # Latest message in current state
    latest_message = chunk["messages"][-1]


    # -------------------------------------------------
    # HUMAN MESSAGE
    # -------------------------------------------------

    if isinstance(latest_message, HumanMessage):

        print("\nUSER:")
        print(latest_message.content)


    # -------------------------------------------------
    # AI MESSAGE
    # -------------------------------------------------

    elif isinstance(latest_message, AIMessage):

        # Tool call detection
        if latest_message.tool_calls:

            tool_names = [
                tc["name"]
                for tc in latest_message.tool_calls
            ]

            print("\nCALLING TOOLS:")
            print(tool_names)

        # Final/generated content
        elif latest_message.content:

            print("\nAGENT:")
            print(latest_message.content)