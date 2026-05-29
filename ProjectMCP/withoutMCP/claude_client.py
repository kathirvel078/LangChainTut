import anthropic
from tool_executor import execute_tool

client = anthropic.Anthropic(api_key="")
tools = [
    {
        "name": "insert_task",
        "description": "Insert a new task",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string"}
            },
            "required": ["title"]
        }
    },
    {
        "name": "read_tasks",
        "description": "Read all tasks",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "delete_task",
        "description": "Delete a task",
        "input_schema": {
            "type": "object",
            "properties": {
                "task_id": {"type": "integer"}
            },
            "required": ["task_id"]
        }
    }
]

def chat(prompt):
    messages = [{"role": "user", "content": prompt}]

    response = client.messages.create(
        model="claude-sonnet-4-0",
        max_tokens=300,
        messages=messages,
        tools=tools
    )

    tool_used = False

    for block in response.content:
        if block.type == "tool_use":
            tool_used = True
            name = block.name
            args = block.input

            result = execute_tool(name, args)

            print("Tool executed:", name)
            print("Result:", result)

    if not tool_used:
        print(response.content[0].text)



chat("Create a task Learn aii tools")
chat("Show all tasks")