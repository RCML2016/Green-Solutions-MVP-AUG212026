"""
Green Solutions
Enterprise AI Sustainability Intelligence Platform

V4 Premium Enterprise UI

Navigation:
    Overview
    AI Intelligence
    Asset 360
    Operations
    Reports

Backend:
    LangGraph
    AI Diagnostics
    Human Review
    AI Report Generation
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
    page_title="Green Solutions | Intelligent Sustainability",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =============================================================================
# PREMIUM ENTERPRISE THEME
# =============================================================================

st.markdown(
    """
<style>

/* =========================================================
   GLOBAL
   ========================================================= */

.stApp {
    background: #F5F7F6;
    color: #172A21;
}

.main .block-container {
    max-width: 1440px;
    padding: 1.0rem 2.4rem 4rem 2.4rem;
}

#MainMenu,
footer,
header {
    visibility: hidden;
}

* {
    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;
}


/* =========================================================
   BRAND HEADER
   ========================================================= */

.brand-wrapper {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 5px 0 10px 0;
}

.brand-left {
    display: flex;
    align-items: center;
    gap: 12px;
}

.brand-mark {
    width: 40px;
    height: 40px;
    border-radius: 12px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: linear-gradient(
        135deg,
        #087443,
        #35B875
    );

    color: white;
    font-size: 20px;

    box-shadow:
        0 8px 22px rgba(8,116,67,.20);
}

.brand-name {
    font-size: 18px;
    font-weight: 800;
    letter-spacing: -.3px;
    color: #17362A;
}

.brand-tagline {
    font-size: 9px;
    color: #82938B;
    letter-spacing: .8px;
    text-transform: uppercase;
    margin-top: 2px;
}

.live-status {
    display: flex;
    align-items: center;
    gap: 6px;

    background: #EAF8F0;
    border: 1px solid #CDEADB;

    color: #177849;

    padding: 7px 12px;

    border-radius: 20px;

    font-size: 9px;
    font-weight: 800;
    letter-spacing: .7px;
}


/* =========================================================
   NAVIGATION
   ========================================================= */

div.stButton > button {

    border: 1px solid #E0E8E3;

    background: rgba(255,255,255,.88);

    color: #5A6E64;

    border-radius: 9px;

    min-height: 38px;

    font-size: 11px;

    font-weight: 700;

    transition:
        all .15s ease;
}

div.stButton > button:hover {

    border-color: #A6D4BA;

    background: #F1FAF5;

    color: #087443;

    transform: translateY(-1px);
}


/* =========================================================
   HERO
   ========================================================= */

.hero {

    position: relative;

    overflow: hidden;

    min-height: 315px;

    margin-top: 15px;

    padding: 48px 55px;

    border-radius: 26px;

    background:
        radial-gradient(
            circle at 85% 15%,
            rgba(80,220,143,.22),
            transparent 25%
        ),
        radial-gradient(
            circle at 65% 100%,
            rgba(28,143,86,.20),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #06291B,
            #0B422A 55%,
            #0A5737
        );

    box-shadow:
        0 25px 65px rgba(13,67,43,.17);
}

.hero::after {

    content: "";

    position: absolute;

    right: -100px;
    bottom: -120px;

    width: 330px;
    height: 330px;

    border-radius: 50%;

    border: 1px solid rgba(255,255,255,.08);
}

.hero-eyebrow {

    color: #7DE0AA;

    font-size: 10px;

    font-weight: 850;

    letter-spacing: 2px;

    text-transform: uppercase;
}

.hero-title {

    color: white;

    font-size: 44px;

    line-height: 1.08;

    font-weight: 850;

    letter-spacing: -1.5px;

    max-width: 750px;

    margin-top: 13px;
}

.hero-title span {
    color: #7FE2AA;
}

.hero-description {

    color: #C4D9CD;

    max-width: 690px;

    font-size: 14px;

    line-height: 1.7;

    margin-top: 17px;
}

.hero-pills {

    display: flex;

    gap: 9px;

    flex-wrap: wrap;

    margin-top: 23px;
}

.hero-pill {

    padding: 7px 11px;

    border-radius: 20px;

    background: rgba(255,255,255,.08);

    border: 1px solid rgba(255,255,255,.10);

    color: #D1E6D9;

    font-size: 9px;

    font-weight: 700;
}


