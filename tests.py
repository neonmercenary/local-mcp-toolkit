import sqlite3
import pytest
from main import query_approved_records, search_notes


@pytest.fixture(autouse=True)
def setup_test_db():
    """Set up and tear down a test database with mock records for each test."""
    conn = sqlite3.connect("local_sandbox.db")
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute("CREATE TABLE IF NOT EXISTS project_milestones (id INTEGER PRIMARY KEY, milestone TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, title TEXT, content TEXT, updated_at TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS secret_passwords (id INTEGER PRIMARY KEY, password TEXT)")
    
    # Insert mock data
    cursor.execute("INSERT OR IGNORE INTO project_milestones (id, milestone) VALUES (1, 'Day 3 MCP Server Built')")
    cursor.execute("INSERT OR IGNORE INTO notes (id, title, content, updated_at) VALUES (1, 'MCP Guide', 'Model Context Protocol secures local tools.', '2026-03-30')")
    cursor.execute("INSERT OR IGNORE INTO secret_passwords (id, password) VALUES (1, 'super_secret_key')")
    
    conn.commit()
    conn.close()
    yield


def test_search_notes_empty_query():
    result = search_notes("")
    assert "error" in result[0]


def test_search_notes_success():
    result = search_notes("Protocol")
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["title"] == "MCP Guide"


def test_query_approved_table_success():
    records = query_approved_records("project_milestones", limit=1)
    assert isinstance(records, list)
    assert len(records) == 1
    assert records[0]["milestone"] == "Day 3 MCP Server Built"


def test_query_unauthorized_table_rejection():
    """Ensures the security boundary rejects unapproved table access."""
    with pytest.raises(ValueError, match="Unauthorized access attempt"):
        query_approved_records("secret_passwords", limit=1)