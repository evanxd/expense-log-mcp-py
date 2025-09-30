import json
from prisma import Prisma

async def get_expense_categories() -> str:
    """
    Retrieves the list of all expense categories.
    """
    try:
        db = Prisma()
        await db.connect()

        categories = await db.expensecategory.find_many()

        await db.disconnect()

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
