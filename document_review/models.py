from dataclasses import dataclass
from typing import Optional

REQUIRED_FIELDS = ("company_name", "start_date", "end_date", "contract_amount", "contract_reference")


@dataclass
class FieldValue:
    value: Optional[str]
    evidence: Optional[str]


@dataclass 
class DocumentResult:
    filename: str
    fields: dict[str, FieldValue]
    missing_fields: list[str]
    validation_errors: list[str]

