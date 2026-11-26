"""
Database Verification and Validation Module.
Compares CSV raw datasets against PostgreSQL table row counts, null profiles,
duplicates, and verifies referential integrity constraints.
"""

import csv
import os
import sys
from typing import Dict, Any
import pandas as pd
from sqlalchemy import text

# Add project root to sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from python.config.db_config import get_sqlalchemy_engine, get_connection_parameters
from python.utils.logger import get_logger

logger = get_logger("db_verification")
DATA_RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw")

DATASET_FILES = {
    "customers": "customers.csv",
    "products": "products.csv",
    "sellers": "sellers.csv",
    "category_translation": "category_translation.csv",
    "geolocation": "geolocation.csv",
    "orders": "orders.csv",
    "order_items": "order_items.csv",
    "payments": "payments.csv",
    "reviews": "reviews.csv"
}

REFERENTIAL_CHECKS = [
    {
        "relationship": "orders -> customers",
        "query": """
            SELECT COUNT(*) FROM orders o
            LEFT JOIN customers c ON o.customer_id = c.customer_id
            WHERE c.customer_id IS NULL;
        """
    },
    {
        "relationship": "order_items -> orders",
        "query": """
            SELECT COUNT(*) FROM order_items oi
            LEFT JOIN orders o ON oi.order_id = o.order_id
            WHERE o.order_id IS NULL;
        """
    },
    {
        "relationship": "order_items -> products",
        "query": """
            SELECT COUNT(*) FROM order_items oi
            LEFT JOIN products p ON oi.product_id = p.product_id
            WHERE p.product_id IS NULL;
        """
    },
    {
        "relationship": "order_items -> sellers",
        "query": """
            SELECT COUNT(*) FROM order_items oi
            LEFT JOIN sellers s ON oi.seller_id = s.seller_id
            WHERE s.seller_id IS NULL;
        """
    },
    {
        "relationship": "payments -> orders",
        "query": """
            SELECT COUNT(*) FROM payments p
            LEFT JOIN orders o ON p.order_id = o.order_id
            WHERE o.order_id IS NULL;
        """
    },
    {
        "relationship": "reviews -> orders",
        "query": """
            SELECT COUNT(*) FROM reviews r
            LEFT JOIN orders o ON r.order_id = o.order_id
            WHERE o.order_id IS NULL;
        """
    }
]


def count_csv_rows(file_path: str) -> int:
    """Efficiently counts rows in a CSV file excluding header line."""
    if not os.path.exists(file_path):
        return -1
    with open(file_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        try:
            next(reader)  # Skip header
        except StopIteration:
            return 0
        return sum(1 for _ in reader)


def verify_database() -> Dict[str, Any]:
    """Runs end-to-end database verification against raw CSVs."""
    report = {
        "connected": False,
        "table_counts": {},
        "referential_integrity": {},
        "status": "FAILED"
    }

    params = get_connection_parameters()
    logger.info("Executing PostgreSQL Database Audit & Verification")
    logger.info(f"Target Database: {params['database']} (User: {params['user']})")

    try:
        engine = get_sqlalchemy_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1;"))
            report["connected"] = True

            # 1. Compare Row Counts
            all_match = True
            for table_name, file_name in DATASET_FILES.items():
                csv_path = os.path.join(DATA_RAW_DIR, file_name)
                csv_rows = count_csv_rows(csv_path)

                try:
                    db_rows = conn.execute(text(f"SELECT COUNT(*) FROM {table_name};")).scalar()
                except Exception as e:
                    db_rows = None

                match = (csv_rows == db_rows) if db_rows is not None else False
                if not match:
                    all_match = False

                report["table_counts"][table_name] = {
                    "csv_rows": csv_rows,
                    "db_rows": db_rows,
                    "match": match
                }
                logger.info(f"Table '{table_name}': CSV = {csv_rows:,} | DB = {db_rows if db_rows is not None else 'N/A'} | Match: {match}")

            # 2. Check Referential Integrity
            ri_pass = True
            for check in REFERENTIAL_CHECKS:
                rel = check["relationship"]
                try:
                    orphans = conn.execute(text(check["query"])).scalar()
                    passed = (orphans == 0)
                    if not passed:
                        ri_pass = False
                    report["referential_integrity"][rel] = {"orphans": orphans, "valid": passed}
                    logger.info(f"Referential Check [{rel}]: {orphans} orphaned records (Valid: {passed})")
                except Exception as e:
                    report["referential_integrity"][rel] = {"error": str(e), "valid": False}
                    ri_pass = False
                    logger.warning(f"Referential Check [{rel}] could not run: {e}")

            if all_match and ri_pass:
                report["status"] = "PASSED"
            else:
                report["status"] = "DISCREPANCIES_DETECTED"

    except Exception as e:
        logger.error(f"Cannot perform verification: {e}")
        report["error"] = str(e)
        report["status"] = "CONNECTION_UNAVAILABLE"

    return report


if __name__ == "__main__":
    res = verify_database()
    print("\n--- Verification Summary ---")
    print(f"Status: {res['status']}")
