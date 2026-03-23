"""Invoices module."""

from stripe_inspector.modules._base import stripe_get


def inspect(key: str) -> dict:
    data = stripe_get(key, "/v1/invoices", {"limit": 100})

    invoices = []
    for inv in data.get("data", []):
        invoices.append({
            "id": inv.get("id"),
            "customer": inv.get("customer"),
            "amount_due": (inv.get("amount_due", 0) or 0) / 100,
            "amount_paid": (inv.get("amount_paid", 0) or 0) / 100,
            "currency": inv.get("currency"),
            "status": inv.get("status"),
            "created": inv.get("created"),
            "hosted_invoice_url": inv.get("hosted_invoice_url"),
        })

    return {
        "count": len(invoices),
        "has_more": data.get("has_more", False),
        "invoices": invoices,
    }
