"""
Delivery Logistics SLA and Review Satisfaction Analysis Module.
Examines correlation between shipping delays, carrier performance, and customer review scores.
"""

from typing import Dict, Any
import pandas as pd
import numpy as np


class DeliverySatisfactionAnalyzer:
    """Analyzes logistics performance and review impact."""

    def __init__(self, orders_df: pd.DataFrame):
        self.orders = orders_df[
            (orders_df["order_status"] == "delivered") &
            (orders_df["review_score"].notnull())
        ].copy()

    def delivery_kpis(self) -> Dict[str, Any]:
        """Calculates overall delivery KPIs."""
        total_delivered = len(self.orders)
        late_orders = int(self.orders["is_late_delivery"].sum())
        late_pct = (late_orders / total_delivered) * 100 if total_delivered > 0 else 0.0

        avg_delivery_time = float(self.orders["actual_delivery_days"].mean())
        avg_estimated_time = float(self.orders["estimated_delivery_days"].mean())

        return {
            "total_delivered_orders": total_delivered,
            "late_deliveries_count": late_orders,
            "late_delivery_rate_pct": round(late_pct, 2),
            "avg_actual_delivery_days": round(avg_delivery_time, 1),
            "avg_estimated_delivery_days": round(avg_estimated_time, 1),
            "avg_review_score_on_time": round(float(self.orders[~self.orders["is_late_delivery"]]["review_score"].mean()), 2),
            "avg_review_score_late": round(float(self.orders[self.orders["is_late_delivery"]]["review_score"].mean()), 2)
        }

    def review_score_by_delivery_performance(self) -> pd.DataFrame:
        """Groups review score distribution by on-time vs late delivery."""
        res = self.orders.groupby("is_late_delivery").agg(
            order_count=("order_id", "count"),
            avg_review_score=("review_score", "mean"),
            one_star_pct=("review_score", lambda x: (x == 1).mean() * 100),
            five_star_pct=("review_score", lambda x: (x == 5).mean() * 100)
        ).reset_index()
        res["delivery_status"] = np.where(res["is_late_delivery"], "Late Delivery", "On-Time Delivery")
        return res.round(2)

    def state_logistics_performance(self) -> pd.DataFrame:
        """Calculates delivery delay and satisfaction per Brazilian state."""
        state_perf = self.orders.groupby("customer_state").agg(
            total_orders=("order_id", "count"),
            avg_delivery_days=("actual_delivery_days", "mean"),
            late_rate_pct=("is_late_delivery", lambda x: x.mean() * 100),
            avg_review_score=("review_score", "mean")
        ).reset_index().sort_values(by="total_orders", ascending=False).round(2)
        return state_perf
