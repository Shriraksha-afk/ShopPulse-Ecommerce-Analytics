# ShopPulse E-Commerce Analytics — Analysis Walkthrough

This notebook guide explains the complete analytical workflow.

## 1. Business Questions
1. How is revenue and profit trending?
2. Which categories/products drive revenue and margin?
3. Who are our highest-value customers?
4. How many customers return after their first purchase?
5. Which regions and acquisition channels perform best?
6. Where should management focus retention and profitability efforts?

## 2. Run the analysis

```bash
python python/analyze.py
```

The script creates:
- `monthly_sales.csv`
- `category_performance.csv`
- `rfm_segments.csv`
- `cohort_retention.csv`
- `product_profitability.csv`

## 3. Recommended visual analysis

Create charts for:
- Monthly revenue and profit
- Revenue by category
- Profit margin by category
- RFM customer segment distribution
- Cohort retention heatmap
- Top 10 products by revenue
- Top 10 products by profit
- State-wise revenue
- Acquisition-channel revenue
