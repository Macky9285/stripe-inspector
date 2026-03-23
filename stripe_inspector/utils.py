"""Shared utilities."""

from datetime import datetime, timezone


def format_timestamp(ts) -> str:
    if ts is None:
        return ""
    try:
        ts = int(ts)
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        return dt.strftime("%Y-%m-%d %H:%M")
    except (ValueError, TypeError, OSError):
        return str(ts)
