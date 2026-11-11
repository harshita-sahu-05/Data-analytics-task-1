# LinkedIn Video Script (3-5 min) - Task 1

Screen-record with OBS Studio / Loom / Windows Game Bar. Keep VS Code and the GitHub repo open. Before recording, run `python clean_data.py` once. Speak in your own words (Hinglish or English is fine).

**0:00 - 0:30 Intro**
"Hi, I'm Aakash. This is Task 1 of my ApexPlanet Data Analytics internship: Data Immersion and Wrangling. I'll show how I checked the quality of a sales dataset and prepared it for analysis."
(Show the GitHub repo.)

**0:30 - 1:15 Dataset and data dictionary**
"The dataset has 1,000 orders and 12 columns: order, customer, age, gender, city, product, category, quantity, unit price and total sales, from January 2025 to January 2026. I wrote a data dictionary with each column's type, meaning and business use."
(Open `data_dictionary.md`.)

**1:15 - 2:30 Data quality issues**
(Open `quality_report.md`.)
"Profiling found these things:
1. Missing values: 20 ages and 13 cities.
2. Order_ID problem: eight different orders all had the ID ORD100050. I compared the full rows, they were different orders, not duplicates. The IDs are otherwise sequential, so the eight missing IDs like ORD100120 were obvious.
3. Dates were stored as text.
4. No outliers in price, quantity or age. 19 very large orders, but they are genuine, so I only flagged them.
5. Customer IDs sometimes have different names or ages on different orders, so I noted that as a limitation."

**2:30 - 4:00 Cleaning process**
(Open `clean_data.py`, scroll, then run it in the terminal.)
"In the script I restored the sequential Order IDs and kept the original ID in a separate column. I converted dates to a real date type. Missing age was filled with the median and flagged, and missing city was set to Unknown instead of guessing. I checked that Total Sales equals Quantity times Unit Price on every row. Then I created new columns: year, month, quarter, weekday, age group, order size and a high-value flag."

**4:00 - 4:45 Result and close**
(Show `cleaned_sales_data.csv`.)
"The final file has 1,000 rows, 24 columns, no missing values and unique Order IDs, ready for EDA in Task 2. My key learning: do not delete a repeated ID without comparing the rows, and always flag what you change. Thank you!"

**Tip:** you should be able to explain the Order_ID fix and why age was filled with the median. Practise once before recording.
