# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-03-24

### Added
- 5 new modules: disputes, refunds, balance_transactions, coupons, permission_scan
- Permission scanner probes 35+ Stripe API endpoints to build a full access matrix
- PDF report generation via `--pdf` flag (requires `pip install stripe-inspector[pdf]`)
- Module selector in web UI with toggle chips, All/None buttons
- Terminal logo and animated demo SVG for README
- CHANGELOG, CONTRIBUTING docs
- Professional README with badges, module table, usage examples

### Changed
- CLI spinner replaced with threaded implementation for Windows compatibility
- Version bumped to 0.2.0

## [0.1.0] - 2026-03-23

### Added
- Initial release
- Core inspection engine with 12 modules: account, balance, customers, charges, payment_intents, products, payouts, subscriptions, invoices, webhooks, events, connected accounts
- CLI interface with `inspect`, `serve`, and `list-modules` commands
- Table, JSON, and HTML report output formats
- FastAPI web UI with dark theme
- Auto-detection of key types (secret/restricted, test/live)
- Per-module permission tracking
- Optional bearer token auth for web UI
- Module filtering with `--modules` flag
- Key masking in reports and output
