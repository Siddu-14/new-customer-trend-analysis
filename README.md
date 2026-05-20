
# 🛍️ Customer Shopping Behavior - Data Analytics Portfolio Project

A complete, industry-standard end-to-end data analytics workflow using **Python**, **SQL**, and an **Interactive Plotly Dashboard** (browser-based alternative to Power BI).

---

## 📌 Project Overview

This project demonstrates the ability to translate raw retail customer data into strategic business intelligence through:

- ✅ **Data Preparation & EDA (Python/Pandas)**: Cleaning, transforming, and feature engineering
- ✅ **Data Analysis (SQL/SQLite)**: Business queries for customer segments, loyalty, and purchase drivers
- ✅ **Interactive Visualization (Plotly HTML)**: A standalone, responsive dashboard with KPIs and insights
- ✅ **Business Reporting**: Actionable recommendations based on data-driven insights

---

## 🗂️ Project Structure

```
customer-trends-project/
├── 📁 data/
│   ├── customer_shopping_behavior.csv          # Raw dataset (3,900 records)
│   ├── customer_shopping_behavior_clean.csv    # Cleaned dataset
│   ├── customer_behavior.db                    # SQLite database
│   ├── revenue_by_gender.csv                   # Aggregated exports
│   ├── revenue_by_age.csv
│   ├── customer_segments.csv
│   ├── top_products.csv
│   └── subscription_stats.csv
│
├── 📁 src/
│   ├── eda_and_sql_pipeline.py                 # Main ETL + SQL pipeline
│   └── build_dashboard.py                      # Dashboard generator script
│
├── 📁 sql/
│   └── business_queries.sql                    # All 10 business SQL queries
│
├── 📁 dashboard/
│   └── index.html                              # Interactive Plotly dashboard
│
└── README.md                                   # Project documentation
```

---

## 🚀 How to Run

### 1️⃣ Run the EDA & SQL Pipeline
```bash
cd customer-trends-project
python src/eda_and_sql_pipeline.py
```
This script will:
- Load and explore the raw data
- Clean missing values and engineer features (`age_group`, `customer_segment`)
- Load data into SQLite (`data/customer_behavior.db`)
- Execute all 10 business SQL queries
- Export aggregated CSVs for dashboarding

### 2️⃣ Generate the Interactive Dashboard
```bash
python src/build_dashboard.py
```
This creates `dashboard/index.html` — a fully interactive, mobile-responsive dashboard.

### 3️⃣ View the Dashboard
Simply open `dashboard/index.html` in any modern web browser. No server or internet required after load (though Plotly CDN is used for rendering).

---

## 📊 Key Performance Indicators

| Metric | Value |
|--------|-------|
| **Total Customers** | 3,900 |
| **Total Revenue** | $233,081 |
| **Avg Purchase** | $59.76 |
| **Avg Review Rating** | 3.75 / 5.0 |
| **Subscription Rate** | 27.0% |
| **Discount Usage** | 43.0% |

---

## 🔍 Business Questions Answered (SQL)

1. **Revenue by Gender** — Male customers generate ~68% of revenue
2. **High-Spending Discount Users** — Customers who used discounts but spent above average
3. **Top Rated Products** — Gloves, Sandals, Boots lead in reviews
4. **Shipping Comparison** — Express vs Standard avg purchase amounts
5. **Subscription Analysis** — Subscribers vs Non-subscribers spend & revenue
6. **Discount Rate by Product** — Hats & Sneakers have ~50% discount rates
7. **Customer Segmentation** — New / Returning / Loyal breakdown
8. **Top Products per Category** — Ranked by order volume within each category
9. **Repeat Buyer Subscription** — Are frequent buyers subscribing?
10. **Revenue by Age Group** — 55+ cohort is the highest revenue contributor

---

## 💡 Key Insights & Recommendations

- **Gender Revenue Gap**: Male customers dominate revenue. Targeted campaigns for female segments can balance streams.
- **Age Opportunity**: 55+ age group contributes highest revenue ($69,590). Prioritize loyalty programs here.
- **Customer Acquisition**: Only 83 New customers vs 3,116 Loyal. Focus on top-funnel acquisition.
- **Subscription Upsell**: 72% of repeat buyers (5+ purchases) are NOT subscribed — huge opportunity.
- **Discount Strategy**: 43% transactions use discounts. Evaluate margin impact vs volume uplift on high-discount products.
- **Shipping Upsell**: Express shipping correlates with slightly higher AOV ($60.48 vs $58.46).

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Language** | Python 3.13 |
| **Data Processing** | Pandas, NumPy |
| **Database** | SQLite |
| **Visualization** | Plotly, HTML/CSS |
| **Dashboard** | Standalone responsive HTML (works offline) |

---

## 📎 Notes

- This project is a rebuild/portfolio adaptation of the original [customer-trends-data-analysis](https://github.com/amlanmohanty1/customer-trends-data-analysis-SQL-Python-PowerBI) project.
- The **Power BI** file (`.pbix`) from the original repo can still be used if you have Power BI Desktop — connect it to `data/customer_behavior.db` or the cleaned CSV.
- The **Plotly dashboard** included here serves as a cross-platform, shareable alternative perfect for GitHub Pages or portfolio hosting.

---

## 👨‍💻 Author

Built for Data Analytics Portfolio & Interview Preparation.

> *"Turning raw data into strategic decisions — one query at a time."*

# New-customer-trend-analysis
End-to-end Customer Shopping Behavior Analytics project using Python, SQL, Pandas, SQLite, and interactive Plotly dashboards for business insights and data visualization.
