-- ============================================================
-- SQL Analysis — Hospital Readmission (SQLite)
-- Run via: python src/run_sql.py
-- ============================================================


-- 1. Overall readmission rate
SELECT
    COUNT(*)                                              AS total_patients,
    SUM(readmitted_binary)                                AS high_risk_readmissions,
    ROUND(100.0 * SUM(readmitted_binary) / COUNT(*), 2)   AS readmission_rate_pct
FROM diabetic;


-- 2. Readmission rate by age group
SELECT
    age,
    COUNT(*)                                              AS total,
    SUM(readmitted_binary)                                AS readmitted,
    ROUND(100.0 * SUM(readmitted_binary) / COUNT(*), 2)   AS rate_pct
FROM diabetic
GROUP BY age
ORDER BY age;


-- 3. Readmission rate by race
SELECT
    race,
    COUNT(*)                                              AS total,
    SUM(readmitted_binary)                                AS readmitted,
    ROUND(100.0 * SUM(readmitted_binary) / COUNT(*), 2)   AS rate_pct
FROM diabetic
GROUP BY race
ORDER BY rate_pct DESC;


-- 4. Readmission rate by gender
SELECT
    gender,
    COUNT(*)                                              AS total,
    SUM(readmitted_binary)                                AS readmitted,
    ROUND(100.0 * SUM(readmitted_binary) / COUNT(*), 2)   AS rate_pct
FROM diabetic
GROUP BY gender;


-- 5. Average hospital stay — readmitted vs not
SELECT
    CASE WHEN readmitted_binary = 1
         THEN 'Readmitted (<30 days)'
         ELSE 'Not Readmitted'
    END                                                   AS group_label,
    ROUND(AVG(time_in_hospital), 2)                       AS avg_days,
    COUNT(*)                                              AS total
FROM diabetic
GROUP BY readmitted_binary;


-- 6. Readmission by number of diagnoses
SELECT
    number_diagnoses,
    COUNT(*)                                              AS total,
    SUM(readmitted_binary)                                AS readmitted,
    ROUND(100.0 * SUM(readmitted_binary) / COUNT(*), 2)   AS rate_pct
FROM diabetic
GROUP BY number_diagnoses
ORDER BY number_diagnoses;


-- 7. Impact of insulin dosage change on readmission
SELECT
    insulin,
    COUNT(*)                                              AS total,
    SUM(readmitted_binary)                                AS readmitted,
    ROUND(100.0 * SUM(readmitted_binary) / COUNT(*), 2)   AS rate_pct
FROM diabetic
GROUP BY insulin
ORDER BY rate_pct DESC;


-- 8. Impact of diabetes medication (on/off) on readmission
SELECT
    diabetesMed,
    COUNT(*)                                              AS total,
    SUM(readmitted_binary)                                AS readmitted,
    ROUND(100.0 * SUM(readmitted_binary) / COUNT(*), 2)   AS rate_pct
FROM diabetic
GROUP BY diabetesMed;


-- 9. Readmission by medication count group
SELECT
    CASE
        WHEN num_medications < 10           THEN 'Low (< 10)'
        WHEN num_medications BETWEEN 10 AND 20 THEN 'Medium (10-20)'
        ELSE                                     'High (> 20)'
    END                                                   AS med_group,
    COUNT(*)                                              AS total,
    SUM(readmitted_binary)                                AS readmitted,
    ROUND(100.0 * SUM(readmitted_binary) / COUNT(*), 2)   AS rate_pct
FROM diabetic
GROUP BY med_group;


-- 10. Readmission by lab procedure count group
SELECT
    CASE
        WHEN num_lab_procedures < 30            THEN 'Low (< 30)'
        WHEN num_lab_procedures BETWEEN 30 AND 60 THEN 'Medium (30-60)'
        ELSE                                         'High (> 60)'
    END                                                   AS lab_group,
    COUNT(*)                                              AS total,
    SUM(readmitted_binary)                                AS readmitted,
    ROUND(100.0 * SUM(readmitted_binary) / COUNT(*), 2)   AS rate_pct
FROM diabetic
GROUP BY lab_group;
