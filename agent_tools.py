from langchain.tools import tool


@tool
def multiply_numbers(a: int, b: int) -> int:
    """
    Multiply two numbers.
    """
    return a * b


@tool
def add_numbers(a: int, b: int) -> int:
    """
    Add two numbers.
    """
    return a + b


@tool
def square_number(a: int) -> int:
    """
    Return square of a number.
    """
    return a * a


# print(multiply_numbers.invoke({"a": 4, "b": 7}))
# print(add_numbers.invoke({"a": 10, "b": 20}))
# print(square_number.invoke({"a": 9}))
# print(multiply_numbers.name)
# print(multiply_numbers.description) #when sould i use this tool

tools = [
    multiply_numbers,
    add_numbers,
    square_number
]

if __name__ == "__main__":
    print(multiply_numbers.invoke({"a": 5, "b": 10}))
    print(add_numbers.invoke({"a": 20, "b": 30}))
    print(square_number.invoke({"a": 9}))

