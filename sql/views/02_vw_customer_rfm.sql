-- =====================================================
-- VIEW: vw_customer_rfm
-- Customer segmentation view calculating Recency, Frequency, and Monetary metrics
-- =====================================================

CREATE OR REPLACE VIEW vw_customer_rfm AS
WITH customer_base AS (
    SELECT
        c.customer_unique_id,
        MIN(o.order_purchase_timestamp) AS first_order_date,
        MAX(o.order_purchase_timestamp) AS last_order_date,
        COUNT(DISTINCT o.order_id) AS total_orders,
        SUM(oi.price + oi.freight_value) AS total_spend,
        AVG(r.review_score) AS avg_review_score,
        MAX(c.customer_state) AS primary_state,
        MAX(c.customer_city) AS primary_city,
        (SELECT MAX(order_purchase_timestamp) + INTERVAL '1 day' FROM orders) AS snapshot_date
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    LEFT JOIN reviews r ON o.order_id = r.order_id
    WHERE o.order_status != 'canceled'
    GROUP BY c.customer_unique_id
),
rfm_scored AS (
    SELECT
        customer_unique_id,
        first_order_date,
        last_order_date,
        total_orders,
        ROUND(total_spend, 2) AS total_spend,
        ROUND(EXTRACT(EPOCH FROM (snapshot_date - last_order_date)) / (24 * 3600), 1) AS recency_days,
        primary_state,
        primary_city,
        ROUND(avg_review_score, 2) AS avg_review_score,
        CASE WHEN total_orders > 1 THEN 'Repeat Customer' ELSE 'One-Time Customer' END AS customer_type,
        NTILE(5) OVER (ORDER BY EXTRACT(EPOCH FROM (snapshot_date - last_order_date)) DESC) AS r_score,
        CASE WHEN total_orders >= 3 THEN 5 WHEN total_orders = 2 THEN 4 ELSE 1 END AS f_score,
        NTILE(5) OVER (ORDER BY total_spend ASC) AS m_score
    FROM customer_base
)
SELECT
    customer_unique_id,
    first_order_date,
    last_order_date,
    total_orders,
    total_spend,
    recency_days,
    primary_state,
    primary_city,
    avg_review_score,
    customer_type,
    r_score,
    f_score,
    m_score,
    CONCAT(r_score, f_score, m_score) AS rfm_score,
    CASE
        WHEN r_score >= 4 AND f_score >= 4 THEN 'Champions'
        WHEN r_score >= 3 AND f_score >= 4 THEN 'Loyal Customers'
        WHEN r_score >= 4 AND f_score <= 2 THEN 'New / Potential Loyalists'
        WHEN r_score <= 2 AND f_score >= 4 THEN 'At Risk / Cannot Lose Them'
        WHEN r_score <= 2 AND f_score <= 2 AND m_score >= 4 THEN 'Hibernating High Spenders'
        WHEN r_score <= 2 AND f_score <= 2 AND m_score <= 2 THEN 'Lost Customers'
        ELSE 'Promising / Standard'
    END AS customer_segment
FROM rfm_scored;
