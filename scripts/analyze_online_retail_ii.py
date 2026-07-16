"""Analyze UCI Online Retail II and export portfolio charts + metrics JSON."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "online_retail_II.xlsx"
OUT = ROOT / "public" / "images" / "case_studies"
DERIVED = ROOT / "data" / "derived"


def main() -> None:
    DERIVED.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    print("reading excel...")
    xl = pd.ExcelFile(RAW)
    print("sheets", xl.sheet_names)
    frames = [pd.read_excel(RAW, sheet_name=s) for s in xl.sheet_names]
    df = pd.concat(frames, ignore_index=True)
    df.columns = [str(c).strip() for c in df.columns]

    rename: dict[str, str] = {}
    for c in df.columns:
        cl = c.lower().replace(" ", "")
        if cl in ("invoiceno", "invoice"):
            rename[c] = "Invoice"
        elif cl == "stockcode":
            rename[c] = "StockCode"
        elif cl == "description":
            rename[c] = "Description"
        elif cl == "quantity":
            rename[c] = "Quantity"
        elif cl == "invoicedate":
            rename[c] = "InvoiceDate"
        elif cl in ("unitprice", "price"):
            rename[c] = "UnitPrice"
        elif cl in ("customerid", "customerid"):
            rename[c] = "CustomerID"
        elif "customer" in cl and "id" in cl:
            rename[c] = "CustomerID"
        elif cl == "country":
            rename[c] = "Country"
    df = df.rename(columns=rename)
    print("rows raw", len(df), "cols", list(df.columns))

    raw_rows = len(df)
    df["Invoice"] = df["Invoice"].astype(str)
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["is_cancel"] = df["Invoice"].str.startswith("C")
    missing_id = int(df["CustomerID"].isna().sum())

    cust = df.dropna(subset=["CustomerID"]).copy()
    cust["CustomerID"] = cust["CustomerID"].astype(int).astype(str)
    cust["Revenue"] = cust["Quantity"] * cust["UnitPrice"]

    sales = cust[~cust["is_cancel"]].copy()
    sales = sales[sales["Quantity"] > 0]
    sales = sales[sales["UnitPrice"] >= 0]

    orders = sales.groupby("Invoice", as_index=False).agg(
        order_revenue=("Revenue", "sum"),
        order_date=("InvoiceDate", "max"),
        customer=("CustomerID", "first"),
        country=("Country", "first"),
    )
    customers = int(sales["CustomerID"].nunique())
    total_revenue = float(sales["Revenue"].sum())
    n_orders = int(orders["Invoice"].nunique())
    aov = total_revenue / n_orders if n_orders else 0.0

    sales["YearMonth"] = sales["InvoiceDate"].dt.to_period("M").astype(str)
    monthly = sales.groupby("YearMonth", as_index=False)["Revenue"].sum().sort_values("YearMonth")
    peak = monthly.loc[monthly["Revenue"].idxmax()]

    snapshot = sales["InvoiceDate"].max() + pd.Timedelta(days=1)
    rfm = sales.groupby("CustomerID").agg(
        Recency=("InvoiceDate", lambda x: (snapshot - x.max()).days),
        Frequency=("Invoice", "nunique"),
        Monetary=("Revenue", "sum"),
    ).reset_index()

    rfm["R"] = pd.qcut(rfm["Recency"], 5, labels=[5, 4, 3, 2, 1]).astype(int)
    rfm["F"] = pd.qcut(rfm["Frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm["M"] = pd.qcut(rfm["Monetary"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)

    def label_row(row: pd.Series) -> str:
        if row["R"] >= 4 and row["F"] >= 4:
            return "Champions"
        if row["R"] >= 3 and row["F"] >= 3:
            return "Loyal"
        if row["R"] >= 4 and row["F"] <= 2:
            return "Promising"
        if row["R"] <= 2 and row["F"] >= 3:
            return "At Risk"
        if row["R"] <= 2 and row["F"] <= 2:
            return "Lost"
        return "Need Attention"

    rfm["Segment"] = rfm.apply(label_row, axis=1)
    seg = (
        rfm.groupby("Segment")
        .agg(customers=("CustomerID", "count"), revenue=("Monetary", "sum"))
        .reset_index()
    )
    seg["share_customers"] = seg["customers"] / seg["customers"].sum()
    seg["share_revenue"] = seg["revenue"] / seg["revenue"].sum()
    seg = seg.sort_values("revenue", ascending=False)

    last_date = sales["InvoiceDate"].max()
    ytd_start = pd.Timestamp(year=last_date.year, month=1, day=1)
    mtd_start = pd.Timestamp(year=last_date.year, month=last_date.month, day=1)
    ytd_rev = float(sales.loc[sales["InvoiceDate"] >= ytd_start, "Revenue"].sum())
    mtd_rev = float(sales.loc[sales["InvoiceDate"] >= mtd_start, "Revenue"].sum())

    metrics = {
        "raw_rows": int(raw_rows),
        "missing_customer_id": missing_id,
        "cancellations": int(cust["is_cancel"].sum()),
        "clean_line_rows": int(len(sales)),
        "customers": customers,
        "orders": n_orders,
        "total_revenue_gbp": round(total_revenue, 2),
        "aov_gbp": round(aov, 2),
        "peak_month": str(peak["YearMonth"]),
        "peak_month_revenue_gbp": round(float(peak["Revenue"]), 2),
        "date_min": str(sales["InvoiceDate"].min().date()),
        "date_max": str(sales["InvoiceDate"].max().date()),
        "ytd_year": int(last_date.year),
        "ytd_revenue_gbp": round(ytd_rev, 2),
        "mtd_month": f"{last_date.year}-{last_date.month:02d}",
        "mtd_revenue_gbp": round(mtd_rev, 2),
        "segments": seg.to_dict(orient="records"),
    }
    (DERIVED / "retail_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps({k: metrics[k] for k in list(metrics) if k != "segments"}, indent=2))
    print("segments", metrics["segments"])

    ink = "#1a1a1a"
    muted = "#5c5c5c"
    teal = "#2a9d8f"
    orange = "#e76f51"
    cream = "#f7f4ef"
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "axes.facecolor": cream,
            "figure.facecolor": cream,
            "axes.edgecolor": ink,
            "text.color": ink,
            "axes.labelcolor": ink,
            "xtick.color": muted,
            "ytick.color": muted,
        }
    )

    fig, ax = plt.subplots(figsize=(10, 4.2), dpi=140)
    ax.plot(range(len(monthly)), monthly["Revenue"] / 1000, color=teal, linewidth=2.2)
    ax.fill_between(range(len(monthly)), monthly["Revenue"] / 1000, color=teal, alpha=0.15)
    ax.set_title("Monthly revenue (GBP thousands), Online Retail II cleaned sales")
    ax.set_ylabel("GBP k")
    step = max(1, len(monthly) // 8)
    ax.set_xticks(range(0, len(monthly), step))
    ax.set_xticklabels(monthly["YearMonth"].iloc[::step], rotation=45, ha="right")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "retail-monthly-revenue.jpg", dpi=140, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4.2), dpi=140)
    order = seg.sort_values("customers", ascending=True)
    ax.barh(order["Segment"], order["customers"], color=teal)
    ax.set_title("Customers by RFM segment")
    ax.set_xlabel("Customers")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "retail-rfm-customers.jpg", dpi=140, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4.2), dpi=140)
    order2 = seg.sort_values("revenue", ascending=True)
    ax.barh(order2["Segment"], order2["share_revenue"] * 100, color=orange)
    ax.set_title("Revenue share by RFM segment (%)")
    ax.set_xlabel("% of cleaned revenue")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "retail-rfm-revenue.jpg", dpi=140, bbox_inches="tight")
    plt.close(fig)

    country = sales.groupby("Country")["Revenue"].sum().sort_values(ascending=False).head(8)
    fig, ax = plt.subplots(figsize=(8, 4.2), dpi=140)
    ax.barh(list(country.index[::-1]), list(country.values[::-1] / 1000), color=teal)
    ax.set_title("Top countries by revenue (GBP thousands)")
    ax.set_xlabel("GBP k")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "retail-top-countries.jpg", dpi=140, bbox_inches="tight")
    plt.close(fig)

    funnel_labels = ["Raw rows", "With CustomerID", "Non-cancel lines", "Qty>0 sales lines"]
    funnel_vals = [
        raw_rows,
        int((~df["CustomerID"].isna()).sum()),
        int((~cust["is_cancel"]).sum()),
        int(len(sales)),
    ]
    fig, ax = plt.subplots(figsize=(8, 4.2), dpi=140)
    ax.bar(funnel_labels, funnel_vals, color=[muted, teal, teal, orange])
    ax.set_title("Cleaning funnel (row counts)")
    ax.tick_params(axis="x", rotation=15)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for i, v in enumerate(funnel_vals):
        ax.text(i, v, f"{v:,}", ha="center", va="bottom", fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "retail-cleaning-funnel.jpg", dpi=140, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.5, 4), dpi=140)
    ax.bar(
        [f"YTD {last_date.year}", f"MTD {metrics['mtd_month']}"],
        [ytd_rev / 1000, mtd_rev / 1000],
        color=[teal, orange],
    )
    ax.set_title("YTD vs MTD revenue (GBP thousands)")
    ax.set_ylabel("GBP k")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "retail-ytd-mtd.jpg", dpi=140, bbox_inches="tight")
    plt.close(fig)

    print("charts written")
    for path in sorted(OUT.glob("retail-*.jpg")):
        print(path.name, round(path.stat().st_size / 1024, 1), "KB")


if __name__ == "__main__":
    main()
