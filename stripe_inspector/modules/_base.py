"""Base utilities for Stripe API requests."""

import requests

STRIPE_BASE = "https://api.stripe.com"


def stripe_get(key: str, endpoint: str, params: dict = None) -> dict:
    url = f"{STRIPE_BASE}{endpoint}"
    resp = requests.get(url, auth=(key, ""), params=params, timeout=30)

    if resp.status_code == 403:
        raise PermissionError(f"Access denied to {endpoint}")
    if resp.status_code == 401:
        raise PermissionError(f"Invalid API key for {endpoint}")
    if resp.status_code >= 500:
        raise ConnectionError(f"Stripe server error ({resp.status_code})")
    if resp.status_code != 200:
        error = resp.json().get("error", {})
        msg = error.get("message", f"HTTP {resp.status_code}")
        raise Exception(msg)

    return resp.json()
