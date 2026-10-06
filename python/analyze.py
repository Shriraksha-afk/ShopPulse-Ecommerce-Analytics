
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data/processed/fact_orders.csv", parse_dates=["order_date"])

# Keep completed orders for core revenue analysis
sales = df[df["order_status"] == "Delivered"].copy()

print("\n--- DATA QUALITY ---")
print("Rows:", len(df))
print("Missing values:\n", df.isna().sum().sort_values(ascending=False).head(10))

print("\n--- EXECUTIVE KPIs ---")
print("Revenue:", round(sales["net_sales"].sum(),2))
print("Profit:", round(sales["profit"].sum(),2))
print("Orders:", len(sales))
print("Customers:", sales["customer_id"].nunique())
print("AOV:", round(sales["net_sales"].mean(),2))
print("Return rate:", round((df["order_status"]=="Returned").mean()*100,2), "%")

# Monthly trend
monthly = sales.groupby(sales["order_date"].dt.to_period("M")).agg(
    revenue=("net_sales","sum"),
    profit=("profit","sum"),
    orders=("order_id","nunique")
).reset_index()
monthly["order_month"] = monthly["order_date"].astype(str)
monthly.to_csv(ROOT/"data/processed/monthly_sales.csv",index=False)

# Category analysis
category = sales.groupby("category").agg(
    revenue=("net_sales","sum"),
    profit=("profit","sum"),
    orders=("order_id","nunique"),
    units=("quantity","sum")
).sort_values("revenue",ascending=False).reset_index()
category["profit_margin_pct"] = category["profit"]/category["revenue"]*100
category.to_csv(ROOT/"data/processed/category_performance.csv",index=False)

# RFM segmentation
snapshot = sales["order_date"].max() + pd.Timedelta(days=1)
rfm = sales.groupby("customer_id").agg(
    recency=("order_date", lambda x: (snapshot-x.max()).days),
    frequency=("order_id","nunique"),
    monetary=("net_sales","sum")
).reset_index()
rfm["R"] = pd.qcut(rfm["recency"],5,labels=[5,4,3,2,1],duplicates="drop").astype(int)
rfm["F"] = pd.qcut(rfm["frequency"].rank(method="first"),5,labels=[1,2,3,4,5]).astype(int)
rfm["M"] = pd.qcut(rfm["monetary"].rank(method="first"),5,labels=[1,2,3,4,5]).astype(int)
rfm["rfm_score"] = rfm["R"]+rfm["F"]+rfm["M"]
rfm["segment"] = np.select(
    [rfm.rfm_score>=13, rfm.rfm_score>=10, rfm.rfm_score>=7, rfm.rfm_score>=4],
    ["Champions","Loyal Customers","Potential Loyalists","At Risk"],
    default="Hibernating"
)
rfm.to_csv(ROOT/"data/processed/rfm_segments.csv",index=False)

# Cohort retention
customer_first = sales.groupby("customer_id")["order_date"].min().rename("first_order")
cohort = sales.merge(customer_first,on="customer_id")
cohort["order_month"] = cohort.order_date.dt.to_period("M")
cohort["cohort_month"] = cohort.first_order.dt.to_period("M")
cohort_index = ((cohort.order_month.dt.year-cohort.cohort_month.dt.year)*12+
                (cohort.order_month.dt.month-cohort.cohort_month.dt.month))
cohort["cohort_index"] = cohort_index
retention = cohort.groupby(["cohort_month","cohort_index"])["customer_id"].nunique().reset_index()
retention.to_csv(ROOT/"data/processed/cohort_retention.csv",index=False)

# Product profitability
product = sales.groupby(["product_id","product_name","category"]).agg(
    revenue=("net_sales","sum"), profit=("profit","sum"), units=("quantity","sum")
).reset_index()
product["margin_pct"]=product["profit"]/product["revenue"]*100
product.to_csv(ROOT/"data/processed/product_profitability.csv",index=False)

print("\nAnalysis outputs written to data/processed/")
