# Expense Tracker MCP

A local Model Context Protocol (MCP) server for recording expenses and reviewing monthly spending. It uses SQLite for storage and exposes tools, a resource, and a prompt to MCP-compatible clients such as Codex.

## Features

- Save expenses with a title, amount, category, and the current date.
- Calculate total spending for a month.
- View spending totals grouped by category.
- Read expenses recorded during the current month.
- Create a prompt for summarizing spending and possible savings.
- Store expense data in a local SQLite database (`expenses.db`).

## MCP capabilities

### Tools

| Tool | Arguments | Description |
| --- | --- | --- |
| `add_expense` | `title: string`, `amount: number`, `category: string` | Saves an expense dated today. The title and category must not be blank, and the amount must be greater than zero. |
| `monthly_total` | `month: string` | Returns the expense total for a month in `YYYY-MM` format, such as `2026-10`. |
| `top_categories` | `month: string` | Returns spending totals grouped by category for a month in `YYYY-MM` format, ordered from highest to lowest total. |

### Resource

| URI | Description |
| --- | --- |
| `expenses://monthly` | Returns all expenses recorded in the current month, including each title, amount, category, and date. |

### Prompt

| Prompt | Argument | Description |
| --- | --- | --- |
| `budget_summary` | `month: string` | Builds a request to summarize the month's expenses, identify total spending and highest-spending categories, and suggest possible savings. |

## Requirements

- Python 3.11 or newer
- Node.js and npm (needed to launch MCP Inspector with `npx`)

The MCP SDK dependency is constrained to the 1.x line to match this server's `FastMCP` implementation.

## Install

Open PowerShell in the project directory:

```powershell
cd <path-to-project>
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install "mcp[cli]>=1.30,<2"
```

The server uses stdio transport by default. Run it directly with:

```powershell
.\.venv\Scripts\python.exe server.py
```

When run directly, it waits for an MCP client to connect over standard input and output.

## Run and inspect with MCP Inspector

From the project directory, start the Inspector and have it launch the server:

```powershell
npx -y @modelcontextprotocol/inspector .\.venv\Scripts\python.exe server.py
```

Open the URL printed by Inspector. Use its **Tools** tab to list and call the three tools, its **Resources** tab to read `expenses://monthly`, and its **Prompts** tab to try `budget_summary` with a month such as `2026-10`.

Calling `add_expense` writes a new row to `expenses.db`. Use test data with that persistent change in mind. `monthly_total` and `top_categories` can be used to inspect totals for a month.

See the [MCP Inspector guide](https://modelcontextprotocol.io/docs/tools/inspector) for more information.

## Configure in Codex on Windows

Codex reads MCP server entries from `%USERPROFILE%\.codex\config.toml`. You can edit that file directly or register a local stdio server from PowerShell:

```powershell
codex mcp add expense-tracker -- "<absolute-path-to-project>\.venv\Scripts\python.exe" "<absolute-path-to-project>\server.py"
```

To configure it manually, add this entry to `config.toml`. Replace the placeholder paths with the actual project location:

```toml
[mcp_servers.expense-tracker]
command = "C:\\Path\\To\\expense-tracker-mcp\\.venv\\Scripts\\python.exe"
args = ["C:\\Path\\To\\expense-tracker-mcp\\server.py"]
cwd = "C:\\Path\\To\\expense-tracker-mcp"
```

The `cwd` keeps the server's relative `expenses.db` path anchored to the project directory. After saving the configuration, restart or refresh Codex and check the MCP server list. The Codex CLI can list configured servers with:

```powershell
codex mcp list
```

See the [Codex MCP documentation](https://learn.chatgpt.com/docs/developer-commands) for configuration and CLI commands.

## Testing and validation

- Reviewed `server.py` to document its tools, resource, prompt, validation rules, and default stdio transport.
- Confirmed the local environment reports Python 3.14.7 and MCP SDK 1.30.0.
- In the connected MCP environment, `monthly_total` was called for `2026-10` and returned `Rs.200.00`.
- MCP Inspector was not run as part of this README review. Follow the Inspector instructions above to check the tools, resource, and prompt interactively.

## Data and implementation notes

- The database file is named `expenses.db` and is created in the server's working directory if needed.
- New expenses use the machine's current date.
- Monthly arguments must use `YYYY-MM` format, for example `2026-10`.
- The server creates the `expenses` table at startup if it does not already exist.
