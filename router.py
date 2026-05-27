from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain.agents import create_agent
from pydantic import BaseModel, Field

# MODEL
model = ChatOllama(
    model="llama3.2",
    temperature=0
)

# DOCS AGENT
class DocsInput(BaseModel):
    query: str = Field(description="Documentation question")


@tool(args_schema=DocsInput)
def docs_search(query: str) -> str:
    """
    Search documentation
    """

    return f"Documentation result for: {query}"


docs_agent = create_agent(
    model=model,
    tools=[docs_search],
    system_prompt="""
    You are a documentation expert.
    Answer documentation-related questions.
    """
)

# CODE AGENT
class CodeInput(BaseModel):
    query: str = Field(description="Programming question")


@tool(args_schema=CodeInput)
def code_helper(query: str) -> str:
    """
    Help with programming questions
    """

    return f"Code solution for: {query}"


code_agent = create_agent(
    model=model,
    tools=[code_helper],
    system_prompt="""
    You are a coding expert.
    Answer programming questions.
    """
)

# ROUTER TOOLS
@tool
def ask_docs_agent(query: str) -> str:
    """
    Send documentation questions to docs agent
    """

    response = docs_agent.invoke({
        "messages": [
            {"role": "user", "content": query}
        ]
    })

    return response["messages"][-1].content


@tool
def ask_code_agent(query: str) -> str:
    """
    Send coding questions to code agent
    """

    response = code_agent.invoke({
        "messages": [
            {"role": "user", "content": query}
        ]
    })

    return response["messages"][-1].content

# ROUTER AGENT
router_agent = create_agent(
    model=model,
    tools=[ask_docs_agent, ask_code_agent],
    system_prompt="""
    You are a router agent.

    - Use ask_docs_agent for documentation questions
    - Use ask_code_agent for programming questions
    """
)

# TEST
response = router_agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "How to create FastAPI routes?"
        }
    ]
})

print(response["messages"][-1].content)