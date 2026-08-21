"""
FastMCP server exposing the pipeline as MCP tools.

This is what turns the project from "a script" into "a thing other
tools/agents can call" — the actual differentiator versus the
dashboard-first competitors, since none of them expose an MCP surface.

Run with:  python mcp_server.py
Then any MCP-compatible client (Claude Desktop, another LangGraph agent,
etc.) can call these tools directly.
"""

from fastmcp import FastMCP
from graph import build_graph

mcp = FastMCP("solar-reporting-copilot")
_app = build_graph()


@mcp.tool()
def run_portfolio_diagnostics(csv_path: str) -> dict:
    """Run the full pipeline on a portfolio CSV file and return the
    diagnoses plus all three drafted report sections.

    Args:
        csv_path: path to a CSV with columns asset_id, timestamp,
            capacity_kw, generation_kw, comm_ok, injected_fault
            (matching the schema produced by synthetic_data.py)
    """
    result = _app.invoke({"raw_data_path": csv_path})
    return {
        "diagnoses": result.get("diagnoses", []),
        "needs_human_review": result.get("needs_human_review", False),
        "work_order": result.get("work_order_text", ""),
        "owner_report": result.get("owner_report_text", ""),
        "compliance_summary": result.get("compliance_summary_text", ""),
    }


@mcp.tool()
def get_asset_summary(csv_path: str, asset_id: str) -> str:
    """Return a quick plain-text performance summary for a single asset,
    without running the full diagnostic/report pipeline."""
    import pandas as pd

    df = pd.read_csv(csv_path, parse_dates=["timestamp"])
    asset_df = df[df["asset_id"] == asset_id]
    if asset_df.empty:
        return f"No data found for asset_id={asset_id}"

    avg_gen = asset_df["generation_kw"].mean()
    capacity = asset_df["capacity_kw"].iloc[0]
    null_pct = asset_df["generation_kw"].isna().mean() * 100
    return (
        f"{asset_id}: capacity={capacity}kW, avg_output={avg_gen:.1f}kW "
        f"({avg_gen / capacity * 100:.0f}% of capacity), "
        f"missing_readings={null_pct:.1f}%"
    )


if __name__ == "__main__":
    mcp.run()
