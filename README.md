# Hospital Patient Readmission Analysis

> 🔗 **[Live Dashboard →](https://sahilansari79923-byte.github.io/webpage/)**


A diabetic patient gets discharged. Within 30 days, they're back. Why? That's what this project digs into. The dataset covers 130 US hospitals from 1999–2008 — around 100,000 records, 50 columns.

Built as a portfolio project while switching into data analytics. Pipeline goes: raw data → cleaning → SQL queries → charts → trained classifier.


---

## Project structure

```
hospital-readmission-analysis/
│
├── data/
│   ├── raw/                    ← put diabetic_data.csv here
│   └── processed/
│       └── diabetic_cleaned.csv
│
├── src/
│   ├── cleaning.py             ← Phase 1: data cleaning
│   ├── eda.py                  ← Phase 3: charts
│   └── model.py                ← Phase 4: ML models
│
├── sql/
│   └── queries.sql             ← all 10 queries
│
├── results/
│   └── model_results.txt       ← accuracy, ROC-AUC, classification reports
│
├── report/
│   └── final_report.docx       ← business-style write-up
│
└── requirements.txt
```

---

## Dataset

**Source:** [UCI Machine Learning Repository — Diabetes 130-US Hospitals](https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008)

Download the CSV (~23MB) from the link above and drop it in `data/raw/diabetic_data.csv`.

- 101,766 rows, 50 columns
- Missing values encoded as `?`
- Target column: `readmitted` — values: `NO`, `>30`, `<30`

---

## How to run it

Open the project folder in VS Code and run each script in order from the terminal:

```bash
python src/cleaning.py     # outputs data/processed/diabetic_cleaned.csv
python src/eda.py          # saves charts to charts/
python src/model.py        # trains models, saves results/model_results.txt
```

**For SQL (MySQL Workbench):**
1. Open MySQL Workbench and connect to your local server
2. Create a new schema (e.g. `hospital_db`)
3. Import `diabetic_cleaned.csv` — right-click the schema → *Table Data Import Wizard*
4. Open `sql/queries.sql` in Workbench and run the queries directly

Each script prints what it's doing as it runs.

---


## SQL Query Results

<table>
  <tr>
    <td align="center"><b>1. Overall Readmission Rate</b><br><img src="https://raw.githubusercontent.com/sahilansari79923-byte/hospital-readmission-analysis-Predictive-Model/main/snaps/overall%20readmission%20rate.png" width="400"/></td>
    <td align="center"><b>2. Readmission Rate by Age Group</b><br><img src="https://raw.githubusercontent.com/sahilansari79923-byte/hospital-readmission-analysis-Predictive-Model/main/snaps/readmission%20rate%20by%20age%20group.png" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><b>3. Readmission Rate by Race</b><br><img src="https://raw.githubusercontent.com/sahilansari79923-byte/hospital-readmission-analysis-Predictive-Model/main/snaps/readmission%20rate%20by%20race.png" width="400"/></td>
    <td align="center"><b>4. Readmission Rate by Gender</b><br><img src="https://raw.githubusercontent.com/sahilansari79923-byte/hospital-readmission-analysis-Predictive-Model/main/snaps/readmission%20rate%20by%20gender.png" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><b>5. Average Hospital Stay — Readmitted vs Not</b><br><img src="https://raw.githubusercontent.com/sahilansari79923-byte/hospital-readmission-analysis-Predictive-Model/main/snaps/average%20hospital%20stay-%20readmission%20or%20not.png" width="400"/></td>
    <td align="center"><b>6. Impact of Insulin Dosage Change on Readmission</b><br><img src="https://raw.githubusercontent.com/sahilansari79923-byte/hospital-readmission-analysis-Predictive-Model/main/snaps/impact%20of%20insulin%20doasage%20change%20on%20readmission.png" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><b>7. Impact of Diabetes Medication on Readmission</b><br><img src="https://raw.githubusercontent.com/sahilansari79923-byte/hospital-readmission-analysis-Predictive-Model/main/snaps/impact%20of%20diabetes%20medication%20(onoff)%20on%20readmission.png" width="400"/></td>
    <td align="center"><b>8. Readmission by Number of Diagnoses</b><br><img src="https://raw.githubusercontent.com/sahilansari79923-byte/hospital-readmission-analysis-Predictive-Model/main/snaps/readmission%20by%20number%20of%20diagnostics.png" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><b>9. Readmission by Medication Count Group</b><br><img src="https://raw.githubusercontent.com/sahilansari79923-byte/hospital-readmission-analysis-Predictive-Model/main/snaps/readmission%20by%20medication%20count%20group.png" width="400"/></td>
    <td align="center"><b>10. Readmission by Lab Procedures</b><br><img src="https://raw.githubusercontent.com/sahilansari79923-byte/hospital-readmission-analysis-Predictive-Model/main/snaps/readmission%20by%20lab%20procedure.png" width="400"/></td>
  </tr>
</table>

---

## What I found

**Overall readmission rate: 8.84%** — 6,150 out of 69,560 cleaned records were readmitted within 30 days.

Age is a big factor. Patients in the 80–90 bracket had a 10.36% readmission rate, more than double those under 40. Mostly expected, but the jump is sharp after 60.

Insulin dosage changes stood out more. Patients whose insulin was *decreased* had the highest readmission rate at 10.42% — higher than patients on no insulin at all (8.17%). A dose reduction that goes wrong means unstable glucose, and unstable glucose means a quick return trip.

More diagnoses means higher risk, pretty consistently. Patients with 9+ diagnoses had a ~9.8% readmission rate versus 3.2% for those with just one. The more conditions someone's managing, the harder clean discharge planning gets.

High medication counts follow the same pattern. 20+ medications: 10.24% readmission rate. Fewer than 10: 7.04%. Probably reflects clinical complexity more than the drugs themselves.

---

## Model results

Two models trained: Logistic Regression and Random Forest. Both used `class_weight='balanced'` because the data is roughly 9:1 imbalanced.

| Model | Accuracy | ROC-AUC |
|---|---|---|
| Logistic Regression | 61.2% | 0.602 |
| Random Forest | 90.7% | 0.554 |

Random Forest's 90% accuracy is a trap — it mostly just predicts "not readmitted" for everyone and coasts on class imbalance. Logistic Regression has the higher ROC-AUC (0.602 vs 0.554), which means it's actually doing a better job separating the two groups despite the lower headline number.

**Top 5 features (Random Forest):**
1. Number of lab procedures — 0.319
2. Number of medications — 0.236
3. Time in hospital — 0.120
4. Age — 0.094
5. Number of diagnoses — 0.089

---

## Limitations

A1Cresult and max_glu_serum got dropped because over 40% of values were missing. For a *diabetic* readmission study, those are arguably the two most clinically meaningful features — so losing them genuinely hurts the model. The 91:9 class imbalance is the other issue. SMOTE or similar resampling would likely improve recall on the minority class. That's what I'd try next.

---

## Tools used

- Python (Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn)
- MySQL Workbench (for SQL analysis)
- HTML, CSS, JavaScript (for the live dashboard)
- VS Code

---

## Dashboard Preview

[![Dashboard Preview](https://github.com/sahilansari79923-byte/hospital-readmission-analysis-Predictive-Model/blob/main/snaps/Dashboard_snap.png)
