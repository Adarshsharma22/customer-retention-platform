-- =====================================================
-- VIEW: vw_orders_analytics
-- Comprehensive denormalized view joining orders, customers, items, payments, and reviews
-- =====================================================

CREATE OR REPLACE VIEW vw_orders_analytics AS
WITH items_agg AS (
    SELECT
        order_id,
        COUNT(order_item_id) AS items_count,
        COUNT(DISTINCT product_id) AS unique_products,
        COUNT(DISTINCT seller_id) AS unique_sellers,
        SUM(price) AS items_gmv,
        SUM(freight_value) AS freight_total,
        SUM(price + freight_value) AS total_order_value
    FROM order_items
    GROUP BY order_id
),
payments_agg AS (
    SELECT
        order_id,
        SUM(payment_value) AS total_payment_value,
        STRING_AGG(DISTINCT payment_type, ', ') AS payment_methods,
        MAX(payment_installments) AS max_installments
    FROM payments
    GROUP BY order_id
),
reviews_agg AS (
    SELECT
        order_id,
        AVG(review_score) AS avg_review_score,
        COUNT(review_id) AS reviews_count
    FROM reviews
    GROUP BY order_id
)
SELECT
    o.order_id,
    o.customer_id,
    c.customer_unique_id,
    c.customer_city,
    c.customer_state,
    c.customer_zip_code_prefix,
    o.order_status,
    o.order_purchase_timestamp,
    TO_CHAR(o.order_purchase_timestamp, 'YYYY-MM') AS purchase_year_month,
    o.order_approved_at,
    o.order_delivered_carrier_date,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,
    ROUND(
        EXTRACT(EPOCH FROM (o.order_delivered_customer_date - o.order_purchase_timestamp)) / (24 * 3600), 1
    ) AS actual_delivery_days,
    ROUND(
        EXTRACT(EPOCH FROM (o.order_estimated_delivery_date - o.order_purchase_timestamp)) / (24 * 3600), 1
    ) AS estimated_delivery_days,
    ROUND(
        EXTRACT(EPOCH FROM (o.order_delivered_customer_date - o.order_estimated_delivery_date)) / (24 * 3600), 1
    ) AS delivery_delay_days,
    CASE
        WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date THEN TRUE
        ELSE FALSE
    END AS is_late_delivery,
    COALESCE(i.items_count, 0) AS items_count,
    COALESCE(i.items_gmv, 0.0) AS items_gmv,
    COALESCE(i.freight_total, 0.0) AS freight_total,
    COALESCE(i.total_order_value, p.total_payment_value, 0.0) AS total_order_value,
    p.total_payment_value,
    p.payment_methods,
    COALESCE(p.max_installments, 1) AS max_installments,
    r.avg_review_score
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN items_agg i ON o.order_id = i.order_id
LEFT JOIN payments_agg p ON o.order_id = p.order_id
LEFT JOIN reviews_agg r ON o.order_id = r.order_id;
