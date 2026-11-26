-- =====================================================
-- 11: Review Scores & Customer Satisfaction vs Delay
-- Tests impact of late delivery on 1-star vs 5-star customer ratings
-- =====================================================

WITH delivery_review_data AS (
    SELECT
        o.order_id,
        r.review_score,
        CASE
            WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date THEN 'Late Delivery'
            ELSE 'On-Time Delivery'
        END AS delivery_sla_status
    FROM orders o
    JOIN reviews r ON o.order_id = r.order_id
    WHERE o.order_status = 'delivered'
      AND o.order_delivered_customer_date IS NOT NULL
)
SELECT
    delivery_sla_status,
    COUNT(order_id) AS total_reviews,
    ROUND(AVG(review_score), 2) AS avg_review_score,
    ROUND(COUNT(CASE WHEN review_score = 5 THEN 1 END)::numeric / COUNT(order_id) * 100, 2) AS five_star_pct,
    ROUND(COUNT(CASE WHEN review_score = 1 THEN 1 END)::numeric / COUNT(order_id) * 100, 2) AS one_star_pct
FROM delivery_review_data
GROUP BY delivery_sla_status;
