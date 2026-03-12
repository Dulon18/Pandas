import pandas as pd

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# 1. Select only required columns
df_filtered = df[['Name', 'Age', 'Sex', 'Pclass', 'Survived']]
df_filtered.head()


# 2. Filter all passengers who survived
survived_passengers = df_filtered[df_filtered['Survived'] == 1]
survived_passengers.head()


# 3. Female passengers in 1st class who survived
female_first_survived = df_filtered[
    (df_filtered['Sex'] == 'female') &
    (df_filtered['Pclass'] == 1) &
    (df_filtered['Survived'] == 1)
]

# Count
female_first_survived_count = female_first_survived.shape[0]
print(female_first_survived_count)


# 4. Passengers whose age is between 18 and 35
age_18_35 = df_filtered[
    (df_filtered['Age'] >= 18) &
    (df_filtered['Age'] <= 35)
]
age_18_35.head()


# 5. Passengers whose name contains "Mr."
mr_passengers = df_filtered[df_filtered['Name'].str.contains("Mr.", na=False)]
mr_passengers.head()


# 6. Male passengers in 3rd class who did NOT survive (using query)
male_3rd_not_survived = df_filtered.query("Sex == 'male' and Pclass == 3 and Survived == 0")
male_3rd_not_survived.head()


# 7. Passengers who survived AND were aged between 10 and 18
survived_10_18 = df_filtered[
    (df_filtered['Survived'] == 1) &
    (df_filtered['Age'].between(10, 18))
]

survived_10_18.head()
