-- =====================================================
-- 03: Customer Retention & Repeat Purchase Rate
-- Identifies first-time vs repeat customers using customer_unique_id
-- =====================================================

WITH customer_order_frequencies AS (
    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) AS total_orders,
        SUM(oi.price + oi.freight_value) AS total_spend,
        MIN(o.order_purchase_timestamp) AS first_order_date,
        MAX(o.order_purchase_timestamp) AS last_order_date
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status != 'canceled'
    GROUP BY c.customer_unique_id
),
segmented_customers AS (
    SELECT
        customer_unique_id,
        total_orders,
        total_spend,
        CASE
            WHEN total_orders > 1 THEN 'Repeat Customer'
            ELSE 'One-Time Customer'
        END AS customer_retention_status
    FROM customer_order_frequencies
)
SELECT
    customer_retention_status,
    COUNT(customer_unique_id) AS customer_count,
    ROUND(COUNT(customer_unique_id)::numeric / SUM(COUNT(customer_unique_id)) OVER () * 100, 2) AS customer_share_pct,
    ROUND(SUM(total_spend), 2) AS total_revenue_contribution,
    ROUND(SUM(total_spend)::numeric / SUM(SUM(total_spend)) OVER () * 100, 2) AS revenue_share_pct,
    ROUND(AVG(total_spend), 2) AS average_spend_per_customer
FROM segmented_customers
GROUP BY customer_retention_status;
