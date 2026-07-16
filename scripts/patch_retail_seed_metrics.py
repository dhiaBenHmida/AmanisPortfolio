"""Patch retail-kpi-storytelling seed with computed Online Retail II metrics and charts."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SEED = ROOT / "backend" / "app" / "seed_data.json"
METRICS = ROOT / "data" / "derived" / "retail_metrics.json"


def gbp(n: float) -> str:
    if n >= 1_000_000:
        return f"£{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"£{n / 1_000:.0f}k"
    return f"£{n:.0f}"


def main() -> None:
    data = json.loads(SEED.read_text(encoding="utf-8"))
    m = json.loads(METRICS.read_text(encoding="utf-8"))
    retail = next(p for p in data["projects"] if p["slug"] == "retail-kpi-storytelling")

    champ = next(s for s in m["segments"] if s["Segment"] == "Champions")
    at_risk = next(s for s in m["segments"] if s["Segment"] == "At Risk")
    loyal = next(s for s in m["segments"] if s["Segment"] == "Loyal")

    retail["image"] = "/images/case_studies/retail-monthly-revenue.jpg"
    retail["impact"] = (
        f"On cleaned Online Retail II sales ({m['date_min']} to {m['date_max']}), the analysis covers "
        f"{m['customers']:,} customers, {m['orders']:,} orders, and {gbp(m['total_revenue_gbp'])} revenue "
        f"(AOV {gbp(m['aov_gbp'])}). Champions are {champ['share_customers'] * 100:.0f}% of customers but "
        f"{champ['share_revenue'] * 100:.0f}% of revenue. Peak month {m['peak_month']} hit "
        f"{gbp(m['peak_month_revenue_gbp'])}."
    )
    retail["metrics"] = [
        {
            "value": f"{m['customers']:,}",
            "label": "Customers",
            "detail": "After dropping missing CustomerID rows.",
        },
        {
            "value": f"{m['orders']:,}",
            "label": "Orders",
            "detail": "Non-cancelled invoices with positive quantity.",
        },
        {
            "value": gbp(m["total_revenue_gbp"]),
            "label": "Clean revenue",
            "detail": "Quantity x UnitPrice on cleaned sales lines.",
        },
        {
            "value": f"{champ['share_revenue'] * 100:.0f}%",
            "label": "Champions revenue",
            "detail": f"{champ['customers']:,} Champions drive most cleaned revenue.",
        },
    ]

    sections = {s["key"]: s for s in retail["sections"]}
    sections["impact"]["body"] = (
        "Computed on the public Online Retail II extract after the cleaning rules in this study.\n\n"
        f"Clean window: {m['date_min']} to {m['date_max']}. Raw rows {m['raw_rows']:,}; "
        f"missing CustomerID {m['missing_customer_id']:,}; cancellations among identified customers "
        f"{m['cancellations']:,}; cleaned sales lines {m['clean_line_rows']:,}.\n\n"
        f"Trading snapshot: {m['customers']:,} customers, {m['orders']:,} orders, "
        f"{gbp(m['total_revenue_gbp'])} revenue, AOV {gbp(m['aov_gbp'])}. "
        f"Peak month {m['peak_month']} at {gbp(m['peak_month_revenue_gbp'])}. "
        f"YTD {m['ytd_year']} {gbp(m['ytd_revenue_gbp'])}; MTD {m['mtd_month']} {gbp(m['mtd_revenue_gbp'])}."
    )

    sections["process-clean"]["images"] = [
        {
            "src": "/images/case_studies/retail-cleaning-funnel.jpg",
            "alt": "Cleaning funnel from raw Online Retail II rows to positive sales lines",
            "caption": (
                f"Funnel: {m['raw_rows']:,} raw rows down to {m['clean_line_rows']:,} "
                "positive sales lines with CustomerID."
            ),
        }
    ]
    sections["process-clean"]["imageLayout"] = "stack"

    sections["process-sql"]["images"] = [
        {
            "src": "/images/case_studies/retail-top-countries.jpg",
            "alt": "Top countries by cleaned revenue",
            "caption": "Country mix after cleaning: UK concentration with international wholesale tails.",
        }
    ]

    sections["process-rfm"]["images"] = [
        {
            "src": "/images/case_studies/retail-rfm-customers.jpg",
            "alt": "Customers by RFM segment",
            "caption": (
                f"Champions {champ['customers']:,} · Loyal {loyal['customers']:,} · "
                f"At Risk {at_risk['customers']:,}."
            ),
        },
        {
            "src": "/images/case_studies/retail-rfm-revenue.jpg",
            "alt": "Revenue share by RFM segment",
            "caption": (
                f"Champions hold {champ['share_revenue'] * 100:.0f}% of cleaned revenue "
                f"with {champ['share_customers'] * 100:.0f}% of customers."
            ),
        },
    ]
    sections["process-rfm"]["imageLayout"] = "row"

    sections["process-kpi"]["images"] = [
        {
            "src": "/images/case_studies/retail-monthly-revenue.jpg",
            "alt": "Monthly cleaned revenue over Online Retail II period",
            "caption": (
                f"Monthly pulse with peak in {m['peak_month']} at "
                f"{gbp(m['peak_month_revenue_gbp'])}."
            ),
        },
        {
            "src": "/images/case_studies/retail-ytd-mtd.jpg",
            "alt": "YTD versus MTD revenue bars",
            "caption": (
                f"YTD {m['ytd_year']} {gbp(m['ytd_revenue_gbp'])} vs "
                f"MTD {m['mtd_month']} {gbp(m['mtd_revenue_gbp'])}."
            ),
        },
    ]
    sections["process-kpi"]["imageLayout"] = "row"

    sections["decision"]["body"] = (
        f"DECISION - Protect Champions ({champ['customers']:,} customers, "
        f"{champ['share_revenue'] * 100:.0f}% of revenue) with white-glove retention, "
        f"keep Loyal ({loyal['customers']:,}) in a steady nurture track, and run a focused "
        f"reactivation offer for At Risk ({at_risk['customers']:,} customers, "
        f"{at_risk['share_revenue'] * 100:.0f}% of revenue) who used to spend.\n\n"
        "INSIGHT - The point of RFM is not prettier colors. It is a shorter meeting: fewer "
        "customers discussed, clearer owners, and a mix you can defend with recency and spend evidence.\n\n"
        "DATA QUESTION - After the campaign window, which At Risk customers returned, and did "
        "Champions hold their share of YTD revenue?"
    )
    sections["decision"]["images"] = [
        {
            "src": "/images/case_studies/retail-rfm-revenue.jpg",
            "alt": "Revenue concentration by RFM segment for decision mix",
            "caption": "Decision mix follows revenue concentration, not equal customer counts.",
        }
    ]

    sections["future"]["body"] = (
        "Charts and cleaned KPIs are now attached from the Online Retail II run. Next depth: "
        "cohort retention and country-mix cuts still tied to the same holiday-priority question, "
        "plus any Formation SQL artifacts you want shown as process proof."
    )
    retail["nextSteps"] = (
        "Optional depth: cohort retention and UK vs international wholesaler cuts, "
        "still framed by the holiday-priority decision."
    )

    SEED.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("patched", retail["slug"])
    print(retail["impact"])


if __name__ == "__main__":
    main()
