-- =====================================================
-- 05: Repeat Purchase Interval & Purchase Velocity
-- Uses Window Function: LAG() to calculate days between repeat purchases
-- =====================================================

WITH customer_order_history AS (
    SELECT
        c.customer_unique_id,
        o.order_id,
        o.order_purchase_timestamp,
        ROW_NUMBER() OVER (
            PARTITION BY c.customer_unique_id
            ORDER BY o.order_purchase_timestamp
        ) AS order_sequence_num,
        LAG(o.order_purchase_timestamp, 1) OVER (
            PARTITION BY c.customer_unique_id
            ORDER BY o.order_purchase_timestamp
        ) AS previous_order_timestamp
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.order_status != 'canceled'
),
repeat_intervals AS (
    SELECT
        customer_unique_id,
        order_id,
        order_sequence_num,
        order_purchase_timestamp,
        previous_order_timestamp,
        ROUND(
            EXTRACT(EPOCH FROM (order_purchase_timestamp - previous_order_timestamp)) / (24 * 3600), 1
        ) AS days_since_prior_order
    FROM customer_order_history
    WHERE order_sequence_num > 1
)
SELECT
    order_sequence_num AS purchase_order_number,
    COUNT(order_id) AS total_repeat_orders,
    ROUND(AVG(days_since_prior_order), 1) AS avg_days_to_repurchase,
    ROUND(MIN(days_since_prior_order), 1) AS min_days_to_repurchase,
    ROUND(MAX(days_since_prior_order), 1) AS max_days_to_repurchase
FROM repeat_intervals
GROUP BY order_sequence_num
ORDER BY order_sequence_num;
