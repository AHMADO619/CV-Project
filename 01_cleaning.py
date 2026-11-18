"""
Step 1: Clean the raw Superstore data.

Input:  data/Superstore.csv          (raw file)
Output: data/Superstore_cleaned.csv  (9,993 rows, 18 columns)

Run from anywhere:  python 01_cleaning.py
"""
from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parent / "data"

# 1. Load the raw file (it is not UTF-8, so we use latin1)
df = pd.read_csv(DATA / "Superstore.csv", encoding="latin1")
print("Raw shape:", df.shape)

# 2. Drop columns we don't need
#    Row ID      -> just a row counter
#    Postal Code -> lost its leading zeros, and we use State/Region for location
#    Country     -> only one value ("United States")
df = df.drop(columns=["Row ID", "Postal Code", "Country"])

# 3. Remove garbled characters (e.g. "ï¿½") from names.
#    The original characters are already lost in the raw file, so we remove them.
df["Customer Name"] = df["Customer Name"].str.replace(r"[^\x00-\x7f]+", "", regex=True)
df["Product Name"] = df["Product Name"].str.replace(r"[^\x00-\x7f]+", " ", regex=True)

# 4. Strip extra spaces in all text columns, and collapse double spaces
for c in df.columns:
    if pd.api.types.is_string_dtype(df[c]):      # only text columns
        df[c] = df[c].str.replace(r"\s+", " ", regex=True).str.strip()

# 5. Convert the dates.
#    The raw dates are month-first, e.g. "11-08-16" = 8 Nov 2016.
#    We try a few month-first formats, so the script also works if a row
#    is written as "11/8/2016" instead of "11-08-16".
def parse_dates(col):
    result = pd.Series(pd.NaT, index=col.index)
    for fmt in ["%m-%d-%y", "%m/%d/%Y", "%m/%d/%y", "%m-%d-%Y", "%Y-%m-%d"]:
        parsed = pd.to_datetime(col, format=fmt, errors="coerce")
        result = result.fillna(parsed)
    return result

df["Order Date"] = parse_dates(df["Order Date"])
df["Ship Date"] = parse_dates(df["Ship Date"])

# 6. Checks (all should print 0)
print("Dates that could not be read:", df["Order Date"].isna().sum() + df["Ship Date"].isna().sum())
print("Ship date before order date:", (df["Ship Date"] < df["Order Date"]).sum())
order_id_year = df["Order ID"].str[3:7].astype(int)   # e.g. "CA-2016-152156" -> 2016
print("Order year different from Order ID year:", (order_id_year != df["Order Date"].dt.year).sum(), "(a few are OK)")
print("Missing values:", df.isnull().sum().sum())

# 7. Remove exact duplicate rows (done last, after text cleaning)
print("Duplicates removed:", df.duplicated().sum())          # expected: 1
df = df.drop_duplicates().reset_index(drop=True)

# 8. Save (dates as YYYY-MM-DD)
df.to_csv(DATA / "Superstore_cleaned.csv", index=False, date_format="%Y-%m-%d")
print("Final shape:", df.shape)                              # expected: (9993, 18)
