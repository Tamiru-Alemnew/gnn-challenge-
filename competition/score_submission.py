"""
The Cold Start Citation Challenge 2026
---------------------------------------
Script: Submission Scoring Engine
Description: Evaluates submissions against ground truth labels using F1-Score and Hit@K metrics.
Author: Competition Organizers

Usage:
    python score_submission.py <submission_path> <ground_truth_path>

Example:
    python score_submission.py \\
        submissions/inbox/team_alpha/run_001 \\
        data/private/test_labels.csv

Note:
    This script requires access to private/test_labels.csv (organizers only).
"""

import pandas as pd
import numpy as np
import sys
import json
from pathlib import Path
from typing import Dict, Tuple


class SubmissionScorer:
    """Scores a submission against ground truth labels."""
    
    def __init__(self, submission_path: Path, ground_truth_path: Path):
        self.submission_path = Path(submission_path)
        self.ground_truth_path = Path(ground_truth_path)
        self.results = {}
    
    def load_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Load predictions and ground truth."""
        pred_path = self.submission_path / "predictions.csv"
        if not pred_path.exists():
            raise FileNotFoundError(f"predictions.csv not found in {self.submission_path}")
        
        predictions = pd.read_csv(pred_path)
        
        if not self.ground_truth_path.exists():
            raise FileNotFoundError(f"Ground truth not found: {self.ground_truth_path}")
        
        ground_truth = pd.read_csv(self.ground_truth_path)
        
        return predictions, ground_truth
    
    def compute_metrics(self, predictions: pd.DataFrame, ground_truth: pd.DataFrame) -> Dict:
        """Compute evaluation metrics."""
        # Convert to sets of tuples for comparison
        pred_edges = set(zip(predictions['source'], predictions['target']))
        true_edges = set(zip(ground_truth['source'], ground_truth['target']))
        
        # Compute basic metrics
        true_positives = len(pred_edges & true_edges)
        false_positives = len(pred_edges - true_edges)
        false_negatives = len(true_edges - pred_edges)
        
        # Precision: Of predicted edges, how many are correct?
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
        
        # Recall: Of true edges, how many did we predict?
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0
        
        # F1-Score: Harmonic mean
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        
        # Compute Hit@K metrics (per-node accuracy)
        test_nodes = ground_truth['source'].unique()
        hits_at_k = {}
        
        for k in [1, 3, 5, 10]:
            hits = 0
            for node in test_nodes:
                # Get true edges for this node
                true_targets = set(ground_truth[ground_truth['source'] == node]['target'])
                
                # Get predicted edges for this node (top K if scored)
                node_preds = predictions[predictions['source'] == node]
                
                # Sort by score if available
                if 'score' in node_preds.columns:
                    node_preds = node_preds.sort_values('score', ascending=False)
                
                pred_targets = set(node_preds.head(k)['target'])
                
                # Check if any prediction is correct
                if len(pred_targets & true_targets) > 0:
                    hits += 1
            
            hits_at_k[f'hit@{k}'] = hits / len(test_nodes) if len(test_nodes) > 0 else 0.0
        
        metrics = {
            'true_positives': int(true_positives),
            'false_positives': int(false_positives),
            'false_negatives': int(false_negatives),
            'precision': float(precision),
            'recall': float(recall),
            'f1_score': float(f1_score),
            **hits_at_k,
            'num_predictions': len(predictions),
            'num_ground_truth': len(ground_truth),
            'num_test_nodes': len(test_nodes)
        }
        
        return metrics
    
    def check_one_submission_limit(self, team_name: str) -> None:
        """
        NeurIPS Requirement: Enforce one submission per team.
        Raises error if team_name already exists in leaderboard.
        """
        base_dir = Path(__file__).parent.parent
        leaderboard_path = base_dir / "leaderboard" / "leaderboard.csv"
        
        if leaderboard_path.exists():
            try:
                leaderboard = pd.read_csv(leaderboard_path)
                if 'team' in leaderboard.columns:
                    existing_teams = leaderboard['team'].str.lower().tolist()
                    if team_name.lower() in existing_teams:
                        raise ValueError(
                            f"SUBMISSION REJECTED: Team '{team_name}' has already submitted. "
                            f"NeurIPS Competition Policy: Only ONE submission per team is allowed."
                        )
            except pd.errors.EmptyDataError:
                # Empty leaderboard is fine
                pass
    
    def score(self) -> Dict:
        """Run scoring and return results."""
        # Load metadata first to get team_name
        meta_path = self.submission_path / "metadata.json"
        if meta_path.exists():
            with open(meta_path, 'r') as f:
                metadata = json.load(f)
        else:
            metadata = {}
        
        # NeurIPS Requirement 1: Check one-submission limit
        team_name = metadata.get('team_name', '')
        if team_name:
            self.check_one_submission_limit(team_name)
        
        # Proceed with scoring
        predictions, ground_truth = self.load_data()
        metrics = self.compute_metrics(predictions, ground_truth)
        
        self.results = {
            'submission_path': str(self.submission_path),
            'metrics': metrics,
            'metadata': metadata
        }
        
        return self.results
    
    def print_results(self):
        """Print formatted results."""
        if not self.results:
            print("No results to display. Run score() first.")
            return
        
        print("=" * 70)
        print("SUBMISSION SCORING RESULTS - Cold Start Citation Challenge 2026")
        print("=" * 70)
        
        if self.results.get('metadata'):
            meta = self.results['metadata']
            print("\n📋 Submission Metadata:")
            print(f"  Team: {meta.get('team_name', 'Unknown')}")
            print(f"  Method: {meta.get('method', 'Unknown')}")
            print(f"  Description: {meta.get('description', 'N/A')}")
        
        metrics = self.results['metrics']
        print("\n📊 Performance Metrics:")
        print(f"  Precision:  {metrics['precision']:.4f}")
        print(f"  Recall:     {metrics['recall']:.4f}")
        print(f"  F1-Score:   {metrics['f1_score']:.4f} ⭐")
        
        print("\n🎯 Hit@K Metrics:")
        print(f"  Hit@1:  {metrics['hit@1']:.4f}")
        print(f"  Hit@3:  {metrics['hit@3']:.4f}")
        print(f"  Hit@5:  {metrics['hit@5']:.4f}")
        print(f"  Hit@10: {metrics['hit@10']:.4f}")
        
        print("\n📈 Detailed Statistics:")
        print(f"  True Positives:  {metrics['true_positives']}")
        print(f"  False Positives: {metrics['false_positives']}")
        print(f"  False Negatives: {metrics['false_negatives']}")
        print(f"  Total Predictions: {metrics['num_predictions']}")
        print(f"  Total Ground Truth: {metrics['num_ground_truth']}")
        print(f"  Test Nodes: {metrics['num_test_nodes']}")
        
        print("\n" + "=" * 70)
        print(f"🏆 FINAL SCORE (F1): {metrics['f1_score']:.4f}")
        print("=" * 70)


def score_submission(submission_path: str, ground_truth_path: str) -> Dict:
    """Score a submission and print results."""
    scorer = SubmissionScorer(submission_path, ground_truth_path)
    results = scorer.score()
    scorer.print_results()
    
    return results


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python score_submission.py <submission_path> <ground_truth_path>")
        print()
        print("Example:")
        print("  python score_submission.py \\")
        print("    submissions/inbox/team_alpha/run_001 \\")
        print("    data/private/test_labels.csv")
        sys.exit(1)
    
    submission_path = sys.argv[1]
    ground_truth_path = sys.argv[2]
    
    try:
        results = score_submission(submission_path, ground_truth_path)
        
        # Save results to JSON
        results_path = Path(submission_path) / "results.json"
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Results saved to: {results_path}")
        
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        sys.exit(1)
