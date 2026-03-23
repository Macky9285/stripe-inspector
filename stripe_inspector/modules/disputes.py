"""Disputes module."""

from stripe_inspector.modules._base import stripe_get


def inspect(key: str) -> dict:
    data = stripe_get(key, "/v1/disputes", {"limit": 100})

    disputes = []
    for d in data.get("data", []):
        disputes.append({
            "id": d.get("id"),
            "amount": (d.get("amount", 0) or 0) / 100,
            "currency": d.get("currency"),
            "status": d.get("status"),
            "reason": d.get("reason"),
            "charge": d.get("charge"),
            "created": d.get("created"),
            "is_charge_refundable": d.get("is_charge_refundable"),
        })

    return {
        "count": len(disputes),
        "has_more": data.get("has_more", False),
        "disputes": disputes,
    }
