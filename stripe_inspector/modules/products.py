"""Products module."""

from stripe_inspector.modules._base import stripe_get


def inspect(key: str) -> dict:
    data = stripe_get(key, "/v1/products", {"limit": 100})

    products = []
    for p in data.get("data", []):
        products.append({
            "id": p.get("id"),
            "name": p.get("name"),
            "description": p.get("description"),
            "active": p.get("active"),
            "type": p.get("type"),
            "created": p.get("created"),
            "default_price": p.get("default_price"),
            "metadata": p.get("metadata", {}),
        })

    return {
        "count": len(products),
        "has_more": data.get("has_more", False),
        "products": products,
    }
