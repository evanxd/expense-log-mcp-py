import json
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone
from expense_log_mcp.models import Expense, ExpenseCategory
from expense_log_mcp.tools.get_grouped_expenses import get_grouped_expenses


mock_category1 = ExpenseCategory(id=1, name="Category 1")
mock_category2 = ExpenseCategory(id=2, name="Category 2")
MOCK_EXPENSES = [
    Expense(
        id=1,
        ledgerId="test-ledger",
        description="E1",
        amount=100.0,
        payer="payer1",
        categoryId=1,
        category=mock_category1,
        createdAt=datetime(2025, 1, 10, tzinfo=timezone.utc),
        updatedAt=datetime(2025, 1, 10, tzinfo=timezone.utc),
    ),
    Expense(
        id=2,
        ledgerId="test-ledger",
        description="E2",
        amount=200.0,
        payer="payer2",
        categoryId=2,
        category=mock_category2,
        createdAt=datetime(2025, 1, 11, tzinfo=timezone.utc),
        updatedAt=datetime(2025, 1, 11, tzinfo=timezone.utc),
    ),
    Expense(
        id=3,
        ledgerId="test-ledger",
        description="E3",
        amount=50.0,
        payer="payer1",
        categoryId=2,
        category=mock_category2,
        createdAt=datetime(2025, 1, 12, tzinfo=timezone.utc),
        updatedAt=datetime(2025, 1, 12, tzinfo=timezone.utc),
    ),
]


@pytest.fixture
def mock_db_session():
    """Fixture to mock the database session."""
    with patch("expense_log_mcp.tools.get_grouped_expenses.get_db") as mock_get_db:
        mock_db = MagicMock()
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_get_db.return_value = iter([mock_db])
        yield mock_db


def test_get_grouped_expenses_success(mock_db_session):
    """
    Tests that get_grouped_expenses returns grouped expenses successfully.
    """
    mock_db_session.query.return_value.filter.return_value.order_by.return_value.all.return_value = (  # noqa: E501
        MOCK_EXPENSES
    )

    result = get_grouped_expenses(ledger_id="test-ledger")
    result_json = json.loads(result)

    assert result_json["success"] is True
    assert result_json["code"] == "OK"
    assert "payer1" in result_json["data"]
    assert "payer2" in result_json["data"]
    assert result_json["data"]["payer1"]["expenseCategories"]["Category 1"] == 100.0
    assert result_json["data"]["payer1"]["expenseCategories"]["Category 2"] == 50.0
    assert result_json["data"]["payer1"]["totalAmount"] == 150.0
    assert result_json["data"]["payer2"]["expenseCategories"]["Category 2"] == 200.0
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


@pytest.mark.parametrize(
    "filter_kwargs, mock_return_expenses, expected_data",
    [
        (
            {"category_ids": ["1"]},
            [MOCK_EXPENSES[0]],
            {
                "payer1": {
                    "expenseCategories": {"Category 1": 100.0},
                    "totalAmount": 100.0,
                }
            },
        ),
        (
            {"payer_name": "payer1"},
            [MOCK_EXPENSES[0], MOCK_EXPENSES[2]],
            {
                "payer1": {
                    "expenseCategories": {"Category 1": 100.0, "Category 2": 50.0},
                    "totalAmount": 150.0,
                }
            },
        ),
        (
            {"start_date": "2025-01-11"},
            [MOCK_EXPENSES[1], MOCK_EXPENSES[2]],
            {
                "payer1": {
                    "expenseCategories": {"Category 2": 50.0},
                    "totalAmount": 50.0,
                },
                "payer2": {
                    "expenseCategories": {"Category 2": 200.0},
                    "totalAmount": 200.0,
                },
            },
        ),
        (
            {"end_date": "2025-01-11"},
            [MOCK_EXPENSES[0], MOCK_EXPENSES[1]],
            {
                "payer1": {
                    "expenseCategories": {"Category 1": 100.0},
                    "totalAmount": 100.0,
                },
                "payer2": {
                    "expenseCategories": {"Category 2": 200.0},
                    "totalAmount": 200.0,
                },
            },
        ),
    ],
)
def test_get_grouped_expenses_with_filters(
    mock_db_session, filter_kwargs, mock_return_expenses, expected_data
):
    """
    Tests that get_grouped_expenses filters correctly based on provided arguments.
    """
    mock_db_session.query.return_value.filter.return_value.order_by.return_value.all.return_value = (  # noqa: E501
        mock_return_expenses
    )

    result = get_grouped_expenses(ledger_id="test-ledger", **filter_kwargs)
    result_json = json.loads(result)

    assert result_json["success"] is True
    assert result_json["data"] == expected_data
