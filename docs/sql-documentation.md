# SQL Queries & Relational Views Documentation

**Project:** Customer Retention & Revenue Intelligence Platform  
**Dialect:** PostgreSQL 18  

---

## 1. Overview of Analytical SQL Queries

All queries are located in `sql/queries/`:

| Query File | Purpose & Business Question | Key Techniques Used |
|---|---|---|
| `01_business_kpi_analysis.sql` | Calculates total orders, unique customers, GMV, freight, revenue, and AOV. | CTEs, `SUM`, `AVG`, `COALESCE`, `CROSS JOIN` |
| `02_monthly_revenue_analysis.sql` | Computes monthly order counts, revenue, and Month-over-Month (MoM) growth rates. | Window functions: `LAG()`, Cumulative `SUM() OVER ()` |
| `03_customer_retention_analysis.sql`| Distinguishes one-time vs repeat purchasers by `customer_unique_id`. | `GROUP BY`, `CASE`, Subqueries, Aggregate windowing |
| `04_customer_cohort_analysis.sql` | Analyzes monthly cohort retention rates over a 12-month lifecycle. | Date math (`EXTRACT`), Cohort indexing, Matrix aggregation |
| `05_repeat_purchase_analysis.sql` | Calculates average days between successive purchases for repeat customers. | Window function: `LAG()`, `ROW_NUMBER() OVER (PARTITION BY ...)` |
| `06_rfm_customer_segmentation.sql` | Implements Recency, Frequency, and Monetary scoring into 7 segments. | Window function: `NTILE(5)`, `CASE` segmentation logic |
| `07_customer_lifetime_value.sql` | Analyzes customer historical monetary lifetime value by deciles. | Window function: `NTILE(10)`, Percentile revenue share |
| `08_product_category_performance.sql`| Ranks product categories by GMV and revenue share percentage. | Window function: `DENSE_RANK()`, `SUM() OVER ()` |
| `09_seller_performance.sql` | Ranks top sellers by fulfilled revenue, delivery delay days, and ratings. | Window function: `DENSE_RANK()`, Multi-table `JOIN` |
| `10_delivery_sla_analysis.sql` | Calculates delivery SLA breach rates and transit times across Brazilian states. | `EXTRACT(EPOCH)`, `CASE`, State-level grouping |
| `11_review_and_satisfaction_analysis.sql`| Analyzes rating degradation on late vs on-time deliveries. | Conditional aggregation, Review score distribution |
| `12_revenue_concentration_analysis.sql`| Evaluates Pareto 80/20 distribution across individual product SKUs. | Cumulative `SUM() OVER (ORDER BY ... ROWS BETWEEN ...)` |

---

## 2. Overview of Analytical SQL Views

All views are located in `sql/views/`:

1. `01_vw_orders_analytics.sql`: Single source of truth denormalized view joining orders, customers, items, payments, and reviews.
2. `02_vw_customer_rfm.sql`: Pre-computed customer segmentation view with RFM scores and segment tags.
3. `03_vw_category_sales.sql`: Aggregated category-level sales, unit volumes, and average prices.
4. `04_vw_seller_fulfillment.sql`: Aggregated merchant performance, fulfillment volume, and transit delays.
