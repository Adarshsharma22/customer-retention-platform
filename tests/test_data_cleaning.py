"""
Unit Tests for Data Cleansing & Transformation Pipeline.
"""

import os
import pytest
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEANED_DIR = os.path.join(PROJECT_ROOT, "data", "cleaned")
PROCESSED_DIR = os.path.join(PROJECT_ROOT, "data", "processed")


def test_cleaned_datasets_exist():
    """Ensures all 9 cleaned datasets exist."""
    files = [
        "category_translation.csv", "customers.csv", "geolocation.csv",
        "orders.csv", "order_items.csv", "payments.csv",
        "products.csv", "reviews.csv", "sellers.csv"
    ]
    for f in files:
        path = os.path.join(CLEANED_DIR, f)
        assert os.path.exists(path), f"Cleaned file missing: {f}"


def test_geolocation_deduplication():
    """Validates that geolocation deduplication eliminated duplicate zip code prefixes."""
    geo = pd.read_csv(os.path.join(CLEANED_DIR, "geolocation.csv"))
    # In cleaned geo, each zip prefix is aggregated to 1 row
    assert geo["geolocation_zip_code_prefix"].duplicated().sum() == 0
    assert len(geo) > 15000  # Expected ~19k Brazilian zip prefixes


def test_order_items_non_negative():
    """Validates that item prices and freight values are non-negative."""
    items = pd.read_csv(os.path.join(CLEANED_DIR, "order_items.csv"))
    assert (items["price"] < 0).sum() == 0
    assert (items["freight_value"] < 0).sum() == 0


def test_orders_date_enrichment():
    """Validates delivery delay calculation and timestamp conversions."""
    orders = pd.read_csv(os.path.join(PROCESSED_DIR, "orders_enriched.csv"))
    assert "actual_delivery_days" in orders.columns
    assert "is_late_delivery" in orders.columns
    assert "total_order_value" in orders.columns
    # Check that delivered orders have positive delivery days
    delivered = orders[orders["order_status"] == "delivered"].dropna(subset=["actual_delivery_days"])
    assert len(delivered) > 90000
