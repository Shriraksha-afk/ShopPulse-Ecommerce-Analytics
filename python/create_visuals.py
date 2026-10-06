import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "visuals"
OUT.mkdir(exist_ok=True)

# Load datasets
category = pd.read_csv(ROOT / "data/processed/category_performance.csv")
monthly = pd.read_csv(ROOT / "data/processed/monthly_sales.csv")
rfm = pd.read_csv(ROOT / "data/processed/rfm_segments.csv")
product = pd.read_csv(ROOT / "data/processed/product_profitability.csv")
cohort = pd.read_csv(ROOT / "data/processed/cohort_retention.csv")

# 1. Revenue by Category
plt.figure(figsize=(10,6))
plt.bar(category["category"], category["revenue"])
plt.title("Revenue by Category")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=35, ha="right")
plt.tight_layout()
plt.savefig(OUT/"revenue_by_category.png", dpi=200)
plt.close()

# 2. Profit by Category
plt.figure(figsize=(10,6))
plt.bar(category["category"], category["profit"])
plt.title("Profit by Category")
plt.ylabel("Profit (₹)")
plt.xticks(rotation=35, ha="right")
plt.tight_layout()
plt.savefig(OUT/"profit_by_category.png", dpi=200)
plt.close()

# 3. Profit Margin by Category
plt.figure(figsize=(10,6))
plt.bar(category["category"], category["profit_margin_pct"])
plt.title("Profit Margin by Category")
plt.ylabel("Profit Margin (%)")
plt.xticks(rotation=35, ha="right")
plt.tight_layout()
plt.savefig(OUT/"profit_margin_by_category.png", dpi=200)
plt.close()

# 4. Monthly Revenue
plt.figure(figsize=(12,6))
plt.plot(monthly["order_month"], monthly["revenue"], marker="o")
plt.title("Monthly Revenue Trend")
plt.ylabel("Revenue (₹)")
plt.xlabel("Month")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(OUT/"monthly_revenue.png", dpi=200)
plt.close()

# 5. Monthly Profit
plt.figure(figsize=(12,6))
plt.plot(monthly["order_month"], monthly["profit"], marker="o")
plt.title("Monthly Profit Trend")
plt.ylabel("Profit (₹)")
plt.xlabel("Month")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(OUT/"monthly_profit.png", dpi=200)
plt.close()

# 6. RFM Segments
segments = rfm["segment"].value_counts()
plt.figure(figsize=(10,6))
plt.bar(segments.index, segments.values)
plt.title("Customer Segmentation — RFM")
plt.ylabel("Number of Customers")
plt.xticks(rotation=35, ha="right")
plt.tight_layout()
plt.savefig(OUT/"rfm_segments.png", dpi=200)
plt.close()

# 7. Top 10 Products by Revenue
top_products = product.nlargest(10, "revenue").sort_values("revenue")
plt.figure(figsize=(10,6))
plt.barh(top_products["product_name"], top_products["revenue"])
plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue (₹)")
plt.tight_layout()
plt.savefig(OUT/"top_products_revenue.png", dpi=200)
plt.close()

# 8. Top 10 Products by Profit
top_profit = product.nlargest(10, "profit").sort_values("profit")
plt.figure(figsize=(10,6))
plt.barh(top_profit["product_name"], top_profit["profit"])
plt.title("Top 10 Products by Profit")
plt.xlabel("Profit (₹)")
plt.tight_layout()
plt.savefig(OUT/"top_products_profit.png", dpi=200)
plt.close()

print("✅ All visualizations created successfully!")
print(f"📁 Saved in: {OUT}")
