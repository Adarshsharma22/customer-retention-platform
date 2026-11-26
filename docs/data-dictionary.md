# Data Dictionary

## Project
Customer Retention & Revenue Intelligence Platform

## Dataset
Olist Brazilian E-Commerce Public Dataset

## Purpose
This document describes all tables, columns, relationships, and business meanings used in this project.

---

## 1. Tables : customers

Contains information about customer accounts and addresses.

| Column | Data Type | Key | Nullable | Description | Example |
|---|---|---|---|---|---|
| `customer_id` | VARCHAR(50) | PK | No | Unique order-level customer identifier | `06b8999e2fba1a1fbc88172c00ba8bc7` |
| `customer_unique_id` | VARCHAR(50) | - | No | Identifies the same natural person across multiple orders | `861eff4711a542e4b93843c6dd7febb0` |
| `customer_zip_code_prefix` | INTEGER | - | No | Customer ZIP code prefix | `14409` |
| `customer_city` | VARCHAR(100)| - | No | Customer city | `Franca` |
| `customer_state` | VARCHAR(5) | - | No | Customer state code | `SP` |

### Business Notes
- One customer (`customer_unique_id`) can place multiple orders under different `customer_id` tokens.
- `customer_unique_id` is the primary key used to evaluate customer retention and RFM segmentation.

---

## 2. Tables : orders

Contains order lifecycle timestamps and status.

| Column | Data Type | Key | Nullable | Description | Example |
|---|---|---|---|---|---|
| `order_id` | VARCHAR(50) | PK | No | Unique order identifier | `e481f51cbdc54678b7cc49136f2d6af7` |
| `customer_id` | VARCHAR(50) | FK | No | Foreign key linking to customers table | `9ef432eb6251297304e76186b10a928d` |
| `order_status` | VARCHAR(30) | - | No | Status (`delivered`, `canceled`, `shipped`, etc.) | `delivered` |
| `order_purchase_timestamp` | TIMESTAMP | - | No | Purchase date and time | `2017-10-02 10:56:33` |
| `order_approved_at` | TIMESTAMP | - | Yes | Payment approval date and time | `2017-10-02 11:07:15` |
| `order_delivered_carrier_date`| TIMESTAMP | - | Yes | Date handed to carrier | `2017-10-04 19:55:00` |
| `order_delivered_customer_date`| TIMESTAMP| - | Yes | Actual customer delivery date | `2017-10-10 21:25:13` |
| `order_estimated_delivery_date`| TIMESTAMP| - | No | Estimated promised delivery date | `2017-10-18 00:00:00` |

---

## 3. Tables : order_items

Contains individual items purchased within each order.

| Column | Data Type | Key | Nullable | Description | Example |
|---|---|---|---|---|---|
| `order_id` | VARCHAR(50) | PK, FK | No | Order identifier | `e481f51cbdc54678b7cc49136f2d6af7` |
| `order_item_id` | INTEGER | PK | No | Sequential item number within order (1, 2, 3...) | `1` |
| `product_id` | VARCHAR(50) | FK | No | Product identifier | `87285b34884572b28435b583ee077680` |
| `seller_id` | VARCHAR(50) | FK | No | Seller identifier | `3504c0c97129e577c16463cd9c92869c` |
| `shipping_limit_date` | TIMESTAMP | - | No | Seller fulfillment shipping deadline | `2017-10-06 11:07:15` |
| `price` | NUMERIC(10,2)| - | No | Item item price in BRL | `29.99` |
| `freight_value` | NUMERIC(10,2)| - | No | Item shipping cost in BRL | `8.72` |

---

## 4. Tables : products

Catalog attributes for products.

