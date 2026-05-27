from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver


# MODEL
llm = ChatOllama(
    model="llama3.2",
    temperature=0
)

# TOOL
@tool
def calculator_tool(query: str) -> str:
    """
    Simple calculator tool
    """

    try:
        result = eval(query)
        return f"Result: {result}"

    except Exception as e:
        return f"Error: {str(e)}"

# MEMORY
memory = InMemorySaver()

# SYSTEM PROMPT
system_message = """
You are a Math Expert Assistant.

Rules:
- Use calculator_tool for math calculations
- Explain answers simply
- Be accurate
"""
# AGENT
agent = create_agent(
    model=llm,
    tools=[calculator_tool],
    checkpointer=memory,
    system_prompt=system_message
)

# CHAT LOOP
print("AI Agent Started")
print("Type 'exit' to stop\n")

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        },
        config={
            "configurable": {
                "thread_id": "1"
            }
        }
    )
    print("\nAI:")

    # Print only assistant message
    print(response["messages"][-1].content)

    print()