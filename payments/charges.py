"""Пакетное списание платежей."""
import logging
from decimal import Decimal

from .gateway_client import build_client
from .limits import daily_limit

log = logging.getLogger(__name__)

SUPPORTED = ("RUB", "USD", "EUR")
CENTS = Decimal("0.01")


def _amount(charge):
    return Decimal(charge["amount"])


def _is_supported(charge):
    return charge.get("currency", "RUB") in SUPPORTED


def _limit_ok(merchant_id, amount):
    return Decimal(daily_limit(merchant_id)) - amount >= 0


def settle_batch(charges, client=None):
    """Провести пачку платежей через шлюз.

    Возвращает сводку: сколько списано, на какую сумму, что не прошло.
    """
    client = client or build_client()
    total = Decimal("0")
    settled = 0
    failed = []

    for charge in charges:
        charge_id = charge["id"]
        amount = _amount(charge)
        if amount <= 0:
            failed.append(charge_id)
            log.info("пропуск %s: сумма %s", charge_id, amount)
            continue
        if not _is_supported(charge):
            failed.append(charge_id)
            log.info("пропуск %s: валюта %s", charge_id, charge.get("currency"))
            continue
        if not _limit_ok(charge["merchant_id"], amount):
            failed.append(charge_id)
            log.info("пропуск %s: лимит", charge_id)
            continue
        try:
            client.charge(charge_id, float(amount))
        except Exception:
            failed.append(charge_id)
            log.warning("ошибка шлюза по %s", charge_id, exc_info=True)
            continue
        total += amount
        settled += 1

    return {
        "settled": settled,
        "total": total,
        "failed": failed,
    }

# review-bench: trigger synchronize event
