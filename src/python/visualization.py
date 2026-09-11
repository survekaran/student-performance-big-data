import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_FILE = BASE_DIR / "data" / "processed" / "student_performance_processed.csv"
OUTPUT_DIR = BASE_DIR / "visualizations"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# LOAD PROCESSED DATA
# ============================================================

df = pd.read_csv(DATA_FILE)

print("===== VISUALIZATION DATASET =====")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")


# ============================================================
# 1. STUDY TIME VS FINAL GRADE
# ============================================================

studytime_analysis = (
    df.groupby("studytime")["G3"]
    .agg(["mean", "count"])
    .reset_index()
)

studytime_labels = {
    1: "<2 hours",
    2: "2-5 hours",
    3: "5-10 hours",
    4: ">10 hours"
}

studytime_analysis["studytime_label"] = (
    studytime_analysis["studytime"].map(studytime_labels)
)

plt.figure(figsize=(8, 5))

plt.bar(
    studytime_analysis["studytime_label"],
    studytime_analysis["mean"]
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
# 2. PREVIOUS FAILURES VS FINAL GRADE
# ============================================================

failure_analysis = (
    df.groupby("failures")["G3"]
    .agg(["mean", "count"])
    .reset_index()
)

plt.figure(figsize=(8, 5))

plt.bar(
    failure_analysis["failures"].astype(str),
    failure_analysis["mean"]
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
# 3. ABSENCES VS FINAL GRADE
# ============================================================

df["absence_category"] = pd.cut(
    df["absences"],
    bins=[-1, 5, 10, 20, float("inf")],
    labels=[
        "Very Low",
        "Moderate",
        "High",
        "Very High"
    ]
)

absence_analysis = (
    df.groupby(
        "absence_category",
        observed=True
    )["G3"]
    .mean()
    .reset_index()
)

plt.figure(figsize=(8, 5))

plt.bar(
    absence_analysis["absence_category"].astype(str),
    absence_analysis["G3"]
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
# 4. SUBJECT VS FINAL GRADE
# ============================================================

subject_analysis = (
    df.groupby("subject")["G3"]
    .agg(["mean", "count"])
    .reset_index()
)

plt.figure(figsize=(8, 5))

plt.bar(
    subject_analysis["subject"],
    subject_analysis["mean"]
)

plt.xlabel("Subject")
plt.ylabel("Average final grade (G3)")
plt.title("Subject vs Final Grade")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "subject_vs_grade.png",
    dpi=300
)

plt.close()


# ============================================================
# 5. PERFORMANCE CATEGORY DISTRIBUTION
# ============================================================

performance_counts = (
    df["performance_category"]
    .value_counts()
    .reindex(["Low", "Medium", "High"])
)

plt.figure(figsize=(8, 5))

plt.bar(
    performance_counts.index,
    performance_counts.values
)

plt.xlabel("Performance category")
plt.ylabel("Number of records")
plt.title("Student Performance Category Distribution")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "performance_distribution.png",
    dpi=300
)

plt.close()


# ============================================================
# COMPLETION MESSAGE
# ============================================================

print("\n===== VISUALIZATION COMPLETE =====")

print("Generated files:")

for file in sorted(OUTPUT_DIR.glob("*.png")):
    print(f"- {file.name}")