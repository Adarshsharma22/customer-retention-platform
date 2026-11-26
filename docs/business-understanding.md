# Business Understanding & Strategic Problem Framing

**Project:** Customer Retention & Revenue Intelligence Platform  
**Target Enterprise Context:** Brazilian E-Commerce Marketplace (Olist)  
**Role:** Senior Data Analyst & Technical Project Manager  

---

## 1. Executive Context

E-commerce marketplaces face intense competition, escalating Customer Acquisition Costs (CAC), and dynamic logistics challenges across large geographic markets like Brazil. 

In traditional transaction-driven business models, companies often over-index on acquisition while neglecting customer retention, post-purchase experience, and fulfillment reliability.

---

## 2. Core Business Problems

### 2.1 The Customer Retention Deficit
- **Observation:** In the analyzed 100k-order marketplace history, **only 3.12% of unique customers place more than one order**.
- **Business Impact:** The business operates almost entirely on single-transaction shoppers, creating high vulnerability to rising marketing acquisition expenses.
- **Objective:** Quantify the monetary uplift of repeat purchasers and establish behavioral segmentation to trigger proactive re-engagement campaigns.

### 2.2 Logistics Friction & Customer Satisfaction
- **Observation:** Average delivery duration is **12.5 days**, with cross-state shipments experiencing significant transit variance. **7.9% of deliveries arrive past the promised estimated date**.
- **Business Impact:** Late deliveries cause a severe **1.78 rating drop** (from an average of 4.23 down to 2.45 stars), driving customer churn and damaging seller credibility.
- **Objective:** Map delivery SLAs across Brazilian states to identify regional fulfillment bottlenecks and root causes of delayed shipments.

### 2.3 Catalog & Revenue Concentration (Pareto Dynamics)
- **Observation:** Over **83% of platform revenue originates from fewer than 20% of product categories** (led by Bed/Bath/Table, Health/Beauty, Computer Accessories, and Furniture).
- **Business Impact:** High category concentration exposes the marketplace to supply disruptions, while long-tail categories generate insufficient velocity.
- **Objective:** Measure category contribution, average order margins, and seller fulfillment metrics to optimize marketplace merchandising.

---

## 3. Key Stakeholders & Strategic Objectives

| Stakeholder Persona | Strategic Business Need | Platform Deliverable |
|---|---|---|
| **Chief Commercial Officer (CCO)** | Overall Gross Merchandise Value (GMV), revenue growth trends, and cohort lifetime value. | Executive Dashboard (Power BI Page 1 & Excel Summary) |
| **Head of Growth & CRM** | RFM segment distributions, repeat purchase rates, and win-back campaign targeting. | Customer Retention & RFM Analysis (Notebook 07 & 08, SQL 06) |
| **Director of Logistics** | Carrier performance, transit delay correlations, and state-level delivery breaches. | Logistics & Satisfaction SLA Engine (SQL 10 & 11, Power BI Page 5) |
| **Category Managers** | Sales velocity, freight-to-price ratios, and seller fulfillment rankings. | Category & Seller Marts (SQL 08 & 09, Power BI Page 4) |
