# 🐼 Pandas Day 7 — Time Series, Visualization & Best Practices

> The final day. Master dates and time series, bring your data to life with plots, write clean Pythonic Pandas code, and learn the performance tricks that make your code production-ready.

---

## 📋 Table of Contents

1. [Parsing Dates — pd.to_datetime()](#1-parsing-dates----pdto_datetime)
2. [The .dt Accessor](#2-the-dt-accessor)
3. [Resampling — .resample()](#3-resampling----resample)
4. [Rolling Windows — .rolling()](#4-rolling-windows----rolling)
5. [Basic Plotting — df.plot()](#5-basic-plotting----dfplot)
6. [Method Chaining — Clean Code](#6-method-chaining----clean-code)
7. [Performance Tips](#7-performance-tips)
8. [Capstone Project](#-capstone-project)

---

## 🗂️ Setup — Dataset We'll Use Today

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Generate a time series sales dataset
np.random.seed(42)

dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")
n = len(dates)

sales_data = pd.DataFrame({
    "date":     dates,
    "revenue":  np.random.randint(10000, 80000, n) + np.sin(np.arange(n) / 30) * 15000,
    "units":    np.random.randint(5, 100, n),
    "category": np.random.choice(["Electronics", "Accessories", "Software"], n),
    "region":   np.random.choice(["North", "South", "East", "West"], n),
    "returns":  np.random.randint(0, 10, n)
})

sales_data["revenue"] = sales_data["revenue"].round(2)
print(sales_data.head())
print(f"\nShape: {sales_data.shape}")
print(f"Date range: {sales_data['date'].min()} → {sales_data['date'].max()}")
```

```
        date    revenue  units     category region  returns
0 2023-01-01  38524.47     72  Electronics  South        3
1 2023-01-02  45231.18     45  Accessories   East        1
2 2023-01-03  29847.63     88     Software  North        7
3 2023-01-04  61432.90     23  Electronics   West        2
4 2023-01-05  42018.55     61  Accessories  South        4

Shape: (365, 6)
Date range: 2023-01-01 → 2023-12-31
```

---

## 1. Parsing Dates — `pd.to_datetime()`

Pandas stores dates as `datetime64` — a powerful type that unlocks time-based operations. Raw CSVs usually store dates as plain strings; you need to parse them first.

### Convert string to datetime

```python
# Single value
pd.to_datetime("2023-06-15")
# → Timestamp('2023-06-15 00:00:00')

# A column of strings
df = pd.DataFrame({"date_str": ["2023-01-15", "2023-06-20", "2023-12-31"]})
df["date"] = pd.to_datetime(df["date_str"])
print(df.dtypes)
```

```
date_str     object
date     datetime64[ns]
```

### Parse on load — the best practice

```python
# Parse while reading CSV — no separate conversion needed
df = pd.read_csv("sales.csv", parse_dates=["date"])

# Or specify the format explicitly for faster parsing
df["date"] = pd.to_datetime(df["date_str"], format="%Y-%m-%d")
```

### Handle messy date formats

```python
# Mixed or non-standard formats
messy_dates = pd.Series(["Jan 15, 2023", "2023/06/20", "15-12-2023", "bad_date"])

# errors="coerce" turns unparseable dates into NaT (Not a Time)
parsed = pd.to_datetime(messy_dates, errors="coerce")
print(parsed)
```

```
0   2023-01-15
1   2023-06-20
2   2023-12-15
3          NaT    ← "bad_date" becomes NaT
dtype: datetime64[ns]
```

### Common date formats

```python
pd.to_datetime("15/06/2023", format="%d/%m/%Y")    # DD/MM/YYYY
pd.to_datetime("06-15-2023", format="%m-%d-%Y")    # MM-DD-YYYY
pd.to_datetime("20230615",   format="%Y%m%d")      # YYYYMMDD
pd.to_datetime("2023-06-15 14:30:00")              # datetime with time
```

### Set date as index — the foundation of time series

```python
# Set the date column as the DataFrame index
sales_data = sales_data.set_index("date")
print(sales_data.index)
```

```
DatetimeIndex(['2023-01-01', '2023-01-02', ..., '2023-12-31'],
              dtype='datetime64[ns]', name='date', freq=None)
```

```python
# Now you can slice by date strings — incredibly convenient
sales_data["2023-03"]                           # all of March 2023
sales_data["2023-Q2"]                           # entire Q2
sales_data["2023-01-01":"2023-03-31"]           # Jan to Mar
sales_data.loc["2023-06-15"]                    # specific day
```

---

## 2. The `.dt` Accessor

Once a column has `datetime64` dtype, the `.dt` accessor unlocks dozens of date/time properties and methods.

### Extract date components

```python
# Reset index so 'date' is a column again for demonstration
df = sales_data.reset_index()

df["year"]       = df["date"].dt.year
df["month"]      = df["date"].dt.month
df["month_name"] = df["date"].dt.month_name()
df["day"]        = df["date"].dt.day
df["day_name"]   = df["date"].dt.day_name()
df["week"]       = df["date"].dt.isocalendar().week
df["quarter"]    = df["date"].dt.quarter
df["day_of_year"]= df["date"].dt.day_of_year

print(df[["date","year","month","month_name","day_name","quarter"]].head(5))
```

```
        date  year  month month_name   day_name  quarter
0 2023-01-01  2023      1    January     Sunday        1
1 2023-01-02  2023      1    January     Monday        1
2 2023-01-03  2023      1    January    Tuesday        1
3 2023-01-04  2023      1    January  Wednesday        1
4 2023-01-05  2023      1    January   Thursday        1
```

### Time-based filters using .dt

```python
# Filter for weekdays only (Mon=0, Sun=6)
weekdays = df[df["date"].dt.dayofweek < 5]

# Filter for a specific month
march = df[df["date"].dt.month == 3]

# Filter for weekends
weekends = df[df["date"].dt.dayofweek >= 5]

# Filter for Q4 (Oct, Nov, Dec)
q4 = df[df["date"].dt.quarter == 4]

# Filter for the first day of each month
month_starts = df[df["date"].dt.is_month_start]
```

### Timedelta — date arithmetic

```python
# Add/subtract time
df["date"] + pd.Timedelta(days=30)      # 30 days later
df["date"] + pd.DateOffset(months=1)    # exactly 1 month later
df["date"] + pd.DateOffset(years=1)     # exactly 1 year later

# Difference between two dates
df["days_since_launch"] = (df["date"] - pd.Timestamp("2023-01-01")).dt.days

# Days until end of year
df["days_remaining"] = (pd.Timestamp("2023-12-31") - df["date"]).dt.days
```

### All `.dt` properties at a glance

```python
df["date"].dt.year           # year (int)
df["date"].dt.month          # month number 1–12
df["date"].dt.month_name()   # "January", "February"…
df["date"].dt.day            # day of month 1–31
df["date"].dt.day_name()     # "Monday", "Tuesday"…
df["date"].dt.dayofweek      # 0=Monday, 6=Sunday
df["date"].dt.dayofyear      # 1–365
df["date"].dt.quarter        # 1–4
df["date"].dt.hour           # hour 0–23
df["date"].dt.minute         # minute 0–59
df["date"].dt.is_month_start # True on 1st of month
df["date"].dt.is_month_end   # True on last of month
df["date"].dt.is_quarter_end # True on last day of quarter
```

---

## 3. Resampling — `.resample()`

`.resample()` groups time-series data into time buckets — like `groupby()` but for dates. It requires a `DatetimeIndex`.

### Basic resampling

```python
# sales_data already has DatetimeIndex from Step 1
# Resample daily data to monthly totals
monthly_revenue = sales_data["revenue"].resample("ME").sum()
print(monthly_revenue.head(4))
```

```
date
2023-01-31    1.284571e+06
2023-02-28    1.156234e+06
2023-03-31    1.312890e+06
2023-04-30    1.198456e+06
Freq: ME, dtype: float64
```

### Resampling frequency aliases

```python
sales_data["revenue"].resample("D").sum()    # daily
sales_data["revenue"].resample("W").sum()    # weekly (Sunday)
sales_data["revenue"].resample("ME").sum()   # month end
sales_data["revenue"].resample("MS").sum()   # month start
sales_data["revenue"].resample("QE").sum()   # quarter end
sales_data["revenue"].resample("YE").sum()   # year end
sales_data["revenue"].resample("h").sum()    # hourly (for time data)
```

### Multiple aggregations on resample

```python
monthly_summary = sales_data.resample("ME").agg(
    total_revenue = ("revenue", "sum"),
    avg_daily_rev = ("revenue", "mean"),
    total_units   = ("units",   "sum"),
    peak_revenue  = ("revenue", "max"),
    total_returns = ("returns", "sum")
).round(2)

print(monthly_summary.head(4))
```

```
            total_revenue  avg_daily_rev  total_units  peak_revenue  total_returns
date
2023-01-31    1284571.23       41437.14         1876      79234.55            95
2023-02-28    1156234.87       41294.10         1654      78901.23            82
2023-03-31    1312890.45       42351.95         2103      79876.32           101
2023-04-30    1198456.78       39948.56         1789      78543.21            88
```

### Resample with groupby

```python
# Monthly revenue BY category
monthly_by_cat = (
    sales_data.groupby("category")["revenue"]
    .resample("ME")
    .sum()
    .reset_index()
)
print(monthly_by_cat.head(6))
```

---

## 4. Rolling Windows — `.rolling()`

`.rolling()` computes statistics over a sliding window of N rows — great for smoothing noisy data and computing moving averages.

### Simple moving average

```python
# 7-day rolling average of revenue
sales_data["revenue_7d_avg"] = sales_data["revenue"].rolling(window=7).mean()

# 30-day rolling average
sales_data["revenue_30d_avg"] = sales_data["revenue"].rolling(window=30).mean()

print(sales_data[["revenue","revenue_7d_avg","revenue_30d_avg"]].head(10))
```

```
              revenue  revenue_7d_avg  revenue_30d_avg
date
2023-01-01  38524.47             NaN              NaN
2023-01-02  45231.18             NaN              NaN
2023-01-03  29847.63             NaN              NaN
2023-01-04  61432.90             NaN              NaN
2023-01-05  42018.55             NaN              NaN
2023-01-06  55234.78             NaN              NaN
2023-01-07  48901.23       45884.39              NaN   ← first 7-day avg
2023-01-08  39234.67       45985.85              NaN
...
```

> The first `window-1` rows are `NaN` because there aren't enough data points yet to fill the window.

### Other rolling aggregations

```python
sales_data["revenue"].rolling(7).sum()     # rolling sum
sales_data["revenue"].rolling(7).min()     # rolling minimum
sales_data["revenue"].rolling(7).max()     # rolling maximum
sales_data["revenue"].rolling(7).std()     # rolling std deviation
sales_data["revenue"].rolling(7).median()  # rolling median
```

### Expanding window — cumulative statistics

```python
# Growing window from start to current row
sales_data["cumulative_revenue"] = sales_data["revenue"].expanding().sum()
sales_data["running_avg"]        = sales_data["revenue"].expanding().mean()
```

### Rolling with `min_periods`

```python
# Start calculating from the 1st row, even with incomplete window
sales_data["revenue"].rolling(window=7, min_periods=1).mean()
# No NaN values — uses whatever data is available
```

### Percentage change

```python
# Day-over-day change
sales_data["revenue_pct_change"] = sales_data["revenue"].pct_change()

# Month-over-month change (after resampling)
monthly = sales_data["revenue"].resample("ME").sum()
monthly_growth = monthly.pct_change().round(4) * 100
print(monthly_growth.head(6))
```

---

## 5. Basic Plotting — `df.plot()`

Pandas has a built-in `.plot()` method powered by Matplotlib. Quick, clean, and requires no extra setup.

### Line chart

```python
import matplotlib.pyplot as plt

# Monthly revenue trend
monthly = sales_data["revenue"].resample("ME").sum() / 1000  # in thousands

monthly.plot(
    kind="line",
    title="Monthly Revenue 2023",
    xlabel="Month",
    ylabel="Revenue (thousands)",
    figsize=(12, 5),
    color="#2060c0",
    linewidth=2,
    marker="o"
)
plt.tight_layout()
plt.savefig("monthly_revenue.png", dpi=150)
plt.show()
```

### Bar chart

```python
# Revenue by category
cat_revenue = sales_data.groupby("category")["revenue"].sum() / 1000

cat_revenue.plot(
    kind="bar",
    title="Total Revenue by Category",
    xlabel="Category",
    ylabel="Revenue (thousands)",
    figsize=(8, 5),
    color=["#2060c0", "#c04020", "#20a060"],
    edgecolor="white",
    rot=0
)
plt.tight_layout()
plt.show()
```

### Horizontal bar chart

```python
cat_revenue.sort_values().plot(
    kind="barh",
    title="Revenue by Category (Sorted)",
    figsize=(8, 4)
)
plt.tight_layout()
plt.show()
```

### Histogram

```python
sales_data["revenue"].plot(
    kind="hist",
    bins=30,
    title="Revenue Distribution",
    xlabel="Revenue",
    figsize=(8, 5),
    color="#2060c0",
    edgecolor="white"
)
plt.tight_layout()
plt.show()
```

### Scatter plot

```python
sales_data.plot(
    kind="scatter",
    x="units",
    y="revenue",
    title="Units Sold vs Revenue",
    figsize=(8, 5),
    alpha=0.4,
    color="#c04020"
)
plt.tight_layout()
plt.show()
```

### Multiple subplots

```python
# Plot multiple columns in one figure
monthly_data = sales_data[["revenue", "units"]].resample("ME").sum()

monthly_data.plot(
    subplots=True,
    figsize=(12, 8),
    title=["Monthly Revenue", "Monthly Units Sold"],
    color=["#2060c0", "#20a060"]
)
plt.tight_layout()
plt.show()
```

### Plot type reference

```python
df.plot(kind="line")      # line chart — trends over time
df.plot(kind="bar")       # vertical bar — category comparison
df.plot(kind="barh")      # horizontal bar — category comparison
df.plot(kind="hist")      # histogram — distribution
df.plot(kind="scatter", x="a", y="b")   # scatter — correlation
df.plot(kind="box")       # box plot — spread + outliers
df.plot(kind="pie", y="col")            # pie chart
df.plot(kind="area")      # area chart — stacked trends
```

---

## 6. Method Chaining — Clean Code

Method chaining pipes multiple operations together in one readable expression — no messy intermediate variables.

### Without chaining — messy

```python
# Intermediate variables everywhere — hard to read
df1 = pd.read_csv("sales.csv")
df2 = df1.dropna(subset=["revenue"])
df3 = df2[df2["revenue"] > 0]
df4 = df3.rename(columns={"revenue": "Revenue_USD"})
df5 = df4.assign(revenue_k=df4["Revenue_USD"] / 1000)
df6 = df5.groupby("category")["revenue_k"].sum()
df7 = df6.reset_index()
df8 = df7.sort_values("revenue_k", ascending=False)
result = df8.head(5)
```

### With chaining — clean

```python
result = (
    pd.read_csv("sales.csv")
    .dropna(subset=["revenue"])
    .query("revenue > 0")
    .rename(columns={"revenue": "Revenue_USD"})
    .assign(revenue_k=lambda df: df["Revenue_USD"] / 1000)
    .groupby("category")["revenue_k"]
    .sum()
    .reset_index()
    .sort_values("revenue_k", ascending=False)
    .head(5)
)
```

> Same result — but the chained version reads like a sentence: *"Load → drop nulls → filter → rename → add column → group → sort → take top 5."*

### Key chaining methods

```python
# .assign() — add/modify columns without breaking the chain
df.assign(
    profit      = lambda df: df["revenue"] - df["cost"],
    profit_pct  = lambda df: df["profit"] / df["revenue"] * 100,
    high_value  = lambda df: df["revenue"] > df["revenue"].median()
)

# .pipe() — apply a custom function mid-chain
def add_moving_avg(df, col, window=7):
    df[f"{col}_{window}d_avg"] = df[col].rolling(window).mean()
    return df

result = (
    sales_data
    .resample("D")
    .sum()
    .pipe(add_moving_avg, "revenue", 7)
    .pipe(add_moving_avg, "revenue", 30)
)

# .query() — filter mid-chain with readable strings
result = (
    df
    .query("region == 'North' and revenue > 50000")
    .assign(revenue_k=lambda df: df["revenue"] / 1000)
    .sort_values("revenue_k", ascending=False)
)
```

### Method chaining tips

```python
# Wrap in () to span multiple lines cleanly
result = (
    df
    .method1()
    .method2()
    .method3()
)

# Use .copy() at the start to avoid SettingWithCopyWarning
result = (
    df.copy()
    .dropna()
    .reset_index(drop=True)
)

# Use .assign() for new columns — never df["new"] = ... mid-chain
# ✅ Chain-friendly
df.assign(new_col=lambda df: df["a"] + df["b"])

# ❌ Breaks the chain
df["new_col"] = df["a"] + df["b"]
```

---

## 7. Performance Tips

When your dataset grows large (millions of rows), these optimizations make a real difference.

### 1. Vectorization beats .apply()

```python
import time

n = 1_000_000
df = pd.DataFrame({"a": np.random.randn(n), "b": np.random.randn(n)})

# ❌ Slow — Python loop via .apply()
start = time.time()
df["c"] = df.apply(lambda row: row["a"] + row["b"], axis=1)
print(f".apply():      {time.time()-start:.3f}s")

# ✅ Fast — vectorized operation
start = time.time()
df["c"] = df["a"] + df["b"]
print(f"Vectorized:    {time.time()-start:.3f}s")
```

```
.apply():      4.821s
Vectorized:    0.004s    ← 1200x faster!
```

### 2. Use efficient data types

```python
# Check current memory usage
print(df.memory_usage(deep=True).sum() / 1024**2, "MB")

# Before optimization
df["category"].dtype        # object → wastes memory

# Convert to category — huge savings for low-cardinality columns
df["category"] = df["category"].astype("category")
df["region"]   = df["region"].astype("category")

# Downcast numeric types
df["units"]   = pd.to_numeric(df["units"],   downcast="integer")
df["revenue"] = pd.to_numeric(df["revenue"], downcast="float")

# After optimization
print(df.memory_usage(deep=True).sum() / 1024**2, "MB")
```

```
Before:  48.3 MB
After:    8.1 MB    ← 83% reduction!
```

### 3. Use `query()` instead of boolean masks for large DataFrames

```python
# Boolean mask — creates intermediate arrays
df[(df["revenue"] > 50000) & (df["region"] == "North")]

# query() — faster on large DataFrames, uses numexpr under the hood
df.query("revenue > 50000 and region == 'North'")
```

### 4. `read_csv()` performance options

```python
# Only load the columns you need
df = pd.read_csv("large.csv", usecols=["date", "revenue", "category"])

# Specify dtypes upfront — avoids inference overhead
df = pd.read_csv("large.csv", dtype={
    "category": "category",
    "region":   "category",
    "units":    "int16",
    "revenue":  "float32"
})

# Load in chunks — for files that don't fit in memory
chunks = []
for chunk in pd.read_csv("huge.csv", chunksize=100_000):
    chunks.append(chunk.groupby("category")["revenue"].sum())
result = pd.concat(chunks).groupby(level=0).sum()
```

### 5. Use `.loc[]` for assignment — avoid SettingWithCopyWarning

```python
# ❌ May trigger warning or fail silently
df[df["region"]=="North"]["revenue"] = 0

# ✅ Safe and explicit
df.loc[df["region"]=="North", "revenue"] = 0
```

### 6. Prefer built-in methods over loops

```python
# ❌ Never do this
total = 0
for i in range(len(df)):
    total += df.iloc[i]["revenue"]

# ✅ Always do this
total = df["revenue"].sum()
```

### Performance cheat sheet

| Slow ❌ | Fast ✅ | Speedup |
|---------|---------|---------|
| `df.apply(func, axis=1)` | Vectorized column ops | 10–1000x |
| `object` dtype for categories | `.astype("category")` | 2–10x less memory |
| Boolean mask on huge df | `.query()` | 2–5x |
| `for i in range(len(df))` | `.sum()` / `.mean()` etc. | 100–10000x |
| `pd.read_csv()` all cols | `usecols=[...]` | 2–10x less memory |
| `float64` everywhere | `downcast="float"` → `float32` | 2x less memory |

---

## 🔗 Full End-to-End Pipeline

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ── Load & parse ───────────────────────────────────────
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

df = (
    pd.read_csv(url)
    .assign(
        # Clean and engineer features
        Age        = lambda df: df["Age"].fillna(df["Age"].median()),
        Embarked   = lambda df: df["Embarked"].fillna(df["Embarked"].mode()[0]),
        FamilySize = lambda df: df["SibSp"] + df["Parch"] + 1,
        IsAlone    = lambda df: (df["SibSp"] + df["Parch"] == 0).astype(int),
        AgeGroup   = lambda df: pd.cut(df["Age"],
                         bins=[0,12,18,60,100],
                         labels=["Child","Teen","Adult","Senior"])
    )
    .drop(columns=["Cabin", "Ticket", "Name"])
    .dropna()
)

# ── Analyze ────────────────────────────────────────────
print("── Survival Rate by Age Group & Class ──")
survival = df.groupby(["AgeGroup", "Pclass"])["Survived"].mean().round(2).unstack()
print(survival)

print("\n── Family Size vs Survival ──")
print(df.groupby("FamilySize").agg(
    count           = ("Survived", "count"),
    survival_rate   = ("Survived", "mean")
).round(2))

# ── Visualize ──────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Titanic — Full Analysis Dashboard", fontsize=16, fontweight="bold")

# 1. Survival by class
df.groupby("Pclass")["Survived"].mean().plot(
    kind="bar", ax=axes[0,0], title="Survival Rate by Class",
    color=["#2060c0","#c04020","#20a060"], rot=0, ylabel="Survival Rate"
)

# 2. Age distribution
df["Age"].plot(
    kind="hist", bins=25, ax=axes[0,1],
    title="Age Distribution", color="#2060c0", edgecolor="white"
)

# 3. Fare vs Age scatter
df.plot(
    kind="scatter", x="Age", y="Fare", ax=axes[1,0],
    title="Age vs Fare", alpha=0.3, color="#c04020"
)

# 4. Survival by age group
df.groupby("AgeGroup")["Survived"].mean().plot(
    kind="bar", ax=axes[1,1], title="Survival Rate by Age Group",
    color="#20a060", rot=0, ylabel="Survival Rate"
)

plt.tight_layout()
plt.savefig("titanic_dashboard.png", dpi=150, bbox_inches="tight")
plt.show()
print("\n✅ Dashboard saved as titanic_dashboard.png")
```

---

## 🎯 Capstone Project

**Full end-to-end analysis — from raw data to insights.**

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Option A — Use the generated sales dataset from the top of this file
# Option B — Pick your own from Kaggle or UCI ML Repository

np.random.seed(42)
dates = pd.date_range("2022-01-01", "2023-12-31", freq="D")
n = len(dates)

df = pd.DataFrame({
    "date":     dates,
    "revenue":  np.random.randint(8000, 90000, n) + np.sin(np.arange(n)/45)*20000,
    "units":    np.random.randint(5, 120, n),
    "category": np.random.choice(["Electronics","Accessories","Software"], n),
    "region":   np.random.choice(["North","South","East","West"], n),
    "rep":      np.random.choice(["Alice","Bob","Carol","David","Eve"], n),
    "returns":  np.random.randint(0, 15, n)
})
df["revenue"] = df["revenue"].clip(lower=5000).round(2)
df["profit"]  = (df["revenue"] * np.random.uniform(0.15, 0.45, n)).round(2)
```

Complete ALL of these tasks:

**Phase 1 — Clean & Prepare**
- [ ] Parse `date` as datetime and set as index
- [ ] Check for and handle any missing values
- [ ] Optimize dtypes — convert `category` and `region` to `"category"` dtype
- [ ] Add `month_name`, `quarter`, `day_of_week`, `is_weekend` columns using `.dt`

**Phase 2 — Analyze**
- [ ] Monthly revenue using `.resample("ME").sum()`
- [ ] 7-day and 30-day rolling average of revenue
- [ ] Top performing region using named aggregations
- [ ] Best and worst month by total revenue
- [ ] YoY (year-over-year) growth: 2022 vs 2023

**Phase 3 — Group & Aggregate**
- [ ] Revenue and profit by `category` — use named aggregations
- [ ] Use `.transform()` to add `region_avg_revenue` — find overperforming reps
- [ ] Pivot table: rows = month, columns = category, values = revenue sum
- [ ] Crosstab: region × quarter frequency count

**Phase 4 — Visualize (create at least 4 charts)**
- [ ] Line chart — monthly revenue trend with 30-day moving average
- [ ] Bar chart — total revenue by category
- [ ] Scatter chart — units sold vs revenue colored by category
- [ ] Your choice — any chart that reveals an interesting insight

**Phase 5 — Report**
- [ ] Write 3–5 bullet point findings from your analysis
- [ ] What was the best month? Best region? Best category?
- [ ] What pattern does the rolling average reveal?

---

## 🧠 Day 7 Quick Reference

```python
# ── Parse dates ─────────────────────────────────────────
pd.to_datetime(df["col"])
pd.to_datetime(df["col"], format="%d/%m/%Y")
pd.to_datetime(df["col"], errors="coerce")    # NaT on failure
df = pd.read_csv("f.csv", parse_dates=["date"])
df = df.set_index("date")                     # DatetimeIndex

# ── .dt accessor ────────────────────────────────────────
df["date"].dt.year          df["date"].dt.month
df["date"].dt.day_name()    df["date"].dt.quarter
df["date"].dt.dayofweek     df["date"].dt.is_month_end
df["date"].dt.month_name()  df["date"].dt.day_of_year

# ── Date filtering ──────────────────────────────────────
df["2023-03"]                              # entire month
df["2023-01":"2023-06"]                    # date range
df[df["date"].dt.quarter == 4]             # Q4 only
df[df["date"].dt.dayofweek < 5]            # weekdays only

# ── Resampling ──────────────────────────────────────────
df["val"].resample("ME").sum()             # monthly total
df["val"].resample("W").mean()             # weekly average
df["val"].resample("QE").agg(["sum","mean"])

# ── Rolling windows ─────────────────────────────────────
df["val"].rolling(7).mean()               # 7-period moving avg
df["val"].rolling(30).sum()               # 30-period rolling sum
df["val"].expanding().sum()               # cumulative sum
df["val"].pct_change()                    # period-over-period %

# ── Plotting ────────────────────────────────────────────
df.plot(kind="line",    figsize=(12,5))
df.plot(kind="bar",     rot=0)
df.plot(kind="barh")
df.plot(kind="hist",    bins=30)
df.plot(kind="scatter", x="a", y="b", alpha=0.4)
df.plot(kind="box")
df.plot(subplots=True,  figsize=(12,8))

# ── Method chaining ─────────────────────────────────────
result = (
    df.copy()
    .dropna(subset=["col"])
    .query("value > 0")
    .assign(new=lambda df: df["a"] / df["b"])
    .groupby("cat")["new"].sum()
    .reset_index()
    .sort_values("new", ascending=False)
)

# ── Performance ─────────────────────────────────────────
df["cat"] = df["cat"].astype("category")       # save memory
pd.to_numeric(df["col"], downcast="integer")   # shrink int
pd.to_numeric(df["col"], downcast="float")     # shrink float
pd.read_csv("f.csv", usecols=["a","b"])        # load less
df.query("a > 5")                              # fast filter
df.loc[mask, "col"] = value                    # safe assignment
```

---

## 🏁 Course Complete — Full 7-Day Summary

| Day | Topic | Key Skills |
|-----|-------|------------|
| ✅ 1 | Foundations | Series, DataFrame, .info(), .loc, .iloc, read_csv |
| ✅ 2 | Selection & Filtering | Boolean masks, .query(), .isin(), .between(), .str.contains() |
| ✅ 3 | Data Cleaning | .dropna(), .fillna(), duplicates, .astype(), string cleaning |
| ✅ 4 | Transformation | .apply(), .map(), lambda, np.where(), pd.cut(), get_dummies |
| ✅ 5 | GroupBy & Aggregation | .groupby(), .agg(), .transform(), pivot_table, crosstab |
| ✅ 6 | Merge & Reshape | pd.concat(), pd.merge(), .melt(), .pivot(), stack/unstack |
| ✅ 7 | Time Series & Viz | to_datetime, .dt, resample, rolling, df.plot(), chaining, performance |

---

## ⏭️ Where to Go From Here

| Topic | Resource |
|-------|----------|
| **More Pandas** | [Official Pandas docs](https://pandas.pydata.org/docs/) |
| **Data Visualization** | Seaborn, Plotly, Matplotlib |
| **Data Analysis** | Kaggle Learn courses |
| **Machine Learning** | Scikit-learn (your clean Pandas data is ready!) |
| **Big Data** | Polars (Pandas-like API, faster for large data) |
| **Practice datasets** | [Kaggle Datasets](https://www.kaggle.com/datasets) |

---

<div align="center">

**🎉 You Did It! All 7 Days Complete! 🎉**

*Pandas A–Z · 7-Day Course · Day 7 of 7*

*You now know everything you need to load, clean, transform, analyze, and visualize real-world data with Pandas.*

</div>
