"""
Green Solutions
Enterprise AI Sustainability Intelligence Platform
UI V4

Navigation:
    Overview
    AI Intelligence
    Asset 360
    Operations
    Reports

Backend remains compatible with:
    agents.py
    graph.py
    state.py
    synthetic_data.py
    feedback_store.py
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
    page_title="Green Solutions | AI Sustainability",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =============================================================================
# PREMIUM UI
# =============================================================================

st.markdown(
    """
<style>

/* ============================================================
   ROOT
   ============================================================ */

:root {
    --green-950: #06261A;
    --green-900: #083A27;
    --green-800: #0B5135;
    --green-700: #0E7048;
    --green-600: #15915B;
    --green-500: #31B875;
    --green-100: #E9F8F0;
    --green-050: #F4FBF7;

    --ink: #142D22;
    --muted: #718178;
    --soft: #9AA8A1;

    --border: #E2EAE5;
    --surface: #FFFFFF;
    --background: #F5F8F6;

    --danger: #C7352C;
    --danger-bg: #FFF1EF;

    --warning: #B76A08;
    --warning-bg: #FFF7E9;

    --success: #147A4D;
    --success-bg: #ECF9F2;
}


/* ============================================================
   APP
   ============================================================ */

.stApp {
    background: var(--background);
    color: var(--ink);
}

.main .block-container {
    max-width: 1440px;
    padding: 1.1rem 2.4rem 4rem 2.4rem;
}

#MainMenu,
footer,
header {
    visibility: hidden;
}


/* ============================================================
   TEXT
   ============================================================ */

h1, h2, h3, h4, h5 {
    color: var(--ink) !important;
}


/* ============================================================
   TOP BRAND
   ============================================================ */

.brand-shell {
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

.brand-mark {
    width: 43px;
    height: 43px;
    border-radius: 13px;

    display: flex;
    align-items: center;
    justify-content: center;

    color: white;
    font-size: 21px;

    background:
        linear-gradient(
            135deg,
            var(--green-800),
            var(--green-500)
        );

    box-shadow:
        0 9px 24px rgba(9, 95, 56, .20);
}

.brand-name {
    font-size: 18px;
    font-weight: 850;
    color: var(--ink);
    line-height: 1;
}

.brand-tagline {
    color: var(--muted);
    font-size: 9px;
    font-weight: 650;
    letter-spacing: .55px;
    margin-top: 5px;
    text-transform: uppercase;
}

.live-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;

    background: var(--green-100);
    border: 1px solid #CBEADB;

    color: var(--success);

    padding: 7px 12px;

    border-radius: 30px;

    font-size: 9px;
    font-weight: 850;
    letter-spacing: .7px;
}


/* ============================================================
   NAVIGATION
   ============================================================ */

.nav-container {
    margin: 8px 0 15px 0;
}

div.stButton > button {
    border-radius: 10px !important;

    border: 1px solid var(--border) !important;

    background: white !important;

    color: #50645A !important;

    min-height: 39px !important;

    font-size: 11px !important;

    font-weight: 750 !important;

    transition: all .15s ease !important;
}

div.stButton > button:hover {
    border-color: #A9D8BD !important;

    background: var(--green-050) !important;

    color: var(--green-800) !important;

    transform: translateY(-1px);
}


/* ============================================================
   HERO
   ============================================================ */

.hero {
    position: relative;
    overflow: hidden;

    border-radius: 27px;

    padding: 45px 52px;

    margin: 20px 0 27px 0;

    background:
        radial-gradient(
            circle at 88% 18%,
            rgba(73, 214, 135, .22),
            transparent 24%
        ),
        radial-gradient(
            circle at 72% 85%,
            rgba(38, 151, 93, .20),
            transparent 25%
        ),
        linear-gradient(
            125deg,
            #06251A,
            #083E29 57%,
            #0B5939
        );

    box-shadow:
        0 25px 70px rgba(6, 57, 36, .17);
}

