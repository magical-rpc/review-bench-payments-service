from payments import charges


class FakeClient:
    def __init__(self, fail_ids=()):
        self.calls = []
        self.fail_ids = set(fail_ids)

    def charge(self, charge_id, amount):
        if charge_id in self.fail_ids:
            raise RuntimeError("gateway down")
        self.calls.append((charge_id, amount))
        return {"status": "ok"}


def test_settles_valid_charges(monkeypatch):
    monkeypatch.setattr(charges, "daily_limit", lambda merchant_id: 10000.0)
    client = FakeClient()
    result = charges.settle_batch(
        [
            {"id": "c1", "amount": "100.00", "merchant_id": "m1"},
            {"id": "c2", "amount": "250.50", "merchant_id": "m1"},
        ],
        client=client,
    )
    assert result["settled"] == 2
    assert result["total"] == 350.5
    assert client.calls == [("c1", 100.0), ("c2", 250.5)]


def test_rejects_unknown_currency(monkeypatch):
    monkeypatch.setattr(charges, "daily_limit", lambda merchant_id: 10000.0)
    client = FakeClient()
    result = charges.settle_batch(
        [{"id": "c1", "amount": "100.00", "currency": "GBP", "merchant_id": "m1"}],
        client=client,
    )
    assert result["failed"] == ["c1"]
    assert client.calls == []


def test_rejects_over_limit(monkeypatch):
    monkeypatch.setattr(charges, "daily_limit", lambda merchant_id: 100.0)
    client = FakeClient()
    result = charges.settle_batch(
        [{"id": "c1", "amount": "150.00", "merchant_id": "m1"}], client=client
    )
    assert result["failed"] == ["c1"]


def test_gateway_error_does_not_break_batch(monkeypatch):
    monkeypatch.setattr(charges, "daily_limit", lambda merchant_id: 10000.0)
    client = FakeClient(fail_ids={"c2"})
    result = charges.settle_batch(
        [
            {"id": "c1", "amount": "10.00", "merchant_id": "m1"},
            {"id": "c2", "amount": "10.00", "merchant_id": "m1"},
        ],
        client=client,
    )
    assert result["settled"] == 1
    assert result["failed"] == ["c2"]

