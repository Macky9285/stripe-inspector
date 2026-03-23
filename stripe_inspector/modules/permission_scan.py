"""Permission scanner — probes every known Stripe endpoint to build a permission matrix."""

import requests

STRIPE_BASE = "https://api.stripe.com"

# Comprehensive list of Stripe API endpoints to probe
ENDPOINTS = {
    "account": "/v1/account",
    "balance": "/v1/balance",
    "balance_transactions": "/v1/balance_transactions?limit=1",
    "charges": "/v1/charges?limit=1",
    "customers": "/v1/customers?limit=1",
    "disputes": "/v1/disputes?limit=1",
    "events": "/v1/events?limit=1",
    "invoices": "/v1/invoices?limit=1",
    "invoice_items": "/v1/invoiceitems?limit=1",
    "payment_intents": "/v1/payment_intents?limit=1",
    "payment_methods": "/v1/payment_methods?limit=1&type=card",
    "payouts": "/v1/payouts?limit=1",
    "prices": "/v1/prices?limit=1",
    "products": "/v1/products?limit=1",
    "promotion_codes": "/v1/promotion_codes?limit=1",
    "refunds": "/v1/refunds?limit=1",
    "setup_intents": "/v1/setup_intents?limit=1",
    "subscriptions": "/v1/subscriptions?limit=1",
    "tax_rates": "/v1/tax_rates?limit=1",
    "transfers": "/v1/transfers?limit=1",
    "webhook_endpoints": "/v1/webhook_endpoints?limit=1",
    "coupons": "/v1/coupons?limit=1",
    "files": "/v1/files?limit=1",
    "file_links": "/v1/file_links?limit=1",
    "connected_accounts": "/v1/accounts?limit=1",
    "application_fees": "/v1/application_fees?limit=1",
    "country_specs": "/v1/country_specs?limit=1",
    "top_ups": "/v1/topups?limit=1",
    "reviews": "/v1/reviews?limit=1",
    "radar_value_lists": "/v1/radar/value_lists?limit=1",
    "reporting_report_runs": "/v1/reporting/report_runs?limit=1",
    "credit_notes": "/v1/credit_notes?limit=1",
    "payment_links": "/v1/payment_links?limit=1",
    "checkout_sessions": "/v1/checkout/sessions?limit=1",
}


def inspect(key: str) -> dict:
    allowed = []
    denied = []
    errors = []

    for name, endpoint in ENDPOINTS.items():
        url = f"{STRIPE_BASE}{endpoint}"
        try:
            resp = requests.get(url, auth=(key, ""), timeout=10)
            if resp.status_code == 200:
                allowed.append(name)
            elif resp.status_code in (401, 403):
                denied.append(name)
            else:
                error_msg = resp.json().get("error", {}).get("message", f"HTTP {resp.status_code}")
                errors.append({"endpoint": name, "status": resp.status_code, "error": error_msg})
        except requests.Timeout:
            errors.append({"endpoint": name, "error": "timeout"})
        except Exception as e:
            errors.append({"endpoint": name, "error": str(e)})

    return {
        "total_endpoints": len(ENDPOINTS),
        "allowed_count": len(allowed),
        "denied_count": len(denied),
        "error_count": len(errors),
        "allowed": allowed,
        "denied": denied,
        "errors": errors,
    }
