-- =====================================================
-- 07: Customer Lifetime Value (CLTV) Distribution
-- Computes observed historical customer value & percentiles
-- =====================================================

WITH customer_spending AS (
    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) AS total_orders,
        SUM(oi.price + oi.freight_value) AS lifetime_monetary_value,
        AVG(oi.price + oi.freight_value) AS avg_item_spend,
        MIN(o.order_purchase_timestamp) AS first_order,
        MAX(o.order_purchase_timestamp) AS last_order
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status != 'canceled'
    GROUP BY c.customer_unique_id
),
cltv_ranked AS (
    SELECT
        customer_unique_id,
        total_orders,
        lifetime_monetary_value,
        ROUND(
            EXTRACT(EPOCH FROM (last_order - first_order)) / (24 * 3600), 1
        ) AS customer_relationship_days,
        NTILE(10) OVER (ORDER BY lifetime_monetary_value) AS cltv_decile
    FROM customer_spending
)
SELECT
    cltv_decile,
    COUNT(customer_unique_id) AS customer_count,
    ROUND(MIN(lifetime_monetary_value), 2) AS min_cltv_brl,
    ROUND(MAX(lifetime_monetary_value), 2) AS max_cltv_brl,
    ROUND(AVG(lifetime_monetary_value), 2) AS avg_cltv_brl,
    ROUND(SUM(lifetime_monetary_value), 2) AS total_decile_revenue_brl,
    ROUND(SUM(lifetime_monetary_value) / SUM(SUM(lifetime_monetary_value)) OVER () * 100, 2) AS pct_of_platform_revenue
FROM cltv_ranked
GROUP BY cltv_decile
ORDER BY cltv_decile DESC;
