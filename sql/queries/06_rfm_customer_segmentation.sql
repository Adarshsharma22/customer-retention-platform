-- =====================================================
-- 06: RFM Customer Segmentation
-- Uses Window Functions: NTILE(5) for Recency and Monetary scoring
-- =====================================================

WITH customer_aggregates AS (
    SELECT
        c.customer_unique_id,
        MAX(o.order_purchase_timestamp) AS last_order_date,
        COUNT(DISTINCT o.order_id) AS total_orders,
        SUM(oi.price + oi.freight_value) AS total_spend,
        (
            SELECT MAX(order_purchase_timestamp) + INTERVAL '1 day' FROM orders
        ) AS snapshot_timestamp
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status != 'canceled'
    GROUP BY c.customer_unique_id
),
rfm_base AS (
    SELECT
        customer_unique_id,
        total_orders,
        ROUND(total_spend, 2) AS monetary_value,
        ROUND(
            EXTRACT(EPOCH FROM (snapshot_timestamp - last_order_date)) / (24 * 3600), 1
        ) AS recency_days
    FROM customer_aggregates
),
rfm_scores AS (
    SELECT
        customer_unique_id,
        recency_days,
        total_orders,
        monetary_value,
        NTILE(5) OVER (ORDER BY recency_days DESC) AS r_score,
        CASE
            WHEN total_orders >= 3 THEN 5
            WHEN total_orders = 2 THEN 4
            ELSE 1
        END AS f_score,
        NTILE(5) OVER (ORDER BY monetary_value ASC) AS m_score
    FROM rfm_base
),
rfm_segmented AS (
    SELECT
        customer_unique_id,
        recency_days,
        total_orders,
        monetary_value,
        r_score,
        f_score,
        m_score,
        CONCAT(r_score, f_score, m_score) AS rfm_combined,
        CASE
            WHEN r_score >= 4 AND f_score >= 4 THEN 'Champions'
            WHEN r_score >= 3 AND f_score >= 4 THEN 'Loyal Customers'
            WHEN r_score >= 4 AND f_score <= 2 THEN 'New / Potential Loyalists'
            WHEN r_score <= 2 AND f_score >= 4 THEN 'At Risk / Cannot Lose'
            WHEN r_score <= 2 AND f_score <= 2 AND m_score >= 4 THEN 'Hibernating High Spenders'
            WHEN r_score <= 2 AND f_score <= 2 AND m_score <= 2 THEN 'Lost Customers'
            ELSE 'Promising / Standard'
        END AS customer_segment
    FROM rfm_scores
)
SELECT
    customer_segment,
    COUNT(customer_unique_id) AS segment_size,
    ROUND(COUNT(customer_unique_id)::numeric / SUM(COUNT(customer_unique_id)) OVER () * 100, 2) AS customer_share_pct,
    ROUND(SUM(monetary_value), 2) AS total_segment_revenue,
    ROUND(SUM(monetary_value)::numeric / SUM(SUM(monetary_value)) OVER () * 100, 2) AS revenue_share_pct,
    ROUND(AVG(recency_days), 1) AS avg_recency_days,
    ROUND(AVG(monetary_value), 2) AS avg_monetary_spend
FROM rfm_segmented
GROUP BY customer_segment
ORDER BY total_segment_revenue DESC;
