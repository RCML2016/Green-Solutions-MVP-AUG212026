"""
Green Solutions
Enterprise AI Sustainability Intelligence Platform

UI:
    Overview
    AI Intelligence
    Asset 360
    Operations
    Reports

Backend:
    LangGraph + AI Diagnostics + Human Review + Report Generation
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
    page_title="Green Solutions | AI Powered - Intelligent Sustainability",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =============================================================================
# DESIGN SYSTEM
# =============================================================================

st.markdown(
    """
<style>

/* ============================================================
   GLOBAL
   ============================================================ */

.stApp {
    background: #F6F9F7;
    color: #183328;
}

.main .block-container {
    max-width: 1380px;
    padding: 1.2rem 2.2rem 4rem 2.2rem;
}

#MainMenu,
footer,
header {
    visibility: hidden;
}


/* ============================================================
   TYPOGRAPHY
   ============================================================ */

h1, h2, h3, h4 {
    color: #173326 !important;
}


/* ============================================================
   BRAND
   ============================================================ */

.brand-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
}

.brand-left {
    display: flex;
    align-items: center;
    gap: 12px;
}

.brand-logo {
    width: 42px;
    height: 42px;
    border-radius: 13px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: linear-gradient(
        135deg,
        #0C7044,
        #35B96E
    );

    color: white;
    font-size: 22px;

    box-shadow:
        0 8px 20px rgba(12,112,68,.18);
}

.brand-title {
    font-size: 19px;
    font-weight: 800;
    color: #173326;
}

.brand-subtitle {
    font-size: 10px;
    color: #7A8D83;
    margin-top: -2px;
}

.live {
    background: #E9F8F0;
    border: 1px solid #CDEBDD;

    color: #157A4A;

    padding: 7px 13px;

    border-radius: 30px;

    font-size: 10px;

    font-weight: 800;

    letter-spacing: .5px;
}


/* ============================================================
   NAVIGATION
   ============================================================ */

div.stButton > button {

    border-radius: 9px;

    border: 1px solid #E1E9E4;

    background: white;

    color: #476055;

    font-size: 12px;

    font-weight: 650;

    min-height: 38px;

    transition: all .15s ease;
}

div.stButton > button:hover {

    border-color: #94CFAE;

    color: #126B42;

    background: #F2FAF5;
}


/* ============================================================
   HERO
   ============================================================ */

.hero {

    position: relative;

    overflow: hidden;

    border-radius: 25px;

    padding: 48px 54px;

    margin: 18px 0 28px 0;

    background:
        radial-gradient(
            circle at 85% 15%,
            rgba(96,215,145,.22),
            transparent 26%
        ),
        linear-gradient(
            135deg,
            #08291C,
            #0D432C 60%,
            #0D5739
        );

    box-shadow:
        0 22px 60px rgba(12,73,46,.16);
}

.hero-eyebrow {

    color: #76DCA6;

    font-size: 11px;

    font-weight: 800;

    letter-spacing: 1.7px;

    text-transform: uppercase;

    margin-bottom: 14px;
}

.hero-title {

    color: white;

    font-size: 43px;

    line-height: 1.08;

    font-weight: 820;

    max-width: 760px;
}

.hero-title span {
    color: #79DDA8;
}

.hero-description {

    color: #C3D9CC;

    font-size: 15px;

    line-height: 1.65;

    max-width: 700px;

    margin-top: 17px;
}

.hero-status {

    display: flex;

    gap: 22px;

    margin-top: 23px;

    color: #A9C8B7;

    font-size: 11px;
}


/* ============================================================
   PAGE HEADER
   ============================================================ */

.page-header {
    margin: 25px 0 20px 0;
}

.page-title {
    font-size: 28px;
    font-weight: 800;
    color: #173326;
}

.page-subtitle {
    color: #778980;
    font-size: 13px;
    margin-top: 4px;
}


/* ============================================================
   KPI CARDS
   ============================================================ */

.kpi {

    background: white;

    border: 1px solid #E0E9E3;

    border-radius: 17px;

    padding: 20px;

    min-height: 128px;

    box-shadow:
        0 5px 20px rgba(25,60,43,.035);
}

