"""
Unit Tests for Analytical Metrics, Retention, and RFM Segmentation.
"""

import os
import pytest
import pandas as pd
from python.analysis.business_kpis import BusinessKPIAnalyzer
from python.analysis.retention_analyzer import RetentionAnalyzer
from python.analysis.rfm_segmentation import RFMSegmentationAnalyzer

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(PROJECT_ROOT, "data", "processed")


@pytest.fixture(scope="module")
def orders_enriched():
    path = os.path.join(PROCESSED_DIR, "orders_enriched.csv")
    return pd.read_csv(path)


@pytest.fixture(scope="module")
def customer_rfm():
    path = os.path.join(PROCESSED_DIR, "customer_rfm_segments.csv")
    return pd.read_csv(path)


def test_business_kpis(orders_enriched):
    analyzer = BusinessKPIAnalyzer(orders_enriched)
    kpis = analyzer.compute_summary_kpis()
    assert kpis["total_orders"] > 90000
    assert kpis["total_customers"] > 90000
    assert kpis["total_revenue"] > 10000000.0
    assert kpis["average_order_value"] > 50.0
    assert 1.0 <= kpis["average_review_score"] <= 5.0


def test_retention_metrics(orders_enriched):
    analyzer = RetentionAnalyzer(orders_enriched)
    metrics = analyzer.calculate_repeat_purchase_metrics()
    assert metrics["total_customers"] > 90000
    assert metrics["repeat_customers"] > 2000
    assert 2.0 <= metrics["repeat_customer_rate_pct"] <= 5.0
    assert metrics["repeat_revenue"] > 500000.0


def test_rfm_segments(customer_rfm):
    analyzer = RFMSegmentationAnalyzer(customer_rfm)
    summary = analyzer.segment_summary()
    assert len(summary) >= 5
    assert set(summary["customer_segment"]).issubset({
        "Champions", "Loyal Customers", "New / Potential Loyalists",
        "At Risk / Cannot Lose Them", "Hibernating High Spenders",
        "Lost / Churned", "Promising / Standard"
    })
    cltv = analyzer.get_cltv_metrics()
    assert cltv["overall_avg_cltv"] > 0
    assert cltv["repeat_cltv_multiple"] > 1.0
