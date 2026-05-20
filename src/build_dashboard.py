"""
Build Interactive HTML Dashboard
================================
Generates a standalone, interactive HTML dashboard using Plotly
that can be opened in any browser — perfect for portfolio hosting!
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

# Load data
print("Loading dashboard data...")
df = pd.read_csv('./data/customer_shopping_behavior_clean.csv')
rev_gender = pd.read_csv('./data/revenue_by_gender.csv')
rev_age = pd.read_csv('./data/revenue_by_age.csv')
segments = pd.read_csv('./data/customer_segments.csv')
top_products = pd.read_csv('./data/top_products.csv')
sub_stats = pd.read_csv('./data/subscription_stats.csv')

# KPIs
total_customers = df['customer_id'].nunique()
total_revenue = df['purchase_amount_usd'].sum()
avg_purchase = df['purchase_amount_usd'].mean()
avg_rating = df['review_rating'].mean()
sub_rate = (df['subscription_status'] == 'Yes').mean() * 100
discount_rate = (df['discount_applied'] == 'Yes').mean() * 100

# ============ CHART 1: Revenue by Gender (Donut) ============
fig_gender = go.Figure(data=[go.Pie(
    labels=rev_gender['gender'],
    values=rev_gender['revenue'],
    hole=0.55,
    marker_colors=['#636EFA', '#EF553B'],
    textinfo='label+percent',
    textposition='outside'
)])
fig_gender.update_layout(
    title_text="Revenue by Gender",
    showlegend=False,
    margin=dict(t=40, b=20, l=20, r=20),
    height=350
)

# ============ CHART 2: Revenue by Age Group (Bar) ============
fig_age = px.bar(
    rev_age, x='age_group', y='total_revenue',
    color='age_group', text='total_revenue',
    color_discrete_sequence=px.colors.sequential.Blues_r
)
fig_age.update_layout(
    title_text="Revenue by Age Group",
    xaxis_title="Age Group",
    yaxis_title="Revenue ($)",
    showlegend=False,
    margin=dict(t=40, b=20, l=20, r=20),
    height=350
)
fig_age.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')

# ============ CHART 3: Customer Segments (Donut) ============
fig_seg = go.Figure(data=[go.Pie(
    labels=segments['customer_segment'],
    values=segments['customer_count'],
    hole=0.55,
    marker_colors=['#00CC96', '#AB63FA', '#FFA15A'],
    textinfo='label+percent',
    textposition='outside'
)])
fig_seg.update_layout(
    title_text="Customer Segments",
    showlegend=False,
    margin=dict(t=40, b=20, l=20, r=20),
    height=350
)

# ============ CHART 4: Subscription Analysis (Grouped Bar) ============
fig_sub = make_subplots(rows=1, cols=2, subplot_titles=('Avg Spend ($)', 'Total Revenue ($)'))
fig_sub.add_trace(
    go.Bar(x=sub_stats['subscription_status'], y=sub_stats['avg_spend'],
           marker_color=['#EF553B', '#636EFA'], name='Avg Spend'),
    row=1, col=1
)
fig_sub.add_trace(
    go.Bar(x=sub_stats['subscription_status'], y=sub_stats['total_revenue'],
           marker_color=['#EF553B', '#636EFA'], name='Total Revenue'),
    row=1, col=2
)
fig_sub.update_layout(
    title_text="Subscription Status Analysis",
    showlegend=False,
    margin=dict(t=50, b=20, l=20, r=20),
    height=350
)

# ============ CHART 5: Top Rated Products (Horizontal Bar) ============
fig_products = px.bar(
    top_products.sort_values('avg_rating'),
    x='avg_rating', y='item_purchased', orientation='h',
    color='avg_rating', color_continuous_scale='Greens',
    text='avg_rating'
)
fig_products.update_layout(
    title_text="Top 5 Products by Avg Review Rating",
    xaxis_title="Average Rating",
    yaxis_title="Product",
    showlegend=False,
    margin=dict(t=40, b=20, l=20, r=20),
    height=350
)
fig_products.update_traces(texttemplate='%{text:.2f}', textposition='outside')

# ============ CHART 6: Purchase Amount by Shipping Type ============
ship_data = df[df['shipping_type'].isin(['Standard', 'Express'])].groupby('shipping_type')['purchase_amount_usd'].mean().reset_index()
fig_ship = px.bar(
    ship_data, x='shipping_type', y='purchase_amount_usd',
    color='shipping_type', text='purchase_amount_usd',
    color_discrete_sequence=['#FF6692', '#19D3F3']
)
fig_ship.update_layout(
    title_text="Avg Purchase: Standard vs Express Shipping",
    xaxis_title="Shipping Type",
    yaxis_title="Avg Purchase ($)",
    showlegend=False,
    margin=dict(t=40, b=20, l=20, r=20),
    height=350
)
fig_ship.update_traces(texttemplate='$%{text:.2f}', textposition='outside')

# ============ CHART 7: Category Distribution ============
cat_data = df['category'].value_counts().reset_index()
cat_data.columns = ['category', 'count']
fig_cat = px.pie(cat_data, names='category', values='count',
                 color_discrete_sequence=px.colors.qualitative.Set3)
fig_cat.update_layout(
    title_text="Orders by Category",
    showlegend=True,
    margin=dict(t=40, b=20, l=20, r=20),
    height=350
)

# ============ CHART 8: Previous Purchases Distribution ============
fig_prev = px.histogram(df, x='previous_purchases', nbins=20,
                        color_discrete_sequence=['#B6E880'])
fig_prev.update_layout(
    title_text="Distribution of Previous Purchases",
    xaxis_title="Previous Purchases",
    yaxis_title="Customer Count",
    margin=dict(t=40, b=20, l=20, r=20),
    height=350
)

# Convert all figures to JSON dicts for embedding
def fig_to_json(fig):
    d = json.loads(fig.to_json())
    return json.dumps(d['data']), json.dumps(d['layout'])

charts = {}
for name, fig in [('gender', fig_gender), ('age', fig_age), ('segment', fig_seg),
                  ('subscription', fig_sub), ('products', fig_products),
                  ('shipping', fig_ship), ('category', fig_cat), ('prev', fig_prev)]:
    charts[name + '_data'], charts[name + '_layout'] = fig_to_json(fig)

# ============ BUILD HTML DASHBOARD ============
html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Customer Shopping Behavior - Analytics Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        :root {{
            --primary: #1f2937;
            --accent: #3b82f6;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --light: #f3f4f6;
            --card-bg: #ffffff;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
        body {{ background: linear-gradient(135deg, #f0f4f8 0%, #d9e2ec 100%); min-height: 100vh; color: var(--primary); }}
        .header {{
            background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
            color: white;
            padding: 2rem 1rem;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header h1 {{ font-size: 2.2rem; margin-bottom: 0.5rem; }}
        .header p {{ opacity: 0.9; font-size: 1.05rem; }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 2rem 1rem; }}
        
        /* KPI Cards */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.2rem;
            margin-bottom: 2rem;
        }}
        .kpi-card {{
            background: var(--card-bg);
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
            transition: transform 0.2s;
            border-left: 5px solid var(--accent);
        }}
        .kpi-card:hover {{ transform: translateY(-4px); }}
        .kpi-card:nth-child(2) {{ border-left-color: var(--success); }}
        .kpi-card:nth-child(3) {{ border-left-color: var(--warning); }}
        .kpi-card:nth-child(4) {{ border-left-color: var(--danger); }}
        .kpi-card:nth-child(5) {{ border-left-color: #8b5cf6; }}
        .kpi-card:nth-child(6) {{ border-left-color: #06b6d4; }}
        .kpi-label {{ font-size: 0.85rem; color: #6b7280; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.3rem; }}
        .kpi-value {{ font-size: 1.8rem; font-weight: 700; color: var(--primary); }}
        .kpi-sub {{ font-size: 0.8rem; color: #9ca3af; margin-top: 0.2rem; }}

        /* Charts Grid */
        .chart-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
            gap: 1.5rem;
        }}
        .chart-card {{
            background: var(--card-bg);
            border-radius: 16px;
            padding: 1rem;
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
        }}
        .chart-card.full-width {{ grid-column: 1 / -1; }}
        .chart-title {{
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            padding-left: 0.5rem;
            border-left: 4px solid var(--accent);
        }}

        /* Insights Section */
        .insights {{
            background: var(--card-bg);
            border-radius: 16px;
            padding: 2rem;
            margin-top: 2rem;
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
        }}
        .insights h2 {{ color: #1e3a8a; margin-bottom: 1rem; }}
        .insights ul {{ list-style: none; }}
        .insights li {{
            padding: 0.6rem 0;
            padding-left: 1.5rem;
            position: relative;
            border-bottom: 1px solid #f3f4f6;
        }}
        .insights li::before {{
            content: "▹";
            position: absolute;
            left: 0;
            color: var(--accent);
            font-weight: bold;
        }}

        .footer {{
            text-align: center;
            padding: 2rem;
            color: #6b7280;
            font-size: 0.9rem;
        }}

        @media (max-width: 768px) {{
            .chart-grid {{ grid-template-columns: 1fr; }}
            .header h1 {{ font-size: 1.6rem; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🛍️ Customer Shopping Behavior Analytics</h1>
        <p>End-to-End Data Analysis Pipeline | Python • SQL • Interactive Visualization</p>
    </div>

    <div class="container">
        <!-- KPI Cards -->
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-label">Total Customers</div>
                <div class="kpi-value">{total_customers:,}</div>
                <div class="kpi-sub">Unique customer records</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Total Revenue</div>
                <div class="kpi-value">${total_revenue:,.0f}</div>
                <div class="kpi-sub">Lifetime revenue generated</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Avg Purchase</div>
                <div class="kpi-value">${avg_purchase:.2f}</div>
                <div class="kpi-sub">Per transaction average</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Avg Rating</div>
                <div class="kpi-value">{avg_rating:.2f}/5.0</div>
                <div class="kpi-sub">Product review rating</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Subscription Rate</div>
                <div class="kpi-value">{sub_rate:.1f}%</div>
                <div class="kpi-sub">Customers subscribed</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Discount Usage</div>
                <div class="kpi-value">{discount_rate:.1f}%</div>
                <div class="kpi-sub">Transactions with discount</div>
            </div>
        </div>

        <!-- Charts -->
        <div class="chart-grid">
            <div class="chart-card">
                <div class="chart-title">Revenue by Gender</div>
                <div id="chart-gender"></div>
            </div>
            <div class="chart-card">
                <div class="chart-title">Revenue by Age Group</div>
                <div id="chart-age"></div>
            </div>
            <div class="chart-card">
                <div class="chart-title">Customer Segments</div>
                <div id="chart-segment"></div>
            </div>
            <div class="chart-card">
                <div class="chart-title">Subscription Analysis</div>
                <div id="chart-subscription"></div>
            </div>
            <div class="chart-card">
                <div class="chart-title">Top 5 Rated Products</div>
                <div id="chart-products"></div>
            </div>
            <div class="chart-card">
                <div class="chart-title">Shipping Type Comparison</div>
                <div id="chart-shipping"></div>
            </div>
            <div class="chart-card">
                <div class="chart-title">Orders by Category</div>
                <div id="chart-category"></div>
            </div>
            <div class="chart-card">
                <div class="chart-title">Previous Purchases Distribution</div>
                <div id="chart-prev"></div>
            </div>
        </div>

        <!-- Insights -->
        <div class="insights">
            <h2>🔍 Key Business Insights & Recommendations</h2>
            <ul>
                <li><strong>Gender Revenue Gap:</strong> Male customers generate ~68% of total revenue ($157,890 vs $75,191). Consider targeted marketing campaigns for female segments to balance revenue streams.</li>
                <li><strong>Age Group Opportunity:</strong> The 55+ age group contributes the highest revenue ($69,590), followed by 25-34. Loyalty programs should prioritize these high-value cohorts.</li>
                <li><strong>Customer Loyalty:</strong> 80% of customers are classified as Loyal (3,116), with only 83 New customers. Focus on acquisition strategies to grow the funnel.</li>
                <li><strong>Subscription Impact:</strong> Non-subscribers outnumber subscribers 2.7:1 and contribute 73% of revenue. Incentivizing subscriptions could improve retention.</li>
                <li><strong>Discount Strategy:</strong> 43% of transactions use discounts, with Hats and Sneakers seeing ~50% discount rates. Evaluate margin impact vs. volume uplift.</li>
                <li><strong>Shipping Preferences:</strong> Express shipping customers spend slightly more ($60.48) than Standard ($58.46). Promote Express for higher AOV.</li>
                <li><strong>Product Quality:</strong> Gloves, Sandals, and Boots have the highest review ratings (>3.82). Leverage these as flagship products in campaigns.</li>
                <li><strong>Repeat Buyer Behavior:</strong> Among customers with >5 previous purchases, 72% are not subscribed — a major upsell opportunity for subscription services.</li>
            </ul>
        </div>
    </div>

    <div class="footer">
        <p>Built with Python, Pandas, SQLite, and Plotly | Portfolio Project</p>
    </div>

    <script>
        Plotly.newPlot('chart-gender', {charts['gender_data']}, {charts['gender_layout']}, {{responsive: true}});
        Plotly.newPlot('chart-age', {charts['age_data']}, {charts['age_layout']}, {{responsive: true}});
        Plotly.newPlot('chart-segment', {charts['segment_data']}, {charts['segment_layout']}, {{responsive: true}});
        Plotly.newPlot('chart-subscription', {charts['subscription_data']}, {charts['subscription_layout']}, {{responsive: true}});
        Plotly.newPlot('chart-products', {charts['products_data']}, {charts['products_layout']}, {{responsive: true}});
        Plotly.newPlot('chart-shipping', {charts['shipping_data']}, {charts['shipping_layout']}, {{responsive: true}});
        Plotly.newPlot('chart-category', {charts['category_data']}, {charts['category_layout']}, {{responsive: true}});
        Plotly.newPlot('chart-prev', {charts['prev_data']}, {charts['prev_layout']}, {{responsive: true}});
    </script>
</body>
</html>
'''

# Save dashboard
output_path = './dashboard/index.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"✅ Interactive dashboard generated: {output_path}")
print("🚀 Open this file in any web browser to view your dashboard!")
