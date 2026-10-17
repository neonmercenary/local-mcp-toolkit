# Local Model MCP Toolkit (Day 3)

A secure, high-performance **Model Context Protocol (MCP)** server built in Python that exposes local system tools and data stores to AI assistants while enforcing strict security boundaries and input validation.

This project is part of a 7-day AI systems portfolio sprint, demonstrating production-ready agentic infrastructure without external API dependencies.

---

## 🏗️ System Architecture & Design

The Model Context Protocol (MCP) acts as an isolated translation and execution layer between an AI client (such as Cursor, Claude Desktop, or custom agent frameworks) and local host resources.

```
┌──────────────────────────┐
│  AI Client / Host LLM    │
└────────────┬─────────────┘
             │ (Stdio / JSON-RPC)
             ▼
┌──────────────────────────┐
│   MCP Server (FastMCP)   │
├──────────────────────────┤
│  • Input Validation      │
│  • Whitelist Security    │
│  • Parameterized SQL     │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│  Local SQLite Sandbox    │
└──────────────────────────┘
```

### Security & Boundaries
1. **Strict Whitelisting:** Reads from arbitrary SQL tables are blocked by default. Only pre-approved tables (`project_milestones`, `system_configs`, `notes`) can be queried.
2. **SQL Injection Defense:** All queries use parameterized inputs; raw dynamic SQL construction is prohibited.
3. **Bound Limits:** Record retrieval limits are hard-capped to prevent context memory overflow attacks.

---

## 🛠️ Stack & Tools

* **Language:** Python 3.10+
* **Framework:** [FastMCP](https://github.com/jlowin/fastmcp) / MCP SDK
* **Database:** SQLite 3
* **Package Manager:** [`uv`](https://github.com/astral-sh/uv)
* **Testing:** `pytest`

---

## 🚀 Quick Start

### 1. Prerequisites & Installation

Ensure you have `uv` installed. Clone the repository and install dependencies:

```bash
git clone https://github.com/your-username/local-mcp-kit.git
cd local-mcp-kit
uv sync
```

### 2. Running Tests

The server logic and security boundaries can be verified completely offline:

```bash
uv run pytest tests.py
```

Expected output:
```text
======================== test session starts ========================
collected 4 items

tests.py ....                                                [100%]

========================= 4 passed in 0.05s =========================
```

### 3. Starting the Server

Launch the MCP server in standard I/O mode:

```bash
uv run python main.py
```

---

## 🔌 Connecting to Claude Desktop / MCP Clients

Add the following configuration to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "local-toolkit": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/local-mcp-kit",
        "run",
        "python",
        "main.py"
      ]
    }
  }
}
```

---

## 🛠️ Exposed Tools Specification

### `search_notes(query: str)`
Searches the local developer notes repository using parameterized matching.
* **Input:** `query` (non-empty string)
* **Returns:** List of note titles, contents, and timestamps.

### `query_approved_records(table_name: str, limit: int = 5)`
Queries records from verified, non-sensitive database tables.
* **Input:** `table_name` (must match approved whitelist), `limit` (max 20)
* **Returns:** Structured JSON list of table rows.
* **Security Behavior:** Raises `ValueError` if an unapproved table is requested.