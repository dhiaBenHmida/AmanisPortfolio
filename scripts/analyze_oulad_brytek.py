"""Analyze OULAD for a BryTek-framed learning analytics portfolio case study.

Public Open University Learning Analytics Dataset (CC BY 4.0) used as a
stand-in for the kinds of decisions a BryTek instructor cockpit should surface.
This is not BryTek production data.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "oulad"
OUT = ROOT / "public" / "images" / "case_studies"
DERIVED = ROOT / "data" / "derived"

EARLY_DAYS = 14
PALETTE = {
    "ink": "#1a1f2e",
    "teal": "#2a9d8f",
    "coral": "#e76f51",
    "amber": "#e9c46a",
    "slate": "#6c757d",
    "pass": "#2a9d8f",
    "distinction": "#264653",
    "fail": "#e76f51",
    "withdrawn": "#9a3412",
}


def style_axes(ax: plt.Axes) -> None:
    ax.set_facecolor("#f7f5f2")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(colors=PALETTE["ink"])
    ax.yaxis.label.set_color(PALETTE["ink"])
    ax.xaxis.label.set_color(PALETTE["ink"])
    ax.title.set_color(PALETTE["ink"])


def save_fig(fig: plt.Figure, name: str) -> Path:
    path = OUT / name
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor="#f7f5f2")
    plt.close(fig)
    print("wrote", path)
    return path


def main() -> None:
    DERIVED.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    info = pd.read_csv(RAW / "studentInfo.csv")
    reg = pd.read_csv(RAW / "studentRegistration.csv")
    vle = pd.read_csv(
        RAW / "studentVle.csv",
        usecols=["code_module", "code_presentation", "id_student", "date", "sum_click"],
    )

    enrollments = len(info)
    students = int(info["id_student"].nunique())
    modules = int(info["code_module"].nunique())
    presentations = int(info.groupby(["code_module", "code_presentation"]).ngroups)

    outcome_counts = info["final_result"].value_counts().to_dict()
    info["success"] = info["final_result"].isin(["Pass", "Distinction"])
    info["at_risk"] = info["final_result"].isin(["Fail", "Withdrawn"])
    success_rate = float(info["success"].mean())
    at_risk_rate = float(info["at_risk"].mean())

    reg["unregistered"] = ~reg["date_unregistration"].astype(str).isin(["?", "nan", ""])
    unreg_rate = float(reg["unregistered"].mean())

    early = (
        vle[vle["date"] <= EARLY_DAYS]
        .groupby(["code_module", "code_presentation", "id_student"], as_index=False)["sum_click"]
        .sum()
        .rename(columns={"sum_click": "early_clicks"})
    )
    m = info.merge(early, on=["code_module", "code_presentation", "id_student"], how="left")
    m["early_clicks"] = m["early_clicks"].fillna(0)

    zero_early = m["early_clicks"] == 0
    zero_early_share = float(zero_early.mean())
    zero_early_at_risk = float(m.loc[zero_early, "at_risk"].mean())

    m["engagement_band"] = pd.qcut(
        m["early_clicks"],
        5,
        labels=["Q1 lowest", "Q2", "Q3", "Q4", "Q5 highest"],
        duplicates="drop",
    )
    band = (
        m.groupby("engagement_band", observed=True)
        .agg(
            enrollments=("id_student", "count"),
            at_risk_rate=("at_risk", "mean"),
            mean_early_clicks=("early_clicks", "mean"),
            success_rate=("success", "mean"),
        )
        .reset_index()
    )
    q1_at_risk = float(band.loc[band["engagement_band"] == "Q1 lowest", "at_risk_rate"].iloc[0])
    q5_at_risk = float(band.loc[band["engagement_band"] == "Q5 highest", "at_risk_rate"].iloc[0])

    by_module = (
        m.groupby("code_module")
        .agg(
            enrollments=("id_student", "count"),
            success_rate=("success", "mean"),
            withdraw_rate=("final_result", lambda s: float((s == "Withdrawn").mean())),
            fail_rate=("final_result", lambda s: float((s == "Fail").mean())),
            at_risk_rate=("at_risk", "mean"),
            mean_early_clicks=("early_clicks", "mean"),
        )
        .reset_index()
        .sort_values("at_risk_rate", ascending=False)
    )
    worst = by_module.iloc[0]
    best = by_module.sort_values("success_rate", ascending=False).iloc[0]

    # --- charts ---
    order = ["Distinction", "Pass", "Fail", "Withdrawn"]
    colors = [PALETTE["distinction"], PALETTE["pass"], PALETTE["fail"], PALETTE["withdrawn"]]
    vals = [outcome_counts.get(o, 0) for o in order]
    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    style_axes(ax)
    bars = ax.bar(order, vals, color=colors)
    ax.set_ylabel("Enrollments")
    ax.set_title("OULAD final outcomes (student x module presentations)")
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 200, f"{v:,}", ha="center", va="bottom", fontsize=9)
    save_fig(fig, "brytek-oulad-outcomes.jpg")

    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    style_axes(ax)
    ax.bar(band["engagement_band"].astype(str), band["at_risk_rate"] * 100, color=PALETTE["coral"])
    ax.set_ylabel("Fail or Withdrawn (%)")
    ax.set_xlabel(f"Early VLE clicks (days 0 to {EARLY_DAYS}), by quintile")
    ax.set_title("Early silence predicts later failure or withdrawal")
    ax.set_ylim(0, 100)
    for i, r in band.iterrows():
        ax.text(
            i,
            r["at_risk_rate"] * 100 + 2,
            f"{r['at_risk_rate'] * 100:.0f}%",
            ha="center",
            va="bottom",
            fontsize=9,
        )
    save_fig(fig, "brytek-oulad-early-risk.jpg")

    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    style_axes(ax)
    mod = by_module.sort_values("code_module")
    x = range(len(mod))
    ax.bar([i - 0.2 for i in x], mod["success_rate"] * 100, width=0.4, color=PALETTE["teal"], label="Pass + Distinction")
    ax.bar([i + 0.2 for i in x], mod["withdraw_rate"] * 100, width=0.4, color=PALETTE["withdrawn"], label="Withdrawn")
    ax.set_xticks(list(x))
    ax.set_xticklabels(mod["code_module"])
    ax.set_ylabel("% of enrollments")
    ax.set_title("Course health by module")
    ax.legend(frameon=False)
    ax.set_ylim(0, 100)
    save_fig(fig, "brytek-oulad-module-health.jpg")

    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    style_axes(ax)
    labels = ["Any early VLE activity", "Zero clicks in first 14 days"]
    rates = [
        float(m.loc[~zero_early, "at_risk"].mean()) * 100,
        zero_early_at_risk * 100,
    ]
    ax.bar(labels, rates, color=[PALETTE["teal"], PALETTE["coral"]])
    ax.set_ylabel("Fail or Withdrawn (%)")
    ax.set_title("Intervention queue: silent starters")
    ax.set_ylim(0, 100)
    for i, r in enumerate(rates):
        ax.text(i, r + 2, f"{r:.0f}%", ha="center", va="bottom", fontsize=10)
    save_fig(fig, "brytek-oulad-silent-starters.jpg")

    metrics = {
        "source": "Open University Learning Analytics Dataset (OULAD)",
        "license": "CC BY 4.0",
        "citation": "Kuzilek, Hlosta, Zdrahal. Nature Scientific Data 4:170171 (2017).",
        "enrollments": enrollments,
        "students": students,
        "modules": modules,
        "presentations": presentations,
        "outcome_counts": outcome_counts,
        "success_rate": success_rate,
        "at_risk_rate": at_risk_rate,
        "unregistration_rate": unreg_rate,
        "early_window_days": EARLY_DAYS,
        "zero_early_share": zero_early_share,
        "zero_early_at_risk": zero_early_at_risk,
        "q1_at_risk": q1_at_risk,
        "q5_at_risk": q5_at_risk,
        "engagement_bands": band.to_dict(orient="records"),
        "modules_table": by_module.to_dict(orient="records"),
        "worst_module": {
            "code_module": str(worst["code_module"]),
            "at_risk_rate": float(worst["at_risk_rate"]),
            "withdraw_rate": float(worst["withdraw_rate"]),
            "enrollments": int(worst["enrollments"]),
        },
        "best_module": {
            "code_module": str(best["code_module"]),
            "success_rate": float(best["success_rate"]),
            "enrollments": int(best["enrollments"]),
        },
        "charts": [
            "brytek-oulad-outcomes.jpg",
            "brytek-oulad-early-risk.jpg",
            "brytek-oulad-module-health.jpg",
            "brytek-oulad-silent-starters.jpg",
        ],
    }
    out_json = DERIVED / "brytek_oulad_metrics.json"
    out_json.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print("wrote", out_json)
    print(
        f"enrollments={enrollments:,} students={students:,} at_risk={at_risk_rate:.1%} "
        f"zero_early_at_risk={zero_early_at_risk:.1%} Q1={q1_at_risk:.1%} Q5={q5_at_risk:.1%}"
    )


if __name__ == "__main__":
    main()
