from langchain_ollama import ChatOllama
from langgraph.types import Command

llm = ChatOllama(model="llama3.2")


def classify_query(query: str) -> str:

    prompt = f"""
    Classify the query into one of these agents:

    - sql_agent
    - coding_agent
    - support_agent

    Query: {query}

    Return only the agent name.
    """

    response = llm.invoke(prompt)

    print(response.content)   # print output

    return response.content.strip()


def route_query(state):

    active_agent = classify_query(state["query"])

    print(active_agent)   # print selected agent

    return Command(goto=active_agent)