# Power BI Dashboard Specification

## Data source
Import `data/processed/fact_orders.csv`.

## Calculated measures (DAX)

```DAX
Revenue = CALCULATE(SUM(fact_orders[net_sales]), fact_orders[order_status] = "Delivered")

Profit = CALCULATE(SUM(fact_orders[profit]), fact_orders[order_status] = "Delivered")

Orders = CALCULATE(DISTINCTCOUNT(fact_orders[order_id]), fact_orders[order_status] = "Delivered")

Customers = CALCULATE(DISTINCTCOUNT(fact_orders[customer_id]), fact_orders[order_status] = "Delivered")

AOV = DIVIDE([Revenue], [Orders])

Profit Margin = DIVIDE([Profit], [Revenue])

Return Rate =
DIVIDE(
    CALCULATE(COUNTROWS(fact_orders), fact_orders[order_status] = "Returned"),
    COUNTROWS(fact_orders)
)
```

## Page 1 — Executive Overview
Cards: Revenue, Profit, Orders, Customers, AOV, Profit Margin

Charts:
- Revenue & Profit by Month
- Revenue by Category
- Revenue by State
- Orders by Sales Channel

## Page 2 — Customer Analytics
- RFM Segment distribution
- Revenue by acquisition channel
- Repeat vs one-time customers
- Top customers by lifetime value

## Page 3 — Product & Profitability
- Top 10 products by revenue
- Top 10 products by profit
- Category revenue vs margin
- Discount percentage vs profit

## Page 4 — Retention
- Cohort retention heatmap
- Monthly active customers
- Customer lifespan distribution

## Page 5 — Management Insights
Summarize:
- strongest growth areas
- low-margin categories
- high-value customer segments
- retention opportunities
- operational issues