.hero::after {
    content: "";

    position: absolute;

    right: -80px;
    bottom: -110px;

    width: 340px;
    height: 340px;

    border-radius: 50%;

    border: 1px solid rgba(146, 235, 179, .12);
}

.hero-eyebrow {
    color: #75DDA5;

    font-size: 10px;

    font-weight: 850;

    letter-spacing: 1.8px;

    text-transform: uppercase;

    margin-bottom: 13px;
}

.hero-title {
    color: white;

    font-size: 42px;

    line-height: 1.08;

    font-weight: 850;

    letter-spacing: -1.2px;

    max-width: 780px;
}

.hero-title span {
    color: #78DEA8;
}

.hero-copy {
    color: #BFD8C9;

    max-width: 700px;

    font-size: 14px;

    line-height: 1.7;

    margin-top: 17px;
}

.hero-meta {
    display: flex;

    gap: 24px;

    margin-top: 22px;

    color: #A8C5B5;

    font-size: 10px;

    font-weight: 650;
}


/* ============================================================
   PAGE HEADER
   ============================================================ */

.page-header {
    margin: 26px 0 20px 0;
}

.page-title {
    color: var(--ink);

    font-size: 28px;

    font-weight: 850;

    letter-spacing: -.5px;
}

.page-subtitle {
    color: var(--muted);

    font-size: 12px;

    margin-top: 5px;
}


/* ============================================================
   KPI
   ============================================================ */

.kpi-card {
    background: var(--surface);

    border: 1px solid var(--border);

    border-radius: 17px;

    padding: 20px 20px 18px 20px;

    min-height: 128px;

    box-shadow:
        0 7px 24px rgba(18, 52, 35, .035);
}

.kpi-label {
    color: #7E8E86;

    font-size: 9px;

    font-weight: 850;

    letter-spacing: .8px;
}

.kpi-value {
    color: var(--ink);

    font-size: 30px;

    font-weight: 850;

    margin-top: 8px;

    letter-spacing: -.6px;
}

.kpi-detail {
    color: var(--soft);

    font-size: 10px;

    margin-top: 4px;
}


/* ============================================================
   SCORE CARD
   ============================================================ */

.score-card {
    background: white;

    border: 1px solid var(--border);

    border-radius: 20px;

    padding: 23px;

    min-height: 245px;
}

.score-label {
    color: var(--muted);

    font-size: 10px;

    font-weight: 800;

    letter-spacing: .8px;
}

.score-value {
    color: var(--green-800);

    font-size: 50px;

    line-height: 1;

    font-weight: 900;

    margin-top: 12px;
}

.score-caption {
    color: var(--muted);

    font-size: 11px;

    margin-top: 7px;
}

.score-bar {
    width: 100%;

    height: 8px;

    background: #E9EFEB;

    border-radius: 20px;

    overflow: hidden;

    margin-top: 22px;
}

.score-fill {
    height: 100%;

    background:
        linear-gradient(
            90deg,
            var(--green-700),
            var(--green-400)
        );

    border-radius: 20px;
}


/* ============================================================
   SECTION
   ============================================================ */

.section {
    margin: 31px 0 14px 0;
}

.section-title {
    color: var(--ink);

    font-size: 19px;

    font-weight: 850;
}

.section-description {
    color: var(--muted);

    font-size: 11px;

    margin-top: 4px;
}


/* ============================================================
   CARDS
   ============================================================ */

.surface {
    background: white;

    border: 1px solid var(--border);

    border-radius: 18px;

    padding: 21px;

    box-shadow:
        0 7px 25px rgba(18, 52, 35, .035);
}


/* ============================================================
   AI HEADER
   ============================================================ */

.ai-head {
    display: flex;

    align-items: center;

    gap: 11px;

    margin-bottom: 10px;
}

.ai-symbol {
    width: 37px;
    height: 37px;

    border-radius: 11px;

    background: var(--green-100);

    display: flex;

    align-items: center;

    justify-content: center;

    font-size: 18px;
}

.ai-title {
    color: var(--ink);

    font-size: 15px;

    font-weight: 850;
}

