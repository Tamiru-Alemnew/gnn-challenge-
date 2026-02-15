# The Cold Start Citation Challenge 2026

> **Can AI predict citations for a paper that doesn't exist yet?**

A novel graph learning competition exploring inductive reasoning on citation networks.

---

## 🎯 Overview

Welcome to the **Cold Start Citation Challenge 2026** — a research competition that tests the limits of machine learning on **inductive graph problems**.

Traditional graph neural networks excel when all nodes are known during training. But what happens when a completely new node appears? This competition simulates the real-world challenge faced by academic search engines: recommending citations for newly published papers with **zero citation history**.

**The Challenge**: Given a citation network of 800 papers, predict which papers 200 brand-new papers will cite using only their abstract embeddings and the structure of the existing graph.

---

## 🧠 The Problem: Inductive Cold Start Learning

### The Cold Start Scenario

In production recommender systems, new items appear constantly:
- New papers on ArXiv
- New products on e-commerce sites  
- New users on social networks

Unlike traditional **transductive** graph learning (where all nodes are known), this competition requires **inductive** methods that generalize to completely unseen nodes.

### Your Task

**Input**:
- Training citation graph: 800 papers with 2,690 citation edges
- Training features: 128-dimensional embeddings for each training paper
- Test features: 128-dimensional embeddings for 200 NEW papers (not in the graph)

**Output**:
- Predicted citation edges: Which existing papers should each new paper cite?

**Constraint**: Test papers have **zero edges** in the training graph. This is the "cold start" condition.

---

## 📊 The Dataset

Located in `data/public/`:

| File | Description | Size |
|------|-------------|------|
| `train_graph.csv` | Citation edges (source → target) | 2,690 edges |
| `train_features.csv` | Feature vectors for training papers | 800 × 128 |
| `test_features.csv` | Feature vectors for test papers | 200 × 128 |
| `test_nodes.csv` | Test node IDs to generate predictions for | 200 nodes |

### Graph Specification

Following NeurIPS competition standards, we explicitly provide:

- **Adjacency Matrix ($A_{train}$)**: `train_graph.csv` contains the training graph adjacency structure as edge list (source, target pairs). This represents the citation network topology among training papers.

- **Node Feature Matrix ($X_{train}$)**: `train_features.csv` contains 128-dimensional feature vectors for each training node. These simulate abstract embeddings (e.g., from SciBERT, Sentence-BERT).

- **Target Node Features ($X_{test}$)**: `test_features.csv` contains 128-dimensional feature vectors for test nodes (new papers). These nodes have **zero edges** in $A_{train}$ (cold start condition).

**Graph Model**: Generated using the Barabási–Albert model to mimic real citation networks with preferential attachment, creating realistic long-tail degree distributions (hubs vs. outliers).

---

## 🚀 Getting Started

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/your-org/gnn-challenge.git
cd gnn-challenge

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Baseline

```bash
cd starter_code
python baseline_inductive.py
```

The baseline uses content-based similarity + graph structure propagation, achieving **F1-Score: 0.0076**. Your goal: beat this baseline using advanced GNN techniques!

### 3. Build Your Solution

**Recommended Approaches**:
- **GraphSAGE**: Inductive learning via neighborhood sampling
- **Graph Attention Networks (GAT)**: Learn attention weights for aggregation
- **Graph Isomorphism Network (GIN)**: Powerful message passing
- **Meta-learning**: Few-shot adaptation to new nodes
- **Transfer learning**: Pre-train on full graph, fine-tune inductively

**Key Insight**: You cannot use transductive methods (Node2Vec, DeepWalk) as they require all nodes during training.

### 4. Submit Your Solution

Create your submission following this structure:

```
submissions/inbox/<your_team_name>/<run_id>/
├── predictions.csv       # Your predictions
└── metadata.json         # Submission metadata
```

**predictions.csv**:
```csv
source,target,score
801,42,0.95
801,156,0.87
802,13,0.91
...
```

**metadata.json**:
```json
{
  "team_name": "your_team",
  "method": "human|llm|hybrid",
  "description": "Brief description of your approach"
}
```

Validate your submission:
```bash
python competition/validate_submission.py submissions/inbox/your_team/run_001
```

Submit via **Pull Request** to the `main` branch. GitHub Actions will automatically score your submission and update the leaderboard.

---

## 📈 Evaluation

### Primary Metric: F1-Score

