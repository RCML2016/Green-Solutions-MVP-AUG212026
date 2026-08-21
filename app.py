"""
Green Solutions Intelligent Platform
V2 - Enterprise SaaS Experience

Existing backend preserved:
    synthetic_data -> LangGraph -> Agents -> Reports -> Feedback

Run:
    streamlit run app.py
"""

import os
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
    page_title="Green Solutions",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =============================================================================
# PREMIUM PRODUCT CSS
# =============================================================================

st.markdown(
    """
<style>

/* ============================================================
   GLOBAL
   ============================================================ */

.stApp {
    background:
        radial-gradient(
            circle at 85% 5%,
            rgba(44, 177, 113, 0.08),
            transparent 28%
        ),
        #f7faf8;
    color: #15261d;
}

.main .block-container {
    max-width: 1320px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}

/* Hide Streamlit chrome */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}


/* ============================================================
   TOP NAV
   ============================================================ */

.top-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 4px 0 25px 0;
}

.brand {
    display: flex;
    align-items: center;
    gap: 10px;
}

.brand-icon {
    width: 38px;
    height: 38px;
    border-radius: 11px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: linear-gradient(
        135deg,
        #0f7b4d,
        #32b76f
    );

    color: white;
    font-size: 20px;
    box-shadow:
        0 6px 18px rgba(15,123,77,.20);
}

.brand-name {
    font-size: 18px;
    font-weight: 750;
    color: #173326;
}

.brand-sub {
    font-size: 10px;
    color: #789084;
    margin-top: -2px;
}

.live-pill {
    background: #eaf8f0;
    color: #16784b;
    border: 1px solid #cdebd9;

    border-radius: 30px;

    padding: 7px 12px;

    font-size: 11px;
    font-weight: 700;
}


/* ============================================================
   HERO
   ============================================================ */

.hero {
    position: relative;

    overflow: hidden;

    border-radius: 26px;

    padding: 54px 58px;

    margin-bottom: 28px;

    background:
        radial-gradient(
            circle at 90% 10%,
            rgba(105, 211, 150, .20),
            transparent 25%
        ),
        linear-gradient(
            135deg,
            #09271b 0%,
            #0d3c29 55%,
            #0c5035 100%
        );

    box-shadow:
        0 20px 60px rgba(15, 75, 48, .15);
}

.hero-eyebrow {
    color: #7de0a9;

    font-size: 12px;

    font-weight: 750;

    letter-spacing: 1.8px;

    text-transform: uppercase;

    margin-bottom: 14px;
}

.hero-title {
    color: white;

    font-size: 46px;

    line-height: 1.05;

    font-weight: 800;

    max-width: 750px;

    margin-bottom: 18px;
}

.hero-title span {
    color: #75dda4;
}

.hero-description {
    color: #c3d9cc;

    font-size: 16px;

    line-height: 1.65;

    max-width: 680px;

    margin-bottom: 25px;
}

.hero-meta {
    display: flex;
    gap: 25px;

    color: #a8c4b4;

    font-size: 12px;
}


/* ============================================================
   SECTION HEADINGS
   ============================================================ */

.section {
    margin-top: 34px;
    margin-bottom: 15px;
}

.section-title {
    font-size: 22px;
    font-weight: 780;
    color: #183328;
}

.section-subtitle {
    color: #72857a;
    font-size: 13px;
    margin-top: 3px;
}


/* ============================================================
   KPI
   ============================================================ */

.kpi {
    background: rgba(255,255,255,.92);

    border: 1px solid #e2ebe5;

    border-radius: 16px;

    padding: 20px;

    min-height: 128px;

    box-shadow:
        0 5px 18px rgba(22,53,38,.035);
}

.kpi-label {
    color: #789084;

    font-size: 11px;

    font-weight: 750;

    letter-spacing: .6px;

    text-transform: uppercase;
}

.kpi-value {
    color: #173326;

    font-size: 31px;

    font-weight: 800;

    margin-top: 8px;
}

.kpi-note {
    color: #8b9c93;

    font-size: 11px;

    margin-top: 4px;
}


/* ============================================================
   AI INSIGHTS
   ============================================================ */

.ai-panel {
    background: white;

    border: 1px solid #e2ebe5;

    border-radius: 18px;

    padding: 23px;

    box-shadow:
        0 8px 25px rgba(22,53,38,.035);
}

.ai-header {
    display: flex;
    align-items: center;
    gap: 11px;

    margin-bottom: 18px;
}

.ai-icon {
    width: 38px;
    height: 38px;

    border-radius: 11px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: #eaf8f0;

    font-size: 19px;
}

.ai-title {
    font-size: 16px;
    font-weight: 760;
    color: #183328;
}

.ai-sub {
    color: #819087;
    font-size: 11px;
}


/* ============================================================
   INSIGHT
   ============================================================ */

.insight {
    padding: 16px 0;

    border-bottom: 1px solid #edf1ee;
}

.insight:last-child {
    border-bottom: none;
}

.insight-top {
    display: flex;

    justify-content: space-between;

    align-items: center;
}

.insight-name {
    font-size: 14px;
    font-weight: 720;
    color: #1b3427;
}

.insight-description {
    color: #73847b;
    font-size: 12px;

    margin-top: 6px;

    line-height: 1.55;
}

.high {
    color: #b42318;
}

.medium {
    color: #b54708;
}

.low {
    color: #16784b;
}


/* ============================================================
   FEATURE CARDS
   ============================================================ */

.feature-card {
    background: white;

    border: 1px solid #e2ebe5;

    border-radius: 18px;

    padding: 24px;

    min-height: 190px;

    transition: all .2s ease;

    box-shadow:
        0 5px 20px rgba(22,53,38,.03);
}

.feature-icon {
    width: 42px;
    height: 42px;

    border-radius: 12px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: #eef8f2;

    font-size: 20px;

    margin-bottom: 18px;
}

.feature-title {
    font-weight: 750;

    font-size: 15px;

    color: #183328;

    margin-bottom: 7px;
}

.feature-text {
    color: #74867c;

    font-size: 12px;

    line-height: 1.6;
}


/* ============================================================
   AI COPILOT
   ============================================================ */

.copilot {
    background:
        linear-gradient(
            135deg,
            #eefaf3,
            #f7fcf9
        );

    border: 1px solid #d7ecdf;

    border-radius: 20px;

    padding: 26px;
}

.copilot-title {
    color: #174d32;

    font-size: 19px;

    font-weight: 780;
}

.copilot-text {
    color: #63796d;

    font-size: 13px;

    line-height: 1.55;

    margin-top: 5px;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    text-align: center;

    color: #91a099;

    font-size: 11px;

    padding-top: 25px;
}

</style>
""",
    unsafe_allow_html=True,
)


