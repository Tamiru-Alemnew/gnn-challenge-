import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
import os

# Create submissions folder if it doesn't exist
os.makedirs("../submissions", exist_ok=True)

# 1. Load data
print("Loading data...")
try:
    train = pd.read_csv('../data/train.csv')
except FileNotFoundError:
    print("Error: ../data/train.csv not found. Please ensure data files are generated.")
    exit(1)

# Drop ID columns for the baseline (Random Forest doesn't know how to use graph structure)
# It will only rely on 'feature_similarity'
X = train.drop(['target', 'node_u', 'node_v'], axis=1)
y = train['target']

# 2. Split into train / validation
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Train a baseline model
print("Training Random Forest...")
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# 4. Evaluate
y_pred = clf.predict(X_val)
score = f1_score(y_val, y_pred, average='macro')
print(f'Validation F1 Score: {score:.4f}')

# 5. Make predictions on test set
try:
    test = pd.read_csv('../data/test.csv')
except FileNotFoundError:
    print("Error: ../data/test.csv not found. Please ensure data files are generated.")
    exit(1)
X_test = test.drop(['node_u', 'node_v'], axis=1) # Drop IDs again
test_preds = clf.predict(X_test)

# Save submission
submission = pd.DataFrame({'target': test_preds})
submission.to_csv('../submissions/sample_submission.csv', index=False)
print("Saved prediction to ../submissions/sample_submission.csv")

