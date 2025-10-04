import json
from unittest.mock import MagicMock, patch

from datetime import datetime
from expense_log_mcp.models import Expense
from expense_log_mcp.tools.delete_expense import delete_expense


def test_delete_expense_success():
    """
    Tests that an expense is deleted successfully.
    """
    mock_db = MagicMock()
    mock_expense = Expense(
        id=1,
        ledgerId="test_ledger",
        messageId="test_message",
        description="Test expense",
        amount=100.0,
        createdAt=datetime.now(),
    )
    mock_db.query.return_value.filter_by.return_value.first.return_value = mock_expense

    with patch("expense_log_mcp.tools.delete_expense.get_db", return_value=iter([mock_db])):
        result = delete_expense(ledger_id="test_ledger", message_id="test_message")

        mock_db.delete.assert_called_once_with(mock_expense)
        mock_db.commit.assert_called_once()

        result_json = json.loads(result)
        assert result_json["success"]
        assert result_json["code"] == "OK"
        assert result_json["message"] == "Expense deleted successfully."
        assert result_json["data"]["id"] == mock_expense.id


def test_delete_expense_not_found():
    """
    Tests that the correct message is returned when an expense is not found.
    """
    mock_db = MagicMock()
    mock_db.query.return_value.filter_by.return_value.first.return_value = None

    with patch("expense_log_mcp.tools.delete_expense.get_db", return_value=iter([mock_db])):
        result = delete_expense(ledger_id="test_ledger", message_id="test_message")

        mock_db.delete.assert_not_called()
        mock_db.commit.assert_not_called()

        result_json = json.loads(result)
        assert not result_json["success"]
        assert result_json["code"] == "NOT_FOUND"
        assert result_json["message"] == "Expense not found."


def test_delete_expense_db_error():
    """
    Tests that a database error is handled correctly.
    """
    with patch(
        "expense_log_mcp.tools.delete_expense.get_db",
        side_effect=Exception("DB error"),
    ):
        result = delete_expense(ledger_id="test_ledger", message_id="test_message")

        result_json = json.loads(result)
        assert not result_json["success"]
        assert result_json["code"] == "ERROR"
        assert result_json["message"] == "DB error"
