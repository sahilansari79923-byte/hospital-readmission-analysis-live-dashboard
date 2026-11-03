# Hospital Patient Readmission Analysis

> 🔗 **[Live Dashboard](https://sahilansari79923-byte.github.io/webpage/)**

<p align="center">
  <img src="https://raw.githubusercontent.com/sahilansari79923-byte/hospital-readmission-analysis-Predictive-Model/main/snaps/powerbi_dashboard.png" width="850"/>
</p>

## Project Overview

This project analyzes the factors contributing to the 30-day hospital readmission rate for diabetic patients. Utilizing a dataset of over 100,000 records from 130 US hospitals (1999–2008), the analysis processes raw clinical data through a complete pipeline—from Python and Excel cleaning to SQL exploratory analysis and Power BI visualization—to uncover trends related to demographics, treatments, and readmission risks.

---

## Key Insights

- **Overall Readmission Rate:** 8.84% (6,150 out of 69,560 cleaned records were readmitted within 30 days).
- **Age as a Predictor:** Readmission risk sharply increases after age 60. Patients in the 80–90 age bracket had a 10.36% readmission rate, which is more than double the rate for patients under 40.
- **Insulin Dosage Changes:** Patients whose insulin dosage was decreased had the highest readmission rate at 10.42%—higher than patients on no insulin at all (8.17%). A dose reduction often points to unstable glucose levels, leading to quick return visits.
- **Clinical Complexity:** Readmission risk scales consistently with the number of diagnoses and medications. Patients with 9+ diagnoses face a ~9.8% readmission rate (vs. 3.2% for a single diagnosis), and those taking 20+ medications have a 10.24% rate. This reflects the difficulty of discharge planning for highly complex medical profiles.

---

## Tools Used

- **Data Cleaning:** Python (Pandas, NumPy, Matplotlib, Seaborn), Microsoft Excel (Power Query, Pivot Tables)
- **Database & Analysis:** MySQL Workbench
- **Visualization:** Power BI Desktop
- **Web Deployment:** HTML, CSS, JavaScript (Live Dashboard)
- **IDE:** VS Code

---

## Dataset

**Source:** [UCI Machine Learning Repository — Diabetes 130-US Hospitals](https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008)

To replicate the project, download the CSV (~23MB) and place it in the `data/raw/` directory as `diabetic_data.csv`.

- **Size:** 101,766 rows, 50 columns
- **Missing Values:** Encoded as `?`
- **Target Column:** `readmitted` (Values: `NO`, `>30`, `<30`)

---

## Project Structure

```text
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
