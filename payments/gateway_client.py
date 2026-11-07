"""Клиент платёжного шлюза из billing-sdk."""
from billing_sdk import GatewayClientV1


def build_client():
    """Боевой клиент шлюза."""
    return GatewayClientV1()
