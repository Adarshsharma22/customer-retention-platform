# Data Dictionary

## Project

Customer Retention & Revenue Intelligence Platform

## Dataset

Olist Brazilian E-Commerce Public Dataset

## Purpose

This document describes all tables, columns, relationships, and business meanings used in this project.


## Tables : customers

## Description

Contains information about customers who placed orders.

| Column | Data Type | Key | Nullable | Description | Example |
|----------|-----------|-----|----------|-------------|---------|
| customer_id | VARCHAR | PK | No | Unique identifier for each customer record | 06b8999e2fba1a1fbc88172c00ba8bc7 |
| customer_unique_id | VARCHAR | - | No | Identifies the same customer across multiple orders | 861eff4711a542e4b93843c6dd7febb0 |
| customer_zip_code_prefix | INTEGER | - | No | Customer ZIP code prefix | 14409 |
| customer_city | VARCHAR | - | No | Customer city | Franca |
| customer_state | VARCHAR | - | No | Customer state | SP |

### Business Notes

- One customer can place multiple orders.
- `customer_id` links to the Orders table.
- `customer_unique_id` identifies returning customers.


## Tables : orders

## Description

Contains order lifecycle information.

| Column | Data Type | Key | Nullable | Description | Example |
|----------|-----------|-----|----------|-------------|---------|
| order_id | VARCHAR | PK | No | Unique order identifier | e481f51cbdc54678b7cc49136f2d6af7 |
| customer_id | VARCHAR | FK | No | Customer who placed the order | 9ef432eb6251297304e76186b10a928d |
| order_status | VARCHAR | - | No | Current status of the order | delivered |
| order_purchase_timestamp | TIMESTAMP | - | No | Purchase date and time | 2017-10-02 10:56:33 |
| order_approved_at | TIMESTAMP | - | Yes | Approval time | 2017-10-02 11:07:15 |
| order_delivered_carrier_date | TIMESTAMP | - | Yes | Handed to carrier | 2017-10-04 19:55:00 |
| order_delivered_customer_date | TIMESTAMP | - | Yes | Delivered to customer | 2017-10-10 21:25:13 |
| order_estimated_delivery_date | TIMESTAMP | - | No | Estimated delivery date | 2017-10-18 |

### Business Notes

- Each order belongs to one customer.
- Orders connect to payments, reviews, and order items.


## Tables : order_items

## Description

Contains information about the items in an order.


| Column | Data Type | Key | Nullable | Description | Example |
|----------|-----------|-----|----------|-------------|---------|
| order_id | VARCHAR | PK | No | Unique identifier for each order record | e481f51cbdc54678b7cc49136f2d6af7 |
| order_item_id | VARCHAR | PK | No | Unique identifier for each order item record | e481f51cbdc54678b7cc49136f2d6af7 |
| product_id | VARCHAR | FK | No | Unique identifier for each product record | e481f51cbdc54678b7cc49136f2d6af7 |
| seller_id | VARCHAR | FK | No | Unique identifier for each seller record | e481f51cbdc54678b7cc49136f2d6af7 |
| shipping_limit_date | TIMESTAMP | - | No | Shipping limit date | 2017-10-02 10:56:33 |
| price | DECIMAL | - | No | Price of the item | 10.99 |
| freight_value | DECIMAL | - | No | Freight value of the item | 0.99 |


### Business Notes

- One order can contain multiple items.

## Tables : products

## Description

Contains information about products.

| Column | Data Type | Key | Nullable | Description | Example |
|----------|-----------|-----|----------|-------------|---------|
| product_id | VARCHAR | PK | No | Unique identifier for each product record | e481f51cbdc54678b7cc49136f2d6af7 |
| product_category_name | VARCHAR | - | No | Product category name | electronics |
| product_name_length | INTEGER | - | No | Product name length | 10 |
| product_description_length | INTEGER | - | No | Product description length | 100 |
| product_photos_qty | INTEGER | - | No | Number of product photos | 1 |
| product_weight_g | DECIMAL | - | No | Product weight | 0.5 |
| product_height_cm | DECIMAL | - | No | Product height | 0.5 |
| product_width_cm | DECIMAL | - | No | Product width | 0.5 |

