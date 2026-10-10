# ======================================
# HHS CARE TRANSITION ANALYTICS PROJECT
# ======================================

# ======================================
# STEP 1 - IMPORT LIBRARIES
# ======================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ======================================
# STEP 2 - LOAD DATASET
# ======================================

df = pd.read_csv("data/HHS_Unaccompanied_Alien_Children_Program.csv")

print("Original Shape:", df.shape)

# ======================================
# STEP 3 - DATA CLEANING
# ======================================

# Remove completely empty rows
df = df.dropna(how='all')

print("Shape after removing empty rows:", df.shape)

# Convert Date column
df["Date"] = pd.to_datetime(df["Date"])
# Sort data chronologically for time-series analysis
df = df.sort_values("Date").reset_index(drop=True)

# Remove commas from HHS Care column
df["Children in HHS Care"] = (
    df["Children in HHS Care"]
    .str.replace(",", "", regex=False)
)

# Convert HHS Care column to numeric
df["Children in HHS Care"] = pd.to_numeric(
    df["Children in HHS Care"],
    errors="coerce"
)

# ======================================
# STEP 4 - VERIFY CLEANED DATA
# ======================================

print("\nMissing Values:")
print(df.isnull().sum())

print("\nData Types:")
print(df.dtypes)

# ======================================
# STEP 5 - SAVE CLEANED DATASET
# ======================================

df.to_csv("outputs/cleaned_hhs_data.csv", index=False)

print("\n✅ Cleaned dataset saved successfully!")

# ======================================
# STEP 6 - EXPLORATORY DATA ANALYSIS (EDA)
# ======================================

# --------------------------------------
# Chart 1: Children Apprehended Over Time
# --------------------------------------

# Set chart style
plt.style.use("ggplot")

# Increase figure size
plt.figure(figsize=(12,6))

# Line chart
plt.plot(
    df["Date"],
    df["Children apprehended and placed in CBP custody*"],
    color="blue",
    linewidth=2
)

# Chart Title
plt.title("Children Apprehended and Placed in CBP Custody Over Time", fontsize=16)

# X and Y labels
plt.xlabel("Date")
plt.ylabel("Number of Children")

# Rotate dates
plt.xticks(rotation=45)

# Make layout neat
plt.tight_layout()

# Save graph
plt.savefig("images/chart1_cbp_apprehended.png")

# Show graph
plt.show()

print("✅ Chart 1 saved successfully!")

# --------------------------------------
# Chart 2: Children Transferred Out of CBP Custody Over Time
# --------------------------------------

# Create a new figure
plt.figure(figsize=(12,6))

# Plot the data
plt.plot(
    df["Date"],
    df["Children transferred out of CBP custody"],
    color="green",
    linewidth=2
)

# Add title and labels
plt.title("Children Transferred Out of CBP Custody Over Time", fontsize=16)
plt.xlabel("Date")
plt.ylabel("Number of Children")

# Rotate x-axis labels
plt.xticks(rotation=45)

# Add grid
plt.grid(True)

# Adjust layout
plt.tight_layout()

# Save the chart
plt.savefig("images/chart2_transferred_cbp.png")

# Display the chart
plt.show()

print("✅ Chart 2 saved successfully!")

# --------------------------------------
# Chart 3: Children in HHS Care Over Time
# --------------------------------------

# Create a new figure
plt.figure(figsize=(12,6))

# Plot the data
plt.plot(
    df["Date"],
    df["Children in HHS Care"],
    color="orange",
    linewidth=2
)

# Add title and labels
plt.title("Children in HHS Care Over Time", fontsize=16)
plt.xlabel("Date")
plt.ylabel("Number of Children")

# Rotate x-axis labels
plt.xticks(rotation=45)

# Add grid
plt.grid(True)

# Adjust layout
plt.tight_layout()

# Save the chart
plt.savefig("images/chart3_hhs_care.png")

# Display the chart
plt.show()

print("✅ Chart 3 saved successfully!")

# --------------------------------------
# Chart 4: Children Discharged from HHS Care
# --------------------------------------

# Create a new figure
plt.figure(figsize=(12,6))

# Plot the data
plt.plot(
    df["Date"],
    df["Children discharged from HHS Care"],
    color="red",
    linewidth=2
)

# Add title and labels
plt.title("Children Discharged from HHS Care Over Time", fontsize=16)
plt.xlabel("Date")
plt.ylabel("Number of Children")

# Rotate x-axis labels
plt.xticks(rotation=45)

