# from langchain_ollama import ChatOllama
from langchain.chat_models import init_chat_model

# model = ChatOllama(
#     model="llama3.2",
#     temperature=0
# )
model = init_chat_model(
    "llama3.2",
    model_provider="ollama",
    # Kwargs passed to the model:
    temperature=0.7,
    timeout=30,
    max_tokens=1000,
    max_retries=6,  # Default; increase for unreliable networks
)

response = model.invoke("Hello")

print(response.content)