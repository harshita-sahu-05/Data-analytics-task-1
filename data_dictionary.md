# Data Dictionary - ApexPlanet Sales Dataset

Source: `ApexPlanet_DataAnalytics_Dataset.xlsx` (sheet `Sales_Dataset`), 1,000 rows, 12 columns.
Grain: one row = one order (one product per order). Period: 2025-01-01 to 2026-01-01.

## Original columns

| # | Column | Type | Meaning | Business relevance |
|---|---|---|---|---|
| 1 | Order_ID | Text (ID) | Unique order identifier (ORD100002 ...) | Primary key for orders; used to detect duplicates |
| 2 | Order_Date | Date (text in source) | Date the order was placed | Trends, seasonality, monthly/quarterly revenue |
| 3 | Customer_ID | Text (ID) | Customer identifier (CUST####) | Customer-level analysis: repeat buyers, retention (see limitation below) |
| 4 | Customer_Name | Text | Customer label (Customer_###) | Reporting only |
| 5 | Age | Integer (years) | Customer age (18-65) | Age-based segmentation |
| 6 | Gender | Categorical | Male / Female | Demographic segmentation |
| 7 | City | Categorical | Patna, Kolkata, Mumbai, Hyderabad, Delhi, Bengaluru, Gaya, Pune | Regional sales performance |
| 8 | Product | Categorical | Mobile, Book, Laptop, Chair, Shoes, Rice | Best/worst sellers |
| 9 | Category | Categorical | Electronics, Education, Furniture, Fashion, Grocery | Category mix and revenue share |
| 10 | Quantity | Integer (1-10) | Units bought in the order | Basket size, volume driver |
| 11 | Unit_Price | Decimal (INR) | Price of one unit | Pricing analysis |
| 12 | Total_Sales | Decimal (INR) | Order revenue = Quantity x Unit_Price | Main revenue measure for KPIs |

Product -> Category is one-to-one (Mobile/Laptop = Electronics, Book = Education, Chair = Furniture, Shoes = Fashion, Rice = Grocery).

## Columns added during cleaning

| Column | Type | Logic | Why |
|---|---|---|---|
| Order_ID_Original | Text | Order_ID exactly as in the source | Audit trail |
| Order_ID_Corrected | Boolean | True for the 8 rows whose repeated ID was replaced | Transparency |
| Age_Imputed | Boolean | True where Age was missing and filled with the median | Lets analysts exclude imputed ages |
| Order_Year | Integer | Year of Order_Date | Year grouping |
| Order_Month | Integer | Month number 1-12 | Correct month sorting |
| Month_Name | Text | Month name | Readable charts |
| Quarter | Text | Q1-Q4 | Quarterly trend |
| Weekday | Text | Day of week | Weekday demand pattern |
| Is_Weekend | Boolean | Saturday or Sunday | Weekend vs weekday sales |
| Age_Group | Categorical | 18-24, 25-34, 35-44, 45-54, 55+ | Segment comparison |
| Order_Size | Categorical | Small (1-3), Medium (4-7), Large (8-10) units | Basket-size analysis |
| Is_High_Value_Order | Boolean | Total_Sales above Q3 + 1.5 x IQR | Flags big orders for separate review |

## Known limitations
- A Customer_ID can appear with different names, ages, genders or cities on different orders (52 IDs), so it is not a reliable unique-person key. Customer-level findings (retention, lifetime value) should be treated with caution.
- Unit_Price varies from about 150 to 50,000 for every product (e.g. Rice), so prices do not look like real catalogue prices.
