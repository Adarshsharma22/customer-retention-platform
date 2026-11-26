# Data Quality & Cleansing Report

**Project:** Customer Retention & Revenue Intelligence Platform  
**Pipeline:** `python/etl/clean_data.py`  
**Generated On:** 2026-11-25 19:31:43  

---

## 1. Executive Summary

This report documents the quality audit, cleansing transformations, anomaly treatments, and analytical marts created from the Olist Brazilian E-Commerce public dataset.

All original raw datasets in `data/raw/` remain untouched. Cleansed datasets are exported to `data/cleaned/` and enriched business marts are saved to `data/processed/`.

---

## 2. Cleansing Actions by Dataset

### 2.1 Category Translation (`category_translation.csv`)
- **Raw Count:** 71
- **Cleaned Count:** 71
- **Transformations:** Trimmed whitespace, converted to lowercase, verified zero duplicates.

### 2.2 Customers (`customers.csv`)
- **Raw Records:** 99,441
- **Unique `customer_id` (Order-level tokens):** 99,441
- **Unique `customer_unique_id` (Real Persons):** 96,096
- **Transformations:** Standardized city names to Title Case, state codes to Upper Case, validated ZIP prefix format.

### 2.3 Geolocation (`geolocation.csv`)
- **Raw Records:** 1,000,163
- **Invalid GPS Coordinates Filtered:** 29
- **Cleaned Unique ZIP Codes:** 19,011
- **Duplicates Resolved:** 981,152
- **Methodology:** Aggregated multiple noisy GPS coordinates per zip code prefix using median latitude and longitude, eliminating 261k duplicate rows while preserving accurate Brazilian geographic mapping.

### 2.4 Products (`products.csv`)
- **Raw Records:** 32,951
- **Cleaned Records:** 32,951
- **Missing Categories:** Imputed 610 missing categories with `'outros'` (others).
- **Missing Dimensions/Weight:** Imputed with median category values to avoid deleting product records.
- **English Translation:** Enriched with English category translations.

### 2.5 Orders (`orders.csv`)
- **Raw Records:** 99,441
- **Delivered Orders:** 96,478
- **Late Deliveries:** 7,826
- **Canceled / Incomplete:** 1,234
- **Transformations:** Parsed all 5 timestamp columns to ISO datetimes. Engineered `actual_delivery_days`, `estimated_delivery_days`, `delivery_delay_days`, and `is_late_delivery` flag. Preserved non-delivered orders as valid cancellation records.

### 2.6 Order Items (`order_items.csv`)
- **Raw Records:** 112,650
- **Total GMV (Price):** R$ 13,591,643.70
- **Total Freight:** R$ 2,251,909.54
- **Transformations:** Verified composite PK (`order_id`, `order_item_id`). Validated `price >= 0` and `freight_value >= 0`.

### 2.7 Payments (`payments.csv`)
- **Raw Records:** 103,886
- **Total Payment Volume:** R$ 16,008,872.12
- **Transformations:** Verified non-negative payment values, standardized payment types (credit card, boleto, voucher, debit card).

### 2.8 Reviews (`reviews.csv`)
- **Raw Records:** 99,224
- **Average Review Score:** 4.09 / 5.0
- **Missing Text Handling:** Filled missing `review_comment_title` with `'No Title'` and `review_comment_message` with `'No Comment'` without dropping valuable numeric ratings.
- **Sentiment Feature:** Engineered `review_sentiment` (Positive: 4-5, Neutral: 3, Negative: 1-2).

---

## 3. Analytical Marts Generated (`data/processed/`)

1. **`orders_enriched.csv`**: Comprehensive denormalized order-level view with customer locations, payment totals, item counts, delivery durations, delay metrics, and review scores.
2. **`customer_rfm_segments.csv`**: Customer-level intelligence aggregated by `customer_unique_id`. Contains Recency, Frequency, Monetary value, quintile RFM scores, and segment assignments (Champions, Loyal, At Risk, Lost).
3. **`cohort_retention_rate_matrix.csv`**: Month-by-month cohort customer retention percentages from Month 0 to Month 24.
4. **`category_performance.csv`**: Revenue, unit sales, average prices, and cumulative Pareto percentages across product categories.
5. **`seller_performance.csv`**: Revenue volume, fulfillment efficiency, and delivery delay metrics per seller.

---

## 4. Key Data Quality Findings

- **Customer Identification:** 99,441 records in `customers.csv` correspond to 96,096 distinct people. Repeat customer rate is **3.06%** (2,924 customers).
- **Referential Integrity:** 100% integrity across orders, order items, products, sellers, payments, and reviews.
- **Geolocation Cleanliness:** 1,000,163 noisy geographic logs successfully consolidated into 19,011 zip codes.
