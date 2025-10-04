# Expense Log MCP

A streamable http-based MCP server providing tools for logging expenses.

## ✨ Features

- Log a new expense to a ledger.
- Delete an expense record.
- Retrieve a list of all available expense categories.
- Retrieve and group expenses by payer and category.
- Retrieve an expense record.

## 🚀 Getting Started

### Prerequisites

- [Python >=3.11](https://www.python.org/)
- A [PostgreSQL](https://www.postgresql.org/) database

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/evanxd/expense-log-mcp-py.git
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    uv venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    uv pip install -e .
    ```

4.  **Configure environment variables:**
    - Create a `.env` file by copying `.env.example` and updating the values:
      ```bash
      cp .env.example .env
      ```
    - **Add server configuration to your `.env` file:**
      ```
      DATABASE_URL="postgresql://postgres:password@localhost:5432/postgres?schema=public"
      BEARER_TOKEN="YOUR_BEARER_TOKEN"
      PORT="8000"
      ```

5.  **Start the server:**
    ```bash
    uv run python -m expense_log_mcp.main
    ```
    This command starts the server, which will listen for incoming requests on the specified `PORT` (defaulting to 8000).

6.  **Configure your MCP host (e.g., Gemini CLI):**
    - Add the following configuration to your Gemini CLI settings (typically found in `~/.gemini-cli/config.json` or similar, depending on your OS):
    ```json
    "mcpServers": {
      "expense-log-mcp": {
        "url": "http://localhost:8000/mcp",
        "headers": {
          "Authorization": "Bearer YOUR_BEARER_TOKEN"
        }
      }
    }
    ```
    **Important:** Replace `YOUR_BEARER_TOKEN` with the actual `BEARER_TOKEN` you set in your `.env` file. This tells the Gemini CLI how to connect to and authenticate with your locally running Expense Log MCP server.

## 🛠️ Tools

The server exposes the following tools:

### `add_expense`

Adds a new expense record.

**Parameters:**

| Name          | Type   | Description                                        |
|---------------|--------|----------------------------------------------------|
| `ledger_id`    | string | The ID of the ledger to add the expense to.        |
| `category_id`  | string | The ID of the expense category.                    |
| `message_id`   | string | A unique ID for the message to prevent duplicates. |
| `description` | string | A description of the expense.                      |
| `amount`      | number | The amount of the expense.                         |
| `payer`       | string | The name of the person who paid.                   |

**Returns:**

A JSON string confirming the expense has been added, e.g.:
```json
{
  "success": true,
  "code": "OK",
  "message": "Expense added successfully.",
  "data": {
    "expense_id": "clx...456"
  }
}
```

### `delete_expense`

Deletes an expense record.

**Parameters:**

| Name        | Type   | Description                                         |
|-------------|--------|-----------------------------------------------------|
| `ledger_id`  | string | The ID of the ledger the expense belongs to.        |
| `message_id` | string | The unique message ID of the expense to be deleted. |

**Returns:**

A JSON string confirming the expense has been deleted, and including details of the deleted expense, e.g.:
```json
{
  "success": true,
  "code": "OK",
  "message": "Expense deleted successfully.",
  "data": {
    "id": "clx...123",
    "description": "Lunch",
    "amount": 15.75,
    "created_at": "Sun Sep 07 2025"
  }
}
```

### `get_expense`

Retrieves the details of a single expense.

**Parameters:**

| Name        | Type   | Description                                         |
|-------------|--------|-----------------------------------------------------|
| `ledger_id`  | string | The ID of the ledger the expense belongs to.        |
| `message_id` | string | The unique message ID of the expense to be deleted. |

**Returns:**

A JSON string confirming the expense has been retrieved, and including details of the expense, e.g.:
```json
{
  "success": true,
  "code": "OK",
  "message": "Expense retrieved successfully.",
  "data": {
    "id": "clx...123",
    "description": "Lunch",
    "amount": 110,
    "payer": "payer1",
    "created_at": "2025-09-07T00:00:00.000Z",
    "updated_at": "2025-09-07T00:00:00.000Z"
  }
}
```

### `get_expense_categories`

Retrieves the list of all expense categories.

**Parameters:**

None.

**Returns:**

A JSON string containing the list of expense categories, e.g.:
```json
{
  "success": true,
  "code": "OK",
  "message": "Expense categories retrieved successfully.",
  "data": [
    {
      "expense_category_id": "clx...1",
      "expense_category_name": "Transportation"
    },
    {
      "expense_category_id": "clx...2",
      "expense_category_name": "Utilities"
    }
  ]
}
```

### `get_grouped_expenses`

Retrieves and groups expenses by payer and then by category name, returning the total amount for each category,
with optional filters for category IDs, payer name, and a date range.
The `start_date` and `end_date` should be ISO 8601 strings, always in UTC.
The timezone for these dates can be adjusted using the `timezone_offset_hours`
parameter (default: 8), which is an integer representing the UTC offset in hours.

**Parameters:**

| Name                  | Type     | Description                                                                                                                              |
|-----------------------|----------|------------------------------------------------------------------------------------------------------------------------------------------|
| `ledger_id`            | string   | The ID of the ledger to retrieve expenses from.                                                                                          |
| `category_ids`         | string[] | Optional. An array of category IDs to filter by.                                                                                         |
| `payer_name`           | string   | Optional. The name of the payer to filter by.                                                                                            |
| `start_date`           | string   | Optional. The start date for filtering expenses (ISO 8601 format, e.g., "2025-01-01T00:00:00Z").                                          |
| `end_date`             | string   | Optional. The end date for filtering expenses (ISO 8601 format, e.g., "2025-12-31T23:59:59Z").                                            |
| `timezone_offset_hours` | number   | Optional. An integer representing the UTC offset in hours to adjust the timezone for `start_date` and `end_date` (default: 8).             |

**Returns:**

A JSON string containing the grouped expenses, e.g.:
```json
{
  "success": true,
  "code": "OK",
  "message": "Grouped expenses retrieved successfully.",
  "data": {
    "Payer1": {
      "expense_categories": {
        "Entertainment": 100,
        "Transportation": 50
      },
      "total_amount": 150
    },
    "Payer2": {
      "expense_categories": {
        "Dining/Snacks": 75
      },
      "total_amount": 75
    }
  }
}
```

## 🗄️ Database Schema

This project uses Prisma to manage the database schema. The schema is defined in `prisma/schema.prisma` and includes the following models:

- `Ledger`: Represents a collection of expenses.
- `ExpenseCategory`: Represents a category for an expense.
- `Expense`: Represents a single expense record. A unique constraint is added on `ledger_id` and `message_id` to prevent duplicate expenses.

All models include `created_at` and `updated_at` timestamps. IDs are generated using `cuid()`.

## 🙌 Contributing

Contributions are welcome! Please feel free to submit a pull request.

## 📄 License

This project is licensed under the [MIT License](LICENSE).
