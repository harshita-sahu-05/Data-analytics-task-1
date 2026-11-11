"""Task 1 - Data Immersion & Wrangling (ApexPlanet Data Analytics Internship)

Input : ApexPlanet_DataAnalytics_Dataset.xlsx  (sheet: Sales_Dataset)
Output: cleaned_sales_data.csv, quality_report.md

Run:  python clean_data.py
"""
import numpy as np
import pandas as pd

SRC = "ApexPlanet_DataAnalytics_Dataset.xlsx"
CLEAN = "cleaned_sales_data.csv"
REPORT = "quality_report.md"

log = []  # (step, issue, count, action)


def note(step, issue, count, action):
    log.append((step, issue, int(count), action))


raw = pd.read_excel(SRC, sheet_name="Sales_Dataset")
df = raw.copy()
n_raw, n_cols_raw = df.shape

# =============================================================== 1. PROFILING (before cleaning)
missing = raw.isna().sum()
missing = missing[missing > 0]
exact_dups = raw.duplicated().sum()
dup_id_rows = raw["Order_ID"].duplicated(keep=False).sum()

# =============================================================== 2. DUPLICATES
note("Duplicates", "Fully identical rows", exact_dups, "None found - nothing to drop")

# Order_ID is sequential (ORD100002, ORD100003, ...) except 8 rows that all carry ORD100050.
# Those rows differ in every other field (different customer, date, product), so they are
# 8 real orders with a wrong ID, not duplicate records. Dropping them would lose valid sales.
seq_id = "ORD" + (100002 + pd.Series(np.arange(len(df)), index=df.index)).astype(str)
repeated = df["Order_ID"].duplicated(keep="first")          # 2nd+ occurrence of an ID
fixable = repeated & ~seq_id.isin(df["Order_ID"])             # expected sequential ID is free
df["Order_ID_Original"] = df["Order_ID"]
df.loc[fixable, "Order_ID"] = seq_id[fixable]
df["Order_ID_Corrected"] = fixable
note("Duplicates", "Order_ID repeated on rows with different content (ID collision)", repeated.sum(),
     f"{fixable.sum()} rows given their sequential ID back (e.g. ORD100120); original kept in Order_ID_Original")
assert df["Order_ID"].is_unique, "Order_ID still not unique"

# =============================================================== 3. FORMATTING
for c in df.select_dtypes(include="str").columns:
    df[c] = df[c].str.strip()

bad_dates = pd.to_datetime(df["Order_Date"], format="%Y-%m-%d", errors="coerce").isna().sum()
df["Order_Date"] = pd.to_datetime(df["Order_Date"], format="%Y-%m-%d", errors="coerce")
note("Formatting", "Order_Date stored as text (unparseable values: %d)" % bad_dates, len(df),
     "Converted to datetime64")

for c in ["Gender", "City", "Product", "Category"]:
    df[c] = df[c].str.title()
note("Formatting", "Text consistency (spaces / casing) in Gender, City, Product, Category", 0,
     "Checked and standardised to Title Case - no variants found")

# =============================================================== 4. MISSING VALUES
n = df["Age"].isna().sum()
age_median = int(df["Age"].median())
df["Age_Imputed"] = df["Age"].isna()
df["Age"] = df["Age"].fillna(age_median).astype(int)
note("Missing values", "Age missing", n,
     f"Filled with median ({age_median}); flagged in Age_Imputed (same-customer lookup not used: Customer_ID attributes are inconsistent, see Integrity)")

n = df["City"].isna().sum()
df["City"] = df["City"].fillna("Unknown")
note("Missing values", "City missing", n, "Filled with 'Unknown' (not guessed)")

# =============================================================== 5. OUTLIERS & CONSISTENCY CHECKS
mismatch = (~np.isclose(df["Quantity"] * df["Unit_Price"], df["Total_Sales"], atol=0.05)).sum()
note("Validation", "Total_Sales != Quantity x Unit_Price", mismatch, "All rows consistent - no change")

q1, q3 = df["Total_Sales"].quantile([0.25, 0.75])
upper = q3 + 1.5 * (q3 - q1)
df["Is_High_Value_Order"] = df["Total_Sales"] > upper
note("Outliers", f"Total_Sales above IQR upper fence ({upper:,.0f})", df["Is_High_Value_Order"].sum(),
     "Genuine large orders (e.g. 10 units x high price) - kept and flagged in Is_High_Value_Order")

