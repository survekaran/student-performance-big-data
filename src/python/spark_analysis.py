from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, count, when, corr

# ============================================================
# CREATE SPARK SESSION
# ============================================================

spark = SparkSession.builder \
    .appName("Student Performance Analysis") \
    .master("local[*]") \
    .getOrCreate()


# ============================================================
# LOAD PROCESSED DATA
# ============================================================

file_path = "data/processed/student_performance_processed.csv"

df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv(file_path)


# ============================================================
# BASIC DATA INFORMATION
# ============================================================

print("\n===== SPARK DATASET =====")

print("Number of rows:", df.count())
print("Number of columns:", len(df.columns))


# ============================================================
# DISPLAY SCHEMA
# ============================================================

print("\n===== DATA SCHEMA =====")

df.printSchema()


# ============================================================
# DISPLAY FIRST 10 RECORDS
# ============================================================

print("\n===== FIRST 10 RECORDS =====")

df.show(10, truncate=False)


# ============================================================
# ANALYSIS 1: STUDY TIME VS FINAL PERFORMANCE
# ============================================================

print("\n===== STUDY TIME VS FINAL PERFORMANCE =====")

studytime_analysis = df.groupBy("studytime") \
    .agg(
        avg("G3").alias("average_final_grade"),
        count("*").alias("student_count")
    ) \
    .orderBy("studytime")

studytime_analysis.show()


# ============================================================
# ANALYSIS 2: ABSENCE CATEGORY VS FINAL PERFORMANCE
# ============================================================

print("\n===== ABSENCE CATEGORY VS FINAL PERFORMANCE =====")

df_with_absence_category = df.withColumn(
    "absence_category",
    when(df["absences"] <= 5, "Very Low")
    .when(df["absences"] <= 10, "Moderate")
    .when(df["absences"] <= 20, "High")
    .otherwise("Very High")
)

absence_analysis = df_with_absence_category.groupBy(
    "absence_category"
).agg(
    avg("G3").alias("average_final_grade"),
    count("*").alias("student_count")
)

absence_analysis.show()


# ============================================================
# ANALYSIS 3: PREVIOUS FAILURES VS FINAL PERFORMANCE
# ============================================================

print("\n===== PREVIOUS FAILURES VS FINAL PERFORMANCE =====")

failure_analysis = df.groupBy("failures") \
    .agg(
        avg("G3").alias("average_final_grade"),
        count("*").alias("student_count")
    ) \
    .orderBy("failures")

failure_analysis.show()


# ============================================================
# ANALYSIS 4: CORRELATION WITH FINAL PERFORMANCE
# ============================================================

print("\n===== CORRELATION WITH FINAL PERFORMANCE (G3) =====")

correlation_columns = [
    "studytime",
    "failures",
    "absences",
    "G1",
    "G2",
    "Medu",
    "Fedu",
    "traveltime",
    "freetime",
    "goout",
    "health"
]

for column in correlation_columns:
    correlation = df.stat.corr(column, "G3")
    print(f"{column:12} : {correlation:.4f}")
    
    

# ============================================================
# ANALYSIS 5: SUBJECT VS FINAL PERFORMANCE
# ============================================================

print("\n===== SUBJECT VS FINAL PERFORMANCE =====")

subject_analysis = df.groupBy("subject") \
    .agg(
        avg("G3").alias("average_final_grade"),
        count("*").alias("student_count")
    ) \
    .orderBy("average_final_grade", ascending=False)

subject_analysis.show()


print("\n===== SPARK SQL ANALYSIS =====")

df.createOrReplaceTempView("student_performance")

sql_result = spark.sql("""
    SELECT
        subject,
        performance_category,
        COUNT(*) AS student_count,
        ROUND(AVG(G3), 2) AS average_final_grade
    FROM student_performance
    GROUP BY subject, performance_category
    ORDER BY subject, average_final_grade DESC
""")

sql_result.show()



# ============================================================
# STOP SPARK
# ============================================================

spark.stop()