/* =========================================================
   PAGE HEADERS
   ========================================================= */

.page-header {
    margin: 27px 0 19px 0;
}

.page-title {

    color: #17362A;

    font-size: 27px;

    font-weight: 820;

    letter-spacing: -.5px;
}

.page-subtitle {

    color: #7B8B84;

    font-size: 12px;

    margin-top: 4px;

    line-height: 1.5;
}


/* =========================================================
   KPI
   ========================================================= */

.kpi-card {

    background: white;

    border: 1px solid #E0E8E3;

    border-radius: 16px;

    padding: 20px;

    min-height: 125px;

    box-shadow:
        0 5px 22px rgba(23,54,42,.035);

    transition:
        transform .15s ease,
        box-shadow .15s ease;
}

.kpi-card:hover {

    transform: translateY(-2px);

    box-shadow:
        0 10px 30px rgba(23,54,42,.07);
}

.kpi-label {

    color: #83928B;

    font-size: 9px;

    font-weight: 800;

    letter-spacing: .9px;
}

.kpi-value {

    color: #18362A;

    font-size: 30px;

    font-weight: 850;

    margin-top: 8px;

    letter-spacing: -.8px;
}

.kpi-meta {

    color: #91A098;

    font-size: 10px;

    margin-top: 4px;
}


/* =========================================================
   CONTENT CARDS
   ========================================================= */

.card {

    background: white;

    border: 1px solid #E0E8E3;

    border-radius: 17px;

    padding: 21px;

    box-shadow:
        0 5px 22px rgba(23,54,42,.035);
}

.card-title {

    color: #19362A;

    font-size: 15px;

    font-weight: 800;
}

.card-subtitle {

    color: #87958E;

    font-size: 10px;

    margin-top: 3px;
}


/* =========================================================
   AI
   ========================================================= */

.ai-badge {

    display: inline-flex;

    align-items: center;

    gap: 6px;

    background: #EAF8F0;

    border: 1px solid #D0EBDD;

    color: #157548;

    border-radius: 20px;

    padding: 5px 9px;

    font-size: 9px;

    font-weight: 800;
}

.finding-row {

    padding: 16px 0;

    border-bottom: 1px solid #EDF1EF;
}

.finding-row:last-child {
    border-bottom: none;
}

.finding-asset {

    color: #18362A;

    font-size: 13px;

    font-weight: 800;
}

.finding-fault {

    color: #687B72;

    font-size: 11px;

    margin-top: 3px;
}

.finding-evidence {

    color: #75857E;

    font-size: 11px;

    line-height: 1.55;

    margin-top: 8px;
}


/* =========================================================
   STATUS
   ========================================================= */

.status-high {

    background: #FFF0EF;

    border: 1px solid #F3D1CC;

    color: #B42318;

    padding: 4px 8px;

    border-radius: 15px;

    font-size: 8px;

    font-weight: 850;
}

.status-medium {

    background: #FFF7E9;

    border: 1px solid #F1DFC1;

    color: #B54708;

    padding: 4px 8px;

    border-radius: 15px;

    font-size: 8px;

    font-weight: 850;
}

.status-low {

    background: #EAF8F0;

    border: 1px solid #D0EBDD;

    color: #18794C;

    padding: 4px 8px;

    border-radius: 15px;

    font-size: 8px;

    font-weight: 850;
}


/* =========================================================
   ASSET
   ========================================================= */

.asset-hero {

    background:
        linear-gradient(
            135deg,
            #FFFFFF,
            #F1F8F4
        );

    border: 1px solid #DDE9E2;

    border-radius: 20px;

    padding: 25px;

    margin-bottom: 17px;
}

.asset-id {

    color: #17362A;

    font-size: 24px;

    font-weight: 850;
}

.asset-type {

    color: #7D8D85;

    font-size: 11px;

    margin-top: 4px;
}


/* =========================================================
   OPERATIONS
   ========================================================= */

.operation-card {

    background: white;

    border: 1px solid #E0E8E3;

    border-radius: 16px;

    padding: 19px;

    margin-bottom: 11px;

    box-shadow:
        0 4px 17px rgba(23,54,42,.025);
}

.operation-number {

    color: #9AA9A1;

    font-size: 11px;

    font-weight: 800;
}

