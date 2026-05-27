from pydantic import BaseModel
from langchain.agents.structured_output import ProviderStrategy
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain_ollama import ChatOllama


# ---------------------------------------------------
# STRUCTURED SCHEMA
# ---------------------------------------------------

class ContactInfo(BaseModel):
    name: str
    email: str
    phone: str


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
    # response_format=ToolStrategy(ContactInfo)
    response_format=ProviderStrategy(ContactInfo)
)


# ---------------------------------------------------
# INPUT
# ---------------------------------------------------

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Extract contact info from: "
                    "John Doe, "
                    "john@example.com, "
                    "(555) 123-4567"
                )
            }
        ]
    }
)


# ---------------------------------------------------
# OUTPUT
# ---------------------------------------------------

print("\nRAW RESULT:\n")
print(result)

print("\nSTRUCTURED RESPONSE:\n")
print(result["structured_response"])