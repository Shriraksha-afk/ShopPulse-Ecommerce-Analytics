
-- ShopPulse SQL Business Analysis
-- Compatible with MySQL 8+

USE shoppulse;

-- 1. Revenue, profit and orders
SELECT
    ROUND(SUM(net_sales),2) AS revenue,
    ROUND(SUM(profit),2) AS profit,
    COUNT(DISTINCT order_id) AS orders,
    COUNT(DISTINCT customer_id) AS customers,
    ROUND(SUM(net_sales)/COUNT(DISTINCT order_id),2) AS avg_order_value
FROM fact_orders
WHERE order_status='Delivered';

-- 2. Monthly revenue trend
SELECT DATE_FORMAT(order_date,'%Y-%m') AS month,
       ROUND(SUM(net_sales),2) AS revenue,
       ROUND(SUM(profit),2) AS profit,
       COUNT(DISTINCT order_id) AS orders
FROM fact_orders
WHERE order_status='Delivered'
GROUP BY DATE_FORMAT(order_date,'%Y-%m')
ORDER BY month;

-- 3. Category performance
SELECT category,
       ROUND(SUM(net_sales),2) revenue,
       ROUND(SUM(profit),2) profit,
       ROUND(SUM(profit)/SUM(net_sales)*100,2) margin_pct
FROM fact_orders
WHERE order_status='Delivered'
GROUP BY category
ORDER BY revenue DESC;

-- 4. Top 10 products by revenue
SELECT product_name, category,
       ROUND(SUM(net_sales),2) revenue,
       SUM(quantity) units
FROM fact_orders
WHERE order_status='Delivered'
GROUP BY product_id, product_name, category
ORDER BY revenue DESC
LIMIT 10;

-- 5. Top 10 products by profit
SELECT product_name, category,
       ROUND(SUM(profit),2) profit
FROM fact_orders
WHERE order_status='Delivered'
GROUP BY product_id, product_name, category
ORDER BY profit DESC
LIMIT 10;

-- 6. Customers by total spend
SELECT customer_id,
       ROUND(SUM(net_sales),2) lifetime_value,
       COUNT(DISTINCT order_id) orders
FROM fact_orders
WHERE order_status='Delivered'
GROUP BY customer_id
ORDER BY lifetime_value DESC
LIMIT 20;

-- 7. Repeat customer rate
WITH customer_orders AS (
    SELECT customer_id, COUNT(DISTINCT order_id) order_count
    FROM fact_orders
    WHERE order_status='Delivered'
    GROUP BY customer_id
)
SELECT
    ROUND(SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END)*100.0/COUNT(*),2)
      AS repeat_customer_rate_pct
FROM customer_orders;

-- 8. Revenue by state
SELECT state, ROUND(SUM(net_sales),2) revenue
FROM fact_orders
WHERE order_status='Delivered'
GROUP BY state
ORDER BY revenue DESC;

-- 9. Acquisition channel performance
SELECT acquisition_channel,
       ROUND(SUM(net_sales),2) revenue,
       COUNT(DISTINCT customer_id) customers,
       ROUND(SUM(net_sales)/COUNT(DISTINCT customer_id),2) revenue_per_customer
FROM fact_orders
WHERE order_status='Delivered'
GROUP BY acquisition_channel
ORDER BY revenue DESC;

-- 10. Payment method performance
SELECT payment_method,
       COUNT(*) orders,
       ROUND(SUM(net_sales),2) revenue
FROM fact_orders
WHERE order_status='Delivered'
GROUP BY payment_method
ORDER BY revenue DESC;

-- 11. Return rate by category
SELECT category,
       ROUND(SUM(order_status='Returned')*100.0/COUNT(*),2) return_rate_pct
FROM fact_orders
GROUP BY category
ORDER BY return_rate_pct DESC;

-- 12. Average delivery time by state
SELECT state,
       ROUND(AVG(delivery_days),2) avg_delivery_days
FROM fact_orders
WHERE order_status='Delivered'
GROUP BY state
ORDER BY avg_delivery_days DESC;

-- 13. Discount vs profit
SELECT discount_pct,
       ROUND(SUM(net_sales),2) revenue,
       ROUND(SUM(profit),2) profit
FROM fact_orders
WHERE order_status='Delivered'
GROUP BY discount_pct
ORDER BY discount_pct;

-- 14. Monthly active customers
SELECT DATE_FORMAT(order_date,'%Y-%m') month,
       COUNT(DISTINCT customer_id) active_customers
FROM fact_orders
WHERE order_status='Delivered'
GROUP BY DATE_FORMAT(order_date,'%Y-%m')
ORDER BY month;

-- 15. Orders by sales channel
SELECT sales_channel, COUNT(*) orders, ROUND(SUM(net_sales),2) revenue
FROM fact_orders
WHERE order_status='Delivered'
GROUP BY sales_channel
ORDER BY revenue DESC;

-- 16. Low-margin products with meaningful revenue
SELECT product_name, category,
       ROUND(SUM(net_sales),2) revenue,
       ROUND(SUM(profit)/SUM(net_sales)*100,2) margin_pct
FROM fact_orders
WHERE order_status='Delivered'
GROUP BY product_id, product_name, category
HAVING SUM(net_sales) > 50000
ORDER BY margin_pct ASC;

-- 17. Monthly order growth
WITH monthly AS (
 SELECT DATE_FORMAT(order_date,'%Y-%m') month,
        COUNT(DISTINCT order_id) orders
 FROM fact_orders
 WHERE order_status='Delivered'
 GROUP BY DATE_FORMAT(order_date,'%Y-%m')
)
SELECT month, orders,
       LAG(orders) OVER(ORDER BY month) previous_orders,
       ROUND((orders-LAG(orders) OVER(ORDER BY month))*100.0/
             NULLIF(LAG(orders) OVER(ORDER BY month),0),2) growth_pct
FROM monthly;

-- 18. Customer first vs latest purchase
WITH purchases AS (
 SELECT customer_id, MIN(order_date) first_order, MAX(order_date) latest_order
 FROM fact_orders
 WHERE order_status='Delivered'
 GROUP BY customer_id
)
SELECT customer_id, first_order, latest_order,
       DATEDIFF(latest_order,first_order) customer_lifespan_days
FROM purchases
ORDER BY customer_lifespan_days DESC;

-- 19. High-value customers who have not purchased recently
WITH x AS (
 SELECT customer_id,
        MAX(order_date) last_order,
        SUM(net_sales) lifetime_value
 FROM fact_orders
 WHERE order_status='Delivered'
 GROUP BY customer_id
)
SELECT customer_id, last_order, ROUND(lifetime_value,2) lifetime_value
FROM x
WHERE last_order < DATE_SUB((SELECT MAX(order_date) FROM fact_orders), INTERVAL 90 DAY)
  AND lifetime_value > 10000
ORDER BY lifetime_value DESC;

-- 20. Category contribution
WITH totals AS (
 SELECT SUM(net_sales) total_revenue
 FROM fact_orders
 WHERE order_status='Delivered'
)
SELECT category,
       ROUND(SUM(net_sales),2) revenue,
       ROUND(SUM(net_sales)*100.0/(SELECT total_revenue FROM totals),2) revenue_share_pct
FROM fact_orders
WHERE order_status='Delivered'
GROUP BY category
ORDER BY revenue DESC;
