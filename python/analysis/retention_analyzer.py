"""
Customer Retention and Cohort Analysis Module.
Calculates repeat purchase rates, first-time vs returning customer revenue,
and builds monthly cohort retention matrices.
"""

from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np


class RetentionAnalyzer:
    """Computes retention metrics and cohort survival rates using customer_unique_id."""

    def __init__(self, orders_df: pd.DataFrame):
        self.orders = orders_df[orders_df["order_status"] != "canceled"].copy()
        if "order_purchase_timestamp" in self.orders.columns and not pd.api.types.is_datetime64_any_dtype(self.orders["order_purchase_timestamp"]):
            self.orders["order_purchase_timestamp"] = pd.to_datetime(self.orders["order_purchase_timestamp"])

    def calculate_repeat_purchase_metrics(self) -> Dict[str, Any]:
        """Calculates repeat purchaser counts and repeat rate."""
        customer_counts = self.orders.groupby("customer_unique_id").agg(
            order_count=("order_id", "nunique"),
            total_spend=("total_order_value", "sum")
        ).reset_index()

        total_customers = len(customer_counts)
        repeat_customers = int((customer_counts["order_count"] > 1).sum())
        one_time_customers = total_customers - repeat_customers
        repeat_rate = (repeat_customers / total_customers) * 100 if total_customers > 0 else 0.0

        repeat_revenue = float(customer_counts[customer_counts["order_count"] > 1]["total_spend"].sum())
        one_time_revenue = float(customer_counts[customer_counts["order_count"] == 1]["total_spend"].sum())
        total_revenue = repeat_revenue + one_time_revenue
        repeat_revenue_share = (repeat_revenue / total_revenue) * 100 if total_revenue > 0 else 0.0

        return {
            "total_customers": total_customers,
            "one_time_customers": one_time_customers,
            "repeat_customers": repeat_customers,
            "repeat_customer_rate_pct": round(repeat_rate, 2),
            "one_time_revenue": round(one_time_revenue, 2),
            "repeat_revenue": round(repeat_revenue, 2),
            "repeat_revenue_share_pct": round(repeat_revenue_share, 2),
            "repeat_customer_avg_spend": round(repeat_revenue / repeat_customers, 2) if repeat_customers > 0 else 0.0,
            "one_time_customer_avg_spend": round(one_time_revenue / one_time_customers, 2) if one_time_customers > 0 else 0.0
        }

    def generate_cohort_matrix(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Generates cohort size counts and retention percentage matrix."""
        df = self.orders.copy()
        df["cohort_month"] = df.groupby("customer_unique_id")["order_purchase_timestamp"].transform("min").dt.to_period("M")
        df["order_period"] = df["order_purchase_timestamp"].dt.to_period("M")

        df["cohort_index"] = (
            (df["order_period"].dt.year - df["cohort_month"].dt.year) * 12 +
            (df["order_period"].dt.month - df["cohort_month"].dt.month)
        )

        cohort_counts = df.groupby(["cohort_month", "cohort_index"])["customer_unique_id"].nunique().reset_index()
        cohort_matrix = cohort_counts.pivot(index="cohort_month", columns="cohort_index", values="customer_unique_id")
        cohort_size = cohort_matrix.iloc[:, 0]
        retention_matrix = cohort_matrix.divide(cohort_size, axis=0) * 100
        return cohort_matrix, retention_matrix.round(2)