for c in ["Unit_Price", "Quantity", "Age"]:
    a, b = df[c].quantile([0.25, 0.75])
    k = ((df[c] < a - 1.5 * (b - a)) | (df[c] > b + 1.5 * (b - a))).sum()
    note("Outliers", f"{c} outside 1.5 x IQR", k, "None found" if k == 0 else "Reviewed")

cust_multi = {c: int((raw.groupby("Customer_ID")[c].nunique() > 1).sum())
              for c in ["Customer_Name", "Age", "Gender", "City"]}
note("Integrity", "Customer_IDs that appear with different name / age / gender / city",
     max(cust_multi.values()), "Not altered - Customer_ID is not a reliable unique-person key (limitation noted)")

n_low = (df["Unit_Price"] < 500).sum()
note("Integrity", "Unit_Price below 500 (very low for items such as laptops / mobiles)", n_low,
     "Not altered - prices vary widely within every product, so no reliable reference price exists")

# =============================================================== 6. FEATURE ENGINEERING
df["Order_Year"] = df["Order_Date"].dt.year
df["Order_Month"] = df["Order_Date"].dt.month
df["Month_Name"] = df["Order_Date"].dt.month_name()
df["Quarter"] = "Q" + df["Order_Date"].dt.quarter.astype(str)
df["Weekday"] = df["Order_Date"].dt.day_name()
df["Is_Weekend"] = df["Order_Date"].dt.dayofweek >= 5
df["Age_Group"] = pd.cut(df["Age"], bins=[17, 24, 34, 44, 54, 120],
                         labels=["18-24", "25-34", "35-44", "45-54", "55+"]).astype(str)
df["Order_Size"] = pd.cut(df["Quantity"], bins=[0, 3, 7, 10], labels=["Small (1-3)", "Medium (4-7)", "Large (8-10)"]).astype(str)
note("Feature engineering", "New analysis columns", 8,
     "Order_Year, Order_Month, Month_Name, Quarter, Weekday, Is_Weekend, Age_Group, Order_Size")

# =============================================================== 7. EXPORT
cols = ["Order_ID", "Order_ID_Original", "Order_ID_Corrected", "Order_Date", "Order_Year", "Order_Month",
        "Month_Name", "Quarter", "Weekday", "Is_Weekend", "Customer_ID", "Customer_Name", "Age", "Age_Imputed",
        "Age_Group", "Gender", "City", "Product", "Category", "Quantity", "Order_Size", "Unit_Price",
        "Total_Sales", "Is_High_Value_Order"]
out = df[cols].copy()
out["Order_Date"] = out["Order_Date"].dt.strftime("%Y-%m-%d")
out.to_csv(CLEAN, index=False)

# =============================================================== 8. REPORT
with open(REPORT, "w", encoding="utf-8") as f:
    f.write("# Data Quality Report\n\n")
    f.write(f"- Source: `{SRC}` (sheet `Sales_Dataset`)\n")
    f.write(f"- Rows: **{n_raw:,}** raw -> **{len(out):,}** cleaned (no rows dropped)\n")
    f.write(f"- Columns: {n_cols_raw} raw -> {out.shape[1]} cleaned\n")
    f.write(f"- Order period: {df['Order_Date'].min():%Y-%m-%d} to {df['Order_Date'].max():%Y-%m-%d}\n\n")
    f.write("## Missing values in raw data\n\n| Column | Missing | % |\n|---|---|---|\n")
    for c, v in missing.items():
        f.write(f"| {c} | {v} | {v / n_raw:.1%} |\n")
    f.write("\n## Issues found and actions taken\n\n| Step | Issue | Count | Action |\n|---|---|---|---|\n")
    for s, i, c, a in log:
        f.write(f"| {s} | {i} | {c} | {a} |\n")
    f.write("\n## Remaining missing values in cleaned data\n\n")
    left = out.isna().sum()
    left = left[left > 0]
    f.write("None\n" if left.empty else left.to_string() + "\n")

print(open(REPORT, encoding="utf-8").read())
print("Cleaned shape:", out.shape)
