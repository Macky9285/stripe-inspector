"""Balance transactions module."""

from stripe_inspector.modules._base import stripe_get


def inspect(key: str) -> dict:
    data = stripe_get(key, "/v1/balance_transactions", {"limit": 100})

    txns = []
    for t in data.get("data", []):
        txns.append({
            "id": t.get("id"),
            "amount": (t.get("amount", 0) or 0) / 100,
            "net": (t.get("net", 0) or 0) / 100,
            "fee": (t.get("fee", 0) or 0) / 100,
            "currency": t.get("currency"),
            "type": t.get("type"),
            "status": t.get("status"),
            "description": t.get("description"),
            "created": t.get("created"),
            "source": t.get("source"),
        })

    return {
        "count": len(txns),
        "has_more": data.get("has_more", False),
        "transactions": txns,
    }
