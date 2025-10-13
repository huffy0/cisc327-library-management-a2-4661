# tests/conftest.py
import sys
import pathlib
import sqlite3
import pytest

HERE = pathlib.Path(__file__).resolve()
PROJECT_ROOT = None
for up in [HERE.parents[1], HERE.parents[2], HERE.parents[3], HERE.parents[4]]:
    if (up / "app.py").exists():
        PROJECT_ROOT = up
        if str(up) not in sys.path:
            sys.path.insert(0, str(up))
        break
if PROJECT_ROOT is None:
    raise RuntimeError("Could not find app.py by walking up from tests")

import app as app_module          # noqa: E402
import database as db_module      # noqa: E402

@pytest.fixture(autouse=True)
def app_and_db(tmp_path, monkeypatch):
    """Per test, use a temp sqlite file and a Flask app context."""
    db_file = tmp_path / "test.sqlite"

    orig_connect = sqlite3.connect

    def connect_to_test_db(*args, **kwargs):
        conn = orig_connect(str(db_file))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    try:
        monkeypatch.setattr(db_module.sqlite3, "connect", connect_to_test_db, raising=False)
    except Exception:
        pass

    for name in ["get_db_connection", "get_connection", "connect_db", "open_connection"]:
        if hasattr(db_module, name):
            monkeypatch.setattr(db_module, name, connect_to_test_db, raising=False)

    if hasattr(db_module, "init_db"):
        db_module.init_db()
    else:
        conn = connect_to_test_db()
        conn.executescript("""
            PRAGMA foreign_keys = ON;
            CREATE TABLE IF NOT EXISTS books(
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT UNIQUE NOT NULL,
                total_copies INTEGER NOT NULL,
                available_copies INTEGER NOT NULL
            );
            CREATE TABLE IF NOT EXISTS borrow_records(
                id INTEGER PRIMARY KEY,
                patron_id TEXT NOT NULL,
                book_id INTEGER,
                borrow_date TEXT NOT NULL,
                due_date TEXT NOT NULL,
                return_date TEXT NULL,
                FOREIGN KEY(book_id) REFERENCES books(id)
            );
        """)
        conn.commit()
        conn.close()

    create_app = getattr(app_module, "create_app", None)
    assert create_app is not None, "create_app not found in app.py"
    flask_app = create_app()
    flask_app.config["TESTING"] = True
    ctx = flask_app.app_context()
    ctx.push()

    yield

    ctx.pop()
