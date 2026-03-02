# 🐼 Pandas A to Z — 7-Day Learning Plan

> A structured, project-driven roadmap to go from zero to confident with **Python Pandas** in just 7 days.

---

## 📋 Overview

| Day | Topic | Level | Time |
|-----|-------|-------|------|
| [Day 1](#-day-1--foundations--data-structures) | Foundations & Data Structures | 🟢 Beginner | 3–4 hrs |
| [Day 2](#-day-2--selection--filtering) | Selection & Filtering | 🟢 Beginner | 3–4 hrs |
| [Day 3](#-day-3--data-cleaning) | Data Cleaning | 🟡 Intermediate | 4–5 hrs |
| [Day 4](#-day-4--data-transformation) | Data Transformation | 🟡 Intermediate | 4–5 hrs |
| [Day 5](#-day-5--groupby--aggregation) | GroupBy & Aggregation | 🟡 Intermediate | 4–5 hrs |
| [Day 6](#-day-6--merging-joining--reshaping) | Merging, Joining & Reshaping | 🔴 Advanced | 4–5 hrs |
| [Day 7](#-day-7--time-series-viz--best-practices) | Time Series, Viz & Best Practices | 🔴 Advanced | 4–5 hrs |

**Total commitment:** ~28–37 hours over 7 days

---

## 📦 Prerequisites

```bash
pip install pandas numpy matplotlib jupyter
```

> **Recommended:** Use [Jupyter Notebook](https://jupyter.org/) or [Google Colab](https://colab.research.google.com/) for all exercises.

---

## 📅 Day 1 — Foundations & Data Structures

> *"Know your tools before you use them."*

### Topics
- [ ] Install Pandas & set up Jupyter Notebook
- [ ] What is a **Series**? Create from list and dict
- [ ] What is a **DataFrame**? Create from dict and list of dicts
- [ ] Key attributes: `.shape`, `.dtypes`, `.columns`, `.index`
- [ ] Exploration methods: `.head()`, `.tail()`, `.info()`, `.describe()`
- [ ] Indexing basics: `.loc[]` vs `.iloc[]`
- [ ] Reading files: `pd.read_csv()`, `pd.read_excel()`

### 🎯 Mini Project
> Load the [Titanic dataset](https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv) and explore it using `.info()`, `.describe()`, and `.head(20)`. Write down 3 observations about the data.

---

## 📅 Day 2 — Selection & Filtering

> *"Find exactly what you need, nothing more."*

### Topics
- [ ] Select a single column: `df["col"]`
- [ ] Select multiple columns: `df[["col1", "col2"]]`
- [ ] Row selection with `.loc[]` and `.iloc[]`
- [ ] Boolean filtering: `df[df["age"] > 25]`
- [ ] Multiple conditions using `&` and `|` operators
- [ ] The `.query()` method for readable filters
- [ ] Useful filter helpers: `.isin()`, `.between()`, `.str.contains()`

### 🎯 Mini Project
> From the Titanic dataset, filter all passengers who **survived**, are **female**, and were in **1st class**. How many are there?

---

## 📅 Day 3 — Data Cleaning

> *"Garbage in, garbage out — clean your data first."*

### Topics
- [ ] Detect missing values: `.isnull()`, `.notnull()`, `.isnull().sum()`
- [ ] Drop missing data: `.dropna()` with `how`, `subset`, `thresh` options
- [ ] Fill missing data: `.fillna()` with values, `.ffill()`, `.bfill()`
- [ ] Find duplicates: `.duplicated()` and remove with `.drop_duplicates()`
- [ ] Rename columns: `.rename(columns={...})`
- [ ] Change data types: `.astype()`
- [ ] String cleaning: `.str.strip()`, `.str.lower()`, `.str.replace()`

### 🎯 Mini Project
> Take a messy CSV with missing values, wrong types, and duplicates. Clean it completely: fill or drop nulls, fix column types, and remove duplicate rows.

---

## 📅 Day 4 — Data Transformation

> *"Shape your data to answer your questions."*

### Topics
- [ ] Create new columns from existing ones: `df["new"] = df["a"] + df["b"]`
- [ ] `.apply()` on columns and rows
- [ ] `.map()` for element-wise transformations
- [ ] Lambda functions with `.apply()`
- [ ] `.replace()` for value substitution
- [ ] Bin numeric data: `pd.cut()` and `pd.qcut()`
- [ ] Encode categorical variables (label encoding, one-hot with `pd.get_dummies()`)

### 🎯 Mini Project
> Add an `age_group` column (Child / Teen / Adult / Senior), normalize a numeric column to 0–1 range, and one-hot encode a categorical column.

---

## 📅 Day 5 — GroupBy & Aggregation

> *"Find the story hidden inside groups."*

### Topics
- [ ] `.groupby()` on single and multiple columns
- [ ] Aggregation methods: `.sum()`, `.mean()`, `.count()`, `.min()`, `.max()`
- [ ] Custom aggregations with `.agg({...})`
- [ ] `.transform()` for group-wise operations (without collapsing rows)
- [ ] Pivot tables: `pd.pivot_table()`
- [ ] Cross-tabulations: `pd.crosstab()`
- [ ] Named aggregations: `.agg(total=("price", "sum"))`

### 🎯 Mini Project
> Using a sales dataset: calculate **total revenue per category**, **average order value by region**, and **top 5 products by quantity sold**.

---

## 📅 Day 6 — Merging, Joining & Reshaping

> *"Combine and reshape data like a pro."*

### Topics
- [ ] Stack DataFrames: `pd.concat()` (axis=0 and axis=1)
- [ ] SQL-style joins: `pd.merge()` — inner, left, right, outer
- [ ] The `.join()` method on index
- [ ] Merging on multiple keys
- [ ] Wide → Long format: `.melt()`
- [ ] Long → Wide format: `.pivot()`
- [ ] Multi-index: `.stack()` and `.unstack()`

### 🎯 Mini Project
> Merge two datasets (customers + orders) on a common key, then reshape the result into a **monthly sales summary table**.

---

## 📅 Day 7 — Time Series, Viz & Best Practices

> *"Bring your analysis to life."*

### Topics
- [ ] Parse dates: `pd.to_datetime()`, `parse_dates` in `read_csv`
- [ ] DatetimeIndex and the `.dt` accessor: `.dt.year`, `.dt.month`, `.dt.day_name()`
- [ ] Resample time data: `.resample("M").sum()`
- [ ] Rolling averages: `.rolling(7).mean()`
- [ ] Quick plots: `.plot()`, `.plot.bar()`, `.plot.hist()`, `.plot.scatter()`
- [ ] Method chaining for clean, readable code
- [ ] Performance tips: vectorization vs `.apply()`, memory-efficient dtypes

### 🎯 Capstone Project
> **End-to-end analysis:** Take a raw real-world dataset, clean it, transform it, group it, merge it with another source, and produce at least 3 meaningful visualizations. Write a short summary of your findings.

> **Suggested datasets:** [Kaggle](https://www.kaggle.com/datasets) · [UCI ML Repo](https://archive.ics.uci.edu/) · [Our World in Data](https://ourworldindata.org/)

---

## 🧠 Quick Reference Cheatsheet

```python
# ── Creation ───────────────────────────────────────
pd.Series([1, 2, 3])
pd.DataFrame({"a": [1,2], "b": [3,4]})
pd.read_csv("file.csv", parse_dates=["date"])

# ── Exploration ────────────────────────────────────
df.shape         # (rows, cols)
df.dtypes        # column types
df.info()        # overview + nulls
df.describe()    # stats summary

# ── Selection ──────────────────────────────────────
df["col"]                  # single column
df[["col1","col2"]]        # multiple columns
df.loc[0:5, "col"]         # label-based
df.iloc[0:5, 0:3]          # position-based
df[df["age"] > 25]         # boolean filter
df.query("age > 25")       # query string

# ── Cleaning ───────────────────────────────────────
df.isnull().sum()          # count nulls
df.dropna(subset=["col"])  # drop rows with null in col
df.fillna(0)               # fill nulls
df.drop_duplicates()       # remove dupes
df.astype({"col": "int"})  # change type

# ── Transform ──────────────────────────────────────
df["new"] = df["a"] * 2
df["col"].apply(lambda x: x.upper())
pd.cut(df["age"], bins=[0,18,65,100], labels=["Youth","Adult","Senior"])

# ── GroupBy ────────────────────────────────────────
df.groupby("col")["val"].mean()
df.groupby("col").agg(total=("val","sum"), avg=("val","mean"))

# ── Merge / Concat ─────────────────────────────────
pd.concat([df1, df2])                         # stack rows
pd.merge(df1, df2, on="id", how="left")       # left join
df.melt(id_vars=["id"], value_vars=["a","b"]) # wide → long

# ── Time Series ────────────────────────────────────
df["date"] = pd.to_datetime(df["date"])
df.set_index("date").resample("M").sum()
df["val"].rolling(7).mean()
```

---

## 📚 Recommended Resources

| Resource | Type | Link |
|----------|------|-------|
| Official Pandas Docs | Documentation | [pandas.pydata.org](https://pandas.pydata.org/docs/) |
| Kaggle Pandas Course | Free Course | [kaggle.com/learn/pandas](https://www.kaggle.com/learn/pandas) |
| Titanic Dataset | Practice Data | [Download CSV](https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv) |
| Python for Data Analysis (Wes McKinney) | Book | O'Reilly |

---

## ✅ Daily Checklist

- [ ] Day 1 — Foundations & Data Structures
- [ ] Day 2 — Selection & Filtering
- [ ] Day 3 — Data Cleaning
- [ ] Day 4 — Data Transformation
- [ ] Day 5 — GroupBy & Aggregation
- [ ] Day 6 — Merging, Joining & Reshaping
- [ ] Day 7 — Time Series, Viz & Best Practices 🎉

---

<div align="center">

**Happy Learning! 🚀**

*Built for focused learners · 7 days · ~4 hrs/day · Python Data Analysis*

</div>
