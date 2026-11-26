"""
Power BI Data Export & Star Schema Generator.
Constructs optimized dimensional and fact tables from cleaned data
for direct consumption in Power BI Desktop.
"""

import os
import sys
import pandas as pd
import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_CLEANED_DIR = os.path.join(PROJECT_ROOT, "data", "cleaned")
DATA_PROCESSED_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
POWERBI_EXPORTS_DIR = os.path.join(PROJECT_ROOT, "powerbi", "exports")
os.makedirs(POWERBI_EXPORTS_DIR, exist_ok=True)


def generate_dim_date(start_date: str = "2016-01-01", end_date: str = "2018-12-31") -> pd.DataFrame:
    """Generates continuous enterprise calendar date dimension table."""
    dates = pd.date_range(start=start_date, end=end_date, freq="D")
    df = pd.DataFrame({"Date": dates})
    df["DateKey"] = df["Date"].dt.strftime("%Y%m%d").astype(int)
    df["Year"] = df["Date"].dt.year
    df["Quarter"] = "Q" + df["Date"].dt.quarter.astype(str)
    df["QuarterYear"] = df["Date"].dt.year.astype(str) + " " + df["Quarter"]
    df["Month"] = df["Date"].dt.month
    df["MonthName"] = df["Date"].dt.strftime("%B")
    df["MonthShort"] = df["Date"].dt.strftime("%b")
    df["YearMonth"] = df["Date"].dt.strftime("%Y-%m")
    df["Day"] = df["Date"].dt.day
    df["DayOfWeek"] = df["Date"].dt.dayofweek + 1
    df["DayName"] = df["Date"].dt.strftime("%A")
    df["IsWeekend"] = df["DayOfWeek"].isin([6, 7])
    return df


def build_star_schema():
    print("Building Power BI Star Schema Tables...")

    # 1. Dim Date
    dim_date = generate_dim_date()
    dim_date.to_csv(os.path.join(POWERBI_EXPORTS_DIR, "dim_date.csv"), index=False)
    print(f"Exported dim_date.csv ({len(dim_date):,} rows)")

    # 2. Dim Customers
    cust = pd.read_csv(os.path.join(DATA_CLEANED_DIR, "customers.csv"))
    rfm = pd.read_csv(os.path.join(DATA_PROCESSED_DIR, "customer_rfm_segments.csv"))
    # Merge customer segment and RFM scores into customer dimension
    dim_customers = cust.merge(
        rfm[[
            "customer_unique_id", "customer_type", "customer_segment",
            "recency_days", "R_score", "F_score", "M_score", "RFM_Score",
            "first_order_date", "last_order_date"
        ]],
        on="customer_unique_id",
        how="left"
    )
    dim_customers.to_csv(os.path.join(POWERBI_EXPORTS_DIR, "dim_customers.csv"), index=False)
    print(f"Exported dim_customers.csv ({len(dim_customers):,} rows)")

    # 3. Dim Products
    prod = pd.read_csv(os.path.join(DATA_CLEANED_DIR, "products.csv"))
    prod.to_csv(os.path.join(POWERBI_EXPORTS_DIR, "dim_products.csv"), index=False)
    print(f"Exported dim_products.csv ({len(prod):,} rows)")

    # 4. Dim Sellers
    sellers = pd.read_csv(os.path.join(DATA_CLEANED_DIR, "sellers.csv"))
    seller_perf = pd.read_csv(os.path.join(DATA_PROCESSED_DIR, "seller_performance.csv"))
    dim_sellers = sellers.merge(
        seller_perf[["seller_id", "total_orders_fulfilled", "total_seller_revenue", "avg_delivery_delay"]],
        on="seller_id",
        how="left"
    )
    dim_sellers.to_csv(os.path.join(POWERBI_EXPORTS_DIR, "dim_sellers.csv"), index=False)
    print(f"Exported dim_sellers.csv ({len(dim_sellers):,} rows)")

    # 5. Dim Geolocation
    geo = pd.read_csv(os.path.join(DATA_CLEANED_DIR, "geolocation.csv"))
    geo.to_csv(os.path.join(POWERBI_EXPORTS_DIR, "dim_geolocation.csv"), index=False)
    print(f"Exported dim_geolocation.csv ({len(geo):,} rows)")

    # 6. Fact Orders
    orders = pd.read_csv(os.path.join(DATA_CLEANED_DIR, "orders.csv"))
    orders_enriched = pd.read_csv(os.path.join(DATA_PROCESSED_DIR, "orders_enriched.csv"))
    # Include financial and review rollups
    fact_orders = orders_enriched[[
        "order_id", "customer_id", "order_status",
        "order_purchase_timestamp", "order_approved_at",
        "order_delivered_carrier_date", "order_delivered_customer_date",
        "order_estimated_delivery_date", "actual_delivery_days",
        "estimated_delivery_days", "delivery_delay_days", "is_delivered",
        "is_late_delivery", "items_count", "order_gmv", "order_freight",
        "total_order_value", "total_paid", "review_score"
    ]].copy()
    fact_orders.to_csv(os.path.join(POWERBI_EXPORTS_DIR, "fact_orders.csv"), index=False)
    print(f"Exported fact_orders.csv ({len(fact_orders):,} rows)")

    # 7. Fact Order Items
    items = pd.read_csv(os.path.join(DATA_CLEANED_DIR, "order_items.csv"))
    items.to_csv(os.path.join(POWERBI_EXPORTS_DIR, "fact_order_items.csv"), index=False)
    print(f"Exported fact_order_items.csv ({len(items):,} rows)")

    # 8. Fact Payments
    payments = pd.read_csv(os.path.join(DATA_CLEANED_DIR, "payments.csv"))
    payments.to_csv(os.path.join(POWERBI_EXPORTS_DIR, "fact_payments.csv"), index=False)
    print(f"Exported fact_payments.csv ({len(payments):,} rows)")

    # 9. Fact Reviews
    reviews = pd.read_csv(os.path.join(DATA_CLEANED_DIR, "reviews.csv"))
    reviews.to_csv(os.path.join(POWERBI_EXPORTS_DIR, "fact_reviews.csv"), index=False)
    print(f"Exported fact_reviews.csv ({len(reviews):,} rows)")

    # 10. Analytical Marts for Direct Visuals
    rfm.to_csv(os.path.join(POWERBI_EXPORTS_DIR, "mart_customer_rfm.csv"), index=False)
    cohort = pd.read_csv(os.path.join(DATA_PROCESSED_DIR, "cohort_retention_rate_matrix.csv"))
    cohort.to_csv(os.path.join(POWERBI_EXPORTS_DIR, "mart_monthly_cohort_retention.csv"), index=False)
    print("Power BI Star Schema export completed successfully!")


if __name__ == "__main__":
    build_star_schema()
