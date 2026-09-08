import pandas as pd
from pathlib import Path


# ============================================================
# FILE PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DIR = BASE_DIR / "data" / "raw" / "student+performance"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

MATH_FILE = RAW_DIR / "student-mat.csv"
PORTUGUESE_FILE = RAW_DIR / "student-por.csv"


# ============================================================
# LOAD DATA
# ============================================================

math_df = pd.read_csv(MATH_FILE, sep=";")
portuguese_df = pd.read_csv(PORTUGUESE_FILE, sep=";")


# ============================================================
# ADD SUBJECT COLUMN
# ============================================================

math_df["subject"] = "Mathematics"
portuguese_df["subject"] = "Portuguese"


# ============================================================
# COMBINE DATASETS
# ============================================================

df = pd.concat(
    [math_df, portuguese_df],
    ignore_index=True
)


# ============================================================
# DATA VALIDATION
# ============================================================

print("\n===== DATA VALIDATION =====")

print("Total rows:", len(df))
print("Total columns:", len(df.columns))

print("\nMissing values:")
print(df.isnull().sum().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())


# ============================================================
# SELECT IMPORTANT COLUMNS
# ============================================================

selected_columns = [
    "school",
    "sex",
    "age",
    "studytime",
    "failures",
    "absences",
    "G1",
    "G2",
    "G3",
    "Medu",
    "Fedu",
    "traveltime",
    "famsup",
    "schoolsup",
    "internet",
    "freetime",
    "goout",
    "health",
    "subject"
]

df = df[selected_columns]


# ============================================================
# CREATE PERFORMANCE CATEGORY
# ============================================================

def performance_category(score):
    if score < 10:
        return "Low"
    elif score < 15:
        return "Medium"
    else:
        return "High"


df["performance_category"] = df["G3"].apply(
    performance_category
)


# ============================================================
# SAVE PROCESSED DATA
# ============================================================

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

output_file = PROCESSED_DIR / "student_performance_processed.csv"

df.to_csv(output_file, index=False)


# ============================================================
# FINAL INFORMATION
# ============================================================

print("\n===== PROCESSED DATA =====")

print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\nSubjects:")
print(df["subject"].value_counts())

print("\nPerformance categories:")
print(df["performance_category"].value_counts())

print("\nProcessed file saved to:")
print(output_file)