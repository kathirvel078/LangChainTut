from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama


# =========================
# LLM
# =========================

llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


# =========================
# STATE
# Shared memory between nodes
# =========================

class AgentState(TypedDict):
    question: str
    route: str
    answer: str


# =========================
# ROUTER NODE
# Deterministic + AI logic
# =========================

def router_node(state: AgentState):

    question = state["question"].lower()

    coding_keywords = [
        "python",
        "code",
        "bug",
        "function",
        "api",
        "javascript"
    ]

    if any(word in question for word in coding_keywords):
        route = "coding"
    else:
        route = "general"

    return {
        **state,
        "route": route
    }


# =========================
# CODING AGENT NODE
# Agentic step
# =========================

def coding_node(state: AgentState):

    question = state["question"]

    prompt = f"""
    You are a senior software engineer.

    Answer this coding question clearly:

    {question}
    """

    response = llm.invoke(prompt)

    return {
        **state,
        "answer": response.content
    }


# =========================
# GENERAL CHAT NODE
# Agentic step
# =========================

def general_node(state: AgentState):

    question = state["question"]

    prompt = f"""
    You are a helpful AI assistant.

    Answer this question:

    {question}
    """

    response = llm.invoke(prompt)

    return {
        **state,
        "answer": response.content
    }


# =========================
# CONDITIONAL ROUTING
# =========================

def route_decision(state: AgentState):

    return state["route"]


# =========================
# BUILD GRAPH
# =========================

workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("router", router_node)
workflow.add_node("coding_agent", coding_node)
workflow.add_node("general_agent", general_node)

# Entry point
workflow.set_entry_point("router")

# Conditional edges
workflow.add_conditional_edges(
    "router",
    route_decision,
    {
        "coding": "coding_agent",
        "general": "general_agent"
    }
)

# Finish edges
workflow.add_edge("coding_agent", END)
workflow.add_edge("general_agent", END)

# Compile graph
app = workflow.compile()


# =========================
# RUN
# =========================

while True:

    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        break

    result = app.invoke({
        "question": user_input,
        "route": "",
        "answer": ""
    })

    print("\nAI:")
    print(result["answer"])