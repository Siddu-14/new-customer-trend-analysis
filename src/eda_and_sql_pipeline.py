"""
Customer Shopping Behavior - End-to-End Data Analytics Pipeline
===============================================================
This script covers:
1. Data Import & Exploration
2. Data Cleaning & Feature Engineering
3. SQLite Database Creation
4. Business SQL Queries Execution
5. Export Clean Data for Dashboard
"""

import pandas as pd
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

print("=" * 60)
print("CUSTOMER SHOPPING BEHAVIOR - DATA ANALYTICS PIPELINE")
print("=" * 60)

# =============================================================================
# 1. DATA IMPORT
# =============================================================================
print("\n[1/6] Loading Dataset...")
df = pd.read_csv('./data/customer_shopping_behavior.csv')
print(f"✅ Dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns")

# =============================================================================
# 2. EXPLORATORY DATA ANALYSIS (EDA)
# =============================================================================
print("\n[2/6] Running Exploratory Data Analysis...")

# Basic info
print("\n--- Data Types & Non-Null Counts ---")
print(df.info())

print("\n--- Descriptive Statistics ---")
print(df.describe())

print("\n--- Missing Values ---")
print(df.isnull().sum())

print("\n--- Duplicate Rows ---")
print(f"Duplicate rows: {df.duplicated().sum()}")

# =============================================================================
# 3. DATA CLEANING & FEATURE ENGINEERING
# =============================================================================
print("\n[3/6] Cleaning Data & Engineering Features...")

# Create clean copy
df_clean = df.copy()

# Standardize column names (snake_case for SQL compatibility)
df_clean.columns = df_clean.columns.str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace('-', '_')
print(f"Standardized columns: {list(df_clean.columns)}")

# Handle missing review ratings
missing_reviews = df_clean['review_rating'].isnull().sum()
if missing_reviews > 0:
    median_rating = df_clean['review_rating'].median()
    df_clean['review_rating'].fillna(median_rating, inplace=True)
    print(f"✅ Filled {missing_reviews} missing review ratings with median ({median_rating})")

# Create age groups
def categorize_age(age):
    if age < 25:
        return '18-24'
    elif age < 35:
        return '25-34'
    elif age < 45:
        return '35-44'
    elif age < 55:
        return '45-54'
    else:
        return '55+'

df_clean['age_group'] = df_clean['age'].apply(categorize_age)
print("✅ Created 'age_group' feature")

# Create customer segment based on previous purchases
def segment_customer(prev_purchases):
    if prev_purchases == 1:
        return 'New'
    elif prev_purchases <= 10:
        return 'Returning'
    else:
        return 'Loyal'

df_clean['customer_segment'] = df_clean['previous_purchases'].apply(segment_customer)
print("✅ Created 'customer_segment' feature")

# Ensure purchase_amount is numeric
df_clean['purchase_amount_usd'] = pd.to_numeric(df_clean['purchase_amount_usd'], errors='coerce')

# Save cleaned data
df_clean.to_csv('./data/customer_shopping_behavior_clean.csv', index=False)
print("✅ Clean dataset saved to: data/customer_shopping_behavior_clean.csv")

# =============================================================================
# 4. SQLITE DATABASE CREATION
# =============================================================================
print("\n[4/6] Creating SQLite Database...")

conn = sqlite3.connect('./data/customer_behavior.db')
cursor = conn.cursor()

# Drop table if exists and create new
cursor.execute("DROP TABLE IF EXISTS customer")
conn.commit()

# Load data to SQL
df_clean.to_sql('customer', conn, index=False, if_exists='replace')
print("✅ Data loaded into SQLite table 'customer'")

# Verify
result = cursor.execute("SELECT COUNT(*) FROM customer").fetchone()
print(f"✅ SQLite table contains {result[0]} records")

# =============================================================================
# 5. BUSINESS SQL QUERIES
# =============================================================================
print("\n[5/6] Executing Business SQL Queries...")

queries = {}

# Q1: Total revenue by gender
queries['q1_gender_revenue'] = """
SELECT gender, SUM(purchase_amount_usd) AS revenue
FROM customer
GROUP BY gender
ORDER BY revenue DESC;
"""

# Q2: Customers with discount but spent above average
queries['q2_discount_high_spenders'] = """
SELECT customer_id, purchase_amount_usd
FROM customer
WHERE discount_applied = 'Yes' 
  AND purchase_amount_usd >= (SELECT AVG(purchase_amount_usd) FROM customer);
"""

# Q3: Top 5 products by average review rating
queries['q3_top_rated_products'] = """
SELECT item_purchased, ROUND(AVG(review_rating), 2) AS avg_rating
FROM customer
GROUP BY item_purchased
ORDER BY avg_rating DESC
LIMIT 5;
"""

