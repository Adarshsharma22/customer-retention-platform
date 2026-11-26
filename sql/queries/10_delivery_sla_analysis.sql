-- =====================================================
-- 10: Delivery SLA & Logistics Fulfillment Analysis
-- Analyzes delivery durations, late rate %, and state logistics bottlenecks
-- =====================================================

WITH delivery_metrics AS (
    SELECT
        o.order_id,
        c.customer_state,
        o.order_purchase_timestamp,
        o.order_delivered_customer_date,
        o.order_estimated_delivery_date,
        ROUND(
            EXTRACT(EPOCH FROM (o.order_delivered_customer_date - o.order_purchase_timestamp)) / (24 * 3600), 1
        ) AS actual_delivery_days,
        ROUND(
            EXTRACT(EPOCH FROM (o.order_estimated_delivery_date - o.order_purchase_timestamp)) / (24 * 3600), 1
        ) AS estimated_delivery_days,
        CASE
            WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date THEN 1
            ELSE 0
        END AS is_late_delivery
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered'
      AND o.order_delivered_customer_date IS NOT NULL
)
SELECT
    customer_state,
    COUNT(order_id) AS total_delivered_orders,
    ROUND(AVG(actual_delivery_days), 1) AS avg_delivery_time_days,
    ROUND(AVG(estimated_delivery_days), 1) AS avg_estimated_delivery_days,
    SUM(is_late_delivery) AS total_late_deliveries,
    ROUND((SUM(is_late_delivery)::numeric / COUNT(order_id)) * 100, 2) AS late_delivery_rate_pct,
    DENSE_RANK() OVER (ORDER BY (SUM(is_late_delivery)::numeric / COUNT(order_id)) DESC) AS state_delay_risk_rank
FROM delivery_metrics
GROUP BY customer_state
HAVING COUNT(order_id) >= 100
ORDER BY late_delivery_rate_pct DESC;
