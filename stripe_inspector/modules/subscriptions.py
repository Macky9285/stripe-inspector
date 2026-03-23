"""Subscriptions module."""

from stripe_inspector.modules._base import stripe_get


def inspect(key: str) -> dict:
    data = stripe_get(key, "/v1/subscriptions", {"limit": 100})

    subs = []
    for s in data.get("data", []):
        subs.append({
            "id": s.get("id"),
            "customer": s.get("customer"),
            "status": s.get("status"),
            "currency": s.get("currency"),
            "created": s.get("created"),
            "current_period_start": s.get("current_period_start"),
            "current_period_end": s.get("current_period_end"),
            "cancel_at_period_end": s.get("cancel_at_period_end"),
        })

    return {
        "count": len(subs),
        "has_more": data.get("has_more", False),
        "subscriptions": subs,
    }
