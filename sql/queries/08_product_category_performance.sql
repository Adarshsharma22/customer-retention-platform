-- =====================================================
-- 08: Product Category Performance & Growth
-- Analyzes sales volume, GMV, and English category mapping
-- =====================================================

WITH category_summary AS (
    SELECT
        COALESCE(ct.product_category_name_english, p.product_category_name, 'Other / Uncategorized') AS category_english,
        COUNT(DISTINCT oi.order_id) AS orders_count,
        COUNT(oi.order_item_id) AS units_sold,
        ROUND(SUM(oi.price), 2) AS total_gmv,
        ROUND(SUM(oi.freight_value), 2) AS total_freight,
        ROUND(SUM(oi.price + oi.freight_value), 2) AS total_category_revenue,
        ROUND(AVG(oi.price), 2) AS avg_unit_price
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    LEFT JOIN category_translation ct ON p.product_category_name = ct.product_category_name
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.order_status != 'canceled'
    GROUP BY COALESCE(ct.product_category_name_english, p.product_category_name, 'Other / Uncategorized')
)
SELECT
    category_english,
    orders_count,
    units_sold,
    total_gmv,
    total_category_revenue,
    avg_unit_price,
    ROUND(total_category_revenue / SUM(total_category_revenue) OVER () * 100, 2) AS revenue_share_pct,
    DENSE_RANK() OVER (ORDER BY total_category_revenue DESC) AS category_revenue_rank
FROM category_summary
ORDER BY total_category_revenue DESC
LIMIT 20;
