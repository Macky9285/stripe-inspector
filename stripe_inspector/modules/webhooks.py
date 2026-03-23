"""Webhook endpoints module."""

from stripe_inspector.modules._base import stripe_get


def inspect(key: str) -> dict:
    data = stripe_get(key, "/v1/webhook_endpoints")

    endpoints = []
    for wh in data.get("data", []):
        endpoints.append({
            "id": wh.get("id"),
            "url": wh.get("url"),
            "status": wh.get("status"),
            "enabled_events": wh.get("enabled_events", []),
            "api_version": wh.get("api_version"),
            "created": wh.get("created"),
        })

    return {
        "count": len(endpoints),
        "endpoints": endpoints,
    }
