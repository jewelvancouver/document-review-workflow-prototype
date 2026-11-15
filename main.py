import argparse
import json
from pathlib import Path

from document_review.loader import collect_input_files
from document_review.workflow import review_documents


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Review fictional .txt/.md documents for missing and conflicting contract fields."
    )
    parser.add_argument("inputs", nargs="+", help="One or more files or folders to review")
    parser.add_argument("--output", default="outputs/review_report.json", help="JSON report destination")
    args = parser.parse_args()

    paths = collect_input_files(args.inputs)
    report = review_documents(paths)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("Document review completed.")
    print(f"Documents processed: {report['document_count']}")
    print(f"Conflicts found: {len(report['conflicts'])}")
    print(f"Missing fields: {', '.join(report['missing_fields']) or 'None'}")
    print(f"Human review required: {'Yes' if report['requires_human_review'] else 'No'}")
    print(f"JSON report saved to: {output_path.resolve()}")
    print("Mode: offline rule-based demo (not an LLM integration).")
    return 0 if report["document_count"] > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
