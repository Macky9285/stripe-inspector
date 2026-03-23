"""CLI interface for StripeInspector."""

import json
import sys
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from stripe_inspector.core import StripeInspector, ALL_MODULES
from stripe_inspector.report import generate_html_report

app = typer.Typer(
    name="stripe-inspector",
    help="Security research tool to enumerate and inspect Stripe API keys.",
    add_completion=False,
)
console = Console()


def render_account(data: dict):
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Field", style="bold cyan", width=24)
    table.add_column("Value")

    table.add_row("Account ID", data.get("id", "N/A"))
    table.add_row("Business Name", data.get("business_name") or "N/A")
    table.add_row("Display Name", data.get("display_name") or "N/A")
    table.add_row("Email", data.get("email") or "N/A")
    table.add_row("Country", data.get("country") or "N/A")
    table.add_row("Currency", data.get("default_currency") or "N/A")
    table.add_row("Business Type", data.get("business_type") or "N/A")
    table.add_row("Type", data.get("type") or "N/A")
    table.add_row("Charges Enabled", str(data.get("charges_enabled", "N/A")))
    table.add_row("Payouts Enabled", str(data.get("payouts_enabled", "N/A")))
    table.add_row("Statement Descriptor", data.get("statement_descriptor") or "N/A")
    table.add_row("URL", data.get("url") or "N/A")
    table.add_row("Support Phone", data.get("support_phone") or "N/A")
    table.add_row("MCC", data.get("mcc") or "N/A")

    individual = data.get("individual", {})
    if individual:
        name = f"{individual.get('first_name', '')} {individual.get('last_name', '')}".strip()
        if name:
            table.add_row("Owner Name", name)
        if individual.get("email"):
            table.add_row("Owner Email", individual["email"])
        if individual.get("title"):
            table.add_row("Owner Title", individual["title"])

    addr = data.get("address", {})
    if addr and any(addr.values()):
        parts = [v for v in [addr.get("line1"), addr.get("city"), addr.get("state"), addr.get("postal_code"), addr.get("country")] if v]
        table.add_row("Address", ", ".join(parts))

    caps = data.get("capabilities", {})
    if caps:
        table.add_row("Capabilities", ", ".join(caps.keys()))

    schedule = data.get("payout_schedule", {})
    if schedule:
        table.add_row("Payout Schedule", f"{schedule.get('interval', 'N/A')} ({schedule.get('delay_days', '?')} day delay)")

    return table


def render_balance(data: dict):
    table = Table(show_header=True, box=None, padding=(0, 2))
    table.add_column("Type", style="bold")
    table.add_column("Amount", justify="right")
    table.add_column("Currency")

    for item in data.get("available", []):
        table.add_row("Available", f"{item['amount']:.2f}", item["currency"].upper())
    for item in data.get("pending", []):
        table.add_row("Pending", f"{item['amount']:.2f}", item["currency"].upper())

    return table


def render_list_table(data: dict, key: str, columns: list[tuple[str, str]]):
    items = data.get(key, [])
    if not items:
        return f"[dim]No {key} found[/dim]"

    table = Table(show_header=True, box=None, padding=(0, 2))
    for col_name, _ in columns:
        table.add_column(col_name, style="bold" if col_name == "ID" else None)

    for item in items[:20]:
        row = []
        for _, field in columns:
            val = item.get(field, "")
            if val is None:
                val = ""
            row.append(str(val))
        table.add_row(*row)

    count = data.get("count", len(items))
    has_more = data.get("has_more", False)
    suffix = f"\n[dim]Showing {min(20, count)} of {count}{'+ (has_more)' if has_more else ''}[/dim]"

    return table, suffix


