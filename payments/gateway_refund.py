"""Возврат через GatewayClientV2 с ключом идемпотентности."""
from decimal import Decimal

from billing_sdk import GatewayClientV2

OPERATION_PREFIX = "refund:"


def build_idempotency_key(operation_id):
    """Ключ строится из номера операции, а не из времени вызова (ADR-0002)."""
    return "%s%s" % (OPERATION_PREFIX, operation_id)


def refund_via_gateway(charge_id, amount, operation_id, client=None):
    """Вернуть сумму по операции. Повтор с тем же operation_id не создаёт второй возврат."""
    client = client or GatewayClientV2()
    key = build_idempotency_key(operation_id)
    result = client.refund(charge_id, Decimal(amount), idempotency_key=key)
    return {
        "charge_id": result.charge_id,
        "amount": result.amount,
        "idempotency_key": result.idempotency_key,
    }
