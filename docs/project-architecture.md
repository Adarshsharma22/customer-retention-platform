# Technical Project Architecture

**Platform:** Customer Retention & Revenue Intelligence Platform  
**Architecture Pattern:** Modern Data Warehouse (Raw -> Cleansed -> Marts -> Serving Layer)  

---

## 1. End-to-End Data Pipeline Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                          1. INGESTION LAYER                            │
│  data/raw/*.csv (9 Olist Datasets: 1.5M+ Total Records)                │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     2. RELATIONAL WAREHOUSE (DDL)                      │
│  PostgreSQL 18: customer_retention_db                                  │
│  Schema: sql/schema/02_create_complete_schema.sql                      │
│  ETL Ingestion: python/etl/load_raw_to_postgres.py                     │
│  Audit: python/etl/verify_database.py                                  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                 3. DATA CLEANING & TRANSFORMATION                      │
│  Script: python/etl/clean_data.py                                      │
│  - Geolocation median coordinates aggregation (1M -> 19k rows)         │
│  - Timestamp parsing & SLA delay calculation                           │
│  - Missing value imputation & English category normalization           │
│  Output Cleaned: data/cleaned/*.csv                                    │
│  Output Marts:   data/processed/*.csv                                  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
               ┌────────────────────┴────────────────────┐
               ▼                                         ▼
┌───────────────────────────────┐       ┌───────────────────────────────┐
│     4. ADVANCED ANALYTICS     │       │      5. SQL ANALYTIC MARTS    │
│  Python Modules:              │       │  12 Production Queries:       │
│  - python/analysis/           │       │  sql/queries/01_to_12.sql     │
│  Jupyter Notebooks:           │       │  4 Relational Views:          │
│  - 06_exploratory_data.ipynb  │       │  sql/views/01_to_04.sql       │
│  - 07_retention_cohorts.ipynb │       └───────────────┬───────────────┘
│  - 08_rfm_segmentation.ipynb  │                       │
└──────────────┬────────────────┘                       │
               │                                        │
               └────────────────────┬───────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        6. SERVING & PRESENTATION                       │
│  - Power BI Desktop: Star Schema (powerbi/exports/) & DAX measures     │
│  - Executive Excel Report: excel/customer_retention_business_report.xlsx│
│  - Markdown Reporting: docs/business-insights.md                       │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Component Design Principles

1. **Idempotence & Safety:** Ingestion and cleaning pipelines can be executed repeatedly without generating duplicate records or destroying data.
2. **Defensive Processing:** Missing categories and dimensional measurements are imputed with statistical medians to prevent catalog records from being dropped.
3. **Data Integrity:** Primary keys, composite keys, and foreign keys are strictly validated. Geolocation deduplication preserves spatial fidelity by computing median geographic centroids.
4. **Modularity:** Separate packages for database configuration (`python/config/`), data engineering (`python/etl/`), quality validation (`python/validation/`), and business algorithms (`python/analysis/`).
