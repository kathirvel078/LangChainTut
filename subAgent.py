from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

# MODEL
llm = ChatOllama(
    model="llama3.2",
    temperature=0
)
memory = InMemorySaver()

# SUB-AGENT
math_subagent = create_agent(
    tools=[],
    model=llm,
    system_prompt=(
        """
        You are a Math Expert Sub-Agent.

        Your job:
        - solve math problems
        - explain clearly
        - only focus on calculations
        """
    )
)
# WRAP SUB-AGENT AS TOOL
@tool
def call_math_subagent(query: str) -> str:
    """
    Use this tool for math calculations and math questions.
    """

    result = math_subagent.run(query)

    return result

# MAIN AGENT
main_agent = create_agent(
    tools=[call_math_subagent],
    model=llm,
    checkpointer=memory,
    system_prompt=
        """
        You are the Main Agent.

        Rules:
        - Use call_math_subagent for math tasks
        - Answer normal questions yourself
        """

)

# CHAT LOOP
print("\nMain Agent Started")
print("Type 'exit' to stop\n")

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    response = main_agent.invoke(
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
    print(response["messages"][-1].content)
    print()