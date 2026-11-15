# Document Review Workflow Prototype

Manual document review in contract management is slow, prone to oversight, and vulnerable to inconsistencies across multiple versions or drafts. This project automates the extraction and validation of critical contract fields (such as company name, start/end dates, contract amounts, and contract references) from text documents, flag missing fields, detect cross-document conflicts, and determine whether human intervention is required.

A small, offline Python portfolio project for a document-workflow internship. It reads fictional `.txt` and `.md` contract summaries, extracts labelled fields, validates values, compares documents and writes a JSON report that flags missing or conflicting information.

> **Honesty note:** This starter version uses rule-based extraction. It is not connected to an AI model and is not an AI agent. A structured-output schema, prompt template and safe integration plan are included to show how a future approved model integration would fit into the workflow.



## What it demonstrates

- Python modules and functions
- Text-file input and size/type checks
- Data normalisation and validation
- Evidence tracking back to the source line
- Cross-document conflict detection
- JSON report generation
- Automated tests using Python's standard `unittest` library
- A defined schema and prompt design for a future LLM integration

## Requirements

- Python 3.10 or newer
- No third-party packages are required for the demo

## Run on Windows PowerShell

1. Open `Document_Review_Workflow_Portfolio_Project` folder in VS Code.
2. In VS Code, choose **Terminal → New Terminal**.
3. Run:

   ```powershell
   py --version
   py main.py sample_documents
   ```

5. Open `outputs/review_report.json` to inspect the report.

The sample documents intentionally disagree about the end date, and the second document omits the amount. The program should flag both for human review.

## Run the tests

In the project root, run:

```powershell
py -m unittest discover -s tests -v
```

All tests should pass. If `py` is not recognised, try `python` instead.

commands used:
py -m unittest discover -s tests -v

results: 
Ran 6 tests in 1.058s

FAILED (failures=2) -> [Resolved after updating mock files and missing field counts] -> 
Ran 6 tests in ~1.0s
OK

## Project structure

```text
Document_Review_Workflow_Portfolio_Project/
├── document_review/       # loader, extractor, validator, comparator, workflow
├── sample_documents/     # fictional examples
├── tests/                 # automated tests
├── schemas/               # structured extraction schema
├── docs/                  # prompt template and AI integration plan
├── outputs/               # generated JSON report
├── main.py                # command-line entry point
└── PORTFOLIO_NOTES.md     # accurate portfolio wording
```

## Known limitations

- Only `.txt` and `.md` files are supported.
- The demo expects explicitly labelled fields; it does not understand arbitrary prose.
- It does not process PDFs, scanned documents or OCR.
- It does not call an LLM or use AI agents.
- It is a learning/portfolio prototype, not a production document-management system.

No live LLM connection: The workflow relies purely on offline regular expression patterns and rule-based extractors rather than generative AI models.

No PDF/OCR support: The system currently processes plain text (.txt) and markdown (.md) files; scanned PDFs or image-based contracts are not supported.

No production security audit: The repository is structured as a portfolio demonstration project and lacks enterprise-grade security hardening, authentication layers, and secrets management.

## Suggested next improvements

To scale document extraction beyond rigid regular expressions, an approved LLM provider (such as OpenAI, Anthropic, or an on-premise open-weights model via vLLM) could be integrated by replacing the rule-based extractor.py module with a structured prompting layer. By leveraging JSON mode or function calling, the model would parse raw text into the exact schema required (schemas/extraction.schema.json). To test this safely, we would introduce mock LLM response fixtures in the unit test suite, implement fallback mechanisms for network timeouts, and run evaluation benchmarks against a golden dataset of contract samples to measure extraction accuracy.
