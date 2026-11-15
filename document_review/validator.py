import re
from datetime import date
from decimal import Decimal, InvalidOperation

from .models import FieldValue, REQUIRED_FIELDS


def validate_fields(fields: dict[str, FieldValue]) -> tuple[list[str], list[str]]:
    """Return missing field names and human-readable validation errors."""
    missing = [name for name in REQUIRED_FIELDS if not fields.get(name) or not fields[name].value]
    errors: list[str] = []

    for name in ("start_date", "end_date"):
        value = fields.get(name).value if fields.get(name) else None
        if value:
            try:
                date.fromisoformat(value)
            except ValueError:
                errors.append(f"{name} is not a recognised date: {value}")

    amount = fields.get("contract_amount").value if fields.get("contract_amount") else None
    if amount:
        match = re.fullmatch(r"NAD ([0-9]+\.[0-9]{2})", amount)
        if not match:
            errors.append(f"contract_amount is not a valid NAD amount: {amount}")
        else:
            try:
                if Decimal(match.group(1)) < 0:
                    errors.append("contract_amount cannot be negative")
            except InvalidOperation:
                errors.append(f"contract_amount is invalid: {amount}")

    return missing, errors
