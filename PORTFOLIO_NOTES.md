# Portfolio notes (use only after you have run, tested and understood the project)

## Accurate project description

Built a Python document-review workflow prototype that reads fictional Markdown/text contract summaries, extracts labelled fields, normalises dates and monetary values, preserves source evidence, validates missing/invalid information, compares documents for conflicts, and exports a JSON review report. Added automated tests for matching data, conflicting dates, missing fields, invalid dates and unsupported files.

## Be transparent

The current implementation uses deterministic, rule-based extraction. It does not call an LLM, does not implement an autonomous agent, and does not process PDFs or scanned images. The project includes a structured-output schema and a prompt design for a future approved AI-provider integration.

## Interview explanation

I built the offline workflow first so I could test the document pipeline independently of a model. The Python code is responsible for validation and cross-document comparison; the model, when an approved provider is connected, should only propose extracted values with evidence. Conflicts are sent for human review rather than guessed.
