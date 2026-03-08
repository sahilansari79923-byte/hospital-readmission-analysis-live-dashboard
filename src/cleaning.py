"""
cleaning.py — Data Cleaning for Diabetic Readmission Dataset
Author: Portfolio Project

The raw data uses '?' for missing values instead of NaN, has duplicate
patient records (multiple hospital encounters per patient), and three
columns that are mostly empty. This script handles all of that.

Output: data/processed/diabetic_cleaned.csv
"""

import pandas as pd
import numpy as np

# ── Load ──────────────────────────────────────────────────────────────
df = pd.read_csv('data/raw/diabetic_data.csv')
print(f"Loaded {len(df):,} rows, {df.shape[1]} columns")

# ── Fix missing values ────────────────────────────────────────────────
# The dataset encodes missing as '?' across all string columns
df.replace('?', np.nan, inplace=True)

# ── Drop high-missing columns ─────────────────────────────────────────
# weight (97% missing), payer_code (40%), medical_specialty (49%)
# max_glu_serum and A1Cresult also exceed 40% — dropped too
threshold = 0.40 * len(df)
drop_cols = [c for c in df.columns if df[c].isna().sum() > threshold]
print(f"Dropping columns >40% missing: {drop_cols}")
df.drop(columns=drop_cols, inplace=True)

# ── One encounter per patient ─────────────────────────────────────────
# Some patients appear multiple times across different visits.
# Keeping the first encounter avoids data leakage in the model.
before = len(df)
df.drop_duplicates(subset='patient_nbr', keep='first', inplace=True)
print(f"Removed {before - len(df):,} duplicate patient records")

# ── Drop rows missing critical fields ─────────────────────────────────
df.dropna(subset=['race', 'diag_1'], inplace=True)

# ── Binary target variable ────────────────────────────────────────────
# Original 'readmitted' has three values: NO, >30, <30
# We care about early readmission (<30 days) = 1, everything else = 0
df['readmitted_binary'] = (df['readmitted'] == '<30').astype(int)
print(f"High-risk readmissions (<30 days): {df['readmitted_binary'].sum():,}")

# ── Numeric age for modeling ──────────────────────────────────────────
# Age comes as brackets like '[60-70)' — mapped to midpoints
age_map = {
    '[0-10)': 5, '[10-20)': 15, '[20-30)': 25, '[30-40)': 35,
    '[40-50)': 45, '[50-60)': 55, '[60-70)': 65, '[70-80)': 75,
    '[80-90)': 85, '[90-100)': 95
}
df['age_numeric'] = df['age'].map(age_map)

# ── Summary ───────────────────────────────────────────────────────────
print(f"\nFinal shape: {df.shape}")
print(f"\nReadmission breakdown:\n{df['readmitted'].value_counts()}")

df.to_csv('data/processed/diabetic_cleaned.csv', index=False)
print("\nSaved: data/processed/diabetic_cleaned.csv")
