"""Shared utilities."""

from datetime import datetime, timezone

TIMESTAMP_KEYS = {
    "created", "arrival_date", "current_period_start", "current_period_end",
}


def format_timestamp(ts) -> str:
    if ts is None:
        return ""
    try:
        ts = int(ts)
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        return dt.strftime("%Y-%m-%d %H:%M")
    except (ValueError, TypeError, OSError):
        return str(ts)


def add_formatted_timestamps(result: dict) -> dict:
    """Walk through all module data and add _formatted versions of timestamp fields.

    For each timestamp field like "created": 1707923179, adds
    "created_formatted": "2024-02-14 15:06" alongside it.
    """
    modules = result.get("modules", {})
    for mod in modules.values():
        if not mod.get("success"):
            continue
        data = mod["data"]
        _format_in_place(data)
    return result


def _format_in_place(obj):
    if isinstance(obj, dict):
        additions = {}
        for key, val in obj.items():
            if key in TIMESTAMP_KEYS and isinstance(val, (int, float)) and val > 1000000000:
                additions[f"{key}_formatted"] = format_timestamp(val)
            elif isinstance(val, (dict, list)):
                _format_in_place(val)
        obj.update(additions)
    elif isinstance(obj, list):
        for item in obj:
            _format_in_place(item)
