import json
from unittest.mock import MagicMock, patch

from expense_log_mcp.models import ExpenseCategory
from expense_log_mcp.tools.get_expense_categories import get_expense_categories


def test_get_expense_categories_success():
    """
    Test that get_expense_categories returns a JSON string with a list of expense categories.
    """
    mock_db = MagicMock()

    mock_categories = [
        ExpenseCategory(id=1, name="Food"),
        ExpenseCategory(id=2, name="Transport"),
    ]

    mock_db.query.return_value.all.return_value = mock_categories

    with patch("expense_log_mcp.tools.get_expense_categories.get_db") as mock_get_db:
        mock_get_db.return_value = iter([mock_db])

        result = get_expense_categories()

        expected_result = {
            "success": True,
            "code": "OK",
            "message": "Expense categories retrieved successfully.",
            "data": [
                {"expenseCategoryId": 1, "expenseCategoryName": "Food"},
                {"expenseCategoryId": 2, "expenseCategoryName": "Transport"},
            ],
        }
        assert json.loads(result) == expected_result


def test_get_expense_categories_exception():
    """
    Test that get_expense_categories returns a JSON string with an error message
    when an exception occurs.
    """
    with patch("expense_log_mcp.tools.get_expense_categories.get_db") as mock_get_db:
        mock_get_db.side_effect = Exception("Something went wrong")

        result = get_expense_categories()

        expected_result = {
            "success": False,
            "code": "ERROR",
            "message": "Something went wrong",
        }
        assert json.loads(result) == expected_result
