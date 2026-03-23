"""Connected accounts module (Stripe Connect)."""

from stripe_inspector.modules._base import stripe_get


def inspect(key: str) -> dict:
    data = stripe_get(key, "/v1/accounts", {"limit": 100})

    accounts = []
    for a in data.get("data", []):
        accounts.append({
            "id": a.get("id"),
            "email": a.get("email"),
            "country": a.get("country"),
            "type": a.get("type"),
            "charges_enabled": a.get("charges_enabled"),
            "payouts_enabled": a.get("payouts_enabled"),
            "created": a.get("created"),
        })

    return {
        "count": len(accounts),
        "has_more": data.get("has_more", False),
        "accounts": accounts,
    }
