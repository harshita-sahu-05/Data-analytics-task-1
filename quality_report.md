# Data Quality Report

- Source: `ApexPlanet_DataAnalytics_Dataset.xlsx` (sheet `Sales_Dataset`)
- Rows: **1,000** raw -> **1,000** cleaned (no rows dropped)
- Columns: 12 raw -> 24 cleaned
- Order period: 2025-01-01 to 2026-01-01

## Missing values in raw data

| Column | Missing | % |
|---|---|---|
| Age | 20 | 2.0% |
| City | 13 | 1.3% |

## Issues found and actions taken

| Step | Issue | Count | Action |
|---|---|---|---|
| Duplicates | Fully identical rows | 0 | None found - nothing to drop |
| Duplicates | Order_ID repeated on rows with different content (ID collision) | 8 | 8 rows given their sequential ID back (e.g. ORD100120); original kept in Order_ID_Original |
| Formatting | Order_Date stored as text (unparseable values: 0) | 1000 | Converted to datetime64 |
| Formatting | Text consistency (spaces / casing) in Gender, City, Product, Category | 0 | Checked and standardised to Title Case - no variants found |
| Missing values | Age missing | 20 | Filled with median (41); flagged in Age_Imputed (same-customer lookup not used: Customer_ID attributes are inconsistent, see Integrity) |
| Missing values | City missing | 13 | Filled with 'Unknown' (not guessed) |
| Validation | Total_Sales != Quantity x Unit_Price | 0 | All rows consistent - no change |
| Outliers | Total_Sales above IQR upper fence (438,707) | 19 | Genuine large orders (e.g. 10 units x high price) - kept and flagged in Is_High_Value_Order |
| Outliers | Unit_Price outside 1.5 x IQR | 0 | None found |
| Outliers | Quantity outside 1.5 x IQR | 0 | None found |
| Outliers | Age outside 1.5 x IQR | 0 | None found |
| Integrity | Customer_IDs that appear with different name / age / gender / city | 52 | Not altered - Customer_ID is not a reliable unique-person key (limitation noted) |
| Integrity | Unit_Price below 500 (very low for items such as laptops / mobiles) | 7 | Not altered - prices vary widely within every product, so no reliable reference price exists |
| Feature engineering | New analysis columns | 8 | Order_Year, Order_Month, Month_Name, Quarter, Weekday, Is_Weekend, Age_Group, Order_Size |

## Remaining missing values in cleaned data

None
