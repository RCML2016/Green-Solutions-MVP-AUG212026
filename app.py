"""
Green Solutions Intelligent Platform
Enterprise AI UI for Solar Asset Intelligence

Backend pipeline remains unchanged:
    synthetic_data -> LangGraph -> agents -> reports -> feedback

Run:
    streamlit run app.py
"""

import os
import re
from datetime import datetime

import pandas as pd
import streamlit as st

import agents
from graph import build_graph
from synthetic_data import generate_portfolio
from feedback_store import save_feedback, load_feedback


# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="Green Solutions | Intelligent Platform",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =============================================================================
# ENTERPRISE UI STYLING
# =============================================================================

st.markdown(
    """
    <style>

    /* ---------- Global ---------- */

    .stApp {
        background: #f7f9fc;
    }

    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    /* ---------- Sidebar ---------- */

    section[data-testid="stSidebar"] {
        background: #0b1724;
    }

    section[data-testid="stSidebar"] * {
        color: #f4f7fa;
    }

    .sidebar-brand {
        padding: 10px 5px 20px 5px;
        border-bottom: 1px solid rgba(255,255,255,0.12);
        margin-bottom: 20px;
    }

    .sidebar-brand-title {
        font-size: 22px;
        font-weight: 700;
    }

    .sidebar-brand-subtitle {
        font-size: 12px;
        color: #9fb1c4 !important;
        margin-top: 3px;
    }

    .sidebar-section {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #7f94aa !important;
        margin: 20px 0 8px 4px;
    }

    /* ---------- Header ---------- */

    .platform-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 4px 0 18px 0;
    }

    .platform-title {
        font-size: 30px;
        font-weight: 750;
        color: #152536;
        margin: 0;
    }

    .platform-subtitle {
        color: #68788a;
        font-size: 14px;
        margin-top: 4px;
    }

    .status-pill {
        display: inline-block;
        padding: 7px 13px;
        border-radius: 18px;
        background: #e8f7ef;
        color: #137a43;
        font-size: 12px;
        font-weight: 600;
    }

    /* ---------- KPI Cards ---------- */

    .kpi-card {
        background: white;
        border: 1px solid #e3e9ef;
        border-radius: 12px;
        padding: 18px 20px;
        min-height: 120px;
        box-shadow: 0 1px 2px rgba(16,24,40,0.03);
    }

    .kpi-label {
        color: #6b7b8c;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: .4px;
    }

    .kpi-value {
        color: #172b3f;
        font-size: 30px;
        font-weight: 750;
        margin-top: 8px;
    }

    .kpi-description {
        color: #8492a1;
        font-size: 12px;
        margin-top: 5px;
    }

    /* ---------- Section ---------- */

    .section-title {
        font-size: 20px;
        font-weight: 700;
        color: #172b3f;
        margin-top: 12px;
        margin-bottom: 3px;
    }

    .section-description {
        color: #728194;
        font-size: 13px;
        margin-bottom: 15px;
    }

    /* ---------- Insight Cards ---------- */

    .insight-card {
        background: white;
        border: 1px solid #e3e9ef;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 10px;
    }

    .insight-title {
        font-weight: 700;
        color: #24384c;
        font-size: 14px;
    }

    .insight-text {
        color: #647487;
        font-size: 13px;
        margin-top: 5px;
        line-height: 1.5;
    }

    /* ---------- Risk ---------- */

    .risk-high {
        color: #b42318;
        font-weight: 700;
    }

    .risk-medium {
        color: #b54708;
        font-weight: 700;
    }

    .risk-low {
        color: #137a43;
        font-weight: 700;
    }

    /* ---------- AI Card ---------- */

    .ai-card {
        background: #eef6ff;
        border: 1px solid #cfe3fa;
        border-radius: 12px;
        padding: 20px;
    }

    .ai-card-title {
        color: #164c7e;
        font-size: 16px;
        font-weight: 700;
    }

    .ai-card-text {
        color: #49677f;
        font-size: 13px;
        line-height: 1.5;
    }

    /* ---------- Governance ---------- */

    .governance-card {
        background: white;
        border: 1px solid #e3e9ef;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
    }

    /* ---------- Hide Streamlit Branding ---------- */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# DEMO MODE
# =============================================================================

def demo_mode_active() -> bool:
    return not (
        os.getenv("GOOGLE_API_KEY")
        or os.getenv("OLLAMA_MODEL")
    )


class DemoResponse:

    def __init__(self, content):
        self.content = content


class DemoLLM:

    def __init__(self, mode):
        self.mode = mode

    def invoke(self, prompt):

        if self.mode == "diagnose":

            return DemoResponse(
                """ASSET: INV-01
FAULT: string_underperformance
CONFIDENCE: 0.83
EVIDENCE: average output is well below the healthy baseline asset
ACTION: dispatch technician to check string connections

ASSET: INV-02
FAULT: inverter_clipping
CONFIDENCE: 0.71
EVIDENCE: output plateaus below expected peak during good sun hours
ACTION: verify inverter sizing and DC input ceiling

ASSET: INV-03
FAULT: soiling
CONFIDENCE: 0.78
EVIDENCE: output shows a gradual decline after the fault window begins
ACTION: inspect module cleanliness and review soiling-loss trend

ASSET: INV-04
FAULT: comm_dropout
CONFIDENCE: 0.91
EVIDENCE: repeated missing readings during midday hours
ACTION: check monitoring gateway connectivity

ASSET: INV-05
FAULT: none
CONFIDENCE: 0.97
EVIDENCE: output tracks capacity with no flagged intervals
ACTION: no action needed"""
            )

        return DemoResponse(
            """=== WORK_ORDER ===
1. INV-01: Inspect string connections and combiner box.
2. INV-02: Check inverter DC input ceiling for clipping.
3. INV-04: Check monitoring gateway and network connectivity.

=== OWNER_REPORT ===
Four assets in your portfolio need attention this period. INV-01 is
underperforming, likely a string connection issue. INV-02 shows signs
of inverter clipping and is under review. INV-04 has a data reporting
gap, not an actual generation loss. The rest of the portfolio is
performing normally.

=== COMPLIANCE_SUMMARY ===
Findings logged for the current review period. INV-01: string
underperformance identified. INV-02: inverter clipping identified.
INV-04: communication fault identified. Remaining assets have nominal
performance."""
        )


# =============================================================================
# PIPELINE
# =============================================================================

@st.cache_data(show_spinner=False)
def run_pipeline():

    df = generate_portfolio()

    df.to_csv("sample_portfolio.csv", index=False)

    if demo_mode_active():

        call_state = {"n": 0}

        def fake_get_llm():

            call_state["n"] += 1

            return DemoLLM(
                "diagnose"
                if call_state["n"] == 1
                else "draft"
            )

        agents.get_llm = fake_get_llm

    app = build_graph()

    return app.invoke(
        {
            "raw_data_path": "sample_portfolio.csv"
        }
    )


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def fault_label(fault):

    if not fault:
        return "Unknown"

    if fault == "none":
        return "Healthy"

    return fault.replace("_", " ").title()


def risk_level(diagnosis):

    fault = diagnosis.get("fault_hypothesis", "none")
    confidence = float(diagnosis.get("confidence", 0))

    if fault == "none":
        return "Low"

    if confidence >= 0.85:
        return "High"

    return "Medium"


def risk_icon(level):

    if level == "High":
        return "🔴"

    if level == "Medium":
        return "🟠"

    return "🟢"


def average_confidence(diagnoses):

    if not diagnoses:
        return 0

    return sum(
        float(d.get("confidence", 0))
        for d in diagnoses
    ) / len(diagnoses)


def count_issues(diagnoses):

    return sum(
        1
        for d in diagnoses
        if d.get("fault_hypothesis") != "none"
    )


# =============================================================================
# LOAD PIPELINE
# =============================================================================

if "pipeline_result" not in st.session_state:

    with st.spinner("Initializing Green Solutions AI..."):

        st.session_state.pipeline_result = run_pipeline()

result = st.session_state.pipeline_result

diagnoses = result.get("diagnoses", [])


# =============================================================================
# SIDEBAR
# =============================================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">

            <div class="sidebar-brand-title">
                🌱 Green Solutions
            </div>

            <div class="sidebar-brand-subtitle">
                Intelligent Sustainability Platform
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-section">Platform</div>',
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigation",
        [
            "Executive Dashboard",
            "AI Command Center",
            "Asset Intelligence",
            "Work Orders",
            "Performance Analytics",
            "Reports",
            "AI Governance",
            "Reviewer Feedback",
        ],
        label_visibility="collapsed",
    )

    st.markdown(
        '<div class="sidebar-section">System</div>',
        unsafe_allow_html=True,
    )

    if demo_mode_active():

        st.info(
            "Demo Mode\n\n"
            "Using synthetic portfolio data and sample AI responses.",
            icon="🧪",
        )

    else:

        st.success(
            "Live AI Mode\n\n"
            "Connected to configured AI provider.",
            icon="🟢",
        )

    st.caption(
        "Green Solutions Intelligent Platform\n"
        "MVP Validation Environment"
    )


# =============================================================================
# HEADER
# =============================================================================

st.markdown(
    f"""
    <div class="platform-header">

        <div>

            <div class="platform-title">
                Green Solutions
            </div>

            <div class="platform-subtitle">
                Intelligent Sustainability & Solar Operations Platform
            </div>

        </div>

        <div class="status-pill">
            ● AI SYSTEM ONLINE
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# EXECUTIVE DASHBOARD
# =============================================================================

if page == "Executive Dashboard":

    st.markdown(
        '<div class="section-title">Executive Dashboard</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-description">'
        'AI-powered portfolio intelligence and operational risk overview.'
        '</div>',
        unsafe_allow_html=True,
    )

    total_assets = len(diagnoses)
    issues = count_issues(diagnoses)
    healthy = total_assets - issues
    avg_conf = average_confidence(diagnoses)

    high_risk = sum(
        1
        for d in diagnoses
        if risk_level(d) == "High"
    )

    human_review = bool(
        result.get("needs_human_review")
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    cards = [
        ("Assets Monitored", total_assets, "Portfolio coverage"),
        ("Issues Detected", issues, "AI-identified findings"),
        ("Healthy Assets", healthy, "No issue detected"),
        ("AI Confidence", f"{avg_conf:.0%}", "Average diagnosis confidence"),
        ("High Risk", high_risk, "Priority attention"),
    ]

    for col, (label, value, desc) in zip(
        [c1, c2, c3, c4, c5],
        cards
    ):

        with col:

            st.markdown(
                f"""
                <div class="kpi-card">

                    <div class="kpi-label">
                        {label}
                    </div>

                    <div class="kpi-value">
                        {value}
                    </div>

                    <div class="kpi-description">
                        {desc}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")

    left, right = st.columns([1.5, 1])

    with left:

        st.markdown(
            '<div class="section-title">Portfolio Intelligence</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-description">'
            'AI-generated asset findings requiring operational attention.'
            '</div>',
            unsafe_allow_html=True,
        )

        for d in diagnoses:

            level = risk_level(d)

            st.markdown(
                f"""
                <div class="insight-card">

                    <div class="insight-title">
                        {risk_icon(level)}
                        {d.get("asset_id")}
                        — {fault_label(d.get("fault_hypothesis"))}
                    </div>

                    <div class="insight-text">
                        {d.get("evidence", "")}
                    </div>

                    <div class="insight-text">
                        <b>Recommended action:</b>
                        {d.get("recommended_action", "")}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

    with right:

        st.markdown(
            '<div class="section-title">AI System Status</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="ai-card">

                <div class="ai-card-title">
                    🤖 AI Diagnostic Engine
                </div>

                <br>

                <div class="ai-card-text">
                    <b>Processing:</b> Portfolio Performance
                </div>

                <div class="ai-card-text">
                    <b>Assets analyzed:</b> {total_assets}
                </div>

                <div class="ai-card-text">
                    <b>Findings:</b> {issues}
                </div>

                <div class="ai-card-text">
                    <b>Average confidence:</b> {avg_conf:.0%}
                </div>

                <div class="ai-card-text">
                    <b>Human review:</b>
                    {"Required" if human_review else "Not required"}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        if human_review:

            st.warning(
                result.get(
                    "review_reason",
                    "Human review required."
                ),
                icon="🔍",
            )

        else:

            st.success(
                "All findings meet the current confidence threshold.",
                icon="✓",
            )


# =============================================================================
# AI COMMAND CENTER
# =============================================================================

elif page == "AI Command Center":

    st.markdown(
        '<div class="section-title">AI Command Center</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-description">'
        'Ask questions about your solar portfolio and operational findings.'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="ai-card">

            <div class="ai-card-title">
                🤖 Green Solutions AI
            </div>

            <div class="ai-card-text">
                Use the portfolio intelligence already generated by the
                diagnostic pipeline to explore operational questions.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    prompt = st.text_area(
        "Ask Green Solutions AI",
        placeholder=(
            "Example: Which assets need immediate attention and why?"
        ),
        height=100,
    )

    quick_questions = [
        "Which assets need immediate attention?",
        "Why is INV-01 underperforming?",
        "Which assets have communication issues?",
        "What should the technicians check?",
    ]

    st.markdown("**Quick questions**")

    cols = st.columns(4)

    for col, question in zip(cols, quick_questions):

        with col:

            if st.button(
                question,
                use_container_width=True
            ):
                prompt = question

    if prompt:

        lower = prompt.lower()

        if "immediate" in lower or "attention" in lower:

            selected = [
                d for d in diagnoses
                if d.get("fault_hypothesis") != "none"
            ]

            response = (
                f"{len(selected)} assets require attention. "
                "The highest-priority findings are "
                + ", ".join(
                    d.get("asset_id")
                    for d in selected
                )
                + "."
            )

        elif "communication" in lower:

            selected = [
                d for d in diagnoses
                if d.get("fault_hypothesis") == "comm_dropout"
            ]

            response = (
                "Communication-related findings: "
                + (
                    ", ".join(
                        d.get("asset_id")
                        for d in selected
                    )
                    if selected
                    else "None identified."
                )
            )

        elif "inv-01" in lower:

            d = next(
                (
                    x for x in diagnoses
                    if x.get("asset_id") == "INV-01"
                ),
                None,
            )

            if d:

                response = (
                    f"INV-01 is showing "
                    f"{fault_label(d.get('fault_hypothesis'))}. "
                    f"{d.get('evidence')} "
                    f"Recommended action: "
                    f"{d.get('recommended_action')}"
                )

            else:

                response = "INV-01 was not found."

        elif "technician" in lower or "check" in lower:

            actions = [
                f"{d.get('asset_id')}: "
                f"{d.get('recommended_action')}"
                for d in diagnoses
                if d.get("fault_hypothesis") != "none"
            ]

            response = "\n\n".join(actions)

        else:

            response = (
                "I can analyze asset health, fault hypotheses, "
                "recommended actions, confidence levels and "
                "operational priorities from the current portfolio."
            )

        st.markdown("### AI Response")

        st.info(response, icon="🤖")


# =============================================================================
# ASSET INTELLIGENCE
# =============================================================================

elif page == "Asset Intelligence":

    st.markdown(
        '<div class="section-title">Solar Asset Intelligence</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-description">'
        'Asset-level AI diagnosis, evidence and recommended action.'
        '</div>',
        unsafe_allow_html=True,
    )

    for d in diagnoses:

        level = risk_level(d)

        with st.container(border=True):

            c1, c2, c3 = st.columns([1.5, 2, 1])

            with c1:

                st.subheader(
                    f"{risk_icon(level)} {d.get('asset_id')}"
                )

                st.caption(
                    f"Risk: {level}"
                )

            with c2:

                st.markdown(
                    f"**Finding:** "
                    f"{fault_label(d.get('fault_hypothesis'))}"
                )

                st.write(
                    d.get("evidence", "")
                )

            with c3:

                st.metric(
                    "AI Confidence",
                    f"{float(d.get('confidence', 0)):.0%}"
                )

                st.caption(
                    d.get("recommended_action", "")
                )


# =============================================================================
# WORK ORDERS
# =============================================================================

elif page == "Work Orders":

    st.markdown(
        '<div class="section-title">Work Order Intelligence</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-description">'
        'AI-generated actions for field technicians and operations teams.'
        '</div>',
        unsafe_allow_html=True,
    )

    work_orders = [
        d for d in diagnoses
        if d.get("fault_hypothesis") != "none"
    ]

    if not work_orders:

        st.success(
            "No work orders required.",
            icon="✓",
        )

    for index, d in enumerate(work_orders, start=1):

        level = risk_level(d)

        with st.container(border=True):

            c1, c2, c3 = st.columns([.6, 1.5, 4])

            with c1:

                st.markdown(
                    f"### {index}"
                )

            with c2:

                st.markdown(
                    f"**{d.get('asset_id')}**"
                )

                st.caption(
                    f"{risk_icon(level)} {level} Priority"
                )

            with c3:

                st.markdown(
                    f"**Fault:** "
                    f"{fault_label(d.get('fault_hypothesis'))}"
                )

                st.write(
                    f"**Action:** "
                    f"{d.get('recommended_action')}"
                )


# =============================================================================
# PERFORMANCE ANALYTICS
# =============================================================================

elif page == "Performance Analytics":

    st.markdown(
        '<div class="section-title">Performance Analytics</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-description">'
        'Portfolio-level performance and AI diagnosis distribution.'
        '</div>',
        unsafe_allow_html=True,
    )

    df = result.get("normalized_df")

    if df is not None:

        st.subheader("Generation by Asset")

        if "generation_kw" in df.columns:

            asset_generation = (
                df.groupby("asset_id")["generation_kw"]
                .mean()
                .sort_values(ascending=False)
            )

            st.bar_chart(
                asset_generation,
                use_container_width=True,
            )

        st.subheader("AI Findings")

        fault_counts = pd.Series(
            [
                fault_label(
                    d.get("fault_hypothesis")
                )
                for d in diagnoses
            ]
        ).value_counts()

        st.bar_chart(
            fault_counts,
            use_container_width=True,
        )

        st.subheader("Portfolio Data")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )


# =============================================================================
# REPORTS
# =============================================================================

elif page == "Reports":

    st.markdown(
        '<div class="section-title">Enterprise Reports</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-description">'
        'AI-generated reports for operations, asset owners and compliance.'
        '</div>',
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "🔧 Field Work Order",
            "🏢 Owner Report",
            "🛡️ Compliance Summary",
        ]
    )

    with tab1:

        text = result.get(
            "work_order_text",
            "(No work order generated)"
        )

        st.text_area(
            "Work Order",
            text,
            height=350,
        )

        st.download_button(
            "Download Work Order",
            data=text,
            file_name="green_solutions_work_order.txt",
            mime="text/plain",
        )

    with tab2:

        text = result.get(
            "owner_report_text",
            "(No owner report generated)"
        )

        st.text_area(
            "Owner Report",
            text,
            height=350,
        )

        st.download_button(
            "Download Owner Report",
            data=text,
            file_name="green_solutions_owner_report.txt",
            mime="text/plain",
        )

    with tab3:

        text = result.get(
            "compliance_summary_text",
            "(No compliance summary generated)"
        )

        st.text_area(
            "Compliance Summary",
            text,
            height=350,
        )

        st.download_button(
            "Download Compliance Summary",
            data=text,
            file_name="green_solutions_compliance_summary.txt",
            mime="text/plain",
        )


# =============================================================================
# AI GOVERNANCE
# =============================================================================

elif page == "AI Governance":

    st.markdown(
        '<div class="section-title">AI Governance & Trust</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-description">'
        'Transparency, confidence and human oversight for AI-generated findings.'
        '</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown(
            """
            <div class="governance-card">

            <b>🤖 AI Provider</b>

            <br><br>

            Gemini / Demo Engine

            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:

        st.markdown(
            f"""
            <div class="governance-card">

            <b>🎯 Average Confidence</b>

            <br><br>

            {average_confidence(diagnoses):.0%}

            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:

        st.markdown(
            f"""
            <div class="governance-card">

            <b>👤 Human Oversight</b>

            <br><br>

            {"Required" if result.get("needs_human_review") else "Not Required"}

            </div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader("AI Decision Evidence")

    governance_rows = []

    for d in diagnoses:

        governance_rows.append(
            {
                "Asset": d.get("asset_id"),
                "Finding": fault_label(
                    d.get("fault_hypothesis")
                ),
                "Confidence": f"{float(d.get('confidence', 0)):.0%}",
                "Evidence": d.get("evidence"),
                "Human Review": (
                    "Yes"
                    if float(d.get("confidence", 0)) < 0.6
                    else "No"
                ),
            }
        )

    st.dataframe(
        pd.DataFrame(governance_rows),
        use_container_width=True,
        hide_index=True,
    )

    st.info(
        "AI findings should be treated as decision support. "
        "Low-confidence findings should be reviewed by an authorized "
        "human before operational publication.",
        icon="🛡️",
    )


# =============================================================================
# REVIEWER FEEDBACK
# =============================================================================

elif page == "Reviewer Feedback":

    st.markdown(
        '<div class="section-title">Reviewer Feedback</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-description">'
        'Help validate whether the AI system is useful, trustworthy and '
        'time-saving for real operational teams.'
        '</div>',
        unsafe_allow_html=True,
    )

    with st.form("feedback_form"):

        trust = st.slider(
            "How much would you trust this without double-checking it yourself?",
            1,
            5,
            3,
            help="1 = not at all, 5 = fully",
        )

        clarity = st.slider(
            "How clear and easy to read was the language?",
            1,
            5,
            3,
        )

        time_saved = st.radio(
            "Compared to how your team writes these today, would this save time?",
            [
                "Yes, clearly",
                "Somewhat",
                "Not really",
                "Not sure",
            ],
            index=None,
        )

        role = st.text_input(
            "Your role",
            placeholder="O&M manager, asset owner, technician..."
        )

        comments = st.text_area(
            "What is missing, confusing, or would make this more useful?"
        )

        submitted = st.form_submit_button(
            "Submit Feedback",
            use_container_width=True,
        )

        if submitted:

            if time_saved is None:

                st.error(
                    "Please answer the time-saved question."
                )

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

                st.success(
                    "Thank you. Your feedback was recorded.",
                    icon="✓",
                )

    st.divider()

    with st.expander(
        "View validation feedback"
    ):

        records = load_feedback()

        if records:

            st.dataframe(
                records,
                use_container_width=True,
            )

        else:

            st.caption(
                "No feedback submitted yet."
            )


# =============================================================================
# FOOTER
# =============================================================================

st.divider()

st.caption(
    f"Green Solutions Intelligent Platform • MVP • "
    f"{datetime.now().strftime('%B %d, %Y')} • "
    f"AI-assisted decision support"
)
