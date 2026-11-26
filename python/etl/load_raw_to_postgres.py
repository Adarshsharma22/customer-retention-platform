"""
Automated ETL Ingestion Pipeline for Customer Retention & Revenue Intelligence Platform.
Safely ingests raw Olist CSV datasets into PostgreSQL adhering to referential integrity constraints.
"""

import os
import sys
import time
from typing import Dict, List, Optional
import pandas as pd
import numpy as np
from sqlalchemy import text

# Add project root to sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from python.config.db_config import get_sqlalchemy_engine, get_connection_parameters
from python.utils.logger import get_logger

logger = get_logger("etl_ingestion")

DATA_RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw")

# Import order respecting foreign key dependencies:
# 1. customers, products, sellers, category_translation, geolocation (independent)
# 2. orders (depends on customers)
# 3. order_items (depends on orders, products, sellers)
# 4. payments (depends on orders)
# 5. reviews (depends on orders)
TABLE_IMPORT_SPECS = [
    {
        "table_name": "customers",
        "file_name": "customers.csv",
        "expected_columns": [
            "customer_id", "customer_unique_id", "customer_zip_code_prefix",
            "customer_city", "customer_state"
        ],
        "date_columns": [],
        "chunk_size": 25000
    },
    {
        "table_name": "products",
        "file_name": "products.csv",
        "expected_columns": [
            "product_id", "product_category_name", "product_name_lenght",
            "product_description_lenght", "product_photos_qty", "product_weight_g",
            "product_length_cm", "product_height_cm", "product_width_cm"
        ],
        "date_columns": [],
        "chunk_size": 15000
    },
    {
        "table_name": "sellers",
        "file_name": "sellers.csv",
        "expected_columns": [
            "seller_id", "seller_zip_code_prefix", "seller_city", "seller_state"
        ],
        "date_columns": [],
        "chunk_size": 10000
    },
    {
        "table_name": "category_translation",
        "file_name": "category_translation.csv",
        "expected_columns": [
            "product_category_name", "product_category_name_english"
        ],
        "date_columns": [],
        "chunk_size": 1000
    },
    {
        "table_name": "geolocation",
        "file_name": "geolocation.csv",
        "expected_columns": [
            "geolocation_zip_code_prefix", "geolocation_lat", "geolocation_lng",
            "geolocation_city", "geolocation_state"
        ],
        "date_columns": [],
        "chunk_size": 50000
    },
    {
        "table_name": "orders",
        "file_name": "orders.csv",
        "expected_columns": [
            "order_id", "customer_id", "order_status", "order_purchase_timestamp",
            "order_approved_at", "order_delivered_carrier_date",
            "order_delivered_customer_date", "order_estimated_delivery_date"
        ],
        "date_columns": [
            "order_purchase_timestamp", "order_approved_at",
            "order_delivered_carrier_date", "order_delivered_customer_date",
            "order_estimated_delivery_date"
        ],
        "chunk_size": 25000
    },
    {
        "table_name": "order_items",
        "file_name": "order_items.csv",
        "expected_columns": [
            "order_id", "order_item_id", "product_id", "seller_id",
            "shipping_limit_date", "price", "freight_value"
        ],
        "date_columns": ["shipping_limit_date"],
        "chunk_size": 25000
    },
    {
        "table_name": "payments",
        "file_name": "payments.csv",
        "expected_columns": [
            "order_id", "payment_sequential", "payment_type",
            "payment_installments", "payment_value"
        ],
        "date_columns": [],
        "chunk_size": 25000
    },
    {
        "table_name": "reviews",
        "file_name": "reviews.csv",
        "expected_columns": [
            "review_id", "order_id", "review_score", "review_comment_title",
            "review_comment_message", "review_creation_date", "review_answer_timestamp"
        ],
        "date_columns": ["review_creation_date", "review_answer_timestamp"],
        "chunk_size": 25000
    }
]


def check_table_row_count(engine, table_name: str) -> Optional[int]:
    """Safely checks existing row count in target table without raising exceptions."""
    try:
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name};"))
            return result.scalar()
    except Exception as e:
        logger.warning(f"Could not query table '{table_name}': {e}")
        return None


