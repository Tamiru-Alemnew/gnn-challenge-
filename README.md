# The Citation Mystery Challenge 2026

## Overview

Welcome to the Link Prediction Challenge! Your task is to predict missing citations between academic papers using Graph Neural Networks.

This challenge is designed to test concepts from **Deep Graph Learning Lectures 1.1 - 4.6**, including:

- Graph representation learning
- Message passing methods
- Node embeddings
- Link prediction techniques

## The Problem

Given a network of academic papers (nodes) and some known citations (edges), predict which additional citation links exist. This is a fundamental GNN problem that requires understanding graph structure beyond simple feature similarity.

## The Data

The dataset represents a synthetic citation network with 500 papers.

- **train.csv**: Contains pairs of paper IDs (`node_u`, `node_v`), a `feature_similarity` score, and the `target` column (`1` if citation exists, `0` otherwise).
- **test.csv**: Contains pairs of papers where the `target` is hidden. You must predict these.

**Important**: The baseline uses only `feature_similarity`, but to achieve high scores, you must leverage the graph structure using `node_u` and `node_v` to reconstruct the network topology.

## The Goal

The provided `baseline.py` uses a Random Forest on simple tabular features. However, since this is a graph, purely tabular methods miss the structural information!

**To achieve a high score, you should use GNN methods (like Node Embeddings, GCNs, or GraphSAGE) using the `node_u` and `node_v` columns to reconstruct the graph topology.**

## How to Run

### For Participants

1. **Install requirements**:

   ```bash
   cd starter_code
   pip install -r requirements.txt
   ```

2. **Run Baseline** (to verify setup):

   ```bash
   cd starter_code
   python baseline.py
   ```

   This creates `submissions/sample_submission.csv` with baseline predictions.

3. **Build your GNN model**:

   - Load `data/train.csv` to build your graph
   - Use `node_u` and `node_v` to reconstruct edges
   - Train your GNN model for link prediction
   - Predict on `data/test.csv`

4. **Create submission**:
   - Save predictions as CSV with format:
     ```csv
     target
     0
     1
     0
     ...
     ```
   - Submit via Pull Request (see [leaderboard.md](leaderboard.md))

### For Organizers

1. **Generate Data**:

   ```bash
   python generate_data.py
   ```

   This creates `data/train.csv`, `data/test.csv`, and `data/test_labels.csv`.

2. **Score Submission**:
   ```bash
   python scoring_script.py submissions/sample_submission.csv
   ```

## Evaluation Metric

Submissions are evaluated on **F1-Score (Macro)** - a metric that balances precision and recall, especially important for imbalanced link prediction tasks.

## Repository Structure

```
gnn-challenge/
├── data/                    # Dataset files
│   ├── train.csv           # Training data with labels
│   ├── test.csv            # Test data (labels hidden)
│   └── test_labels.csv     # Hidden ground truth (organizers only)
├── submissions/            # Submission files
│   └── sample_submission.csv
├── starter_code/           # Starter code for participants
│   ├── baseline.py         # Random Forest baseline model
│   └── requirements.txt    # Python dependencies
├── scoring_script.py       # Evaluation script
├── generate_data.py        # Data generator (organizers only)
├── leaderboard.md          # Competition leaderboard
├── LICENSE                 # License file
└── README.md               # This file
```

## Constraints & Tips

- **No external data**: Use only the provided dataset
- **Graph structure matters**: The baseline ignores graph topology - beat it by using GNNs!
- **Small but challenging**: The dataset is designed to be solvable with methods from DGL 1.1-4.6
- **F1-Score is tricky**: Imbalanced classes make this metric difficult to optimize

## Contributing

Submit your solutions via Pull Request. The GitHub Actions workflow will automatically score your submission and update the leaderboard.

Good luck! 🚀
