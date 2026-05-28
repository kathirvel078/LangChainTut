from pydantic import BaseModel
from langchain_ollama import ChatOllama


# Step 1: Create Schema
class Person(BaseModel):
    name: str
    age: int
    job: str


# Step 2: Create LLM
llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


# Step 3: Convert into structured LLM
structured_llm = llm.with_structured_output(Person)


# Step 4: User input
user_input = input("Enter text: ")


# Step 5: Invoke model
result = structured_llm.invoke(user_input)


# Step 6: Print result
print("\nStructured Output:\n")
print(result)

print("\nAccess Individual Fields:\n")
print("Name:", result.name)
print("Age:", result.age)
print("Job:", result.job)