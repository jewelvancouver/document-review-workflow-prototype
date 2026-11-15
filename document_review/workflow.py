from pathlib import Path

from .comparator import find_conflicts
from .extractor import extract_fields
from .loader import read_document
from .models import DocumentResult, REQUIRED_FIELDS
from .validator import validate_fields


def review_documents(paths: list[Path]) -> dict:
    document_results: list[DocumentResult] = []
    rejected_inputs: list[dict] = []

    for path in paths:
        try:
            text = read_document(path)
            fields = extract_fields(text)
            missing, errors = validate_fields(fields)
            document_results.append(DocumentResult(
                filename=path.name,
                fields=fields,
                missing_fields=missing,
                validation_errors=errors,
            ))
        except (OSError, ValueError) as exc:
            rejected_inputs.append({"filename": path.name, "reason": str(exc)})

    conflicts = find_conflicts(document_results)
    missing_anywhere = sorted({
        field for document in document_results for field in document.missing_fields
    })
    validation_errors = [
        {"document": document.filename, "errors": document.validation_errors}
        for document in document_results if document.validation_errors
    ]

    serialised_documents = []
    for document in document_results:
        serialised_documents.append({
            "filename": document.filename,
            "fields": {
                key: {"value": value.value, "evidence": value.evidence}
                for key, value in document.fields.items()
            },
            "missing_fields": document.missing_fields,
            "validation_errors": document.validation_errors,
        })

    requires_review = bool(conflicts or missing_anywhere or validation_errors or rejected_inputs)
    return {
        "project": "Document Review Workflow Prototype",
        "processing_mode": "offline_rule_based_demo",
        "document_count": len(document_results),
        "documents": serialised_documents,
        "missing_fields": missing_anywhere,
        "conflicts": conflicts,
        "validation_errors": validation_errors,
        "rejected_inputs": rejected_inputs,
        "requires_human_review": requires_review,
        "important_note": (
            "This portfolio prototype uses explicit labelled-field rules, not an AI model. "
            "It demonstrates document workflow, validation, evidence tracking and testing."
        ),
    }
