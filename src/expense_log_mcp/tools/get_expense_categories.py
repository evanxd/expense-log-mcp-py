import json
from expense_log_mcp.database import get_db
from expense_log_mcp.models import ExpenseCategory

def get_expense_categories() -> str:
    """
    Retrieves the list of all expense categories.
    """
    try:
        db = next(get_db())

        categories = db.query(ExpenseCategory).all()

        return json.dumps({
            "success": True,
            "code": "OK",
            "message": "Expense categories retrieved successfully.",
            "data": [
                {
                    "expenseCategoryId": category.id,
                    "expenseCategoryName": category.name
                }
                for category in categories
            ]
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "code": "ERROR",
            "message": str(e),
        })
