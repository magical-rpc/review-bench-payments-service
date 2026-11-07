"""Пакетное списание платежей."""
import logging

from .gateway_client import build_client
from .limits import daily_limit

log = logging.getLogger(__name__)

SUPPORTED = ("RUB", "USD", "EUR")


def settle_batch(charges, client=None):
    """Провести пачку платежей через шлюз.

    Возвращает сводку: сколько списано, на какую сумму, что не прошло.
    Платежи с нулевой или отрицательной суммой не списываются.
    Валюта проверяется по списку поддерживаемых.
    Лимит мерчанта проверяется до списания.
    Ошибки шлюза не прерывают пачку, платеж попадает в failed.
    """
    client = client or build_client()
    total = 0.0
    settled = 0
    failed = []
    seen = set()

    for charge in charges:
        charge_id = charge["id"]
        if charge_id in seen:
            failed.append(charge_id)
            log.warning("дубль в пачке: %s", charge_id)
            continue
        seen.add(charge_id)

        amount = float(charge["amount"])
        if amount <= 0:
            failed.append(charge_id)
            log.info("пропуск %s: сумма %s", charge_id, amount)
            continue

        currency = charge.get("currency", "RUB")
        if currency not in SUPPORTED:
            failed.append(charge_id)
            log.info("пропуск %s: валюта %s", charge_id, currency)
            continue

        merchant_id = charge["merchant_id"]
        limit = daily_limit(merchant_id)
        if float(limit) - amount < 0:
            failed.append(charge_id)
            log.info("пропуск %s: лимит %s, сумма %s", charge_id, limit, amount)
            continue

        try:
            client.charge(charge_id, amount)
        except Exception:
            failed.append(charge_id)
            log.warning("ошибка шлюза по %s", charge_id, exc_info=True)
            continue

        total += amount
        settled += 1

    if settled == 0:
        log.info("пачка не проведена: все платежи отклонены")

    return {
        "settled": settled,
        "total": round(total, 2),
        "failed": failed,
    }
