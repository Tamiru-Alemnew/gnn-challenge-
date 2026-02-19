"""
The Cold Start Citation Challenge 2026
--------------------------------------
Script: Submission Validator
Description: Validates that submissions follow the required format and structure.
             For security, predictions must be encrypted as predictions.enc.
Author: Competition Organizers
"""

import json
import sys
from pathlib import Path
from typing import Tuple, List


class SubmissionValidator:
    """Validates submission format and structure."""

    REQUIRED_META_FIELDS = ['team_name', 'method', 'description']
    VALID_METHODS = ['human', 'llm', 'hybrid']

    def __init__(self, submission_path: Path):
        self.submission_path = Path(submission_path)
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate(self) -> Tuple[bool, List[str], List[str]]:
        """Run all validation checks."""
        self.errors = []
        self.warnings = []

        if not self.submission_path.exists():
            self.errors.append(f"Submission path does not exist: {self.submission_path}")
            return False, self.errors, self.warnings

        if not self.submission_path.is_dir():
            self.errors.append(f"Submission path is not a directory: {self.submission_path}")
            return False, self.errors, self.warnings

        # Encrypted predictions required
        pred_csv = self.submission_path / "predictions.csv"
        pred_enc = self.submission_path / "predictions.enc"

        if pred_csv.exists():
            self.errors.append(
                "Plain text submissions are not allowed. "
                "Please run the encryption script to create predictions.enc."
            )
        if not pred_enc.exists():
            self.errors.append("Missing required file: predictions.enc")
        else:
            try:
                size = pred_enc.stat().st_size
                if size <= 0:
                    self.errors.append("predictions.enc is empty")
            except Exception as e:
                self.errors.append(f"Unable to read predictions.enc: {e}")

        # Validate metadata.json
        meta_path = self.submission_path / "metadata.json"
        if not meta_path.exists():
            self.errors.append("Missing required file: metadata.json")
        else:
            self._validate_metadata(meta_path)

        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings

    def _validate_metadata(self, meta_path: Path):
        """Validate metadata.json format."""
        try:
            with open(meta_path, 'r') as f:
                metadata = json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON in metadata.json: {str(e)}")
            return
        except Exception as e:
            self.errors.append(f"Failed to read metadata.json: {str(e)}")
            return

        missing_fields = [field for field in self.REQUIRED_META_FIELDS if field not in metadata]
        if missing_fields:
            self.errors.append(f"metadata.json missing required fields: {missing_fields}")

        if 'method' in metadata:
            method = metadata['method']
            if method not in self.VALID_METHODS:
                self.errors.append(
                    f"metadata.json 'method' must be one of {self.VALID_METHODS}, got: {method}"
                )

        if 'description' in metadata and not metadata['description'].strip():
            self.warnings.append("metadata.json 'description' field is empty")


def validate_submission(submission_path: str) -> bool:
    """Validate a submission and print results."""
    print("=" * 70)
    print("SUBMISSION VALIDATOR - Cold Start Citation Challenge 2026")
    print("=" * 70)
    print(f"\nValidating: {submission_path}\n")

    validator = SubmissionValidator(Path(submission_path))
    is_valid, errors, warnings = validator.validate()

    if warnings:
        print("⚠️  WARNINGS:")
        for w in warnings:
            print(f"  - {w}")
        print()

    if errors:
        print("❌ VALIDATION FAILED:")
        for e in errors:
            print(f"  - {e}")
        print()
    else:
        print("✅ VALIDATION PASSED\n")

    print("=" * 70)
    return is_valid


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_submission.py <submission_path>")
        print()
        print("Example:")
        print("  python validate_submission.py submissions/inbox/team_alpha/run_001")
        sys.exit(1)

    submission_path = sys.argv[1]
    ok = validate_submission(submission_path)
    sys.exit(0 if ok else 1)

