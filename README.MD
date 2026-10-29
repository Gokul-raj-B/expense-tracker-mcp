# Expense Tracker MCP Server

## About the Project
This project is an Expense Tracker built using the Model Context Protocol (MCP) and Python. It stores personal expenses in an SQLite database and provides tools to calculate spending.

## Features
- Add a new expense
- Calculate monthly expenses
- View spending totals by category
- Read expenses for the current month through an MCP resource
- Generate a budget summary prompt
- Validate expense inputs

## Technologies Used
- Python
- MCP (Model Context Protocol)
- SQLite
- MCP Inspector

## Available Tools

### 1. `add_expense`
Adds an expense with a title, amount, and category.

### 2. `monthly_total`
Calculates the total expenses for a month in `YYYY-MM` format.

### 3. `top_categories`
Returns expense totals grouped by category for a selected month.

## Resource
- `expenses://monthly` — returns expenses recorded in the current month.

## Prompt
- `budget_summary` — creates instructions for summarizing monthly expenses and identifying possible savings.

## Project Structure
```text
mcp-intern/
├── server.py
├── README.md
├── .gitignore
└── .venv/
```

The `.venv/` directory and SQLite database are excluded from Git using `.gitignore`.

## Run the Project

1. Create and activate a Python virtual environment.
2. Install the compatible MCP SDK version:

   `python -m pip install "mcp<2"`

3. Run the server:

   `python server.py`

4. Connect the server to MCP Inspector using the Python executable from your virtual environment and the path to `server.py`.

## Testing
The following have been tested using MCP Inspector:
- Adding an expense
- Calculating monthly expenses
- Viewing category totals
- Reading the monthly expenses resource
- Generating the budget summary prompt
- Rejecting invalid expense inputs

## Future Improvements
- Add expense editing and deletion
- Support budgets and spending limits
- Add automated unit tests
- Connect the server to an AI application
