# Enterprise DAX Measures Library

**Project:** Customer Retention & Revenue Intelligence Platform  
**Target:** Power BI Model Calculations  

---

## 1. Core Financial & Volume Measures

```dax
-- Total Orders
Total Orders = 
DISTINCTCOUNT(fact_orders[order_id])

-- Completed Orders (Excluding Cancellations)
Completed Orders = 
CALCULATE(
    [Total Orders],
    fact_orders[order_status] <> "canceled"
)

-- Total Gross Merchandise Value (GMV)
Total GMV = 
SUM(fact_order_items[price])

-- Total Freight Value
Total Freight = 
SUM(fact_order_items[freight_value])

-- Total Platform Revenue
Total Revenue = 
SUM(fact_orders[total_order_value])

-- Average Order Value (AOV)
Average Order Value = 
DIVIDE([Total Revenue], [Completed Orders], 0)

-- Total Items Sold
Total Items Sold = 
COUNT(fact_order_items[order_item_id])

-- Average Items Per Order
Items Per Order = 
DIVIDE([Total Items Sold], [Completed Orders], 0)
```

---

## 2. Customer Retention & Lifecycle Measures

```dax
-- Total Unique Customers (Natural Entities)
Total Unique Customers = 
DISTINCTCOUNT(dim_customers[customer_unique_id])

-- Repeat Customers (Customers with > 1 completed order)
Repeat Customers = 
CALCULATE(
    DISTINCTCOUNT(dim_customers[customer_unique_id]),
    dim_customers[customer_type] = "Repeat Customer"
)

-- One-Time Customers
One-Time Customers = 
CALCULATE(
    DISTINCTCOUNT(dim_customers[customer_unique_id]),
    dim_customers[customer_type] = "One-Time Customer"
)

-- Repeat Purchase Rate (%)
Repeat Purchase Rate % = 
DIVIDE([Repeat Customers], [Total Unique Customers], 0) * 100

-- Revenue from Repeat Customers
Repeat Customer Revenue = 
CALCULATE(
    [Total Revenue],
    dim_customers[customer_type] = "Repeat Customer"
)

-- Repeat Revenue Contribution Share (%)
Repeat Revenue Share % = 
DIVIDE([Repeat Customer Revenue], [Total Revenue], 0) * 100

-- Customer Lifetime Value (Observed Average CLTV)
Customer Lifetime Value = 
DIVIDE([Total Revenue], [Total Unique Customers], 0)
```

---

## 3. Logistics & Delivery Performance Measures

```dax
-- Delivered Orders Count
Delivered Orders = 
CALCULATE(
    [Total Orders],
    fact_orders[order_status] = "delivered"
)

-- Late Delivery Orders Count
Late Delivered Orders = 
CALCULATE(
    [Total Orders],
    fact_orders[order_status] = "delivered",
    fact_orders[is_late_delivery] = TRUE()
)

-- On-Time Delivered Orders Count
On-Time Delivered Orders = 
[Delivered Orders] - [Late Delivered Orders]

-- Late Delivery Rate (%)
Late Delivery Rate % = 
DIVIDE([Late Delivered Orders], [Delivered Orders], 0) * 100

-- On-Time Delivery Rate (SLA %)
On-Time Delivery SLA % = 
DIVIDE([On-Time Delivered Orders], [Delivered Orders], 0) * 100

-- Average Actual Delivery Duration (Days)
Average Delivery Days = 
AVERAGE(fact_orders[actual_delivery_days])

-- Average Estimated Delivery Duration (Days)
Average Estimated Days = 
AVERAGE(fact_orders[estimated_delivery_days])
```

---

## 4. Customer Review & Satisfaction Measures

```dax
-- Average Customer Review Score
Average Review Score = 
AVERAGE(fact_reviews[review_score])

-- Average Review Score for On-Time Deliveries
Review Score (On-Time) = 
CALCULATE(
    [Average Review Score],
    fact_orders[is_late_delivery] = FALSE()
)

-- Average Review Score for Late Deliveries
Review Score (Late) = 
CALCULATE(
    [Average Review Score],
    fact_orders[is_late_delivery] = TRUE()
)

-- Satisfaction Impact (Score Drop from Late Delivery)
Satisfaction Drop from Delay = 
[Review Score (On-Time)] - [Review Score (Late)]

-- 5-Star Reviews Percentage (%)
5 Star Review Pct % = 
DIVIDE(
    CALCULATE(COUNT(fact_reviews[review_id]), fact_reviews[review_score] = 5),
    COUNT(fact_reviews[review_id]),
    0
) * 100

-- 1-Star Reviews Percentage (%)
1 Star Review Pct % = 
DIVIDE(
    CALCULATE(COUNT(fact_reviews[review_id]), fact_reviews[review_score] = 1),
    COUNT(fact_reviews[review_id]),
    0
) * 100
```

---

## 5. Time Intelligence & Growth Measures

```dax
-- Previous Month Revenue
Revenue PM = 
CALCULATE(
    [Total Revenue],
    DATEADD(dim_date[Date], -1, MONTH)
)

-- Month-over-Month Revenue Growth (%)
MoM Revenue Growth % = 
DIVIDE([Total Revenue] - [Revenue PM], [Revenue PM], 0) * 100

-- Cumulative YTD Revenue
YTD Revenue = 
TOTALYTD([Total Revenue], dim_date[Date])
```
