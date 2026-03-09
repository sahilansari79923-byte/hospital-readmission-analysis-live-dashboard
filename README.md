# Hospital Patient Readmission Analysis

> 🔗 **[Live Dashboard](https://sahilansari79923-byte.github.io/webpage/)**

A diabetic patient gets discharged. Within 30 days, they're back. Why? That's what this project digs into. The dataset covers 130 US hospitals from 1999–2008 — around 100,000 records, 50 columns.

Built as a portfolio project while switching into data analytics. Pipeline goes: raw data → cleaning (Python + Excel) → SQL queries → Power BI dashboard → charts.

---

## Project Structure

```
hospital-readmission-analysis/
│
├── data/
│   ├── raw/                        ← put diabetic_data.csv here
│   └── processed/
│       └── diabetic_cleaned.csv
│
├── src/
│   ├── cleaning.py / diabetic_cleaning.xlsx   ← Phase 1: data cleaning (Python / Excel)
│   └── eda.py                                 ← Phase 3: charts
│
├── sql/
│   └── queries.sql                 ← all 10 queries
│
├── dashboard/
│   └── readmission_dashboard.pbix  ← Power BI dashboard
│
├── charts/                         ← EDA output charts
│
├── report/
│   └── final_report.docx           ← business-style write-up
│
└── webpage/                        ← live dashboard source
```

---

## Dataset

**Source:** [UCI Machine Learning Repository — Diabetes 130-US Hospitals](https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008)

Download the CSV (~23MB) and drop it in `data/raw/diabetic_data.csv`.

- 101,766 rows, 50 columns
- Missing values encoded as `?`
- Target column: `readmitted` — values: `NO`, `>30`, `<30`

---

## How to Run

**Python cleaning + charts:**
```bash
python src/cleaning.py     # outputs data/processed/diabetic_cleaned.csv
python src/eda.py          # saves charts to charts/
```

**Excel cleaning:**
1. Open `excel/diabetic_cleaning.xlsx`
2. The workbook walks through each cleaning step with documented formulas and Power Query
3. Final sheet exports to `diabetic_cleaned.csv`

**SQL (MySQL Workbench):**
1. Open MySQL Workbench and connect to your local server
2. Create a schema (e.g. `hospital_db`)
3. Import `diabetic_cleaned.csv` — right-click schema → *Table Data Import Wizard*
4. Open `sql/queries.sql` and run the queries

**Power BI:**
1. Open `dashboard/readmission_dashboard.pbix` in Power BI Desktop
2. Update the data source path to your local `diabetic_cleaned.csv`
3. Refresh

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

## Power BI Dashboard

<p align="center">
  <img src="https://raw.githubusercontent.com/sahilansari79923-byte/hospital-readmission-analysis-Predictive-Model/main/snaps/powerbi_dashboard.png" width="850"/>
</p>

---

## What I Found

**Overall readmission rate: 8.84%** — 6,150 out of 69,560 cleaned records were readmitted within 30 days.

Age is a big factor. Patients in the 80–90 bracket had a 10.36% readmission rate, more than double those under 40. The jump gets sharp after 60.

Insulin dosage changes stood out. Patients whose insulin was *decreased* had the highest readmission rate at 10.42% — higher than patients on no insulin at all (8.17%). A dose reduction that doesn't hold means unstable glucose, and unstable glucose means a quick return trip.

More diagnoses means higher risk, pretty consistently. Patients with 9+ diagnoses had a ~9.8% readmission rate versus 3.2% for those with just one. The more conditions someone's managing, the harder clean discharge planning gets.

High medication counts follow the same pattern. 20+ medications: 10.24% readmission rate. Fewer than 10: 7.04%. Probably reflects clinical complexity more than the drugs themselves.

---

## Limitations

A1Cresult and max_glu_serum got dropped because over 40% of values were missing. For a diabetic readmission study, those are arguably the two most clinically relevant features — losing them hurts the analysis. The 91:9 class imbalance in readmission vs non-readmission is the other issue, and worth keeping in mind when reading any rates.

---

## Tools Used

- Python (Pandas, NumPy, Matplotlib, Seaborn)
- Microsoft Excel (Power Query, pivot tables)
- MySQL Workbench
- Power BI Desktop
- HTML, CSS, JavaScript (live dashboard)
- VS Code
