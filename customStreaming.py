from langchain_ollama import ChatOllama

# Create LLM
llm = ChatOllama(
    model="llama3.2",
    temperature=0,
)

# User input
question = input("Enter your prompt: ")

print("\nAI Response:\n")

# Stream tokens live
for chunk in llm.stream(question):
    print(chunk.content, end="", flush=True)  #flush->buffer

print("\n")