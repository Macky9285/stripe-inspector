# Contributing to StripeInspector

Thanks for your interest in contributing! Here's how to get started.

## Development Setup

```bash
# Clone the repo
git clone https://github.com/mrdebugger/stripe-inspector.git
cd stripe-inspector

# Install in development mode
pip install -e ".[dev]"

# Or with uv
uv pip install -e ".[dev]"
```

## Project Structure

```
stripe_inspector/
  core.py            # Main inspector engine
  cli.py             # CLI commands (typer)
  report.py          # HTML report generator
  modules/           # One file per Stripe API module
    _base.py         # Shared HTTP request logic
    account.py       # /v1/account
    balance.py       # /v1/balance
    ...
  web/
    app.py           # FastAPI application
    static/          # Frontend HTML/CSS/JS
    templates/       # Jinja2 report template
```

## Adding a New Module

1. Create `stripe_inspector/modules/your_module.py`:

```python
from stripe_inspector.modules._base import stripe_get

def inspect(key: str) -> dict:
    data = stripe_get(key, "/v1/your_endpoint", {"limit": 100})
    # Parse and return structured data
    return {"count": len(data.get("data", [])), "items": [...]}
```

2. Register it in `stripe_inspector/core.py`:

```python
from stripe_inspector.modules import your_module

ALL_MODULES = {
    ...
    "your_module": your_module,
}
```

3. Add a renderer in `cli.py` under `MODULE_RENDERERS`.

## Code Style

- Keep modules simple and focused — one file per Stripe API area
- Handle errors gracefully: raise `PermissionError` for 403/401, `ConnectionError` for 5xx
- Never log or store API keys to disk
- Use type hints

## Submitting Changes

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Test with a Stripe test key: `stripe-inspector inspect sk_test_...`
5. Submit a pull request

## Reporting Issues

- Include the error output
- Specify which module(s) are affected
- Never include real API keys in issues

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
