import json
from unittest.mock import MagicMock, patch

from expense_log_mcp.tools.add_expense import add_expense


def test_add_expense_success():
    """
    Tests that an expense is added successfully.
    """
    mock_db = MagicMock()
    with patch("expense_log_mcp.tools.add_expense.get_db", return_value=iter([mock_db])):
        ledger_id = "test_ledger"
        category_id = "test_category"
        message_id = "test_message"
        description = "Test expense"
        amount = 100.0
        payer = "test_payer"

        result = add_expense(
            ledger_id=ledger_id,
            category_id=category_id,
            message_id=message_id,
            description=description,
            amount=amount,
            payer=payer,
        )

        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()

        result_json = json.loads(result)
        assert result_json["success"]
        assert result_json["code"] == "OK"
        assert result_json["message"] == "Expense added successfully."
        assert "expenseId" in result_json["data"]


def test_add_expense_db_error():
    """
    Tests that a database error is handled correctly.
    """
    with patch("expense_log_mcp.tools.add_expense.get_db", side_effect=Exception("DB error")):
        result = add_expense(
            ledger_id="test_ledger",
            category_id="test_category",
            message_id="test_message",
            description="Test expense",
            amount=100.0,
            payer="test_payer",
        )

        result_json = json.loads(result)
        assert not result_json["success"]
        assert result_json["code"] == "ERROR"
        assert result_json["message"] == "DB error"
