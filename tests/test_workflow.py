import tempfile
import unittest
from pathlib import Path

from document_review.extractor import extract_fields
from document_review.loader import read_document
from document_review.workflow import review_documents

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "sample_documents"


class ExtractorTests(unittest.TestCase):
    def test_normalises_date_and_amount(self):
        fields = extract_fields(
            "Company: Demo Ltd\nStart date: 1 December 2026\n"
            "End date: 2026-12-20\nContract amount: N$1,250.50\n"
        )
        self.assertEqual(fields["start_date"].value, "2026-12-01")
        self.assertEqual(fields["end_date"].value, "2026-12-20")
        self.assertEqual(fields["contract_amount"].value, "NAD 1250.50")


class WorkflowTests(unittest.TestCase):
    def test_sample_documents_flag_conflicting_end_dates_and_missing_amount(self):
        report = review_documents([SAMPLES / "contract_a.md", SAMPLES / "contract_b.md"])
        conflict_fields = [item["field"] for item in report["conflicts"]]
        self.assertIn("end_date", conflict_fields)
        self.assertIn("contract_amount", report["missing_fields"])
        self.assertTrue(report["requires_human_review"])

    def test_same_values_do_not_create_conflict(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            first = Path(temp_dir) / "one.md"
            second = Path(temp_dir) / "two.md"
            content = (
                "Company: Demo Ltd\nStart date: 1 December 2026\n"
                "End date: 15 December 2026\nContract amount: N$100.00\n"
                "Contract reference: CN-2026-001\n"
            )
            first.write_text(content, encoding="utf-8")
            second.write_text(content, encoding="utf-8")
            report = review_documents([first, second])
            self.assertEqual(report["conflicts"], [])
            self.assertFalse(report["requires_human_review"])

    def test_empty_document_is_flagged(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            empty = Path(temp_dir) / "empty.txt"
            empty.write_text("", encoding="utf-8")
            report = review_documents([empty])
            self.assertTrue(report["requires_human_review"])
            self.assertEqual(len(report["missing_fields"]), 5)

    def test_unsupported_extension_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            unsupported = Path(temp_dir) / "file.pdf"
            unsupported.write_bytes(b"not a real PDF")
            report = review_documents([unsupported])
            self.assertEqual(report["document_count"], 0)
            self.assertEqual(len(report["rejected_inputs"]), 1)

    def test_invalid_date_is_reported(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            invalid = Path(temp_dir) / "invalid.md"
            invalid.write_text(
                "Company: Demo Ltd\nStart date: 45 Smarch 2026\n"
                "End date: 15 December 2026\nContract amount: N$10.00\n",
                encoding="utf-8",
            )
            report = review_documents([invalid])
            self.assertTrue(report["validation_errors"])
            self.assertTrue(report["requires_human_review"])


def test_extract_contract_reference(self):
        sample_text = "Contract reference: CN-2026-001"
        fields = extract_fields(sample_text)
        
        self.assertIn("contract_reference", fields)
        self.assertEqual(fields["contract_reference"].value, "CN-2026-001")
        self.assertIsNotNone(fields["contract_reference"].evidence)


if __name__ == "__main__":
    unittest.main()
