"""
RFM (Recency, Frequency, Monetary) Customer Segmentation & CLTV Module.
Calculates RFM scores, classifies behavioral clusters, and analyzes segment revenue.
"""

from typing import Dict, Any
import pandas as pd
import numpy as np


class RFMSegmentationAnalyzer:
    """Performs RFM scoring and Customer Lifetime Value (CLTV) analysis."""

    def __init__(self, rfm_df: pd.DataFrame):
        self.rfm = rfm_df.copy()

    def segment_summary(self) -> pd.DataFrame:
        """Summarizes key metrics across customer segments."""
        summary = self.rfm.groupby("customer_segment").agg(
            customer_count=("customer_unique_id", "count"),
            total_revenue=("total_spent", "sum"),
            avg_recency=("recency_days", "mean"),
            avg_frequency=("total_orders", "mean"),
            avg_monetary=("total_spent", "mean"),
            avg_review_score=("avg_review_score", "mean")
        ).reset_index()

        total_customers = summary["customer_count"].sum()
        total_rev = summary["total_revenue"].sum()

        summary["customer_pct"] = (summary["customer_count"] / total_customers) * 100
        summary["revenue_pct"] = (summary["total_revenue"] / total_rev) * 100

        # Sort by total revenue descending
        summary = summary.sort_values(by="total_revenue", ascending=False).round(2)
        return summary

    def get_cltv_metrics(self) -> Dict[str, Any]:
        """Calculates observed Historical Customer Lifetime Value metrics."""
        return {
            "overall_avg_cltv": round(float(self.rfm["total_spent"].mean()), 2),
            "median_cltv": round(float(self.rfm["total_spent"].median()), 2),
            "top_10_pct_cltv": round(float(self.rfm["total_spent"].quantile(0.90)), 2),
            "top_1_pct_cltv": round(float(self.rfm["total_spent"].quantile(0.99)), 2),
            "repeat_cltv_multiple": round(
                float(self.rfm[self.rfm["total_orders"] > 1]["total_spent"].mean()) /
                float(self.rfm[self.rfm["total_orders"] == 1]["total_spent"].mean()), 2
            )
        }
