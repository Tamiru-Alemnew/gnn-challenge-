# Competition Infrastructure

This folder contains scripts for validating and scoring submissions.

## Scripts

### `validate_submission.py`
Checks if a submission follows the required format.

**Usage:**
```bash
python validate_submission.py <submission_path>
```

**Example:**
```bash
python validate_submission.py submissions/inbox/team_alpha/run_001
```

**Checks:**
- ✅ `predictions.csv` exists with columns: `source`, `target`
- ✅ `metadata.json` exists with fields: `team_name`, `method`, `description`
- ✅ `method` is one of: `"human"`, `"llm"`, `"hybrid"`
- ⚠️ Warns about duplicates, empty predictions, etc.

### `score_submission.py`
Evaluates a submission against ground truth labels.

**Usage:**
```bash
python score_submission.py <submission_path> <ground_truth_path>
```

**Example:**
```bash
python score_submission.py \
  submissions/inbox/team_alpha/run_001 \
  data/private/test_labels.csv
```

**Metrics Computed:**
- **F1-Score**: Primary ranking metric
- **Precision**: Correctness of predictions
- **Recall**: Coverage of true edges
- **Hit@K**: Accuracy per test node (K=1,3,5,10)

**Output:**
- Prints detailed results to console
- Saves `results.json` in submission folder

## Workflow

**For Participants (validation only):**
```bash
# Validate your submission before creating PR
python competition/validate_submission.py submissions/inbox/your_team/run_001
```

**For Organizers (validation + scoring):**
```bash
# 1. Validate format
python competition/validate_submission.py submissions/inbox/team_name/run_id

# 2. If valid, score it
python competition/score_submission.py \
  submissions/inbox/team_name/run_id \
  data/private/test_labels.csv

# 3. Update leaderboard.md with results
```

## GitHub Actions Integration

For automated scoring via CI/CD, create a workflow that:

1. Triggers on PR to `submissions/inbox/`
2. Runs `validate_submission.py`
3. If valid, runs `score_submission.py`
4. Comments results on PR
5. Updates `leaderboard.md` if merged

**Example workflow** (`.github/workflows/score.yml`):

```yaml
name: Score Submission

on:
  pull_request:
    paths:
      - 'submissions/inbox/**'

jobs:
  score:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: pip install -r starter_code/requirements.txt
      
      - name: Validate submission
        run: |
          # Find new submission path from PR diff
          python competition/validate_submission.py $SUBMISSION_PATH
      
      - name: Score submission
        run: |
          python competition/score_submission.py \
            $SUBMISSION_PATH \
            data/private/test_labels.csv
```

## Security Notes

- **Never expose** `data/private/test_labels.csv` in public repos
- Scoring should only run in private CI/CD with access to secrets
- Validate all submissions before scoring to prevent malicious code execution





