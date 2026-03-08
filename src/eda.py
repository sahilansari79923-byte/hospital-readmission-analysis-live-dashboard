"""
eda.py — Exploratory Data Analysis & Visualizations
Author: Portfolio Project

Generates 8 charts saved to charts/. Run after cleaning.py.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('data/processed/diabetic_cleaned.csv')
CHART_DIR = 'charts/'
sns.set_style("whitegrid")
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 12})

print("Generating charts...")

# ── 1. Readmission Distribution ───────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Patient Readmission Distribution', fontsize=16, fontweight='bold', y=1.02)

counts = df['readmitted'].value_counts()
bar_colors = ['#2E86AB', '#F18F01', '#C73E1D']

axes[0].bar(counts.index, counts.values, color=bar_colors, edgecolor='white', linewidth=1.5, width=0.6)
axes[0].set_title('Count by Category', fontweight='bold')
axes[0].set_xlabel('Readmission Status')
axes[0].set_ylabel('Patients')
for i, v in enumerate(counts.values):
    axes[0].text(i, v + 200, f'{v:,}', ha='center', fontweight='bold', fontsize=11)
axes[0].set_ylim(0, max(counts.values) * 1.12)

wedges, texts, autotexts = axes[1].pie(
    counts.values, labels=counts.index, autopct='%1.1f%%',
    colors=bar_colors, startangle=140,
    wedgeprops=dict(edgecolor='white', linewidth=2))
for at in autotexts:
    at.set_fontweight('bold')
axes[1].set_title('Readmission Share', fontweight='bold')

plt.tight_layout()
plt.savefig(CHART_DIR + '01_readmission_distribution.png', dpi=150, bbox_inches='tight')
plt.close()
print("  01_readmission_distribution.png")

# ── 2. Readmission Rate by Age Group ─────────────────────────────────
age_order = ['[0-10)', '[10-20)', '[20-30)', '[30-40)', '[40-50)',
             '[50-60)', '[60-70)', '[70-80)', '[80-90)', '[90-100)']
age_data = (df.groupby('age')['readmitted_binary'].mean() * 100).reindex(age_order)

fig, ax = plt.subplots(figsize=(13, 6))
bars = ax.bar(age_data.index, age_data.values, color='#2E86AB', edgecolor='white',
              linewidth=1.5, width=0.65)
max_val = age_data.max()
for bar, val in zip(bars, age_data.values):
    bar.set_color('#C73E1D' if val >= max_val * 0.97 else '#2E86AB')
    ax.text(bar.get_x() + bar.get_width() / 2, val + 0.1,
            f'{val:.1f}%', ha='center', fontsize=10, fontweight='bold')
ax.set_title('Readmission Rate by Age Group', fontsize=15, fontweight='bold', pad=15)
ax.set_xlabel('Age Group')
ax.set_ylabel('Readmission Rate (%)')
ax.set_ylim(0, age_data.max() * 1.2)
ax.tick_params(axis='x', rotation=30)
plt.tight_layout()
plt.savefig(CHART_DIR + '02_readmission_by_age.png', dpi=150, bbox_inches='tight')
plt.close()
print("  02_readmission_by_age.png")

# ── 3. Time in Hospital Boxplot ───────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6))
bp = ax.boxplot(
    [df[df['readmitted_binary'] == 0]['time_in_hospital'],
     df[df['readmitted_binary'] == 1]['time_in_hospital']],
    labels=['Not Readmitted', 'Readmitted (<30 days)'],
    patch_artist=True,
    medianprops=dict(color='white', linewidth=2.5),
    flierprops=dict(marker='o', markersize=3, alpha=0.4))
for patch, color in zip(bp['boxes'], ['#2E86AB', '#C73E1D']):
    patch.set_facecolor(color)
    patch.set_alpha(0.85)
means = [df[df['readmitted_binary'] == g]['time_in_hospital'].mean() for g in [0, 1]]
for i, mean in enumerate(means, 1):
    ax.annotate(f'Mean: {mean:.1f}d', xy=(i, mean), xytext=(i + 0.15, mean),
                fontsize=10, fontweight='bold')
ax.set_title('Time in Hospital: Readmitted vs Not', fontsize=14, fontweight='bold', pad=15)
ax.set_ylabel('Days in Hospital')
plt.tight_layout()
plt.savefig(CHART_DIR + '03_time_in_hospital_boxplot.png', dpi=150, bbox_inches='tight')
plt.close()
print("  03_time_in_hospital_boxplot.png")

# ── 4. Correlation Heatmap ────────────────────────────────────────────
num_cols = ['time_in_hospital', 'num_lab_procedures', 'num_procedures',
            'num_medications', 'number_outpatient', 'number_emergency',
            'number_inpatient', 'number_diagnoses', 'readmitted_binary', 'age_numeric']
corr = df[num_cols].corr()
mask = np.triu(np.ones_like(corr, dtype=bool))

fig, ax = plt.subplots(figsize=(12, 9))
sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r',
            center=0, vmin=-1, vmax=1, linewidths=0.5, linecolor='white',
            annot_kws={'size': 10, 'weight': 'bold'}, ax=ax, square=True)
ax.set_title('Correlation Heatmap — Numeric Features', fontsize=14, fontweight='bold', pad=15)
plt.xticks(rotation=35, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig(CHART_DIR + '04_correlation_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
print("  04_correlation_heatmap.png")

# ── 5. Readmission by Insulin ─────────────────────────────────────────
insulin_data = (df.groupby('insulin')['readmitted_binary'].mean() * 100).sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(10, 6))
bar_cols = ['#C73E1D' if v == insulin_data.max() else '#2E86AB' for v in insulin_data.values]
bars = ax.bar(insulin_data.index, insulin_data.values, color=bar_cols, edgecolor='white',
              linewidth=1.5, width=0.5)
for bar, val in zip(bars, insulin_data.values):
    ax.text(bar.get_x() + bar.get_width() / 2, val + 0.1,
            f'{val:.1f}%', ha='center', fontsize=11, fontweight='bold')
ax.set_title('Readmission Rate by Insulin Usage', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Insulin Dosage Change')
ax.set_ylabel('Readmission Rate (%)')
ax.set_ylim(0, insulin_data.max() * 1.2)
legend_elements = [mpatches.Patch(color='#C73E1D', label='Highest risk'),
                   mpatches.Patch(color='#2E86AB', label='Other groups')]
ax.legend(handles=legend_elements, loc='upper right')
plt.tight_layout()
plt.savefig(CHART_DIR + '05_readmission_by_insulin.png', dpi=150, bbox_inches='tight')
plt.close()
print("  05_readmission_by_insulin.png")

# ── 6. Medications Distribution ───────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Number of Medications Distribution', fontsize=15, fontweight='bold')

axes[0].hist(df['num_medications'], bins=30, color='#2E86AB', edgecolor='white', alpha=0.9)
axes[0].axvline(df['num_medications'].mean(), color='#C73E1D', linewidth=2.5,
                linestyle='--', label=f"Mean: {df['num_medications'].mean():.1f}")
axes[0].axvline(df['num_medications'].median(), color='#F18F01', linewidth=2.5,
                linestyle='--', label=f"Median: {df['num_medications'].median():.1f}")
axes[0].set_title('All Patients')
axes[0].set_xlabel('Number of Medications')
axes[0].set_ylabel('Count')
axes[0].legend()

for label, grp, color in [('Not Readmitted', df[df['readmitted_binary']==0], '#2E86AB'),
                            ('Readmitted', df[df['readmitted_binary']==1], '#C73E1D')]:
    axes[1].hist(grp['num_medications'], bins=30, alpha=0.65,
                 color=color, edgecolor='white', label=label, density=True)
axes[1].set_title('By Readmission Status')
axes[1].set_xlabel('Number of Medications')
axes[1].set_ylabel('Density')
axes[1].legend()

plt.tight_layout()
plt.savefig(CHART_DIR + '06_medications_distribution.png', dpi=150, bbox_inches='tight')
plt.close()
print("  06_medications_distribution.png")

print("\nAll charts saved to charts/")
