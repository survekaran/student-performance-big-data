from pyspark.sql import SparkSession
from pyspark.sql.functions import when, col, corr, avg, count, round


# ============================================================
# 1. CREATE SPARK SESSION
# ============================================================

spark = SparkSession.builder \
    .appName("Student Performance Big Data Output") \
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
# 3. CREATE PERFORMANCE CATEGORY
# ============================================================

df_category = df.withColumn(
    "performance_category",
    when(col("G3") < 10, "Low")
    .when(col("G3") < 15, "Medium")
    .otherwise("High")
)


# ============================================================
# 4. OUTPUT DIRECTORY
# ============================================================

output_base = "hdfs://localhost:9000/student-performance/analytics"


# ============================================================
# 5. OVERALL PERFORMANCE
# ============================================================

overall = df.agg(
    count("*").alias("students"),
    round(avg("G3"), 2).alias("average_G3"),
    round(avg("G1"), 2).alias("average_G1"),
    round(avg("G2"), 2).alias("average_G2"),
    round(avg("failures"), 2).alias("average_failures"),
    round(avg("absences"), 2).alias("average_absences")
)

overall.coalesce(1).write.mode("overwrite").option(
    "header", "true"
).csv(output_base + "/overall")


# ============================================================
# 6. SCHOOL ANALYSIS
# ============================================================

school_analysis = df.groupBy("school").agg(
    count("*").alias("students"),
    round(avg("G3"), 2).alias("average_G3")
)

school_analysis.coalesce(1).write.mode("overwrite").option(
    "header", "true"
).csv(output_base + "/school")


# ============================================================
# 7. GENDER ANALYSIS
# ============================================================

gender_analysis = df.groupBy("sex").agg(
    count("*").alias("students"),
    round(avg("G3"), 2).alias("average_G3")
)

gender_analysis.coalesce(1).write.mode("overwrite").option(
    "header", "true"
).csv(output_base + "/gender")


# ============================================================
# 8. STUDY TIME ANALYSIS
# ============================================================

studytime_analysis = df.groupBy("studytime").agg(
    count("*").alias("students"),
    round(avg("G3"), 2).alias("average_G3")
).orderBy("studytime")

studytime_analysis.coalesce(1).write.mode("overwrite").option(
    "header", "true"
).csv(output_base + "/studytime")


# ============================================================
# 9. PERFORMANCE CATEGORY
# ============================================================

performance_analysis = df_category.groupBy(
    "performance_category"
).agg(
    count("*").alias("students"),
    round(avg("G3"), 2).alias("average_G3")
)

performance_analysis.coalesce(1).write.mode("overwrite").option(
    "header", "true"
).csv(output_base + "/performance_category")


# ============================================================
# 10. FAILURE ANALYSIS
# ============================================================

failure_analysis = df_category.groupBy("failures").agg(
    count("*").alias("students"),
    round(avg("G3"), 2).alias("average_G3")
).orderBy("failures")

failure_analysis.coalesce(1).write.mode("overwrite").option(
    "header", "true"
).csv(output_base + "/failures")


# ============================================================
# 11. ABSENCE ANALYSIS
# ============================================================

df_absence = df_category.withColumn(
    "absence_category",
    when(col("absences") <= 5, "Very Low")
    .when(col("absences") <= 10, "Moderate")
    .when(col("absences") <= 20, "High")
    .otherwise("Very High")
)

absence_analysis = df_absence.groupBy(
    "absence_category"
).agg(
    count("*").alias("students"),
    round(avg("G3"), 2).alias("average_G3")
)

absence_analysis.coalesce(1).write.mode("overwrite").option(
    "header", "true"
).csv(output_base + "/absence")


# ============================================================
# 12. CORRELATION ANALYSIS
# ============================================================

correlation_analysis = df.select(
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

correlation_analysis.coalesce(1).write.mode("overwrite").option(
    "header", "true"
).csv(output_base + "/correlation")


# ============================================================
# 13. SAVE PROCESSED DATASET
# ============================================================

df_absence.coalesce(1).write.mode("overwrite").option(
    "header", "true"
).csv(output_base + "/processed_student_data")


# ============================================================
# 14. COMPLETION MESSAGE
# ============================================================

print("\n==============================================")
print("PYSPARK ANALYSIS OUTPUT SAVED TO HDFS")
print("==============================================")
print("Output location:")
print(output_base)
print("==============================================\n")


spark.stop()
