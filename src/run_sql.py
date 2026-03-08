"""
run_sql.py — Load cleaned data into SQLite and run all 10 queries
Author: Portfolio Project

Prints results to console. No external SQL client needed.
"""

import pandas as pd
import sqlite3

df = pd.read_csv('data/processed/diabetic_cleaned.csv')
conn = sqlite3.connect(':memory:')   # in-memory DB, no file needed
df.to_sql('diabetic', conn, if_exists='replace', index=False)
print(f"Loaded {len(df):,} rows into SQLite\n")

queries = {
    "1. Overall Readmission Rate": """
        SELECT COUNT(*) AS total_patients,
               SUM(readmitted_binary) AS high_risk,
               ROUND(100.0 * SUM(readmitted_binary) / COUNT(*), 2) AS rate_pct
        FROM diabetic""",

    "2. By Age Group": """
        SELECT age, COUNT(*) AS total, SUM(readmitted_binary) AS readmitted,
               ROUND(100.0 * SUM(readmitted_binary) / COUNT(*), 2) AS rate_pct
        FROM diabetic GROUP BY age ORDER BY age""",

    "3. By Race": """
        SELECT race, COUNT(*) AS total, SUM(readmitted_binary) AS readmitted,
               ROUND(100.0 * SUM(readmitted_binary) / COUNT(*), 2) AS rate_pct
        FROM diabetic GROUP BY race ORDER BY rate_pct DESC""",

    "4. By Gender": """
        SELECT gender, COUNT(*) AS total, SUM(readmitted_binary) AS readmitted,
               ROUND(100.0 * SUM(readmitted_binary) / COUNT(*), 2) AS rate_pct
        FROM diabetic GROUP BY gender""",

    "5. Avg Hospital Stay — Readmitted vs Not": """
        SELECT CASE WHEN readmitted_binary=1 THEN 'Readmitted (<30d)' ELSE 'Not Readmitted' END AS grp,
               ROUND(AVG(time_in_hospital), 2) AS avg_days, COUNT(*) AS total
        FROM diabetic GROUP BY readmitted_binary""",

    "6. By Number of Diagnoses": """
        SELECT number_diagnoses, COUNT(*) AS total, SUM(readmitted_binary) AS readmitted,
               ROUND(100.0 * SUM(readmitted_binary) / COUNT(*), 2) AS rate_pct
        FROM diabetic GROUP BY number_diagnoses ORDER BY number_diagnoses""",

    "7. By Insulin Dosage Change": """
        SELECT insulin, COUNT(*) AS total, SUM(readmitted_binary) AS readmitted,
               ROUND(100.0 * SUM(readmitted_binary) / COUNT(*), 2) AS rate_pct
        FROM diabetic GROUP BY insulin ORDER BY rate_pct DESC""",

    "8. By Diabetes Medication": """
        SELECT diabetesMed, COUNT(*) AS total, SUM(readmitted_binary) AS readmitted,
               ROUND(100.0 * SUM(readmitted_binary) / COUNT(*), 2) AS rate_pct
        FROM diabetic GROUP BY diabetesMed""",

    "9. By Medication Count Group": """
        SELECT CASE WHEN num_medications < 10 THEN 'Low (< 10)'
                    WHEN num_medications BETWEEN 10 AND 20 THEN 'Medium (10-20)'
                    ELSE 'High (> 20)' END AS grp,
               COUNT(*) AS total, SUM(readmitted_binary) AS readmitted,
               ROUND(100.0 * SUM(readmitted_binary) / COUNT(*), 2) AS rate_pct
        FROM diabetic GROUP BY grp""",

    "10. By Lab Procedure Count": """
        SELECT CASE WHEN num_lab_procedures < 30 THEN 'Low (< 30)'
                    WHEN num_lab_procedures BETWEEN 30 AND 60 THEN 'Medium (30-60)'
                    ELSE 'High (> 60)' END AS grp,
               COUNT(*) AS total, SUM(readmitted_binary) AS readmitted,
               ROUND(100.0 * SUM(readmitted_binary) / COUNT(*), 2) AS rate_pct
        FROM diabetic GROUP BY grp"""
}

for title, query in queries.items():
    print(f"\n{'─'*55}")
    print(f"  {title}")
    print('─'*55)
    result = pd.read_sql_query(query, conn)
    print(result.to_string(index=False))

conn.close()
