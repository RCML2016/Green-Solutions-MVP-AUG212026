"""
Agent node implementations.

Each function takes the shared PipelineState, does its work, and returns
a partial state update. Kept deliberately simple / readable over clever —
this is a validation-phase skeleton, not production code.
"""

import os
import pandas as pd
from state import PipelineState, AssetDiagnosis


# ---------------------------------------------------------------------------
# LLM setup (swap providers freely — this is the only place that changes)
# ---------------------------------------------------------------------------
def get_llm():
    """
    Returns a callable LLM. Defaults to Gemini free tier via
    GOOGLE_API_KEY. Falls back to a local Ollama model if
    OLLAMA_MODEL is set, so this can run fully offline / free.
    """
    if os.getenv("OLLAMA_MODEL"):
        from langchain_community.chat_models import ChatOllama

        return ChatOllama(model=os.environ["OLLAMA_MODEL"], temperature=0.2)

    from langchain_google_genai import ChatGoogleGenerativeAI

    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.2,
        google_api_key=os.environ.get("GOOGLE_API_KEY"),
    )


# ---------------------------------------------------------------------------
# Agent 1 — Data Normalizer
# ---------------------------------------------------------------------------
def data_normalizer_node(state: PipelineState) -> dict:
    """Reads raw CSV/time-series data and produces a normalized dataframe
    plus a compact plain-text summary the next agent can reason over."""
    df = pd.read_csv(state["raw_data_path"], parse_dates=["timestamp"])

    summary_lines = []
    for asset_id, group in df.groupby("asset_id"):
        capacity = group["capacity_kw"].iloc[0]
        avg_gen = group["generation_kw"].mean()
        null_pct = group["generation_kw"].isna().mean() * 100
        fault_days = group.loc[group["injected_fault"] != "none", "timestamp"].nunique()
        summary_lines.append(
            f"- {asset_id}: capacity={capacity}kW, avg_output={avg_gen:.1f}kW, "
            f"missing_readings={null_pct:.1f}%, flagged_intervals={fault_days}"
        )

    portfolio_summary = "\n".join(summary_lines)

    return {
        "normalized_df": df,
        "portfolio_summary": portfolio_summary,
        "next_step": "diagnose",
    }


# ---------------------------------------------------------------------------
# Agent 2 — Diagnostic Reasoner
# ---------------------------------------------------------------------------
DIAGNOSTIC_PROMPT = """You are a solar asset diagnostics engineer.

Given this per-asset performance summary, identify the most likely fault
type for each asset that shows abnormal behavior (or "none" if it looks
healthy). Possible fault types: string_underperformance, inverter_clipping,
soiling, comm_dropout, none.

For each asset, respond in this exact format, one block per asset:

ASSET: <asset_id>
FAULT: <fault_type>
CONFIDENCE: <0.0-1.0>
EVIDENCE: <one sentence, grounded in the numbers given>
ACTION: <one concrete next step>

Portfolio summary:
{summary}
"""


def diagnostic_reasoner_node(state: PipelineState) -> dict:
    """Calls the LLM to produce a grounded root-cause hypothesis per asset."""
    llm = get_llm()
    prompt = DIAGNOSTIC_PROMPT.format(summary=state["portfolio_summary"])
    response = llm.invoke(prompt)
    text = response.content if hasattr(response, "content") else str(response)

    diagnoses: list[AssetDiagnosis] = []
    blocks = [b.strip() for b in text.split("ASSET:") if b.strip()]
    for block in blocks:
        lines = ("ASSET:" + block).splitlines()
        fields = {}
        for line in lines:
            if ":" in line:
                key, _, val = line.partition(":")
                fields[key.strip().upper()] = val.strip()
        if "ASSET" not in fields:
            continue
        try:
            confidence = float(fields.get("CONFIDENCE", "0.5"))
        except ValueError:
            confidence = 0.5
        diagnoses.append(
            AssetDiagnosis(
                asset_id=fields.get("ASSET", "unknown"),
                fault_hypothesis=fields.get("FAULT", "unknown"),
                confidence=confidence,
                evidence=fields.get("EVIDENCE", ""),
                recommended_action=fields.get("ACTION", ""),
            )
        )

    # Low-confidence findings get routed to human review instead of
    # auto-publishing straight into an owner-facing report.
    low_confidence = [d for d in diagnoses if d["confidence"] < 0.6]
    needs_review = len(low_confidence) > 0

    return {
        "diagnoses": diagnoses,
        "needs_human_review": needs_review,
        "review_reason": (
            f"{len(low_confidence)} diagnosis(es) below 0.6 confidence"
            if needs_review
            else None
        ),
        "next_step": "human_review" if needs_review else "draft_reports",
    }


# ---------------------------------------------------------------------------
# Agent 3 — Report Drafter
# ---------------------------------------------------------------------------
REPORT_PROMPT = """You are drafting three different documents from the same
underlying diagnostic findings for a solar asset portfolio. Use the
diagnoses below. Be concrete and concise — no filler.

Diagnoses:
{diagnoses}

Produce exactly three sections, each starting with the header shown:

=== WORK_ORDER ===
(technical, for field technicians — asset IDs, fault type, what to check)

=== OWNER_REPORT ===
(plain English, for the asset owner — what happened, expected impact, what's being done)

=== COMPLIANCE_SUMMARY ===
(formal tone, for regulatory/investor records — dated findings, actions taken, status)
"""


def report_drafter_node(state: PipelineState) -> dict:
    """Turns diagnoses into three audience-specific documents in one pass."""
    llm = get_llm()
    diag_text = "\n".join(
        f"- {d['asset_id']}: {d['fault_hypothesis']} "
        f"(confidence {d['confidence']:.2f}) — {d['evidence']} "
        f"Action: {d['recommended_action']}"
        for d in state["diagnoses"]
    )
    prompt = REPORT_PROMPT.format(diagnoses=diag_text)
    response = llm.invoke(prompt)
    text = response.content if hasattr(response, "content") else str(response)

    sections = {"WORK_ORDER": "", "OWNER_REPORT": "", "COMPLIANCE_SUMMARY": ""}
    current = None
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("=== ") and stripped.endswith(" ==="):
            current = stripped.strip("= ").strip()
            continue
        if current in sections:
            sections[current] += line + "\n"

    return {
        "work_order_text": sections["WORK_ORDER"].strip(),
        "owner_report_text": sections["OWNER_REPORT"].strip(),
        "compliance_summary_text": sections["COMPLIANCE_SUMMARY"].strip(),
        "next_step": "done",
    }


# ---------------------------------------------------------------------------
# Human review stub — in the MVP this just logs; a real version would
# pause the graph and wait for approval (LangGraph supports interrupts).
# ---------------------------------------------------------------------------
def human_review_node(state: PipelineState) -> dict:
    print(f"[HUMAN REVIEW NEEDED] {state.get('review_reason')}")
    print("Low-confidence diagnoses:")
    for d in state["diagnoses"]:
        if d["confidence"] < 0.6:
            print(f"  - {d['asset_id']}: {d['fault_hypothesis']} ({d['confidence']:.2f})")
    # For the MVP we proceed anyway after logging; swap for an
    # interrupt() call once you want a real approval gate.
    return {"next_step": "draft_reports"}
