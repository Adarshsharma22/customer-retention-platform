-- =====================================================
-- 09: Seller Fulfillment & Performance Rankings
-- Evaluates seller sales volume, fulfillment delay, and review scores
-- =====================================================

WITH seller_orders AS (
    SELECT
        s.seller_id,
        s.seller_state,
        COUNT(DISTINCT oi.order_id) AS fulfilled_orders,
        COUNT(oi.order_item_id) AS items_sold,
        ROUND(SUM(oi.price), 2) AS total_sales_volume,
        ROUND(AVG(oi.price), 2) AS avg_item_price,
        ROUND(AVG(
            EXTRACT(EPOCH FROM (o.order_delivered_customer_date - o.order_estimated_delivery_date)) / (24 * 3600)
        ), 1) AS avg_delivery_delay_days,
        ROUND(AVG(r.review_score), 2) AS avg_seller_review
    FROM sellers s
    JOIN order_items oi ON s.seller_id = oi.seller_id
    JOIN orders o ON oi.order_id = o.order_id
    LEFT JOIN reviews r ON o.order_id = r.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY s.seller_id, s.seller_state
)
SELECT
    seller_id,
    seller_state,
    fulfilled_orders,
    items_sold,
    total_sales_volume,
    avg_item_price,
    avg_delivery_delay_days,
    avg_seller_review,
    DENSE_RANK() OVER (ORDER BY total_sales_volume DESC) AS seller_revenue_rank
FROM seller_orders
ORDER BY total_sales_volume DESC
LIMIT 25;