# Add grid
plt.grid(True)

# Adjust layout
plt.tight_layout()

# Save the chart
plt.savefig("images/chart4_hhs_discharged.png")

# Display the chart
plt.show()

print("✅ Chart 4 saved successfully!")

# --------------------------------------
# Chart 5: Combined Trend Analysis
# --------------------------------------

plt.figure(figsize=(14,7))

plt.plot(
    df["Date"],
    df["Children apprehended and placed in CBP custody*"],
    label="Apprehended",
    linewidth=2
)

plt.plot(
    df["Date"],
    df["Children transferred out of CBP custody"],
    label="Transferred",
    linewidth=2
)

plt.plot(
    df["Date"],
    df["Children in HHS Care"],
    label="HHS Care",
    linewidth=2
)

plt.plot(
    df["Date"],
    df["Children discharged from HHS Care"],
    label="Discharged",
    linewidth=2
)

plt.title("Overall Care Transition Trend", fontsize=16)
plt.xlabel("Date")
plt.ylabel("Number of Children")

plt.xticks(rotation=45)

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig("images/chart5_overall_trend.png")

plt.show()

print("✅ Chart 5 saved successfully!")

# --------------------------------------
# Chart 6: Correlation Heatmap
# --------------------------------------

plt.figure(figsize=(10,8))

correlation = df.drop(columns=["Date"]).corr()

sns.heatmap(
    correlation,
    annot=True,
    cmap="coolwarm",
    linewidths=0.5
)

plt.title("Correlation Between Variables")

plt.tight_layout()

plt.savefig("images/chart6_correlation_heatmap.png")

plt.show()

print("✅ Chart 6 saved successfully!")

# --------------------------------------
# Chart 7: Distribution of Numerical Variables
# --------------------------------------

columns = [
    "Children apprehended and placed in CBP custody*",
    "Children in CBP custody",
    "Children transferred out of CBP custody",
    "Children in HHS Care",
    "Children discharged from HHS Care"
]

for column in columns:

    plt.figure(figsize=(8,5))

    plt.hist(df[column], bins=25)

    plt.title(f"Distribution of {column}")

    plt.xlabel(column)
    plt.ylabel("Frequency")

    plt.tight_layout()

    filename = column.replace(" ", "_").replace("*","")

    plt.savefig(f"images/{filename}_distribution.png")

    plt.show()

print("✅ Chart 7 completed successfully!")

# --------------------------------------
# Chart 8: Boxplots
# --------------------------------------

plt.figure(figsize=(14,7))

sns.boxplot(data=df.drop(columns=["Date"]))

plt.xticks(rotation=30)

plt.title("Boxplot of Numerical Variables")

plt.tight_layout()

plt.savefig("images/chart8_boxplot.png")

plt.show()

print("✅ Chart 8 saved successfully!")

# --------------------------------------
# Chart 9: Monthly Average Apprehensions
# --------------------------------------

df["Month"] = df["Date"].dt.month_name()

monthly_avg = (
    df.groupby("Month")["Children apprehended and placed in CBP custody*"]
      .mean()
      .reindex([
          "January","February","March","April","May","June",
          "July","August","September","October","November","December"
      ])
)

plt.figure(figsize=(12,6))

monthly_avg.plot(kind="bar")

plt.title("Average Monthly Apprehensions")

plt.ylabel("Average Number of Children")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("images/chart9_monthly_average.png")

plt.show()

print("✅ Chart 9 saved successfully!")

# --------------------------------------
# Chart 10: Pairplot
# --------------------------------------

sns.pairplot(
    df.drop(columns=["Date"])
)

plt.savefig("images/chart10_pairplot.png")

plt.show()

print("✅ Chart 10 saved successfully!")

# ======================================
# STEP 7 - KPI CALCULATIONS
# ======================================

total_apprehended = df["Children apprehended and placed in CBP custody*"].sum()

print("\nTotal Children Apprehended:")
print(total_apprehended)

total_transferred = df["Children transferred out of CBP custody"].sum()

print("\nTotal Children Transferred:")
print(total_transferred)

total_discharged = df["Children discharged from HHS Care"].sum()

print("\nTotal Children Discharged:")
print(total_discharged)

avg_apprehended = df["Children apprehended and placed in CBP custody*"].mean()

print("\nAverage Daily Apprehensions:")
print(round(avg_apprehended,2))

avg_transfer = df["Children transferred out of CBP custody"].mean()

print("\nAverage Daily Transfers:")
print(round(avg_transfer,2))

