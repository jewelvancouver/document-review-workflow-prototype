import re
from datetime import datetime
from decimal import Decimal, InvalidOperation

from .models import FieldValue

TEXT_PATTERNS = {
    "company_name": re.compile(r"(?im)^\s*(?:company|company name)\s*:\s*(.+?)\s*$"),
    "start_date": re.compile(r"(?im)^\s*(?:contract\s+)?start date\s*:\s*(.+?)\s*$"),
    "end_date": re.compile(r"(?im)^\s*(?:contract\s+)?(?:end|expiry|expiration) date\s*:\s*(.+?)\s*$"),
    "contract_reference": re.compile(r"(?im)^\s*(?:contract reference)\s*:\s*(.+?)\s*$"),
}
AMOUNT_PATTERN = re.compile(
    r"(?im)^\s*(?:contract\s+amount|amount|contract\s+value)\s*:\s*(?:N\$|NAD\s*)?\s*([0-9][0-9,]*(?:\.\d{1,2})?)\s*$"
)


def _normalise_date(raw: str) -> str:
    for date_format in ("%d %B %Y", "%d %b %Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(raw.strip(), date_format).date().isoformat()
        except ValueError:
            pass
    return raw.strip()


def _normalise_amount(raw: str) -> str:
    try:
        amount = Decimal(raw.replace(",", "")).quantize(Decimal("0.01"))
    except InvalidOperation:
        return raw.strip()
    return f"NAD {amount:.2f}"


def extract_fields(text: str) -> dict[str, FieldValue]:
    """Extract explicitly labelled fields; this is rule-based, not an LLM."""
    fields: dict[str, FieldValue] = {}

    for field_name, pattern in TEXT_PATTERNS.items():
        match = pattern.search(text)
        if match:
            raw_value = match.group(1).strip()
            value = _normalise_date(raw_value) if field_name in {"start_date", "end_date"} else raw_value
            fields[field_name] = FieldValue(value=value, evidence=match.group(0).strip())
        else:
            fields[field_name] = FieldValue(value=None, evidence=None)

    amount_match = AMOUNT_PATTERN.search(text)
    fields["contract_amount"] = FieldValue(
        value=_normalise_amount(amount_match.group(1)) if amount_match else None,
        evidence=amount_match.group(0).strip() if amount_match else None,
    )
    return fields
