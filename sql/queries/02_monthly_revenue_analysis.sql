-- =====================================================
-- 02: Monthly Revenue Velocity & MoM Growth Analysis
-- Uses Window Functions: LAG() to compute Month-over-Month Growth
-- =====================================================

WITH monthly_orders AS (
    SELECT
        TO_CHAR(o.order_purchase_timestamp, 'YYYY-MM') AS order_year_month,
        COUNT(DISTINCT o.order_id) AS order_volume,
        COUNT(DISTINCT c.customer_unique_id) AS active_customers,
        ROUND(SUM(oi.price + oi.freight_value), 2) AS monthly_revenue,
        ROUND(AVG(oi.price + oi.freight_value), 2) AS monthly_aov
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status != 'canceled'
      AND o.order_purchase_timestamp >= '2017-01-01'
      AND o.order_purchase_timestamp < '2018-09-01'
    GROUP BY TO_CHAR(o.order_purchase_timestamp, 'YYYY-MM')
)
SELECT
    order_year_month,
    order_volume,
    active_customers,
    monthly_revenue,
    monthly_aov,
    ROUND(
        (monthly_revenue - LAG(monthly_revenue, 1) OVER (ORDER BY order_year_month)) /
        NULLIF(LAG(monthly_revenue, 1) OVER (ORDER BY order_year_month), 0) * 100, 2
    ) AS revenue_mom_growth_pct,
    ROUND(
        (order_volume - LAG(order_volume, 1) OVER (ORDER BY order_year_month))::numeric /
        NULLIF(LAG(order_volume, 1) OVER (ORDER BY order_year_month), 0) * 100, 2
    ) AS orders_mom_growth_pct,
    ROUND(
        SUM(monthly_revenue) OVER (ORDER BY order_year_month ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2
    ) AS cumulative_revenue_brl
FROM monthly_orders
ORDER BY order_year_month;
