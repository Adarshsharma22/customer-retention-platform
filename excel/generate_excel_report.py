"""
Automated Production Excel Business Report Generator.
Uses openpyxl to compile an executive 8-sheet corporate workbook
with formatted styles, KPI cards, formulas, and data tables.
"""

import os
import sys
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
EXCEL_OUTPUT = os.path.join(PROJECT_ROOT, "excel", "customer_retention_business_report.xlsx")


def style_header(cell, text, bg_color="1E3A8A", font_color="FFFFFF"):
    cell.value = text
    cell.font = Font(name="Segoe UI", size=11, bold=True, color=font_color)
    cell.fill = PatternFill(start_color=bg_color, end_color=bg_color, fill_type="solid")
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)


def auto_fit_columns(ws, min_width=12):
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val_str = str(cell.value or "")
            if len(val_str) > max_len:
                max_len = len(val_str)
        ws.column_dimensions[col_letter].width = max(max_len + 3, min_width)


def build_workbook():
    print("Generating Executive Excel Business Report...")
    wb = Workbook()
    thin_border = Border(
        left=Side(style='thin', color='CBD5E1'),
        right=Side(style='thin', color='CBD5E1'),
        top=Side(style='thin', color='CBD5E1'),
        bottom=Side(style='thin', color='CBD5E1')
    )

    # Load data
    orders = pd.read_csv(os.path.join(DATA_DIR, "orders_enriched.csv"))
    rfm = pd.read_csv(os.path.join(DATA_DIR, "customer_rfm_segments.csv"))
    categories = pd.read_csv(os.path.join(DATA_DIR, "category_performance.csv"))
    sellers = pd.read_csv(os.path.join(DATA_DIR, "seller_performance.csv"))

    # -------------------------------------------------------------
    # 1. Executive Summary Sheet
    # -------------------------------------------------------------
    ws1 = wb.active
    ws1.title = "Executive Summary"
    ws1.views.sheetView[0].showGridLines = True

    # Title Banner
    ws1.merge_cells("A1:G2")
    title_cell = ws1["A1"]
    title_cell.value = "Customer Retention & Revenue Intelligence Platform"
    title_cell.font = Font(name="Segoe UI", size=16, bold=True, color="FFFFFF")
    title_cell.fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
    title_cell.alignment = Alignment(horizontal="center", vertical="center")

    # KPI Summary Cards
    total_orders = orders["order_id"].nunique()
    total_customers = rfm["customer_unique_id"].nunique()
    total_revenue = orders["total_order_value"].sum()
    repeat_rate = (rfm["total_orders"] > 1).mean() * 100
    aov = total_revenue / total_orders
    avg_review = orders["review_score"].mean()

    kpis = [
        ("Total Platform Revenue", f"R$ {total_revenue:,.2f}"),
        ("Completed Orders", f"{total_orders:,}"),
        ("Unique Customers", f"{total_customers:,}"),
        ("Repeat Purchase Rate", f"{repeat_rate:.2f}%"),
        ("Average Order Value (AOV)", f"R$ {aov:.2f}"),
        ("Average Review Score", f"{avg_review:.2f} / 5.0")
    ]

    ws1.cell(row=4, column=1, value="Core Business Key Performance Indicators").font = Font(name="Segoe UI", size=13, bold=True, color="1E3A8A")

    for i, (metric, val) in enumerate(kpis):
        r = 6 + i * 2
        ws1.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
        c1 = ws1.cell(row=r, column=1, value=metric)
        c1.font = Font(name="Segoe UI", size=11, bold=True, color="334155")
        c1.fill = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
        c1.border = thin_border

        ws1.merge_cells(start_row=r, start_column=4, end_row=r, end_column=5)
        c2 = ws1.cell(row=r, column=4, value=val)
        c2.font = Font(name="Segoe UI", size=11, bold=True, color="1E3A8A")
        c2.alignment = Alignment(horizontal="right")
        c2.fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
        c2.border = thin_border

    auto_fit_columns(ws1)

    # -------------------------------------------------------------
    # 2. Monthly Revenue Sheet
    # -------------------------------------------------------------
    ws2 = wb.create_sheet(title="Monthly Revenue")
    ws2.views.sheetView[0].showGridLines = True
    orders["order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"])
    orders["year_month"] = orders["order_purchase_timestamp"].dt.to_period("M").astype(str)

    monthly = orders[orders["year_month"].between("2017-01", "2018-08")].groupby("year_month").agg(
        orders_count=("order_id", "nunique"),
        customers_count=("customer_unique_id", "nunique"),
        total_gmv=("order_gmv", "sum"),
        freight_total=("order_freight", "sum"),
        total_revenue=("total_order_value", "sum")
    ).reset_index().sort_values("year_month")

    headers = ["Purchase Month", "Order Count", "Active Customers", "GMV (R$)", "Freight (R$)", "Total Revenue (R$)"]
    for col_idx, h in enumerate(headers, 1):
        style_header(ws2.cell(row=1, column=col_idx), h)

    for row_idx, row in enumerate(monthly.itertuples(), 2):
        ws2.cell(row=row_idx, column=1, value=row.year_month).alignment = Alignment(horizontal="center")
        ws2.cell(row=row_idx, column=2, value=row.orders_count).number_format = "#,##0"
        ws2.cell(row=row_idx, column=3, value=row.customers_count).number_format = "#,##0"
        ws2.cell(row=row_idx, column=4, value=row.total_gmv).number_format = "R$ #,##0.00"
        ws2.cell(row=row_idx, column=5, value=row.freight_total).number_format = "R$ #,##0.00"
        ws2.cell(row=row_idx, column=6, value=row.total_revenue).number_format = "R$ #,##0.00"
        for c in range(1, 7):
            ws2.cell(row=row_idx, column=c).border = thin_border

    # Totals Row with Formulas
    last_r = len(monthly) + 1
    tot_r = last_r + 1
    ws2.cell(row=tot_r, column=1, value="Total").font = Font(bold=True)
    ws2.cell(row=tot_r, column=2, value=f"=SUM(B2:B{last_r})").font = Font(bold=True)
    ws2.cell(row=tot_r, column=2).number_format = "#,##0"
    ws2.cell(row=tot_r, column=3, value=f"=SUM(C2:C{last_r})").font = Font(bold=True)
    ws2.cell(row=tot_r, column=3).number_format = "#,##0"
    ws2.cell(row=tot_r, column=4, value=f"=SUM(D2:D{last_r})").font = Font(bold=True)
    ws2.cell(row=tot_r, column=4).number_format = "R$ #,##0.00"
    ws2.cell(row=tot_r, column=5, value=f"=SUM(E2:E{last_r})").font = Font(bold=True)
    ws2.cell(row=tot_r, column=5).number_format = "R$ #,##0.00"
    ws2.cell(row=tot_r, column=6, value=f"=SUM(F2:F{last_r})").font = Font(bold=True)
    ws2.cell(row=tot_r, column=6).number_format = "R$ #,##0.00"

    auto_fit_columns(ws2)

    # -------------------------------------------------------------
    # 3. Customer Retention Sheet
    # -------------------------------------------------------------
    ws3 = wb.create_sheet(title="Customer Retention")
    ws3.views.sheetView[0].showGridLines = True

    retention_summary = [
        ("Metric Description", "One-Time Customers", "Repeat Customers", "Total / Ratio"),
        ("Customer Entity Count", f"{len(rfm[rfm['total_orders'] == 1]):,}", f"{len(rfm[rfm['total_orders'] > 1]):,}", f"{len(rfm):,}"),
        ("Customer Percentage Share", f"{(len(rfm[rfm['total_orders'] == 1])/len(rfm))*100:.2f}%", f"{(len(rfm[rfm['total_orders'] > 1])/len(rfm))*100:.2f}%", "100.0%"),
        ("Total Spend Contribution (R$)", f"R$ {rfm[rfm['total_orders'] == 1]['total_spent'].sum():,.2f}", f"R$ {rfm[rfm['total_orders'] > 1]['total_spent'].sum():,.2f}", f"R$ {rfm['total_spent'].sum():,.2f}"),
        ("Revenue Percentage Share", f"{(rfm[rfm['total_orders'] == 1]['total_spent'].sum()/rfm['total_spent'].sum())*100:.2f}%", f"{(rfm[rfm['total_orders'] > 1]['total_spent'].sum()/rfm['total_spent'].sum())*100:.2f}%", "100.0%"),
        ("Average Spend Per Customer", f"R$ {rfm[rfm['total_orders'] == 1]['total_spent'].mean():.2f}", f"R$ {rfm[rfm['total_orders'] > 1]['total_spent'].mean():.2f}", f"{rfm[rfm['total_orders'] > 1]['total_spent'].mean()/rfm[rfm['total_orders'] == 1]['total_spent'].mean():.2f}x Multiplier")
    ]

    for row_idx, rdata in enumerate(retention_summary, 1):
        for col_idx, val in enumerate(rdata, 1):
            cell = ws3.cell(row=row_idx, column=col_idx, value=val)
            if row_idx == 1:
                style_header(cell, val)
            else:
                cell.border = thin_border
                if col_idx > 1:
                    cell.alignment = Alignment(horizontal="right")

    auto_fit_columns(ws3)

    # -------------------------------------------------------------
    # 4. RFM Segmentation Sheet
    # -------------------------------------------------------------
    ws4 = wb.create_sheet(title="RFM Segmentation")
    ws4.views.sheetView[0].showGridLines = True

    rfm_summary = rfm.groupby("customer_segment").agg(
        cust_count=("customer_unique_id", "count"),
        total_rev=("total_spent", "sum"),
        avg_recency=("recency_days", "mean"),
        avg_orders=("total_orders", "mean"),
        avg_spend=("total_spent", "mean")
    ).reset_index().sort_values(by="total_rev", ascending=False)

    rfm_headers = ["Customer Segment", "Customer Count", "Revenue Contribution (R$)", "Avg Recency (Days)", "Avg Orders", "Avg Spend (R$)"]
    for col_idx, h in enumerate(rfm_headers, 1):
        style_header(ws4.cell(row=1, column=col_idx), h)

    for row_idx, row in enumerate(rfm_summary.itertuples(), 2):
        ws4.cell(row=row_idx, column=1, value=row.customer_segment).border = thin_border
        ws4.cell(row=row_idx, column=2, value=row.cust_count).number_format = "#,##0"
        ws4.cell(row=row_idx, column=3, value=row.total_rev).number_format = "R$ #,##0.00"
        ws4.cell(row=row_idx, column=4, value=round(row.avg_recency, 1)).number_format = "0.0"
        ws4.cell(row=row_idx, column=5, value=round(row.avg_orders, 2)).number_format = "0.00"
        ws4.cell(row=row_idx, column=6, value=round(row.avg_spend, 2)).number_format = "R$ #,##0.00"
        for c in range(1, 7):
            ws4.cell(row=row_idx, column=c).border = thin_border

    auto_fit_columns(ws4)

    # -------------------------------------------------------------
    # 5. Category Performance Sheet
    # -------------------------------------------------------------
    ws5 = wb.create_sheet(title="Category Performance")
    ws5.views.sheetView[0].showGridLines = True
    cat_headers = ["Category Name (English)", "Units Sold", "Category GMV (R$)", "Freight Value (R$)", "Avg Item Price (R$)", "Revenue Share %"]
    for col_idx, h in enumerate(cat_headers, 1):
        style_header(ws5.cell(row=1, column=col_idx), h)

    for row_idx, row in enumerate(categories.head(25).itertuples(), 2):
        ws5.cell(row=row_idx, column=1, value=row.product_category_name_english).border = thin_border
        ws5.cell(row=row_idx, column=2, value=row.total_items_sold).number_format = "#,##0"
        ws5.cell(row=row_idx, column=3, value=row.total_category_revenue).number_format = "R$ #,##0.00"
        ws5.cell(row=row_idx, column=4, value=row.total_freight_revenue).number_format = "R$ #,##0.00"
        ws5.cell(row=row_idx, column=5, value=row.avg_item_price).number_format = "R$ #,##0.00"
        ws5.cell(row=row_idx, column=6, value=row.revenue_share_pct / 100).number_format = "0.0%"
        for c in range(1, 7):
            ws5.cell(row=row_idx, column=c).border = thin_border

    auto_fit_columns(ws5)

    # -------------------------------------------------------------
    # 6. Seller Performance Sheet
    # -------------------------------------------------------------
    ws6 = wb.create_sheet(title="Seller Performance")
    ws6.views.sheetView[0].showGridLines = True
    seller_headers = ["Seller ID", "State", "Orders Fulfilled", "Total Sales (R$)", "Avg Item Price (R$)", "Avg Delay (Days)"]
    for col_idx, h in enumerate(seller_headers, 1):
        style_header(ws6.cell(row=1, column=col_idx), h)

    for row_idx, row in enumerate(sellers.sort_values(by="total_seller_revenue", ascending=False).head(30).itertuples(), 2):
        ws6.cell(row=row_idx, column=1, value=row.seller_id[:16] + "...").border = thin_border
        ws6.cell(row=row_idx, column=2, value=str(row.seller_state)).alignment = Alignment(horizontal="center")
        ws6.cell(row=row_idx, column=3, value=row.total_orders_fulfilled).number_format = "#,##0"
        ws6.cell(row=row_idx, column=4, value=row.total_seller_revenue).number_format = "R$ #,##0.00"
        ws6.cell(row=row_idx, column=5, value=row.avg_item_price).number_format = "R$ #,##0.00"
        ws6.cell(row=row_idx, column=6, value=round(row.avg_delivery_delay, 1)).number_format = "0.0"
        for c in range(1, 7):
            ws6.cell(row=row_idx, column=c).border = thin_border

    auto_fit_columns(ws6)

    # -------------------------------------------------------------
    # 7. Delivery Performance Sheet
    # -------------------------------------------------------------
    ws7 = wb.create_sheet(title="Delivery Performance")
    ws7.views.sheetView[0].showGridLines = True
    delivered = orders[(orders["order_status"] == "delivered") & (orders["review_score"].notnull())]

    state_delivery = delivered.groupby("customer_state").agg(
        orders_delivered=("order_id", "count"),
        avg_delivery_days=("actual_delivery_days", "mean"),
        late_rate=("is_late_delivery", lambda x: x.mean()),
        avg_score=("review_score", "mean")
    ).reset_index().sort_values(by="orders_delivered", ascending=False)

    del_headers = ["Customer State", "Delivered Orders", "Avg Delivery Time (Days)", "Late Delivery Rate %", "Average Review Score"]
    for col_idx, h in enumerate(del_headers, 1):
        style_header(ws7.cell(row=1, column=col_idx), h)

    for row_idx, row in enumerate(state_delivery.itertuples(), 2):
        ws7.cell(row=row_idx, column=1, value=row.customer_state).alignment = Alignment(horizontal="center")
        ws7.cell(row=row_idx, column=2, value=row.orders_delivered).number_format = "#,##0"
        ws7.cell(row=row_idx, column=3, value=round(row.avg_delivery_days, 1)).number_format = "0.0"
        ws7.cell(row=row_idx, column=4, value=row.late_rate).number_format = "0.0%"
        ws7.cell(row=row_idx, column=5, value=round(row.avg_score, 2)).number_format = "0.00"
        for c in range(1, 6):
            ws7.cell(row=row_idx, column=c).border = thin_border

    auto_fit_columns(ws7)

    # -------------------------------------------------------------
    # 8. Data Quality Sheet
    # -------------------------------------------------------------
    ws8 = wb.create_sheet(title="Data Quality")
    ws8.views.sheetView[0].showGridLines = True
    dq_headers = ["Audit Item", "Raw Observation", "Cleansing Treatment", "Status / Integrity"]
    for col_idx, h in enumerate(dq_headers, 1):
        style_header(ws8.cell(row=1, column=col_idx), h)

    dq_rows = [
        ("Geolocation Duplicates", "261,831 exact duplicate rows found in raw GPS logs", "Grouped by ZIP prefix to median coordinates", "PASSED (19,011 Clean ZIPs)"),
        ("Missing Delivery Dates", "2,965 orders without delivered date in orders.csv", "Preserved as canceled/in-transit orders without dropping", "VERIFIED"),
        ("Product Categories", "610 records without category name in products.csv", "Imputed with 'outros' (others) to preserve catalog", "RESOLVED"),
        ("Review Text Nulls", "87,656 null titles, 58,247 null comment texts", "Filled with 'No Title'/'No Comment'; numeric scores retained", "RESOLVED"),
        ("Referential Integrity", "Checked all foreign keys across 9 relational tables", "0 orphaned foreign key records detected across all entities", "100% INTEGRITY")
    ]

    for row_idx, rdata in enumerate(dq_rows, 2):
        for col_idx, val in enumerate(rdata, 1):
            c = ws8.cell(row=row_idx, column=col_idx, value=val)
            c.border = thin_border
            if col_idx == 4:
                c.font = Font(bold=True, color="16A34A" if "PASSED" in val or "100%" in val else "2563EB")

    auto_fit_columns(ws8)

    # Save
    wb.save(EXCEL_OUTPUT)
    print(f"Excel Business Report successfully saved: {EXCEL_OUTPUT}")


if __name__ == "__main__":
    build_workbook()
