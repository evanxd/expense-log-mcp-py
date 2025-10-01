import json
from prisma import Prisma

async def delete_expense(ledger_id: str, message_id: str) -> str:
    """
    Deletes an expense record.
    """
    try:
        db = Prisma()
        await db.connect()

        expense = await db.expense.find_unique(
            where={
                "ledgerId_messageId": {
                    "ledgerId": ledger_id,
                    "messageId": message_id,
                }
            }
        )

        if not expense:
            return json.dumps({
                "success": False,
                "code": "NOT_FOUND",
                "message": "Expense not found.",
            })

        await db.expense.delete(
            where={
                "ledgerId_messageId": {
                    "ledgerId": ledger_id,
                    "messageId": message_id,
                }
            }
        )

        await db.disconnect()

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
