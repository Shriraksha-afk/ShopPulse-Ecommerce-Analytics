import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="ShopPulse | E-Commerce Analytics",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .metric-card {
        background: #161b22;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #30363d;
    }

    h1, h2, h3 {
        color: #ffffff;
    }

    .subtitle {
        color: #8b949e;
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():

    orders = pd.read_csv(
        "data/processed/fact_orders.csv",
        parse_dates=["order_date"]
    )

    monthly = pd.read_csv(
        "data/processed/monthly_sales.csv"
    )

    category = pd.read_csv(
        "data/processed/category_performance.csv"
    )

    rfm = pd.read_csv(
        "data/processed/rfm_segments.csv"
    )

    products = pd.read_csv(
        "data/processed/product_profitability.csv"
    )

    return orders, monthly, category, rfm, products


orders, monthly, category, rfm, products = load_data()


# -----------------------------
# TITLE
# -----------------------------
st.title("📊 ShopPulse")

st.markdown(
    '<p class="subtitle">E-Commerce Business Intelligence & Customer Analytics Dashboard</p>',
    unsafe_allow_html=True
)

st.divider()


# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.title("🔎 Filters")

categories = sorted(orders["category"].dropna().unique())

selected_categories = st.sidebar.multiselect(
    "Category",
    categories,
    default=categories
)

channels = sorted(orders["sales_channel"].dropna().unique())

selected_channels = st.sidebar.multiselect(
    "Sales Channel",
    channels,
    default=channels
)

payment_methods = sorted(
    orders["payment_method"].dropna().unique()
)

selected_payment = st.sidebar.multiselect(
    "Payment Method",
    payment_methods,
    default=payment_methods
)


# -----------------------------
# APPLY FILTERS
# -----------------------------
filtered_orders = orders[
    orders["category"].isin(selected_categories)
    & orders["sales_channel"].isin(selected_channels)
    & orders["payment_method"].isin(selected_payment)
].copy()


# -----------------------------
# KPI CALCULATIONS
# -----------------------------
total_revenue = filtered_orders["net_sales"].sum()
total_profit = filtered_orders["profit"].sum()
total_orders = filtered_orders["order_id"].nunique()
total_customers = filtered_orders["customer_id"].nunique()

profit_margin = (
    total_profit / total_revenue * 100
    if total_revenue > 0
    else 0
)


# -----------------------------
# KPI CARDS
# -----------------------------
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Revenue",
        f"₹{total_revenue:,.0f}"
    )

with col2:
    st.metric(
        "Profit",
        f"₹{total_profit:,.0f}"
    )

with col3:
    st.metric(
        "Orders",
        f"{total_orders:,}"
    )

with col4:
    st.metric(
        "Customers",
        f"{total_customers:,}"
    )

with col5:
    st.metric(
        "Profit Margin",
        f"{profit_margin:.1f}%"
    )


st.divider()


# -----------------------------
# REVENUE & PROFIT TREND
# -----------------------------
st.subheader("📈 Revenue & Profit Trend")

trend = (
    filtered_orders
    .groupby(filtered_orders["order_date"].dt.to_period("M"))
    .agg(
        Revenue=("net_sales", "sum"),
        Profit=("profit", "sum")
    )
    .reset_index()
)

trend["order_date"] = trend["order_date"].astype(str)

fig_trend = px.line(
    trend,
    x="order_date",
    y=["Revenue", "Profit"],
    markers=True,
    title="Monthly Revenue vs Profit"
)

fig_trend.update_layout(
    xaxis_title="Month",
    yaxis_title="Amount (₹)",
    template="plotly_dark",
    hovermode="x unified"
)

st.plotly_chart(
    fig_trend,
    use_container_width=True
)


# -----------------------------
# CATEGORY ANALYSIS
# -----------------------------
st.subheader("🛍️ Category Performance")

category_filtered = (
    filtered_orders
    .groupby("category")
    .agg(
        Revenue=("net_sales", "sum"),
        Profit=("profit", "sum"),
        Orders=("order_id", "nunique")
    )
    .reset_index()
)

col1, col2 = st.columns(2)

with col1:

    fig_category_revenue = px.bar(
        category_filtered.sort_values(
            "Revenue",
            ascending=True
        ),
        x="Revenue",
        y="category",
        orientation="h",
        title="Revenue by Category",
        text_auto=".2s"
    )

    fig_category_revenue.update_layout(
        template="plotly_dark",
        xaxis_title="Revenue (₹)",
        yaxis_title=""
    )

    st.plotly_chart(
        fig_category_revenue,
        use_container_width=True
    )