.operation-asset {

    color: #17362A;

    font-size: 14px;

    font-weight: 800;
}

.operation-action {

    color: #687B72;

    font-size: 11px;

    line-height: 1.5;

    margin-top: 5px;
}


/* =========================================================
   REPORT
   ========================================================= */

.report-card {

    background: white;

    border: 1px solid #E0E8E3;

    border-radius: 17px;

    padding: 21px;

    min-height: 155px;

    box-shadow:
        0 5px 20px rgba(23,54,42,.035);
}

.report-icon {

    width: 39px;
    height: 39px;

    border-radius: 11px;

    background: #EDF8F2;

    display: flex;

    align-items: center;

    justify-content: center;

    font-size: 18px;

    margin-bottom: 12px;
}

.report-name {

    color: #18362A;

    font-size: 14px;

    font-weight: 800;
}

.report-description {

    color: #7A8B83;

    font-size: 10px;

    line-height: 1.55;

    margin-top: 5px;
}


/* =========================================================
   COPILOT
   ========================================================= */

.copilot {

    border-radius: 18px;

    padding: 22px;

    background:
        linear-gradient(
            135deg,
            #EAF8F0,
            #F7FBF8
        );

    border: 1px solid #D4EBDD;
}

.copilot-title {

    color: #164E33;

    font-size: 16px;

    font-weight: 820;
}

.copilot-description {

    color: #6F8178;

    font-size: 11px;

    line-height: 1.6;

    margin-top: 5px;
}


/* =========================================================
   FOOTER
   ========================================================= */

.footer {

    text-align: center;

    color: #98A59F;

    font-size: 9px;

    padding: 20px 0 5px 0;
}


/* =========================================================
   STREAMLIT INPUTS
   ========================================================= */

.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {

    border-radius: 9px !important;

    border-color: #DCE6E0 !important;
}

.stSlider {
    padding-top: 5px;
}


/* =========================================================
   TABS
   ========================================================= */

button[data-baseweb="tab"] {

    font-size: 11px !important;

    font-weight: 700 !important;
}


/* =========================================================
   EXPANDERS
   ========================================================= */

.streamlit-expanderHeader {

    font-size: 12px !important;

    font-weight: 700 !important;
}

</style>
""",
    unsafe_allow_html=True,
)


# =============================================================================
# DEMO AI
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

    if diagnosis.get("fault_hypothesis") == "none":
        return "Low"

    confidence = float(
        diagnosis.get("confidence", 0)
    )

    if confidence >= 0.80:
        return "High"

    return "Medium"


def status_html(level):

    if level == "High":

        return (
            '<span class="status-high">'
            'HIGH PRIORITY'
            '</span>'
        )

    if level == "Medium":

        return (
            '<span class="status-medium">'
            'MEDIUM PRIORITY'
            '</span>'
        )

    return (
        '<span class="status-low">'
        'HEALTHY'
        '</span>'
    )


# =============================================================================
# LOAD PIPELINE
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

active_findings = [
    d for d in diagnoses
    if d.get("fault_hypothesis") != "none"
]

healthy_assets = [
    d for d in diagnoses
    if d.get("fault_hypothesis") == "none"
]

high_risk = [
    d for d in active_findings
    if risk_level(d) == "High"
]

medium_risk = [
    d for d in active_findings
    if risk_level(d) == "Medium"
]

total_assets = len(diagnoses)

health_score = (
    len(healthy_assets) / total_assets * 100
    if total_assets
    else 0
)

avg_confidence = (
    sum(
        float(d.get("confidence", 0))
        for d in diagnoses
    )
    / total_assets
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
<div class="brand-wrapper">

    <div class="brand-left">

        <div class="brand-mark">
            🌱
        </div>

        <div>

            <div class="brand-name">
                Green Solutions
            </div>

            <div class="brand-tagline">
                Intelligent Sustainability Platform
            </div>

        </div>

    </div>

    <div class="live-status">
        ● PLATFORM LIVE
    </div>

</div>
""",
    unsafe_allow_html=True,
)


# =============================================================================
# NAVIGATION
# =============================================================================

columns = st.columns(
    [1, 1.25, 1, 1, 1]
)

