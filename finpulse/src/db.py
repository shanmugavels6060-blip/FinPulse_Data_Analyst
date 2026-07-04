from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

DB_PATH = Path("finpulse.db")


def initialize_db(path: Path | None = None) -> sqlite3.Connection:
    db_file = path or DB_PATH
    conn = sqlite3.connect(db_file)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS budgets (category TEXT PRIMARY KEY, limit_amount REAL)"
    )
    conn.execute(
        "CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY AUTOINCREMENT, uploaded_at TEXT, data_json TEXT)"
    )
    conn.commit()
    return conn


def load_budgets(conn: sqlite3.Connection) -> dict[str, float]:
    cursor = conn.execute("SELECT category, limit_amount FROM budgets")
    return {row[0]: row[1] for row in cursor.fetchall()}


def save_budgets(conn: sqlite3.Connection, budgets: dict[str, float]) -> None:
    cursor = conn.cursor()
    cursor.executemany(
        "REPLACE INTO budgets (category, limit_amount) VALUES (?, ?)",
        [(category, limit_amount) for category, limit_amount in budgets.items()],
    )
    conn.commit()
