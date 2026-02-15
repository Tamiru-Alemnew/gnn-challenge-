"""
The Cold Start Citation Challenge 2026
---------------------------------------
Script: Submission Validator
Description: Validates that submissions follow the required format and structure.
Author: Competition Organizers

Usage:
    python validate_submission.py <submission_path>

Example:
    python validate_submission.py submissions/inbox/team_alpha/run_001
"""

import json
import pandas as pd
import sys
from pathlib import Path
from typing import Tuple, List


class SubmissionValidator:
    """Validates submission format and structure."""
    
    REQUIRED_PRED_COLUMNS = ['source', 'target']
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
        
        # Validate predictions.csv
        pred_path = self.submission_path / "predictions.csv"
        if not pred_path.exists():
            self.errors.append("Missing required file: predictions.csv")
        else:
            self._validate_predictions(pred_path)
        
        # Validate metadata.json
        meta_path = self.submission_path / "metadata.json"
        if not meta_path.exists():
            self.errors.append("Missing required file: metadata.json")
        else:
            self._validate_metadata(meta_path)
        
        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings
    
    def _validate_predictions(self, pred_path: Path):
        """Validate predictions.csv format."""
        try:
            df = pd.read_csv(pred_path)
        except Exception as e:
            self.errors.append(f"Failed to read predictions.csv: {str(e)}")
            return
        
        # Check required columns
        missing_cols = [col for col in self.REQUIRED_PRED_COLUMNS if col not in df.columns]
        if missing_cols:
            self.errors.append(f"predictions.csv missing required columns: {missing_cols}")
        
        # Check for empty predictions
        if len(df) == 0:
            self.warnings.append("predictions.csv is empty - no predictions made")
        
        # Check for duplicates
        if 'source' in df.columns and 'target' in df.columns:
            duplicates = df.duplicated(subset=['source', 'target']).sum()
            if duplicates > 0:
                self.warnings.append(f"predictions.csv contains {duplicates} duplicate edges")
        
        # Check for valid node IDs (should be integers)
        if 'source' in df.columns:
            try:
                df['source'].astype(int)
            except:
                self.errors.append("predictions.csv 'source' column contains non-integer values")
        
        if 'target' in df.columns:
            try:
                df['target'].astype(int)
            except:
                self.errors.append("predictions.csv 'target' column contains non-integer values")
    
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
        
        # Check required fields
        missing_fields = [field for field in self.REQUIRED_META_FIELDS if field not in metadata]
        if missing_fields:
            self.errors.append(f"metadata.json missing required fields: {missing_fields}")
        
        # Validate method field
        if 'method' in metadata:
            method = metadata['method']
            if method not in self.VALID_METHODS:
                self.errors.append(
                    f"metadata.json 'method' must be one of {self.VALID_METHODS}, got: {method}"
                )
        
        # Check description is not empty
        if 'description' in metadata and not metadata['description'].strip():
            self.warnings.append("metadata.json 'description' field is empty")


def validate_submission(submission_path: str) -> bool:
    """Validate a submission and print results."""
    print("=" * 70)
    print("SUBMISSION VALIDATOR - Cold Start Citation Challenge 2026")
    print("=" * 70)
    print(f"\nValidating: {submission_path}\n")
    
    validator = SubmissionValidator(submission_path)
    is_valid, errors, warnings = validator.validate()
    
    # Print warnings
    if warnings:
        print("⚠️  WARNINGS:")
        for warning in warnings:
            print(f"  - {warning}")
        print()
    
    # Print errors
    if errors:
        print("❌ VALIDATION FAILED:")
        for error in errors:
            print(f"  - {error}")
        print()
    else:
        print("✅ VALIDATION PASSED")
        print()
    
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
    is_valid = validate_submission(submission_path)
    
    sys.exit(0 if is_valid else 1)
