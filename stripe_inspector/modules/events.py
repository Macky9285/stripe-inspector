"""Events module."""

from stripe_inspector.modules._base import stripe_get


def inspect(key: str) -> dict:
    data = stripe_get(key, "/v1/events", {"limit": 20})

    events = []
    for e in data.get("data", []):
        events.append({
            "id": e.get("id"),
            "type": e.get("type"),
            "created": e.get("created"),
            "livemode": e.get("livemode"),
        })

    return {
        "count": len(events),
        "has_more": data.get("has_more", False),
        "events": events,
    }
