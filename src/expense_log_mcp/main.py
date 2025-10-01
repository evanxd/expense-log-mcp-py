import sys
import os
from dotenv import load_dotenv
from fastmcp import FastMCP

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from expense_log_mcp.auth import BearerTokenVerifier
from expense_log_mcp.tools import (
    add_expense,
    delete_expense,
    get_expense,
    get_expense_categories,
    get_grouped_expenses,
)

load_dotenv()

auth = BearerTokenVerifier(
    client_id="expense-log-agent",
    token=os.getenv("BEARER_TOKEN"),
)
mcp = FastMCP(name="Expense Log MCP", auth=auth)

mcp.tool(add_expense)
mcp.tool(delete_expense)
mcp.tool(get_expense)
mcp.tool(get_expense_categories)
mcp.tool(get_grouped_expenses)

if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=int(os.getenv("PORT")) | 8000)