```
Precision = TP / (TP + FP)
Recall = TP / (TP + FN)
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

**F1-Score** balances precision (are your predictions correct?) with recall (did you find the true citations?).

### Secondary Metrics: Hit@K

- **Hit@1**: Percentage of test nodes with at least 1 correct prediction in top-1
- **Hit@5**: Percentage of test nodes with at least 1 correct prediction in top-5
- **Hit@10**: Percentage of test nodes with at least 1 correct prediction in top-10

---

## 🏆 Leaderboard

View the live leaderboard at: [https://your-org.github.io/gnn-challenge](https://your-org.github.io/gnn-challenge)

Current standings are also tracked in `leaderboard/leaderboard.csv`.

**Baseline Performance**:
- F1-Score: 0.0076
- Hit@5: 0.0200 (2%)
- Hit@10: 0.0500 (5%)

---

## 📋 Competition Timeline

- **Start Date**: February 5, 2026
- **End Date**: TBD
- **Submission Deadline**: TBD
- **Winner Announcement**: TBD

---

## 📜 Rules & Limitations

### Competition Rules

1. **One Submission Per Team**: NeurIPS policy - each team is allowed **ONLY ONE** submission attempt. Duplicate submissions will be rejected.

2. **No External Data**: Use only the provided dataset

3. **No Test Leakage**: Do not access `data/private/test_labels.csv`

4. **Inductive Methods Only**: Your model must generalize to unseen nodes

5. **Single Training Run**: Each submission must be from a single reproducible training run

6. **Honest Method Reporting**: Accurately label your approach as `human`, `llm`, or `hybrid`

7. **Submission Privacy**: Private submissions (predictions.csv, metadata.json) are not made public. Only final scores and ranks appear on the leaderboard.

**Violations**: Submissions violating these rules will be disqualified.

### Resource Limitations

**Runtime Limit**: Training must complete within **3 hours on a standard CPU**. This ensures fair competition and prevents excessive computational requirements.

**LLM Policy**: You may use LLMs for coding assistance, but **not** for:
- Generating the dataset
- Defining the task/problem formulation
- Creating synthetic data

LLMs are permitted for:
- Code generation and debugging
- Algorithm implementation
- Documentation and comments

---

## 🤝 Human vs. LLM Research

This competition is part of a research initiative studying:
- Can LLMs generate competitive graph learning solutions?
- How do LLM-generated approaches differ from human-coded solutions?
- What is the quality gap between human and AI-generated code?

Your `metadata.json` helps us analyze these questions. Please be honest about your method!

---

## 💡 Tips for Success

### Why the Baseline is Weak

The baseline only uses:
- Cosine similarity between features
- First-order graph structure (direct neighbors)

It ignores:
- Higher-order graph structure (2-hop, 3-hop)
- Learnable embeddings
- Advanced message passing

### Winning Strategies

✅ **Use Inductive GNNs**: GraphSAGE, GAT, GIN  
✅ **Leverage Features**: The 128-dim vectors contain semantic information  
✅ **Multi-hop Reasoning**: Look beyond immediate neighbors  
✅ **Negative Sampling**: Learn what NOT to cite  
✅ **Ensemble Methods**: Combine multiple approaches  

❌ **Avoid Transductive Methods**: Node2Vec, DeepWalk won't work  
❌ **Don't Ignore Features**: Pure structure-based methods will fail  

---

## 📚 Resources

**Papers**:
- [Inductive Representation Learning on Large Graphs (Hamilton et al., 2017)](https://arxiv.org/abs/1706.02216) - GraphSAGE
- [Graph Attention Networks (Veličković et al., 2018)](https://arxiv.org/abs/1710.10903) - GAT
- [How Powerful are Graph Neural Networks? (Xu et al., 2019)](https://arxiv.org/abs/1810.00826) - GIN

**Libraries**:
- [PyTorch Geometric](https://pytorch-geometric.readthedocs.io/)
- [DGL (Deep Graph Library)](https://www.dgl.ai/)
- [NetworkX](https://networkx.org/)

---

## 🔧 For Organizers

See `organizer_tools/README.md` for dataset generation and scoring utilities.

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-org/gnn-challenge/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/gnn-challenge/discussions)
- **Email**: 

---

## 📄 License

This competition is released under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

This competition uses synthetic data generated with NetworkX. The cold start formulation is inspired by real-world challenges in academic recommendation systems.

---

**Good luck, and happy graph learning! 🚀**

*"The true test of a model is not what it knows, but how it adapts to what it doesn't know."*
