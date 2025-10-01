import json
from ..database import get_db
from ..models import Expense

def delete_expense(ledger_id: str, message_id: str) -> str:
    """
    Deletes an expense record.
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

        db.delete(expense)
        db.commit()

        return json.dumps({
            "success": True,
            "code": "OK",
            "message": "Expense deleted successfully.",
            "data": {
                "id": expense.id,
                "description": expense.description,
                "amount": expense.amount,
                "createdAt": expense.createdAt.strftime('%a %b %d %Y')
            }
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "code": "ERROR",
            "message": str(e),
        })