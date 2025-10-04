import json
from unittest.mock import MagicMock, patch
from datetime import datetime
from expense_log_mcp.models import Expense
from expense_log_mcp.tools.get_expense import get_expense


def test_get_expense_success():
    """
    Tests that get_expense returns expense details successfully.
    """
    mock_expense = Expense(
        id=1,
        ledgerId="test-ledger",
        messageId="test-message",
        description="Test Expense",
        amount=100.0,
        payer="test-payer",
        createdAt=datetime.now(),
        updatedAt=datetime.now(),
    )

    with patch("expense_log_mcp.tools.get_expense.get_db") as mock_get_db:
        mock_db = MagicMock()
        mock_db.query.return_value.filter_by.return_value.first.return_value = mock_expense
        mock_get_db.return_value = iter([mock_db])

        result = get_expense(ledger_id="test-ledger", message_id="test-message")
        result_json = json.loads(result)

        assert result_json["success"] is True
        assert result_json["code"] == "OK"
        assert result_json["data"]["id"] == mock_expense.id


def test_get_expense_not_found():
    """
    Tests that get_expense returns a NOT_FOUND error when the expense does not exist.
    """
    with patch("expense_log_mcp.tools.get_expense.get_db") as mock_get_db:
        mock_db = MagicMock()
        mock_db.query.return_value.filter_by.return_value.first.return_value = None
        mock_get_db.return_value = iter([mock_db])

        result = get_expense(ledger_id="test-ledger", message_id="test-message")
        result_json = json.loads(result)

        assert result_json["success"] is False
        assert result_json["code"] == "NOT_FOUND"


def test_get_expense_error():
    """
    Tests that get_expense returns an ERROR on exception.
    """
    with patch("expense_log_mcp.tools.get_expense.get_db") as mock_get_db:
        mock_get_db.side_effect = Exception("DB error")

        result = get_expense(ledger_id="test-ledger", message_id="test-message")
        result_json = json.loads(result)

        assert result_json["success"] is False
        assert result_json["code"] == "ERROR"
        assert "DB error" in result_json["message"]
