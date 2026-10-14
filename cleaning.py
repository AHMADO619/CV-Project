import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# Load the data
df = pd.read_csv("Superstore.csv", encoding='latin1')

# # remove the postal code column no need for it
# df.drop(columns=['Postal Code'], inplace=True)

# # see file data
# df.info()
# print(df.shape)

# # check if null values are found
# print(df.isnull().sum())

# # check to see duplicates
# print(df.duplicated().sum())

# # check to see if there are sales lower or equal to zero
# print(df[df["Sales"] <= 0])

# # check to see if there are Discount lower or equal to zero
# print(df[df["Discount"]<0])

# unified the date format

# 1. Safely convert the messy strings into correct datetime 
df['Order Date'] = pd.to_datetime(df['Order Date'], format='mixed')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='mixed')

# 2. Now you can safely format them to YYYY-MM-DD
df['Order Date'] = df['Order Date'].dt.strftime('%Y-%m-%d')
df['Ship Date'] = df['Ship Date'].dt.strftime('%Y-%m-%d')

print(df['Order Date'])
print(df['Ship Date'])




# to save file after cleaning
df.to_csv("Superstore_cleaned2.csv", index=False)

# # to display the data
# print(df.head())

# # to display the columns
# print(df.columns)

# to display the data types
# print(df.dtypes)

# to display the summary of the data