# =============================================================================
# DEMO MODE
# =============================================================================

def demo_mode_active():

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
# HELPERS
# =============================================================================

def fault_label(fault):

    if not fault:
        return "Unknown"

    if fault == "none":
        return "Healthy"

    return fault.replace("_", " ").title()


def risk_level(d):

    fault = d.get("fault_hypothesis", "none")

    confidence = float(
        d.get("confidence", 0)
    )

    if fault == "none":
        return "Low"

    if confidence >= .85:
        return "High"

    return "Medium"


def risk_class(level):

    if level == "High":
        return "high"

    if level == "Medium":
        return "medium"

    return "low"


def average_confidence(diagnoses):

    if not diagnoses:
        return 0

    return sum(
        float(d.get("confidence", 0))
        for d in diagnoses
    ) / len(diagnoses)


# =============================================================================
# LOAD DATA
# =============================================================================

if "pipeline_result" not in st.session_state:

    with st.spinner("Preparing your intelligent sustainability workspace..."):

        st.session_state.pipeline_result = run_pipeline()

result = st.session_state.pipeline_result

diagnoses = result.get(
    "diagnoses",
    []
)

total_assets = len(diagnoses)

issues = sum(
    1
    for d in diagnoses
    if d.get("fault_hypothesis") != "none"
)

healthy = total_assets - issues

avg_confidence = average_confidence(
    diagnoses
)

high_risk = sum(
    1
    for d in diagnoses
    if risk_level(d) == "High"
)


# =============================================================================
# SESSION NAVIGATION
# =============================================================================

