import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# Load the already-cleaned file
df = pd.read_csv("Superstore_cleaned_last2.csv", encoding="UTF-8")

# dates
df["Order Date"] = pd.to_datetime(df["Order Date"], format="%Y-%m-%d")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%Y-%m-%d")

# remove garbage characters in Customer and Product Name columns
df["Customer Name"] = df["Customer Name"].str.replace(r"[^\x00-\x7f]+", "", regex=True)
df["Product Name"] = df["Product Name"].str.replace(r"[^\x00-\x7f]+", " ", regex=True)

# strip spaces and collapse double spaces
for c in ["Customer Name", "Product Name"]:
    df[c] = df[c].str.replace(r"\s+", " ", regex=True).str.strip()

# # print to check the data 
# print("Ship before order:", (df["Ship Date"] < df["Order Date"]).sum())
# print("Nulls:", df.isnull().sum().sum())

# # remove duplicates has to to be last inn order
# print("Duplicates:", df.duplicated().sum())
# df = df.drop_duplicates()
# print(df.shape)

# save the clean data
df.to_csv("Superstore_cleaned_last2.csv", index=False)