
CREATE DATABASE IF NOT EXISTS shoppulse;
USE shoppulse;

CREATE TABLE fact_orders (
 order_id INT PRIMARY KEY,
 customer_id INT,
 product_id INT,
 order_date DATE,
 quantity INT,
 order_status VARCHAR(30),
 payment_method VARCHAR(30),
 sales_channel VARCHAR(30),
 unit_price DECIMAL(12,2),
 unit_cost DECIMAL(12,2),
 gross_sales DECIMAL(12,2),
 discount_pct DECIMAL(5,2),
 discount_amount DECIMAL(12,2),
 net_sales DECIMAL(12,2),
 shipping_cost DECIMAL(12,2),
 profit DECIMAL(12,2),
 delivery_days DECIMAL(6,2),
 order_month VARCHAR(7),
 city VARCHAR(100),
 state VARCHAR(100),
 acquisition_channel VARCHAR(50)
);