avg_discharge = df["Children discharged from HHS Care"].mean()

print("\nAverage Daily Discharges:")
print(round(avg_discharge,2))

max_hhs = df["Children in HHS Care"].max()

print("\nMaximum Children in HHS Care:")
print(max_hhs)

transfer_efficiency = (
    total_transferred / total_apprehended
) * 100

print("\nTransfer Efficiency:")
print(f"{transfer_efficiency:.2f}%")

discharge_efficiency = (
    total_discharged / total_transferred
) * 100

print("\nDischarge Efficiency:")
print(f"{discharge_efficiency:.2f}%")

average_hhs = df["Children in HHS Care"].mean()

print("\nAverage HHS Population:")
print(round(average_hhs,2))

print("\n========== ADDITIONAL KPIs ==========")

# Total records (days)
total_days = len(df)

# Average children currently in HHS care
avg_hhs_population = df["Children in HHS Care"].mean()

# Peak HHS care population
peak_hhs_population = df["Children in HHS Care"].max()

# Peak apprehensions
peak_apprehensions = df["Children apprehended and placed in CBP custody*"].max()

# Peak transfers
peak_transfers = df["Children transferred out of CBP custody"].max()

# Peak discharges
peak_discharges = df["Children discharged from HHS Care"].max()

print(f"Total Days Analysed: {total_days}")
print(f"Average HHS Population: {avg_hhs_population:.2f}")
print(f"Peak HHS Population: {peak_hhs_population}")
print(f"Peak Daily Apprehensions: {peak_apprehensions}")
print(f"Peak Daily Transfers: {peak_transfers}")
print(f"Peak Daily Discharges: {peak_discharges}")

kpi_summary = pd.DataFrame({
    "KPI": [
        "Total Apprehended",
        "Total Transferred",
        "Total Discharged",
        "Average Daily Apprehensions",
        "Average Daily Transfers",
        "Average Daily Discharges",
        "Average HHS Population",
        "Peak HHS Population"
    ],
    "Value": [
        total_apprehended,
        total_transferred,
        total_discharged,
        round(avg_apprehended,2),
        round(avg_transfer,2),
        round(avg_discharge,2),
        round(avg_hhs_population,2),
        peak_hhs_population
    ]
})

kpi_summary.to_csv("outputs/kpi_summary.csv", index=False)

print("\n✅ KPI Summary saved successfully!")

# ======================================
# STEP 8 - PROJECT-SPECIFIC ANALYTICS
# ======================================

# Transfer Efficiency Ratio
transfer_efficiency_ratio = (
    df["Children transferred out of CBP custody"].sum()
    / df["Children in CBP custody"].sum()
) * 100

print("\nTransfer Efficiency Ratio:")
print(f"{transfer_efficiency_ratio:.2f}%")


# Discharge Effectiveness
discharge_effectiveness = (
    df["Children discharged from HHS Care"].sum()
    / df["Children in HHS Care"].sum()
) * 100

print("\nDischarge Effectiveness:")
print(f"{discharge_effectiveness:.2f}%")


# Pipeline Throughput Rate
pipeline_throughput = (
    df["Children discharged from HHS Care"].sum()
    / df["Children apprehended and placed in CBP custody*"].sum()
) * 100

print("\nPipeline Throughput Rate:")
print(f"{pipeline_throughput:.2f}%")


# ======================================
# BACKLOG ANALYSIS
# ======================================

df["Daily Inflow"] = df[
    "Children apprehended and placed in CBP custody*"
]

df["Daily Outflow"] = df[
    "Children discharged from HHS Care"
]

df["Backlog Change"] = (
    df["Daily Inflow"] - df["Daily Outflow"]
)

df["Cumulative Backlog"] = df["Backlog Change"].cumsum()

print("\nMaximum Cumulative Backlog:")
print(f"{df['Cumulative Backlog'].max():.2f}")


# Save analytical dataset
df.to_csv(
    "outputs/analytical_hhs_data.csv",
    index=False
)

print("\n✅ Project-specific analytics completed!")

# ======================================
# STEP 9 - WEEKDAY VS WEEKEND ANALYSIS
# ======================================

df["Day Type"] = df["Date"].dt.dayofweek.map(
    lambda x: "Weekend" if x >= 5 else "Weekday"
)

weekday_analysis = (
    df.groupby("Day Type")[
        [
            "Children transferred out of CBP custody",
            "Children discharged from HHS Care"
        ]
    ].mean()
)

