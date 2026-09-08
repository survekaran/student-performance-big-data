import streamlit as st
import pandas as pd
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Student Performance Analytics",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "student_performance_processed.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE)


df = load_data()


# ============================================================
# HEADER
# ============================================================

st.title("📊 Student Performance Analytics Dashboard")

st.markdown(
    """
    ### Big Data Analytics Project

    This dashboard presents analytical insights from the
    Student Performance dataset using Python, PySpark,
    Spark SQL, and data visualization.
    """
)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("🔎 Filters")


# ------------------------------------------------------------
# Subject Filter
# ------------------------------------------------------------

subject_options = ["All"] + sorted(
    df["subject"].unique().tolist()
)

selected_subject = st.sidebar.selectbox(
    "Subject",
    subject_options
)


# ------------------------------------------------------------
# School Filter
# ------------------------------------------------------------

school_options = ["All"] + sorted(
    df["school"].unique().tolist()
)

selected_school = st.sidebar.selectbox(
    "School",
    school_options
)


# ------------------------------------------------------------
# Gender Filter
# ------------------------------------------------------------

gender_options = ["All"] + sorted(
    df["sex"].unique().tolist()
)

selected_gender = st.sidebar.selectbox(
    "Gender",
    gender_options
)


# ------------------------------------------------------------
# Performance Filter
# ------------------------------------------------------------

performance_options = ["All"] + sorted(
    df["performance_category"].unique().tolist()
)

selected_performance = st.sidebar.selectbox(
    "Performance Category",
    performance_options
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()


if selected_subject != "All":

    filtered_df = filtered_df[
        filtered_df["subject"] == selected_subject
    ]


if selected_school != "All":

    filtered_df = filtered_df[
        filtered_df["school"] == selected_school
    ]


if selected_gender != "All":

    filtered_df = filtered_df[
        filtered_df["sex"] == selected_gender
    ]


if selected_performance != "All":

    filtered_df = filtered_df[
        filtered_df["performance_category"]
        == selected_performance
    ]


# ============================================================
# HANDLE EMPTY FILTER RESULTS
# ============================================================

if filtered_df.empty:

    st.warning(
        "No records match the selected filters."
    )

    st.stop()


# ============================================================
# KEY PERFORMANCE INDICATORS
# ============================================================

st.subheader("📌 Overview")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Records",
        len(filtered_df)
    )


with col2:

    st.metric(
        "Average Final Grade",
        f"{filtered_df['G3'].mean():.2f}"
    )


with col3:

    st.metric(
        "Average G1",
        f"{filtered_df['G1'].mean():.2f}"
    )


with col4:

    st.metric(
        "Average G2",
        f"{filtered_df['G2'].mean():.2f}"
    )


# ============================================================
# ANALYTICAL VISUALIZATIONS
# ============================================================

st.subheader("📈 Performance Analysis")


# ============================================================
# STUDY TIME VS FINAL GRADE
# ============================================================

studytime_analysis = (
    filtered_df
    .groupby("studytime")["G3"]
    .mean()
    .reset_index()
)


studytime_labels = {

    1: "<2 hours",

    2: "2-5 hours",

    3: "5-10 hours",

    4: ">10 hours"
}


studytime_analysis["Study Time"] = (
    studytime_analysis["studytime"]
    .map(studytime_labels)
)


studytime_order = [

    "<2 hours",

    "2-5 hours",

    "5-10 hours",

    ">10 hours"
]


studytime_analysis["Study Time"] = pd.Categorical(

    studytime_analysis["Study Time"],

    categories=studytime_order,

    ordered=True
)


studytime_analysis = (
    studytime_analysis
    .sort_values("Study Time")
    .rename(
        columns={
            "G3": "Average Final Grade"
        }
    )
)


# ============================================================
# PREVIOUS FAILURES VS FINAL GRADE
# ============================================================

failure_analysis = (
    filtered_df
    .groupby("failures")["G3"]
    .mean()
    .reset_index()
    .rename(
        columns={
            "G3": "Average Final Grade"
        }
    )
)


# ============================================================
# SUBJECT VS FINAL GRADE
# ============================================================

subject_analysis = (
    filtered_df
    .groupby("subject")["G3"]
    .mean()
    .reset_index()
    .rename(
        columns={
            "G3": "Average Final Grade"
        }
    )
)


