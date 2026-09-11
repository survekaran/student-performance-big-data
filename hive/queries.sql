-- ============================================================
-- STUDENT PERFORMANCE BIG DATA ANALYTICS
-- HIVE ANALYTICS QUERIES
-- ============================================================

USE student_performance;

-- Use MapReduce instead of Tez
SET hive.execution.engine=mr;


-- ============================================================
-- 1. MATHEMATICS DATASET SUMMARY
-- ============================================================

SELECT
    'Mathematics' AS subject,
    COUNT(*) AS students,
    ROUND(AVG(CAST(g3 AS DOUBLE)), 2) AS average_g3,
    MAX(CAST(g3 AS INT)) AS highest_g3,
    MIN(CAST(g3 AS INT)) AS lowest_g3
FROM student_mat
WHERE school != 'school';


-- ============================================================
-- 2. PORTUGUESE DATASET SUMMARY
-- ============================================================

SELECT
    'Portuguese' AS subject,
    COUNT(*) AS students,
    ROUND(AVG(CAST(g3 AS DOUBLE)), 2) AS average_g3,
    MAX(CAST(g3 AS INT)) AS highest_g3,
    MIN(CAST(g3 AS INT)) AS lowest_g3
FROM student_por
WHERE school != 'school';


-- ============================================================
-- 3. MATHEMATICS PERFORMANCE BY SCHOOL
-- ============================================================

SELECT
    school,
    COUNT(*) AS students,
    ROUND(AVG(CAST(g3 AS DOUBLE)), 2) AS average_g3
FROM student_mat
WHERE school != 'school'
GROUP BY school;


-- ============================================================
-- 4. MATHEMATICS PERFORMANCE BY GENDER
-- ============================================================

SELECT
    sex,
    COUNT(*) AS students,
    ROUND(AVG(CAST(g3 AS DOUBLE)), 2) AS average_g3
FROM student_mat
WHERE school != 'school'
GROUP BY sex;


-- ============================================================
-- 5. MATHEMATICS PERFORMANCE BY STUDY TIME
-- ============================================================

SELECT
    studytime,
    COUNT(*) AS students,
    ROUND(AVG(CAST(g3 AS DOUBLE)), 2) AS average_g3
FROM student_mat
WHERE school != 'school'
GROUP BY studytime
ORDER BY studytime;


-- ============================================================
-- 6. MATHEMATICS PERFORMANCE BY FAILURES
-- ============================================================

SELECT
    failures,
    COUNT(*) AS students,
    ROUND(AVG(CAST(g3 AS DOUBLE)), 2) AS average_g3
FROM student_mat
WHERE school != 'school'
GROUP BY failures
ORDER BY failures;


-- ============================================================
-- 7. MATHEMATICS PERFORMANCE CATEGORIES
-- ============================================================

SELECT
    CASE
        WHEN CAST(g3 AS INT) < 10 THEN 'Low'
        WHEN CAST(g3 AS INT) < 15 THEN 'Medium'
        ELSE 'High'
    END AS performance_category,
    COUNT(*) AS students,
    ROUND(AVG(CAST(g3 AS DOUBLE)), 2) AS average_g3
FROM student_mat
WHERE school != 'school'
GROUP BY
    CASE
        WHEN CAST(g3 AS INT) < 10 THEN 'Low'
        WHEN CAST(g3 AS INT) < 15 THEN 'Medium'
        ELSE 'High'
    END;


-- ============================================================
-- 8. MATHEMATICS ABSENCE ANALYSIS
-- ============================================================

SELECT
    CASE
        WHEN CAST(absences AS INT) <= 5 THEN 'Very Low'
        WHEN CAST(absences AS INT) <= 10 THEN 'Moderate'
        WHEN CAST(absences AS INT) <= 20 THEN 'High'
        ELSE 'Very High'
    END AS absence_category,
    COUNT(*) AS students,
    ROUND(AVG(CAST(g3 AS DOUBLE)), 2) AS average_g3
FROM student_mat
WHERE school != 'school'
GROUP BY
    CASE
        WHEN CAST(absences AS INT) <= 5 THEN 'Very Low'
        WHEN CAST(absences AS INT) <= 10 THEN 'Moderate'
        WHEN CAST(absences AS INT) <= 20 THEN 'High'
        ELSE 'Very High'
    END;


-- ============================================================
-- 9. SUBJECT COMPARISON
-- ============================================================

SELECT
    'Mathematics' AS subject,
    COUNT(*) AS students,
    ROUND(AVG(CAST(g3 AS DOUBLE)), 2) AS average_g3
FROM student_mat
WHERE school != 'school';

SELECT
    'Portuguese' AS subject,
    COUNT(*) AS students,
    ROUND(AVG(CAST(g3 AS DOUBLE)), 2) AS average_g3
FROM student_por
WHERE school != 'school';
