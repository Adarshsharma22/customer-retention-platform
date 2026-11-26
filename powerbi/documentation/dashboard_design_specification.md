# Power BI Dashboard Design Specification & Theme Guide

**Project:** Customer Retention & Revenue Intelligence Platform  
**Target Resolution:** 1920 × 1080 (16:9 Standard Presentation Canvas)  
**Theme Support:** Default Theme, Light Theme, and Dark Theme  

---

## 1. Theme Color Palettes (Default, Light, Dark)

To comply with enterprise design standards and accessibility guidelines, the dashboard supports three distinct aesthetic themes:

### A. Default Theme (Balanced Modern Corporate Blue)
- **Background:** `#F4F7FC`
- **Card / Surface Container:** `#FFFFFF`
- **Border / Divider:** `#E2E8F0`
- **Primary Text:** `#1E293B`
- **Secondary Text:** `#64748B`
- **Primary Accent / Brand:** `#2563EB` (Royal Blue)
- **Secondary Accent:** `#0D9488` (Teal)
- **Warning / Delay Accent:** `#DC2626` (Crimson)
- **Success / On-Time:** `#16A34A` (Emerald)

### B. Light Theme (Clean Minimalist Editorial)
- **Background:** `#FAFAFA`
- **Card / Surface Container:** `#FFFFFF`
- **Border / Divider:** `#E5E7EB`
- **Primary Text:** `#111827`
- **Secondary Text:** `#6B7280`
- **Primary Accent:** `#3B82F6` (Sky Corporate Blue)
- **Secondary Accent:** `#10B981` (Mint Green)
- **Warning / Alert:** `#EF4444` (Coral Red)

### C. Dark Theme (High-Contrast Executive Command Center)
- **Background:** `#0F172A` (Deep Slate Navy)
- **Card / Surface Container:** `#1E293B` (Midnight Blue Container)
- **Border / Divider:** `#334155`
- **Primary Text:** `#F8FAFC` (Pure Off-White)
- **Secondary Text:** `#94A3B8` (Muted Slate)
- **Primary Accent:** `#60A5FA` (Luminous Blue)
- **Secondary Accent:** `#34D399` (Neon Mint)
- **Warning / Alert:** `#F87171` (Vibrant Coral)

---

## 2. Multi-Page Dashboard Architecture

### PAGE 1: EXECUTIVE REVENUE & SALES OVERVIEW
- **Top KPI Strip (6 Cards):**
  1. `Total Revenue` (R$ 15.84M)
  2. `Total Orders` (99.4K)
  3. `Total Customers` (96.1K)
  4. `Repeat Purchase Rate` (3.12%)
  5. `Average Order Value (AOV)` (R$ 159.85)
  6. `Average Review Score` (4.09 ★)
- **Visual 1 (Area & Column Combo):** Monthly Revenue and Order Volume Trend (2017–2018).
- **Visual 2 (Horizontal Bar Chart):** Top 10 Product Categories by Revenue Contribution.
- **Visual 3 (Donut Chart):** Customer Share by Type (One-Time: 96.9% vs Repeat: 3.1%).
- **Visual 4 (Filled Map / Bar Chart):** Top Revenue Contributing States (SP, RJ, MG, RS, PR).
- **Global Slicers:** Date Range Slider, Order Status, Customer State.

### PAGE 2: CUSTOMER RETENTION & COHORT ANALYSIS
- **Top KPI Cards:**
  1. `Repeat Customer Spend` (R$ 967K, 6.1% of GMV)
  2. `Spend Multiplier` (2.05x higher spend from repeat shoppers)
  3. `Average Retention Rate` (0.5% – 0.8% Month 1 return)
- **Visual 1 (Heatmap Matrix):** Monthly Cohort Retention Matrix (Cohorts Jan 2017 – Dec 2017 over Month 0 to Month 12).
- **Visual 2 (Stacked Bar Chart):** Monthly Revenue Breakdown: First-time vs Returning Shopper Contribution.
- **Visual 3 (Histogram / Bar):** Customer Order Frequency Distribution (1 order, 2 orders, 3 orders, 4+ orders).

### PAGE 3: CUSTOMER SEGMENTATION (RFM)
- **Top KPI Cards:**
  1. `Champions Count` (High Recency, High Frequency, High Monetary)
  2. `At-Risk Customers`
  3. `Hibernating High Spenders`
- **Visual 1 (Treemap / Donut):** Customer Distribution across 7 RFM Segments.
- **Visual 2 (Clustered Column Chart):** Average Monetary Spend (R$) and Recency Days per Segment.
- **Visual 3 (Scatter Plot):** Recency (Days) vs Monetary Spend (R$) colored by Customer Segment.

### PAGE 4: PRODUCT & SELLER PERFORMANCE
- **Top KPI Cards:**
  1. `Active Sellers Count` (3,095)
  2. `Active Categories` (74)
  3. `Top 20% Category Revenue Share` (83.2% - Strong Pareto Concentration)
- **Visual 1 (Pareto Chart):** Cumulative Revenue % curve over Product Categories.
- **Visual 2 (Matrix Table):** Top 25 Sellers ranked by Total GMV, Items Sold, Average Delivery Delay, and Review Score.
- **Visual 3 (Bar Chart):** Average Freight Cost by Category and Customer Region.

### PAGE 5: DELIVERY LOGISTICS & SATISFACTION SLA
- **Top KPI Cards:**
  1. `On-Time Delivery SLA %` (92.1%)
  2. `Late Delivery Rate %` (7.9%)
  3. `Average Delivery Days` (12.5 Days)
  4. `Satisfaction Drop from Delay` (-1.78 Rating Points: 4.23 on-time vs 2.45 late)
- **Visual 1 (Box Plot / Column):** Customer Review Score Distribution for On-Time vs. Late Shipments.
- **Visual 2 (Horizontal Bar Chart):** Average Delivery Duration and Late Rate % by Customer State.
- **Visual 3 (Scatter Plot):** Carrier Delay (Days) vs Review Score (Showing precipitous rating collapse beyond Day 0).

---

## 3. Power BI Desktop Import Instructions

1. Open **Power BI Desktop**.
2. Click **Get Data** -> **Folder** or **Text/CSV**.
3. Select files from `powerbi/exports/`:
   - `dim_date.csv`
   - `dim_customers.csv`
   - `dim_products.csv`
   - `dim_sellers.csv`
   - `dim_geolocation.csv`
   - `fact_orders.csv`
   - `fact_order_items.csv`
   - `fact_payments.csv`
   - `fact_reviews.csv`
4. Switch to **Model View** and verify relationships match `data_model_architecture.md`.
5. Create a new measure table `_Measures` and paste DAX formulas from `dax_measures.md`.
6. Apply theme JSON or select Canvas Theme (Default / Light / Dark) and assemble dashboard pages.
