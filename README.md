<p align="center">
  <img src="assets/logo.svg" width="120" alt="StripeInspector Logo">
</p>

<h1 align="center">StripeInspector</h1>

<p align="center">
  <strong>Security research tool for Stripe API key enumeration and inspection</strong>
</p>

<p align="center">
  <a href="https://pypi.org/project/stripe-inspector/"><img src="https://img.shields.io/pypi/v/stripe-inspector?color=6c63ff&style=flat-square" alt="PyPI"></a>
  <a href="https://pypi.org/project/stripe-inspector/"><img src="https://img.shields.io/pypi/pyversions/stripe-inspector?style=flat-square" alt="Python"></a>
  <a href="https://github.com/mrdebugger/stripe-inspector/blob/main/LICENSE"><img src="https://img.shields.io/github/license/mrdebugger/stripe-inspector?style=flat-square" alt="License"></a>
</p>

---

StripeInspector takes a Stripe API key and enumerates everything accessible through it — account details, customers, charges, payouts, products, webhooks, and more. Built for security researchers, penetration testers, and bug bounty hunters.

## Features

- **12 inspection modules** — account, balance, customers, charges, payment intents, products, payouts, subscriptions, invoices, webhooks, events, connected accounts
- **CLI + Web UI** — both treated as first-class interfaces
- **3 output formats** — colored terminal tables, JSON, standalone HTML reports
- **Key type detection** — auto-identifies test/live, secret/restricted keys
- **Permission mapping** — shows which API endpoints the key can access
- **Self-hosted web UI** — dark-themed dashboard with FastAPI backend
- **Optional auth** — bearer token support for securing the web UI

## Installation

```bash
pip install stripe-inspector
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv pip install stripe-inspector
```

## Quick Start

### CLI

```bash
# Inspect a key (all modules)
stripe-inspector inspect sk_test_xxxx

# JSON output (pipe to jq, scripts, etc.)
stripe-inspector inspect sk_test_xxxx --output json

# Generate a standalone HTML report
stripe-inspector inspect sk_test_xxxx --report findings.html

# Inspect specific modules only
stripe-inspector inspect sk_test_xxxx --modules account,customers,charges

# List all available modules
stripe-inspector list-modules
```

### Web UI

```bash
# Start on localhost:8000
stripe-inspector serve

# Custom port with auth token
stripe-inspector serve --port 9000 --token mysecrettoken

# Expose to network (use with --token)
stripe-inspector serve --host 0.0.0.0 --token mysecrettoken
```

Open `http://localhost:8000` in your browser, paste a key, and hit Inspect.

## Modules

| Module | Endpoint | What It Finds |
|--------|----------|---------------|
| `account` | `/v1/account` | Owner name, email, country, address, business type, MCC, capabilities |
| `balance` | `/v1/balance` | Available and pending balances per currency |
| `customers` | `/v1/customers` | Customer names, emails, phone numbers, metadata |
| `charges` | `/v1/charges` | Payment amounts, payer details, card info, countries |
| `payment_intents` | `/v1/payment_intents` | Intent status, amounts, payment methods |
| `products` | `/v1/products` | Product names, types, pricing, active status |
| `payouts` | `/v1/payouts` | Payout amounts, bank destinations, schedules |
| `subscriptions` | `/v1/subscriptions` | Active plans, billing cycles, customers |
| `invoices` | `/v1/invoices` | Invoice amounts, payment status, hosted URLs |
| `webhooks` | `/v1/webhook_endpoints` | Endpoint URLs, subscribed event types |
| `events` | `/v1/events` | Recent API activity and event log |
| `connected` | `/v1/accounts` | Connected accounts (Stripe Connect platforms) |

## Key Types

| Prefix | Type | Risk Level |
|--------|------|------------|
| `sk_test_` | Secret test key | Low — sandbox data only |
| `sk_live_` | Secret live key | **High** — real customer data |
| `rk_test_` | Restricted test key | Low — limited permissions |
| `rk_live_` | Restricted live key | Medium — limited but real data |

## Security

- Keys are **never logged or stored** to disk
- The web UI sends keys **only to Stripe's API** from the backend — never to third parties
- HTML reports **mask keys** (show first 8 + last 4 characters only)
- Use `--token` to protect the web UI when exposing beyond localhost

## Disclaimer

This tool is intended for **authorized security testing**, bug bounty programs, penetration testing engagements, and educational purposes only. Only use it on API keys you own or have explicit written authorization to test.

Unauthorized access to third-party systems is illegal. The author assumes no liability for misuse of this tool.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## License

[MIT](LICENSE) - Ijaz Ur Rahim