.kpi-label {

    color: #7C8E85;

    font-size: 10px;

    font-weight: 800;

    letter-spacing: .7px;
}

.kpi-value {

    color: #173326;

    font-size: 31px;

    font-weight: 820;

    margin-top: 8px;
}

.kpi-description {

    color: #8A9991;

    font-size: 11px;

    margin-top: 4px;
}


/* ============================================================
   SECTION
   ============================================================ */

.section {
    margin: 34px 0 15px 0;
}

.section-title {

    color: #183328;

    font-size: 20px;

    font-weight: 790;
}

.section-description {

    color: #7B8C83;

    font-size: 12px;

    margin-top: 4px;
}


/* ============================================================
   AI CARD
   ============================================================ */

.ai-card {

    background: white;

    border: 1px solid #DFE9E3;

    border-radius: 18px;

    padding: 21px;

    box-shadow:
        0 6px 22px rgba(22,53,38,.035);
}

.ai-header {

    display: flex;

    align-items: center;

    gap: 11px;

    margin-bottom: 14px;
}

.ai-icon {

    width: 38px;
    height: 38px;

    border-radius: 11px;

    background: #EAF8F0;

    display: flex;

    align-items: center;

    justify-content: center;

    font-size: 19px;
}

.ai-name {

    font-size: 15px;

    font-weight: 780;

    color: #183328;
}

.ai-label {

    font-size: 10px;

    color: #829189;
}


/* ============================================================
   FINDINGS
   ============================================================ */

.finding {

    border-top: 1px solid #ECF1EE;

    padding: 16px 0;
}

.finding-header {

    display: flex;

    justify-content: space-between;

    align-items: center;
}

.finding-title {

    color: #1B3528;

    font-size: 14px;

    font-weight: 760;
}

.finding-description {

    color: #74857C;

    font-size: 12px;

    line-height: 1.6;

    margin-top: 6px;
}

.risk-high {
    color: #B42318;
    font-weight: 750;
}

.risk-medium {
    color: #B54708;
    font-weight: 750;
}

.risk-low {
    color: #16784B;
    font-weight: 750;
}


/* ============================================================
   ASSET CARD
   ============================================================ */

.asset-card {

    background: white;

    border: 1px solid #E1E9E4;

    border-radius: 17px;

    padding: 20px;

    margin-bottom: 12px;
}

.asset-id {

    font-size: 17px;

    font-weight: 800;

    color: #173326;
}

.asset-fault {

    color: #5D7467;

    font-size: 12px;

    margin-top: 4px;
}


/* ============================================================
   OPERATIONS
   ============================================================ */

.priority-high {

    background: #FFF0EF;

    color: #B42318;

    border: 1px solid #F5D0CC;

    border-radius: 20px;

    padding: 5px 9px;

    font-size: 10px;

    font-weight: 800;
}

.priority-medium {

    background: #FFF6E8;

    color: #B54708;

    border: 1px solid #F2DFC1;

    border-radius: 20px;

    padding: 5px 9px;

    font-size: 10px;

    font-weight: 800;
}


/* ============================================================
   COPILOT
   ============================================================ */

.copilot {

    background:

        linear-gradient(
            135deg,
            #ECF9F2,
            #F8FCF9
        );

    border: 1px solid #D6EBDD;

    border-radius: 19px;

    padding: 24px;
}

.copilot-title {

    color: #174B31;

    font-size: 18px;

    font-weight: 800;
}

.copilot-description {

    color: #667B70;

    font-size: 12px;

    line-height: 1.6;

    margin-top: 6px;
}


/* ============================================================
   REPORT CARD
   ============================================================ */

.report-card {

    background: white;

    border: 1px solid #E0E9E3;

    border-radius: 17px;

    padding: 22px;

    min-height: 170px;
}

.report-title {

    color: #173326;

    font-size: 15px;

    font-weight: 780;
}

