from decimal import Decimal

from payments.handlers import payment_status_handler, refund_handler


def test_refund_handler_writes_refund(db):
    result = refund_handler({"payment_id": "p1", "amount": "100.00", "share_percent": 50}, db_path=db)
    assert result["refund"] == "50.00"


def test_payment_status_unknown(db):
    assert payment_status_handler({"payment_id": "nope"}, db_path=db)["status"] == "unknown"
