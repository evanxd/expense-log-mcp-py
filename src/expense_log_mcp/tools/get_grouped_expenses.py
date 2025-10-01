import json
from datetime import datetime
from collections import defaultdict
from typing import List, Optional
from expense_log_mcp.database import get_db
from expense_log_mcp.models import Expense

def get_grouped_expenses(
    ledger_id: str,
    category_ids: Optional[List[str]] = None,
    payer: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> str:
    """
    Retrieves and groups expenses by payer and then by category name, returning the total amount for each category,
    with optional filters for category IDs, payer, and a date range.
    """
    try:
        db = next(get_db())

        query = db.query(Expense).filter(Expense.ledgerId == ledger_id)

        if category_ids:
            query = query.filter(Expense.categoryId.in_(category_ids))
        if payer:
            query = query.filter(Expense.payer == payer)
        if start_date:
            query = query.filter(Expense.createdAt >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Expense.createdAt <= datetime.fromisoformat(end_date))

        expenses = query.all()

        grouped_expenses = defaultdict(lambda: {"expenseCategories": defaultdict(float), "totalAmount": 0.0})

        for expense in expenses:
            payer_name = expense.payer
            category_name = expense.category.name
            amount = expense.amount

            grouped_expenses[payer_name]["expenseCategories"][category_name] += amount
            grouped_expenses[payer_name]["totalAmount"] += amount

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