print("\nWeekday vs Weekend Analysis:")
print(weekday_analysis)

# ======================================
# STEP 10 - MONTH-OVER-MONTH DISCHARGE TREND
# ======================================

monthly_discharge = (
    df.set_index("Date")["Children discharged from HHS Care"]
    .resample("ME")
    .mean()
)

print("\nMonthly Average Discharges:")
print(monthly_discharge)


# ======================================
# STEP 11 - STAGNATION / BOTTLENECK ANALYSIS
# ======================================

df["Inflow vs Outflow"] = (
    df["Children apprehended and placed in CBP custody*"]
    - df["Children discharged from HHS Care"]
)

bottleneck_days = df[df["Inflow vs Outflow"] > 0]

print("\nBottleneck Analysis:")
print("Days with more inflow than outflow:", len(bottleneck_days))

if len(bottleneck_days) > 0:
    highest_bottleneck = bottleneck_days.loc[
        bottleneck_days["Inflow vs Outflow"].idxmax()
    ]

    print("\nHighest Bottleneck Day:")
    print("Date:", highest_bottleneck["Date"].date())
    print("Backlog Increase:", highest_bottleneck["Inflow vs Outflow"])

    # ======================================
# STEP 11A - SUSTAINED IMBALANCE ANALYSIS
# ======================================

print("\n======================================")
print("SUSTAINED IMBALANCE ANALYSIS")
print("======================================")


# A day is considered an imbalance day when
# inflow is greater than successful outflow.

df["Imbalance Flag"] = (
    df["Inflow vs Outflow"] > 0
)


# --------------------------------------
# Identify consecutive imbalance periods
# --------------------------------------

periods = []

start_date = None
end_date = None
period_length = 0

for i in range(len(df)):

    current_date = df.iloc[i]["Date"]
    is_imbalance = df.iloc[i]["Imbalance Flag"]

    if is_imbalance:

        if start_date is None:
            start_date = current_date

        end_date = current_date
        period_length += 1

    else:

        if period_length > 0:

            periods.append({
                "Start Date": start_date,
                "End Date": end_date,
                "Duration (Days)": period_length
            })

        start_date = None
        end_date = None
        period_length = 0


# Capture final period if dataset ends
# during an imbalance period.

if period_length > 0:

    periods.append({
        "Start Date": start_date,
        "End Date": end_date,
        "Duration (Days)": period_length
    })


imbalance_periods = pd.DataFrame(periods)


# --------------------------------------
# Sustained imbalance = 3 or more days
# --------------------------------------

sustained_imbalance = imbalance_periods[
    imbalance_periods["Duration (Days)"] >= 3
].copy()


print(
    f"Total sustained imbalance periods: "
    f"{len(sustained_imbalance)}"
)


if len(sustained_imbalance) > 0:

    longest_period = sustained_imbalance.loc[
        sustained_imbalance["Duration (Days)"].idxmax()
    ]

    print("\nLongest Sustained Imbalance:")
    print(
        "Start Date:",
        longest_period["Start Date"].date()
    )
    print(
        "End Date:",
        longest_period["End Date"].date()
    )
    print(
        "Duration:",
        int(longest_period["Duration (Days)"]),
        "days"
    )

else:

    print(
        "No sustained imbalance periods "
        "of 3 or more consecutive days."
    )


# Save sustained imbalance periods

sustained_imbalance.to_csv(
    "outputs/sustained_imbalance_periods.csv",
    index=False
)


print(
    "\n✅ Sustained imbalance analysis saved!"
)


# ======================================
# STEP 11B - PROLONGED STAGNATION ANALYSIS
# ======================================

print("\n======================================")
print("PROLONGED STAGNATION ANALYSIS")
print("======================================")


# A prolonged stagnation period is defined here
# as 7 or more consecutive days where inflow
# exceeds successful outflow.

prolonged_stagnation = imbalance_periods[
    imbalance_periods["Duration (Days)"] >= 7
].copy()


print(
    f"Total prolonged stagnation periods: "
    f"{len(prolonged_stagnation)}"
)


if len(prolonged_stagnation) > 0:

    longest_stagnation = prolonged_stagnation.loc[
        prolonged_stagnation["Duration (Days)"].idxmax()
    ]

    print("\nLongest Prolonged Stagnation:")
    print(
        "Start Date:",
        longest_stagnation["Start Date"].date()
    )
    print(
        "End Date:",
        longest_stagnation["End Date"].date()
    )
    print(
        "Duration:",
        int(longest_stagnation["Duration (Days)"]),
        "days"
    )

