"""Тест из ветки QA: сумма пачки должна быть Decimal (C1)."""
from decimal import Decimal

from payments import charges


class Client:
    def charge(self, charge_id, amount):
        return {"status": "ok"}


def test_total_is_decimal(monkeypatch):
    monkeypatch.setattr(charges, "daily_limit", lambda merchant_id: 10000.0)
    result = charges.settle_batch(
        [
            {"id": "c1", "amount": "100.00", "merchant_id": "m1"},
            {"id": "c2", "amount": "250.50", "merchant_id": "m1"},
        ],
        client=Client(),
    )
    assert isinstance(result["total"], Decimal)
    assert result["total"] == Decimal("350.50")
