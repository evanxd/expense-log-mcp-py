import json
from prisma import Prisma
from datetime import datetime
from collections import defaultdict
from typing import List, Optional

async def get_grouped_expenses(
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
        db = Prisma()
        await db.connect()

        where_clause = {"ledgerId": ledger_id}
        if category_ids:
            where_clause["categoryId"] = {"in": category_ids}
        if payer:
            where_clause["payer"] = payer
        if start_date:
            where_clause["createdAt"] = {"gte": datetime.fromisoformat(start_date)}
        if end_date:
            if "createdAt" not in where_clause:
                where_clause["createdAt"] = {}
            where_clause["createdAt"]["lte"] = datetime.fromisoformat(end_date)

        expenses = await db.expense.find_many(
            where=where_clause,
            include={"category": True}
        )

        await db.disconnect()

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
