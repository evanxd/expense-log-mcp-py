import json
from expense_log_mcp.database import get_db
from expense_log_mcp.models import Expense

def get_expense(ledger_id: str, message_id: str) -> str:
    """
    Retrieves the details of a single expense.
    """
    try:
        db = next(get_db())

        expense = db.query(Expense).filter_by(ledgerId=ledger_id, messageId=message_id).first()

        if not expense:
            return json.dumps({
                "success": False,
                "code": "NOT_FOUND",
                "message": "Expense not found.",
            })

        return json.dumps({
            "success": True,
            "code": "OK",
            "message": "Expense retrieved successfully.",
            "data": {
                "id": expense.id,
                "description": expense.description,
                "amount": expense.amount,
                "payer": expense.payer,
                "createdAt": expense.createdAt.isoformat(),
                "updatedAt": expense.updatedAt.isoformat(),
            }
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "code": "ERROR",
            "message": str(e),
        })