.ai-subtitle {
    color: var(--muted);

    font-size: 9px;

    margin-top: 2px;
}


/* ============================================================
   FINDING
   ============================================================ */

.finding-row {
    border-top: 1px solid #EDF1EE;

    padding: 16px 0;
}

.finding-top {
    display: flex;

    align-items: center;

    justify-content: space-between;
}

.finding-name {
    color: var(--ink);

    font-size: 13px;

    font-weight: 800;
}

.finding-body {
    color: #687A71;

    font-size: 11px;

    line-height: 1.65;

    margin-top: 7px;
}

.confidence {
    color: var(--green-700);

    font-size: 9px;

    font-weight: 850;

    background: var(--green-100);

    border-radius: 20px;

    padding: 5px 8px;
}


/* ============================================================
   BADGES
   ============================================================ */

.badge-high {
    display: inline-block;

    background: var(--danger-bg);

    border: 1px solid #F3D0CC;

    color: var(--danger);

    border-radius: 20px;

    padding: 5px 8px;

    font-size: 8px;

    font-weight: 850;

    letter-spacing: .4px;
}

.badge-medium {
    display: inline-block;

    background: var(--warning-bg);

    border: 1px solid #F2DEBB;

    color: var(--warning);

    border-radius: 20px;

    padding: 5px 8px;

    font-size: 8px;

    font-weight: 850;

    letter-spacing: .4px;
}

.badge-low {
    display: inline-block;

    background: var(--success-bg);

    border: 1px solid #CBEADB;

    color: var(--success);

    border-radius: 20px;

    padding: 5px 8px;

    font-size: 8px;

    font-weight: 850;

    letter-spacing: .4px;
}


/* ============================================================
   COPILOT
   ============================================================ */

.copilot {
    background:
        linear-gradient(
            135deg,
            #EAF8F0,
            #F9FCFA
        );

    border: 1px solid #D5EBDD;

    border-radius: 20px;

    padding: 23px;

    box-shadow:
        0 9px 28px rgba(24, 91, 57, .045);
}

.copilot-title {
    color: #174C32;

    font-size: 17px;

    font-weight: 850;
}

.copilot-copy {
    color: #667B70;

    font-size: 11px;

    line-height: 1.65;

    margin-top: 6px;
}


/* ============================================================
   ASSET
   ============================================================ */

.asset-header {
    background:
        linear-gradient(
            135deg,
            #083A27,
            #0E6B45
        );

    color: white;

    border-radius: 21px;

    padding: 26px;

    margin-bottom: 18px;

    box-shadow:
        0 17px 45px rgba(8, 73, 46, .14);
}

.asset-id {
    font-size: 25px;

    font-weight: 900;
}

.asset-fault {
    color: #B9D6C6;

    font-size: 12px;

    margin-top: 4px;
}


/* ============================================================
   REPORT
   ============================================================ */

.report-card {
    background: white;

    border: 1px solid var(--border);

    border-radius: 18px;

    padding: 22px;

    min-height: 165px;

    box-shadow:
        0 7px 25px rgba(18, 52, 35, .035);
}

.report-icon {
    width: 39px;
    height: 39px;

    border-radius: 11px;

    background: var(--green-100);

    display: flex;

    align-items: center;

    justify-content: center;

    font-size: 17px;

    margin-bottom: 13px;
}

.report-name {
    color: var(--ink);

    font-size: 14px;

    font-weight: 850;
}

.report-copy {
    color: var(--muted);

    font-size: 10px;

    line-height: 1.6;

    margin-top: 6px;
}


/* ============================================================
   STREAMLIT INPUTS
   ============================================================ */

.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] > div {
    border-radius: 10px !important;
    border-color: var(--border) !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #9AD4B3 !important;
    box-shadow: 0 0 0 1px #9AD4B3 !important;
}


/* ============================================================
   EXPANDER
   ============================================================ */

.streamlit-expanderHeader {
    border-radius: 12px !important;
    font-weight: 750 !important;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    text-align: center;

    color: #95A29B;

    font-size: 9px;

    padding-top: 22px;

    letter-spacing: .2px;
}

