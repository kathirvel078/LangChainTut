from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.utils.uuid import uuid7


# ----------------------------------------
# MODEL
# ----------------------------------------

model = ChatOllama(
    model="llama3.2",
    temperature=0
)


# ----------------------------------------
# MEMORY CHECKPOINTER
# ----------------------------------------

memory = InMemorySaver()


# ----------------------------------------
# AGENT
# ----------------------------------------

agent = create_agent(
    model=model,
    tools=[],
    checkpointer=memory,
)


# ----------------------------------------
# THREAD ID
# ----------------------------------------

thread_id = str(uuid7())

config = {
    "configurable": {
        "thread_id": thread_id
    }
}


# ----------------------------------------
# FIRST MESSAGE
# ----------------------------------------

result1 = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "My favorite city is Chennai."
            }
        ]
    },
    config=config,
)

print("\nFIRST RESPONSE:\n")
print(result1["messages"][-1].content)


# ----------------------------------------
# SECOND MESSAGE
# ----------------------------------------

result2 = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What city did I mention earlier?"
            }
        ]
    },
    config=config,
)

print("\nSECOND RESPONSE:\n")
print(result2["messages"][-1].content)