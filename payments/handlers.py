"""HTTP-обработчики (упрощённо, без веб-фреймворка)."""
import sqlite3
from decimal import Decimal

from .refund import calculate_refund


def refund_handler(payload, db_path="payments.db"):
    """Обработчик POST /refund: рассчитать возврат и записать в БД."""
    payment_id = payload["payment_id"]
    amount = Decimal(payload["amount"])
    share = payload.get("share_percent", 100)

    refund_amount = calculate_refund(amount, share)

    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            "INSERT INTO refunds (payment_id, amount) VALUES (?, ?)",
            (payment_id, str(refund_amount)),
        )
        conn.commit()
    finally:
        conn.close()

    return {"payment_id": payment_id, "refund": str(refund_amount)}


def payment_status_handler(payload, db_path="payments.db"):
    conn = sqlite3.connect(db_path)
    try:
        row = conn.execute(
            "SELECT status FROM payments WHERE payment_id = ?",
            (payload["payment_id"],),
        ).fetchone()
    finally:
        conn.close()
    if row is None:
        return {"payment_id": payload["payment_id"], "status": "unknown"}
    return {"payment_id": payload["payment_id"], "status": row[0]}
