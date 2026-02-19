# Organizer Tools

**⚠️ ORGANIZERS ONLY - Do not share with participants**

This folder contains scripts for managing the Cold Start Citation Challenge.

## Files

### `make_dataset.py`
Generates the Cold Start dataset with proper train/test split.

**Usage:**
```bash
python make_dataset.py
```

**What it does:**
1. Generates a synthetic citation network (Barabasi-Albert model)
2. Creates 128-dimensional feature vectors for all nodes
3. Splits nodes into train (80%) and test (20%)
4. Removes all edges involving test nodes (cold start constraint)
5. Saves public data to `data/public/`
6. Saves ground truth to `data/private/` (never commit this!)

**Output files:**
- **Public** (share with participants):
  - `data/public/train_graph.csv` - Edges between training nodes
  - `data/public/train_features.csv` - Features for training nodes
  - `data/public/test_features.csv` - Features for test nodes (NO edges)
  
- **Private** (organizers only):
  - `data/private/test_labels.csv` - True citations from test nodes
  - `data/private/test_nodes.csv` - List of test node IDs

## Security

**Critical**: Never commit `data/private/` to version control!

The `.gitignore` is configured to exclude this folder, but double-check before any commits.

## Dataset Configuration

Edit `make_dataset.py` to adjust:
- `NUM_NODES`: Total papers (default: 1000)
- `NUM_FEATURES`: Feature dimension (default: 128)
- `TEST_RATIO`: Fraction of test nodes (default: 0.2)
- `RANDOM_SEED`: For reproducibility (default: 2026)

## Regenerating Data

To regenerate with different parameters:
1. Edit configuration in `make_dataset.py`
2. Run: `python make_dataset.py`
3. **Important**: Re-run baseline to update baseline scores
4. Clear previous submissions if significant changes made

## Workflow

**Initial Setup:**
```bash
# 1. Generate dataset
python organizer_tools/make_dataset.py

# 2. Generate baseline submission
python starter_code/baseline_inductive.py

# 3. Score baseline
python competition/score_submission.py \
  submissions/inbox/baseline_team/run_001 \
  data/private/test_labels.csv
```

**Scoring Submissions:**
```bash
# Validate format
python competition/validate_submission.py \
  submissions/inbox/<team_name>/<run_id>

# Score against ground truth
python competition/score_submission.py \
  submissions/inbox/<team_name>/<run_id> \
  data/private/test_labels.csv
```










