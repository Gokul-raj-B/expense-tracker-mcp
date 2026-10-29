
import sqlite3
from datetime import date
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Expense Tracker MCP")

DB_NAME = "expenses.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_table():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount > 0),
                category TEXT NOT NULL,
                expense_date TEXT NOT NULL
            )
        """)


@mcp.tool()
def add_expense(title: str, amount: float, category: str) -> str:
    """Save a new expense in the SQLite database."""
    if not title.strip():
        raise ValueError("Title cannot be empty.")

    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")

    if not category.strip():
        raise ValueError("Category cannot be empty.")

    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO expenses (title, amount, category, expense_date)
            VALUES (?, ?, ?, ?)
            """,
            (title, amount, category, date.today().isoformat()),
        )
        expense_id = cursor.lastrowid

    return f"Expense #{expense_id} saved successfully."


@mcp.tool()
def monthly_total(month: str) -> str:
    """Calculate total expenses for a month in YYYY-MM format."""
    try:
        parsed_month = date.fromisoformat(month + "-01")
        if parsed_month.strftime("%Y-%m") != month:
            raise ValueError
    except ValueError:
        raise ValueError("Month must use YYYY-MM format, for example 2026-10.")

    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT COALESCE(SUM(amount), 0)
            FROM expenses
            WHERE substr(expense_date, 1, 7) = ?
            """,
            (month,),
        ).fetchone()

    return f"Total expenses for {month}: Rs.{row[0]:.2f}"


@mcp.tool()
def top_categories(month: str) -> dict:
    """Show spending totals grouped by category for a month (YYYY-MM)."""
    try:
        parsed_month = date.fromisoformat(month + "-01")
        if parsed_month.strftime("%Y-%m") != month:
            raise ValueError
    except ValueError:
        raise ValueError("Month must use YYYY-MM format, for example 2026-10.")

    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT category, SUM(amount) AS total
            FROM expenses
            WHERE substr(expense_date, 1, 7) = ?
            GROUP BY category
            ORDER BY total DESC
            """,
            (month,),
        ).fetchall()

    return {category: round(total, 2) for category, total in rows}


create_table()

@mcp.resource("expenses://monthly")
def monthly_expenses_resource() -> str:
    """Return all expenses recorded in the current month."""
    month = date.today().strftime("%Y-%m")

    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT title, amount, category, expense_date
            FROM expenses
            WHERE substr(expense_date, 1, 7) = ?
            ORDER BY expense_date DESC
            """,
            (month,),
        ).fetchall()

    if not rows:
        return "No expenses recorded this month."

    return "\n".join(
        f"{title}: Rs.{amount:.2f}, {category}, {expense_date}"
        for title, amount, category, expense_date in rows
    )


@mcp.prompt()
def budget_summary(month: str) -> str:
    """Create a prompt for summarizing expenses for a given month."""
    return (
        f"Summarize my expenses for {month}. "
        "Use the available expense tools or resource to identify "
        "total spending, highest-spending categories, and possible savings."
    )

if __name__ == "__main__":
    mcp.run()
