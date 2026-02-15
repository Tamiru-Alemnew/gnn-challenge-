"""
The Cold Start Citation Challenge 2026
---------------------------------------
Script: Dataset Generator
Description: Generates the cold start inductive learning dataset using Barabási-Albert model.
Author: Competition Organizers

ORGANIZERS ONLY - Do not share this script with participants.

Usage:
    python make_dataset.py

Output:
    - data/public/train_graph.csv       (2690 edges between training nodes)
    - data/public/train_features.csv    (800×128 features)
    - data/public/test_features.csv     (200×128 features)
    - data/public/test_nodes.csv        (200 test node IDs)
    - data/private/test_labels.csv      (1147 ground truth edges)

Concept:
    Simulates a real-world scenario where NEW papers are published with NO citation history.
    Test nodes have zero edges in the training graph (cold start condition).
    
    Challenge: Predict which existing papers these new papers cite based on:
      1. Feature similarity (content-based)
      2. Graph structure of target nodes (structural patterns)
"""

import pandas as pd
import numpy as np
import networkx as nx
import os
from pathlib import Path

# Configuration
NUM_NODES = 1000
NUM_FEATURES = 128
TEST_RATIO = 0.2
RANDOM_SEED = 2026

np.random.seed(RANDOM_SEED)

print("=" * 70)
print("COLD START CITATION CHALLENGE 2026 - Dataset Generator")
print("=" * 70)

# Setup directories
base_dir = Path(__file__).parent.parent
public_dir = base_dir / "data" / "public"
private_dir = base_dir / "data" / "private"

public_dir.mkdir(parents=True, exist_ok=True)
private_dir.mkdir(parents=True, exist_ok=True)

# Generate synthetic citation network
# NeurIPS Requirement 6: Dataset Realism (Imbalance)
# Barabási-Albert model creates a "Long Tail" distribution:
# - Hub nodes (high degree) vs. outlier nodes (low degree)
# - This creates natural label imbalance in citation patterns
# - Some papers are highly cited (hubs), others rarely cited (tail)
# - Parameter m=4 controls attachment strength, creating realistic imbalance
print("\n[Step 1/5] Generating synthetic citation network...")
G = nx.barabasi_albert_graph(NUM_NODES, m=4, seed=RANDOM_SEED)
print(f"  ✓ Created graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
print(f"  ✓ Imbalance: Long-tail distribution (hubs vs. outliers) for realistic challenge")

# Generate node features
print("\n[Step 2/5] Generating node features...")
node_features = np.random.randn(NUM_NODES, NUM_FEATURES)
node_features = node_features / (np.linalg.norm(node_features, axis=1, keepdims=True) + 1e-10)
print(f"  ✓ Generated {NUM_FEATURES}-dimensional features for all nodes")

# Split into train/test (cold start split)
print("\n[Step 3/5] Splitting into train/test...")
all_nodes = np.arange(NUM_NODES)
np.random.shuffle(all_nodes)
num_test = int(NUM_NODES * TEST_RATIO)
test_nodes = set(all_nodes[:num_test])
train_nodes = set(all_nodes[num_test:])

print(f"  ✓ Training nodes: {len(train_nodes)}")
print(f"  ✓ Test nodes (cold start): {len(test_nodes)}")

# Mask edges and create splits
print("\n[Step 4/5] Masking edges and creating splits...")
all_edges = list(G.edges())
train_edges = []
test_edges = []
removed_edges = []

for u, v in all_edges:
    if u in test_nodes or v in test_nodes:
        removed_edges.append((u, v))
        if u in test_nodes and v in train_nodes:
            test_edges.append((u, v))
        elif v in test_nodes and u in train_nodes:
            test_edges.append((v, u))
    else:
        train_edges.append((u, v))

print(f"  ✓ Training edges: {len(train_edges)}")
print(f"  ✓ Test edges (ground truth): {len(test_edges)}")
print(f"  ✓ Total removed edges: {len(removed_edges)}")

# Save dataset files
print("\n[Step 5/5] Saving dataset files...")

# Save training graph
train_graph_df = pd.DataFrame(train_edges, columns=['source', 'target'])
train_graph_path = public_dir / "train_graph.csv"
train_graph_df.to_csv(train_graph_path, index=False)
print(f"  ✓ Saved: {train_graph_path}")

# Save training features
train_features_df = pd.DataFrame(
    node_features[list(train_nodes)],
    index=list(train_nodes)
)
train_features_df.index.name = 'node_id'
train_features_path = public_dir / "train_features.csv"
train_features_df.to_csv(train_features_path)
print(f"  ✓ Saved: {train_features_path}")

# Save test features
test_features_df = pd.DataFrame(
    node_features[list(test_nodes)],
    index=list(test_nodes)
)
test_features_df.index.name = 'node_id'
test_features_path = public_dir / "test_features.csv"
test_features_df.to_csv(test_features_path)
print(f"  ✓ Saved: {test_features_path}")

# Save test node IDs (public)
test_nodes_df = pd.DataFrame({'node_id': sorted(test_nodes)})
test_nodes_path = public_dir / "test_nodes.csv"
test_nodes_df.to_csv(test_nodes_path, index=False)
print(f"  ✓ Saved: {test_nodes_path}")

# Save ground truth labels (private)
test_labels_df = pd.DataFrame(test_edges, columns=['source', 'target'])
test_labels_df['label'] = 1
test_labels_path = private_dir / "test_labels.csv"
test_labels_df.to_csv(test_labels_path, index=False)
print(f"  ✓ Saved (PRIVATE): {test_labels_path}")

# Create README for private folder
private_readme = """# PRIVATE DATA - DO NOT COMMIT

This folder contains ground truth labels for the Cold Start Challenge.

Files:
- test_labels.csv: True citations from test nodes to train nodes

This file is used by the scoring script but should NEVER be made public.
"""
with open(private_dir / "README.md", "w") as f:
    f.write(private_readme)

print("\n" + "=" * 70)
print("Dataset generation complete!")
print("=" * 70)
print("\nPublic files (share with participants):")
print(f"  - {train_graph_path}")
print(f"  - {train_features_path}")
print(f"  - {test_features_path}")
print(f"  - {test_nodes_path}")
print("\nPrivate files (organizers only - DO NOT COMMIT):")
print(f"  - {test_labels_path}")
print("\nDataset Statistics:")
print(f"  - Total nodes: {NUM_NODES}")
print(f"  - Train nodes: {len(train_nodes)} ({(1-TEST_RATIO)*100:.0f}%)")
print(f"  - Test nodes: {len(test_nodes)} ({TEST_RATIO*100:.0f}%)")
print(f"  - Train edges: {len(train_edges)}")
print(f"  - Test edges to predict: {len(test_edges)}")
print(f"  - Feature dimension: {NUM_FEATURES}")
print("=" * 70)
