# ShopPulse — E-Commerce Business Intelligence & Customer Analytics

![Python](https://img.shields.io/badge/Python-3.x-blue)
![SQL](https://img.shields.io/badge/SQL-MySQL-orange)
![Power%20BI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

## 📌 Project Overview

**ShopPulse** is an end-to-end e-commerce analytics project designed to answer real business questions using **Python, SQL and Power BI**.

The project analyzes sales performance, customer behavior, product profitability, retention and regional performance and converts the findings into actionable business recommendations.

## 🎯 Business Objectives

- Track revenue, profit and order trends
- Identify high-performing and low-performing products
- Segment customers using RFM analysis
- Measure repeat purchase behavior and retention
- Compare acquisition channels and regions
- Identify profitability and discounting opportunities
- Build an executive-ready Power BI dashboard

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python | Data cleaning, EDA and analytics |
| Pandas | Data manipulation |
| NumPy | Numerical analysis |
| Matplotlib | Visualization |
| MySQL | Business querying |
| Power BI | Interactive dashboard |
| Git/GitHub | Version control and portfolio |

## 📂 Dataset

The project contains synthetic but realistic e-commerce data generated with a fixed random seed for reproducibility:

- **2,500 customers**
- **180 products**
- **12,000 orders**
- 6 product categories
- Multiple Indian cities and states
- Payment methods and sales channels
- Discounts, shipping costs, returns and profit

This dataset is created for portfolio/learning purposes and does not represent a real company.

## 📊 Analysis Performed

### Sales Analytics
- Monthly revenue
- Profit trends
- Average order value
- Order growth
- Category contribution

### Customer Analytics
- RFM segmentation
- Lifetime value
- Repeat customer rate
- High-value inactive customers
- Cohort retention

### Product Analytics
- Top products
- Product profitability
- Category margin
- Discount vs profit

### Operations
- Return rate
- Delivery performance
- State-level performance
- Sales channel performance

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ShopPulse-Ecommerce-Analytics.git
cd ShopPulse-Ecommerce-Analytics
```

### 2. Install Python packages

```bash
pip install -r requirements.txt
```

### 3. Run the analysis

```bash
python python/analyze.py
```

### 4. Use SQL

Create a MySQL database and run:

```text
sql/schema.sql
sql/business_analysis.sql
```

### 5. Build the Power BI dashboard

Import:

```text
data/processed/fact_orders.csv
```

Follow `powerbi/POWER_BI_GUIDE.md` for the dashboard structure and DAX measures.

## 💡 Key Business Questions

1. Which categories generate the most revenue?
2. Which categories have the best profit margins?
3. Who are our highest-value customers?
4. What percentage of customers return?
5. Which acquisition channels bring valuable customers?
6. Which states contribute the most revenue?
7. Which products have high revenue but weak margins?
8. How does discounting affect profitability?
9. How does customer retention change over time?
10. Which high-value customers are at risk of churn?

## 📈 Recommended Dashboard

Build a 5-page Power BI report:

1. **Executive Overview**
2. **Customer Analytics**
3. **Product & Profitability**
4. **Customer Retention**
5. **Management Insights**

## 🧠 Portfolio Value

This project demonstrates:

- Data cleaning
- Exploratory data analysis
- SQL business analysis
- Customer segmentation
- Cohort analysis
- KPI development
- Data visualization
- Business storytelling
- Dashboard design
- Git/GitHub workflow

## 👩‍💻 Resume Description

**ShopPulse — E-Commerce Business Intelligence & Customer Analytics**

Built an end-to-end e-commerce analytics solution using Python, SQL and Power BI to analyze 12K+ transactions across sales, customer behavior, product profitability and retention. Implemented RFM customer segmentation and cohort analysis, developed business KPIs and SQL insights, and designed an executive dashboard to identify growth, profitability and customer-retention opportunities.

## 📜 License

MIT License
