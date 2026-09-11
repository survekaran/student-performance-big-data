import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

ANALYTICS_DIR = BASE_DIR / "output" / "analytics"
OUTPUT_DIR = BASE_DIR / "visualizations" / "big_data"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# LOAD PYSPARK ANALYTICS
# ============================================================

overall = pd.read_csv(ANALYTICS_DIR / "overall.csv")
school = pd.read_csv(ANALYTICS_DIR / "school.csv")
gender = pd.read_csv(ANALYTICS_DIR / "gender.csv")
studytime = pd.read_csv(ANALYTICS_DIR / "studytime.csv")
failures = pd.read_csv(ANALYTICS_DIR / "failures.csv")
performance = pd.read_csv(
    ANALYTICS_DIR / "performance_category.csv"
)
absence = pd.read_csv(ANALYTICS_DIR / "absence.csv")
correlation = pd.read_csv(
    ANALYTICS_DIR / "correlation.csv"
)


print("===== BIG DATA VISUALIZATION =====")
print(f"Students: {overall.loc[0, 'students']}")
print(f"Average G3: {overall.loc[0, 'average_G3']}")


# ============================================================
# 1. SCHOOL VS FINAL GRADE
# ============================================================

plt.figure(figsize=(8, 5))

plt.bar(
    school["school"],
    school["average_G3"]
)

plt.xlabel("School")
plt.ylabel("Average final grade (G3)")
plt.title("School vs Final Grade")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "school_vs_grade.png",
    dpi=300
)

plt.close()


# ============================================================
# 2. GENDER VS FINAL GRADE
# ============================================================

plt.figure(figsize=(8, 5))

plt.bar(
    gender["sex"],
    gender["average_G3"]
)

plt.xlabel("Gender")
plt.ylabel("Average final grade (G3)")
plt.title("Gender vs Final Grade")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "gender_vs_grade.png",
    dpi=300
)

plt.close()


# ============================================================
# 3. STUDY TIME VS FINAL GRADE
# ============================================================

studytime_labels = {
    1: "<2 hours",
    2: "2-5 hours",
    3: "5-10 hours",
    4: ">10 hours"
}

studytime["studytime_label"] = (
    studytime["studytime"].map(studytime_labels)
)

plt.figure(figsize=(8, 5))

plt.bar(
    studytime["studytime_label"],
    studytime["average_G3"]
)

plt.xlabel("Weekly study time")
plt.ylabel("Average final grade (G3)")
plt.title("Study Time vs Final Grade")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "studytime_vs_grade.png",
    dpi=300
)

plt.close()


# ============================================================
# 4. PREVIOUS FAILURES VS FINAL GRADE
# ============================================================

plt.figure(figsize=(8, 5))

plt.bar(
    failures["failures"].astype(str),
    failures["average_G3"]
)

plt.xlabel("Number of previous failures")
plt.ylabel("Average final grade (G3)")
plt.title("Previous Failures vs Final Grade")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "failures_vs_grade.png",
    dpi=300
)

plt.close()


# ============================================================
# 5. ABSENCE CATEGORY VS FINAL GRADE
# ============================================================

absence_order = [
    "Very Low",
    "Moderate",
    "High",
    "Very High"
]

absence["absence_category"] = pd.Categorical(
    absence["absence_category"],
    categories=absence_order,
    ordered=True
)

absence = absence.sort_values("absence_category")

plt.figure(figsize=(8, 5))

plt.bar(
    absence["absence_category"].astype(str),
    absence["average_G3"]
)

plt.xlabel("Absence category")
plt.ylabel("Average final grade (G3)")
plt.title("Absence Category vs Final Grade")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "absences_vs_grade.png",
    dpi=300
)

plt.close()


# ============================================================
# 6. PERFORMANCE CATEGORY DISTRIBUTION
# ============================================================

performance_order = [
    "Low",
    "Medium",
    "High"
]

performance["performance_category"] = pd.Categorical(
    performance["performance_category"],
    categories=performance_order,
    ordered=True
)

performance = performance.sort_values(
    "performance_category"
)

plt.figure(figsize=(8, 5))

plt.bar(
    performance["performance_category"].astype(str),
    performance["students"]
)

plt.xlabel("Performance category")
plt.ylabel("Number of students")
plt.title("Student Performance Category Distribution")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "performance_distribution.png",
    dpi=300
)

plt.close()


# ============================================================
# 7. CORRELATION WITH FINAL GRADE
# ============================================================

correlation_values = correlation.iloc[0]

correlation_features = [
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

correlation_plot = pd.DataFrame({
    "feature": correlation_features,
    "correlation": [
        correlation_values[feature]
        for feature in correlation_features
    ]
})

correlation_plot = correlation_plot.sort_values(
    "correlation"
)

plt.figure(figsize=(10, 6))

plt.barh(
    correlation_plot["feature"],
    correlation_plot["correlation"]
)

plt.xlabel("Pearson correlation with G3")
plt.ylabel("Feature")
plt.title("Correlation of Student Factors with Final Grade")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "correlation_with_grade.png",
    dpi=300
)

plt.close()


# ============================================================
# COMPLETION MESSAGE
# ============================================================

print("\n===== BIG DATA VISUALIZATION COMPLETE =====")

print("Generated files:")

for file in sorted(OUTPUT_DIR.glob("*.png")):
    print(f"- {file.name}")
