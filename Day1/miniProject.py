import pandas as pd

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# shape, info, describe
print(df.shape)
df.info()
print(df.describe())

# first 10 rows
print(df.head(10))

# columns with missing values
print(df.isnull().sum())
print((df.isnull().sum() > 0).sum())

# select Name and Age
print(df.loc[:, ["Name", "Age"]])

# first 5 rows using iloc
print(df.iloc[0:5])



