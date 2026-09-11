-- ============================================================
-- STUDENT PERFORMANCE BIG DATA ANALYTICS
-- HIVE SCHEMA
-- ============================================================

CREATE DATABASE IF NOT EXISTS student_performance;

USE student_performance;


-- ============================================================
-- MATHEMATICS DATASET
-- ============================================================

CREATE EXTERNAL TABLE IF NOT EXISTS student_mat (
    school STRING,
    sex STRING,
    age INT,
    address STRING,
    famsize STRING,
    pstatus STRING,
    medu INT,
    fedu INT,
    mjob STRING,
    fjob STRING,
    reason STRING,
    guardian STRING,
    traveltime INT,
    studytime INT,
    failures INT,
    schoolsup STRING,
    famsup STRING,
    paid STRING,
    activities STRING,
    nursery STRING,
    higher STRING,
    internet STRING,
    romantic STRING,
    famrel INT,
    freetime INT,
    goout INT,
    dalc INT,
    walc INT,
    health INT,
    absences INT,
    g1 INT,
    g2 INT,
    g3 INT
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
    "separatorChar" = ";",
    "quoteChar" = "\""
)
STORED AS TEXTFILE
LOCATION 'hdfs://localhost:9000/student-performance/uci/mat/';


-- ============================================================
-- PORTUGUESE DATASET
-- ============================================================

CREATE EXTERNAL TABLE IF NOT EXISTS student_por (
    school STRING,
    sex STRING,
    age INT,
    address STRING,
    famsize STRING,
    pstatus STRING,
    medu INT,
    fedu INT,
    mjob STRING,
    fjob STRING,
    reason STRING,
    guardian STRING,
    traveltime INT,
    studytime INT,
    failures INT,
    schoolsup STRING,
    famsup STRING,
    paid STRING,
    activities STRING,
    nursery STRING,
    higher STRING,
    internet STRING,
    romantic STRING,
    famrel INT,
    freetime INT,
    goout INT,
    dalc INT,
    walc INT,
    health INT,
    absences INT,
    g1 INT,
    g2 INT,
    g3 INT
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
    "separatorChar" = ";",
    "quoteChar" = "\""
)
STORED AS TEXTFILE
LOCATION 'hdfs://localhost:9000/student-performance/uci/por/';
