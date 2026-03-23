"""Coupons module."""

from stripe_inspector.modules._base import stripe_get


def inspect(key: str) -> dict:
    data = stripe_get(key, "/v1/coupons", {"limit": 100})

    coupons = []
    for c in data.get("data", []):
        coupons.append({
            "id": c.get("id"),
            "name": c.get("name"),
            "percent_off": c.get("percent_off"),
            "amount_off": (c.get("amount_off") or 0) / 100 if c.get("amount_off") else None,
            "currency": c.get("currency"),
            "duration": c.get("duration"),
            "times_redeemed": c.get("times_redeemed"),
            "valid": c.get("valid"),
            "created": c.get("created"),
        })

    return {
        "count": len(coupons),
        "has_more": data.get("has_more", False),
        "coupons": coupons,
    }
