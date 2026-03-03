# 🐼 Pandas Day 2 — Selection & Filtering

> Learn how to slice, dice, and extract exactly the data you need from any DataFrame using boolean masks, queries, and powerful filter helpers.

---

## 📋 Table of Contents

1. [Select a Single Column](#1-select-a-single-column)
2. [Select Multiple Columns](#2-select-multiple-columns)
3. [Row Selection with .loc and .iloc](#3-row-selection-with-loc-and-iloc)
4. [Boolean Filtering](#4-boolean-filtering)
5. [Multiple Conditions — & and |](#5-multiple-conditions----and-)
6. [The .query() Method](#6-the-query-method)
7. [Filter Helpers — .isin(), .between(), .str.contains()](#7-filter-helpers----isin-between-strcontains)
8. [Mini Project](#-mini-project)

---

## 🗂️ Setup — Dataset We'll Use Today

Throughout Day 2 we'll work with a sample student dataset and the Titanic CSV.

```python
import pandas as pd

# Sample dataset
data = {
    "name":    ["Alice", "Bob", "Carol", "David", "Eve", "Frank"],
    "age":     [25, 30, 22, 35, 28, 19],
    "city":    ["Dhaka", "Jessore", "Sylhet", "Dhaka", "Chittagong", "Sylhet"],
    "score":   [88, 92, 75, 95, 60, 72],
    "passed":  [True, True, True, True, False, True],
    "grade":   ["B", "A", "C", "A", "F", "C"]
}

df = pd.DataFrame(data)
print(df)
```

```
    name  age        city  score  passed grade
0  Alice   25       Dhaka     88    True     B
1    Bob   30     Jessore     92    True     A
2  Carol   22      Sylhet     75    True     C
3  David   35       Dhaka     95    True     A
4    Eve   28  Chittagong     60   False     F
5  Frank   19      Sylhet     72    True     C
```

---

## 1. Select a Single Column

The simplest selection — pick one column using square brackets.

```python
# Returns a Series
names = df["name"]
print(names)
```

```
0    Alice
1      Bob
2    Carol
3    David
4      Eve
5    Frank
Name: name, dtype: object
```

```python
# You can also use dot notation (only when column name has no spaces)
ages = df.age
print(ages)
```

```
0    25
1    30
2    22
3    35
4    28
5    19
Name: age, dtype: int64
```

> ⚠️ **Prefer `df["col"]` over `df.col`** — dot notation breaks if the column name has spaces, matches a Pandas method name (like `df.count`), or is created dynamically.

---

## 2. Select Multiple Columns

Pass a **list of column names** inside square brackets — notice the double brackets `[[ ]]`.

```python
# Returns a DataFrame (not a Series)
subset = df[["name", "score", "grade"]]
print(subset)
```

```
    name  score grade
0  Alice     88     B
1    Bob     92     A
2  Carol     75     C
3  David     95     A
4    Eve     60     F
5  Frank     72     C
```

```python
# Store column names in a list — useful when columns change
cols = ["name", "age", "city"]
print(df[cols])
```

> **🔑 Key idea:** Single bracket `df["col"]` → returns **Series**. Double bracket `df[["col"]]` → returns **DataFrame**. This distinction matters when chaining operations.

---

## 3. Row Selection with `.loc` and `.iloc`

*(Building on Day 1 — now with more patterns)*

```python
# ── .loc[] — Label-based ──────────────────────────────

df.loc[0]                      # single row → Series
df.loc[2:4]                    # rows 2, 3, 4 (inclusive)
df.loc[[0, 2, 4]]              # specific rows by label list
df.loc[0, "name"]              # single cell → "Alice"
df.loc[0:3, "name":"score"]    # rows 0–3, columns name to score
df.loc[:, "age"]               # ALL rows, one column


# ── .iloc[] — Position-based ─────────────────────────

df.iloc[0]                     # first row → Series
df.iloc[2:4]                   # rows at position 2, 3 (exclusive end)
df.iloc[[0, 2, 4]]             # rows at positions 0, 2, 4
df.iloc[0, 0]                  # row 0, col 0 → "Alice"
df.iloc[0:3, 0:3]              # first 3 rows, first 3 columns
df.iloc[:, 1]                  # ALL rows, column at position 1
```

### Selecting a Single Cell

```python
# Two ways to get one specific value
val1 = df.loc[2, "score"]     # → 75
val2 = df.iloc[2, 3]          # → 75  (same cell)

# Fastest method for a single value
val3 = df.at[2, "score"]      # .at — optimized for single cell
val4 = df.iat[2, 3]           # .iat — optimized, position-based
```

| Method | Type | Speed | Use when |
|--------|------|-------|----------|
| `.loc[]` | Label | Normal | Selecting ranges or multiple cells |
| `.iloc[]` | Position | Normal | Selecting ranges by position |
| `.at[]` | Label | **Fast** | Accessing a single cell by label |
| `.iat[]` | Position | **Fast** | Accessing a single cell by position |

---

## 4. Boolean Filtering

This is the most powerful and most-used filtering technique. You create a **boolean mask** — a Series of `True`/`False` — then pass it into the DataFrame.

### How it works (step by step)

```python
# Step 1: Create a boolean mask
mask = df["score"] > 80
print(mask)
```

```
0     True
1     True
2    False
3     True
4    False
5    False
Name: score, dtype: bool
```

```python
# Step 2: Pass the mask to the DataFrame
result = df[mask]
print(result)
```

```
    name  age     city  score  passed grade
0  Alice   25    Dhaka     88    True     B
1    Bob   30  Jessore     92    True     A
3  David   35    Dhaka     95    True     A
```

```python
# In practice: do it in one line
df[df["score"] > 80]
```

### More Boolean Filter Examples

```python
# Equal to
df[df["city"] == "Dhaka"]

# Not equal to
df[df["grade"] != "F"]

# Greater than or equal to
df[df["age"] >= 28]

# Filter by boolean column directly
df[df["passed"]]             # passed == True
df[~df["passed"]]            # passed == False  (~ means NOT)

# String equality
df[df["grade"] == "A"]
```

> **🔑 Key idea:** The `~` operator inverts a boolean mask. `~df["passed"]` is the same as `df["passed"] == False`.

---

## 5. Multiple Conditions — `&` and `|`

Combine filters using `&` (AND) and `|` (OR). **Always wrap each condition in parentheses.**

```python
# AND — both conditions must be True
df[(df["score"] > 80) & (df["age"] < 30)]
```

```
    name  age   city  score  passed grade
0  Alice   25  Dhaka     88    True     B
```

```python
# OR — at least one condition must be True
df[(df["city"] == "Dhaka") | (df["city"] == "Sylhet")]
```

```
    name  age   city  score  passed grade
0  Alice   25  Dhaka     88    True     B
2  Carol   22  Sylhet    75    True     C
3  David   35  Dhaka     95    True     A
5  Frank   19  Sylhet    72    True     C
```

```python
# Three conditions combined
df[(df["score"] >= 75) & (df["passed"] == True) & (df["age"] < 35)]
```

```python
# NOT with & and |
df[~(df["city"] == "Dhaka") & (df["score"] > 70)]
```

> ⚠️ **Common mistake:** Using Python's `and` / `or` keywords instead of `&` / `|`. These will raise a `ValueError`. Always use `&` and `|` for Pandas conditions.

```python
# ❌ WRONG — raises ValueError
df[df["score"] > 80 and df["age"] < 30]

# ✅ CORRECT
df[(df["score"] > 80) & (df["age"] < 30)]
```

---

## 6. The `.query()` Method

`.query()` lets you write filters as a **readable string** — great for complex conditions and cleaner code.

```python
# Basic query — same as df[df["score"] > 80]
df.query("score > 80")

# Multiple conditions
df.query("score > 80 and age < 30")

# OR condition
df.query("city == 'Dhaka' or city == 'Sylhet'")

# NOT condition
df.query("grade != 'F'")

# Using a variable inside query with @
min_score = 75
df.query("score >= @min_score")
```

### `.query()` vs Boolean Filtering

```python
# These two are identical:
df[(df["score"] > 80) & (df["age"] < 30)]

df.query("score > 80 and age < 30")   # ← much cleaner!
```

| | Boolean Filter | `.query()` |
|---|---|---|
| **Readability** | Can get messy with multiple conditions | Clean string syntax |
| **Variable use** | Direct (`df["col"] > var`) | Use `@var` prefix |
| **Performance** | Same | Same |
| **Best for** | Simple 1–2 conditions | 3+ conditions |

---

## 7. Filter Helpers — `.isin()`, `.between()`, `.str.contains()`

These three methods make common filtering patterns much simpler.

### `.isin()` — Match any value from a list

```python
# Instead of: (df["city"] == "Dhaka") | (df["city"] == "Sylhet")
df[df["city"].isin(["Dhaka", "Sylhet"])]
```

```
    name  age    city  score  passed grade
0  Alice   25   Dhaka     88    True     B
2  Carol   22  Sylhet     75    True     C
3  David   35   Dhaka     95    True     A
5  Frank   19  Sylhet     72    True     C
```

```python
# Exclude a list of values with ~
df[~df["grade"].isin(["F", "C"])]     # only A and B grades

# Works great with a variable
good_cities = ["Dhaka", "Chittagong"]
df[df["city"].isin(good_cities)]
```

### `.between()` — Range filter (inclusive on both ends)

```python
# Age between 22 and 30 (inclusive)
df[df["age"].between(22, 30)]
```

```
    name  age        city  score  passed grade
0  Alice   25       Dhaka     88    True     B
2  Carol   22      Sylhet     75    True     C
4    Eve   28  Chittagong     60   False     F
```

```python
# Score between 70 and 90
df[df["score"].between(70, 90)]

# Combine with other filters
df[df["age"].between(20, 30) & (df["passed"] == True)]
```

> **💡 Tip:** `.between(a, b)` is equivalent to `(df["col"] >= a) & (df["col"] <= b)` — both ends are **inclusive**.

### `.str.contains()` — Substring search in text columns

```python
# Names containing the letter 'a' (case-sensitive)
df[df["name"].str.contains("a")]

# Case-insensitive search
df[df["name"].str.contains("a", case=False)]

# Cities starting with 'S'
df[df["city"].str.startswith("S")]

# Cities ending with 'a'
df[df["city"].str.endswith("a")]

# Names containing 'al' OR 'ob' using regex
df[df["name"].str.contains("al|ob", case=False)]
```

```python
# Handle NaN values safely — na=False prevents errors
df[df["name"].str.contains("alice", case=False, na=False)]
```

### All Three Helpers — Side by Side

```python
# .isin()     → "Is the value one of these?"
df[df["grade"].isin(["A", "B"])]

# .between()  → "Is the value in this range?"
df[df["score"].between(75, 95)]

# .str.contains() → "Does the text contain this?"
df[df["city"].str.contains("a", case=False)]
```

---

## 🔗 Combining Everything

Real-world filtering usually combines multiple techniques:

```python
# Load Titanic
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
titanic = pd.read_csv(url)

# Female passengers in 1st class who survived
titanic[
    (titanic["Sex"] == "female") &
    (titanic["Pclass"] == 1) &
    (titanic["Survived"] == 1)
]

# Passengers aged 18–40 from Southampton or Cherbourg
titanic[
    titanic["Age"].between(18, 40) &
    titanic["Embarked"].isin(["S", "C"])
]

# Passengers with "Miss" in their name
titanic[titanic["Name"].str.contains("Miss", na=False)]

# Same query using .query()
titanic.query("Sex == 'female' and Pclass == 1 and Survived == 1")
```

---

## 🎯 Mini Project

**Filter the Titanic dataset** using everything from today.

```python
import pandas as pd

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)
```

Complete these tasks:

- [ ] Select only the columns: `Name`, `Age`, `Sex`, `Pclass`, `Survived`
- [ ] Filter all passengers who **survived** (`Survived == 1`)
- [ ] Filter all **female** passengers in **1st class** who survived — how many are there?
- [ ] Find passengers whose age is **between 18 and 35**
- [ ] Find passengers whose name contains `"Mr."` using `.str.contains()`
- [ ] Use `.query()` to find male passengers in 3rd class who did NOT survive
- [ ] Combine: passengers who survived **AND** were aged between 10 and 18

**Bonus challenge:**
```python
# What % of female 1st-class passengers survived?
female_1st = df[(df["Sex"] == "female") & (df["Pclass"] == 1)]
survival_rate = female_1st["Survived"].mean() * 100
print(f"{survival_rate:.1f}%")
```

---

## 🧠 Day 2 Quick Reference

```python
# ── Single column ──────────────────────────────────────
df["col"]                          # → Series

# ── Multiple columns ───────────────────────────────────
df[["col1", "col2"]]               # → DataFrame

# ── Row selection ──────────────────────────────────────
df.loc[0:3, ["col1", "col2"]]      # by label
df.iloc[0:3, 0:2]                  # by position
df.at[0, "col"]                    # single cell (fast)

# ── Boolean filter ─────────────────────────────────────
df[df["col"] > value]
df[df["col"] == "text"]
df[~df["col"].isin(["a", "b"])]    # NOT in list

# ── Multiple conditions ────────────────────────────────
df[(df["a"] > 5) & (df["b"] == "x")]     # AND
df[(df["a"] > 5) | (df["b"] == "x")]     # OR
df[~(df["a"] > 5)]                        # NOT

# ── .query() ───────────────────────────────────────────
df.query("a > 5 and b == 'x'")
df.query("a > @my_var")            # use external variable

# ── Filter helpers ─────────────────────────────────────
df[df["col"].isin(["a", "b"])]          # match list
df[df["col"].between(10, 20)]           # range (inclusive)
df[df["col"].str.contains("txt")]       # substring search
df[df["col"].str.startswith("A")]       # starts with
df[df["col"].str.endswith("z")]         # ends with
```

---

## ⏭️ What's Next

| | Topic |
|---|---|
| ✅ Day 1 | Foundations & Data Structures |
| ✅ Day 2 | Selection & Filtering |
| ▶️ **Day 3** | **Data Cleaning** — missing values, duplicates, type fixing |
| Day 4 | Data Transformation |
| Day 5 | GroupBy & Aggregation |
| Day 6 | Merging, Joining & Reshaping |
| Day 7 | Time Series, Viz & Best Practices |

---

<div align="center">

**Day 2 Complete! 🎉**

*Pandas A–Z · 7-Day Course · Day 2 of 7*

</div>
