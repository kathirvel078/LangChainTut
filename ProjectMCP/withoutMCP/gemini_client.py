from google import genai
from tool_executor import execute_tool

client = genai.Client(api_key="")

tools = [{
    "function_declarations": [
        {
            "name": "insert_task",
            "description": "Insert a new task",
            "parameters": {
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
            "parameters": {
                "type": "object",
                "properties": {}
            }
        },
        {
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
    ]
}]


def chat(prompt):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config={
            "tools": tools
        }
    )

    candidate = response.candidates[0]
    part = candidate.content.parts[0]

    if hasattr(part, "function_call"):
        name = part.function_call.name
        args = dict(part.function_call.args)

        result = execute_tool(name, args)

        print("Tool:", name)
        print("Result:", result)
    else:
        print(response.text)

chat("Create a task Learn Geminiii tools")