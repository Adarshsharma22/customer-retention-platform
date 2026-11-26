"""
Business Key Performance Indicator (KPI) Module.
Calculates high-level revenue, order velocity, growth rates, and average order value.
"""

from typing import Dict, Any
import pandas as pd
import numpy as np


class BusinessKPIAnalyzer:
    """Computes overall business performance metrics."""

    def __init__(self, orders_df: pd.DataFrame):
        # Filter for completed or valid orders
        self.orders = orders_df[orders_df["order_status"] != "canceled"].copy()
        if "order_purchase_timestamp" in self.orders.columns and not pd.api.types.is_datetime64_any_dtype(self.orders["order_purchase_timestamp"]):
            self.orders["order_purchase_timestamp"] = pd.to_datetime(self.orders["order_purchase_timestamp"])
        self.orders["year_month"] = self.orders["order_purchase_timestamp"].dt.to_period("M").astype(str)

    def compute_summary_kpis(self) -> Dict[str, Any]:
        """Calculates core executive KPIs."""
        total_orders = int(self.orders["order_id"].nunique())
        total_customers = int(self.orders["customer_unique_id"].nunique())
        total_gmv = float(self.orders["order_gmv"].sum()) if "order_gmv" in self.orders.columns else float(self.orders["total_order_value"].sum())
        total_revenue = float(self.orders["total_order_value"].sum())
        aov = float(total_revenue / total_orders) if total_orders > 0 else 0.0
        avg_review = float(self.orders["review_score"].mean()) if "review_score" in self.orders.columns else 0.0

        return {
            "total_orders": total_orders,
            "total_customers": total_customers,
            "total_gmv": round(total_gmv, 2),
            "total_revenue": round(total_revenue, 2),
            "average_order_value": round(aov, 2),
            "average_review_score": round(avg_review, 2)
        }

    def compute_monthly_trends(self) -> pd.DataFrame:
        """Calculates monthly revenue, orders, active customers, and MoM growth."""
        monthly = self.orders.groupby("year_month").agg(
            monthly_orders=("order_id", "nunique"),
            monthly_customers=("customer_unique_id", "nunique"),
            monthly_revenue=("total_order_value", "sum"),
            avg_order_value=("total_order_value", "mean")
        ).reset_index().sort_values("year_month")

        monthly["revenue_mom_growth_pct"] = monthly["monthly_revenue"].pct_change() * 100
        monthly["orders_mom_growth_pct"] = monthly["monthly_orders"].pct_change() * 100
        return monthly
