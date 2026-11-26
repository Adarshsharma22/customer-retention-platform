"""
Unit Tests for Raw Dataset Ingestion and Column Integrity.
"""

import os
import pytest
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw")

EXPECTED_FILES = [
    "category_translation.csv",
    "customers.csv",
    "geolocation.csv",
    "orders.csv",
    "order_items.csv",
    "payments.csv",
    "products.csv",
    "reviews.csv",
    "sellers.csv"
]


@pytest.mark.parametrize("file_name", EXPECTED_FILES)
def test_raw_files_exist(file_name):
    """Verifies all 9 original Olist CSV datasets exist in data/raw/."""
    file_path = os.path.join(DATA_RAW_DIR, file_name)
    assert os.path.exists(file_path), f"Missing raw dataset: {file_name}"
    assert os.path.getsize(file_path) > 0, f"Raw dataset {file_name} is empty."


def test_customers_schema():
    df = pd.read_csv(os.path.join(DATA_RAW_DIR, "customers.csv"), nrows=10)
    expected_cols = {"customer_id", "customer_unique_id", "customer_zip_code_prefix", "customer_city", "customer_state"}
    assert expected_cols.issubset(set(df.columns))


def test_orders_schema():
    df = pd.read_csv(os.path.join(DATA_RAW_DIR, "orders.csv"), nrows=10)
    expected_cols = {
        "order_id", "customer_id", "order_status", "order_purchase_timestamp",
        "order_approved_at", "order_delivered_carrier_date",
        "order_delivered_customer_date", "order_estimated_delivery_date"
    }
    assert expected_cols.issubset(set(df.columns))


def test_order_items_schema():
    df = pd.read_csv(os.path.join(DATA_RAW_DIR, "order_items.csv"), nrows=10)
    expected_cols = {"order_id", "order_item_id", "product_id", "seller_id", "shipping_limit_date", "price", "freight_value"}
    assert expected_cols.issubset(set(df.columns))
