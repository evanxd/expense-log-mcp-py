import json
from datetime import datetime, timedelta, timezone
from collections import defaultdict
from typing import List, Optional
from expense_log_mcp.database import get_db
from expense_log_mcp.models import Expense

def get_grouped_expenses(
    ledger_id: str,
    category_ids: Optional[List[str]] = None,
    payer_name: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    timezone_offset_hours: int = 8,
) -> str:
    """
    Retrieves and groups expenses by payer name and then by category name, returning the total amount for each category,
    with optional filters for category IDs, payer name, and a date range. The `start_date` and `end_date` should be
    ISO 8601 strings, always in UTC. The timezone for these dates can be adjusted using
    the `timezone_offset_hours` parameter (default: 8), which is an integer representing the UTC offset in hours.
    """
    try:
        db = next(get_db())
        query = db.query(Expense).filter(Expense.ledgerId == ledger_id)

        if category_ids:
            query = query.filter(Expense.categoryId.in_(category_ids))
        if payer_name:
            query = query.filter(Expense.payer == payer_name)
        if start_date:
            query = query.filter(
                Expense.createdAt
                >= datetime.fromisoformat(start_date).replace(
                    tzinfo=timezone(timedelta(hours=timezone_offset_hours))
                )
            )
        if end_date:
            query = query.filter(
                Expense.createdAt
                <= datetime.fromisoformat(end_date).replace(
                    tzinfo=timezone(timedelta(hours=timezone_offset_hours))
                )
            )

        expenses = query.order_by(Expense.payer).all()
        grouped_expenses = defaultdict(lambda: {"expenseCategories": defaultdict(float), "totalAmount": 0.0})

        for expense in expenses:
            amount = expense.amount
            grouped_expenses[expense.payer]["expenseCategories"][expense.category.name] += amount
            grouped_expenses[expense.payer]["totalAmount"] += amount

        return json.dumps({
            "success": True,
            "code": "OK",
            "message": "Grouped expenses retrieved successfully.",
            "data": grouped_expenses
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "code": "ERROR",
            "message": str(e),
        })
