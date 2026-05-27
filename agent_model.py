from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage


llm = ChatOllama(
    model="llama3.2",
    temperature=0.1
)

# llm = ChatOllama(
#     model="deepseek-coder",
#     temperature=0.1
# )

messages = [
    SystemMessage(
        content="You are a helpful AI assistant."
        # content="you are computer science or programming "
    ),
    HumanMessage(
        content="What is an Vector Database?"
    )
]

response = llm.invoke(messages)

print(response.content)