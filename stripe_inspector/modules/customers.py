"""Customers module."""

from stripe_inspector.modules._base import stripe_get


def inspect(key: str) -> dict:
    data = stripe_get(key, "/v1/customers", {"limit": 100})

    customers = []
    for c in data.get("data", []):
        customers.append({
            "id": c.get("id"),
            "name": c.get("name"),
            "email": c.get("email"),
            "phone": c.get("phone"),
            "currency": c.get("currency"),
            "balance": (c.get("balance", 0) or 0) / 100,
            "created": c.get("created"),
            "metadata": c.get("metadata", {}),
            "country": (c.get("address") or {}).get("country"),
        })

    return {
        "count": len(customers),
        "has_more": data.get("has_more", False),
        "customers": customers,
    }
