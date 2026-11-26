# Customer Retention & Revenue Intelligence Platform

[![Python 3.13](https://img.shields.io/badge/Python-3.13.2-blue.svg)](https://www.python.org/)
[![PostgreSQL 18](https://img.shields.io/badge/PostgreSQL-18-336791.svg)](https://www.postgresql.org/)
[![Tests Passing](https://img.shields.io/badge/Tests-21%20Passed-brightgreen.svg)]()
[![Dataset](https://img.shields.io/badge/Dataset-Olist%20E--Commerce-orange.svg)]()

> A production-grade Data Analytics and Business Intelligence portfolio project simulating the work of a Senior Data Analyst at a major Brazilian e-commerce marketplace.

---

## 1. Project Overview & Business Problem

In high-growth e-commerce marketplaces, customer acquisition is costly, yet businesses often suffer from a severe **Retention Deficit**. 

Analyzing **99,441 real-world e-commerce orders** from the Olist public dataset revealed:
- **96.88% of customers are one-time shoppers.**
- **Only 3.12% of customers return to place a 2nd order.**
- Repeat customers spend **2.05x more** per order than one-time shoppers, contributing **6.1% of revenue (R$ 967K)** despite their tiny share.
- Late delivery is the **#1 driver of customer dissatisfaction**, causing an immediate **1.78 rating drop** (from 4.23 down to 2.45 stars).

This platform provides an end-to-end data intelligence solution: from automated PostgreSQL ETL and reproducible Pandas cleaning to advanced SQL cohort modeling, RFM customer segmentation, an 8-sheet corporate Excel workbook, and interactive Power BI dashboards.

---

## 2. Technology Stack

- **Relational Data Warehouse:** PostgreSQL 18, SQLAlchemy 2.0.51, psycopg2-binary 2.9.12
- **Data Engineering & ETL:** Python 3.13.2, Pandas 2.3.3, NumPy 2.3.5
- **Analytics & Data Science:** Matplotlib 3.10.0, Seaborn 0.13.2, Plotly 6.8.0, JupyterLab
- **Business Intelligence & Reporting:** Power BI Desktop, Microsoft Excel (`openpyxl`), Markdown
- **Testing & Quality Assurance:** `pytest 9.2.0`, `DataValidator` suite

---

## 3. End-to-End Architecture

```
[Raw Olist CSVs (9 Datasets / 1.5M+ rows)]
                     │
                     ▼
[Automated ETL Pipeline: load_raw_to_postgres.py]
                     │
                     ▼
[PostgreSQL Relational Warehouse: customer_retention_db]
                     │
                     ├──► [Production SQL Views (01-04) & 12 Analytical Queries]
                     │
                     ▼
[Data Cleansing & Transformation: clean_data.py]
  - Geolocation centroid aggregation (1M -> 19k rows)
  - Date parsing & delivery SLA calculation
  - Missing value imputation
                     │
                     ├──► data/cleaned/*.csv (Cleaned Tables)
                     ├──► data/processed/*.csv (Analytical Marts)
                     │
                     ├──► [Power BI Star Schema (powerbi/exports/)]
                     ├──► [Executive Excel Report: customer_retention_business_report.xlsx]
                     └──► [Jupyter Notebooks: EDA, Cohort Retention, RFM Segments]
```

---

## 4. Key Business Findings

| Domain | Finding | Business Impact | Strategic Recommendation |
|---|---|---|---|
| **Retention** | 3.12% repeat rate; 2.05x spend multiple | High CAC vulnerability; single purchase trap | Implement 30/60/90-day automated replenishment campaigns. |
| **Logistics** | 7.9% late delivery rate; 12.5 days avg delivery | Rating plunges from 4.23 to 2.45 stars on late delivery | Establish regional fulfillment hubs in northeastern Brazil. |
| **RFM Segments**| 18,000+ "Hibernating High Spenders" | Idle capital; high-value churning | Trigger VIP win-back incentives with free shipping credits. |
| **Catalog** | Top 20% categories drive 83% of GMV | Severe catalog concentration risk | Expand supplier base in high-margin growth categories. |

---

## 5. Repository Structure

```
customer-retention-platform/
├── data/
│   ├── raw/                 # Original 9 Olist CSV files
│   ├── cleaned/             # 9 Cleansed datasets
│   └── processed/           # Analytical marts (RFM, orders enriched, cohorts)
├── docs/                    # Full technical documentation suite
│   ├── business-understanding.md
│   ├── project-architecture.md
│   ├── business-insights.md
│   ├── data-dictionary.md
│   ├── data-quality-report.md
│   ├── sql-documentation.md
│   ├── powerbi-guide.md
│   └── project-execution-guide.md
├── excel/
│   ├── customer_retention_business_report.xlsx  # 8-sheet formatted Excel workbook
│   └── generate_excel_report.py
├── notebooks/               # 8 Production Jupyter Notebooks
│   ├── 01_reading_dataset.ipynb
│   ├── 02_dataset_exploration.ipynb
│   ├── 03_data_validation.ipynb
│   ├── 04_data_cleaning.ipynb
│   ├── 05_relationship_validation.ipynb
│   ├── 06_exploratory_data_analysis.ipynb
│   ├── 07_customer_retention_cohorts.ipynb
│   └── 08_rfm_customer_segmentation.ipynb
├── powerbi/
│   ├── dashboard/           # Star schema generator
│   ├── exports/             # Ready-to-import CSV dimension & fact tables
│   └── documentation/       # Data model, DAX library, theme guide (Default, Light, Dark)
├── python/
│   ├── config/              # Centralized db_config.py
│   ├── etl/                 # load_raw_to_postgres.py, clean_data.py, verify_database.py
│   ├── validation/          # data_validator.py
│   └── analysis/            # business_kpis.py, retention_analyzer.py, rfm_segmentation.py
├── sql/
│   ├── schema/              # DDL schema definitions
│   ├── queries/             # 12 Advanced SQL queries (CTEs, Window Functions)
│   └── views/               # 4 Analytical SQL views
├── tests/                   # 21 Automated pytest test cases (100% passing)
├── reports/
│   └── final_project_audit.md
├── requirements.txt
└── README.md
```

---

## 6. Execution Instructions

1. **Clone & Activate Virtual Environment:**
   ```powershell
   git clone https://github.com/Adarshsharma22/customer-retention-platform.git
   cd customer-retention-platform
   .\.venv\Scripts\Activate.ps1
   ```

2. **Configure Database Credentials:**
   Copy `.env.example` to `.env` and set your PostgreSQL password.

3. **Run Cleansing & Analytics Pipeline:**
   ```powershell
   .\.venv\Scripts\python.exe python/etl/clean_data.py
   .\.venv\Scripts\python.exe powerbi/dashboard/generate_powerbi_data.py
   .\.venv\Scripts\python.exe excel/generate_excel_report.py
   ```

4. **Run Ingestion & Verification (with PostgreSQL connected):**
   ```powershell
   .\.venv\Scripts\python.exe python/etl/load_raw_to_postgres.py
   .\.venv\Scripts\python.exe python/etl/verify_database.py
   ```

5. **Run Automated Test Suite:**
   ```powershell
   .\.venv\Scripts\python.exe -m pytest -v
   ```

---

## 7. Power BI Dashboard Preview

The dashboard includes 5 fully designed pages supporting **Default Theme**, **Light Theme**, and **Dark Theme** (see `powerbi/documentation/dashboard_design_specification.md`):
- **Page 1:** Executive Overview (Revenue, Volume, AOV, Review Scores)
- **Page 2:** Customer Retention & Cohort Heatmap Matrix
- **Page 3:** RFM Customer Segmentation & Behavioral Clusters
- **Page 4:** Product & Seller Fulfillment Performance
- **Page 5:** Delivery Logistics SLA & Review Degradation
