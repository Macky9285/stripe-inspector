"""Balance information module."""

from stripe_inspector.modules._base import stripe_get


def inspect(key: str) -> dict:
    data = stripe_get(key, "/v1/balance")

    result = {
        "livemode": data.get("livemode"),
        "available": [],
        "pending": [],
    }

    for item in data.get("available", []):
        result["available"].append({
            "amount": item.get("amount", 0) / 100,
            "currency": item.get("currency"),
        })

    for item in data.get("pending", []):
        result["pending"].append({
            "amount": item.get("amount", 0) / 100,
            "currency": item.get("currency"),
        })

    return result
