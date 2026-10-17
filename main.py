import sqlite3
from typing import Any
from fastmcp import FastMCP

mcp = FastMCP("Local Secure Toolkit")

DB_PATH = "local_sandbox.db"
APPROVED_TABLES = {"project_milestones", "system_configs", "notes"}


def get_db_connection():
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  return conn


@mcp.tool()
def search_notes(query: str) -> list[dict[str, Any]]:
  """Search local developer notes for specific keywords or topics."""
  if not query or len(query.strip()) == 0:
    return [{"error": "Query string cannot be empty."}]

  conn = get_db_connection()
  cursor = conn.cursor()
  
  cursor.execute(
      "SELECT title, content, updated_at FROM notes WHERE content LIKE ? OR"
      " title LIKE ?",
      (f"%{query}%", f"%{query}%"),
  )
  rows = cursor.fetchall()
  conn.close()

  return [dict(row) for row in rows]


@mcp.tool()
def query_approved_records(table_name: str, limit: int = 5) -> list[dict[str, Any]]:
  """Retrieve records from an approved database table. Unauthorized tables are strictly blocked."""
  
  # 1. Enforce strict whitelist security check
  if table_name not in APPROVED_TABLES:
    raise ValueError(
        f"Unauthorized access attempt: Table '{table_name}' is not in the"
        " approved registry."
    )

  # Enforce reasonable bounds on limit
  safe_limit = max(1, min(limit, 20))

  conn = get_db_connection()
  cursor = conn.cursor()

  # Table name is checked against whitelist, safe_limit is an integer
  cursor.execute(f"SELECT * FROM {table_name} LIMIT ?", (safe_limit,))
  rows = cursor.fetchall()
  conn.close()

  return [dict(row) for row in rows]


if __name__ == "__main__":
  mcp.run()