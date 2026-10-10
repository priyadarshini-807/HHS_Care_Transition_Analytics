# ======================================
# HHS CARE TRANSITION ANALYTICS DASHBOARD
# ======================================

import streamlit as st
import pandas as pd

# ======================================
# PAGE CONFIGURATION
# ======================================

st.set_page_config(
    page_title="HHS Care Transition Dashboard",
    page_icon="📊",
    layout="wide"
)

# ======================================
# TITLE
# ======================================

st.title("📊 HHS Care Transition Analytics Dashboard")

st.markdown("""
This dashboard analyzes care-transition efficiency, discharge outcomes,
pipeline bottlenecks, and outcome stability within the HHS
Unaccompanied Alien Children Program.
""")

# ======================================
# LOAD DATA
# ======================================

df = pd.read_csv("outputs/cleaned_hhs_data.csv")

df["Date"] = pd.to_datetime(df["Date"])

# Sort chronologically
df = df.sort_values("Date").reset_index(drop=True)

# ======================================
# SIDEBAR FILTERS
# ======================================

st.sidebar.header("📅 Dashboard Filters")

start_date = st.sidebar.date_input(
    "Start Date",
    value=df["Date"].min().date()
)

end_date = st.sidebar.date_input(
    "End Date",
    value=df["Date"].max().date()
)

# Check date range
if start_date > end_date:
    st.error("Start Date cannot be later than End Date.")
    st.stop()

# Filter dataset
filtered_df = df[
    (df["Date"] >= pd.to_datetime(start_date)) &
    (df["Date"] <= pd.to_datetime(end_date))
].copy()

# ======================================
# DATASET INFORMATION
# ======================================

st.sidebar.markdown("---")
st.sidebar.write(
    f"**Days Selected:** {len(filtered_df):,}"
)

# ======================================
# KPI CALCULATIONS
# ======================================

total_apprehended = filtered_df[
    "Children apprehended and placed in CBP custody*"
].sum()

total_transferred = filtered_df[
    "Children transferred out of CBP custody"
].sum()

total_cbp_custody = filtered_df[
    "Children in CBP custody"
].sum()

total_hhs_care = filtered_df[
    "Children in HHS Care"
].sum()

total_discharged = filtered_df[
    "Children discharged from HHS Care"
].sum()

# --------------------------------------
# Transfer Efficiency Ratio
# --------------------------------------

if total_cbp_custody != 0:
    transfer_ratio = (
        total_transferred / total_cbp_custody
    ) * 100
else:
    transfer_ratio = 0

# --------------------------------------
# Discharge Effectiveness Index
# --------------------------------------

if total_hhs_care != 0:
    discharge_effectiveness = (
        total_discharged / total_hhs_care
    ) * 100
else:
    discharge_effectiveness = 0

# --------------------------------------
# Pipeline Throughput
# --------------------------------------

if total_apprehended != 0:
    pipeline_throughput = (
        total_discharged / total_apprehended
    ) * 100
else:
    pipeline_throughput = 0

# --------------------------------------
# Backlog Accumulation Rate
# Definition:
# Percentage of days where inflow > outflow
# --------------------------------------

filtered_df["Inflow"] = filtered_df[
    "Children apprehended and placed in CBP custody*"
]

filtered_df["Outflow"] = filtered_df[
    "Children discharged from HHS Care"
]

filtered_df["Backlog Change"] = (
    filtered_df["Inflow"] -
    filtered_df["Outflow"]
)

bottleneck_days = filtered_df[
    filtered_df["Backlog Change"] > 0
]

if len(filtered_df) > 0:
    backlog_accumulation_rate = (
        len(bottleneck_days) /
        len(filtered_df)
    ) * 100
else:
    backlog_accumulation_rate = 0

# --------------------------------------
# Outcome Stability Score
# Definition:
# 100 - discharge coefficient of variation
# --------------------------------------

discharge_mean = filtered_df[
    "Children discharged from HHS Care"
].mean()

discharge_std = filtered_df[
    "Children discharged from HHS Care"
].std()

if discharge_mean != 0:

    discharge_cv = (
        discharge_std /
        discharge_mean
    ) * 100

    outcome_stability_score = max(
        0,
        100 - discharge_cv
    )

else:

    discharge_cv = 0
    outcome_stability_score = 0


# ======================================
# DATASET PREVIEW
# ======================================

st.subheader("📋 Dataset Preview")

st.dataframe(
    filtered_df[
        [
            "Date",
            "Children apprehended and placed in CBP custody*",
            "Children in CBP custody",
            "Children transferred out of CBP custody",
            "Children in HHS Care",
            "Children discharged from HHS Care"
        ]
    ].head(10),
    width="stretch"
)

# ======================================
# KEY PERFORMANCE INDICATORS
# ======================================