# Q4: Average purchase by shipping type
queries['q4_shipping_comparison'] = """
SELECT shipping_type, ROUND(AVG(purchase_amount_usd), 2) AS avg_purchase
FROM customer
WHERE shipping_type IN ('Standard', 'Express')
GROUP BY shipping_type;
"""

# Q5: Subscribed vs Non-subscribed customers
queries['q5_subscription_analysis'] = """
SELECT subscription_status,
       COUNT(customer_id) AS total_customers,
       ROUND(AVG(purchase_amount_usd), 2) AS avg_spend,
       ROUND(SUM(purchase_amount_usd), 2) AS total_revenue
FROM customer
GROUP BY subscription_status
ORDER BY total_revenue DESC;
"""

# Q6: Top 5 products with highest discount rate
queries['q6_discount_rate'] = """
SELECT item_purchased,
       ROUND(100.0 * SUM(CASE WHEN discount_applied = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS discount_rate
FROM customer
GROUP BY item_purchased
ORDER BY discount_rate DESC
LIMIT 5;
"""

# Q7: Customer segment counts
queries['q7_customer_segments'] = """
SELECT customer_segment, COUNT(*) AS customer_count
FROM customer
GROUP BY customer_segment
ORDER BY customer_count DESC;
"""

# Q8: Top 3 products per category
queries['q8_top_products_per_category'] = """
WITH item_counts AS (
    SELECT category, item_purchased,
           COUNT(customer_id) AS total_orders,
           ROW_NUMBER() OVER (PARTITION BY category ORDER BY COUNT(customer_id) DESC) AS item_rank
    FROM customer
    GROUP BY category, item_purchased
)
SELECT item_rank, category, item_purchased, total_orders
FROM item_counts
WHERE item_rank <= 3;
"""

# Q9: Repeat buyers subscription behavior
queries['q9_repeat_buyers_subscription'] = """
SELECT subscription_status, COUNT(customer_id) AS repeat_buyers
FROM customer
WHERE previous_purchases > 5
GROUP BY subscription_status;
"""

# Q10: Revenue by age group
queries['q10_revenue_by_age_group'] = """
SELECT age_group, SUM(purchase_amount_usd) AS total_revenue
FROM customer
GROUP BY age_group
ORDER BY total_revenue DESC;
"""

# Execute and display all queries
results = {}
for name, query in queries.items():
    results[name] = pd.read_sql_query(query, conn)
    print(f"\n--- {name.upper().replace('_', ' ')} ---")
    print(results[name].to_string(index=False))

# =============================================================================
# 6. EXPORT SUMMARY STATS FOR DASHBOARD
# =============================================================================
print("\n[6/6] Exporting Summary Data for Dashboard...")

# Key metrics for dashboard
kpis = {
    'total_customers': df_clean['customer_id'].nunique(),
    'total_revenue': df_clean['purchase_amount_usd'].sum(),
    'avg_purchase': df_clean['purchase_amount_usd'].mean(),
    'avg_review': df_clean['review_rating'].mean(),
    'subscription_rate': (df_clean['subscription_status'] == 'Yes').mean() * 100,
    'discount_usage_rate': (df_clean['discount_applied'] == 'Yes').mean() * 100
}

print(f"\n📊 KEY PERFORMANCE INDICATORS:")
print(f"   Total Customers: {kpis['total_customers']:,}")
print(f"   Total Revenue: ${kpis['total_revenue']:,.2f}")
print(f"   Average Purchase: ${kpis['avg_purchase']:.2f}")
print(f"   Average Review Rating: {kpis['avg_review']:.2f}/5")
print(f"   Subscription Rate: {kpis['subscription_rate']:.1f}%")
print(f"   Discount Usage Rate: {kpis['discount_usage_rate']:.1f}%")

# Save aggregated data for dashboard
revenue_by_gender = results['q1_gender_revenue']
revenue_by_age = results['q10_revenue_by_age_group']
customer_segments = results['q7_customer_segments']
top_products = results['q3_top_rated_products']
subscription_stats = results['q5_subscription_analysis']

revenue_by_gender.to_csv('./data/revenue_by_gender.csv', index=False)
revenue_by_age.to_csv('./data/revenue_by_age.csv', index=False)
customer_segments.to_csv('./data/customer_segments.csv', index=False)
top_products.to_csv('./data/top_products.csv', index=False)
subscription_stats.to_csv('./data/subscription_stats.csv', index=False)

print("\n✅ Dashboard data exports complete!")
print("✅ SQLite database ready at: data/customer_behavior.db")

# Close connection
conn.close()
print("\n" + "=" * 60)
print("PIPELINE EXECUTED SUCCESSFULLY!")
print("=" * 60)
