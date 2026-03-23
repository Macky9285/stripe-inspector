"""PII (Personally Identifiable Information) scanner.

Scans inspection results and extracts all PII found across modules.
"""

import re

EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
PHONE_RE = re.compile(r'\+?[\d\s\-\(\)]{7,20}')


def scan_pii(result: dict) -> dict:
    emails = set()
    names = set()
    phones = set()
    cards = set()
    addresses = set()
    countries = set()

    modules = result.get("modules", {})

    for mod_name, mod in modules.items():
        if not mod.get("success"):
            continue

        data = mod["data"]
        _extract_from_dict(data, emails, names, phones, cards, addresses, countries)

    return {
        "total_pii_items": len(emails) + len(names) + len(phones) + len(cards) + len(addresses),
        "emails": sorted(emails),
        "names": sorted(names),
        "phones": sorted(phones),
        "cards": sorted(cards),
        "addresses": sorted(addresses),
        "countries": sorted(countries),
        "email_count": len(emails),
        "name_count": len(names),
        "phone_count": len(phones),
        "card_count": len(cards),
        "address_count": len(addresses),
        "country_count": len(countries),
    }


def _extract_from_dict(obj, emails, names, phones, cards, addresses, countries):
    if isinstance(obj, dict):
        for key, val in obj.items():
            if val is None or val == "":
                continue

            if isinstance(val, str):
                k = key.lower()
                if k in ("email", "receipt_email", "support_email", "payer_email", "company_email"):
                    emails.add(val)
                elif k in ("name", "full_name", "payer_name", "first_name", "last_name", "display_name", "business_name"):
                    names.add(val)
                elif k in ("phone", "support_phone", "phone_number"):
                    phones.add(val)
                elif k == "card_last4" and val:
                    cards.add(f"**** {val}")
                elif k in ("country", "card_country"):
                    countries.add(val)
                elif k in ("line1",) and val:
                    addresses.add(val)
            elif isinstance(val, (dict, list)):
                _extract_from_dict(val, emails, names, phones, cards, addresses, countries)

    elif isinstance(obj, list):
        for item in obj:
            _extract_from_dict(item, emails, names, phones, cards, addresses, countries)
