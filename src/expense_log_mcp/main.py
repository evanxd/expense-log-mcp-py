import subprocess
# Workaround: Run prisma generate since FastMCP Cloud doesn't support setup commands.
subprocess.run(["python", "-m", "prisma", "generate"], check=True)
import os
from dotenv import load_dotenv
from fastmcp import FastMCP

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
