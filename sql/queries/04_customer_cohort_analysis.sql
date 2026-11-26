-- =====================================================
-- 04: Monthly Customer Cohort Retention Analysis
-- Tracks customer cohorts over 12 months from first purchase
-- =====================================================

WITH customer_first_orders AS (
    SELECT
        c.customer_unique_id,
        TO_CHAR(MIN(o.order_purchase_timestamp), 'YYYY-MM') AS cohort_month,
        MIN(o.order_purchase_timestamp) AS first_order_timestamp
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.order_status != 'canceled'
    GROUP BY c.customer_unique_id
),
customer_activities AS (
    SELECT
        c.customer_unique_id,
        f.cohort_month,
        TO_CHAR(o.order_purchase_timestamp, 'YYYY-MM') AS activity_month,
        (
            EXTRACT(YEAR FROM o.order_purchase_timestamp) * 12 + EXTRACT(MONTH FROM o.order_purchase_timestamp)
        ) - (
            EXTRACT(YEAR FROM f.first_order_timestamp) * 12 + EXTRACT(MONTH FROM f.first_order_timestamp)
        ) AS cohort_index
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN customer_first_orders f ON c.customer_unique_id = f.customer_unique_id
    WHERE o.order_status != 'canceled'
),
cohort_sizes AS (
    SELECT
        cohort_month,
        COUNT(DISTINCT customer_unique_id) AS cohort_size
    FROM customer_first_orders
    GROUP BY cohort_month
),
retention_counts AS (
    SELECT
        a.cohort_month,
        a.cohort_index,
        COUNT(DISTINCT a.customer_unique_id) AS active_customers
    FROM customer_activities a
    GROUP BY a.cohort_month, a.cohort_index
)
SELECT
    r.cohort_month,
    s.cohort_size,
    r.cohort_index,
    r.active_customers,
    ROUND((r.active_customers::numeric / s.cohort_size) * 100, 2) AS retention_rate_pct
FROM retention_counts r
JOIN cohort_sizes s ON r.cohort_month = s.cohort_month
WHERE r.cohort_month >= '2017-01' AND r.cohort_month <= '2017-12'
  AND r.cohort_index <= 12
ORDER BY r.cohort_month, r.cohort_index;
