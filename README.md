# Hospital Patient Readmission Analysis

> 🔗 **[Live Dashboard](https://sahilansari79923-byte.github.io/webpage/)**

<p align="center">
  <img src="https://raw.githubusercontent.com/sahilansari79923-byte/hospital-readmission-analysis-Predictive-Model/main/snaps/powerbi_dashboard.png" width="850"/>
</p>

## Project Overview

This project analyzes the factors contributing to the 30-day hospital readmission rate for diabetic patients. Utilizing a dataset of over 100,000 records from 130 US hospitals (1999–2008), the analysis processes raw clinical data through a complete pipeline—from Python and Excel cleaning to SQL exploratory analysis and Power BI visualization—to uncover trends related to demographics, treatments, and readmission risks.

## Key Insights

- **Overall Readmission Rate:** 8.84% (6,150 out of 69,560 cleaned records were readmitted within 30 days).
- **Age as a Predictor:** Readmission risk sharply increases after age 60. Patients in the 80–90 age bracket had a 10.36% readmission rate, which is more than double the rate for patients under 40.
- **Insulin Dosage Changes:** Patients whose insulin dosage was decreased had the highest readmission rate at 10.42%—higher than patients on no insulin at all (8.17%). A dose reduction often points to unstable glucose levels, leading to quick return visits.
- **Clinical Complexity:** Readmission risk scales consistently with the number of diagnoses and medications. Patients with 9+ diagnoses face a ~9.8% readmission rate (vs. 3.2% for a single diagnosis), and those taking 20+ medications have a 10.24% rate. This reflects the difficulty of discharge planning for highly complex medical profiles.

## Tools Used

- **Data Cleaning & EDA:** Python (Pandas, NumPy, Matplotlib, Seaborn), Microsoft Excel (Power Query, Pivot Tables)
- **Database & Analysis:** MySQL Workbench
- **Visualization:** Power BI Desktop
- **Web Deployment:** HTML, CSS, JavaScript (Live Dashboard)
- **IDE:** VS Code

## Dataset

**Source:** [UCI Machine Learning Repository — Diabetes 130-US Hospitals](https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008)

To replicate the project, download the CSV (~23MB) and place it in the `data/raw/` directory as `diabetic_data.csv`.

- **Size:** 101,766 rows, 50 columns
- **Missing Values:** Encoded as `?`
- **Target Column:** `readmitted` (Values: `NO`, `>30`, `<30`)

## Project Structure

- **`assets/`** — Dashboard screenshots and saved EDA output charts.
- **`data/`** — Contains the raw (`diabetic_data.csv`) and processed (`diabetic_cleaned.csv`) datasets.
- **`docs/`** — Final business-style write-up and project documentation.
- **`public/`** — Source HTML/CSS/JS files for the live web dashboard.
- **`sql/`** — Contains all 10 analysis queries.
- **`src/`** — Data cleaning (`cleaning.py`, `.xlsx`) and exploratory data analysis scripts (`eda.py`).

## How to Run

**1. Excel Cleaning:**
1. Open `src/diabetic_cleaning.xlsx`.
2. The workbook documents each cleaning step with formulas and Power Query.
3. The final sheet exports to `diabetic_cleaned.csv` inside the `data/processed/` folder.

**2. Exploratory Data Analysis (Python):**
1. Ensure you have the required libraries installed: `pip install pandas numpy matplotlib seaborn`
2. Run the EDA script from the project root: `python src/eda.py`
3. The script will generate 6 analytical visualizations and save them directly to the `assets/` folder. *(Note: Ensure `CHART_DIR` in `eda.py` is set to `'assets/'`)*

**3. SQL Analysis:**
1. Open MySQL Workbench and connect to your local server.
2. Create a new schema (e.g., `hospital_db`).
3. Import `diabetic_cleaned.csv` via right-click on schema → *Table Data Import Wizard*.
4. Open `sql/queries.sql` and execute the queries.

**4. Power BI:**
1. Open `dashboard/readmission_dashboard.pbix` in Power BI Desktop (or whichever folder contains your `.pbix` file).
2. Update the data source settings to point to your local `diabetic_cleaned.csv` file.
3. Refresh the dashboard.

## SQL Query Results

<details>
<summary><b>Click to view all 10 SQL Query Result Images</b></summary>
<br>

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

</details>