navigation = [
    ("Overview", "⌂  Overview"),
    ("AI Intelligence", "✦  AI Intelligence"),
    ("Asset 360", "◉  Asset 360"),
    ("Operations", "⚙  Operations"),
    ("Reports", "▣  Reports"),
]

for col, (page, label) in zip(
    columns,
    navigation
):

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
        """
<div class="hero">

    <div class="hero-eyebrow">
        AI-POWERED SUSTAINABILITY INTELLIGENCE
    </div>

    <div class="hero-title">
        Turn sustainability data<br>
        into <span>intelligent action.</span>
    </div>

    <div class="hero-description">
        Green Solutions analyzes renewable-energy asset performance,
        identifies anomalies, explains the evidence behind each finding,
        and recommends the next best operational action.
    </div>

    <div class="hero-pills">

        <div class="hero-pill">
            ✦ AI Diagnostics
        </div>

        <div class="hero-pill">
            ✦ Evidence-Based Intelligence
        </div>

        <div class="hero-pill">
            ✦ Human Review
        </div>

        <div class="hero-pill">
            ✦ Operational Recommendations
        </div>

    </div>

</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="page-header">

    <div class="page-title">
        Portfolio Overview
    </div>

    <div class="page-subtitle">
        Executive view of asset health, AI findings and operational priorities.
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

    # KPI ROW

    kpis = [
        (
            "PORTFOLIO HEALTH",
            f"{health_score:.0f}%",
            "Healthy asset ratio",
        ),
        (
            "ASSETS MONITORED",
            str(total_assets),
            "Active portfolio",
        ),
        (
            "AI FINDINGS",
            str(len(active_findings)),
            "Anomalies identified",
        ),
        (
            "HIGH PRIORITY",
            str(len(high_risk)),
            "Requires attention",
        ),
        (
            "AI CONFIDENCE",
            f"{avg_confidence:.0%}",
            "Average confidence",
        ),
    ]

    kcols = st.columns(5)

    for col, (
        label,
        value,
        meta,
    ) in zip(
        kcols,
        kpis
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

    <div class="kpi-meta">
        {meta}
    </div>

</div>
""",
                unsafe_allow_html=True,
            )

    # AI + OPERATIONS

    st.markdown(
        """
<div class="page-header">

    <div class="page-title">
        Intelligence at a Glance
    </div>

    <div class="page-subtitle">
        AI findings and recommended operational priorities.
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
<div class="card">

    <div style="display:flex;
                justify-content:space-between;
                align-items:center;">

        <div>

            <div class="card-title">
                AI Intelligence
            </div>

            <div class="card-subtitle">
                Evidence-backed portfolio findings
            </div>

        </div>

        <div class="ai-badge">
            ✦ AI ACTIVE
        </div>

    </div>
""",
            unsafe_allow_html=True,
        )

        for d in diagnoses:

            level = risk_level(d)

            st.markdown(
                f"""
<div class="finding-row">

    <div style="display:flex;
                justify-content:space-between;
                align-items:center;">

        <div>

            <div class="finding-asset">
                {d.get("asset_id")}
                ·
                {fault_label(d.get("fault_hypothesis"))}
            </div>

            <div class="finding-fault">
                {d.get("recommended_action")}
            </div>

        </div>

        <div>
            {status_html(level)}
        </div>

    </div>

    <div class="finding-evidence">
        {d.get("evidence")}
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
            f"""
<div class="card">

    <div class="card-title">
        Operational Priorities
    </div>

    <div class="card-subtitle">
        Where your team should focus next
    </div>

    <br>

    <div class="finding-row">

        <div class="finding-asset">
            🔴 High Priority
        </div>

        <div class="finding-evidence">
            {len(high_risk)} assets require immediate attention.
        </div>

    </div>

    <div class="finding-row">

        <div class="finding-asset">
            🟠 Medium Priority
        </div>

        <div class="finding-evidence">
            {len(medium_risk)} assets require review.
        </div>

    </div>

    <div class="finding-row">

        <div class="finding-asset">
            🟢 Healthy
        </div>

        <div class="finding-evidence">
            {len(healthy_assets)} assets currently show nominal behavior.
        </div>

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
        Explore the reasoning, evidence, confidence and recommended actions
        behind every AI finding.
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="copilot">

    <div class="copilot-title">
        ✦ Green Solutions Intelligence
    </div>

    <div class="copilot-description">
        Ask questions about your portfolio, assets, findings and
        recommended operational actions.
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

    question = st.text_input(
        "Ask Green Solutions AI",
        placeholder=(
            "Which assets require immediate attention and why?"
        ),
    )

    if question:

        q = question.lower()

        if "attention" in q or "priority" in q:

            response = (
                f"There are {len(active_findings)} active findings. "
                f"{len(high_risk)} are classified as high priority. "
                f"The assets requiring attention are: "
                + ", ".join(
                    d.get("asset_id")
                    for d in active_findings
                )
                + "."
            )

        elif "healthy" in q:

            response = (
                f"{len(healthy_assets)} assets are currently classified "
                "as healthy based on the available performance data."
            )

        elif "inv-01" in q:

            asset = next(
                (
                    d for d in diagnoses
                    if d.get("asset_id") == "INV-01"
                ),
                None,
            )

            if asset:

                response = (
                    f"INV-01 is showing "
                    f"{fault_label(asset.get('fault_hypothesis'))}. "
                    f"Evidence: {asset.get('evidence')}. "
                    f"Recommended action: "
                    f"{asset.get('recommended_action')}."
                )

            else:

                response = "INV-01 was not found."

        elif "action" in q:

            response = "\n\n".join(
                f"{d.get('asset_id')}: "
                f"{d.get('recommended_action')}"
                for d in active_findings
            )

        else:

            response = (
                "I can currently analyze asset health, AI findings, "
                "confidence, evidence and recommended actions."
            )

        st.markdown("### Intelligence Response")

        st.info(response)

    st.markdown(
        """
<div class="page-header">

    <div class="page-title">
        Diagnostic Findings
    </div>

    <div class="page-subtitle">
        Detailed AI findings across the portfolio.
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

    for d in diagnoses:

        level = risk_level(d)

        with st.expander(
            f"{d.get('asset_id')}  ·  "
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
                    "AI Status",
                    (
                        "Finding"
                        if d.get("fault_hypothesis") != "none"
                        else "Healthy"
                    )
                )

            st.markdown("**Evidence**")

            st.write(
                d.get(
                    "evidence",
                    ""
                )
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
        A complete intelligence view of every monitored asset.
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

    asset_ids = [
        d.get("asset_id")
        for d in diagnoses
    ]

    selected_id = st.selectbox(
        "Select asset",
        asset_ids,
    )

    selected = next(
        (
            d for d in diagnoses
            if d.get("asset_id") == selected_id
        ),
        None,
    )

    if selected:

        level = risk_level(selected)

        st.markdown(
            f"""
<div class="asset-hero">

    <div style="display:flex;
                justify-content:space-between;
                align-items:flex-start;">

        <div>

            <div class="asset-id">
                {selected.get("asset_id")}
            </div>

            <div class="asset-type">
                Solar generation asset · AI monitored
            </div>

        </div>

        <div>
            {status_html(level)}
        </div>

    </div>

</div>
""",
            unsafe_allow_html=True,
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "AI Confidence",
                f"{float(selected.get('confidence', 0)):.0%}"
            )

        with c2:

            st.metric(
                "Priority",
                level
            )

        with c3:

            st.metric(
                "Diagnosis",
                fault_label(
                    selected.get(
                        "fault_hypothesis"
                    )
                )
            )

        with c4:

            st.metric(
                "Monitoring",
                "Active"
            )

        st.markdown(
            """
<div class="page-header">

    <div class="page-title">
        Asset Intelligence
    </div>

</div>
""",
            unsafe_allow_html=True,
        )

        left, right = st.columns(2)

        with left:

            st.markdown(
                f"""
<div class="card">

    <div class="card-title">
        What is happening?
    </div>

    <div class="card-subtitle">
        AI-generated evidence
    </div>

    <br>

    <div class="finding-evidence"
         style="font-size:12px;">

        {selected.get("evidence")}

    </div>

</div>
""",
                unsafe_allow_html=True,
            )

        with right:

            st.markdown(
                f"""
<div class="card">

    <div class="card-title">
        Recommended Next Action
    </div>

    <div class="card-subtitle">
        AI operational recommendation
    </div>

    <br>

    <div class="finding-evidence"
         style="font-size:12px;">

        {selected.get("recommended_action")}

    </div>

</div>
""",
                unsafe_allow_html=True,
            )

        st.markdown(
            """
<div class="page-header">

    <div class="page-title">
        AI Governance
    </div>

    <div class="page-subtitle">
        Every AI recommendation includes confidence and evidence
        before operational action.
    </div>

</div>
""",
            unsafe_allow_html=True,
        )

        st.info(
            "This recommendation should be reviewed by an authorized "
            "operator before production execution."
        )


# =============================================================================
# OPERATIONS
# =============================================================================

elif st.session_state.page == "Operations":

    st.markdown(
        """
<div class="page-header">

    <div class="page-title">
        Operations Command Center
    </div>

    <div class="page-subtitle">
        Convert AI findings into prioritized operational work.
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

    o1, o2, o3 = st.columns(3)

    with o1:

        st.metric(
            "High Priority",
            len(high_risk)
        )

    with o2:

        st.metric(
            "Medium Priority",
            len(medium_risk)
        )

    with o3:

        st.metric(
            "Total Actions",
            len(active_findings)
        )

    st.markdown(
        """
<div class="page-header">

    <div class="page-title">
        Recommended Actions
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

    for index, d in enumerate(
        active_findings,
        start=1
    ):

        level = risk_level(d)

        st.markdown(
            f"""
<div class="operation-card">

    <div style="display:flex;
                justify-content:space-between;
                align-items:flex-start;">

        <div>

            <div class="operation-number">
                ACTION {index:02d}
            </div>

            <div class="operation-asset">
                {d.get("asset_id")}
                ·
                {fault_label(d.get("fault_hypothesis"))}
            </div>

            <div class="operation-action">
                {d.get("recommended_action")}
            </div>

        </div>

        <div>
            {status_html(level)}
        </div>

    </div>

</div>
""",
            unsafe_allow_html=True,
        )

        if st.button(
            "Review Action",
            key=f"operation_{index}",
        ):

            st.success(
                f"Review initiated for {d.get('asset_id')}. "
                "Production version can route this through "
                "an approval and assignment workflow."
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
        AI-generated documentation for field teams, asset owners
        and compliance stakeholders.
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

    report_cards = [
        (
            "📋",
            "Field Work Order",
            "Technician-ready operational actions.",
        ),
        (
            "◉",
            "Owner Report",
            "Executive-friendly portfolio summary.",
        ),
        (
            "✓",
            "Compliance Summary",
            "Formal findings and action record.",
        ),
    ]

    cols = st.columns(3)

    for col, (
        icon,
        title,
        description,
    ) in zip(
        cols,
        report_cards
    ):

        with col:

            st.markdown(
                f"""
<div class="report-card">

    <div class="report-icon">
        {icon}
    </div>

    <div class="report-name">
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

    reports = [
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

    for tab, key, filename in reports:

        with tab:

            report_text = result.get(
                key,
                "(No report generated)"
            )

            st.text_area(
                "Generated report",
                report_text,
                height=330,
            )

            st.download_button(
                "Download Report",
                data=report_text,
                file_name=filename,
                mime="text/plain",
                use_container_width=True,
            )

    # FEEDBACK

    st.markdown(
        """
<div class="page-header">

    <div class="page-title">
        Product Feedback
    </div>

    <div class="page-subtitle">
        Help validate Green Solutions with real operational users.
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

    with st.form("feedback_form"):

        c1, c2 = st.columns(2)

        with c1:

            trust = st.slider(
                "How much would you trust the AI findings?",
                1,
                5,
                3,
            )

        with c2:

            clarity = st.slider(
                "How clear are the recommendations?",
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
            horizontal=True,
        )

        role = st.text_input(
            "Your role"
        )

        comments = st.text_area(
            "What would make Green Solutions more useful?"
        )

        submitted = st.form_submit_button(
            "Submit Feedback",
            use_container_width=True,
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

mode = (
    "Demo AI"
    if demo_mode_active()
    else "Live AI"
)

st.markdown(
    f"""
<div class="footer">

    🌱 <b>Green Solutions</b>
    &nbsp; · &nbsp;
    Intelligent Sustainability Platform
    &nbsp; · &nbsp;
    {mode}
    &nbsp; · &nbsp;
    {datetime.now().year}

</div>
""",
    unsafe_allow_html=True,
)