else:

    print(
        "No prolonged stagnation periods "
        "of 7 or more consecutive days."
    )


# Save prolonged stagnation periods

prolonged_stagnation.to_csv(
    "outputs/prolonged_stagnation_periods.csv",
    index=False
)


print(
    "\n✅ Prolonged stagnation analysis saved!"
)


# ======================================
# STEP 12 - OUTCOME STABILITY / VARIABILITY
# ======================================

discharge_mean = df[
    "Children discharged from HHS Care"
].mean()

discharge_std = df[
    "Children discharged from HHS Care"
].std()

coefficient_of_variation = (
    discharge_std / discharge_mean
) * 100

print("\nOutcome Stability Analysis:")
print(f"Average Daily Discharges: {discharge_mean:.2f}")
print(f"Discharge Standard Deviation: {discharge_std:.2f}")
print(f"Discharge Variability (CV): {coefficient_of_variation:.2f}%")


# ======================================
# STEP 13 - SAVE FINAL ANALYTICAL DATASET
# ======================================

df.to_csv(
    "outputs/analytical_hhs_data.csv",
    index=False
)

print("\n✅ Final analytical dataset saved successfully!")
print("\n======================================")
print("ANALYTICAL KPI CALCULATIONS COMPLETED")
print("======================================")

# ======================================
# STEP 14 - FINAL PROJECT KPIs
# ======================================

print("\n======================================")
print("FINAL PROJECT KPIs")
print("======================================")

# --------------------------------------
# 1. Transfer Efficiency Ratio
# --------------------------------------

transfer_efficiency = (
    df["Children transferred out of CBP custody"].sum()
    / df["Children in CBP custody"].sum()
) * 100

print(f"Transfer Efficiency Ratio: {transfer_efficiency:.2f}%")


# --------------------------------------
# 2. Discharge Effectiveness Index
# --------------------------------------

discharge_effectiveness = (
    df["Children discharged from HHS Care"].sum()
    / df["Children in HHS Care"].sum()
) * 100

print(
    f"Discharge Effectiveness Index: "
    f"{discharge_effectiveness:.2f}%"
)


# --------------------------------------
# 3. Pipeline Throughput Rate
# --------------------------------------

pipeline_throughput = (
    df["Children discharged from HHS Care"].sum()
    / df["Children apprehended and placed in CBP custody*"].sum()
) * 100

print(
    f"Pipeline Throughput Rate: "
    f"{pipeline_throughput:.2f}%"
)


# --------------------------------------
# 4. Backlog Accumulation Rate
# --------------------------------------

# Number of days where inflow exceeded outflow
bottleneck_days_count = len(
    df[df["Inflow vs Outflow"] > 0]
)

total_days = len(df)

backlog_accumulation_rate = (
    bottleneck_days_count / total_days
) * 100

print(
    f"Backlog Accumulation Rate: "
    f"{backlog_accumulation_rate:.2f}%"
)


# --------------------------------------
# 5. Outcome Stability Score
# --------------------------------------

discharge_mean = df[
    "Children discharged from HHS Care"
].mean()

discharge_std = df[
    "Children discharged from HHS Care"
].std()

if discharge_mean != 0:

    coefficient_variation = (
        discharge_std / discharge_mean
    ) * 100

    # Convert variability into a stability score.
    # Lower variability = higher stability.
    outcome_stability_score = max(
        0,
        100 - coefficient_variation
    )

else:

    coefficient_variation = 0
    outcome_stability_score = 0


print(
    f"Outcome Stability Score: "
    f"{outcome_stability_score:.2f}/100"
)


# --------------------------------------
# Save Final KPI Summary
# --------------------------------------

final_kpi_summary = pd.DataFrame({

    "KPI": [
        "Transfer Efficiency Ratio",
        "Discharge Effectiveness Index",
        "Pipeline Throughput Rate",
        "Backlog Accumulation Rate",
        "Outcome Stability Score"
    ],

    "Value": [
        round(transfer_efficiency, 2),
        round(discharge_effectiveness, 2),
        round(pipeline_throughput, 2),
        round(backlog_accumulation_rate, 2),
        round(outcome_stability_score, 2)
    ],

    "Unit": [
        "%",
        "%",
        "%",
        "%",
        "Score / 100"
    ]
})

final_kpi_summary.to_csv(
    "outputs/final_kpi_summary.csv",
    index=False
)

print("\n✅ Final KPI summary saved successfully!")