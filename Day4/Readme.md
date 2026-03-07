# 🐼 Pandas Day 4 — Data Transformation

> Learn how to reshape, enrich, and engineer your data — creating new columns, applying custom logic with functions, binning numeric values, and encoding categorical variables.

---

## 📋 Table of Contents

1. [Creating New Columns](#1-creating-new-columns)
2. [.apply() — Apply a Function to a Column or Row](#2-apply----apply-a-function-to-a-column-or-row)
3. [.map() — Element-wise Mapping](#3-map----element-wise-mapping)
4. [Lambda Functions with .apply()](#4-lambda-functions-with-apply)
5. [.replace() — Value Substitution](#5-replace----value-substitution)
6. [Binning Data — pd.cut() and pd.qcut()](#6-binning-data----pdcut-and-pdqcut)
7. [Encoding Categorical Variables](#7-encoding-categorical-variables)
8. [Mini Project](#-mini-project)

---

## 🗂️ Setup — Dataset We'll Use Today

```python
import pandas as pd
import numpy as np

data = {
    "name":   ["Alice", "Bob", "Carol", "David", "Eve", "Frank", "Grace", "Hank"],
    "age":    [25, 30, 22, 35, 28, 19, 42, 31],
    "city":   ["Dhaka", "Jessore", "Sylhet", "Dhaka", "Chittagong", "Sylhet", "Dhaka", "Jessore"],
    "salary": [50000, 60000, 45000, 80000, 55000, 30000, 95000, 62000],
    "dept":   ["HR", "IT", "IT", "Finance", "HR", "IT", "Finance", "HR"],
    "score":  [88, 92, 75, 95, 60, 72, 98, 85],
    "gender": ["F", "M", "F", "M", "F", "M", "F", "M"]
}

df = pd.DataFrame(data)
print(df)
```

```
    name  age        city  salary     dept  score gender
0  Alice   25       Dhaka   50000       HR     88      F
1    Bob   30     Jessore   60000       IT     92      M
2  Carol   22      Sylhet   45000       IT     75      F
3  David   35       Dhaka   80000  Finance     95      M
4    Eve   28  Chittagong   55000       HR     60      F
5  Frank   19      Sylhet   30000       IT     72      M
6  Grace   42       Dhaka   95000  Finance     98      F
7   Hank   31     Jessore   62000       HR     85      M
```

---

## 1. Creating New Columns

The most common transformation — derive new information from existing columns.

### From arithmetic

```python
# Simple math on a column
df["salary_monthly"] = df["salary"] / 12
df["score_out_100"]  = df["score"]           # already out of 100

# Math between two columns
df["score_to_salary_ratio"] = df["score"] / df["salary"] * 1000

print(df[["name", "salary", "salary_monthly"]].head(3))
```

```
    name  salary  salary_monthly
0  Alice   50000     4166.666667
1    Bob   60000     5000.000000
2  Carol   45000     3750.000000
```

### From string operations

```python
# Combine first and last name columns (hypothetical)
df["greeting"] = "Hello, " + df["name"] + "!"

# Extract domain from email (hypothetical email column)
# df["domain"] = df["email"].str.split("@").str[1]
```

### From conditions — `np.where()`

```python
# np.where(condition, value_if_true, value_if_false)
df["is_senior"] = np.where(df["age"] >= 35, "Senior", "Junior")

print(df[["name", "age", "is_senior"]])
```

```
    name  age is_senior
0  Alice   25    Junior
1    Bob   30    Junior
2  Carol   22    Junior
3  David   35    Senior
4    Eve   28    Junior
5  Frank   19    Junior
6  Grace   42    Senior
7   Hank   31    Junior
```

### From multiple conditions — `np.select()`

```python
# np.select() for multiple conditions (like if/elif/else)
conditions = [
    df["salary"] < 40000,
    df["salary"].between(40000, 69999),
    df["salary"] >= 70000
]
choices = ["Low", "Mid", "High"]

df["salary_band"] = np.select(conditions, choices, default="Unknown")
print(df[["name", "salary", "salary_band"]])
```

```
    name  salary salary_band
0  Alice   50000         Mid
1    Bob   60000         Mid
2  Carol   45000         Mid
3  David   80000        High
4    Eve   55000         Mid
5  Frank   30000         Low
6  Grace   95000        High
7   Hank   62000         Mid
```

> **🔑 Key idea:** `np.where()` = one condition (if/else). `np.select()` = multiple conditions (if/elif/elif/else). Both are **vectorized** — much faster than loops or `.apply()`.

---

## 2. `.apply()` — Apply a Function to a Column or Row

`.apply()` lets you run any custom Python function across a column or row.

### Apply to a single column (Series)

```python
# Define a function
def classify_score(score):
    if score >= 90:
        return "Excellent"
    elif score >= 75:
        return "Good"
    elif score >= 60:
        return "Average"
    else:
        return "Poor"

# Apply it to the 'score' column
df["performance"] = df["score"].apply(classify_score)
print(df[["name", "score", "performance"]])
```

```
    name  score performance
0  Alice     88        Good
1    Bob     92   Excellent
2  Carol     75        Good
3  David     95   Excellent
4    Eve     60     Average
5  Frank     72        Good
6  Grace     98   Excellent
7   Hank     85        Good
```

### Apply to multiple columns (axis=1 — row-wise)

```python
# Function that uses values from multiple columns
def bonus(row):
    if row["dept"] == "Finance" and row["score"] >= 90:
        return row["salary"] * 0.20
    elif row["score"] >= 85:
        return row["salary"] * 0.10
    else:
        return row["salary"] * 0.05

# axis=1 means apply row-by-row
df["bonus"] = df.apply(bonus, axis=1)
print(df[["name", "dept", "score", "salary", "bonus"]])
```

```
    name     dept  score  salary    bonus
0  Alice       HR     88   50000   5000.0
1    Bob       IT     92   60000   6000.0
2  Carol       IT     75   45000   2250.0
3  David  Finance     95   80000  16000.0
4    Eve       HR     60   55000   2750.0
5  Frank       IT     72   30000   1500.0
6  Grace  Finance     98   95000  19000.0
7   Hank       HR     85   62000   6200.0
```

### Apply with `result_type`

```python
# Return multiple values as new columns
def get_stats(row):
    return pd.Series({
        "salary_daily": row["salary"] / 365,
        "salary_hourly": row["salary"] / (365 * 8)
    })

df[["salary_daily", "salary_hourly"]] = df.apply(get_stats, axis=1)
```

> ⚠️ **Performance note:** `.apply()` loops row-by-row in Python — it's slower than vectorized operations. Use `np.where()`, `np.select()`, or direct column math when possible. Reserve `.apply()` for complex logic that can't be vectorized.

---

## 3. `.map()` — Element-wise Mapping

`.map()` works on a **Series** (single column) and is perfect for substituting values using a dictionary or function.

### Map with a dictionary

```python
# Replace coded values with full labels
gender_map = {"M": "Male", "F": "Female"}
df["gender_full"] = df["gender"].map(gender_map)

dept_map = {
    "HR":      "Human Resources",
    "IT":      "Information Technology",
    "Finance": "Finance & Accounting"
}
df["dept_full"] = df["dept"].map(dept_map)

print(df[["name", "gender", "gender_full", "dept", "dept_full"]].head(4))
```

```
    name gender gender_full     dept                   dept_full
0  Alice      F      Female       HR           Human Resources
1    Bob      M        Male       IT    Information Technology
2  Carol      F      Female       IT    Information Technology
3  David      M        Male  Finance      Finance & Accounting
```

### Map with a function

```python
# Apply a simple function element-wise
df["name_length"] = df["name"].map(len)
df["name_upper"]  = df["name"].map(str.upper)

print(df[["name", "name_length", "name_upper"]].head(3))
```

```
    name  name_length name_upper
0  Alice            5      ALICE
1    Bob            3        BOB
2  Carol            5      CAROL
```

### `.map()` vs `.apply()` — when to use which

| | `.map()` | `.apply()` |
|---|---|---|
| **Works on** | Series only | Series or DataFrame |
| **Best for** | Simple 1-to-1 value substitution | Complex logic, multi-column logic |
| **Input** | Dict, Series, or function | Function only |
| **Speed** | Faster for dict lookup | Slower (Python loop) |

```python
# These are equivalent for simple functions on a Series:
df["name"].map(str.upper)
df["name"].apply(str.upper)

# But only .apply() can work row-wise across multiple columns:
df.apply(bonus, axis=1)    # ✅
df.map(bonus)              # ❌ won't work row-wise
```

---

## 4. Lambda Functions with `.apply()`

A **lambda** is an anonymous one-liner function. Combined with `.apply()`, it's perfect for quick transformations without defining a full function.

```python
# Syntax: lambda arguments: expression

# Without lambda
def square(x):
    return x ** 2

df["score_squared"] = df["score"].apply(square)

# With lambda — same result, one line
df["score_squared"] = df["score"].apply(lambda x: x ** 2)
```

### Practical lambda examples

```python
# Normalize score to 0–1 range
df["score_norm"] = df["score"].apply(lambda x: (x - df["score"].min()) /
                                               (df["score"].max() - df["score"].min()))

# Categorize salary
df["pay_level"] = df["salary"].apply(lambda x: "High" if x > 70000 else "Normal")

# Extract first name initial
df["initial"] = df["name"].apply(lambda x: x[0] + ".")

# Multi-column lambda with axis=1
df["value_score"] = df.apply(
    lambda row: row["score"] * 1000 / row["salary"], axis=1
)

print(df[["name", "score", "salary", "value_score"]].head(4))
```

```
    name  score  salary  value_score
0  Alice     88   50000     1.760000
1    Bob     92   60000     1.533333
2  Carol     75   45000     1.666667
3  David     95   80000     1.187500
```

> **💡 Rule of thumb:** Use a lambda when the logic fits in one line. Use a named function (`def`) when the logic is complex, needs comments, or will be reused elsewhere.

---

## 5. `.replace()` — Value Substitution

`.replace()` swaps specific values in a column or DataFrame — great for fixing typos, standardizing codes, or encoding labels.

### Replace in a single column

```python
# Replace one value
df["dept"].replace("HR", "Human Resources")

# Replace multiple values at once using a dict
df["gender"] = df["gender"].replace({"M": "Male", "F": "Female"})
df["dept"]   = df["dept"].replace({
    "HR":      "Human Resources",
    "IT":      "Information Technology",
    "Finance": "Finance Dept"
})
```

### Replace across the whole DataFrame

```python
# Replace a value anywhere in the DataFrame
df.replace(np.nan, 0)

# Replace multiple values with one value
df.replace(["unknown", "n/a", "none"], np.nan)
```

### Replace with regex

```python
# Replace patterns using regex=True
df["name"].replace(r"^\s+|\s+$", "", regex=True)   # strip whitespace
df["city"].replace(r"[0-9]", "", regex=True)        # remove digits
```

### `.replace()` vs `.map()`

```python
# .replace() — leaves unmatched values unchanged
df["gender"].replace({"M": "Male"})
# "F" stays as "F" — only "M" is replaced

# .map() — unmatched values become NaN
df["gender"].map({"M": "Male"})
# "F" becomes NaN — every value must be in the dict
```

> **💡 Use `.replace()`** when you only want to change some values and leave the rest as-is. **Use `.map()`** when you want a complete 1-to-1 remapping of all values.

---

## 6. Binning Data — `pd.cut()` and `pd.qcut()`

Binning converts a continuous numeric column into discrete categories (buckets). Essential for age groups, score ranges, income brackets, etc.

### `pd.cut()` — Fixed-width bins (you define the edges)

```python
# Divide age into 4 fixed ranges
df["age_group"] = pd.cut(
    df["age"],
    bins=[0, 20, 30, 40, 100],
    labels=["Teen", "Twenties", "Thirties", "40+"]
)

print(df[["name", "age", "age_group"]])
```

```
    name  age age_group
0  Alice   25  Twenties
1    Bob   30  Thirties
2  Carol   22  Twenties
3  David   35  Thirties
4    Eve   28  Twenties
5  Frank   19      Teen
6  Grace   42       40+
7   Hank   31  Thirties
```

```python
# Without labels — returns interval notation like (20, 30]
df["age_bin"] = pd.cut(df["age"], bins=4)   # auto 4 equal-width bins

# right=False makes bins left-inclusive: [0, 20) instead of (0, 20]
df["age_group"] = pd.cut(df["age"], bins=[0, 20, 30, 40, 100],
                          labels=["Teen", "Twenties", "Thirties", "40+"],
                          right=False)
```

### `pd.qcut()` — Quantile-based bins (equal-frequency)

```python
# Divide salary into 4 equal-sized groups (quartiles)
df["salary_quartile"] = pd.qcut(
    df["salary"],
    q=4,
    labels=["Q1-Low", "Q2", "Q3", "Q4-High"]
)

print(df[["name", "salary", "salary_quartile"]])
```

```
    name  salary salary_quartile
0  Alice   50000              Q2
1    Bob   60000              Q3
2  Carol   45000           Q1-Low
3  David   80000         Q4-High
4    Eve   55000              Q2
5  Frank   30000          Q1-Low
6  Grace   95000         Q4-High
7   Hank   62000              Q3
```

```python
# Percentiles — split into deciles (10 equal groups)
df["score_decile"] = pd.qcut(df["score"], q=10, labels=False)

# Tertiles (3 groups)
df["salary_tier"] = pd.qcut(df["salary"], q=3, labels=["Low", "Mid", "High"])
```

### `pd.cut()` vs `pd.qcut()`

| | `pd.cut()` | `pd.qcut()` |
|---|---|---|
| **Bin width** | Fixed (you define edges) | Variable (equal frequency) |
| **Bin size** | Unequal — varies by data | Equal — same number per bin |
| **Best for** | Known categories (age groups, grades) | Ranking, percentiles, quartiles |
| **Example** | Age: 0–18, 18–35, 35–60, 60+ | Top 25%, Bottom 25% |

---

## 7. Encoding Categorical Variables

Machine learning models need numbers, not text. Encoding converts categories to numeric form.

### Label Encoding — map categories to integers

```python
# Manual label encoding
dept_codes = {"HR": 0, "IT": 1, "Finance": 2}
df["dept_encoded"] = df["dept"].map(dept_codes)

# Or use pandas Categorical codes (auto-assigns integers)
df["dept_cat"]     = df["dept"].astype("category")
df["dept_code"]    = df["dept_cat"].cat.codes

print(df[["dept", "dept_code"]].drop_duplicates().sort_values("dept_code"))
```

```
      dept  dept_code
3  Finance          0
0       HR          1
1       IT          2
```

> ⚠️ Label encoding implies an order (0 < 1 < 2). Only use it for ordinal data (Low < Mid < High). For nominal data (HR, IT, Finance have no order), use One-Hot Encoding.

### One-Hot Encoding — `pd.get_dummies()`

```python
# Create binary columns for each category
dummies = pd.get_dummies(df["dept"], prefix="dept")
print(dummies.head(4))
```

```
   dept_Finance  dept_HR  dept_IT
0             0        1        0
1             0        0        1
2             0        0        1
3             1        0        0
```

```python
# Add the dummy columns to the DataFrame
df = pd.concat([df, dummies], axis=1)

# Or use get_dummies directly on the DataFrame
df = pd.get_dummies(df, columns=["dept", "gender"], drop_first=True)
# drop_first=True removes one column to avoid multicollinearity
```

### Ordinal Encoding — preserve meaningful order

```python
# For ordered categories: Low < Mid < High
grade_order = {"F": 0, "D": 1, "C": 2, "B": 3, "A": 4}
df["grade_num"] = df["score"].apply(classify_score).map({
    "Poor": 0, "Average": 1, "Good": 2, "Excellent": 3
})
```

### Encoding summary

| Method | When to use | Example |
|--------|-------------|---------|
| **Label Encoding** | Ordered categories | Low=0, Mid=1, High=2 |
| **One-Hot Encoding** | Unordered categories | HR, IT, Finance → binary columns |
| **Ordinal Encoding** | Custom order mapping | F < D < C < B < A |
| **Binary Encoding** | High-cardinality categories | Cities, postal codes |

---

## 🔗 Full Transformation Pipeline

```python
import pandas as pd
import numpy as np

# Start with raw data
data = {
    "name":   ["Alice", "Bob", "Carol", "David", "Eve", "Frank", "Grace", "Hank"],
    "age":    [25, 30, 22, 35, 28, 19, 42, 31],
    "salary": [50000, 60000, 45000, 80000, 55000, 30000, 95000, 62000],
    "dept":   ["HR", "IT", "IT", "Finance", "HR", "IT", "Finance", "HR"],
    "score":  [88, 92, 75, 95, 60, 72, 98, 85],
    "gender": ["F", "M", "F", "M", "F", "M", "F", "M"]
}
df = pd.DataFrame(data)

# ── Step 1: Create new columns ─────────────────────────
df["salary_monthly"] = df["salary"] / 12
df["is_senior"]      = np.where(df["age"] >= 35, True, False)

# ── Step 2: Classify with apply ────────────────────────
df["performance"] = df["score"].apply(classify_score)

# ── Step 3: Map coded values ───────────────────────────
df["gender"] = df["gender"].map({"M": "Male", "F": "Female"})

# ── Step 4: Bin age into groups ────────────────────────
df["age_group"] = pd.cut(
    df["age"], bins=[0, 25, 35, 100],
    labels=["Young", "Mid", "Senior"]
)

# ── Step 5: Salary quartile ────────────────────────────
df["salary_q"] = pd.qcut(df["salary"], q=4,
                          labels=["Q1", "Q2", "Q3", "Q4"])

# ── Step 6: One-hot encode department ─────────────────
df = pd.get_dummies(df, columns=["dept"], drop_first=False)

print(df.head())
print(df.dtypes)
```

---

## 🎯 Mini Project

**Transform the Titanic dataset.**

```python
import pandas as pd
import numpy as np

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)
df["Age"].fillna(df["Age"].median(), inplace=True)
```

Complete these tasks:

- [ ] Create a new column `FamilySize` = `SibSp` + `Parch` + 1
- [ ] Create `IsAlone` column: `1` if `FamilySize == 1`, else `0` using `np.where()`
- [ ] Bin `Age` into groups: Child (0–12), Teen (13–17), Adult (18–60), Senior (60+) using `pd.cut()`
- [ ] Bin `Fare` into 4 quartiles using `pd.qcut()`
- [ ] Map `Sex` column: `"male"` → `0`, `"female"` → `1` using `.map()`
- [ ] One-hot encode `Embarked` using `pd.get_dummies()`
- [ ] Create `Title` column by extracting title from `Name` using `.str.extract(r" ([A-Za-z]+)\.")`

**Bonus challenge:**
```python
# What is the survival rate for each age group?
df.groupby("age_group")["Survived"].mean().round(2)
```

---

## 🧠 Day 4 Quick Reference

```python
# ── New columns ────────────────────────────────────────
df["new"] = df["a"] + df["b"]                    # arithmetic
df["flag"] = np.where(df["a"] > 5, "Yes", "No")  # if/else
df["level"] = np.select(conditions, choices)      # if/elif/else

# ── .apply() ───────────────────────────────────────────
df["col"].apply(my_function)                      # column-wise
df.apply(my_function, axis=1)                     # row-wise
df["col"].apply(lambda x: x * 2)                  # with lambda

# ── .map() ─────────────────────────────────────────────
df["col"].map({"A": 1, "B": 2})                   # dict mapping
df["col"].map(len)                                 # function mapping

# ── .replace() ─────────────────────────────────────────
df["col"].replace("old", "new")                   # single value
df["col"].replace({"a": 1, "b": 2})               # multiple values
df.replace(np.nan, 0)                             # whole DataFrame

# ── Binning ────────────────────────────────────────────
pd.cut(df["age"], bins=[0,18,65,100],
       labels=["Youth","Adult","Senior"])          # fixed edges
pd.qcut(df["salary"], q=4,
        labels=["Q1","Q2","Q3","Q4"])              # equal frequency

# ── Encoding ───────────────────────────────────────────
df["col"].map({"A": 0, "B": 1})                   # label encode
pd.get_dummies(df, columns=["col"])               # one-hot encode
df["col"].astype("category").cat.codes            # auto label encode
```

---

## ⏭️ What's Next

| | Topic |
|---|---|
| ✅ Day 1 | Foundations & Data Structures |
| ✅ Day 2 | Selection & Filtering |
| ✅ Day 3 | Data Cleaning |
| ✅ Day 4 | Data Transformation |
| ▶️ **Day 5** | **GroupBy & Aggregation** — split-apply-combine, pivot tables, crosstab |
| Day 6 | Merging, Joining & Reshaping |
| Day 7 | Time Series, Viz & Best Practices |

---

<div align="center">

**Day 4 Complete! 🎉**

*Pandas A–Z · 7-Day Course · Day 4 of 7*

</div>
