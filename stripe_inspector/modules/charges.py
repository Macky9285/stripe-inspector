"""Charges module."""

from stripe_inspector.modules._base import stripe_get


def inspect(key: str) -> dict:
    data = stripe_get(key, "/v1/charges", {"limit": 100})

    charges = []
    total_amount = 0
    currencies = set()

    for c in data.get("data", []):
        amount = (c.get("amount", 0) or 0) / 100
        currency = c.get("currency", "")
        total_amount += amount
        currencies.add(currency)

        billing = c.get("billing_details", {})
        card = (c.get("payment_method_details", {}).get("card") or {})

        charges.append({
            "id": c.get("id"),
            "amount": amount,
            "currency": currency,
            "status": c.get("status"),
            "paid": c.get("paid"),
            "refunded": c.get("refunded"),
            "created": c.get("created"),
            "description": c.get("description"),
            "payer_name": billing.get("name"),
            "payer_email": billing.get("email"),
            "card_brand": card.get("brand"),
            "card_last4": card.get("last4"),
            "card_country": card.get("country"),
            "receipt_email": c.get("receipt_email"),
            "statement_descriptor": c.get("calculated_statement_descriptor"),
        })

    return {
        "count": len(charges),
        "has_more": data.get("has_more", False),
        "total_amount": total_amount,
        "currencies": list(currencies),
        "charges": charges,
    }
