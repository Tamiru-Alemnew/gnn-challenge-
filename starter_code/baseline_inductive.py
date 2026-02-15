"""
The Cold Start Citation Challenge 2026
---------------------------------------
Script: Inductive Baseline Solution
Description: Simple baseline using content-based similarity and graph structure.
             Demonstrates how to approach the cold start problem without deep learning.
Author: Competition Organizers

Usage:
    python baseline_inductive.py

Output:
    Creates submission folder: submissions/inbox/baseline_team/run_001/
    - predictions.csv: Predicted citation edges
    - metadata.json: Submission metadata
"""

import pandas as pd
import numpy as np
import networkx as nx
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
import json
import os

# Configuration
TOP_K_SIMILAR = 20  # Number of similar train nodes to consider
TOP_K_CITATIONS = 10  # Maximum citations per test node to predict
SIMILARITY_THRESHOLD = 0.1  # Minimum similarity to consider

# Paths
base_dir = Path(__file__).parent.parent
data_dir = base_dir / "data" / "public"

print("=" * 70)
print("COLD START CITATION CHALLENGE - Baseline Inductive Model")
print("=" * 70)

# Load data
print("\n[Step 1/4] Loading data...")
train_graph = pd.read_csv(data_dir / "train_graph.csv")
print(f"  ✓ Loaded training graph: {len(train_graph)} edges")

test_nodes_df = pd.read_csv(data_dir / "test_nodes.csv")
test_node_ids = test_nodes_df['node_id'].tolist()
print(f"  ✓ Loaded test node IDs: {len(test_node_ids)} nodes")

train_features = pd.read_csv(data_dir / "train_features.csv", index_col='node_id')
test_features = pd.read_csv(data_dir / "test_features.csv", index_col='node_id')
print(f"  ✓ Loaded train features: {len(train_features)} nodes")
print(f"  ✓ Loaded test features: {len(test_features)} nodes")

# Verify test node IDs match
assert set(test_node_ids) == set(test_features.index), "Test node ID mismatch!"

# Build graph structure
G = nx.DiGraph()
G.add_edges_from(train_graph[['source', 'target']].values)
print(f"  ✓ Built graph structure")

# Compute feature similarity
print("\n[Step 2/4] Computing feature similarity...")
test_ids = test_node_ids
train_ids = train_features.index.tolist()

test_features_ordered = test_features.loc[test_ids]
similarity_matrix = cosine_similarity(test_features_ordered.values, train_features.values)
print(f"  ✓ Computed similarity matrix: {similarity_matrix.shape}")

# Generate predictions using graph structure
print("\n[Step 3/4] Generating predictions using graph structure...")
predictions = []

for i, test_node in enumerate(test_ids):
    # Find most similar training nodes
    similarities = similarity_matrix[i]
    
    # Get top-K similar nodes
    top_k_indices = np.argsort(similarities)[-TOP_K_SIMILAR:][::-1]
    similar_nodes = [(train_ids[idx], similarities[idx]) for idx in top_k_indices]
    
    # Aggregate citations from similar nodes
    citation_scores = {}
    
    for similar_node, sim_score in similar_nodes:
        if sim_score < SIMILARITY_THRESHOLD:
            continue
        
        # Get what this similar node cites
        if similar_node in G:
            for cited_node in G.successors(similar_node):
                if cited_node not in citation_scores:
                    citation_scores[cited_node] = 0
                citation_scores[cited_node] += sim_score
    
    # Rank and select top citations
    if citation_scores:
        top_citations = sorted(citation_scores.items(), key=lambda x: x[1], reverse=True)[:TOP_K_CITATIONS]
        
        for cited_node, score in top_citations:
            predictions.append({
                'source': test_node,
                'target': cited_node,
                'score': score
            })
    
    if (i + 1) % 20 == 0:
        print(f"  Progress: {i + 1}/{len(test_ids)} test nodes processed")

print(f"  ✓ Generated {len(predictions)} predictions")

# Save submission
print("\n[Step 4/4] Saving submission...")
team_name = "baseline_team"
run_id = "run_001"
submission_dir = base_dir / "submissions" / "inbox" / team_name / run_id
submission_dir.mkdir(parents=True, exist_ok=True)

# Save predictions
predictions_df = pd.DataFrame(predictions)
predictions_path = submission_dir / "predictions.csv"
predictions_df.to_csv(predictions_path, index=False)
print(f"  ✓ Saved predictions: {predictions_path}")

# Create metadata
metadata = {
    "team_name": team_name,
    "method": "hybrid",
    "description": "Baseline using content-based similarity + graph structure propagation",
    "model_type": "content_based_with_structure",
    "parameters": {
        "top_k_similar": TOP_K_SIMILAR,
        "top_k_citations": TOP_K_CITATIONS,
        "similarity_threshold": SIMILARITY_THRESHOLD
    }
}

metadata_path = submission_dir / "metadata.json"
with open(metadata_path, 'w') as f:
    json.dump(metadata, f, indent=2)
print(f"  ✓ Saved metadata: {metadata_path}")

print("\n" + "=" * 70)
print("Baseline submission complete!")
print("=" * 70)
print(f"\nSubmission location: {submission_dir}")
print(f"  - predictions.csv: {len(predictions)} predicted edges")
print(f"  - metadata.json: submission metadata")
print("\nTo submit, copy this folder structure and create a Pull Request.")
print("=" * 70)
