# Power BI Data Model Architecture & Star Schema Design

**Project:** Customer Retention & Revenue Intelligence Platform  
**Model Design:** Conformed Star Schema  
**Target Application:** Power BI Desktop  

---

## 1. Dimensional Model Overview

The analytical data model uses an enterprise Star Schema centered around transactional and dimensional business processes:

```
                          ┌────────────────────┐
                          │    dim_customers   │
                          └─────────┬──────────┘
                                    │ 1
                                    │ 
                                    │ *
                          ┌─────────▼──────────┐
  ┌──────────────────┐    │                    │    ┌──────────────────┐
  │     dim_date     ├───►│    fact_orders     │◄───┤  dim_geolocation │
  └──────────────────┘ *  │                    │ 1  └──────────────────┘
                          └─────────┬──────────┘
                                    │ 1
                                    │
               ┌────────────────────┼────────────────────┐
               │ *                  │ *                  │ *
     ┌─────────▼──────────┐ ┌───────▼──────────┐ ┌───────▼──────────┐
     │  fact_order_items  │ │   fact_payments  │ │   fact_reviews   │
     └─────────┬──────────┘ └──────────────────┘ └──────────────────┘
               │ *
        ┌──────┴──────┐
        │ 1           │ 1
 ┌──────▼──────┐ ┌────▼────────┐
 │ dim_products│ │ dim_sellers │
 └─────────────┘ └─────────────┘
```

---

## 2. Table Catalog & Role

| Table Name | Type | Key Field | Description |
|---|---|---|---|
| `fact_orders` | Fact (Header) | `order_id` (PK) | Grain: One row per order. Order lifecycle, delivery status, financial rollups. |
| `fact_order_items` | Fact (Line-Item)| `order_id`, `order_item_id` (Composite PK) | Grain: One row per purchased item. Price, freight, seller, product links. |
| `fact_payments` | Fact (Financial)| `order_id`, `payment_sequential` (Composite PK) | Grain: One row per payment transaction installment. |
| `fact_reviews` | Fact (Feedback) | `review_id`, `order_id` | Grain: One row per customer review submission. |
| `dim_customers` | Dimension | `customer_id` (PK), `customer_unique_id` | Enriched with RFM segments, customer type (One-time vs Repeat). |
| `dim_products` | Dimension | `product_id` (PK) | Product categories, English translations, physical dimensions. |
| `dim_sellers` | Dimension | `seller_id` (PK) | Seller geographic location and performance tier. |
| `dim_geolocation`| Dimension | `geolocation_zip_code_prefix` (PK) | Clean consolidated coordinates (median lat/lng) by ZIP code. |
| `dim_date` | Dimension | `Date` (PK), `DateKey` | Standard continuous business calendar (2016-2018). |

---

## 3. Relationships & Cardinality

1. `dim_customers[customer_id]` 1 ───► * `fact_orders[customer_id]` (Single direction)
2. `dim_date[Date]` 1 ───► * `fact_orders[order_purchase_timestamp]` (Single direction, Active)
3. `fact_orders[order_id]` 1 ───► * `fact_order_items[order_id]` (Single direction)
4. `fact_orders[order_id]` 1 ───► * `fact_payments[order_id]` (Single direction)
5. `fact_orders[order_id]` 1 ───► * `fact_reviews[order_id]` (Single direction)
6. `dim_products[product_id]` 1 ───► * `fact_order_items[product_id]` (Single direction)
7. `dim_sellers[seller_id]` 1 ───► * `fact_order_items[seller_id]` (Single direction)
8. `dim_geolocation[geolocation_zip_code_prefix]` 1 ───► * `dim_customers[customer_zip_code_prefix]` (Single direction)

---

## 4. Verification & Integrity Checklist

- **No Many-to-Many Relationships:** Avoided snowflake loops and bridge tables.
- **Deduplicated Geolocation:** Resolved 261,831 duplicate coordinates down to unique zip code prefixes.
- **Date Continuity:** Calendar covers full dataset range with zero gaps.
