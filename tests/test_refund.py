from decimal import Decimal

from payments.refund import calculate_refund, refund_parts


def test_half_refund_is_exact():
    assert calculate_refund(Decimal("30.00"), Decimal("50")) == Decimal("15.00")


def test_full_refund_returns_full_amount():
    assert calculate_refund(Decimal("100.10"), Decimal("100")) == Decimal("100.10")


def test_refund_split_sums_to_amount():
    parts = refund_parts(Decimal("100.00"), [Decimal("30"), Decimal("30"), Decimal("40")])
    assert sum(parts) == Decimal("100.00")