# ============================================================
# PERFORMANCE CATEGORY DISTRIBUTION
# ============================================================

performance_order = [

    "Low",

    "Medium",

    "High"
]


performance_counts = (
    filtered_df["performance_category"]
    .value_counts()
    .reindex(
        performance_order,
        fill_value=0
    )
)


performance_counts = performance_counts.rename(
    "Student Count"
)


# ============================================================
# ABSENCE CATEGORY VS FINAL GRADE
# ============================================================

absence_category = pd.cut(

    filtered_df["absences"],

    bins=[
        -1,
        5,
        10,
        20,
        float("inf")
    ],

    labels=[

        "Very Low",

        "Moderate",

        "High",

        "Very High"
    ]
)


absence_analysis = (

    filtered_df
    .assign(
        absence_category=absence_category
    )

    .groupby(
        "absence_category",
        observed=True
    )["G3"]

    .mean()

    .reset_index()

    .rename(
        columns={
            "G3": "Average Final Grade"
        }
    )
)


# ============================================================
# ROW 1
# STUDY TIME + FAILURES
# ============================================================

col1, col2 = st.columns(2)


with col1:

    st.markdown(
        "#### 📚 Study Time vs Final Grade"
    )

    st.bar_chart(

        studytime_analysis.set_index(
            "Study Time"
        )["Average Final Grade"]

    )


with col2:

    st.markdown(
        "#### 📉 Previous Failures vs Final Grade"
    )

    st.bar_chart(

        failure_analysis.set_index(
            "failures"
        )["Average Final Grade"]

    )


# ============================================================
# ROW 2
# SUBJECT + PERFORMANCE DISTRIBUTION
# ============================================================

col1, col2 = st.columns(2)


with col1:

    st.markdown(
        "#### 📚 Subject vs Final Grade"
    )

    st.bar_chart(

        subject_analysis.set_index(
            "subject"
        )["Average Final Grade"]

    )


with col2:

    st.markdown(
        "#### 🎯 Performance Category Distribution"
    )

    st.bar_chart(
        performance_counts
    )


# ============================================================
# ROW 3
# ABSENCE ANALYSIS
# ============================================================

st.markdown(
    "#### 📅 Absence Category vs Final Grade"
)


st.bar_chart(

    absence_analysis.set_index(
        "absence_category"
    )["Average Final Grade"]

)


# ============================================================
# CORRELATION ANALYSIS
# ============================================================

st.markdown(
    "#### 🔬 Correlation with Final Grade (G3)"
)


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


correlation_labels = {

    "studytime":
        "Study Time",

    "failures":
        "Previous Failures",

    "absences":
        "Absences",

    "G1":
        "G1",

    "G2":
        "G2",

    "Medu":
        "Mother's Education",

    "Fedu":
        "Father's Education",

    "traveltime":
        "Travel Time",

    "freetime":
        "Free Time",

    "goout":
        "Going Out",

    "health":
        "Health"
}


correlation_results = []


for column in correlation_columns:

    correlation = (
        filtered_df[column]
        .corr(filtered_df["G3"])
    )

    correlation_results.append({

        "Factor":
            correlation_labels[column],

        "Correlation":
            correlation

    })


correlation_df = pd.DataFrame(
    correlation_results
)


correlation_df = (
    correlation_df
    .sort_values(
        "Correlation",
        ascending=False
    )
)


st.bar_chart(

    correlation_df.set_index(
        "Factor"
    )["Correlation"]

)


# ============================================================
# DATASET INFORMATION
# ============================================================

st.subheader(
    "📋 Dataset Information"
)


col1, col2 = st.columns(2)


with col1:

    st.write(
        "**Records:**",
        len(filtered_df)
    )

    # Keep the original dataset's 20 columns
    st.write(
        "**Columns:**",
        len(df.columns)
    )


with col2:

    st.write(

        "**Average Final Grade:**",

        f"{filtered_df['G3'].mean():.2f}"

    )


    st.write(

        "**Maximum Final Grade:**",

        filtered_df["G3"].max()

    )


# ============================================================
# FILTERED DATA PREVIEW
# ============================================================

with st.expander(
    "View filtered dataset"
):

    st.dataframe(

        filtered_df,

        use_container_width=True

    )