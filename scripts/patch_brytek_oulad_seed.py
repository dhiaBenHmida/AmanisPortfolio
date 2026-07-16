"""Insert / refresh brytek-learning-analytics in seed_data.json from Open University Learning Analytics Dataset metrics."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SEED = ROOT / "backend" / "app" / "seed_data.json"
METRICS = ROOT / "data" / "derived" / "brytek_oulad_metrics.json"
# Served from the API static mount so Netlify credits are not required for new assets.
MEDIA_BASE = "https://amanisportfolio-production.up.railway.app"


def media(path: str) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        return path
    return f"{MEDIA_BASE}{path}"


def pct(x: float) -> str:
    return f"{x * 100:.0f}%"


def build_project(m: dict) -> dict:
    worst = m["worst_module"]
    best = m["best_module"]
    oc = m["outcome_counts"]

    return {
        "slug": "brytek-learning-analytics",
        "image": media("/images/case_studies/brytek-oulad-early-risk.jpg"),
        "title": "BryTek | Learning Analytics for Instructor Decisions",
        "tools": [
            "Python",
            "pandas",
            "Matplotlib",
            "Learning analytics",
            "Open University Learning Analytics Dataset",
            "VLE engagement",
        ],
        "impact": (
            f"On the Open University Learning Analytics Dataset ({m['enrollments']:,} enrollments across {m['modules']} modules), "
            f"{pct(m['at_risk_rate'])} end Fail or Withdrawn. Silent starters "
            f"({pct(m['zero_early_share'])} with zero VLE clicks in the first "
            f"{m['early_window_days']} days) reach {pct(m['zero_early_at_risk'])} at-risk. "
            f"Lowest early-engagement quintile: {pct(m['q1_at_risk'])} at-risk vs "
            f"{pct(m['q5_at_risk'])} in the highest."
        ),
        "problem": (
            "In online teaching, learners can disappear quietly. A BryTek instructor who only sees "
            "enrollments and earnings cannot tell who has gone silent early enough to help, so support "
            "arrives after fail or withdrawal instead of before. A client cannot approve that cockpit "
            "on UI fiction alone."
        ),
        "summary": (
            "I worked the BryTek data study together with the BryTek UX case to justify the product to "
            "the client: design shows how the platform feels, and this analysis shows why the instructor "
            "cockpit must surface early retention risk. Distance learning creates a human gap: teachers "
            "cannot see the room, so early Virtual Learning Environment (VLE) silence often warns that a "
            "learner is drifting toward fail or withdrawal. I ground that job in the public Open "
            "University Learning Analytics Dataset (CC BY 4.0), published for learning-analytics research "
            "(Kuzilek, Hlosta, Zdrahal, Nature Scientific Data, 2017). Public Open University "
            "data is used as a scientific stand-in, not BryTek production telemetry."
        ),
        "tagline": (
            "Retention evidence for BryTek, paired with UX, to justify the product to the client."
        ),
        "approach": (
            "Treat design and data as one client justification package. Start from the human retention "
            "problem in online teaching, place it in the Open University learning-analytics tradition "
            "(early at-risk detection from VLE behaviour), then measure outcomes and early clicks on the "
            "Open University Learning Analytics Dataset so the BryTek instructor queue has a defensible "
            "basis the client can fund."
        ),
        "category": "Data analysis",
        "highlights": [
            "Paired with BryTek UX so the client sees product shape and retention evidence in one case.",
            "Human stake: online teachers cannot see the room; early silence warns before fail or withdrawal.",
            "Scientific stake: Open University learning-analytics research on early at-risk detection from VLE behaviour.",
            "Uses the Open University Learning Analytics Dataset (Nature Scientific Data / UCI, CC BY 4.0) as public evidence.",
        ],
        "externalUrl": "https://analyse.kmi.open.ac.uk/open_dataset",
        "externalLabel": "Open University Learning Analytics Dataset",
        "timeline": "Client justification study: data + paired BryTek UX · Open University Learning Analytics Dataset (2013 - 2014)",
        "platform": "Learning analytics (Python / pandas / EdTech decision framing)",
        "role": "Data analyst (paired with UX design)",
        "roleBody": (
            "Owned the analytical half of the client justification package: why the study exists "
            "(human retention + scientific tradition), source honesty, early-engagement risk, module "
            "health, and an intervention queue a BryTek teacher could act on, delivered beside the UX "
            "case so the client could approve both product and evidence."
        ),
        "goal": (
            "Help the client say yes to BryTek with evidence: prove the instructor cockpit should "
            "surface who is going silent early, using a public learning-analytics dataset published for "
            "this class of retention questions."
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
                    "I worked this data study together with the BryTek UX case to justify the product "
                    "to the client. Design alone shows screens. Design plus retention evidence shows why "
                    "those screens deserve budget.\n\n"
                    "This study exists because online teaching hides the human signal that a classroom "
                    "makes obvious. On BryTek, a teacher can see enrollments, ratings, and earnings. What "
                    "they still need is an early answer to a quieter question: who has stopped showing up "
                    "in the learning environment before the first failed assessment or a withdrawal letter.\n\n"
                    "The UX case designed that instructor cockpit. This data case fills it with a "
                    "retention logic learning-analytics research already treats as serious work, so the "
                    "client can approve BryTek with both product shape and evidence in hand.\n\n"
                    "MY ROLE - Data analyst on the client justification package: human and scientific "
                    "context, then early engagement risk on a public Open University dataset, paired with UX."
                ),
                "images": [],
            },
            {
                "key": "context",
                "title": "Why this study: human and scientific context",
                "layout": "stack",
                "imageLayout": "stack",
                "body": (
                    "CLIENT CONTEXT - The brief needed more than a pretty instructor dashboard. I owned "
                    "both the BryTek design study and this data study so the client could decide with a "
                    "full case: what the product looks like, and why early learner outreach belongs in "
                    "scope. Approving UX without retention evidence would leave the cockpit half-justified.\n\n"
                    "HUMAN CONTEXT - In distance and online learning, absence is easy to miss. A learner "
                    "can register, open nothing, and drift toward fail or withdrawal without a corridor "
                    "conversation. Tutors and support teams only intervene if the product surfaces risk "
                    "while there is still time. That is the morning job behind BryTek's teacher dashboard: "
                    "not prettier KPIs, but a shortlist of people who need a human message this week.\n\n"
                    "SCIENTIFIC CONTEXT - Learning analytics exists to use learner data to improve the "
                    "learning experience and guide support. At the Open University, that line of work "
                    "became operational in systems such as OU Analyse, built for early identification of "
                    "students at risk of failing so tutors and Student Support Teams can act. The Open "
                    "University Learning Analytics Dataset was published so researchers and practitioners "
                    "can study those questions with real, anonymized course, demographic, assessment, and "
                    "Virtual Learning Environment (VLE) interaction data from 2013 and 2014 presentations "
                    "(Kuzilek, Hlosta, Zdrahal, Nature Scientific Data 4:170171, 2017; CC BY 4.0; also "
                    "available via UCI and OU Analyse).\n\n"
                    "WHY THIS DATASET HERE - BryTek does not ship production LMS logs in a client pitch. "
                    "The Open University Learning Analytics Dataset is the public evidence base that "
                    "matches the same job: early risk from learning behaviour, not invented grades. This "
                    "analysis does not claim to reproduce OU Analyse as a product. It borrows the "
                    "scientific question (who is at risk early?) and turns it into a BryTek instructor "
                    "decision story the client can fund beside the UX."
                ),
                "images": [],
            },
            {
                "key": "problem",
                "title": "Problem",
                "layout": "stack",
                "imageLayout": "stack",
                "body": (
                    "PROBLEM - Online teachers lose the room. Without an engagement risk view, BryTek's "
                    "morning cockpit cannot tell who needs outreach today.\n\n"
                    "EXAMPLE - Two courses can show similar enrollment counts while one is filled with "
                    "learners who never opened the VLE in the first two weeks.\n\n"
                    "IMPACT - Support waits until after a failed assessment or a withdrawal. The human "
                    "cost is a learner who might have stayed with one timely message; the product cost is "
                    "a dashboard that looks busy and still fails the teacher.\n\n"
                    "PROBLEM - Retention research needs clean outcome and time definitions. Raw LMS tables "
                    "mix Pass, Distinction, Fail, Withdrawn, and daily click summaries until you choose "
                    "what 'at risk' means and how early you look.\n\n"
                    "EXAMPLE - The Open University Learning Analytics Dataset labels final results and "
                    "stores VLE click summaries on a relative course calendar. Those fields only become "
                    "actionable when you define an early window and an intervention outcome.\n\n"
                    "IMPACT - Without those definitions, 'engagement' stays a decorative chart instead of "
                    "a queue a teacher can defend."
                ),
                "images": [],
            },
            {
                "key": "goals",
                "title": "Goals",
                "layout": "stack",
                "imageLayout": "stack",
                "body": (
                    "BUSINESS GOALS - Give the client a clear case for BryTek: retention evidence that "
                    "stands beside the UX package, so approving the instructor product is not a leap of faith.\n\n"
                    "Show that BryTek's instructor cockpit answers a real retention problem "
                    "learning-analytics research already takes seriously.\n\n"
                    "USER GOALS - Give a BryTek teacher a shortlist: silent starters first, then low early "
                    "engagement, with module context so staffing follows course risk.\n\n"
                    "Give the client the human reason (protect drifting learners) and the scientific "
                    "reason (Open University early at-risk tradition + published dataset) in one story "
                    "they can verify before build."
                ),
                "images": [],
            },
            {
                "key": "impact",
                "title": "Impact",
                "layout": "stack",
                "imageLayout": "stack",
                "body": (
                    f"Computed on the public Open University Learning Analytics Dataset after joining studentInfo to early VLE activity "
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
                    f"({pct(worst['at_risk_rate'])} at-risk, {pct(worst['withdraw_rate'])} withdrawn).\n\n"
                    "Those numbers matter because they quantify the human gap: a large share of "
                    "enrollments end badly, and the worst outcomes concentrate where early VLE activity "
                    "never starts."
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
                    "Secondary readers: a platform owner comparing course health across modules, and an "
                    "analyst who must defend the early-window definition against the Open University "
                    "learning-analytics tradition in that same review."
                ),
                "images": [
                    {
                        "src": media("/images/case_studies/brytek-instructor-dashboard.jpg"),
                        "alt": "BryTek instructor dashboard from the UX case study",
                        "caption": "UX companion: the cockpit this retention story is meant to feed.",
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
                    "That question is not arbitrary. Open University research on at-risk detection treats "
                    "early engagement with the Virtual Learning Environment as a practical signal for "
                    "tutor and support action. This portfolio study asks the same question in BryTek "
                    "language: who should the teacher message now?\n\n"
                    "Source choice follows that context. Thin Hugging Face engagement samples and "
                    "AI-tutor grade logs do not match an instructor cockpit. The Open University Learning "
                    "Analytics Dataset does: real module presentations, final results, and daily VLE "
                    "click summaries published for learning-analytics research.\n\n"
                    "The storyboard: define the retention outcome, measure early clicks, rank risk bands, "
                    "read module health, then leave with a decision mix a teacher can own."
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
                    "That binary matches the human job. Before finer grading models, a teacher needs to "
                    "know who is drifting out of the course entirely."
                ),
                "images": [
                    {
                        "src": media("/images/case_studies/brytek-oulad-outcomes.jpg"),
                        "alt": "Open University Learning Analytics Dataset final outcome counts",
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
                    f"Early window: days 0 to {m['early_window_days']} on the Open University Learning "
                    "Analytics Dataset relative course calendar. Sum of VLE clicks per enrollment. "
                    "Missing VLE rows count as zero early clicks. The window is short on purpose: "
                    "retention action is useful in the first weeks, not after the final result lands.\n\n"
                    f"INSIGHT - Risk falls as early activity rises: {pct(m['q1_at_risk'])} at-risk in the "
                    f"lowest quintile vs {pct(m['q5_at_risk'])} in the highest. "
                    f"Silent starters ({pct(m['zero_early_share'])} of enrollments) hit "
                    f"{pct(m['zero_early_at_risk'])} Fail or Withdrawn.\n\n"
                    "That pattern is why BryTek's recent-activity and course-health widgets should amplify "
                    "early silence, not only lifetime averages."
                ),
                "images": [
                    {
                        "src": media("/images/case_studies/brytek-oulad-early-risk.jpg"),
                        "alt": "At-risk rate by early VLE engagement quintile",
                        "caption": (
                            f"Q1 {pct(m['q1_at_risk'])} at-risk vs Q5 {pct(m['q5_at_risk'])} "
                            f"(first {m['early_window_days']} days)."
                        ),
                    },
                    {
                        "src": media("/images/case_studies/brytek-oulad-silent-starters.jpg"),
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
                        "src": media("/images/case_studies/brytek-oulad-module-health.jpg"),
                        "alt": "Pass and withdrawal rates by Open University Learning Analytics Dataset module",
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
                    "Enrollments and earnings without an intervention list leave the human retention "
                    "problem unsolved.\n\n"
                    "DATA QUESTION - After two weeks of outreach, did silent starters return to the VLE, "
                    "and did Fail + Withdrawn fall in the next assessment window?"
                ),
                "images": [
                    {
                        "src": media("/images/case_studies/brytek-oulad-silent-starters.jpg"),
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
                    "A client justification needs a reason before it needs a chart. Here the reason is "
                    "triple: protect online learners who go quiet, sit that job inside a published Open "
                    "University learning-analytics tradition, and deliver it beside BryTek UX so design "
                    "and data argue for the same build decision.\n\n"
                    "Say the source out loud. Claiming the Open University Learning Analytics Dataset as "
                    "BryTek production data would break trust with the client.\n\n"
                    "Early windows beat lifetime averages for instructor action. Teachers intervene in "
                    "weeks, not after the final result lands.\n\n"
                    "Keep the pair visible in reviews. Design shows the cockpit; analytics shows why "
                    "silent starters belong on the first scroll."
                ),
                "images": [],
            },
            {
                "key": "future",
                "title": "Future",
                "layout": "stack",
                "imageLayout": "stack",
                "body": (
                    "Next depth on the same human and scientific question: first-assessment timing, "
                    "weekly engagement trajectories, and a lightweight risk score behind BryTek's "
                    "recent-activity panel. Keep Retail KPI Storytelling as the separate commerce data study."
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
        "image": media("/images/case_studies/brytek-oulad-early-risk.jpg"),
        "title": "BryTek data: retention evidence to justify the product",
        "meta": "Data analysis · Open University Learning Analytics Dataset · client case",
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