if "page" not in st.session_state:

    st.session_state.page = "Home"


# =============================================================================
# TOP NAVIGATION
# =============================================================================

st.markdown(
    """
<div class="top-nav">

    <div class="brand">

        <div class="brand-icon">
            🌱
        </div>

        <div>

            <div class="brand-name">
                Green Solutions
            </div>

            <div class="brand-sub">
                Intelligent Sustainability Platform
            </div>

        </div>

    </div>

    <div class="live-pill">
        ● PLATFORM LIVE
    </div>

</div>
""",
    unsafe_allow_html=True,
)


# =============================================================================
# NAVIGATION
# =============================================================================

nav1, nav2, nav3, nav4, nav5 = st.columns(
    [1, 1, 1, 1, 1]
)

with nav1:

    if st.button(
        "⌂  Home",
        use_container_width=True
    ):

        st.session_state.page = "Home"


with nav2:

    if st.button(
        "✦  AI Copilot",
        use_container_width=True
    ):

        st.session_state.page = "AI Copilot"


with nav3:

    if st.button(
        "☀  Assets",
        use_container_width=True
    ):

        st.session_state.page = "Assets"


with nav4:

    if st.button(
        "⚙  Operations",
        use_container_width=True
    ):

        st.session_state.page = "Operations"


with nav5:

    if st.button(
        "▣  Reports",
        use_container_width=True
    ):

        st.session_state.page = "Reports"


st.divider()


# =============================================================================
# HOME
# =============================================================================

