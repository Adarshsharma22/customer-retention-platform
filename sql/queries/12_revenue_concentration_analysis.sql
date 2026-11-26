-- =====================================================
-- 12: Pareto 80/20 Revenue Concentration Analysis
-- Uses Window Function: Cumulative SUM() to evaluate revenue concentration
-- =====================================================

WITH product_revenues AS (
    SELECT
        oi.product_id,
        COALESCE(ct.product_category_name_english, 'Uncategorized') AS category,
        ROUND(SUM(oi.price), 2) AS product_revenue
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    LEFT JOIN category_translation ct ON p.product_category_name = ct.product_category_name
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.order_status != 'canceled'
    GROUP BY oi.product_id, COALESCE(ct.product_category_name_english, 'Uncategorized')
),
ranked_products AS (
    SELECT
        product_id,
        category,
        product_revenue,
        ROW_NUMBER() OVER (ORDER BY product_revenue DESC) AS product_rank,
        COUNT(*) OVER () AS total_products,
        SUM(product_revenue) OVER (ORDER BY product_revenue DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_revenue,
        SUM(product_revenue) OVER () AS total_platform_revenue
    FROM product_revenues
)
SELECT
    product_rank,
    product_id,
    category,
    product_revenue,
    ROUND((product_rank::numeric / total_products) * 100, 2) AS product_percentile,
    ROUND((cumulative_revenue / total_platform_revenue) * 100, 2) AS cumulative_revenue_pct
FROM ranked_products
WHERE product_rank IN (1, 10, 50, 100, 500, 1000, 2500, 5000, 10000)
ORDER BY product_rank;
