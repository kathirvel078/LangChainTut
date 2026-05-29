import asyncio
from openai import OpenAI
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession

client = OpenAI(api_key="")
async def main():
    server = StdioServerParameters(
        command="python",
        args=["db_mcp_server.py"]
    )

    async with stdio_client(server) as (r, w):
        async with ClientSession(r, w) as session:
            await session.initialize()

            mcp_tools = await session.list_tools()

            # Convert MCP tools → OpenAI format
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": t.name,
                        "description": t.description or "MCP tool",
                        "parameters": t.inputSchema
                    }
                }
                for t in mcp_tools.tools
            ]

            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{
                    "role": "user",
                    "content": "Insert task Learn MCP OpenAIII"
                }],
                tools=tools
            )

            msg = response.choices[0].message

            if msg.tool_calls:
                tool_call = msg.tool_calls[0]

                print("Executing MCP tool:", tool_call.function.name)

                result = await session.call_tool(
                    tool_call.function.name,
                    eval(tool_call.function.arguments)
                )

                print("MCP result:", result)

asyncio.run(main())