import json
from prisma import Prisma

async def add_expense(ledger_id: str, category_id: str, message_id: str, description: str, amount: float, payer: str) -> str:
    """
    Adds a new expense record.
    """
    try:
        db = Prisma()
        await db.connect()

        expense = await db.expense.create(
            data={
                "ledgerId": ledger_id,
                "categoryId": category_id,
                "messageId": message_id,
                "description": description,
                "amount": amount,
                "payer": payer,
            }
        )

        await db.disconnect()

        return json.dumps({
            "success": True,
            "code": "OK",
            "message": "Expense added successfully.",
            "data": {
                "expenseId": expense.id
            }
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "code": "ERROR",
            "message": str(e),
        })
