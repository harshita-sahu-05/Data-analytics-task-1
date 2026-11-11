# Task 1 - Data Immersion & Wrangling

**Internship:** ApexPlanet Software Pvt. Ltd. - Data Analytics
**Tools:** Python 3, Pandas, NumPy

## Objective
Understand the provided sales dataset, assess its quality, clean it and produce an analysis-ready file.

## Dataset
`ApexPlanet_DataAnalytics_Dataset.xlsx` - 1,000 sales orders, 12 columns (order, customer, product, quantity, price, total sales), Jan 2025 to Jan 2026.

## Repository contents

| File | Purpose |
|---|---|
| `ApexPlanet_DataAnalytics_Dataset.xlsx` | Original dataset (unchanged) |
| `data_dictionary.md` | Meaning, type and business relevance of every column |
| `clean_data.py` | Profiling, cleaning and feature-engineering script |
| `cleaned_sales_data.csv` | Final analysis-ready dataset (1,000 rows, 24 columns) |
| `quality_report.md` | Auto-generated list of issues found and actions taken |

## Data quality findings

| Check | Result | Action |
|---|---|---|
| Missing values | Age: 20 (2.0%), City: 13 (1.3%) | Age filled with median (41) and flagged; City set to `Unknown` |
| Exact duplicate rows | 0 | - |
| Repeated Order_ID | 8 different orders all carried `ORD100050`; the IDs are otherwise sequential and the 8 expected IDs (ORD100120, ORD100240 ...) were missing | Restored the sequential IDs, kept the original in `Order_ID_Original` |
| Date format | Order_Date stored as text | Converted to a real date |
| Text consistency | No spacing/casing variants | Standardised to Title Case anyway |
| Total_Sales check | Quantity x Unit_Price matches on all rows | - |
| Outliers | No outliers in Unit_Price, Quantity or Age; 19 high-value orders (IQR rule) | Genuine large orders, kept and flagged |
| Customer_ID integrity | 52 IDs appear with different name/age/gender/city | Not changed; limitation documented |
| Low prices | 7 orders with Unit_Price below 500 (e.g. laptop) | Not changed; no reliable reference price |

## New columns (feature engineering)
Order_Year, Order_Month, Month_Name, Quarter, Weekday, Is_Weekend, Age_Group, Order_Size, Is_High_Value_Order, plus audit columns Order_ID_Original, Order_ID_Corrected, Age_Imputed.

## Result
1,000 rows kept (nothing dropped), 24 columns, no missing values, unique Order_ID.

## How to run
```
pip install pandas numpy openpyxl
python clean_data.py
```
This creates `cleaned_sales_data.csv` and `quality_report.md`.

## Key learnings
- Profile before cleaning and document every decision.
- A repeated ID does not always mean a duplicate record: compare the full rows before deleting.
- Flag imputed or corrected values so later analysis can account for them.
- Check data against business logic (Total = Quantity x Price), not just for nulls.
