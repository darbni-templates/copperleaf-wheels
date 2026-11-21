"""The SQLite database and its migrations.

The database is built from the .sql files in wheels/migrations/, in name order. Each file runs
ONCE per database: create_app runs the files that are new and writes their names in the table
applied_migrations. To change the database, add a NEW file with a higher number
(0010_promo_dates.sql, ...). Never edit a file that has already run: a database that has it
would never see the change.
"""

import sqlite3
from pathlib import Path

from flask import current_app

MIGRATIONS = Path(__file__).with_name("migrations")


def migrate(path):
    conn = sqlite3.connect(path)
    try:
        conn.execute("CREATE TABLE IF NOT EXISTS applied_migrations (name TEXT PRIMARY KEY)")
        done = {row[0] for row in conn.execute("SELECT name FROM applied_migrations")}
        for script in sorted(MIGRATIONS.glob("*.sql")):
            if script.name in done:
                continue
            conn.executescript(script.read_text(encoding="utf-8"))
            conn.execute("INSERT INTO applied_migrations (name) VALUES (?)", (script.name,))
            conn.commit()
    finally:
        conn.close()


def connect():
    """A connection to the app's database. Close it when you are done:

    conn = db.connect()
    try:
        ...
    finally:
        conn.close()
    """
    conn = sqlite3.connect(current_app.config["DATABASE"])
    conn.row_factory = sqlite3.Row  # rows work like dicts: row["daily_fils"]
    return conn
