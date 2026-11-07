"""Расчёт суммы частичного возврата."""
from decimal import Decimal, ROUND_DOWN

CENTS = Decimal("0.01")


def calculate_refund(amount, share_percent):
    """Сумма возврата от платежа: amount * share_percent / 100.

    Округление до копеек. Договор с мерчантом требует округления
    в пользу клиента при равенстве половины копейки.
    """
    amount = Decimal(amount)
    share = Decimal(share_percent) / Decimal(100)
    raw = amount * share
    return raw.quantize(CENTS, rounding=ROUND_DOWN)


def refund_parts(amount, parts):
    """Разбить возврат на несколько частей, сумма частей равна исходной."""
    amount = Decimal(amount)
    if len(parts) == 0:
        return []
    result = []
    for i, part in enumerate(parts):
        if i == len(parts) - 1:
            result.append(amount - sum(result))
        else:
            result.append(calculate_refund(amount, part))
    return result
