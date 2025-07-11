# 1. IMPORT LIBRARIES
import pandas as pd
import matplotlib.pyplot as plt

# LOAD DATA
df = pd.read_csv("data/movie_dataset.csv")

# INITIAL INSPECTION
print("\nDataset shape:", df.shape)
print("\nColumns:\n", df.columns)
print("\nBasic Info:")
print(df.info())
print("\nSummary Statistics:")
print(df.describe())

# CHECK MISSING VALUES
print("\nMissing values per column:")
print(df.isnull().sum().sort_values(ascending=False))

# DROP UNUSED COLUMNS & MISSING VALUES
cols_to_drop = ['status','revenue','poster_path', 'backdrop_path','budget','video','imdb_id','tagline','homepage','production_companies','production_countries','keywords']
df_clean_col = df.drop(columns=[col for col in cols_to_drop if col in df.columns])

df_clean = df_clean_col.dropna()

print(df_clean.head())
print(len(df_clean))

df_sample = df_clean.sample(frac=0.5, random_state=42)  # keep 50%
df_sample.to_csv("cleaned_dataset.csv", index=False)

import os
file_size = os.path.getsize("cleaned_dataset.csv") / (1024 * 1024)  # size in MB
print(f"File size: {file_size:.2f} MB")




