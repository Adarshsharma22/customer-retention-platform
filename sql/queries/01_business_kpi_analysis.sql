-- =====================================================
-- 01: Executive Business KPI Analysis
-- Core Metrics: Total Orders, Unique Customers, GMV, Freight, Total Revenue, AOV
-- =====================================================

WITH order_financials AS (
    SELECT
        o.order_id,
        o.customer_id,
        c.customer_unique_id,
        o.order_status,
        COALESCE(SUM(oi.price), 0) AS total_items_gmv,
        COALESCE(SUM(oi.freight_value), 0) AS total_freight,
        COALESCE(SUM(oi.price + oi.freight_value), 0) AS total_order_value
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    LEFT JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status != 'canceled'
    GROUP BY o.order_id, o.customer_id, c.customer_unique_id, o.order_status
),
reviews_summary AS (
    SELECT
        AVG(review_score) AS avg_review_score,
        COUNT(review_id) AS total_reviews
    FROM reviews
)
SELECT
    COUNT(DISTINCT f.order_id) AS total_completed_orders,
    COUNT(DISTINCT f.customer_unique_id) AS total_unique_customers,
    ROUND(SUM(f.total_items_gmv), 2) AS total_gmv_brl,
    ROUND(SUM(f.total_freight), 2) AS total_freight_brl,
    ROUND(SUM(f.total_order_value), 2) AS total_revenue_brl,
    ROUND(AVG(f.total_order_value), 2) AS average_order_value_brl,
    ROUND(r.avg_review_score, 2) AS platform_avg_review_score
FROM order_financials f
CROSS JOIN reviews_summary r
GROUP BY r.avg_review_score;
