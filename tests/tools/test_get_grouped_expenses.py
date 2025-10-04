import json
from unittest.mock import MagicMock, patch
from datetime import datetime
from expense_log_mcp.models import Expense, ExpenseCategory
from expense_log_mcp.tools.get_grouped_expenses import get_grouped_expenses


def test_get_grouped_expenses_success():
    """
    Tests that get_grouped_expenses returns grouped expenses successfully.
    """
    mock_category = ExpenseCategory(id=1, name="Test Category")
    mock_expenses = [
        Expense(
            id=1,
            ledgerId="test-ledger",
            description="Test Expense 1",
            amount=100.0,
            payer="payer1",
            categoryId=1,
            category=mock_category,
            createdAt=datetime.now(),
            updatedAt=datetime.now(),
        ),
        Expense(
            id=2,
            ledgerId="test-ledger",
            description="Test Expense 2",
            amount=200.0,
            payer="payer2",
            categoryId=1,
            category=mock_category,
            createdAt=datetime.now(),
            updatedAt=datetime.now(),
        ),
        Expense(
            id=3,
            ledgerId="test-ledger",
            description="Test Expense 3",
            amount=50.0,
            payer="payer1",
            categoryId=1,
            category=mock_category,
            createdAt=datetime.now(),
            updatedAt=datetime.now(),
        ),
    ]

    with patch("expense_log_mcp.tools.get_grouped_expenses.get_db") as mock_get_db:
        mock_db = MagicMock()
        mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = (
            mock_expenses
        )
        mock_get_db.return_value = iter([mock_db])

        result = get_grouped_expenses(ledger_id="test-ledger")
        result_json = json.loads(result)

        assert result_json["success"] is True
        assert result_json["code"] == "OK"
        assert "payer1" in result_json["data"]
        assert "payer2" in result_json["data"]
        assert result_json["data"]["payer1"]["expenseCategories"]["Test Category"] == 150.0
        assert result_json["data"]["payer1"]["totalAmount"] == 150.0
        assert result_json["data"]["payer2"]["expenseCategories"]["Test Category"] == 200.0
        assert result_json["data"]["payer2"]["totalAmount"] == 200.0


def test_get_grouped_expenses_error():
    """
    Tests that get_grouped_expenses returns an ERROR on exception.
    """
    with patch("expense_log_mcp.tools.get_grouped_expenses.get_db") as mock_get_db:
        mock_get_db.side_effect = Exception("DB error")

        result = get_grouped_expenses(ledger_id="test-ledger")
        result_json = json.loads(result)

        assert result_json["success"] is False
        assert result_json["code"] == "ERROR"
        assert "DB error" in result_json["message"]
