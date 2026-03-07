# 🐼 Pandas Day 5 — GroupBy & Aggregation

> Master the split-apply-combine pattern — the most powerful analytical tool in Pandas. Group your data, summarize it, transform it, and build pivot tables like a pro.

---

## 📋 Table of Contents

1. [The Split-Apply-Combine Pattern](#1-the-split-apply-combine-pattern)
2. [.groupby() Basics](#2-groupby-basics)
3. [Aggregation Methods](#3-aggregation-methods)
4. [.agg() — Custom & Multiple Aggregations](#4-agg----custom--multiple-aggregations)
5. [.transform() — Group-wise Operations](#5-transform----group-wise-operations)
6. [Pivot Tables — pd.pivot_table()](#6-pivot-tables----pdpivot_table)
7. [Cross-tabulations — pd.crosstab()](#7-cross-tabulations----pdcrosstab)
8. [Named Aggregations](#8-named-aggregations)
9. [Mini Project](#-mini-project)

---

## 🗂️ Setup — Dataset We'll Use Today

```python
import pandas as pd
import numpy as np

data = {
    "name":   ["Alice","Bob","Carol","David","Eve","Frank","Grace","Hank",
               "Ivy","Jack","Karen","Leo"],
    "dept":   ["HR","IT","IT","Finance","HR","IT","Finance","HR",
               "IT","Finance","HR","IT"],
    "city":   ["Dhaka","Jessore","Sylhet","Dhaka","Chittagong","Sylhet",
               "Dhaka","Jessore","Dhaka","Sylhet","Chittagong","Dhaka"],
    "gender": ["F","M","F","M","F","M","F","M","F","M","F","M"],
    "salary": [50000,60000,45000,80000,55000,30000,95000,62000,
               40000,75000,52000,48000],
    "score":  [88,92,75,95,60,72,98,85,70,90,65,78],
    "years":  [3,5,2,8,4,1,10,6,2,7,3,2]
}

df = pd.DataFrame(data)
print(df)
```

```
    name     dept        city gender  salary  score  years
0  Alice       HR       Dhaka      F   50000     88      3
1    Bob       IT     Jessore      M   60000     92      5
2  Carol       IT      Sylhet      F   45000     75      2
3  David  Finance       Dhaka      M   80000     95      8
4    Eve       HR  Chittagong      F   55000     60      4
5  Frank       IT      Sylhet      M   30000     72      1
6  Grace  Finance       Dhaka      F   95000     98     10
7   Hank       HR     Jessore      M   62000     85      6
8    Ivy       IT       Dhaka      F   40000     70      2
9   Jack  Finance      Sylhet      M   75000     90      7
10 Karen       HR  Chittagong      F   52000     65      3
11   Leo       IT       Dhaka      M   48000     78      2
```

---

## 1. The Split-Apply-Combine Pattern

GroupBy works in three steps:

```
SPLIT          →      APPLY          →     COMBINE
─────────────────────────────────────────────────────
Split the             Apply a               Combine the
DataFrame             function to           results back
into groups           each group            into one table
by a column
```

```python
# Example: What is the average salary per department?

# SPLIT  — group by 'dept'
# APPLY  — calculate mean() on each group
# COMBINE — merge results into a single Series

df.groupby("dept")["salary"].mean()
```

```
dept
Finance    83333.333333
HR         54750.000000
IT         44600.000000
Name: salary, dtype: float64
```

> **🔑 Key idea:** Think of `.groupby()` like SQL's `GROUP BY`. It answers "What is X *per* Y?" — revenue per region, avg score per department, count per category.

---

## 2. `.groupby()` Basics

### Group by a single column

```python
# The GroupBy object — lazy, nothing computed yet
grouped = df.groupby("dept")
print(type(grouped))    # → <pandas.core.groupby.DataFrameGroupBy>

# Apply aggregations
grouped["salary"].sum()         # total salary per dept
grouped["salary"].mean()        # avg salary per dept
grouped["score"].max()          # highest score per dept
grouped.size()                  # row count per dept
```

```
dept
Finance    3
HR         4
IT         5
dtype: int64
```

### Group by multiple columns

```python
# Average salary by dept AND gender
df.groupby(["dept", "gender"])["salary"].mean()
```

```
dept     gender
Finance  F         95000.000000
         M         77500.000000
HR       F         52333.333333
         M         62000.000000
IT       F         42500.000000
         M         46000.000000
```

```python
# Flatten multi-level index with reset_index()
df.groupby(["dept", "gender"])["salary"].mean().reset_index()
```

```
      dept gender        salary
0  Finance      F  95000.000000
1  Finance      M  77500.000000
2       HR      F  52333.333333
3       HR      M  62000.000000
4       IT      F  42500.000000
5       IT      M  46000.000000
```

### Iterate over groups

```python
for dept_name, group_df in df.groupby("dept"):
    print(f"\n── {dept_name} ({len(group_df)} people) ──")
    print(group_df[["name", "salary"]].to_string(index=False))
```

---

## 3. Aggregation Methods

All built-in aggregations available after `.groupby()`:

```python
g = df.groupby("dept")

g["salary"].sum()       # total
g["salary"].mean()      # average
g["salary"].median()    # median
g["salary"].min()       # minimum
g["salary"].max()       # maximum
g["salary"].std()       # standard deviation
g["salary"].var()       # variance
g["salary"].count()     # non-null count
g["salary"].nunique()   # count of unique values
g["salary"].first()     # first value in group
g["salary"].last()      # last value in group
```

### Multiple columns at once

```python
df.groupby("dept")[["salary", "score", "years"]].mean()
```

```
              salary      score     years
dept
Finance  83333.3333  94.333333  8.333333
HR       54750.0000  74.500000  4.000000
IT       44600.0000  77.400000  2.400000
```

### `.value_counts()` — category frequencies

```python
df["dept"].value_counts()
```

```
IT         5
HR         4
Finance    3
Name: dept, dtype: int64
```

```python
# As percentages
df["dept"].value_counts(normalize=True).round(2)
```

```
IT         0.42
HR         0.33
Finance    0.25
```

---

## 4. `.agg()` — Custom & Multiple Aggregations

`.agg()` lets you apply **multiple functions at once** to one or more columns.

### Multiple functions on one column

```python
df.groupby("dept")["salary"].agg(["mean", "min", "max", "count"])
```

```
              mean    min    max  count
dept
Finance  83333.33  75000  95000      3
HR       54750.00  50000  62000      4
IT       44600.00  30000  60000      5
```

### Different functions per column

```python
df.groupby("dept").agg({
    "salary": ["mean", "max"],
    "score":  ["mean", "min"],
    "years":  "sum"
})
```

```
           salary         score       years
             mean    max   mean  min   sum
dept
Finance  83333.33  95000  94.33   90    25
HR       54750.00  62000  74.50   60    16
IT       44600.00  60000  77.40   70    12
```

### Custom aggregation functions

```python
def salary_range(x):
    return x.max() - x.min()

df.groupby("dept")["salary"].agg(["mean", "std", salary_range])
```

```
              mean           std  salary_range
dept
Finance  83333.33  10408.329997         20000
HR       54750.00   5737.304825         12000
IT       44600.00  11676.186682         30000
```

---

## 5. `.transform()` — Group-wise Operations

`.transform()` applies a function per group but returns a result with the **same shape as the original DataFrame** — the group result is broadcast back to every row.

### Key difference from `.agg()`

```python
# .agg()  → collapses to one row per group
df.groupby("dept")["salary"].agg("mean")
# → 3 rows

# .transform() → keeps all original rows
df.groupby("dept")["salary"].transform("mean")
# → 12 rows (same as df)
```

### Add group statistics as new columns

```python
# Each person gets their department's average salary
df["dept_avg_salary"] = df.groupby("dept")["salary"].transform("mean")

# How much does each person earn vs their dept average?
df["vs_dept_avg"] = df["salary"] - df["dept_avg_salary"]

print(df[["name", "dept", "salary", "dept_avg_salary", "vs_dept_avg"]])
```

```
    name     dept  salary  dept_avg_salary  vs_dept_avg
0  Alice       HR   50000         54750.00      -4750.0
1    Bob       IT   60000         44600.00      15400.0
2  Carol       IT   45000         44600.00        400.0
3  David  Finance   80000         83333.33      -3333.3
4    Eve       HR   55000         54750.00        250.0
5  Frank       IT   30000         44600.00     -14600.0
6  Grace  Finance   95000         83333.33      11666.7
7   Hank       HR   62000         54750.00       7250.0
...
```

### Normalize within groups (z-score)

```python
df["salary_zscore"] = df.groupby("dept")["salary"].transform(
    lambda x: (x - x.mean()) / x.std()
)
```

### Rank within groups

```python
# Rank each person's salary within their department (1 = highest)
df["dept_salary_rank"] = df.groupby("dept")["salary"].rank(ascending=False)

print(df[["name", "dept", "salary", "dept_salary_rank"]])
```

```
    name     dept  salary  dept_salary_rank
0  Alice       HR   50000               3.0
1    Bob       IT   60000               1.0
2  Carol       IT   45000               3.0
3  David  Finance   80000               2.0
4    Eve       HR   55000               2.0
5  Frank       IT   30000               5.0
6  Grace  Finance   95000               1.0
7   Hank       HR   62000               1.0
```

| | `.agg()` | `.transform()` |
|---|---|---|
| **Output shape** | One row per group | Same as original |
| **Use for** | Summary/reporting tables | Adding group stats back to rows |
| **Index** | Group labels | Original index |

---

## 6. Pivot Tables — `pd.pivot_table()`

A pivot table is a 2D summary — rows = one category, columns = another, cells = aggregated values. The Pandas version of Excel pivot tables.

### Basic pivot table

```python
pd.pivot_table(
    df,
    values="salary",
    index="dept",
    columns="gender",
    aggfunc="mean"
)
```

```
gender            F             M
dept
Finance   95000.000    77500.000
HR        52333.333    62000.000
IT        42500.000    46000.000
```

### Multiple aggregations

```python
pd.pivot_table(
    df,
    values="salary",
    index="dept",
    columns="gender",
    aggfunc=["mean", "count"]
)
```

### Multiple value columns

```python
pd.pivot_table(
    df,
    values=["salary", "score"],
    index="dept",
    aggfunc={
        "salary": "mean",
        "score":  ["mean", "max"]
    }
)
```

### Add margins (grand totals)

```python
pd.pivot_table(
    df,
    values="salary",
    index="dept",
    columns="gender",
    aggfunc="mean",
    margins=True,
    margins_name="Total",
    fill_value=0
)
```

```
gender             F             M         Total
dept
Finance    95000.000    77500.000    83333.333
HR         52333.333    62000.000    54750.000
IT         42500.000    46000.000    44600.000
Total      57666.667    56500.000    57083.333
```

---

## 7. Cross-tabulations — `pd.crosstab()`

`pd.crosstab()` counts combinations of two categorical variables. Perfect for frequency tables.

### Basic crosstab

```python
pd.crosstab(df["dept"], df["gender"])
```

```
gender   F  M
dept
Finance  1  2
HR       3  1
IT       2  3
```

### Normalize to percentages

```python
# Row % — what % of each dept is male/female?
pd.crosstab(df["dept"], df["gender"], normalize="index").round(2)
```

```
gender      F     M
dept
Finance  0.33  0.67
HR       0.75  0.25
IT       0.40  0.60
```

```python
# Column % — what % of males/females are in each dept?
pd.crosstab(df["dept"], df["gender"], normalize="columns").round(2)
```

### With values and aggregation

```python
pd.crosstab(
    df["dept"],
    df["gender"],
    values=df["salary"],
    aggfunc="mean"
)
```

### With margins

```python
pd.crosstab(df["dept"], df["city"], margins=True, margins_name="Total")
```

### `crosstab()` vs `pivot_table()`

| | `pd.crosstab()` | `pd.pivot_table()` |
|---|---|---|
| **Default output** | Frequency count | Mean of value column |
| **Input** | Series / arrays | DataFrame |
| **Best for** | Counting category combinations | Summarizing numeric values |
| **Normalize** | Built-in `normalize=` param | Calculate manually |

---

## 8. Named Aggregations

Named aggregations give output columns **clean, descriptive names** directly — no renaming needed afterward.

```python
# Old way — ugly column names, extra rename step required
result = df.groupby("dept")["salary"].agg(["mean", "max", "count"])
result.columns = ["avg_salary", "max_salary", "headcount"]  # tedious!

# New way — named aggregations (Pandas 0.25+)
result = df.groupby("dept").agg(
    avg_salary  = ("salary", "mean"),
    max_salary  = ("salary", "max"),
    min_salary  = ("salary", "min"),
    headcount   = ("salary", "count"),
    avg_score   = ("score",  "mean"),
    total_years = ("years",  "sum")
)

print(result)
```

```
           avg_salary  max_salary  min_salary  headcount  avg_score  total_years
dept
Finance  83333.333333       95000       75000          3  94.333333           25
HR       54750.000000       62000       50000          4  74.500000           16
IT       44600.000000       60000       30000          5  77.400000           12
```

### Syntax

```python
# output_col_name = ("source_col", "aggregation_function")
df.groupby("group_col").agg(
    new_col_name = ("source_col", "function"),
    ...
)
```

### With custom lambda functions

```python
df.groupby("dept").agg(
    salary_spread = ("salary", lambda x: x.max() - x.min()),
    top_score     = ("score",  "max"),
    avg_tenure    = ("years",  "mean")
)
```

> **💡 Always prefer named aggregations** in real code — your output is immediately readable and self-documenting with no extra steps.

---

## 🔗 Full GroupBy Analysis Pipeline

```python
import pandas as pd

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
titanic = pd.read_csv(url)

# 1. Survival rate by passenger class
print("── Survival Rate by Class ──")
print(titanic.groupby("Pclass")["Survived"].mean().round(2))

# 2. Named aggregation — class + gender summary
print("\n── Summary by Class & Gender ──")
print(titanic.groupby(["Pclass", "Sex"]).agg(
    avg_fare    = ("Fare",     "mean"),
    avg_age     = ("Age",      "mean"),
    total_count = ("Survived", "count"),
    survival_rt = ("Survived", "mean")
).round(1))

# 3. Add group average back to each row
titanic["class_avg_fare"] = titanic.groupby("Pclass")["Fare"].transform("mean")
titanic["fare_vs_class"]  = titanic["Fare"] - titanic["class_avg_fare"]

# 4. Pivot table — survival by class and gender
print("\n── Pivot: Survival by Class & Gender ──")
print(pd.pivot_table(
    titanic,
    values="Survived",
    index="Pclass",
    columns="Sex",
    aggfunc="mean",
    margins=True
).round(2))

# 5. Crosstab — class vs embarkation port
print("\n── Crosstab: Class vs Embarked ──")
print(pd.crosstab(titanic["Pclass"], titanic["Embarked"],
                  normalize="index").round(2))
```

---

## 🎯 Mini Project

**Analyze a sales dataset using GroupBy.**

```python
import pandas as pd
import numpy as np

np.random.seed(42)
n = 200

sales = pd.DataFrame({
    "order_id":   range(1, n+1),
    "product":    np.random.choice(["Laptop","Phone","Tablet","Monitor","Keyboard"], n),
    "category":   np.random.choice(["Electronics","Accessories"], n),
    "region":     np.random.choice(["North","South","East","West"], n),
    "rep":        np.random.choice(["Alice","Bob","Carol","David","Eve"], n),
    "units":      np.random.randint(1, 10, n),
    "unit_price": np.random.choice([500, 1500, 8000, 25000, 55000], n),
    "month":      np.random.choice(["Jan","Feb","Mar","Apr","May","Jun"], n)
})
sales["revenue"] = sales["units"] * sales["unit_price"]
```

Complete these tasks:

- [ ] Total revenue per **product** — which product earns the most?
- [ ] Average order value per **region**
- [ ] Use `.agg()` to get `total_revenue`, `avg_revenue`, `total_units`, `order_count` per **category**
- [ ] Use `.transform()` to add `region_avg_revenue` — how does each order compare to its region average?
- [ ] Rank sales reps by total revenue using `.groupby()` + `.sum()` + `.rank()`
- [ ] Build a **pivot table**: rows = region, columns = product, values = sum of revenue
- [ ] Use `pd.crosstab()` to count orders by region and month
- [ ] Use **named aggregations** for a clean per-rep summary: `total_revenue`, `avg_units`, `best_order`

---

## 🧠 Day 5 Quick Reference

```python
# ── Basic GroupBy ───────────────────────────────────────
df.groupby("col")["val"].mean()
df.groupby(["col1","col2"])["val"].sum()
df.groupby("col").size()                       # row count

# ── All aggregation methods ─────────────────────────────
g = df.groupby("col")
g["val"].sum()     g["val"].mean()    g["val"].median()
g["val"].min()     g["val"].max()     g["val"].std()
g["val"].count()   g["val"].nunique() g["val"].first()

# ── .agg() ──────────────────────────────────────────────
df.groupby("col")["val"].agg(["mean","max","count"])
df.groupby("col").agg({"a":"mean", "b":["min","max"]})

# ── Named aggregations ──────────────────────────────────
df.groupby("col").agg(
    avg_val  = ("val", "mean"),
    max_val  = ("val", "max"),
    n        = ("val", "count")
)

# ── .transform() ────────────────────────────────────────
df["grp_mean"] = df.groupby("col")["val"].transform("mean")
df["grp_rank"] = df.groupby("col")["val"].rank(ascending=False)
df["z_score"]  = df.groupby("col")["val"].transform(
                     lambda x: (x - x.mean()) / x.std())

# ── Pivot table ─────────────────────────────────────────
pd.pivot_table(df, values="val", index="a",
               columns="b", aggfunc="mean",
               margins=True, fill_value=0)

# ── Crosstab ────────────────────────────────────────────
pd.crosstab(df["a"], df["b"])
pd.crosstab(df["a"], df["b"], normalize="index")
pd.crosstab(df["a"], df["b"], values=df["val"], aggfunc="mean")

# ── value_counts ────────────────────────────────────────
df["col"].value_counts()
df["col"].value_counts(normalize=True)
```

---

## ⏭️ What's Next

| | Topic |
|---|---|
| ✅ Day 1 | Foundations & Data Structures |
| ✅ Day 2 | Selection & Filtering |
| ✅ Day 3 | Data Cleaning |
| ✅ Day 4 | Data Transformation |
| ✅ Day 5 | GroupBy & Aggregation |
| ▶️ **Day 6** | **Merging, Joining & Reshaping** — concat, merge, melt, pivot, stack |
| Day 7 | Time Series, Viz & Best Practices |

---

<div align="center">

**Day 5 Complete! 🎉**

*Pandas A–Z · 7-Day Course · Day 5 of 7*

</div>
