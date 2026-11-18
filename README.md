# Superstore Sales Analysis & ML Project

Analysis and machine learning project on the Superstore dataset (US retail orders, 2014–2017).

## Setup

1. Install the same Python version as the team (check with `python --version`).
2. Clone the repo and enter the folder.
3. Create a virtual environment: `python -m venv venv`
4. Activate it:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
5. Install the libraries: `pip install -r requirements.txt`

## Data files

| File | Description |
|---|---|
| `Superstore.csv` | Raw data (latin1 encoding, dates as `mm-dd-yy` text) |
| `Superstore_cleaned_last3.csv` | Cleaned data with date parts |
| `Superstore_features.csv` | Cleaned data + engineered features |
| `Superstore_features_log.csv` | Same + `Log Sales` |
| `Superstore_step2.csv` | City dropped, `Discount Band` added (latest file) |

All cleaned files are UTF-8 and use `YYYY-MM-DD` dates.
Do not open and save the CSV files in Excel: Excel changes the date format.

## Data cleaning

- Loaded the raw file with `latin1` encoding (it is not UTF-8).
- Dropped `Row ID` (row counter), `Postal Code` (lost leading zeros), and `Country` (one value only).
- Removed garbled characters from `Customer Name` (89 rows) and `Product Name` (278 rows).
  The original special characters were already lost in the raw file, so they were removed, not restored.
- Stripped extra spaces and collapsed double spaces in text columns.
- Converted `Order Date` and `Ship Date` to real dates with a fixed format.
- Checked that no ship date comes before its order date (0 cases).
- Removed 1 exact duplicate row (order US-2014-150119). Final size: 9,993 rows.
- Kept 8 pairs of rows with the same Order ID + Product ID. They look like split order lines
  (different quantities, same unit price), not errors.
- Kept outliers. Very large sales and large losses are real business events.
- No missing values in the data.

## Data notes

### Product IDs
In the raw data, 32 Product IDs are used for more than one product name,
and 16 product names have more than one Product ID.
The original Product IDs were not changed and no rows were removed.
A new column, `Product Key` (Product ID + Product Name),
is used to identify each product in the analysis (1,894 unique products vs 1,862 Product IDs).

### Date columns fix
The `Year` column was first created in Excel and was shifted by 3 rows
(about 65% of rows had the wrong year). It was recalculated from `Order Date`,
and `Month`, `Week Day` and `Quarter` were checked against `Order Date` (0 mismatches).
Saving the CSV in Excel had also changed the dates to `dd-mm-yy`;
they were converted back to `YYYY-MM-DD`.

## Feature engineering

| Column | Description |
|---|---|
| `Month`, `Year`, `Week Day`, `Quarter` | From `Order Date` (`Week Day`: 0 = Monday) |
| `Ship Days` | Ship Date − Order Date (0 to 7 days) |
| `Unit Price` | Sales ÷ Quantity (price per unit after discount) |
| `Is Loss` | 1 if Profit < 0, else 0 (18.7% of rows) |
| `Product Key` | Product ID + Product Name |
| `Log Sales` | log(1 + Sales), reduces skew from 12.97 to 0.28 |

| `Discount Band` | No Discount (0), Low (up to 20%), Medium (20–40%), High (over 40%) |

Profit was not log-transformed (it has negative values).

`City` was dropped (531 values, too many for the model). `State` and `Region` are kept for location.

### Discount and losses
| Discount Band | Orders | Loss rate |
|---|---|---|
| No Discount | 4,798 | 0% |
| Low (up to 20%) | 3,803 | 13.8% |
| Medium (20–40%) | 459 | 90.2% |
| High (over 40%) | 933 | 100% |

Every order with a discount above 40% lost money, and no order without a discount did.

## Notes for modeling

- `Is Loss` and `Profit` are targets. Never use one as an input when predicting the other.
- Drop ID and name columns before training (`Order ID`, `Customer ID`, `Customer Name`,
  `Product ID`, `Product Name`, `Product Key`), plus the raw date columns.
- Classes are imbalanced (18.7% loss rows): use class weights and look at recall/F1, not only accuracy.
- Use a stratified split for classification and a time-based split for forecasting.

## Model

Notebook: `Superstore_Loss_Model.ipynb` (runs in Google Colab).

- Target: `Is Loss`
- Inputs: Ship Mode, Segment, Region, Category, Sub-Category, Quantity, Discount, Discount Band,
  Month, Year, Week Day, Quarter, Ship Days, Unit Price, Log Sales (one-hot encoded, 44 columns)
- Split: 80% train / 20% test, stratified
- Model: Random Forest, 300 trees, `class_weight="balanced"`

| Metric (test data, loss class) | Value |
|---|---|
| Recall | 0.90 |
| Precision | 0.81 |
| F1 | 0.85 |
| ROC-AUC | 0.99 |

## Progress

- [x] Data cleaning
- [x] Date features, Ship Days, Unit Price, Is Loss, Product Key
- [x] Log transform of Sales
- [x] Reduce City, use State or Region for location
- [x] Discount bands
- [x] Encode categorical columns
- [x] Drop ID/name/date columns, remove leaking columns
- [x] Train/test split
- [x] Scaling (not needed for Random Forest)
- [x] Handle class imbalance
- [x] Choose business question and target ("Why do orders lose money?", `Is Loss`)
- [x] Train first model (Random Forest)
- [ ] Compare with other models (Logistic Regression, XGBoost)
- [ ] Dashboard
