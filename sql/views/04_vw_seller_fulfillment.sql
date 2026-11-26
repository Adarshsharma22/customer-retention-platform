-- =====================================================
-- VIEW: vw_seller_fulfillment
-- Seller performance view tracking orders fulfilled, revenue, delay days, and customer scores
-- =====================================================

CREATE OR REPLACE VIEW vw_seller_fulfillment AS
SELECT
    s.seller_id,
    s.seller_state,
    s.seller_city,
    COUNT(DISTINCT oi.order_id) AS orders_fulfilled,
    COUNT(oi.order_item_id) AS items_sold,
    ROUND(SUM(oi.price), 2) AS seller_revenue,
    ROUND(AVG(oi.price), 2) AS avg_unit_price,
    ROUND(AVG(
        EXTRACT(EPOCH FROM (o.order_delivered_customer_date - o.order_estimated_delivery_date)) / (24 * 3600)
    ), 1) AS avg_delivery_delay_days,
    ROUND(AVG(r.review_score), 2) AS avg_seller_review
FROM sellers s
JOIN order_items oi ON s.seller_id = oi.seller_id
JOIN orders o ON oi.order_id = o.order_id
LEFT JOIN reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
GROUP BY s.seller_id, s.seller_state, s.seller_city;