st.subheader("📊 Key Performance Indicators")

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.metric(
        "Transfer Efficiency",
        f"{transfer_ratio:.2f}%"
    )

with kpi2:
    st.metric(
        "Discharge Effectiveness",
        f"{discharge_effectiveness:.2f}%"
    )

with kpi3:
    st.metric(
        "Pipeline Throughput",
        f"{pipeline_throughput:.2f}%"
    )

with kpi4:
    st.metric(
        "Backlog Accumulation",
        f"{backlog_accumulation_rate:.2f}%"
    )

with kpi5:
    st.metric(
        "Outcome Stability",
        f"{outcome_stability_score:.2f}/100"
    )


st.caption(
    "Backlog Accumulation Rate = percentage of selected days "
    "where inflow exceeded outflow. "
    "Outcome Stability Score = 100 minus discharge coefficient "
    "of variation, clipped at zero."
)


# ======================================
# BASIC PROGRAM METRICS
# ======================================

st.subheader("📌 Program Activity Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Apprehended",
        f"{int(total_apprehended):,}"
    )

with col2:
    st.metric(
        "Total Transferred",
        f"{int(total_transferred):,}"
    )

with col3:
    st.metric(
        "Total Discharged",
        f"{int(total_discharged):,}"
    )

col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "Average HHS Population",
        f"{filtered_df['Children in HHS Care'].mean():,.0f}"
    )

with col5:
    st.metric(
        "Peak HHS Population",
        f"{int(filtered_df['Children in HHS Care'].max()):,}"
    )

with col6:
    st.metric(
        "Average Daily Apprehensions",
        f"{filtered_df['Children apprehended and placed in CBP custody*'].mean():.2f}"
    )


# ======================================
# CARE PIPELINE FLOW
# ======================================

st.subheader("🔄 Care Pipeline Flow")

pipeline1, pipeline2, pipeline3 = st.columns(3)

with pipeline1:
    st.metric(
        "1️⃣ CBP Apprehensions",
        f"{int(total_apprehended):,}"
    )

with pipeline2:
    st.metric(
        "2️⃣ Transfers to HHS",
        f"{int(total_transferred):,}"
    )

with pipeline3:
    st.metric(
        "3️⃣ HHS Discharges",
        f"{int(total_discharged):,}"
    )

st.markdown(
    """
    **CBP Apprehension → CBP Custody → HHS Care → Sponsor Placement / Discharge**
    """
)


# ======================================
# RATIO-BASED METRIC TOGGLE
# ======================================

st.subheader("⚙️ Ratio-Based Metric Analysis")

metric_option = st.radio(
    "Select a ratio to analyze:",
    [
        "Transfer Efficiency Ratio",
        "Discharge Effectiveness Index",
        "Pipeline Throughput Rate"
    ],
    horizontal=True
)

if metric_option == "Transfer Efficiency Ratio":

    st.info(
        f"Transfer Efficiency Ratio: **{transfer_ratio:.2f}%**"
    )

elif metric_option == "Discharge Effectiveness Index":

    st.info(
        f"Discharge Effectiveness Index: "
        f"**{discharge_effectiveness:.2f}%**"
    )

else:

    st.info(
        f"Pipeline Throughput Rate: "
        f"**{pipeline_throughput:.2f}%**"
    )


# ======================================
# TRANSFER & DISCHARGE EFFICIENCY
# ======================================

st.subheader("📈 Transfer & Discharge Efficiency")

eff1, eff2 = st.columns(2)

with eff1:

    st.metric(
        "Transfer Efficiency Ratio",
        f"{transfer_ratio:.2f}%"
    )

    st.progress(
        min(transfer_ratio / 100, 1.0)
    )

with eff2:

    st.metric(
        "Discharge Effectiveness Index",
        f"{discharge_effectiveness:.2f}%"
    )

    st.progress(
        min(discharge_effectiveness / 100, 1.0)
    )


# ======================================
# APPREHENSION TREND
# ======================================

st.subheader("📈 Apprehensions Over Time")

st.line_chart(
    filtered_df.set_index("Date")[
        "Children apprehended and placed in CBP custody*"
    ]
)


# ======================================
# HHS CARE POPULATION
# ======================================

st.subheader("🏥 Children in HHS Care")

st.line_chart(
    filtered_df.set_index("Date")[
        "Children in HHS Care"
    ]
)


# ======================================
# TRANSFERS VS DISCHARGES
# ======================================

st.subheader("📊 Transfers vs Discharges")

comparison_df = filtered_df.set_index("Date")[
    [
        "Children transferred out of CBP custody",
        "Children discharged from HHS Care"
    ]
]

st.line_chart(comparison_df)


# ======================================
# BOTTLENECK DETECTION
# ======================================

st.subheader("🚨 Bottleneck Detection")

st.write(
    f"Days with higher inflow than outflow: "
    f"**{len(bottleneck_days)}**"
)

