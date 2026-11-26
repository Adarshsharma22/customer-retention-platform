-- =====================================================
-- VIEW: vw_category_sales
-- Product category dimensional view with English naming and revenue contribution
-- =====================================================

CREATE OR REPLACE VIEW vw_category_sales AS
SELECT
    COALESCE(ct.product_category_name_english, p.product_category_name, 'Other / Uncategorized') AS category_name,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    COUNT(oi.order_item_id) AS units_sold,
    ROUND(SUM(oi.price), 2) AS gmv,
    ROUND(SUM(oi.freight_value), 2) AS total_freight,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS total_revenue,
    ROUND(AVG(oi.price), 2) AS avg_item_price,
    ROUND(AVG(r.review_score), 2) AS avg_category_review
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
LEFT JOIN category_translation ct ON p.product_category_name = ct.product_category_name
JOIN orders o ON oi.order_id = o.order_id
LEFT JOIN reviews r ON o.order_id = r.order_id
WHERE o.order_status != 'canceled'
GROUP BY COALESCE(ct.product_category_name_english, p.product_category_name, 'Other / Uncategorized');
