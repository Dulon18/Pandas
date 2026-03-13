import pandas as pd

# Load the Titanic dataset
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# 1. Check which columns have missing values
print(df.isnull().sum())

# 2. Fill missing Age values with the median age
df['Age'] = df['Age'].fillna(df['Age'].median())

# 3. Fill missing Embarked values with the mode
df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])

# 4. Drop the Cabin column
df = df.drop(columns=['Cabin'])

# 5. Remove duplicate rows
df = df.drop_duplicates()

# 6. Convert Age to integer (Int64 type)
df['Age'] = df['Age'].astype("Int64")

# 7. Standardize the Sex column to title case
df['Sex'] = df['Sex'].str.title()

# 8. Verify no missing values remain
print(df.isnull().sum())