.report-description {

    color: #778980;

    font-size: 12px;

    line-height: 1.6;

    margin-top: 7px;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {

    text-align: center;

    color: #91A098;

    font-size: 10px;

    padding-top: 25px;
}

</style>
""",
    unsafe_allow_html=True,
)


# =============================================================================
# DEMO / LLM
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

    df.to_csv(
        "sample_portfolio.csv",
        index=False
    )

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

    return fault.replace(
        "_",
        " "
    ).title()


def risk_level(diagnosis):

    fault = diagnosis.get(
        "fault_hypothesis",
        "none"
    )

    confidence = float(
        diagnosis.get(
            "confidence",
            0
        )
    )

    if fault == "none":
        return "Low"

    if confidence >= .85:
        return "High"

    return "Medium"


def risk_class(level):

    if level == "High":
        return "risk-high"

    if level == "Medium":
        return "risk-medium"

    return "risk-low"


# =============================================================================
# RUN
# =============================================================================

if "result" not in st.session_state:

    with st.spinner(
        "Initializing Green Solutions Intelligence..."
    ):

        st.session_state.result = run_pipeline()

result = st.session_state.result

diagnoses = result.get(
    "diagnoses",
    []
)

total_assets = len(
    diagnoses
)

active_findings = [
    d
    for d in diagnoses
    if d.get("fault_hypothesis") != "none"
]

healthy_assets = (
    total_assets
    - len(active_findings)
)

high_risk_assets = [
    d
    for d in active_findings
    if risk_level(d) == "High"
]

avg_confidence = (
    sum(
        float(d.get("confidence", 0))
        for d in diagnoses
    )
    / total_assets
    if total_assets
    else 0
)

health_score = (
    healthy_assets
    / total_assets
    * 100
    if total_assets
    else 0
)


# =============================================================================
# SESSION NAV
# =============================================================================

if "page" not in st.session_state:

    st.session_state.page = "Overview"


# =============================================================================
# BRAND
# =============================================================================

st.markdown(
    """
<div class="brand-row">

    <div class="brand-left">

        <div class="brand-logo">
            🌱
        </div>

        <div>

            <div class="brand-title">
                Green Solutions
            </div>

            <div class="brand-subtitle">
                Intelligent Sustainability Platform
            </div>

        </div>

    </div>

    <div class="live">
        ● PLATFORM LIVE
    </div>

</div>
""",
    unsafe_allow_html=True,
)


# =============================================================================
# NAV
# =============================================================================

n1, n2, n3, n4, n5 = st.columns(
    [1, 1.15, 1, 1, 1]
)

nav_items = [
    (n1, "Overview", "⌂  Overview"),
    (n2, "AI Intelligence", "✦  AI Intelligence"),
    (n3, "Asset 360", "◉  Asset 360"),
    (n4, "Operations", "⚙  Operations"),
    (n5, "Reports", "▣  Reports"),
]

for col, page, label in nav_items:

    with col:

        if st.button(
            label,
            key=f"nav_{page}",
            use_container_width=True,
        ):

            st.session_state.page = page

            st.rerun()


st.divider()


# =============================================================================
# OVERVIEW
# =============================================================================

if st.session_state.page == "Overview":

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
        Green Solutions continuously analyzes asset performance,
        identifies operational anomalies, explains the evidence,
        and recommends the next best action for your teams.
    </div>

    <div class="hero-status">
        <span>✦ AI Diagnostics</span>
        <span>✦ Evidence-based insights</span>
        <span>✦ Human review</span>
        <span>✦ Action-oriented intelligence</span>
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="page-header">

            <div class="page-title">
                Executive Overview
            </div>

            <div class="page-subtitle">
                A real-time view of portfolio health and AI-generated intelligence.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    k1, k2, k3, k4, k5 = st.columns(5)

    kpis = [
        (
            k1,
            "PORTFOLIO HEALTH",
            f"{health_score:.0f}%",
            "Healthy assets",
        ),
        (
            k2,
            "ASSETS MONITORED",
            str(total_assets),
            "Active portfolio",
        ),
        (
            k3,
            "AI FINDINGS",
            str(len(active_findings)),
            "Issues detected",
        ),
        (
            k4,
            "HIGH PRIORITY",
            str(len(high_risk_assets)),
            "Requires attention",
        ),
        (
            k5,
            "AI CONFIDENCE",
            f"{avg_confidence:.0%}",
            "Average confidence",
        ),
    ]

    for col, label, value, desc in kpis:

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

                    <div class="kpi-description">
                        {desc}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

    # -------------------------------------------------------------------------
    # AI INSIGHTS
    # -------------------------------------------------------------------------

    st.markdown(
        """
        <div class="section">

            <div class="section-title">
                AI Intelligence
            </div>

            <div class="section-description">
                The most important findings generated by the AI diagnostic engine.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns(
        [1.55, 1]
    )

    with left:

        st.markdown(
            """
            <div class="ai-card">

                <div class="ai-header">

                    <div class="ai-icon">
                        ✦
                    </div>

                    <div>

                        <div class="ai-name">
                            Green Solutions Intelligence
                        </div>

                        <div class="ai-label">
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
                <div class="finding">

                    <div class="finding-header">

                        <div class="finding-title">
                            {icon}
                            {d.get("asset_id")}
                            ·
                            {fault_label(d.get("fault_hypothesis"))}
                        </div>

                        <div class="{risk_class(level)}">
                            {float(d.get("confidence", 0)):.0%}
                            confidence
                        </div>

                    </div>

                    <div class="finding-description">

                        {d.get("evidence", "")}

                        <br><br>

                        <b>Recommended action:</b>
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
                    ✦ Green Solutions AI
                </div>

                <div class="copilot-description">
                    Ask questions about your portfolio,
                    asset health, findings and recommended actions.
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        if st.button(
            "Open AI Intelligence →",
            key="overview_ai",
            use_container_width=True,
        ):

            st.session_state.page = "AI Intelligence"

            st.rerun()

        st.write("")

        st.markdown(
            f"""
            <div class="ai-card">

                <div class="ai-name">
                    Operational Priorities
                </div>

                <br>

                <div class="finding-description">

                    🔴 <b>{len(high_risk_assets)}</b>
                    high-priority assets

                    <br><br>

                    🟠 <b>{len(active_findings)}</b>
                    active findings

                    <br><br>

                    🟢 <b>{healthy_assets}</b>
                    healthy assets

                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


# =============================================================================
# AI INTELLIGENCE
# =============================================================================

elif st.session_state.page == "AI Intelligence":

    st.markdown(
        """
        <div class="page-header">

            <div class="page-title">
                AI Intelligence
            </div>

            <div class="page-subtitle">
                Understand what the AI discovered, why it matters,
                and what action is recommended.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="copilot">

            <div class="copilot-title">
                ✦ Ask Green Solutions AI
            </div>

            <div class="copilot-description">
                Explore portfolio intelligence using natural language.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    question = st.text_input(
        "Ask a question",
        placeholder=(
            "Example: Which assets need immediate attention and why?"
        ),
    )

    if question:

        q = question.lower()

        if "attention" in q:

            response = (
                f"{len(active_findings)} assets currently "
                "require attention: "
                + ", ".join(
                    d.get("asset_id")
                    for d in active_findings
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

            response = (
                f"INV-01 is showing "
                f"{fault_label(d.get('fault_hypothesis'))}. "
                f"{d.get('evidence')} "
                f"Recommended action: "
                f"{d.get('recommended_action')}"
                if d
                else "INV-01 was not found."
            )

        elif "communication" in q:

            communication = [
                d for d in diagnoses
                if d.get("fault_hypothesis")
                == "comm_dropout"
            ]

            response = (
                "Communication anomalies were detected for: "
                + ", ".join(
                    d.get("asset_id")
                    for d in communication
                )
                if communication
                else
                "No communication anomalies were detected."
            )

        elif "action" in q or "technician" in q:

            response = "\n\n".join(
                f"{d.get('asset_id')}: "
                f"{d.get('recommended_action')}"
                for d in active_findings
            )

        else:

            response = (
                "Green Solutions AI can currently analyze "
                "asset health, findings, evidence, confidence "
                "and recommended actions."
            )

        st.markdown("### AI Response")

        st.info(response)

    st.markdown(
        """
        <div class="section">

            <div class="section-title">
                Diagnostic Findings
            </div>

            <div class="section-description">
                Evidence-backed findings generated by the AI engine.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    for d in diagnoses:

        level = risk_level(d)

        with st.expander(
            f"{'🔴' if level == 'High' else '🟠' if level == 'Medium' else '🟢'} "
            f"{d.get('asset_id')} — "
            f"{fault_label(d.get('fault_hypothesis'))}"
        ):

            c1, c2, c3 = st.columns(3)

            with c1:

                st.metric(
                    "AI Confidence",
                    f"{float(d.get('confidence', 0)):.0%}"
                )

            with c2:

                st.metric(
                    "Priority",
                    level
                )

            with c3:

                st.metric(
                    "Status",
                    "Needs Action"
                    if d.get("fault_hypothesis") != "none"
                    else "Healthy"
                )

            st.markdown("**Evidence**")

            st.write(
                d.get("evidence", "")
            )

            st.markdown("**Recommended Action**")

            st.success(
                d.get(
                    "recommended_action",
                    ""
                )
            )


# =============================================================================
# ASSET 360
# =============================================================================

elif st.session_state.page == "Asset 360":

    st.markdown(
        """
        <div class="page-header">

            <div class="page-title">
                Asset 360
            </div>

            <div class="page-subtitle">
                A complete intelligence view for every monitored asset.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    asset_options = [
        d.get("asset_id")
        for d in diagnoses
    ]

    selected_asset = st.selectbox(
        "Select asset",
        asset_options
    )

    selected = next(
        (
            d for d in diagnoses
            if d.get("asset_id")
            == selected_asset
        ),
        None,
    )

    if selected:

        level = risk_level(selected)

        st.markdown(
            f"""
            <div class="asset-card">

                <div class="asset-id">
                    {selected.get("asset_id")}
                </div>

                <div class="asset-fault">
                    {fault_label(selected.get("fault_hypothesis"))}
                    ·
                    {level} priority
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        a1, a2, a3 = st.columns(3)

        with a1:

            st.metric(
                "AI Confidence",
                f"{float(selected.get('confidence', 0)):.0%}"
            )

        with a2:

            st.metric(
                "Risk",
                level
            )

        with a3:

            st.metric(
                "Status",
                "Attention Required"
                if selected.get("fault_hypothesis") != "none"
                else "Healthy"
            )

        st.markdown(
            """
            <div class="section">

                <div class="section-title">
                    AI Diagnosis
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns(2)

        with c1:

            st.markdown(
                """
                <div class="ai-card">

                    <div class="ai-name">
                        What is happening?
                    </div>

                    <br>

                """,
                unsafe_allow_html=True,
            )

            st.write(
                selected.get(
                    "evidence",
                    ""
                )
            )

            st.markdown(
                "</div>",
                unsafe_allow_html=True,
            )

        with c2:

            st.markdown(
                """
                <div class="ai-card">

                    <div class="ai-name">
                        Recommended next action
                    </div>

                    <br>

                """,
                unsafe_allow_html=True,
            )

            st.success(
                selected.get(
                    "recommended_action",
                    ""
                )
            )

            st.markdown(
                "</div>",
                unsafe_allow_html=True,
            )


# =============================================================================
# OPERATIONS
# =============================================================================

elif st.session_state.page == "Operations":

    st.markdown(
        """
        <div class="page-header">

            <div class="page-title">
                Operations
            </div>

            <div class="page-subtitle">
                Convert AI findings into prioritized operational actions.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    if not active_findings:

        st.success(
            "No operational actions are currently required."
        )

    else:

        for index, d in enumerate(
            active_findings,
            start=1
        ):

            level = risk_level(d)

            with st.container(border=True):

                c1, c2, c3, c4 = st.columns(
                    [.4, 1.3, 2.2, 3.5]
                )

                with c1:

                    st.markdown(
                        f"### {index}"
                    )

                with c2:

                    st.markdown(
                        f"**{d.get('asset_id')}**"
                    )

                    if level == "High":

                        st.markdown(
                            '<span class="priority-high">'
                            'HIGH PRIORITY'
                            '</span>',
                            unsafe_allow_html=True,
                        )

                    else:

                        st.markdown(
                            '<span class="priority-medium">'
                            'MEDIUM PRIORITY'
                            '</span>',
                            unsafe_allow_html=True,
                        )

                with c3:

                    st.markdown(
                        f"**{fault_label(d.get('fault_hypothesis'))}**"
                    )

                    st.caption(
                        f"Confidence: "
                        f"{float(d.get('confidence', 0)):.0%}"
                    )

                with c4:

                    st.write(
                        d.get(
                            "recommended_action",
                            ""
                        )
                    )

                    if st.button(
                        "Review Action",
                        key=f"review_{index}",
                    ):

                        st.info(
                            "Human review workflow selected. "
                            "Production version can route this action "
                            "through an approval workflow."
                        )


# =============================================================================
# REPORTS
# =============================================================================

elif st.session_state.page == "Reports":

    st.markdown(
        """
        <div class="page-header">

            <div class="page-title">
                Reports
            </div>

            <div class="page-subtitle">
                AI-generated documentation for operations,
                asset owners and compliance teams.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    r1, r2, r3 = st.columns(3)

    report_cards = [
        (
            r1,
            "Field Work Order",
            "Technician-ready actions generated from AI findings.",
        ),
        (
            r2,
            "Owner Report",
            "Plain-language portfolio summary for asset owners.",
        ),
        (
            r3,
            "Compliance Summary",
            "Formal record of findings, actions and status.",
        ),
    ]

    for col, title, description in report_cards:

        with col:

            st.markdown(
                f"""
                <div class="report-card">

                    <div class="report-title">
                        {title}
                    </div>

                    <div class="report-description">
                        {description}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")

    tab1, tab2, tab3 = st.tabs(
        [
            "Field Work Order",
            "Owner Report",
            "Compliance Summary",
        ]
    )

    report_data = [
        (
            tab1,
            "work_order_text",
            "green_solutions_work_order.txt",
        ),
        (
            tab2,
            "owner_report_text",
            "green_solutions_owner_report.txt",
        ),
        (
            tab3,
            "compliance_summary_text",
            "green_solutions_compliance.txt",
        ),
    ]

    for tab, key, filename in report_data:

        with tab:

            text = result.get(
                key,
                "(No report generated)"
            )

            st.text_area(
                "Generated report",
                text,
                height=350,
            )

            st.download_button(
                "Download Report",
                data=text,
                file_name=filename,
                mime="text/plain",
                use_container_width=True,
            )

    # -------------------------------------------------------------------------
    # FEEDBACK
    # -------------------------------------------------------------------------

    st.markdown(
        """
        <div class="section">

            <div class="section-title">
                Product Feedback
            </div>

            <div class="section-description">
                Help us validate whether Green Solutions is useful
                for real sustainability operations.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("feedback"):

        trust = st.slider(
            "How much would you trust the AI findings?",
            1,
            5,
            3,
        )

        clarity = st.slider(
            "How clear were the findings and recommendations?",
            1,
            5,
            3,
        )

        time_saved = st.radio(
            "Would this save your team time?",
            [
                "Yes, clearly",
                "Somewhat",
                "Not really",
                "Not sure",
            ],
        )

        role = st.text_input(
            "Your role"
        )

        comments = st.text_area(
            "What would make Green Solutions more useful?"
        )

        submitted = st.form_submit_button(
            "Submit Feedback"
        )

        if submitted:

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
                "Thank you. Your feedback has been recorded."
            )


# =============================================================================
# FOOTER
# =============================================================================

st.divider()

st.markdown(
    f"""
    <div class="footer">

        🌱 Green Solutions
        &nbsp; • &nbsp;
        Intelligent Sustainability Platform
        &nbsp; • &nbsp;
        {'Demo AI' if demo_mode_active() else 'Live AI'}
        &nbsp; • &nbsp;
        {datetime.now().year}

    </div>
    """,
    unsafe_allow_html=True,
)
