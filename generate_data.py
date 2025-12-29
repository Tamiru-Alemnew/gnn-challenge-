import pandas as pd
import numpy as np
import networkx as nx
import os
from sklearn.model_selection import train_test_split

# 1. Setup
NUM_NODES = 500
NUM_FEATURES = 16  # Small feature vectors
os.makedirs("data", exist_ok=True)
os.makedirs("submissions", exist_ok=True)

print("Generating synthetic Citation Network...")

# 2. Generate Graph (Barabasi-Albert model mimics citation networks)
G = nx.barabasi_albert_graph(NUM_NODES, 3)
node_features = np.random.rand(NUM_NODES, NUM_FEATURES)

# 3. Create Edge Dataset (Link Prediction)
# We need Positive edges (citations) and Negative edges (no citation)
pos_edges = list(G.edges())
# Generate equal number of fake edges
neg_edges = []
while len(neg_edges) < len(pos_edges):
    u, v = np.random.randint(0, NUM_NODES, 2)
    if not G.has_edge(u, v) and u != v:
        neg_edges.append((u, v))

# Combine and label
all_pairs = pos_edges + neg_edges
labels = [1] * len(pos_edges) + [0] * len(neg_edges)

# 4. Create DataFrame
data = []
for (u, v), label in zip(all_pairs, labels):
    # We include simple features like "feature similarity" 
    # This gives the Random Forest something to look at, but GNNs will do better.
    feat_sim = np.dot(node_features[u], node_features[v])
    
    row = {
        "node_u": u,
        "node_v": v,
        "feature_similarity": feat_sim,  # A hint for the baseline
        "target": label
    }
    data.append(row)

df = pd.DataFrame(data)

# 5. Split Data (Train / Test)
train_df, test_df = train_test_split(df, test_size=0.3, random_state=42)

# Save Train (with Target)
train_df.to_csv("data/train.csv", index=False)

# Save Test (Features only) & Hidden Truth
test_labels = test_df[["target"]].copy()  # The hidden answers
test_features = test_df.drop(columns=["target"]) # The puzzle

test_features.to_csv("data/test.csv", index=False)
test_labels.to_csv("data/test_labels.csv", index=False)

print(f"Done! Created data/train.csv ({len(train_df)} rows) and data/test.csv ({len(test_df)} rows).")