</style>
""",
    unsafe_allow_html=True,
)


# =============================================================================
# DEMO LLM
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

    if confidence >= 0.85:
        return "High"

    return "Medium"


def badge_html(level):

    if level == "High":
        return '<span class="badge-high">HIGH PRIORITY</span>'

    if level == "Medium":
        return '<span class="badge-medium">MEDIUM PRIORITY</span>'

    return '<span class="badge-low">HEALTHY</span>'


# =============================================================================
# INITIALIZE
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

high_risk_assets = [
    d for d in active_findings
    if risk_level(d) == "High"
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
    ) / total_assets
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
<div class="brand-shell">

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

    <div class="live-pill">
        ● LIVE INTELLIGENCE
    </div>

</div>
""",
    unsafe_allow_html=True,
)


# =============================================================================
# NAVIGATION
# =============================================================================

nav_cols = st.columns(
    [1, 1.25, 1, 1, 1]
)

nav_items = [
    ("Overview", "⌂  Overview"),
    ("AI Intelligence", "✦  AI Intelligence"),
    ("Asset 360", "◉  Asset 360"),
    ("Operations", "⚙  Operations"),
    ("Reports", "▣  Reports"),
]

for col, (page, label) in zip(
    nav_cols,
    nav_items
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
        f"""
<div class="hero">

    <div class="hero-eyebrow">
        AI-POWERED SUSTAINABILITY INTELLIGENCE
    </div>

    <div class="hero-title">
        Turn sustainability data<br>
        into <span>intelligent action.</span>
    </div>

    <div class="hero-copy">
        Green Solutions continuously analyzes asset performance,
        detects operational anomalies, explains the evidence,
        and recommends the next best action for your teams.
    </div>

    <div class="hero-meta">
        <span>✦ AI Diagnostics</span>
        <span>✦ Evidence-based intelligence</span>
        <span>✦ Human review</span>
        <span>✦ Operational actions</span>
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
        Portfolio health, AI findings and operational priorities.
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

    # KPI ROW
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
            "Detected anomalies",
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

    for col, label, value, detail in kpis:

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

    <div class="kpi-detail">
        {detail}
    </div>

</div>
""",
                unsafe_allow_html=True,
            )

    # HEALTH + PRIORITIES
    st.markdown(
        """
<div class="section">

    <div class="section-title">
        Portfolio Intelligence
    </div>

    <div class="section-description">
        A high-level view of the current asset portfolio.
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(
        [1, 1.8]
    )

    with c1:

        st.markdown(
            f"""
<div class="score-card">

    <div class="score-label">
        PORTFOLIO HEALTH SCORE
    </div>

    <div class="score-value">
        {health_score:.0f}%
    </div>

    <div class="score-caption">
        {len(healthy_assets)} of {total_assets}
        assets currently operating normally.
    </div>

    <div class="score-bar">

        <div
            class="score-fill"
            style="width:{health_score:.0f}%"
        ></div>

    </div>

</div>
""",
            unsafe_allow_html=True,
        )

    with c2:

        st.markdown(
            """
<div class="surface">

    <div class="ai-head">

        <div class="ai-symbol">
            ✦
        </div>

        <div>

            <div class="ai-title">
                Latest AI Findings
            </div>

            <div class="ai-subtitle">
                PRIORITIZED BY OPERATIONAL IMPACT
            </div>

        </div>

    </div>
""",
            unsafe_allow_html=True,
        )

        for d in active_findings:

            level = risk_level(d)

            st.markdown(
                f"""
<div class="finding-row">

    <div class="finding-top">

        <div class="finding-name">
            {d.get("asset_id")}
            ·
            {fault_label(d.get("fault_hypothesis"))}
        </div>

        {badge_html(level)}

    </div>

    <div class="finding-body">

        {d.get("evidence", "")}

        <br><br>

        <b>Next action:</b>
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

    # AI COPILOT
    st.markdown(
        """
<div class="section">

    <div class="section-title">
        Green Solutions AI
    </div>

    <div class="section-description">
        Your intelligent portfolio copilot.
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

    left, right = st.columns(
        [1.6, 1]
    )

    with left:

        st.markdown(
            """
<div class="copilot">

    <div class="copilot-title">
        ✦ What would you like to know?
    </div>

    <div class="copilot-copy">
        Ask about asset health, AI findings, risks,
        evidence or recommended operational actions.
    </div>

</div>
""",
            unsafe_allow_html=True,
        )

        question = st.text_input(
            "Portfolio question",
            placeholder="Example: Which assets need immediate attention?",
            label_visibility="collapsed",
        )

        if question:

            q = question.lower()

            if "attention" in q:

                response = (
                    f"{len(active_findings)} assets require "
                    f"attention: "
                    + ", ".join(
                        d.get("asset_id")
                        for d in active_findings
                    )
                )

            elif "action" in q:

                response = "\n".join(
                    f"• {d.get('asset_id')}: "
                    f"{d.get('recommended_action')}"
                    for d in active_findings
                )

            else:

                response = (
                    "Green Solutions currently understands "
                    "portfolio health, asset findings, "
                    "confidence, evidence and recommended actions."
                )

            st.info(response)

    with right:

        st.markdown(
            f"""
<div class="surface">

    <div class="ai-title">
        Operational Snapshot
    </div>

    <br>

    🔴 <b>{len(high_risk_assets)}</b>
    high-priority assets

    <br><br>

    🟠 <b>{len(active_findings)}</b>
    active findings

    <br><br>

    🟢 <b>{len(healthy_assets)}</b>
    healthy assets

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
        Evidence-backed intelligence generated from portfolio performance data.
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="copilot">

    <div class="copilot-title">
        ✦ Green Solutions AI Intelligence Engine
    </div>

    <div class="copilot-copy">
        Review AI diagnoses, confidence levels, supporting evidence
        and recommended actions.
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

    st.write("")

    for d in diagnoses:

        level = risk_level(d)

        icon = (
            "🔴"
            if level == "High"
            else "🟠"
            if level == "Medium"
            else "🟢"
        )

        with st.expander(
            f"{icon}  {d.get('asset_id')}  ·  "
            f"{fault_label(d.get('fault_hypothesis'))}"
        ):

            a, b, c = st.columns(3)

            with a:

                st.metric(
                    "AI Confidence",
                    f"{float(d.get('confidence', 0)):.0%}"
                )

            with b:

                st.metric(
                    "Priority",
                    level
                )

            with c:

                st.metric(
                    "Status",
                    "Attention Required"
                    if d.get("fault_hypothesis") != "none"
                    else "Healthy"
                )

            st.markdown("#### Evidence")

            st.write(
                d.get(
                    "evidence",
                    ""
                )
            )

            st.markdown("#### Recommended Action")

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
        Deep intelligence for every monitored asset.
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
        "Select an asset",
        asset_options,
    )

    selected = next(
        (
            d for d in diagnoses
            if d.get("asset_id") == selected_asset
        ),
        None,
    )

    if selected:

        level = risk_level(selected)

        st.markdown(
            f"""
<div class="asset-header">

    <div class="asset-id">
        {selected.get("asset_id")}
    </div>

    <div class="asset-fault">
        {fault_label(selected.get("fault_hypothesis"))}
        ·
        {level} Priority
    </div>

</div>
""",
            unsafe_allow_html=True,
        )

        a, b, c = st.columns(3)

        with a:

            st.metric(
                "AI Confidence",
                f"{float(selected.get('confidence', 0)):.0%}"
            )

        with b:

            st.metric(
                "Risk Level",
                level
            )

        with c:

            st.metric(
                "Operational Status",
                "Attention Required"
                if selected.get("fault_hypothesis") != "none"
                else "Healthy"
            )

        st.markdown(
            """
<div class="section">

    <div class="section-title">
        Asset Intelligence
    </div>

</div>
""",
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns(2)

        with c1:

            st.markdown(
                f"""
<div class="surface">

    <div class="ai-title">
        What is happening?
    </div>

    <br>

    <div class="finding-body">
        {selected.get("evidence", "")}
    </div>

</div>
""",
                unsafe_allow_html=True,
            )

        with c2:

            st.markdown(
                f"""
<div class="surface">

    <div class="ai-title">
        Recommended next action
    </div>

    <br>

    <div class="finding-body">
        {selected.get("recommended_action", "")}
    </div>

</div>
""",
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
        Operations Command Center
    </div>

    <div class="page-subtitle">
        Move from AI insight to operational action.
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

    if not active_findings:

        st.success(
            "No operational actions are currently required."
        )

    for index, d in enumerate(
        active_findings,
        1
    ):

        level = risk_level(d)

        with st.container(border=True):

            c1, c2, c3, c4 = st.columns(
                [.35, 1.1, 2, 3]
            )

            with c1:

                st.markdown(
                    f"**{index:02d}**"
                )

            with c2:

                st.markdown(
                    f"**{d.get('asset_id')}**"
                )

                st.markdown(
                    badge_html(level),
                    unsafe_allow_html=True,
                )

            with c3:

                st.markdown(
                    f"**{fault_label(d.get('fault_hypothesis'))}**"
                )

                st.caption(
                    f"AI confidence "
                    f"{float(d.get('confidence', 0)):.0%}"
                )

            with c4:

                st.write(
                    d.get(
                        "recommended_action",
                        ""
                    )
                )

                st.button(
                    "Review Action",
                    key=f"operation_{index}",
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
        AI-generated documentation for field teams,
        asset owners and compliance stakeholders.
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

    r1, r2, r3 = st.columns(3)

    cards = [
        (
            r1,
            "📋",
            "Field Work Order",
            "Technician-ready operational actions.",
        ),
        (
            r2,
            "◉",
            "Owner Report",
            "Executive-friendly portfolio summary.",
        ),
        (
            r3,
            "✓",
            "Compliance Summary",
            "Formal findings and action record.",
        ),
    ]

    for col, icon, title, description in cards:

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

    <div class="report-copy">
        {description}
    </div>

</div>
""",
                unsafe_allow_html=True,
            )

    st.write("")

    tabs = st.tabs(
        [
            "Field Work Order",
            "Owner Report",
            "Compliance Summary",
        ]
    )

    report_items = [
        (
            tabs[0],
            "work_order_text",
            "green_solutions_work_order.txt",
        ),
        (
            tabs[1],
            "owner_report_text",
            "green_solutions_owner_report.txt",
        ),
        (
            tabs[2],
            "compliance_summary_text",
            "green_solutions_compliance.txt",
        ),
    ]

    for tab, key, filename in report_items:

        with tab:

            text = result.get(
                key,
                "(No report generated)"
            )

            st.text_area(
                "Generated report",
                text,
                height=360,
            )

            st.download_button(
                "Download Report",
                data=text,
                file_name=filename,
                mime="text/plain",
                use_container_width=True,
            )

    # FEEDBACK
    st.markdown(
        """
<div class="section">

    <div class="section-title">
        Product Feedback
    </div>

    <div class="section-description">
        Help validate Green Solutions with real users.
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

    with st.form("feedback_form"):

        c1, c2 = st.columns(2)

        with c1:

            trust = st.slider(
                "Trust in AI findings",
                1,
                5,
                3,
            )

        with c2:

            clarity = st.slider(
                "Clarity of recommendations",
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
            "What would make this product more useful?"
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
                "Thank you — your feedback has been recorded."
            )


# =============================================================================
# FOOTER
# =============================================================================

st.divider()

mode = (
    "Demo Intelligence"
    if demo_mode_active()
    else "Live AI Intelligence"
)

st.markdown(
    f"""
<div class="footer">

    🌱 Green Solutions
    &nbsp; • &nbsp;
    Intelligent Sustainability Platform
    &nbsp; • &nbsp;
    {mode}
    &nbsp; • &nbsp;
    {datetime.now().year}

</div>
""",
    unsafe_allow_html=True,
)
