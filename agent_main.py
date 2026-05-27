from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain.agents import create_agent



# TOOLS
@tool
def get_student_grade(mark: int) -> str:
    """
    Return grade based on student marks.
    """

    if mark >= 90:
        return "A"

    elif mark >= 75:
        return "B"

    elif mark >= 50:
        return "C"

    else:
        return "Fail"

@tool
def divide_numbers(a: int, b: int) -> str:
    """
    Divide two numbers.
    """

    try:
        return str(a / b)

    except ZeroDivisionError:
        return "Cannot divide by zero."


@tool
def multiply_numbers(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@tool
def square_number(a: int) -> int:
    """Return square of a number."""
    return a * a


tools = [
    multiply_numbers,
    add_numbers,
    square_number,
    get_student_grade,
    divide_numbers
]


# -----------------------------
# MODEL
# -----------------------------

llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


# -----------------------------
# AGENT
# -----------------------------

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="You are a helpful AI assistant.",
    debug=True
)


# -----------------------------
# CHAT LOOP
# -----------------------------

print("\nAI Agent Started")
print("Type 'exit' to quit.\n")


while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    response = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": user_input
            }
        ]
    })

    print("\nAgent:")
    print(response["messages"][-1].content)
    print()