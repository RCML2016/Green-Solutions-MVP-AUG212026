"""
Reviewer-facing demo app.

Run with:  streamlit run app.py

Shows the pipeline's output in plain language (no code, no logs) and
captures structured feedback from a non-technical reviewer — an O&M
shop owner, asset manager, etc. Falls back to a labeled demo mode with
sample output if no LLM API key is configured, so this can be shared
even before you've wired up a live model.
"""

import streamlit as st
import agents
from graph import build_graph
from synthetic_data import generate_portfolio
from feedback_store import save_feedback, load_feedback

st.set_page_config(page_title="Solar Reporting Copilot — Preview", layout="centered")


# ---------------------------------------------------------------------------
# Demo-mode fallback so this is shareable with zero setup on the reviewer's
# end. If a real API key is configured server-side, this is skipped and
# the actual LLM runs instead.
# ---------------------------------------------------------------------------
def _demo_mode_active() -> bool:
    import os
    return not (os.getenv("GOOGLE_API_KEY") or os.getenv("OLLAMA_MODEL"))


class _DemoResponse:
    def __init__(self, content):
        self.content = content


class _DemoLLM:
    def __init__(self, mode):
        self.mode = mode

    def invoke(self, prompt):
        if self.mode == "diagnose":
            return _DemoResponse(
                "ASSET: INV-01\nFAULT: string_underperformance\nCONFIDENCE: 0.83\n"
                "EVIDENCE: average output is well below the healthy baseline asset\n"
                "ACTION: dispatch technician to check string connections\n\n"
                "ASSET: INV-02\nFAULT: inverter_clipping\nCONFIDENCE: 0.71\n"
                "EVIDENCE: output plateaus below expected peak during good sun hours\n"
                "ACTION: verify inverter sizing and DC input ceiling\n\n"
                "ASSET: INV-03\nFAULT: soiling\nCONFIDENCE: 0.78\n"
                "EVIDENCE: output shows a gradual decline after the fault window begins\n"
                "ACTION: inspect module cleanliness and review soiling-loss trend\n\n"
                "ASSET: INV-04\nFAULT: comm_dropout\nCONFIDENCE: 0.91\n"
                "EVIDENCE: repeated missing readings during midday hours\n"
                "ACTION: check monitoring gateway connectivity\n\n"
                "ASSET: INV-05\nFAULT: none\nCONFIDENCE: 0.97\n"
                "EVIDENCE: output tracks capacity with no flagged intervals\n"
                "ACTION: no action needed"
            )
        return _DemoResponse(
            "=== WORK_ORDER ===\n"
            "1. INV-01: Inspect string connections and combiner box.\n"
            "2. INV-02: Check inverter DC input ceiling for clipping.\n"
            "3. INV-04: Check monitoring gateway and network connectivity.\n\n"
            "=== OWNER_REPORT ===\n"
            "Four assets in your portfolio need attention this period. INV-01 is "
            "underperforming, likely a string connection issue — a technician has "
            "been dispatched. INV-02 shows signs of inverter clipping and is under "
            "review. INV-04 has a data reporting gap, not an actual generation "
            "loss, and is being resolved with the monitoring vendor. The rest of "
            "the portfolio is performing normally.\n\n"
            "=== COMPLIANCE_SUMMARY ===\n"
            "Findings logged for the current review period. INV-01: string "
            "underperformance identified, corrective work order issued. INV-02: "
            "inverter clipping identified, engineering review in progress. INV-04: "
            "communication fault identified, not a generation-loss event. Remaining "
            "assets: no findings, nominal performance."
        )


@st.cache_data(show_spinner=False)
def run_pipeline():
    df = generate_portfolio()
    df.to_csv("sample_portfolio.csv", index=False)

    if _demo_mode_active():
        call_state = {"n": 0}

        def fake_get_llm():
            call_state["n"] += 1
            return _DemoLLM("diagnose" if call_state["n"] == 1 else "draft")

        agents.get_llm = fake_get_llm

    app = build_graph()
    return app.invoke({"raw_data_path": "sample_portfolio.csv"})


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------
st.title("Solar reporting copilot — preview")
st.caption(
    "This tool reads solar asset performance data and drafts the reports your "
    "team currently writes by hand. Please review the output below and share "
    "your honest reaction at the bottom — there are no wrong answers."
)

if _demo_mode_active():
    st.info(
        "Demo mode: showing sample AI output so you can review the format "
        "and content without any setup on your end.",
        icon="ℹ️",
    )

with st.spinner("Reviewing portfolio data..."):
    result = run_pipeline()

st.subheader("What was found")
for d in result.get("diagnoses", []):
    label = "No issue found" if d["fault_hypothesis"] == "none" else d["fault_hypothesis"].replace("_", " ").title()
    icon = "✅" if d["fault_hypothesis"] == "none" else "⚠️"
    with st.expander(f"{icon} {d['asset_id']} — {label}"):
        st.write(f"**What we saw:** {d['evidence']}")
        st.write(f"**Suggested next step:** {d['recommended_action']}")
        st.caption(f"Model confidence: {d['confidence']:.0%}")

if result.get("needs_human_review"):
    st.warning(
        "One or more findings had lower confidence and would normally be "
        "flagged for your team to confirm before being sent to an owner.",
        icon="🔍",
    )

st.subheader("Drafted reports")
tab1, tab2, tab3 = st.tabs(["Field work order", "Owner report", "Compliance summary"])
with tab1:
    st.write(result.get("work_order_text", "(empty)"))
with tab2:
    st.write(result.get("owner_report_text", "(empty)"))
with tab3:
    st.write(result.get("compliance_summary_text", "(empty)"))

st.divider()

# ---------------------------------------------------------------------------
# Feedback form
# ---------------------------------------------------------------------------
st.subheader("Your feedback")

with st.form("feedback_form"):
    trust = st.slider(
        "How much would you trust this without double-checking it yourself?",
        1, 5, 3,
        help="1 = not at all, 5 = fully",
    )
    clarity = st.slider(
        "How clear and easy to read was the language?",
        1, 5, 3,
    )
    time_saved = st.radio(
        "Compared to how your team writes these today, would this save time?",
        ["Yes, clearly", "Somewhat", "Not really", "Not sure"],
        index=None,
    )
    role = st.text_input("Your role (e.g. O&M manager, asset owner, technician)")
    comments = st.text_area(
        "What's missing, confusing, or would make this more useful to you?"
    )
    submitted = st.form_submit_button("Submit feedback")

    if submitted:
        if time_saved is None:
            st.error("Please answer the time-saved question before submitting.")
        else:
            save_feedback(
                {
                    "trust_score": trust,
                    "clarity_score": clarity,
                    "time_saved": time_saved,
                    "role": role,
                    "comments": comments,
                }
            )
            st.success("Thanks — your feedback was recorded.")

with st.expander("View all feedback so far (for you, not the reviewer)"):
    records = load_feedback()
    if records:
        st.dataframe(records, use_container_width=True)
    else:
        st.caption("No feedback submitted yet.")
