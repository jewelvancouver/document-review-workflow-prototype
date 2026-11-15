from .models import DocumentResult, REQUIRED_FIELDS


def find_conflicts(documents: list[DocumentResult]) -> list[dict]:
    """Flag fields with more than one distinct non-empty value."""
    conflicts: list[dict] = []
    for field_name in REQUIRED_FIELDS:
        observed = []
        seen = set()
        for document in documents:
            field = document.fields[field_name]
            if field.value:
                comparable = " ".join(field.value.casefold().split())
                if comparable not in seen:
                    seen.add(comparable)
                    observed.append({
                        "document": document.filename,
                        "value": field.value,
                        "evidence": field.evidence,
                    })
        if len(observed) > 1:
            conflicts.append({"field": field_name, "values": observed})
    return conflicts
