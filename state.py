"""
Shared state schema for the multi-agent pipeline.

LangGraph passes this dict-like object between every node. Each node
reads what it needs and returns a partial update that gets merged in.
"""

from typing import TypedDict, Literal, Optional
import pandas as pd


class AssetDiagnosis(TypedDict):
    asset_id: str
    fault_hypothesis: str
    confidence: float  # 0.0 - 1.0
    evidence: str
    recommended_action: str


class PipelineState(TypedDict, total=False):
    # Input
    raw_data_path: str

    # After Data Normalizer
    normalized_df: Optional[pd.DataFrame]
    portfolio_summary: Optional[str]

    # After Diagnostic Reasoner
    diagnoses: list[AssetDiagnosis]

    # After Report Drafter
    work_order_text: Optional[str]
    owner_report_text: Optional[str]
    compliance_summary_text: Optional[str]

    # Supervisor control
    needs_human_review: bool
    review_reason: Optional[str]
    next_step: Literal[
        "normalize", "diagnose", "draft_reports", "human_review", "done"
    ]
