# Project Execution & Reproduction Guide

**Platform:** Customer Retention & Revenue Intelligence Platform  
**Environment:** Windows (PowerShell) / Python 3.13.2 / PostgreSQL 18  

---

## 1. Environment Activation

Open PowerShell in the project workspace:

```powershell
cd "c:\Users\HARSH SHARMA\Desktop\My_GitHub_Repos\Work_In_Progress_Repos\customer-retention-platform"
.\.venv\Scripts\Activate.ps1
```

Verify python path:
```powershell
.\.venv\Scripts\python.exe --version
```

---

## 2. Environment Variables Configuration

Copy `.env.example` to `.env` and insert your local PostgreSQL password:

```powershell
Copy-Item .env.example .env
```

Edit `.env`:
```ini
DB_HOST=localhost
DB_PORT=5432
DB_NAME=customer_retention_db
DB_USER=postgres
DB_PASSWORD=your_actual_postgres_password
```

---

## 3. Executing the End-to-End Pipeline

### Step 3.1: Data Cleaning & Feature Engineering
Processes all 9 raw datasets, cleans geolocation, parses timestamps, and builds analytical marts:

```powershell
.\.venv\Scripts\python.exe python/etl/clean_data.py
```

### Step 3.2: Export Power BI Star Schema
Extracts dimensional and fact tables into `powerbi/exports/`:

```powershell
.\.venv\Scripts\python.exe powerbi/dashboard/generate_powerbi_data.py
```

### Step 3.3: Generate Executive Excel Business Report
Builds the 8-sheet formatted Excel workbook:

```powershell
.\.venv\Scripts\python.exe excel/generate_excel_report.py
```

### Step 3.4: PostgreSQL Ingestion (When Database Password is Set)
Loads all 9 raw CSVs into PostgreSQL:

```powershell
.\.venv\Scripts\python.exe python/etl/load_raw_to_postgres.py
.\.venv\Scripts\python.exe python/etl/verify_database.py
```

---

## 4. Running Automated Tests

Run the full pytest suite:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Bytecode compilation validation:

```powershell
.\.venv\Scripts\python.exe -m compileall python
```
