# 🐼 Pandas Day 6 — Merging, Joining & Reshaping

> Learn how to combine multiple DataFrames and reshape data between wide and long formats — essential skills for working with real-world multi-table datasets.

---

## 📋 Table of Contents

1. [pd.concat() — Stacking DataFrames](#1-pdconcat----stacking-dataframes)
2. [pd.merge() — SQL-style Joins](#2-pdmerge----sql-style-joins)
3. [.join() — Index-based Joining](#3-join----index-based-joining)
4. [Merging on Multiple Keys](#4-merging-on-multiple-keys)
5. [.melt() — Wide to Long Format](#5-melt----wide-to-long-format)
6. [.pivot() — Long to Wide Format](#6-pivot----long-to-wide-format)
7. [Stack and Unstack — Multi-index Reshaping](#7-stack-and-unstack----multi-index-reshaping)
8. [Mini Project](#-mini-project)

---

## 🗂️ Setup — Datasets We'll Use Today

```python
import pandas as pd
import numpy as np

# Customers table
customers = pd.DataFrame({
    "customer_id": [1, 2, 3, 4, 5],
    "name":        ["Alice", "Bob", "Carol", "David", "Eve"],
    "city":        ["Dhaka", "Jessore", "Sylhet", "Dhaka", "Chittagong"],
    "tier":        ["Gold", "Silver", "Gold", "Bronze", "Silver"]
})

# Orders table
orders = pd.DataFrame({
    "order_id":    [101, 102, 103, 104, 105, 106, 107],
    "customer_id": [1, 2, 1, 3, 5, 1, 6],        # customer 4 has no orders
    "product":     ["Laptop","Phone","Tablet","Laptop","Phone","Monitor","Keyboard"],
    "amount":      [55000, 25000, 35000, 55000, 25000, 18000, 5000],
    "month":       ["Jan", "Jan", "Feb", "Feb", "Mar", "Mar", "Mar"]
})

# Products table
products = pd.DataFrame({
    "product":   ["Laptop", "Phone", "Tablet", "Monitor", "Keyboard"],
    "category":  ["Electronics", "Electronics", "Electronics",
                  "Electronics", "Accessories"],
    "cost":      [40000, 18000, 25000, 12000, 2000]
})

print("── Customers ──")
print(customers)
print("\n── Orders ──")
print(orders)
```

```
── Customers ──
   customer_id   name        city    tier
0            1  Alice       Dhaka    Gold
1            2    Bob     Jessore  Silver
2            3  Carol      Sylhet    Gold
3            4  David       Dhaka  Bronze
4            5    Eve  Chittagong  Silver

── Orders ──
   order_id  customer_id   product  amount month
0       101            1    Laptop   55000   Jan
1       102            2     Phone   25000   Jan
2       103            1    Tablet   35000   Feb
3       104            3    Laptop   55000   Feb
4       105            5     Phone   25000   Mar
5       106            1   Monitor   18000   Mar
6       107            6  Keyboard    5000   Mar
```

---

## 1. `pd.concat()` — Stacking DataFrames

`pd.concat()` stacks DataFrames either **vertically** (add rows) or **horizontally** (add columns).

### Stack rows vertically (axis=0, default)

```python
# Two DataFrames with the same columns
jan_sales = pd.DataFrame({
    "product": ["Laptop", "Phone"],
    "amount":  [55000, 25000],
    "month":   ["Jan", "Jan"]
})

feb_sales = pd.DataFrame({
    "product": ["Tablet", "Laptop"],
    "amount":  [35000, 55000],
    "month":   ["Feb", "Feb"]
})

# Stack them vertically
all_sales = pd.concat([jan_sales, feb_sales])
print(all_sales)
```

```
  product  amount month
0  Laptop   55000   Jan
1   Phone   25000   Jan
0  Tablet   35000   Feb
1  Laptop   55000   Feb
```

```python
# Reset index to avoid duplicate index values
all_sales = pd.concat([jan_sales, feb_sales], ignore_index=True)
print(all_sales)
```

```
  product  amount month
0  Laptop   55000   Jan
1   Phone   25000   Jan
2  Tablet   35000   Feb
3  Laptop   55000   Feb
```

### Add a key to identify the source

```python
all_sales = pd.concat(
    [jan_sales, feb_sales],
    keys=["January", "February"],
    ignore_index=False
)
print(all_sales)
```

```
             product  amount month
January  0    Laptop   55000   Jan
         1     Phone   25000   Jan
February 0    Tablet   35000   Feb
         1    Laptop   55000   Feb
```

### Stack columns horizontally (axis=1)

```python
df_a = pd.DataFrame({"name": ["Alice", "Bob"], "age": [25, 30]})
df_b = pd.DataFrame({"city": ["Dhaka", "Jessore"], "score": [88, 92]})

combined = pd.concat([df_a, df_b], axis=1)
print(combined)
```

```
    name  age     city  score
0  Alice   25    Dhaka     88
1    Bob   30  Jessore     92
```

### Handle mismatched columns

```python
# DataFrames with different columns — NaN fills missing
df1 = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
df2 = pd.DataFrame({"b": [5, 6], "c": [7, 8]})

pd.concat([df1, df2], ignore_index=True)
```

```
     a  b    c
0  1.0  3  NaN
1  2.0  4  NaN
2  NaN  5  7.0
3  NaN  6  8.0
```

```python
# Only keep columns present in BOTH DataFrames
pd.concat([df1, df2], join="inner", ignore_index=True)
```

```
   b
0  3
1  4
2  5
3  6
```

| Parameter | Options | Use when |
|-----------|---------|----------|
| `axis` | `0` (rows), `1` (cols) | Stack direction |
| `ignore_index` | `True` / `False` | Reset index after concat |
| `keys` | list of labels | Track which source each row came from |
| `join` | `"outer"` (default), `"inner"` | Keep all cols vs common cols only |

---

## 2. `pd.merge()` — SQL-style Joins

`pd.merge()` is the most powerful combining tool — joins two DataFrames on a common key column, just like SQL `JOIN`.

### The four join types

```
LEFT JOIN             RIGHT JOIN            INNER JOIN            OUTER JOIN
─────────────         ─────────────         ─────────────         ─────────────
All left rows    +    All right rows   +    Only matching    +    All rows from
matching right        matching left         rows in both          both tables
rows                  rows
(unmatched →NaN)      (unmatched →NaN)      (unmatched dropped)   (unmatched →NaN)
```

### INNER JOIN — only matching rows

```python
# Only customers who have placed at least one order
inner = pd.merge(customers, orders, on="customer_id", how="inner")
print(inner)
```

```
   customer_id   name        city    tier  order_id   product  amount month
0            1  Alice       Dhaka    Gold       101    Laptop   55000   Jan
1            1  Alice       Dhaka    Gold       103    Tablet   35000   Feb
2            1  Alice       Dhaka    Gold       106   Monitor   18000   Mar
3            2    Bob     Jessore  Silver       102     Phone   25000   Jan
4            3  Carol      Sylhet    Gold       104    Laptop   55000   Feb
5            5    Eve  Chittagong  Silver       105     Phone   25000   Mar
```

> Customer 4 (David) and Order 107 (customer_id=6) are both **excluded** — no match exists for either.

### LEFT JOIN — all left rows, matching right rows

```python
# All customers — show orders where they exist, NaN where they don't
left = pd.merge(customers, orders, on="customer_id", how="left")
print(left)
```

```
   customer_id   name        city    tier  order_id   product   amount month
0            1  Alice       Dhaka    Gold     101.0    Laptop  55000.0   Jan
1            1  Alice       Dhaka    Gold     103.0    Tablet  35000.0   Feb
2            1  Alice       Dhaka    Gold     106.0   Monitor  18000.0   Mar
3            2    Bob     Jessore  Silver     102.0     Phone  25000.0   Jan
4            3  Carol      Sylhet    Gold     104.0    Laptop  55000.0   Feb
5            4  David       Dhaka  Bronze       NaN      None      NaN  None
6            5    Eve  Chittagong  Silver     105.0     Phone  25000.0   Mar
```

> David appears with NaN — he's a customer but has no orders.

### RIGHT JOIN — all right rows, matching left rows

```python
# All orders — show customer info where it exists
right = pd.merge(customers, orders, on="customer_id", how="right")
print(right)
```

```
   customer_id   name        city    tier  order_id   product  amount month
0          1.0  Alice       Dhaka    Gold       101    Laptop   55000   Jan
1          1.0  Alice       Dhaka    Gold       103    Tablet   35000   Feb
2          1.0  Alice       Dhaka    Gold       106   Monitor   18000   Mar
3          2.0    Bob     Jessore  Silver       102     Phone   25000   Jan
4          3.0  Carol      Sylhet    Gold       104    Laptop   55000   Feb
5          5.0    Eve  Chittagong  Silver       105     Phone   25000   Mar
6          NaN   None        None    None       107  Keyboard    5000   Mar
```

> Order 107 (customer_id=6) appears with NaN — order exists but customer record doesn't.

### OUTER JOIN — all rows from both tables

```python
# Every customer AND every order — NaN where no match
outer = pd.merge(customers, orders, on="customer_id", how="outer")
```

### Visualizing join types

```
customers:   1  2  3  4  5          orders:   1  1  1  2  3  5  6
                                              ↑ customer_ids in orders

INNER:       1  2  3     5          (4 dropped — no orders)
                                    (6 dropped — no customer record)

LEFT:        1  2  3  4  5          (4 kept with NaN)
                                    (6 dropped)

RIGHT:       1  2  3     5  6       (4 dropped)
                                    (6 kept with NaN)

OUTER:       1  2  3  4  5  6       (all kept, NaN where no match)
```

### Rename conflicting columns with `suffixes`

```python
# Both DataFrames have a 'name' column
df1 = pd.DataFrame({"id": [1,2], "name": ["Alice","Bob"],  "score": [88,92]})
df2 = pd.DataFrame({"id": [1,2], "name": ["AliceCo","BobCo"], "revenue": [5000,8000]})

merged = pd.merge(df1, df2, on="id", suffixes=("_person", "_company"))
print(merged)
```

```
   id name_person  score name_company  revenue
0   1       Alice     88      AliceCo     5000
1   2         Bob     92        BobCo     8000
```

---

## 3. `.join()` — Index-based Joining

`.join()` merges two DataFrames using their **index** instead of a column.

```python
# Set customer_id as index on both DataFrames
cust_indexed = customers.set_index("customer_id")
ord_indexed  = orders.set_index("customer_id")

# Join on index
result = cust_indexed.join(ord_indexed, how="left", lsuffix="_cust", rsuffix="_ord")
print(result.head())
```

```python
# Shortcut — when one DataFrame has the key as index
# and the other has it as a column, use merge() instead
# .join() is most useful when both share a natural index
```

> **💡 When to use `.join()` vs `.merge()`:**
> - Use `.merge()` for most joins — it's more explicit and flexible
> - Use `.join()` as a shortcut when joining on the index

---

## 4. Merging on Multiple Keys

Merge on two or more columns at once to avoid false matches.

```python
# Sales data with the same product appearing in multiple regions
sales_q1 = pd.DataFrame({
    "product": ["Laptop", "Phone", "Laptop", "Phone"],
    "region":  ["North",  "North", "South",  "South"],
    "q1_units":[100, 200, 150, 250]
})

sales_q2 = pd.DataFrame({
    "product": ["Laptop", "Phone", "Laptop", "Phone"],
    "region":  ["North",  "North", "South",  "South"],
    "q2_units":[120, 180, 170, 230]
})

# Merge on BOTH product AND region
result = pd.merge(sales_q1, sales_q2, on=["product", "region"])
print(result)
```

```
  product region  q1_units  q2_units
0  Laptop  North       100       120
1   Phone  North       200       180
2  Laptop  South       150       170
3   Phone  South       250       230
```

### Merge on columns with different names

```python
# Left has 'cust_id', right has 'customer_id'
pd.merge(
    df_left,
    df_right,
    left_on="cust_id",
    right_on="customer_id"
)
```

### Merge on index and column

```python
# Left key is a column, right key is the index
pd.merge(
    df_left,
    df_right,
    left_on="customer_id",
    right_index=True
)
```

---

## 5. `.melt()` — Wide to Long Format

`.melt()` transforms a **wide** table (many columns) into a **long** table (fewer columns, more rows). Essential for tidy data and visualization.

### Understanding wide vs long

```
WIDE FORMAT                          LONG FORMAT
─────────────────────────────────    ─────────────────────────────
name   Jan    Feb    Mar             name   month   sales
Alice  50000  35000  18000    →      Alice  Jan     50000
Bob    25000  40000  30000           Alice  Feb     35000
                                     Alice  Mar     18000
                                     Bob    Jan     25000
                                     Bob    Feb     40000
                                     Bob    Mar     30000
```

```python
# Wide format — monthly sales per person
wide = pd.DataFrame({
    "name": ["Alice", "Bob", "Carol"],
    "Jan":  [50000, 25000, 45000],
    "Feb":  [35000, 40000, 30000],
    "Mar":  [18000, 30000, 22000]
})

print("── Wide ──")
print(wide)

# Melt to long format
long = wide.melt(
    id_vars="name",           # columns to keep as-is
    value_vars=["Jan","Feb","Mar"],  # columns to melt
    var_name="month",         # name for the new variable column
    value_name="sales"        # name for the new value column
)

print("\n── Long ──")
print(long.sort_values(["name","month"]).reset_index(drop=True))
```

```
── Wide ──
    name    Jan    Feb    Mar
0  Alice  50000  35000  18000
1    Bob  25000  40000  30000
2  Carol  45000  30000  22000

── Long ──
    name month  sales
0  Alice   Feb  35000
1  Alice   Jan  50000
2  Alice   Mar  18000
3    Bob   Feb  40000
4    Bob   Jan  25000
5    Bob   Mar  30000
6  Carol   Feb  30000
7  Carol   Jan  45000
8  Carol   Mar  22000
```

### Real-world example — Titanic

```python
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
titanic = pd.read_csv(url)

# Melt SibSp and Parch into one 'relatives' column
melted = titanic[["Name","SibSp","Parch"]].head(5).melt(
    id_vars="Name",
    value_vars=["SibSp","Parch"],
    var_name="relative_type",
    value_name="count"
)
print(melted)
```

---

## 6. `.pivot()` — Long to Wide Format

`.pivot()` is the **reverse of melt** — turns a long table back into a wide table.

```python
# Start with the long format from above
print(long)

# Pivot back to wide
wide_again = long.pivot(
    index="name",    # column to use as row labels
    columns="month", # column whose values become new columns
    values="sales"   # column whose values fill the cells
)

print(wide_again)
```

```
month    Feb    Jan    Mar
name
Alice  35000  50000  18000
Bob    40000  25000  30000
Carol  30000  45000  22000
```

```python
# Clean up the column axis name
wide_again.columns.name = None
wide_again = wide_again.reset_index()
print(wide_again)
```

```
    name    Feb    Jan    Mar
0  Alice  35000  50000  18000
1    Bob  40000  25000  30000
2  Carol  30000  45000  22000
```

### `.pivot()` vs `pd.pivot_table()`

| | `.pivot()` | `pd.pivot_table()` |
|---|---|---|
| **Duplicates** | Raises error if duplicate index+column combinations | Aggregates duplicates |
| **Aggregation** | None — just reshapes | Required — mean, sum, etc. |
| **Use for** | Clean long→wide reshaping | Summarizing with aggregation |

```python
# .pivot() FAILS with duplicates
# Use pd.pivot_table() when you have duplicate index+column combos
pd.pivot_table(long, values="sales", index="name",
               columns="month", aggfunc="sum")
```

---

## 7. Stack and Unstack — Multi-index Reshaping

`stack()` and `unstack()` move levels between the column axis and the row index — useful for working with multi-level (hierarchical) DataFrames.

### `.stack()` — columns → index (wide to long)

```python
# Start with wide multi-column data
df_wide = pd.DataFrame({
    ("Sales",  "Jan"): [100, 200],
    ("Sales",  "Feb"): [120, 180],
    ("Profit", "Jan"): [20,  40],
    ("Profit", "Feb"): [25,  35]
}, index=["North", "South"])

df_wide.columns = pd.MultiIndex.from_tuples(df_wide.columns)
print(df_wide)
```

```
      Sales      Profit
        Jan  Feb    Jan  Feb
North   100  120     20   25
South   200  180     40   35
```

```python
# Stack — move innermost column level to row index
stacked = df_wide.stack()
print(stacked)
```

```
            Profit  Sales
North Jan       20    100
      Feb       25    120
South Jan       40    200
      Feb       35    180
```

### `.unstack()` — index → columns (long to wide)

```python
# Reverse — move innermost index level back to columns
unstacked = stacked.unstack()
print(unstacked)
```

```
      Profit      Sales
         Jan  Feb   Jan  Feb
North     20   25   100  120
South     40   35   200  180
```

### Practical example with groupby

```python
# GroupBy result with multi-index → use unstack to make it readable
result = df.groupby(["dept", "gender"])["salary"].mean()
print(result)
```

```
dept     gender
Finance  F    95000.0
         M    77500.0
HR       F    52333.3
         M    62000.0
IT       F    42500.0
         M    46000.0
```

```python
# Unstack gender from index to columns
print(result.unstack())
```

```
gender        F         M
dept
Finance   95000.0   77500.0
HR        52333.3   62000.0
IT        42500.0   46000.0
```

---

## 🔗 Full Merge & Reshape Pipeline

```python
import pandas as pd

# ── Step 1: Merge customers + orders + products ────────
full = (
    pd.merge(orders, customers, on="customer_id", how="left")
      .merge(products, on="product", how="left")
)

print(full[["name", "product", "category", "amount", "cost", "month"]])
```

```
    name   product     category  amount   cost month
0  Alice    Laptop  Electronics   55000  40000   Jan
1    Bob     Phone  Electronics   25000  18000   Jan
2  Alice    Tablet  Electronics   35000  25000   Feb
3  Carol    Laptop  Electronics   55000  40000   Feb
4    Eve     Phone  Electronics   25000  18000   Mar
5  Alice   Monitor  Electronics   18000  12000   Mar
6    NaN  Keyboard  Accessories    5000   2000   Mar
```

```python
# ── Step 2: Add profit column ──────────────────────────
full["profit"] = full["amount"] - full["cost"]

# ── Step 3: Monthly revenue summary ───────────────────
monthly = full.groupby("month").agg(
    total_revenue = ("amount", "sum"),
    total_profit  = ("profit", "sum"),
    order_count   = ("order_id", "count")
).reset_index()

# ── Step 4: Pivot to wide format ───────────────────────
wide_monthly = monthly.melt(
    id_vars="month",
    value_vars=["total_revenue", "total_profit"],
    var_name="metric",
    value_name="value"
).pivot(index="metric", columns="month", values="value")

print(wide_monthly)
```

---

## 🎯 Mini Project

**Merge and reshape a multi-table dataset.**

```python
import pandas as pd

# Load these two Titanic-related tables
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
titanic = pd.read_csv(url)

# Create a separate 'class info' table
class_info = pd.DataFrame({
    "Pclass":       [1, 2, 3],
    "class_name":   ["First", "Second", "Third"],
    "base_fare":    [50, 15, 8],
    "deck":         ["A-E", "D-F", "G"]
})
```

Complete these tasks:

- [ ] **Merge** `titanic` with `class_info` on `Pclass` (left join) — add class name and deck info
- [ ] Use `pd.concat()` to stack survivors and non-survivors into one DataFrame with a `"group"` key
- [ ] **Melt** the result to create a long-format table with `SibSp` and `Parch` as a single `relatives` column
- [ ] Create a **wide summary table**: rows = Pclass, columns = Sex, values = survival rate using `pivot_table()`
- [ ] **Unstack** the result of `groupby(["Pclass","Sex"])["Survived"].mean()` to make it wide
- [ ] Merge on **multiple keys**: find passengers with the same `Pclass` AND `Embarked` using a self-merge trick
- [ ] Build a **monthly boarding analysis**: use `pd.crosstab()` to count passengers by class and embarkation port

**Bonus challenge:**
```python
# Chain all three merges in one pipeline
# titanic → class_info → a custom fare_bands table
fare_bands = pd.DataFrame({
    "fare_band": ["Low", "Mid", "High"],
    "fare_min":  [0,   50,  100],
    "fare_max":  [50, 100, 9999]
})
# Hint: use pd.cut() to create a fare_band column first, then merge
```

---

## 🧠 Day 6 Quick Reference

```python
# ── pd.concat() ─────────────────────────────────────────
pd.concat([df1, df2])                        # stack rows
pd.concat([df1, df2], ignore_index=True)     # reset index
pd.concat([df1, df2], axis=1)                # stack columns
pd.concat([df1, df2], join="inner")          # only common cols
pd.concat([df1, df2], keys=["a","b"])        # add source labels

# ── pd.merge() ──────────────────────────────────────────
pd.merge(df1, df2, on="key")                 # inner join (default)
pd.merge(df1, df2, on="key", how="left")     # left join
pd.merge(df1, df2, on="key", how="right")    # right join
pd.merge(df1, df2, on="key", how="outer")    # outer join
pd.merge(df1, df2, on=["k1","k2"])           # multi-key join
pd.merge(df1, df2, left_on="a", right_on="b")# different key names
pd.merge(df1, df2, on="key", suffixes=("_x","_y"))  # rename conflicts

# ── .join() ─────────────────────────────────────────────
df1.join(df2, how="left")                    # join on index

# ── .melt() — wide → long ───────────────────────────────
df.melt(id_vars="id",
        value_vars=["col1","col2"],
        var_name="variable",
        value_name="value")

# ── .pivot() — long → wide ──────────────────────────────
df.pivot(index="row_col",
         columns="col_col",
         values="val_col")

# ── stack / unstack ─────────────────────────────────────
df.stack()                                   # cols → row index
df.unstack()                                 # row index → cols
grouped.unstack("col")                       # unstack specific level
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
| ✅ Day 6 | Merging, Joining & Reshaping |
| ▶️ **Day 7** | **Time Series, Viz & Best Practices** — dates, resampling, plotting, performance |

---

<div align="center">

**Day 6 Complete! 🎉**

*Pandas A–Z · 7-Day Course · Day 6 of 7*

</div>