MODULE_RENDERERS = {
    "account": lambda d: (render_account(d), ""),
    "balance": lambda d: (render_balance(d), ""),
    "customers": lambda d: render_list_table(d, "customers", [
        ("ID", "id"), ("Name", "name"), ("Email", "email"), ("Country", "country"),
    ]),
    "charges": lambda d: render_list_table(d, "charges", [
        ("ID", "id"), ("Amount", "amount"), ("Currency", "currency"), ("Payer", "payer_name"), ("Email", "payer_email"), ("Card", "card_last4"),
    ]),
    "payment_intents": lambda d: render_list_table(d, "intents", [
        ("ID", "id"), ("Amount", "amount"), ("Currency", "currency"), ("Status", "status"),
    ]),
    "products": lambda d: render_list_table(d, "products", [
        ("ID", "id"), ("Name", "name"), ("Type", "type"), ("Active", "active"),
    ]),
    "payouts": lambda d: render_list_table(d, "payouts", [
        ("ID", "id"), ("Amount", "amount"), ("Currency", "currency"), ("Status", "status"),
    ]),
    "subscriptions": lambda d: render_list_table(d, "subscriptions", [
        ("ID", "id"), ("Customer", "customer"), ("Status", "status"), ("Currency", "currency"),
    ]),
    "invoices": lambda d: render_list_table(d, "invoices", [
        ("ID", "id"), ("Customer", "customer"), ("Amount Due", "amount_due"), ("Status", "status"),
    ]),
    "webhooks": lambda d: render_list_table(d, "endpoints", [
        ("ID", "id"), ("URL", "url"), ("Status", "status"),
    ]),
    "events": lambda d: render_list_table(d, "events", [
        ("ID", "id"), ("Type", "type"), ("Live", "livemode"),
    ]),
    "connected": lambda d: render_list_table(d, "accounts", [
        ("ID", "id"), ("Email", "email"), ("Country", "country"), ("Type", "type"),
    ]),
}


def display_results(result: dict):
    # Key info header
    key_type = result.get("key_type", "unknown")
    is_live = result.get("is_live", False)
    style = "bold red" if is_live else "bold yellow"
    label = "LIVE KEY" if is_live else "TEST KEY"
    if result.get("is_restricted"):
        label = f"RESTRICTED {label}"

    console.print()
    console.print(Panel(
        f"[{style}]{label}[/{style}]  {result['masked_key']}\n"
        f"[dim]{result.get('timestamp', '')}[/dim]",
        title="[bold]StripeInspector[/bold]",
        border_style="bright_blue",
    ))

    # Permissions summary
    perms = result.get("permissions", {})
    allowed = sum(1 for v in perms.values() if v == "allowed")
    denied = sum(1 for v in perms.values() if v == "denied")
    errors = sum(1 for v in perms.values() if v == "error")
    console.print(f"\n[bold]Permissions:[/bold] [green]{allowed} allowed[/green] | [red]{denied} denied[/red] | [yellow]{errors} errors[/yellow]\n")

    # Module results
    for name, module_result in result.get("modules", {}).items():
        if not module_result.get("success"):
            console.print(f"[bold]{name.upper()}[/bold]: [red]{module_result.get('error', 'Failed')}[/red]\n")
            continue

        data = module_result["data"]
        renderer = MODULE_RENDERERS.get(name)

        if renderer:
            output = renderer(data)
            if isinstance(output, tuple):
                table, suffix = output
                console.print(f"[bold bright_blue]{name.upper()}[/bold bright_blue]")
                if isinstance(table, str):
                    console.print(table)
                else:
                    console.print(table)
                if suffix:
                    console.print(suffix)
            else:
                console.print(f"[bold bright_blue]{name.upper()}[/bold bright_blue]")
                console.print(output)
        else:
            console.print(f"[bold bright_blue]{name.upper()}[/bold bright_blue]")
            console.print(f"[dim]{json.dumps(data, indent=2, default=str)[:500]}[/dim]")

        console.print()