### Business Notes

- One product can be in multiple categories.
- One product can have multiple photos.


## Tables : payments

## Description

Contains information about payments.

| Column | Data Type | Key | Nullable | Description | Example |
|----------|-----------|-----|----------|-------------|---------|
| order_id | VARCHAR | PK | No | Unique identifier for each payment record | e481f51cbdc54678b7cc49136f2d6af7 |
| payment_sequential | INTEGER | - | No | Sequential number for each payment record | 1 |
| payment_type | VARCHAR | - | No | Type of payment | cash |
| payment_installments | INTEGER | - | No | Number of installments | 1 |
| paymeny_value | DECIMAL | - | No | Payment value | 10.99 |


### Business Notes

- One payment belongs to one order.


## Tables : reviews

## Description

Contains information about reviews.

| Column | Data Type | Key | Nullable | Description | Example |
|----------|-----------|-----|----------|-------------|---------|
| review_id | VARCHAR | PK | No | Unique identifier for each review record | e481f51cbdc54678b7cc49136f2d6af7 |
| order_id | VARCHAR | FK | No | Unique identifier for each order record | e481f51cbdc54678b7cc49136f2d6af7 |
| review_score | INTEGER | - | No | Review score | 5 |
| review_comment_title | VARCHAR | - | No | Review comment title | Excellent |
| review_comment_message | VARCHAR | - | No | Review comment message | I loved it!
| review_creation_date | TIMESTAMP | - | No | Review creation date | 2017-10-02 10:56:33 |
| review_answer_timestamp | TIMESTAMP | - | No | Review answer timestamp | 2017-10-02 11:07:15 |

### Business Notes

- One review belongs to one order.


## Tables : sellers

## Description

Contains information about sellers.

| Column | Data Type | Key | Nullable | Description | Example |
|----------|-----------|-----|----------|-------------|---------|
| seller_id | VARCHAR | PK | No | Unique identifier for each seller record | e481f51cbdc54678b7cc49136f2d6af7 |
| seller_zip_code_prefix | INTEGER | - | No | Seller ZIP code prefix | 14409 |
| seller_city | VARCHAR | - | No | Seller city | Franca |
| seller_state | VARCHAR | - | No | Seller state | SP |

### Business Notes

- One seller can sell multiple products.
- `seller_id` links to the Products table.


## Tables : geolocations

## Description

Contains information about geolocations.

| Column | Data Type | Key | Nullable | Description | Example |
|----------|-----------|-----|----------|-------------|---------|
| geolocation_zip_code_prefix | INTEGER | - | No | ZIP code prefix | 14409 |
| geolocation_lat | DECIMAL | - | No | Latitude | 10.99 |
| geolocation_lng | DECIMAL | - | No | Longitude | 10.99 |
| geolocation_city | VARCHAR | - | No | City | Franca |
| geolocation_state | VARCHAR | - | No | State | SP |

### Business Notes

- One geolocation can have multiple products.


## Tables : category_translation

## Description

Contains information about category translations.

| Column | Data Type | Key | Nullable | Description | Example |
|----------|-----------|-----|----------|-------------|---------|
| product_category_name | VARCHAR | PK | No | Product category name | electronics |
| product_category_name_english | VARCHAR | - | No | Product category name in English | electronics |

### Business Notes

- One product category can have multiple translations.


# Table Relationships

customers
│
└── customer_id
      │
      ▼
orders
│
├── order_items
├── payments
└── reviews

order_items
│
├── products
└── sellers



# Business Rules

- One customer can place multiple orders.
- One order can contain multiple products.
- One seller can sell many products.
- One order may have multiple payment records.
- Each order can have at most one review.
- Customer lifetime value is calculated from total order value.


# Data Quality Notes

Potential issues to investigate:

- Missing delivery dates
- Missing product dimensions
- Duplicate customer records
- Null review comments
- Inconsistent payment installments


