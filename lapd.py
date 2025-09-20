import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
from helper import descent_map
import os

# Create a folder to save figures if it doesn't exist
figures_folder = "figures"
os.makedirs(figures_folder, exist_ok=True)

# --------------------------
# 1. Load the dataset
# --------------------------
# df = pd.read_csv("lapd_crime_data.csv", low_memory=False)
url = "https://data.lacity.org/api/views/2nrs-mtv8/rows.csv?accessType=DOWNLOAD"
df = pd.read_csv(url, low_memory=False)

# --------------------------
# 2. Standardize column names (lowercase, underscores)
# --------------------------
df.columns = df.columns.str.strip().str.lower().str.replace(r"[^\w]+", "_", regex=True)

# --------------------------
# 3. Handle dates and times
# --------------------------
# Use "date_occ" if available, otherwise "date_rptd"
if "date_occ" in df.columns:
    df["date_occ"] = pd.to_datetime(df["date_occ"], errors="coerce")
elif "date_rptd" in df.columns:
    df["date_occ"] = pd.to_datetime(df["date_rptd"], errors="coerce")

# Parse time (time_occ like 2300 -> 23:00)
if "time_occ" in df.columns:
    df["time_occ"] = df["time_occ"].astype(str).str.zfill(4).str[-4:]
    df["hour"] = pd.to_numeric(df["time_occ"].str[:2], errors="coerce")
else:
    df["hour"] = np.nan

# Derive more columns
df["year"] = df["date_occ"].dt.year
df["month"] = df["date_occ"].dt.month
df["weekday"] = df["date_occ"].dt.day_name()
df["month_year"] = df["date_occ"].dt.to_period("M")

# --------------------------
# 4. KPIs (summary)
# --------------------------
print("\n========= KPI Summary =========")
print("Total records:               ", len(df))
print("Date range:                  ", df["date_occ"].min(), "to", df["date_occ"].max())

if "crm_cd_desc" in df.columns:
    print("Unique crime types:          ", df["crm_cd_desc"].nunique())
    top_crime = df["crm_cd_desc"].value_counts().idxmax()
    print("Most common crime type:      ", top_crime)

if "area_name" in df.columns:
    top_area = df["area_name"].value_counts().idxmax()
    print("Top area by count:           ", top_area)
    print(f"Crimes in {top_area}:           ", df["area_name"].value_counts().max())

# Average crimes per month
if "month_year" in df.columns:
    avg_monthly = df.groupby("month_year").size().mean()
    print(f"Average crimes per month:     {avg_monthly:.1f}")

# Victim stats
if "vict_age" in df.columns:
    valid_ages = pd.to_numeric(df["vict_age"], errors="coerce")
    valid_ages = valid_ages[(valid_ages > 0) & (valid_ages < 120)]
    if len(valid_ages) > 0:
        print(f"Average victim age:           {valid_ages.mean():.1f}")

if "vict_descent" in df.columns:
    max_descent = df["vict_descent"].fillna("X").value_counts().nlargest(1)
    print("Top victim descent code:")
    for code, count in max_descent.items():
        print(f"      {descent_map[code]}: {count}")

print("===============================")


# --------------------------
# 5. Plots
# --------------------------

# Monthly trend
monthly = df.groupby("month_year").size()
plt.figure(figsize=(12,4))
monthly.plot(color="cyan", label="Monthly Crimes")
monthly.rolling(12, min_periods=1).mean().plot(linewidth=2, color="orange", label="12-Month Rolling Avg")
plt.title("Crimes per Month")
plt.xlabel("Month")
plt.ylabel("Count")
# Legend
plt.legend(facecolor="#0a1a2f", edgecolor="white", labelcolor="white")
plt.savefig(os.path.join(figures_folder, "monthly_trend.png"), dpi=300, facecolor='#0a1a2f')