@app.command()
def inspect(
    key: str = typer.Argument(..., help="Stripe API key to inspect"),
    output: str = typer.Option("table", "--output", "-o", help="Output format: table, json"),
    report: Optional[str] = typer.Option(None, "--report", "-r", help="Generate HTML report to file"),
    modules: Optional[str] = typer.Option(None, "--modules", "-m", help="Comma-separated modules to run"),
    no_color: bool = typer.Option(False, "--no-color", help="Disable colored output"),
):
    """Inspect a Stripe API key and enumerate accessible data."""
    if no_color:
        console.no_color = True

    module_list = None
    if modules:
        module_list = [m.strip() for m in modules.split(",")]
        invalid = [m for m in module_list if m not in ALL_MODULES]
        if invalid:
            console.print(f"[red]Unknown modules: {', '.join(invalid)}[/red]")
            console.print(f"[dim]Available: {', '.join(ALL_MODULES.keys())}[/dim]")
            raise typer.Exit(1)

    inspector = StripeInspector(key, modules=module_list)

    if not inspector.validate_key():
        console.print("[red]Invalid key format.[/red] Expected: sk_test_*, sk_live_*, rk_test_*, rk_live_*")
        raise typer.Exit(1)

    if inspector.key_type and "live" in inspector.key_type:
        console.print("[bold red]WARNING: This is a LIVE key. Data accessed is real.[/bold red]\n")

    import threading, itertools

    spinner_running = True
    spinner_text = "Starting..."

    def spinner_thread():
        frames = itertools.cycle(["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"])
        while spinner_running:
            sys.stderr.write(f"\r  {next(frames)} {spinner_text}" + " " * 20)
            sys.stderr.flush()
            import time; time.sleep(0.08)

    t = threading.Thread(target=spinner_thread, daemon=True)
    t.start()

    def on_progress(module_name: str):
        nonlocal spinner_text
        spinner_text = f"Scanning {module_name}..."

    result = inspector.inspect(progress_callback=on_progress)
    spinner_running = False
    t.join(timeout=0.2)
    sys.stderr.write("\r  Done." + " " * 40 + "\n")
    sys.stderr.flush()

    if output == "json":
        print(json.dumps(result, indent=2, default=str))
    else:
        display_results(result)

    if report:
        html = generate_html_report(result)
        with open(report, "w", encoding="utf-8") as f:
            f.write(html)
        console.print(f"\n[green]Report saved to {report}[/green]")


@app.command()
def serve(
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="Host to bind to"),
    port: int = typer.Option(8000, "--port", "-p", help="Port to listen on"),
    token: Optional[str] = typer.Option(None, "--token", "-t", help="Bearer token for API auth"),
):
    """Start the web UI server."""
    import uvicorn
    from stripe_inspector.web.app import create_app

    web_app = create_app(token=token)

    console.print(Panel(
        f"[bold green]StripeInspector Web UI[/bold green]\n\n"
        f"URL: [link]http://{host}:{port}[/link]\n"
        f"Auth: {'[yellow]Token required[/yellow]' if token else '[dim]None (local only)[/dim]'}",
        border_style="bright_blue",
    ))

    uvicorn.run(web_app, host=host, port=port, log_level="warning")


@app.command(name="list-modules")
def list_modules():
    """List available inspection modules."""
    table = Table(title="Available Modules", show_header=True)
    table.add_column("Module", style="bold cyan")
    table.add_column("Endpoint")

    endpoints = {
        "account": "/v1/account",
        "balance": "/v1/balance",
        "customers": "/v1/customers",
        "charges": "/v1/charges",
        "payment_intents": "/v1/payment_intents",
        "products": "/v1/products",
        "payouts": "/v1/payouts",
        "subscriptions": "/v1/subscriptions",
        "invoices": "/v1/invoices",
        "webhooks": "/v1/webhook_endpoints",
        "events": "/v1/events",
        "connected": "/v1/accounts",
    }

    for name in ALL_MODULES:
        table.add_row(name, endpoints.get(name, ""))

    console.print(table)


if __name__ == "__main__":
    app()
