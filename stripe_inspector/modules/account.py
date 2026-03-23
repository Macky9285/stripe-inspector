"""Account information module."""

from stripe_inspector.modules._base import stripe_get


def inspect(key: str) -> dict:
    data = stripe_get(key, "/v1/account")

    result = {
        "id": data.get("id"),
        "business_name": None,
        "display_name": None,
        "email": data.get("email"),
        "country": data.get("country"),
        "default_currency": data.get("default_currency"),
        "business_type": data.get("business_type"),
        "charges_enabled": data.get("charges_enabled"),
        "payouts_enabled": data.get("payouts_enabled"),
        "details_submitted": data.get("details_submitted"),
        "type": data.get("type"),
    }

    # Business profile
    bp = data.get("business_profile", {})
    if bp:
        result["business_name"] = bp.get("name")
        result["support_email"] = bp.get("support_email")
        result["support_phone"] = bp.get("support_phone")
        result["url"] = bp.get("url")
        result["mcc"] = bp.get("mcc")
        addr = bp.get("support_address", {})
        if addr:
            result["address"] = {
                "line1": addr.get("line1"),
                "city": addr.get("city"),
                "state": addr.get("state"),
                "postal_code": addr.get("postal_code"),
                "country": addr.get("country"),
            }

    # Individual info (if available)
    individual = data.get("individual", {})
    if individual:
        result["individual"] = {
            "first_name": individual.get("first_name"),
            "last_name": individual.get("last_name"),
            "email": individual.get("email"),
            "title": individual.get("relationship", {}).get("title"),
        }

    # Dashboard display name
    settings = data.get("settings", {})
    if settings:
        result["display_name"] = settings.get("dashboard", {}).get("display_name")
        result["statement_descriptor"] = settings.get("payments", {}).get("statement_descriptor")
        payout_schedule = settings.get("payouts", {}).get("schedule", {})
        if payout_schedule:
            result["payout_schedule"] = {
                "interval": payout_schedule.get("interval"),
                "delay_days": payout_schedule.get("delay_days"),
            }

    # Capabilities
    caps = data.get("capabilities", {})
    if caps:
        result["capabilities"] = {k: v for k, v in caps.items() if v == "active"}

    return result