if st.session_state.page == "Home":

    st.markdown(
        f"""
<div class="hero">

    <div class="hero-eyebrow">
        AI-POWERED SUSTAINABILITY INTELLIGENCE
    </div>

    <div class="hero-title">
        Turn sustainability data<br>
        into <span>intelligent action.</span>
    </div>

    <div class="hero-description">
        Green Solutions uses AI to detect operational issues,
        explain what is happening, and recommend the next best
        action for your sustainability and asset operations teams.
    </div>

    <div class="hero-meta">

        <span>✦ AI Diagnostics</span>

        <span>✦ Human-in-the-loop</span>

        <span>✦ Evidence-based insights</span>

    </div>

</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section">'
        '<div class="section-title">Portfolio at a glance</div>'
        '<div class="section-subtitle">'
        'AI-generated operational intelligence from your current portfolio.'
        '</div></div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)

    kpis = [
        (
            c1,
            "PORTFOLIO HEALTH",
            f"{(healthy / total_assets * 100) if total_assets else 0:.0f}%",
            "Assets without active findings",
        ),
        (
            c2,
            "ASSETS MONITORED",
            total_assets,
            "AI-analyzed assets",
        ),
        (
            c3,
            "AI FINDINGS",
            issues,
            "Operational issues detected",
        ),
        (
            c4,
            "AI CONFIDENCE",
            f"{avg_confidence:.0%}",
            "Average diagnostic confidence",
        ),
    ]

    for col, label, value, note in kpis:

        with col:

            st.markdown(
                f"""
                <div class="kpi">

                    <div class="kpi-label">
                        {label}
                    </div>

                    <div class="kpi-value">
                        {value}
                    </div>

                    <div class="kpi-note">
                        {note}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

    # -------------------------------------------------------------------------
    # AI INSIGHTS
    # -------------------------------------------------------------------------

    st.markdown(
        '<div class="section">'
        '<div class="section-title">AI-generated insights</div>'
        '<div class="section-subtitle">'
        'The most important things your operations team should know right now.'
        '</div></div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns(
        [1.45, 1]
    )

    with left:

        st.markdown(
            """
            <div class="ai-panel">

                <div class="ai-header">

                    <div class="ai-icon">
                        ✦
                    </div>

                    <div>

                        <div class="ai-title">
                            Green Solutions Intelligence
                        </div>

                        <div class="ai-sub">
                            AI diagnostic engine
                        </div>

                    </div>

                </div>
            """,
            unsafe_allow_html=True,
        )

        for d in diagnoses:

            level = risk_level(d)

            icon = (
                "🔴"
                if level == "High"
                else "🟠"
                if level == "Medium"
                else "🟢"
            )

            st.markdown(
                f"""
                <div class="insight">

                    <div class="insight-top">

                        <div class="insight-name">
                            {icon}
                            {d.get("asset_id")}
                            · {fault_label(d.get("fault_hypothesis"))}
                        </div>

                        <div class="{risk_class(level)}">
                            {level}
                        </div>

                    </div>

                    <div class="insight-description">

                        {d.get("evidence", "")}

                        <br><br>

                        <b>Next best action:</b>
                        {d.get("recommended_action", "")}

                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

    with right:

        st.markdown(
            """
            <div class="copilot">

                <div class="copilot-title">
                    ✦ Ask Green Solutions AI
                </div>

                <div class="copilot-text">
                    Explore your portfolio using natural language.
                    Ask why an asset is underperforming, what requires
                    attention, or what your technicians should do next.
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        if st.button(
            "Open AI Copilot →",
            use_container_width=True
        ):

            st.session_state.page = "AI Copilot"

            st.rerun()

    # -------------------------------------------------------------------------
    # PRODUCT CAPABILITIES
    # -------------------------------------------------------------------------

    st.markdown(
        '<div class="section">'
        '<div class="section-title">Intelligence built for operations</div>'
        '<div class="section-subtitle">'
        'From raw operational data to decisions your teams can act on.'
        '</div></div>',
        unsafe_allow_html=True,
    )

    f1, f2, f3 = st.columns(3)

    features = [
        (
            f1,
            "✦",
            "AI Asset Diagnostics",
            "Automatically identify abnormal asset behavior, classify likely faults, and explain the evidence behind every finding.",
        ),
        (
            f2,
            "⚙",
            "Operational Intelligence",
            "Turn AI findings into technician-ready actions and operational priorities.",
        ),
        (
            f3,
            "🛡",
            "Responsible AI",
            "Confidence scoring, evidence grounding and human-review controls help keep AI decisions transparent.",
        ),
    ]

    for col, icon, title, text in features:

        with col:

            st.markdown(
                f"""
                <div class="feature-card">

                    <div class="feature-icon">
                        {icon}
                    </div>

                    <div class="feature-title">
                        {title}
                    </div>

                    <div class="feature-text">
                        {text}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )


# =============================================================================
# AI COPILOT
# =============================================================================

elif st.session_state.page == "AI Copilot":

    st.markdown(
        """
        <div class="hero">

            <div class="hero-eyebrow">
                GREEN SOLUTIONS AI
            </div>

            <div class="hero-title">
                Your sustainability<br>
                <span>intelligence copilot.</span>
            </div>

            <div class="hero-description">
                Ask questions about your portfolio and get answers
                grounded in the AI diagnostics already generated.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    question = st.text_area(
        "Ask Green Solutions AI",
        placeholder=(
            "Try: Which assets need immediate attention and why?"
        ),
        height=120,
    )

    quick = [
        "Which assets need immediate attention?",
        "Why is INV-01 underperforming?",
        "Which assets have communication issues?",
        "What should the technicians check?",
    ]

    st.markdown("**Suggested questions**")

    cols = st.columns(4)

    for col, q in zip(cols, quick):

        with col:

            if st.button(
                q,
                use_container_width=True
            ):

                question = q

    if question:

        q = question.lower()

        if "immediate" in q or "attention" in q:

            selected = [
                d for d in diagnoses
                if d.get("fault_hypothesis") != "none"
            ]

            response = (
                f"{len(selected)} assets currently require "
                "operational attention: "
                + ", ".join(
                    d.get("asset_id")
                    for d in selected
                )
                + "."
            )

        elif "communication" in q:

            selected = [
                d for d in diagnoses
                if d.get("fault_hypothesis")
                == "comm_dropout"
            ]

            response = (
                "Communication issues were detected for: "
                + (
                    ", ".join(
                        d.get("asset_id")
                        for d in selected
                    )
                    if selected
                    else "none of the analyzed assets"
                )
                + "."
            )

        elif "inv-01" in q:

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

        elif "technician" in q or "check" in q:

            response = "\n\n".join(
                f"{d.get('asset_id')}: "
                f"{d.get('recommended_action')}"
                for d in diagnoses
                if d.get("fault_hypothesis") != "none"
            )

        else:

            response = (
                "I can currently help you explore asset health, "
                "diagnoses, evidence, confidence and recommended actions."
            )

        st.markdown("### ✦ AI Response")

        st.markdown(
            f"""
            <div class="ai-panel">

                <div class="ai-title">
                    Green Solutions AI
                </div>

                <br>

                <div style="color:#40584b;line-height:1.7;">
                    {response}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


# =============================================================================
# ASSETS
# =============================================================================

elif st.session_state.page == "Assets":

    st.markdown(
        """
        <div class="section">
            <div class="section-title">
                Solar Asset Intelligence
            </div>

            <div class="section-subtitle">
                Understand what is happening at every asset.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for d in diagnoses:

        level = risk_level(d)

        with st.container(border=True):

            c1, c2, c3 = st.columns(
                [1.3, 2.8, 1]
            )

            with c1:

                st.markdown(
                    f"### {d.get('asset_id')}"
                )

                st.caption(
                    f"{level} priority"
                )

            with c2:

                st.markdown(
                    f"**{fault_label(d.get('fault_hypothesis'))}**"
                )

                st.write(
                    d.get("evidence", "")
                )

                st.caption(
                    f"Recommended action: "
                    f"{d.get('recommended_action', '')}"
                )

            with c3:

                st.metric(
                    "Confidence",
                    f"{float(d.get('confidence', 0)):.0%}"
                )


# =============================================================================
# OPERATIONS
# =============================================================================

elif st.session_state.page == "Operations":

    st.markdown(
        """
        <div class="section">
            <div class="section-title">
                Operations Command Center
            </div>

            <div class="section-subtitle">
                Convert AI findings into prioritized field actions.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    work_orders = [
        d for d in diagnoses
        if d.get("fault_hypothesis") != "none"
    ]

    if work_orders:

        for index, d in enumerate(
            work_orders,
            start=1
        ):

            level = risk_level(d)

            with st.container(border=True):

                c1, c2, c3 = st.columns(
                    [.5, 1.3, 4]
                )

                with c1:

                    st.markdown(
                        f"### {index}"
                    )

                with c2:

                    st.markdown(
                        f"**{d.get('asset_id')}**"
                    )

                    st.caption(
                        f"{level} priority"
                    )

                with c3:

                    st.markdown(
                        f"**{fault_label(d.get('fault_hypothesis'))}**"
                    )

                    st.write(
                        d.get("recommended_action", "")
                    )

    else:

        st.success(
            "No operational actions are currently required."
        )


# =============================================================================
# REPORTS
# =============================================================================

elif st.session_state.page == "Reports":

    st.markdown(
        """
        <div class="section">
            <div class="section-title">
                Enterprise Reports
            </div>

            <div class="section-subtitle">
                AI-generated documentation for operations, owners and compliance.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "Field Work Order",
            "Owner Report",
            "Compliance Summary",
        ]
    )

    reports = [
        (
            tab1,
            "work_order_text",
            "green_solutions_work_order.txt",
            "Field Work Order",
        ),
        (
            tab2,
            "owner_report_text",
            "green_solutions_owner_report.txt",
            "Owner Report",
        ),
        (
            tab3,
            "compliance_summary_text",
            "green_solutions_compliance.txt",
            "Compliance Summary",
        ),
    ]

    for tab, key, filename, label in reports:

        with tab:

            text = result.get(
                key,
                "(No report generated)"
            )

            st.text_area(
                label,
                text,
                height=380,
            )

            st.download_button(
                f"Download {label}",
                text,
                file_name=filename,
                mime="text/plain",
                use_container_width=True,
            )


# =============================================================================
# FOOTER / SYSTEM STATUS
# =============================================================================

st.divider()

mode = (
    "Demo AI"
    if demo_mode_active()
    else "Live AI"
)

st.markdown(
    f"""
    <div class="footer">

        Green Solutions Intelligent Platform
        &nbsp;•&nbsp;
        {mode}
        &nbsp;•&nbsp;
        AI-assisted decision support
        &nbsp;•&nbsp;
        {datetime.now().strftime("%Y")}

    </div>
    """,
    unsafe_allow_html=True,
)
