"""
Step 2: Create new columns (feature engineering).

Input:  data/Superstore_cleaned.csv  (output of 01_cleaning.py)
Output: data/Superstore_step2.csv    (9,993 rows, 27 columns)

Run from anywhere:  python 02_features.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent / "data"

df = pd.read_csv(DATA / "Superstore_cleaned.csv", encoding="utf-8")

# Dates come back from a CSV as text, so convert them again
df["Order Date"] = pd.to_datetime(df["Order Date"], format="%Y-%m-%d")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%Y-%m-%d")

# 1. Date parts (from Order Date)
df["Month"] = df["Order Date"].dt.month
df["Year"] = df["Order Date"].dt.year
df["Week Day"] = df["Order Date"].dt.dayofweek      # 0 = Monday ... 6 = Sunday
df["Quarter"] = df["Order Date"].dt.quarter

# 2. Days between order and shipping
df["Ship Days"] = (df["Ship Date"] - df["Order Date"]).dt.days

# 3. Price of one item (Sales is already after discount)
df["Unit Price"] = df["Sales"] / df["Quantity"]

# 4. Target: 1 if the order lost money, else 0
df["Is Loss"] = (df["Profit"] < 0).astype(int)

# 5. Product key: some Product IDs are used for two different product names,
#    so ID + name identifies each product. The original Product IDs are not changed.
df["Product Key"] = df["Product ID"] + " | " + df["Product Name"]

# 6. Log of Sales, to reduce the skew (log1p = log(1 + x), safe for small values)
df["Log Sales"] = np.log1p(df["Sales"])

# 7. Drop City (531 values, too many). We keep State and Region for location.
df = df.drop(columns=["City"])

# 8. Discount bands
#    No Discount = 0, Low = up to 20%, Medium = 20-40%, High = over 40%
#    (don't call the first band "None": pandas reads "None" back as a missing value)
df["Discount Band"] = pd.cut(
    df["Discount"],
    bins=[-0.01, 0, 0.2, 0.4, 1],
    labels=["No Discount", "Low", "Medium", "High"],
)

# Checks
print("Shape:", df.shape)                                            # expected: (9993, 27)
print("Ship Days:", df["Ship Days"].min(), "to", df["Ship Days"].max())   # expected: 0 to 7
print("Years:", df["Year"].min(), "to", df["Year"].max())                  # expected: 2014 to 2017
print("Loss share:", round(df["Is Loss"].mean(), 3))                       # expected: 0.187
print("Sales skew:", round(df["Sales"].skew(), 2), "-> Log Sales skew:", round(df["Log Sales"].skew(), 2))
print("Missing values:", df.isnull().sum().sum())                          # expected: 0
print("\nLoss rate by discount band (%):")
print((df.groupby("Discount Band", observed=True)["Is Loss"].mean() * 100).round(1))

# Save
df.to_csv(DATA / "Superstore_step2.csv", index=False, date_format="%Y-%m-%d")
print("\nSaved data/Superstore_step2.csv")
