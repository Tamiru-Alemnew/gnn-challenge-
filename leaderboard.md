# Leaderboard

## The Citation Mystery Challenge 2026

Submissions are ranked by **F1-Score (Macro)**.

| Rank | Participant              | F1-Score | Submission Date | Method                              |
| ---- | ------------------------ | -------- | --------------- | ----------------------------------- |
| -    | Baseline (Random Forest) | TBD      | -               | Random Forest on feature_similarity |

---

### How to Submit

1. Fork this repository
2. Create your GNN model using the `node_u` and `node_v` columns to reconstruct graph topology
3. Generate predictions on `data/test.csv`
4. Save as `submissions/your_username_submission.csv` with format:
   ```
   target
   0
   1
   0
   ...
   ```
5. Submit a Pull Request with your submission file

### Evaluation

Submissions are automatically scored using `scoring_script.py` which compares predictions against the hidden ground truth (`data/test_labels.csv`).