def sanitize_dataframe(df: pd.DataFrame, date_columns: List[str]) -> pd.DataFrame:
    """Standardizes types and replaces NaN/Inf with None for clean PostgreSQL NULL representation."""
    df_clean = df.copy()

    # Parse datetime columns safely
    for col in date_columns:
        if col in df_clean.columns:
            df_clean[col] = pd.to_datetime(df_clean[col], errors="coerce")

    # Replace NaN, NaT, and infinite values with None
    df_clean = df_clean.replace({np.nan: None})
    return df_clean


def ingest_table(engine, spec: dict, skip_if_populated: bool = True) -> bool:
    """Loads a single CSV file into the target PostgreSQL table in chunks."""
    table_name = spec["table_name"]
    file_name = spec["file_name"]
    file_path = os.path.join(DATA_RAW_DIR, file_name)

    if not os.path.exists(file_path):
        logger.error(f"Raw dataset file missing: {file_path}")
        return False

    existing_rows = check_table_row_count(engine, table_name)
    if existing_rows is not None and existing_rows > 0:
        if skip_if_populated:
            logger.info(f"Table '{table_name}' already contains {existing_rows:,} rows. Skipping to avoid duplicates.")
            return True
        else:
            logger.warning(f"Table '{table_name}' contains {existing_rows:,} rows; proceeding with ingestion.")

    logger.info(f"Starting ingestion: '{file_name}' -> '{table_name}'")
    start_time = time.time()
    total_loaded = 0

    try:
        reader = pd.read_csv(
            file_path,
            chunksize=spec["chunk_size"],
            low_memory=False,
            encoding="utf-8"
        )

        for chunk_idx, chunk in enumerate(reader):
            # Validate required columns
            missing_cols = set(spec["expected_columns"]) - set(chunk.columns)
            if missing_cols:
                raise ValueError(f"File {file_name} is missing expected columns: {missing_cols}")

            # Reorder to match expected columns
            chunk = chunk[spec["expected_columns"]]
            chunk = sanitize_dataframe(chunk, spec["date_columns"])

            # Bulk append to PostgreSQL
            chunk.to_sql(
                name=table_name,
                con=engine,
                if_exists="append",
                index=False,
                method="multi",
                chunksize=2000
            )
            total_loaded += len(chunk)
            logger.info(f"  [{table_name}] Ingested chunk {chunk_idx + 1} ({len(chunk):,} rows, total: {total_loaded:,})")

        elapsed = time.time() - start_time
        logger.info(f"Completed '{table_name}': {total_loaded:,} rows loaded in {elapsed:.2f}s")
        return True

    except Exception as e:
        logger.error(f"Ingestion failed for table '{table_name}': {e}", exc_info=False)
        return False


def run_etl(skip_if_populated: bool = True):
    """Executes the full automated raw-to-PostgreSQL ETL pipeline."""
    params = get_connection_parameters()
    logger.info("Initializing Raw Dataset Ingestion Pipeline")
    logger.info(f"Target Database: {params['database']} on {params['host']}:{params['port']} (User: {params['user']})")

    if not params["password_configured"]:
        logger.error("DB_PASSWORD is not set in .env. Please configure credentials before running ETL.")
        return False

    try:
        engine = get_sqlalchemy_engine()
        # Verify connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1;"))
        logger.info("Database connection handshake successful.")
    except Exception as e:
        logger.error(f"Failed to connect to PostgreSQL: {e}")
        logger.info("Please verify that PostgreSQL service is running and credentials in .env are correct.")
        return False

    success_count = 0
    total_tables = len(TABLE_IMPORT_SPECS)

    for spec in TABLE_IMPORT_SPECS:
        ok = ingest_table(engine, spec, skip_if_populated=skip_if_populated)
        if ok:
            success_count += 1
        else:
            logger.error(f"Stopping ETL sequence due to failure at table: {spec['table_name']}")
            break

    logger.info(f"ETL Execution Summary: {success_count}/{total_tables} tables successfully processed.")
    return success_count == total_tables


if __name__ == "__main__":
    run_etl(skip_if_populated=True)
