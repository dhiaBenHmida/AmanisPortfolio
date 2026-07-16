"""Insert / refresh brytek-learning-analytics in seed_data.json from OULAD metrics."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SEED = ROOT / "backend" / "app" / "seed_data.json"
METRICS = ROOT / "data" / "derived" / "brytek_oulad_metrics.json"


def pct(x: float) -> str:
    return f"{x * 100:.0f}%"


def build_project(m: dict) -> dict:
    worst = m["worst_module"]
    best = m["best_module"]
    oc = m["outcome_counts"]

    return {
        "slug": "brytek-learning-analytics",
        "image": "/images/case_studies/brytek-oulad-early-risk.jpg",
        "title": "BryTek | Learning Analytics for Instructor Decisions",
        "tools": [
            "Python",
            "pandas",
            "Matplotlib",
            "Learning analytics",
            "OULAD",
            "VLE engagement",
        ],
        "impact": (
            f"On OULAD ({m['enrollments']:,} enrollments across {m['modules']} modules), "
            f"{pct(m['at_risk_rate'])} end Fail or Withdrawn. Silent starters "
            f"({pct(m['zero_early_share'])} with zero VLE clicks in the first "
            f"{m['early_window_days']} days) reach {pct(m['zero_early_at_risk'])} at-risk. "
            f"Lowest early-engagement quintile: {pct(m['q1_at_risk'])} at-risk vs "
            f"{pct(m['q5_at_risk'])} in the highest."
        ),
        "problem": (
            "An instructor cockpit that only shows enrollments and revenue still leaves teachers "
            "guessing who needs help this week. BryTek's dashboard UX needs a data story that "
            "turns engagement into an intervention queue."
        ),
        "summary": (
            "Data lens companion to the BryTek UX study. I use the public Open University Learning "
            "Analytics Dataset (OULAD, CC BY 4.0) as a real EdTech stand-in: demographics, assessments, "
            "and VLE click summaries for 32k+ students. The question is the same one a BryTek teacher "
            "dashboard should answer: who needs outreach before they fail or withdraw. Honest framing: "
            "this is public OU data, not BryTek production telemetry."
        ),
        "tagline": "OULAD learning analytics framed for BryTek instructor intervention decisions.",
        "approach": (
            "Start from the BryTek instructor job (morning course health), ground it in OULAD outcomes "
            "and early VLE activity, then leave with a decision mix: silent starters first, then "
            "low-engagement bands, with module-level health as context."
        ),
        "category": "Data analysis",
        "highlights": [
            "Paired with the BryTek UX case: same instructor cockpit question, measured on real public LMS data.",
            "Grounded in OULAD (Nature Scientific Data / UCI), CC BY 4.0, not synthetic grades.",
            "Early VLE silence (first 14 days) as the primary risk signal for Fail or Withdrawn.",
            "Module health view so teachers see which courses need staffing attention, not only which students.",
        ],
        "externalUrl": "https://analyse.kmi.open.ac.uk/open_dataset",
        "externalLabel": "OULAD source",
        "timeline": "Portfolio data study · OULAD (2013 - 2014 presentations)",
        "platform": "Learning analytics (Python / pandas / EdTech decision framing)",
        "role": "Data analyst",
        "roleBody": (
            "Owned the analytical narrative for a BryTek-framed instructor decision: source honesty, "
            "early-engagement risk signal, module health, and an intervention queue a teacher could act on. "
            "Validate how this sits beside your Formation Data and BI craft and the BryTek UX entry."
        ),
        "goal": (
            "Show that BryTek's instructor cockpit is not only a UI: it should surface who is going silent "
            "early enough to intervene, using real public learning analytics as proof of method."
        ),
        "metrics": [
            {
                "value": f"{m['enrollments']:,}",
                "label": "Enrollments",
                "detail": f"{m['students']:,} students across {m['presentations']} module presentations.",
            },
            {
                "value": pct(m["at_risk_rate"]),
                "label": "At-risk rate",
                "detail": "Share ending Fail or Withdrawn.",
            },
            {
                "value": pct(m["zero_early_at_risk"]),
                "label": "Silent starters",
                "detail": (
                    f"At-risk among the {pct(m['zero_early_share'])} with zero clicks "
                    f"in the first {m['early_window_days']} days."
                ),
            },
            {
                "value": f"{pct(m['q1_at_risk'])} vs {pct(m['q5_at_risk'])}",
                "label": "Q1 vs Q5 risk",
                "detail": "Lowest vs highest early-engagement quintiles.",
            },
        ],
        "sections": [
            {
                "key": "introduction",
                "title": "Introduction",
                "layout": "stack",
                "imageLayout": "stack",
                "body": (
                    "This is the data lens beside BryTek Online Learning (UX). The design study gives "
                    "teachers a cockpit for enrollments, ratings, and earnings. This study asks what that "
                    "cockpit should prioritize when the signal is learning behaviour, not revenue.\n\n"
                    "I use the Open University Learning Analytics Dataset (OULAD): anonymized course, "
                    "student, assessment, and Virtual Learning Environment (VLE) interaction data from "
                    "Open University presentations in 2013 and 2014. License: CC BY 4.0. Citation: "
                    "Kuzilek, Hlosta, Zdrahal, Nature Scientific Data 4:170171 (2017).\n\n"
                    "Framing rule: OULAD is a public EdTech proxy. It is not BryTek production data. "
                    "The point is transferable decisions a BryTek-style instructor dashboard should surface.\n\n"
                    "MY ROLE - Data analyst framing the instructor question, early-engagement risk, "
                    "module health, and intervention narrative."
                ),
                "images": [],
            },
            {
                "key": "problem",
                "title": "Problem",
                "layout": "stack",
                "imageLayout": "stack",
                "body": (
                    "PROBLEM - A teacher opens BryTek and sees headcount and money. Without engagement "
                    "risk, the morning view cannot say who needs a message today.\n\n"
                    "EXAMPLE - Two courses can show similar enrollment counts while one is filled with "
                    "learners who never opened the VLE in the first two weeks.\n\n"
                    "IMPACT - Outreach waits until after the first failed assessment. Retention work "
                    "arrives too late.\n\n"
                    "PROBLEM - Public LMS logs are noisy: withdrawals, fails, distinctions, and silent "
                    "accounts sit in the same table until you define an outcome and a time window.\n\n"
                    "EXAMPLE - OULAD labels final_result as Distinction, Pass, Fail, or Withdrawn, and "
                    "stores daily VLE click summaries that only help if you pick an early window.\n\n"
                    "IMPACT - Without those definitions, 'engagement' stays a vague chart instead of a queue."
                ),
                "images": [],
            },
            {
                "key": "goals",
                "title": "Goals",
                "layout": "stack",
                "imageLayout": "stack",
                "body": (
                    "BUSINESS GOALS - Prove that BryTek's instructor product can be backed by a real "
                    "learning-analytics decision story, not only UI fiction on the dashboard cards.\n\n"
                    "USER GOALS - Give an instructor a shortlist: silent starters first, then low early "
                    "engagement, with module context so staffing attention follows course risk.\n\n"
                    "Give a portfolio reader an honest source trail (OULAD / UCI / OU Analyse) they can verify."
                ),
                "images": [],
            },
            {
                "key": "impact",
                "title": "Impact",
                "layout": "stack",
                "imageLayout": "stack",
                "body": (
                    f"Computed on public OULAD after joining studentInfo to early VLE activity "
                    f"(days 0 to {m['early_window_days']}).\n\n"
                    f"Scale: {m['enrollments']:,} enrollments, {m['students']:,} students, "
                    f"{m['modules']} modules, {m['presentations']} presentations.\n\n"
                    f"Outcomes: Distinction {oc.get('Distinction', 0):,}, Pass {oc.get('Pass', 0):,}, "
                    f"Fail {oc.get('Fail', 0):,}, Withdrawn {oc.get('Withdrawn', 0):,}. "
                    f"Combined Fail + Withdrawn: {pct(m['at_risk_rate'])}.\n\n"
                    f"Silent starters ({pct(m['zero_early_share'])} with zero early clicks): "
                    f"{pct(m['zero_early_at_risk'])} at-risk. "
                    f"Lowest early-engagement quintile {pct(m['q1_at_risk'])} at-risk vs "
                    f"{pct(m['q5_at_risk'])} in the highest. "
                    f"Highest-risk module in this cut: {worst['code_module']} "
                    f"({pct(worst['at_risk_rate'])} at-risk, {pct(worst['withdraw_rate'])} withdrawn)."
                ),
                "images": [],
            },
            {
                "key": "stakeholders",
                "title": "Stakeholders",
                "layout": "stack",
                "imageLayout": "stack",
                "body": (
                    "Primary reader: a BryTek Teacher using the instructor cockpit from the UX case.\n\n"
                    "JOB TO BE DONE - When I open BryTek in the morning, I want a clear queue of learners "
                    "going silent so I message the right people before they withdraw.\n\n"
                    "Secondary reader: a platform owner comparing course health across modules, and an "
                    "analyst who must defend the early-window definition in that same review."
                ),
                "images": [
                    {
                        "src": "/images/case_studies/brytek-instructor-dashboard.jpg",
                        "alt": "BryTek instructor dashboard from the UX case study",
                        "caption": "UX companion: the cockpit this data story is meant to feed.",
                    }
                ],
            },
            {
                "key": "scenario",
                "title": "Scenario: who needs outreach",
                "layout": "stack",
                "imageLayout": "stack",
                "body": (
                    "DATA QUESTION - In the first two weeks of a presentation, which enrollments should "
                    "enter an instructor intervention queue because early VLE silence predicts Fail or Withdrawn?\n\n"
                    "Hugging Face check before locking the source: edu-interactions is AI-tutor oriented; "
                    "student-engagement-and-performance is only ~50 rows; OULAD-derived HF artifacts are "
                    "prompts or benchmarks, not the raw LMS tables. OULAD via OU Analyse / UCI remains the "
                    "best public fit for a BryTek instructor story.\n\n"
                    "The storyboard: define outcomes, measure early clicks, rank risk bands, read module "
                    "health, then leave with a decision mix tied to the BryTek teacher job."
                ),
                "images": [],
            },
            {
                "key": "process-outcomes",
                "title": "Process: define the risk outcome",
                "layout": "stack",
                "imageLayout": "stack",
                "body": (
                    "Grain is student x module presentation (enrollment). Final result is the outcome label.\n\n"
                    "INSIGHT - Pass and Distinction are success. Fail and Withdrawn are the at-risk bucket "
                    f"for intervention planning ({pct(m['at_risk_rate'])} of enrollments in this extract).\n\n"
                    "That binary is deliberate for a teacher queue. Finer grading can come later; the first "
                    "cockpit job is who needs a human touch."
                ),
                "images": [
                    {
                        "src": "/images/case_studies/brytek-oulad-outcomes.jpg",
                        "alt": "OULAD final outcome counts",
                        "caption": (
                            f"Outcomes: Pass {oc.get('Pass', 0):,} · Withdrawn {oc.get('Withdrawn', 0):,} · "
                            f"Fail {oc.get('Fail', 0):,} · Distinction {oc.get('Distinction', 0):,}."
                        ),
                    }
                ],
            },
            {
                "key": "process-early",
                "title": "Process: early VLE engagement",
                "layout": "stack",
                "imageLayout": "row",
                "body": (
                    f"Early window: days 0 to {m['early_window_days']} in OULAD's relative course calendar. "
                    "Sum of VLE clicks per enrollment. Missing VLE rows count as zero early clicks.\n\n"
                    f"INSIGHT - Risk falls as early activity rises: {pct(m['q1_at_risk'])} at-risk in the "
                    f"lowest quintile vs {pct(m['q5_at_risk'])} in the highest. "
                    f"Silent starters ({pct(m['zero_early_share'])} of enrollments) hit "
                    f"{pct(m['zero_early_at_risk'])} Fail or Withdrawn.\n\n"
                    "This is the signal BryTek's recent-activity and course-health widgets should amplify."
                ),
                "images": [
                    {
                        "src": "/images/case_studies/brytek-oulad-early-risk.jpg",
                        "alt": "At-risk rate by early VLE engagement quintile",
                        "caption": (
                            f"Q1 {pct(m['q1_at_risk'])} at-risk vs Q5 {pct(m['q5_at_risk'])} "
                            f"(first {m['early_window_days']} days)."
                        ),
                    },
                    {
                        "src": "/images/case_studies/brytek-oulad-silent-starters.jpg",
                        "alt": "At-risk rate for silent starters versus learners with early activity",
                        "caption": (
                            f"Zero early clicks: {pct(m['zero_early_at_risk'])} at-risk "
                            f"({pct(m['zero_early_share'])} of enrollments)."
                        ),
                    },
                ],
            },
            {
                "key": "process-modules",
                "title": "Process: course health by module",
                "layout": "stack",
                "imageLayout": "stack",
                "body": (
                    "Teachers do not only triage people. They also need to know which courses are structurally harder.\n\n"
                    f"INSIGHT - Module {worst['code_module']} shows the highest at-risk rate in this cut "
                    f"({pct(worst['at_risk_rate'])}, withdraw {pct(worst['withdraw_rate'])}, "
                    f"{worst['enrollments']:,} enrollments). "
                    f"Module {best['code_module']} leads success at {pct(best['success_rate'])}.\n\n"
                    "On BryTek, that belongs next to My Courses: a health stripe, not only a title list."
                ),
                "images": [
                    {
                        "src": "/images/case_studies/brytek-oulad-module-health.jpg",
                        "alt": "Pass and withdrawal rates by OULAD module",
                        "caption": "Module health: success vs withdrawal side by side.",
                    }
                ],
            },
            {
                "key": "decision",
                "title": "Decision storyboard",
                "layout": "stack",
                "imageLayout": "stack",
                "body": (
                    f"DECISION - Week-2 outreach queue: message every silent starter first "
                    f"({pct(m['zero_early_share'])} of enrollments, {pct(m['zero_early_at_risk'])} at-risk), "
                    f"then prioritize the lowest early-engagement quintile ({pct(m['q1_at_risk'])} at-risk). "
                    f"Staffing review: inspect module {worst['code_module']} for content or support gaps "
                    f"before the next presentation.\n\n"
                    "INSIGHT - The BryTek dashboard earns its KPI row when those queues exist. "
                    "Enrollments and earnings without an intervention list are still a pretty empty morning.\n\n"
                    "DATA QUESTION - After two weeks of outreach, did silent starters return to the VLE, "
                    "and did Fail + Withdrawn fall in the next assessment window?"
                ),
                "images": [
                    {
                        "src": "/images/case_studies/brytek-oulad-silent-starters.jpg",
                        "alt": "Silent starter risk for the intervention decision",
                        "caption": "Decision anchor: silent starters enter the queue first.",
                    }
                ],
            },
            {
                "key": "learnings",
                "title": "What we learned",
                "layout": "stack",
                "imageLayout": "stack",
                "body": (
                    "Hugging Face is useful for discovery, but the best BryTek-shaped public table set is still "
                    "OULAD from OU Analyse / UCI, not a 50-row engagement toy set.\n\n"
                    "Say the source out loud. Claiming OULAD as BryTek production data would break trust.\n\n"
                    "Early windows beat lifetime averages for instructor action. Teachers intervene in weeks, "
                    "not after the final result lands.\n\n"
                    "Pair the UX and data entries. Design shows the cockpit; analytics shows what should fill it."
                ),
                "images": [],
            },
            {
                "key": "future",
                "title": "Future",
                "layout": "stack",
                "imageLayout": "stack",
                "body": (
                    "Next depth on the same question: first-assessment timing, weekly engagement trajectories, "
                    "and a lightweight risk score that could sit behind BryTek's recent-activity panel. "
                    "Keep Retail KPI Storytelling as the separate commerce data study."
                ),
                "images": [],
            },
        ],
    }


def main() -> None:
    data = json.loads(SEED.read_text(encoding="utf-8"))
    m = json.loads(METRICS.read_text(encoding="utf-8"))
    project = build_project(m)

    projects = data["projects"]
    idx = next((i for i, p in enumerate(projects) if p["slug"] == "brytek-learning-analytics"), None)
    if idx is None:
        brytek_ux = next(i for i, p in enumerate(projects) if p["slug"] == "brytek-online-learning")
        projects.insert(brytek_ux + 1, project)
    else:
        projects[idx] = project

    highlight = {
        "slug": "brytek-learning-analytics",
        "image": "/images/case_studies/brytek-oulad-early-risk.jpg",
        "title": "BryTek data: early VLE risk for instructor outreach",
        "meta": "Data analysis · OULAD · Learning analytics",
    }
    highlights = data["highlights"]
    h_idx = next((i for i, h in enumerate(highlights) if h["slug"] == "brytek-learning-analytics"), None)
    if h_idx is None:
        ux_h = next(i for i, h in enumerate(highlights) if h["slug"] == "brytek-online-learning")
        highlights.insert(ux_h + 1, highlight)
    else:
        highlights[h_idx] = highlight

    SEED.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("patched", SEED, "slug=brytek-learning-analytics")


if __name__ == "__main__":
    main()
