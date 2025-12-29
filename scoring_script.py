import pandas as pd
from sklearn.metrics import f1_score
import sys

# Usage: python scoring_script.py submissions/sample_submission.csv

if len(sys.argv) < 2:
    print("Error: Please provide the submission file path.")
    sys.exit(1)

submission_file = sys.argv[1]

# Load submission
try:
    submission = pd.read_csv(submission_file)
except FileNotFoundError:
    print(f"Error: File {submission_file} not found.")
    sys.exit(1)

# Load ground truth (hidden)
truth = pd.read_csv('data/test_labels.csv')

# Compute F1 score
# Ensure the submission has the same length as truth
if len(submission) != len(truth):
    print(f"Error: Submission has {len(submission)} rows, expected {len(truth)}.")
    sys.exit(1)

score = f1_score(truth['target'], submission['target'], average='macro')
print(f'Submission F1 Score: {score:.4f}')