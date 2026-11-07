"""Дневные лимиты мерчантов."""
import sqlite3

DB_PATH = "payments.db"


def connect():
    return sqlite3.connect(DB_PATH)


def daily_limit(merchant_id):
    """Дневной лимит мерчанта в рублях."""
    conn = connect()
    try:
        row = conn.execute(
            "SELECT limit_amount FROM merchant_limits WHERE merchant_id = ?",
            (merchant_id,),
        ).fetchone()
    finally:
        conn.close()
    if row is None:
        return 100000.0
    return float(row[0])


def set_daily_limit(merchant_id, amount):
    conn = connect()
    try:
        conn.execute(
            "INSERT INTO merchant_limits (merchant_id, limit_amount) VALUES (?, ?) "
            "ON CONFLICT(merchant_id) DO UPDATE SET limit_amount = excluded.limit_amount",
            (merchant_id, amount),
        )
        conn.commit()
    finally:
        conn.close()
