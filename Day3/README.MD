# 🐼 Pandas Day 3 — Data Cleaning

> Real-world data is messy. Learn how to detect and fix missing values, remove duplicates, rename columns, fix data types, and clean text — the essential skills every data analyst needs.

---

## 📋 Table of Contents

1. [Why Data Cleaning Matters](#1-why-data-cleaning-matters)
2. [Detecting Missing Values](#2-detecting-missing-values)
3. [Dropping Missing Values — .dropna()](#3-dropping-missing-values----dropna)
4. [Filling Missing Values — .fillna()](#4-filling-missing-values----fillna)
5. [Detecting & Removing Duplicates](#5-detecting--removing-duplicates)
6. [Renaming Columns — .rename()](#6-renaming-columns----rename)
7. [Changing Data Types — .astype()](#7-changing-data-types----astype)
8. [String Cleaning](#8-string-cleaning)
9. [Mini Project](#-mini-project)

---

## 🗂️ Setup — The Messy Dataset We'll Clean Today

```python
import pandas as pd
import numpy as np

data = {
    "Name":    ["Alice", "bob", " Carol ", "David", "Alice", "eve", None],
    "Age":     [25, 30, None, 35, 25, 28, 22],
    "City":    ["Dhaka", "jessore", "Sylhet", None, "Dhaka", "chittagong", "Sylhet"],
    "Score":   [88, 92, 75, None, 88, 60, 72],
    "Salary":  ["50000", "60000", "45000", "70000", "50000", None, "55000"],
    "Joined":  ["2021-01-15", "2020-06-01", "bad_date", "2019-03-10",
                "2021-01-15", "2022-11-20", "2023-05-05"]
}

df = pd.DataFrame(data)
print(df)
```

```
      Name   Age        City  Score  Salary      Joined
0    Alice  25.0       Dhaka   88.0   50000  2021-01-15
1      bob  30.0     jessore   92.0   60000  2020-06-01
2   Carol   None      Sylhet   75.0   45000    bad_date
3    David  35.0        None    NaN   70000  2019-03-10
4    Alice  25.0       Dhaka   88.0   50000  2021-01-15
5      eve  28.0  chittagong   60.0    None  2022-11-20
6     None  22.0      Sylhet   72.0   55000  2023-05-05
```

> This dataset has **7 problems**: missing values, duplicates, inconsistent casing, leading/trailing spaces, wrong data types, bad dates, and a `None` in the Name column. We'll fix them all.

---

## 1. Why Data Cleaning Matters

Before any analysis or machine learning, your data must be clean. Dirty data causes:

- **Wrong results** — averages skewed by outliers or wrong types
- **Crashes** — many functions break on `NaN` or wrong dtypes
- **Bad models** — ML models trained on messy data perform poorly

> **Rule of thumb:** Data scientists spend ~80% of their time cleaning data. Master this and you're ahead of most beginners.

The standard cleaning checklist:

- [ ] Check for missing values
- [ ] Handle or remove duplicates
- [ ] Fix column names
- [ ] Fix data types
- [ ] Clean string values (whitespace, casing)
- [ ] Handle outliers (covered in Day 4)

---

## 2. Detecting Missing Values

Pandas represents missing data as `NaN` (Not a Number) for numeric columns and `None` or `NaN` for object columns.

### Check for missing values

```python
# True where value is missing
df.isnull()

# Count missing values per column
df.isnull().sum()
```

```
Name      1
Age       1
City      1
Score     1
Salary    1
Joined    0
dtype: int64
```

```python
# Percentage of missing values per column
df.isnull().sum() / len(df) * 100
```

```
Name      14.29
Age       14.29
City      14.29
Score     14.29
Salary    14.29
Joined     0.00
dtype: float64
```

```python
# Total missing values in the entire DataFrame
print(df.isnull().sum().sum())      # → 5

# Which rows have ANY missing value?
df[df.isnull().any(axis=1)]

# Which rows have NO missing values?
df[df.notnull().all(axis=1)]

# Columns that have at least one missing value
df.columns[df.isnull().any()].tolist()
```

### Visual summary

```python
# Quick info — always run this first
df.info()
```

```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 7 entries, 0 to 6
Data columns (total 6 columns):
 #   Column  Non-Null Count  Dtype
---  ------  --------------  -----
 0   Name    6 non-null      object
 1   Age     6 non-null      float64
 2   City    6 non-null      object
 3   Score   6 non-null      float64
 4   Salary  6 non-null      object
 5   Joined  7 non-null      object
dtypes: float64(2), object(4)
```

> **💡 Tip:** In `.info()`, any column where `Non-Null Count < total rows` has missing values. That's your cleaning target list.

---

## 3. Dropping Missing Values — `.dropna()`

Sometimes the best solution is to remove rows (or columns) with missing data.

### Drop rows with ANY missing value (default)

```python
df_clean = df.dropna()
print(df_clean.shape)   # → (2, 6) — most rows had at least one NaN
```

### Drop rows only if ALL values are missing

```python
df.dropna(how="all")    # only drops rows where every value is NaN
```

### Drop rows missing in specific columns

```python
# Only drop rows where 'Age' OR 'Score' is missing
df.dropna(subset=["Age", "Score"])

# Only drop rows where BOTH 'Age' AND 'Score' are missing
df.dropna(subset=["Age", "Score"], how="all")
```

### Keep rows with at least N non-null values

```python
# Keep rows that have at least 5 non-null values (out of 6 columns)
df.dropna(thresh=5)
```

### Drop columns with missing values

```python
# Drop any column that has at least one missing value
df.dropna(axis=1)

# Drop columns where ALL values are missing
df.dropna(axis=1, how="all")
```

### `inplace` — modify the original DataFrame

```python
# Without inplace — returns a new DataFrame
df_new = df.dropna()

# With inplace — modifies df directly (use carefully!)
df.dropna(inplace=True)
```

> ⚠️ **When to drop vs fill:** Drop rows when missing data is rare (<5%) and random. Fill (impute) when missing data is common or follows a pattern.

| Parameter | Options | Default | Use when |
|-----------|---------|---------|----------|
| `how` | `"any"`, `"all"` | `"any"` | Control how strict the drop is |
| `subset` | list of columns | all cols | Only care about specific columns |
| `thresh` | integer | None | Need a minimum number of valid values |
| `axis` | `0` (rows), `1` (cols) | `0` | Drop columns instead of rows |

---

## 4. Filling Missing Values — `.fillna()`

Often you don't want to lose data — you fill the gaps intelligently.

### Fill with a fixed value

```python
# Fill all NaN with 0
df["Score"].fillna(0)

# Fill with a string
df["City"].fillna("Unknown")

# Fill different columns with different values
df.fillna({
    "Age":    df["Age"].mean(),
    "Score":  0,
    "City":   "Unknown",
    "Salary": "N/A"
})
```

### Fill with statistical values (mean, median, mode)

```python
# Fill with column mean — good for normally distributed data
df["Age"].fillna(df["Age"].mean(), inplace=True)

# Fill with median — better when data has outliers
df["Score"].fillna(df["Score"].median(), inplace=True)

# Fill with mode (most common value) — good for categorical
df["City"].fillna(df["City"].mode()[0], inplace=True)
```

> **💡 Mean vs Median:** Use **mean** when data is symmetric. Use **median** when data is skewed or has outliers — it's more robust.

### Forward fill and backward fill

```python
# Forward fill — propagate last valid value downward
df["Score"].ffill()

# Backward fill — propagate next valid value upward
df["Score"].bfill()
```

```python
# Example — time series style
temps = pd.Series([20, None, None, 23, None, 25])
print(temps.ffill())
```

```
0    20.0
1    20.0    ← filled from row 0
2    20.0    ← filled from row 0
3    23.0
4    23.0    ← filled from row 3
5    25.0
```

> **💡 Tip:** Forward fill is great for time-series data where a missing value likely has the same value as the previous reading (e.g., stock prices, sensor data).

### Interpolation — fill with estimated values

```python
# Linear interpolation between surrounding values
df["Score"].interpolate(method="linear")
```

---

## 5. Detecting & Removing Duplicates

### Detect duplicate rows

```python
# Returns True for rows that are duplicates
df.duplicated()
```

```
0    False
1    False
2    False
3    False
4     True     ← row 4 is a duplicate of row 0
5    False
6    False
dtype: bool
```

```python
# Count total duplicate rows
print(df.duplicated().sum())    # → 1

# Show all duplicate rows
df[df.duplicated(keep=False)]   # keep=False marks ALL copies as True
```

### Remove duplicates

```python
# Remove duplicate rows — keep first occurrence (default)
df.drop_duplicates()

# Keep last occurrence
df.drop_duplicates(keep="last")

# Remove ALL rows that have any duplicate (including original)
df.drop_duplicates(keep=False)
```

### Find duplicates based on specific columns

```python
# Find rows where Name AND Age are the same
df.duplicated(subset=["Name", "Age"])

# Drop rows with duplicate Name + Age combination
df.drop_duplicates(subset=["Name", "Age"], keep="first")
```

```python
# Practical example — full dedup workflow
print(f"Before: {df.shape}")
df = df.drop_duplicates()
print(f"After:  {df.shape}")
```

```
Before: (7, 6)
After:  (6, 6)
```

| `keep` option | Behavior |
|---------------|----------|
| `"first"` (default) | Keep first occurrence, drop rest |
| `"last"` | Keep last occurrence, drop rest |
| `False` | Drop ALL copies — keep none |

---

## 6. Renaming Columns — `.rename()`

Clean, consistent column names make your code easier to read and write.

### Rename specific columns

```python
# Pass a dict: {old_name: new_name}
df = df.rename(columns={
    "Name":   "name",
    "Age":    "age",
    "City":   "city",
    "Score":  "score",
    "Salary": "salary",
    "Joined": "joined"
})

print(df.columns.tolist())
# → ['name', 'age', 'city', 'score', 'salary', 'joined']
```

### Rename all columns at once

```python
# Replace entire columns list
df.columns = ["name", "age", "city", "score", "salary", "joined"]
```

### Common column name cleaning patterns

```python
# Make all column names lowercase
df.columns = df.columns.str.lower()

# Replace spaces with underscores
df.columns = df.columns.str.replace(" ", "_")

# Remove special characters
df.columns = df.columns.str.replace(r"[^a-zA-Z0-9_]", "", regex=True)

# Chain them all together
df.columns = (df.columns
              .str.lower()
              .str.strip()
              .str.replace(" ", "_"))
```

> **💡 Convention:** Use `snake_case` (lowercase with underscores) for column names — e.g., `first_name`, `join_date`. Avoids issues with spaces and dot notation.

---

## 7. Changing Data Types — `.astype()`

Wrong data types are a silent killer. A "number" stored as a string won't calculate. A "date" stored as object won't sort correctly.

### Check current types

```python
print(df.dtypes)
```

```
name      object
age      float64
city      object
score    float64
salary    object    ← should be numeric!
joined    object    ← should be datetime!
```

### Convert with `.astype()`

```python
# String → integer
df["age"] = df["age"].astype(int)

# String → float
df["salary"] = df["salary"].astype(float)

# Integer → string
df["score"] = df["score"].astype(str)

# Convert multiple columns at once
df = df.astype({
    "age":    "int64",
    "score":  "float64",
    "salary": "float64"
})
```

### Convert to numeric safely — `pd.to_numeric()`

```python
# astype() crashes on bad values — pd.to_numeric() is safer
df["salary"] = pd.to_numeric(df["salary"], errors="coerce")
# errors="coerce" turns bad values into NaN instead of crashing
```

```python
# Example
s = pd.Series(["50000", "60000", "bad_value", "70000"])
pd.to_numeric(s, errors="coerce")
```

```
0    50000.0
1    60000.0
2        NaN    ← "bad_value" becomes NaN
3    70000.0
dtype: float64
```

### Convert to datetime — `pd.to_datetime()`

```python
# Convert string dates to datetime
df["joined"] = pd.to_datetime(df["joined"], errors="coerce")

# errors="coerce" turns "bad_date" into NaT (Not a Time)
print(df["joined"].dtype)    # → datetime64[ns]
```

### Convert to categorical — saves memory

```python
# Good for columns with few unique values
df["city"] = df["city"].astype("category")
df["grade"] = df["grade"].astype("category")
```

| From | To | Method |
|------|----|--------|
| `object` (string) | `int` / `float` | `.astype(int)` or `pd.to_numeric()` |
| `object` (string) | `datetime` | `pd.to_datetime()` |
| `float` | `int` | `.astype(int)` (no NaN allowed) |
| Any | `category` | `.astype("category")` |
| `int` / `float` | `bool` | `.astype(bool)` |

> ⚠️ **Important:** You cannot convert a column with `NaN` to `int` directly — Pandas will raise an error. Either fill the NaNs first or use `"Int64"` (nullable integer type).

```python
# ❌ Crashes if NaN present
df["age"].astype(int)

# ✅ Safe nullable integer
df["age"].astype("Int64")

# ✅ Or fill NaN first
df["age"].fillna(0).astype(int)
```

---

## 8. String Cleaning

Text data is almost always messy. These `.str` methods fix the most common problems.

### Strip whitespace

```python
# Remove leading and trailing spaces
df["name"] = df["name"].str.strip()

# Remove only left spaces
df["name"] = df["name"].str.lstrip()

# Remove only right spaces
df["name"] = df["name"].str.rstrip()
```

### Fix casing

```python
df["name"] = df["name"].str.lower()       # alice, bob, carol
df["name"] = df["name"].str.upper()       # ALICE, BOB, CAROL
df["name"] = df["name"].str.title()       # Alice, Bob, Carol
df["city"] = df["city"].str.capitalize()  # Dhaka, Jessore
```

### Replace substrings

```python
# Replace a substring
df["city"] = df["city"].str.replace("jessore", "Jessore")

# Replace using regex
df["name"] = df["name"].str.replace(r"\s+", " ", regex=True)  # collapse spaces

# Remove characters
df["salary"] = df["salary"].str.replace(",", "").str.replace("$", "")
```

### Full cleaning pipeline for our messy dataset

```python
import pandas as pd
import numpy as np

# Reload the original messy data
data = {
    "Name":   ["Alice", "bob", " Carol ", "David", "Alice", "eve", None],
    "Age":    [25, 30, None, 35, 25, 28, 22],
    "City":   ["Dhaka", "jessore", "Sylhet", None, "Dhaka", "chittagong", "Sylhet"],
    "Score":  [88, 92, 75, None, 88, 60, 72],
    "Salary": ["50000", "60000", "45000", "70000", "50000", None, "55000"],
    "Joined": ["2021-01-15", "2020-06-01", "bad_date", "2019-03-10",
               "2021-01-15", "2022-11-20", "2023-05-05"]
}
df = pd.DataFrame(data)

# ── Step 1: Fix column names ──────────────────────────
df.columns = df.columns.str.lower()

# ── Step 2: Remove duplicates ─────────────────────────
df = df.drop_duplicates()

# ── Step 3: Clean string columns ──────────────────────
df["name"] = df["name"].str.strip().str.title()
df["city"] = df["city"].str.strip().str.title()

# ── Step 4: Fix data types ────────────────────────────
df["salary"] = pd.to_numeric(df["salary"], errors="coerce")
df["joined"] = pd.to_datetime(df["joined"], errors="coerce")
df["age"]    = pd.to_numeric(df["age"], errors="coerce")

# ── Step 5: Handle missing values ────────────────────
df["age"].fillna(df["age"].median(), inplace=True)
df["score"].fillna(df["score"].median(), inplace=True)
df["salary"].fillna(df["salary"].median(), inplace=True)
df["city"].fillna("Unknown", inplace=True)
df.dropna(subset=["name"], inplace=True)   # drop rows with no name

# ── Step 6: Verify ────────────────────────────────────
print(df.info())
print(df.isnull().sum())
print(df)
```

```
      name   age        city  score   salary     joined
0    Alice  25.0       Dhaka   88.0  50000.0 2021-01-15
1      Bob  30.0     Jessore   92.0  60000.0 2020-06-01
2    Carol  25.0      Sylhet   75.0  45000.0        NaT
3    David  35.0     Unknown   88.0  70000.0 2019-03-10
4      Eve  28.0  Chittagong   60.0  55000.0 2022-11-20
5    Frank  22.0      Sylhet   72.0  55000.0 2023-05-05
```

> ✅ **Clean!** Missing values handled, duplicates removed, types fixed, strings standardized.

---

## 🎯 Mini Project

**Clean a real messy dataset from scratch.**

```python
import pandas as pd

# Load the Titanic dataset
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)
```

Complete these tasks:

- [ ] Run `df.isnull().sum()` — which columns have missing values?
- [ ] Fill missing `Age` values with the **median** age
- [ ] Fill missing `Embarked` values with the **mode**
- [ ] Drop the `Cabin` column (too many missing values — >77%)
- [ ] Remove any duplicate rows
- [ ] Convert `Age` to `int` after filling nulls (use `"Int64"`)
- [ ] Standardize the `Sex` column to title case
- [ ] Verify: run `df.isnull().sum()` again — all zeros? ✅

**Bonus challenge:**
```python
# What is the median age before and after cleaning?
# How many rows were dropped as duplicates?
# What % of the dataset did you lose?
```

---

## 🧠 Day 3 Quick Reference

```python
# ── Detect missing values ──────────────────────────────
df.isnull().sum()                        # count per column
df.isnull().sum() / len(df) * 100        # percentage
df[df.isnull().any(axis=1)]             # rows with any null

# ── Drop missing values ────────────────────────────────
df.dropna()                              # drop rows with any NaN
df.dropna(subset=["col"])               # only if 'col' is NaN
df.dropna(thresh=N)                     # keep rows with N+ valid
df.dropna(axis=1)                       # drop columns with NaN

# ── Fill missing values ────────────────────────────────
df["col"].fillna(0)                     # fill with value
df["col"].fillna(df["col"].mean())      # fill with mean
df["col"].fillna(df["col"].median())    # fill with median
df["col"].fillna(df["col"].mode()[0])   # fill with mode
df["col"].ffill()                       # forward fill
df["col"].bfill()                       # backward fill

# ── Duplicates ─────────────────────────────────────────
df.duplicated().sum()                   # count duplicates
df.drop_duplicates()                    # remove duplicates
df.drop_duplicates(subset=["col"])      # by specific column
df.drop_duplicates(keep=False)          # remove all copies

# ── Rename columns ─────────────────────────────────────
df.rename(columns={"old": "new"})
df.columns = df.columns.str.lower().str.replace(" ", "_")

# ── Fix data types ─────────────────────────────────────
df["col"].astype(int)
pd.to_numeric(df["col"], errors="coerce")
pd.to_datetime(df["col"], errors="coerce")
df["col"].astype("category")

# ── String cleaning ────────────────────────────────────
df["col"].str.strip()                   # remove whitespace
df["col"].str.lower()                   # lowercase
df["col"].str.title()                   # Title Case
df["col"].str.replace("a", "b")        # replace substring
df["col"].str.contains("text")         # check substring
```

---

## ⏭️ What's Next

| | Topic |
|---|---|
| ✅ Day 1 | Foundations & Data Structures |
| ✅ Day 2 | Selection & Filtering |
| ✅ Day 3 | Data Cleaning |
| ▶️ **Day 4** | **Data Transformation** — apply, map, lambda, new columns, binning |
| Day 5 | GroupBy & Aggregation |
| Day 6 | Merging, Joining & Reshaping |
| Day 7 | Time Series, Viz & Best Practices |

---

<div align="center">

**Day 3 Complete! 🎉**

*Pandas A–Z · 7-Day Course · Day 3 of 7*

</div>
