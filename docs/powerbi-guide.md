# Power BI Implementation & User Guide

**Project:** Customer Retention & Revenue Intelligence Platform  
**Target Application:** Power BI Desktop  

---

## 1. Quick Start & Model Ingestion

1. Launch **Power BI Desktop**.
2. Click **Get Data** -> **Folder** (or Text/CSV) and select:
   `c:\Users\HARSH SHARMA\Desktop\My_GitHub_Repos\Work_In_Progress_Repos\customer-retention-platform\powerbi\exports`
3. Load the 9 core tables:
   - `dim_date.csv`
   - `dim_customers.csv`
   - `dim_products.csv`
   - `dim_sellers.csv`
   - `dim_geolocation.csv`
   - `fact_orders.csv`
   - `fact_order_items.csv`
   - `fact_payments.csv`
   - `fact_reviews.csv`
4. In **Model View**, verify relationships connect as documented in `powerbi/documentation/data_model_architecture.md`.

---

## 2. DAX Calculations Setup

Create a new table named `_Measures` and copy all 20+ formulas provided in:
`powerbi/documentation/dax_measures.md`

Key DAX measures to highlight:
- `[Total Revenue]`
- `[Repeat Purchase Rate %]`
- `[Average Order Value]`
- `[Late Delivery Rate %]`
- `[Satisfaction Drop from Delay]`

---

## 3. Theme Customization

To ensure accessibility and professional executive presentation, follow the color specifications in `powerbi/documentation/dashboard_design_specification.md`:
- **Default Theme:** Modern Corporate Blue (`#2563EB`) with clean white surfaces.
- **Light Theme:** Minimalist Editorial (`#FAFAFA` background, `#3B82F6` accents).
- **Dark Theme:** Executive Command Center (`#0F172A` deep navy background, `#1E293B` cards).
