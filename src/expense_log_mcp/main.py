import os
from dotenv import load_dotenv
from fastmcp import FastMCP
from tools import (
    add_expense,
    delete_expense,
    get_expense,
    get_expense_categories,
    get_grouped_expenses,
)

load_dotenv()

mcp = FastMCP("Expense Log MCP")

mcp.tool(add_expense)
mcp.tool(delete_expense)
mcp.tool(get_expense)
mcp.tool(get_expense_categories)
mcp.tool(get_grouped_expenses)

if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=int(os.getenv("PORT")) | 8000)
