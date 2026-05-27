from langchain.tools import tool
from langchain.agents import create_agent
from langchain_ollama import ChatOllama

# Create Ollama model
model = ChatOllama(
    model="llama3.2",
    temperature=0.5
)

# Tool
@tool
def load_skill(skill_name: str) -> str:
    """Load a specialized skill prompt."""

    skills = {
        "write_sql": """
You are an SQL expert.
Write optimized MySQL queries.
Explain joins clearly.
""",

        "review_legal_doc": """
You are a legal document reviewer.
Find risky clauses and summarize them.
"""
    }

    return skills.get(skill_name, "Skill not found")


# Create agent
agent = create_agent(
    model=model,
    tools=[load_skill],
    system_prompt=(
        "You are a helpful assistant. "
        "You have access to two skills: "
        "write_sql and review_legal_doc. "
        "Use load_skill when needed."
    ),
)

# Run agent
response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Use write_sql skill and create query to find top 5 employees by salary"
            }
        ]
    }
)

last_msg = response["messages"][-1]
print(last_msg.content)