# Crimes by weekday
plt.figure(figsize=(8,4))
sns.countplot(x="weekday", data=df,
              order=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
plt.title("Crimes by Weekday")
plt.savefig(os.path.join(figures_folder, "crimes_weekday.png"), dpi=300, facecolor='#0a1a2f')


# Crimes by hour
plt.figure(figsize=(10,4))
sns.countplot(x="hour", data=df)
plt.title("Crimes by Hour")
plt.savefig(os.path.join(figures_folder, "crimes_hours.png"), dpi=300, facecolor='#0a1a2f')


# Heatmap: Hour vs Weekday
pivot = pd.pivot_table(df, index="hour", columns="weekday", values="dr_no", aggfunc="count", fill_value=0)
pivot = pivot[["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]]  # reorder
plt.figure(figsize=(9,6))
sns.heatmap(pivot, cmap="YlOrRd")
plt.title("Heatmap: Crimes by Hour and Weekday")
plt.savefig(os.path.join(figures_folder, "hour_weekday_heatmap.png"), dpi=300, facecolor='#0a1a2f')


# Top areas
if "area_name" in df.columns:
    plt.figure(figsize=(10,5))
    df["area_name"].value_counts().nlargest(10).plot(kind="barh")
    plt.title("Top 10 Areas by Crime Count")
    plt.savefig(os.path.join(figures_folder, "top_areas.png"), dpi=300, facecolor='#0a1a2f')
    

# Top crimes
if "crm_cd_desc" in df.columns:
    plt.figure(figsize=(10,6))
    df["crm_cd_desc"].value_counts().nlargest(15).plot(kind="bar")
    plt.title("Top 15 Crimes")
    plt.xticks(rotation=45, ha="right")
    plt.savefig(os.path.join(figures_folder, "top_crimes.png"), dpi=300, facecolor='#0a1a2f')
    

# Victim age
if "vict_age" in df.columns:
    ages = pd.to_numeric(df["vict_age"], errors="coerce")
    ages = ages[(ages > 0) & (ages < 120)]
    plt.figure(figsize=(9,4))
    plt.hist(ages, bins=20, color="skyblue", edgecolor="black")
    plt.title("Victim Age Distribution")
    plt.xlabel("Age")
    plt.ylabel("Count")
    plt.savefig(os.path.join(figures_folder, "victim_age.png"), dpi=300, facecolor='#0a1a2f')
    

# Victim sex
if "vict_sex" in df.columns:
    plt.figure(figsize=(6,6))
    
    counts = df["vict_sex"].fillna("Unknown").value_counts()
    labels = counts.index
    sizes = counts.values
    colors = ["#ff6f61", "#6ec6ff", "#ffd166", "#06d6a0"] 
    
    plt.pie(
        sizes,
        labels=labels,
        colors=colors[:len(labels)],
        autopct="%1.1f%%")
    
    plt.title("Victim Sex Distribution")
    plt.ylabel("")
    plt.savefig(os.path.join(figures_folder, "victim_sex.png"), dpi=300, facecolor='#0a1a2f')

    

# Victim descent
if "vict_descent" in df.columns:
    plt.figure(figsize=(9,5))
    (df["vict_descent"].fillna("X").map(descent_map).value_counts().nlargest(10).plot(kind="bar"))
    plt.title("Top 10 Victim Descent Groups")
    plt.ylabel("Count")
    plt.xlabel("Descent")
    plt.xticks(rotation=45, ha="right")
    plt.savefig(os.path.join(figures_folder, "victim_descent.png"), dpi=300, facecolor='#0a1a2f')


# Scatter of lat/lon
if {"lat","lon"}.issubset(df.columns):
    sub = df.dropna(subset=["lat","lon"]).sample(n=min(100_000, len(df)), random_state=1)
    plt.figure(figsize=(6,6))
    plt.scatter(sub["lon"].astype(float), sub["lat"].astype(float), s=1, alpha=0.5, color="white")
    plt.xlim([-118.7, -118.1])
    plt.ylim([33.7, 34.3])
    plt.title("Spatial Scatter of Incidents (LA)")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.savefig(os.path.join(figures_folder, "la_lat_lon.png"), dpi=300, facecolor='#0a1a2f')
    

# Year vs Month heatmap
df2 = df.dropna(subset=["year","month"])
pivot2 = pd.pivot_table(df2, index="year", columns="month", values="dr_no", aggfunc="count", fill_value=0)
plt.figure(figsize=(10,6))
sns.heatmap(pivot2, cmap="YlGnBu", annot=False)
plt.xticks(ticks=np.arange(12)+0.5, labels=[calendar.month_abbr[i] for i in range(1,13)], rotation=45)
plt.title("Heatmap: Crimes by Year and Month")
plt.savefig(os.path.join(figures_folder, "year_month_heatmap.png"), dpi=300, facecolor='#0a1a2f')

plt.tight_layout()
plt.show()

