from decimal import Decimal

from payments.gateway_refund import build_idempotency_key, refund_via_gateway


def test_refund_returns_decimal_and_key():
    result = refund_via_gateway("ch_9", "10.05", "op-17")
    assert result["amount"] == Decimal("10.05")
    assert result["idempotency_key"] == "refund:op-17"


def test_idempotency_key_is_stable_for_operation():
    assert build_idempotency_key("op-17") == build_idempotency_key("op-17")
