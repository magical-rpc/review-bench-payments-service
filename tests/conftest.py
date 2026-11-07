import sqlite3

import pytest

from payments import limits

SCHEMA = """
CREATE TABLE IF NOT EXISTS merchant_limits (
    merchant_id TEXT PRIMARY KEY,
    limit_amount REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS payments (
    payment_id TEXT PRIMARY KEY,
    status TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS refunds (
    payment_id TEXT NOT NULL,
    amount TEXT NOT NULL
);
"""


@pytest.fixture
def db(tmp_path, monkeypatch):
    path = tmp_path / "payments.db"
    conn = sqlite3.connect(path)
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()
    monkeypatch.setattr(limits, "DB_PATH", str(path))
    return str(path)
