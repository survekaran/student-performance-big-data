import pandas as pd

# Dataset paths
math_path = "data/raw/student+performance/student-mat.csv"
portuguese_path = "data/raw/student+performance/student-por.csv"

# Load datasets
math_df = pd.read_csv(math_path, sep=";")
portuguese_df = pd.read_csv(portuguese_path, sep=";")

# ============================================================
# BASIC INFORMATION
# ============================================================

print("\n===== MATHEMATICS DATASET =====")
print("Rows:", math_df.shape[0])
print("Columns:", math_df.shape[1])

print("\n===== PORTUGUESE DATASET =====")
print("Rows:", portuguese_df.shape[0])
print("Columns:", portuguese_df.shape[1])


# ============================================================
# MISSING VALUES
# ============================================================

print("\n===== MISSING VALUES: MATHEMATICS =====")
print(math_df.isnull().sum())

print("\n===== MISSING VALUES: PORTUGUESE =====")
print(portuguese_df.isnull().sum())


# ============================================================
# DUPLICATES
# ============================================================

print("\n===== DUPLICATES =====")
print("Mathematics duplicates:", math_df.duplicated().sum())
print("Portuguese duplicates:", portuguese_df.duplicated().sum())


# ============================================================
# DATA TYPES
# ============================================================

print("\n===== DATA TYPES =====")
print(math_df.dtypes)


# ============================================================
# STATISTICAL SUMMARY
# ============================================================

print("\n===== MATHEMATICS STATISTICS =====")
print(math_df.describe())


print("\n===== PORTUGUESE STATISTICS =====")
print(portuguese_df.describe())


# ============================================================
# IMPORTANT VARIABLES
# ============================================================

print("\n===== STUDY TIME DISTRIBUTION =====")
print(math_df["studytime"].value_counts().sort_index())

print("\n===== FAILURES DISTRIBUTION =====")
print(math_df["failures"].value_counts().sort_index())

print("\n===== ABSENCES STATISTICS =====")
print(math_df["absences"].describe())


# ============================================================
# FINAL GRADE
# ============================================================

print("\n===== FINAL GRADE (G3) =====")
print("Mathematics:")
print(math_df["G3"].describe())

print("\nPortuguese:")
print(portuguese_df["G3"].describe())