from mcp.server.fastmcp import FastMCP
from db_tools import read_tasks, insert_task, update_task

mcp = FastMCP("mysql-tools")

@mcp.tool()
def read_tasks_tool():
    return read_tasks()

@mcp.tool()
def insert_task_tool(title: str):
    return insert_task(title)

@mcp.tool()
def update_task_tool(task_id: int, title: str):
    return update_task(task_id, title)

if __name__ == "__main__":
    mcp.run()
    print("MCP SERVER STARTED")