from pyspark.sql import SparkSession
from pyspark.sql.functions import when, col, corr, avg, count, round


# ============================================================
# 1. CREATE SPARK SESSION
# ============================================================

spark = SparkSession.builder \
    .appName("Student Performance Analysis") \
    .getOrCreate()


# ============================================================
# 2. READ DATASET FROM HDFS
# ============================================================

input_path = "hdfs://localhost:9000/student-performance/uci/mat/student-mat.csv"

df = spark.read.csv(
    input_path,
    header=True,
    inferSchema=True,
    sep=";"
)


# ============================================================
# 3. DATASET INFORMATION
# ============================================================

print("\n===== DATASET INFORMATION =====")

print("Total records:", df.count())
print("Total columns:", len(df.columns))

df.printSchema()


# ============================================================
# 4. SAMPLE DATA
# ============================================================

print("\n===== SAMPLE DATA =====")

df.select(
    "school",
    "sex",
    "age",
    "studytime",
    "failures",
    "absences",
    "G1",
    "G2",
    "G3"
).show(5)


# ============================================================
# 5. DESCRIPTIVE STATISTICS
# ============================================================

print("\n===== DESCRIPTIVE STATISTICS =====")

df.select(
    "age",
    "studytime",
    "failures",
    "absences",
    "G1",
    "G2",
    "G3"
).describe().show()


# ============================================================
# 6. AVERAGE PERFORMANCE BY SCHOOL
# ============================================================

print("\n===== AVERAGE G3 BY SCHOOL =====")

df.groupBy("school").agg(
    round(avg("G3"), 2).alias("average_G3"),
    count("*").alias("students")
).show()


# ============================================================
# 7. AVERAGE PERFORMANCE BY GENDER
# ============================================================

print("\n===== AVERAGE G3 BY GENDER =====")

df.groupBy("sex").agg(
    round(avg("G3"), 2).alias("average_G3"),
    count("*").alias("students")
).show()


# ============================================================
# 8. AVERAGE PERFORMANCE BY STUDY TIME
# ============================================================

print("\n===== AVERAGE G3 BY STUDY TIME =====")

df.groupBy("studytime").agg(
    round(avg("G3"), 2).alias("average_G3"),
    count("*").alias("students")
).orderBy("studytime").show()


# ============================================================
# 9. PERFORMANCE CATEGORIES
# ============================================================

df_category = df.withColumn(
    "performance_category",
    when(col("G3") < 10, "Low")
    .when(col("G3") < 15, "Medium")
    .otherwise("High")
)

print("\n===== PERFORMANCE CATEGORY =====")

df_category.groupBy("performance_category").agg(
    count("*").alias("students"),
    round(avg("G3"), 2).alias("average_G3")
).orderBy("performance_category").show()


# ============================================================
# 10. FAILURE ANALYSIS
# ============================================================

print("\n===== AVERAGE G3 BY FAILURES =====")

df_category.groupBy("failures").agg(
    count("*").alias("students"),
    round(avg("G3"), 2).alias("average_G3")
).orderBy("failures").show()


print("\n===== FAILURES VS PERFORMANCE CATEGORY =====")

df_category.groupBy(
    "failures",
    "performance_category"
).count().orderBy(
    "failures",
    "performance_category"
).show()


# ============================================================
# 11. ABSENCE CATEGORIES
# ============================================================

df_absence = df_category.withColumn(
    "absence_category",
    when(col("absences") <= 5, "Very Low")
    .when(col("absences") <= 10, "Moderate")
    .when(col("absences") <= 20, "High")
    .otherwise("Very High")
)

print("\n===== ABSENCE CATEGORY ANALYSIS =====")

df_absence.groupBy("absence_category").agg(
    count("*").alias("students"),
    round(avg("G3"), 2).alias("average_G3")
).show()


# ============================================================
# 12. CORRELATION ANALYSIS
# ============================================================

print("\n===== CORRELATION WITH FINAL GRADE G3 =====")

correlation_df = df.select(
    corr("studytime", "G3").alias("studytime"),
    corr("failures", "G3").alias("failures"),
    corr("absences", "G3").alias("absences"),
    corr("G1", "G3").alias("G1"),
    corr("G2", "G3").alias("G2"),
    corr("Medu", "G3").alias("Medu"),
    corr("Fedu", "G3").alias("Fedu"),
    corr("traveltime", "G3").alias("traveltime"),
    corr("freetime", "G3").alias("freetime"),
    corr("goout", "G3").alias("goout"),
    corr("health", "G3").alias("health")
)

correlation_df.show(truncate=False)


# ============================================================
# 13. PERFORMANCE SUMMARY
# ============================================================

print("\n===== OVERALL PERFORMANCE =====")

df.agg(
    count("*").alias("students"),
    round(avg("G3"), 2).alias("average_G3"),
    round(avg("G1"), 2).alias("average_G1"),
    round(avg("G2"), 2).alias("average_G2"),
    round(avg("failures"), 2).alias("average_failures"),
    round(avg("absences"), 2).alias("average_absences")
).show()


# ============================================================
# 14. STOP SPARK
# ============================================================

spark.stop()

print("\n===== ANALYSIS COMPLETED SUCCESSFULLY =====")
