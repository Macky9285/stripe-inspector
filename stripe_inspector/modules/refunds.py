"""Refunds module."""

from stripe_inspector.modules._base import stripe_get


def inspect(key: str) -> dict:
    data = stripe_get(key, "/v1/refunds", {"limit": 100})

    refunds = []
    for r in data.get("data", []):
        refunds.append({
            "id": r.get("id"),
            "amount": (r.get("amount", 0) or 0) / 100,
            "currency": r.get("currency"),
            "status": r.get("status"),
            "reason": r.get("reason"),
            "charge": r.get("charge"),
            "created": r.get("created"),
        })

    return {
        "count": len(refunds),
        "has_more": data.get("has_more", False),
        "refunds": refunds,
    }
