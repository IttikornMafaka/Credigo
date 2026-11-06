import pandas as pd 
df = pd.read_csv("credigo_credit_default_dataset.csv")
print("Dataset Shape:", df.shape)

print("\nFirst 5 Rows:")
print(df.head())

print("\nData Types:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nTarget Distribution:")
print(df["default_flag"].value_counts())

print("\nTarget Percentage:")
print(df["default_flag"].value_counts(normalize=True) * 100)