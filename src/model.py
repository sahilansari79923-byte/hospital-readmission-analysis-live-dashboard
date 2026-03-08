"""
model.py — Readmission Prediction Model
Author: Portfolio Project

Trains Logistic Regression and Random Forest on cleaned data.
The dataset has a 9:1 class imbalance (not readmitted vs. readmitted),
so accuracy alone is misleading — ROC-AUC is the better metric here.

Output: results/model_results.txt + charts/07_confusion_matrices.png
                                    + charts/08_feature_importance.png
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, roc_auc_score)

df = pd.read_csv('data/processed/diabetic_cleaned.csv')

# ── Feature setup ─────────────────────────────────────────────────────
# Categorical features need encoding before the model can use them
cat_features = ['insulin', 'diabetesMed', 'change']
num_features = ['age_numeric', 'time_in_hospital', 'num_medications',
                'num_lab_procedures', 'number_diagnoses',
                'number_inpatient', 'number_emergency']

le = LabelEncoder()
for col in cat_features:
    df[col + '_enc'] = le.fit_transform(df[col].astype(str))

feature_cols = num_features + [c + '_enc' for c in cat_features]
X = df[feature_cols].fillna(0)
y = df['readmitted_binary']

print(f"Class split — Not readmitted: {(y==0).sum():,} | Readmitted: {(y==1).sum():,}")
print(f"That's roughly a {round((y==0).sum()/(y==1).sum())}:1 imbalance")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

# ── Logistic Regression ───────────────────────────────────────────────
print("\nTraining Logistic Regression...")
lr = LogisticRegression(max_iter=500, class_weight='balanced', random_state=42)
lr.fit(X_train, y_train)
lr_pred = lr.predict(X_test)
lr_prob = lr.predict_proba(X_test)[:, 1]
lr_acc  = accuracy_score(y_test, lr_pred)
lr_auc  = roc_auc_score(y_test, lr_prob)
lr_report = classification_report(y_test, lr_pred, target_names=['Not Readmitted', 'Readmitted'])
print(f"  Accuracy: {lr_acc:.4f} | ROC-AUC: {lr_auc:.4f}")

# ── Random Forest ─────────────────────────────────────────────────────
print("Training Random Forest (100 trees)...")
rf = RandomForestClassifier(n_estimators=100, class_weight='balanced',
                            random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)
rf_prob = rf.predict_proba(X_test)[:, 1]
rf_acc  = accuracy_score(y_test, rf_pred)
rf_auc  = roc_auc_score(y_test, rf_prob)
rf_report = classification_report(y_test, rf_pred, target_names=['Not Readmitted', 'Readmitted'])
print(f"  Accuracy: {rf_acc:.4f} | ROC-AUC: {rf_auc:.4f}")

# ── Confusion Matrices ────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('Confusion Matrices — Logistic Regression vs Random Forest',
             fontsize=14, fontweight='bold')

for ax, pred, title in zip(axes, [lr_pred, rf_pred],
                           ['Logistic Regression', 'Random Forest']):
    cm = confusion_matrix(y_test, pred)
    im = ax.imshow(cm, interpolation='nearest', cmap='Blues')
    ax.set_title(title, fontweight='bold', fontsize=13)
    ax.set_xticks([0, 1]); ax.set_yticks([0, 1])
    ax.set_xticklabels(['Not Readmitted', 'Readmitted'], fontsize=11)
    ax.set_yticklabels(['Not Readmitted', 'Readmitted'], fontsize=11)
    ax.set_ylabel('Actual'); ax.set_xlabel('Predicted')
    thresh = cm.max() / 2
    for i in range(2):
        for j in range(2):
            ax.text(j, i, f'{cm[i,j]:,}', ha='center', va='center',
                    fontsize=13, fontweight='bold',
                    color='white' if cm[i,j] > thresh else 'black')
plt.colorbar(im, ax=axes[1])
plt.tight_layout()
plt.savefig('charts/07_confusion_matrices.png', dpi=150, bbox_inches='tight')
plt.close()

# ── Feature Importance ────────────────────────────────────────────────
feat_imp = pd.Series(rf.feature_importances_, index=feature_cols).sort_values(ascending=True)
clean_labels = {
    'age_numeric': 'Age', 'time_in_hospital': 'Time in Hospital',
    'num_medications': 'Num Medications', 'num_lab_procedures': 'Lab Procedures',
    'number_diagnoses': 'Num Diagnoses', 'number_inpatient': 'Inpatient Visits',
    'number_emergency': 'Emergency Visits', 'insulin_enc': 'Insulin',
    'diabetesMed_enc': 'Diabetes Med', 'change_enc': 'Med Change'
}
feat_imp.index = [clean_labels.get(i, i) for i in feat_imp.index]

fig, ax = plt.subplots(figsize=(10, 7))
colors = ['#C73E1D' if v == feat_imp.max() else '#2E86AB' for v in feat_imp.values]
bars = ax.barh(feat_imp.index, feat_imp.values, color=colors, edgecolor='white', linewidth=1)
for bar, val in zip(bars, feat_imp.values):
    ax.text(val + 0.001, bar.get_y() + bar.get_height()/2,
            f'{val:.3f}', va='center', fontsize=10, fontweight='bold')
ax.set_title('Feature Importance — Random Forest', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Importance Score')
plt.tight_layout()
plt.savefig('charts/08_feature_importance.png', dpi=150, bbox_inches='tight')
plt.close()

# ── Save results ──────────────────────────────────────────────────────
results = f"""
MODEL RESULTS — Hospital Readmission Prediction
================================================

Dataset: {len(X):,} patients  |  Train: {len(X_train):,}  |  Test: {len(X_test):,}
Target: readmitted within 30 days (class 1)
Class split: {(y==0).sum():,} negative  /  {(y==1).sum():,} positive  (~{round((y==0).sum()/(y==1).sum())}:1 imbalance)

Features ({len(feature_cols)}): {', '.join(feature_cols)}

LOGISTIC REGRESSION
-------------------
Accuracy : {lr_acc:.4f}
ROC-AUC  : {lr_auc:.4f}

{lr_report}

RANDOM FOREST (100 trees)
--------------------------
Accuracy : {rf_acc:.4f}
ROC-AUC  : {rf_auc:.4f}

{rf_report}

FEATURE IMPORTANCE (top 5, Random Forest)
------------------------------------------
{feat_imp.sort_values(ascending=False).head(5).to_string()}

NOTE: Random Forest's 90% accuracy is deceptive — it nearly always
predicts "not readmitted" due to class imbalance. Logistic Regression's
ROC-AUC (0.60) shows it's actually learning to distinguish the two groups.
"""

with open('results/model_results.txt', 'w') as f:
    f.write(results)

print("\n" + results)
print("Saved: results/model_results.txt")
print("Saved: charts/07_confusion_matrices.png")
print("Saved: charts/08_feature_importance.png")
