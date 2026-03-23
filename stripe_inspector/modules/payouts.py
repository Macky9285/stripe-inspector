"""Payouts module."""

from stripe_inspector.modules._base import stripe_get


def inspect(key: str) -> dict:
    data = stripe_get(key, "/v1/payouts", {"limit": 100})

    payouts = []
    for p in data.get("data", []):
        payouts.append({
            "id": p.get("id"),
            "amount": (p.get("amount", 0) or 0) / 100,
            "currency": p.get("currency"),
            "status": p.get("status"),
            "method": p.get("method"),
            "type": p.get("type"),
            "arrival_date": p.get("arrival_date"),
            "created": p.get("created"),
            "destination": p.get("destination"),
            "description": p.get("description"),
        })

    return {
        "count": len(payouts),
        "has_more": data.get("has_more", False),
        "payouts": payouts,
    }
