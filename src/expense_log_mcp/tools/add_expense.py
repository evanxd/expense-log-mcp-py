import json
from expense_log_mcp.database import get_db
from expense_log_mcp.models import Expense
from typing import Callable
from cuid2 import cuid_wrapper

cuid_generator: Callable[[], str] = cuid_wrapper()


def add_expense(
    ledger_id: str,
    category_id: str,
    message_id: str,
    description: str,
    amount: float,
    payer: str,
) -> str:
    """
    Adds a new expense record.
    """
    try:
        db = next(get_db())

        expense = Expense(
            id=cuid_generator(),
            ledgerId=ledger_id,
            categoryId=category_id,
            messageId=message_id,
            description=description,
            amount=amount,
            payer=payer,
        )

        db.add(expense)
        db.commit()
        db.refresh(expense)

        return json.dumps(
            {
                "success": True,
                "code": "OK",
                "message": "Expense added successfully.",
                "data": {"expenseId": expense.id},
            }
        )
    except Exception as e:
        return json.dumps(
            {
                "success": False,
                "code": "ERROR",
                "message": str(e),
            }
        )