| Column | Data Type | Key | Nullable | Description | Example |
|---|---|---|---|---|---|
| `product_id` | VARCHAR(50) | PK | No | Unique product identifier | `1e9e8ef04dbcff4541ed26657ea517e5` |
| `product_category_name` | VARCHAR(150)| - | Yes | Portuguese category name | `perfumaria` |
| `product_name_lenght` | INTEGER | - | Yes | Product title character length | `40` |
| `product_description_lenght` | INTEGER | - | Yes | Product description character length | `287` |
| `product_photos_qty` | INTEGER | - | Yes | Number of product photos | `1` |
| `product_weight_g` | NUMERIC(10,2)| - | Yes | Weight in grams | `225.0` |
| `product_length_cm` | NUMERIC(10,2)| - | Yes | Length in centimeters | `16.0` |
| `product_height_cm` | NUMERIC(10,2)| - | Yes | Height in centimeters | `10.0` |
| `product_width_cm` | NUMERIC(10,2)| - | Yes | Width in centimeters | `14.0` |

---

## 5. Tables : payments

Customer transaction payment methods and values.

| Column | Data Type | Key | Nullable | Description | Example |
|---|---|---|---|---|---|
| `order_id` | VARCHAR(50) | PK, FK | No | Order identifier | `e481f51cbdc54678b7cc49136f2d6af7` |
| `payment_sequential` | INTEGER | PK | No | Sequence number for split payments | `1` |
| `payment_type` | VARCHAR(50) | - | No | Method (`credit_card`, `boleto`, `voucher`, `debit_card`) | `credit_card` |
| `payment_installments`| INTEGER | - | No | Number of installment payments | `1` |
| `payment_value` | NUMERIC(10,2)| - | No | Total amount paid in BRL | `18.12` |

---

## 6. Tables : reviews

Customer feedback and review ratings.

| Column | Data Type | Key | Nullable | Description | Example |
|---|---|---|---|---|---|
| `review_id` | VARCHAR(50) | - | No | Unique review identifier | `a54f0611dd941cc31a16d9a7de3a37cd` |
| `order_id` | VARCHAR(50) | FK | No | Order identifier | `e481f51cbdc54678b7cc49136f2d6af7` |
| `review_score` | INTEGER | - | No | Rating from 1 (lowest) to 5 (highest) | `5` |
| `review_comment_title` | TEXT | - | Yes | Review title header | `Recomendo` |
| `review_comment_message`| TEXT | - | Yes | Written review body text | `Muito bom produto!` |
| `review_creation_date` | TIMESTAMP | - | No | Date survey was sent | `2017-10-11 00:00:00` |
| `review_answer_timestamp`| TIMESTAMP| - | No | Date customer submitted answer | `2017-10-12 10:22:05` |

---

## 7. Tables : sellers

Registered merchant information.

| Column | Data Type | Key | Nullable | Description | Example |
|---|---|---|---|---|---|
| `seller_id` | VARCHAR(50) | PK | No | Unique seller identifier | `3504c0c97129e577c16463cd9c92869c` |
| `seller_zip_code_prefix`| INTEGER | - | No | Seller location ZIP code prefix | `13075` |
| `seller_city` | VARCHAR(100)| - | No | Seller city | `Campinas` |
| `seller_state` | VARCHAR(5) | - | No | Seller state code | `SP` |

---

## 8. Tables : geolocation

Geographic coordinates for Brazilian ZIP code prefixes.

| Column | Data Type | Key | Nullable | Description | Example |
|---|---|---|---|---|---|
| `geolocation_zip_code_prefix` | INTEGER | PK | No | Brazilian ZIP code prefix | `01001` |
| `geolocation_lat` | NUMERIC(12,8)| - | No | Median latitude coordinate | `-23.549292` |
| `geolocation_lng` | NUMERIC(12,8)| - | No | Median longitude coordinate | `-46.633559` |
| `geolocation_city` | VARCHAR(100)| - | No | Consolidated city name | `Sao Paulo` |
| `geolocation_state` | VARCHAR(5) | - | No | Consolidated state code | `SP` |

---

## 9. Tables : category_translation

Bilingual lookup mapping Portuguese category names to English.

| Column | Data Type | Key | Nullable | Description | Example |
|---|---|---|---|---|---|
| `product_category_name` | VARCHAR(150)| PK | No | Category name in Portuguese | `cama_mesa_banho` |
| `product_category_name_english`| VARCHAR(150)| - | No | Standard English translation | `bed_bath_table` |
