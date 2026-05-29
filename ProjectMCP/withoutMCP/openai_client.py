from openai import OpenAI
import json
from tool_executor import execute_tool

client = OpenAI(api_key="")
tools = [
    {
        "type": "function",
        "function": {
            "name": "read_tasks",
            "description": "Read all tasks",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "insert_task",
            "description": "Insert a new task",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"}
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer"}
                },
                "required": ["task_id"]
            }
        }
    }
]

def chat(user_message):
    messages = [{"role": "user", "content": user_message}]

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        tools=tools
    )

    msg = response.choices[0].message

    if msg.tool_calls:
        tool_call = msg.tool_calls[0]
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        result = execute_tool(name, args)

        print("Tool:", name)
        print("Result:", result)
    else:
        print(msg.content)

chat("load  Learn ai as task") #insert
chat("Show all tasks") #select