with col2:

    fig_category_profit = px.bar(
        category_filtered.sort_values(
            "Profit",
            ascending=True
        ),
        x="Profit",
        y="category",
        orientation="h",
        title="Profit by Category",
        text_auto=".2s"
    )

    fig_category_profit.update_layout(
        template="plotly_dark",
        xaxis_title="Profit (₹)",
        yaxis_title=""
    )

    st.plotly_chart(
        fig_category_profit,
        use_container_width=True
    )


# -----------------------------
# TOP PRODUCTS
# -----------------------------
st.subheader("🏆 Top Products")

top_products = (
    filtered_orders
    .groupby(["product_id", "product_name"])
    .agg(
        Revenue=("net_sales", "sum"),
        Profit=("profit", "sum"),
        Orders=("order_id", "nunique")
    )
    .reset_index()
    .sort_values(
        "Revenue",
        ascending=False
    )
    .head(10)
)

fig_products = px.bar(
    top_products.sort_values(
        "Revenue",
        ascending=True
    ),
    x="Revenue",
    y="product_name",
    orientation="h",
    title="Top 10 Products by Revenue",
    text_auto=".2s"
)

fig_products.update_layout(
    template="plotly_dark",
    xaxis_title="Revenue (₹)",
    yaxis_title=""
)

st.plotly_chart(
    fig_products,
    use_container_width=True
)


# -----------------------------
# RFM CUSTOMER SEGMENTATION
# -----------------------------
st.subheader("👥 Customer Segmentation")

rfm_summary = (
    rfm
    .groupby("segment")
    .agg(
        Customers=("customer_id", "count"),
        Revenue=("monetary", "sum")
    )
    .reset_index()
)

col1, col2 = st.columns(2)

with col1:

    fig_rfm = px.pie(
        rfm_summary,
        names="segment",
        values="Customers",
        hole=0.45,
        title="Customers by RFM Segment"
    )

    fig_rfm.update_layout(
        template="plotly_dark"
    )

    st.plotly_chart(
        fig_rfm,
        use_container_width=True
    )


with col2:

    fig_rfm_revenue = px.bar(
        rfm_summary.sort_values(
            "Revenue",
            ascending=True
        ),
        x="Revenue",
        y="segment",
        orientation="h",
        title="Revenue by Customer Segment",
        text_auto=".2s"
    )

    fig_rfm_revenue.update_layout(
        template="plotly_dark",
        xaxis_title="Revenue (₹)",
        yaxis_title=""
    )

    st.plotly_chart(
        fig_rfm_revenue,
        use_container_width=True
    )


# -----------------------------
# BUSINESS INSIGHTS
# -----------------------------
st.subheader("💡 Business Insights")

best_category = category_filtered.loc[
    category_filtered["Revenue"].idxmax(),
    "category"
]

best_profit_category = category_filtered.loc[
    category_filtered["Profit"].idxmax(),
    "category"
]

best_product = top_products.iloc[0]["product_name"]

st.markdown(f"""
### Key Findings

- **{best_category}** is the highest-revenue category in the selected data.
- **{best_profit_category}** generates the highest total profit.
- **{best_product}** is the highest-revenue product among the top-performing products.
- Customer segmentation helps identify **high-value customers, loyal customers, potential loyalists and at-risk customers**.
- Profitability should be evaluated alongside revenue when prioritizing products and categories.
""")


# -----------------------------
# DATA TABLE
# -----------------------------
st.subheader("📋 Filtered Order Data")

st.dataframe(
    filtered_orders[
        [
            "order_id",
            "customer_id",
            "order_date",
            "product_name",
            "category",
            "net_sales",
            "profit",
            "payment_method",
            "sales_channel"
        ]
    ].sort_values(
        "order_date",
        ascending=False
    ),
    use_container_width=True,
    height=400
)


# -----------------------------
# DOWNLOAD
# -----------------------------
csv = filtered_orders.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Data",
    data=csv,
    file_name="shoppulse_filtered_orders.csv",
    mime="text/csv"
)


# -----------------------------
# FOOTER
# -----------------------------
st.divider()

st.caption(
    "ShopPulse | E-Commerce Business Intelligence Portfolio Project"
)