if len(bottleneck_days) > 0:

    highest_bottleneck_row = bottleneck_days.loc[
        bottleneck_days["Backlog Change"].idxmax()
    ]

    highest_bottleneck = highest_bottleneck_row[
        "Backlog Change"
    ]

    highest_bottleneck_date = (
        highest_bottleneck_row["Date"].strftime("%d %b %Y")
    )

    st.warning(
        f"⚠️ Highest daily backlog increase: "
        f"**{highest_bottleneck:.0f} children** "
        f"on **{highest_bottleneck_date}**."
    )

else:

    st.success(
        "No bottleneck days found in the selected period."
    )


st.bar_chart(
    filtered_df.set_index("Date")[
        "Backlog Change"
    ]
)


# ======================================
# SUSTAINED IMBALANCE
# ======================================

st.subheader("⏳ Sustained Imbalance Detection")

# Identify consecutive positive backlog-change periods

positive_days = (
    filtered_df["Backlog Change"] > 0
)

periods = []
start = None

for i in range(len(filtered_df)):

    if positive_days.iloc[i]:

        if start is None:
            start = i

    else:

        if start is not None:

            end = i - 1

            duration = end - start + 1

            periods.append({
                "Start Date":
                    filtered_df.iloc[start]["Date"],
                "End Date":
                    filtered_df.iloc[end]["Date"],
                "Duration (Days)":
                    duration
            })

            start = None

# Close final period
if start is not None:

    end = len(filtered_df) - 1

    duration = end - start + 1

    periods.append({
        "Start Date":
            filtered_df.iloc[start]["Date"],
        "End Date":
            filtered_df.iloc[end]["Date"],
        "Duration (Days)":
            duration
    })

imbalance_df = pd.DataFrame(periods)

sustained_df = imbalance_df[
    imbalance_df["Duration (Days)"] >= 3
] if not imbalance_df.empty else pd.DataFrame()


if not sustained_df.empty:

    st.write(
        f"Sustained imbalance periods (≥3 days): "
        f"**{len(sustained_df)}**"
    )

    longest_period = sustained_df.loc[
        sustained_df["Duration (Days)"].idxmax()
    ]

    st.warning(
        f"Longest sustained imbalance: "
        f"**{longest_period['Duration (Days)']} days** "
        f"({longest_period['Start Date'].strftime('%d %b %Y')} "
        f"to "
        f"{longest_period['End Date'].strftime('%d %b %Y')})"
    )

    st.dataframe(
    sustained_df,
    width="stretch"
)

else:

    st.success(
        "No sustained imbalance periods of 3 or more "
        "consecutive days were detected."
    )


# ======================================
# OUTCOME TREND ANALYSIS
# ======================================

st.subheader("📊 Discharge Outcome Trend")

monthly_discharge = (
    filtered_df
    .set_index("Date")[
        "Children discharged from HHS Care"
    ]
    .resample("ME")
    .mean()
)

st.line_chart(monthly_discharge)


# ======================================
# WEEKDAY VS WEEKEND
# ======================================

st.subheader("📅 Weekday vs Weekend Performance")

weekday_df = filtered_df.copy()

weekday_df["Day Type"] = weekday_df[
    "Date"
].dt.dayofweek.apply(
    lambda x: "Weekend" if x >= 5 else "Weekday"
)

weekday_summary = weekday_df.groupby(
    "Day Type"
)[
    [
        "Children transferred out of CBP custody",
        "Children discharged from HHS Care"
    ]
].mean()

st.dataframe(
    weekday_summary.round(2),
    width="stretch"
)


# ======================================
# THRESHOLD-BASED ALERTS
# ======================================

st.subheader("⚠️ Performance Alerts")

threshold = st.slider(
    "Set Discharge Effectiveness Alert Threshold (%)",
    min_value=0.0,
    max_value=10.0,
    value=2.0,
    step=0.5
)

if discharge_effectiveness < threshold:

    st.error(
        f"⚠️ Discharge Effectiveness "
        f"({discharge_effectiveness:.2f}%) is below "
        f"the selected threshold of {threshold:.1f}%."
    )

else:

    st.success(
        f"✅ Discharge Effectiveness "
        f"({discharge_effectiveness:.2f}%) is at or above "
        f"the selected threshold of {threshold:.1f}%."
    )


# ======================================
# DATA DOWNLOAD
# ======================================

st.subheader("📥 Download Filtered Dataset")

download_df = filtered_df.drop(
    columns=[
        "Inflow",
        "Outflow",
        "Backlog Change"
    ],
    errors="ignore"
)

csv = download_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Filtered Dataset",
    data=csv,
    file_name="filtered_hhs_data.csv",
    mime="text/csv"
)


# ======================================
# FOOTER
# ======================================

st.markdown("---")

st.caption(
    "HHS Care Transition Analytics | "
    "Care Transition Efficiency & Placement Outcome Analytics"
)