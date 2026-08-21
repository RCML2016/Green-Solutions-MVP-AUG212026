"""
Synthetic SCADA / DAS data generator.

Simulates a small portfolio of solar assets (inverters/strings) with
normal generation curves plus injected fault patterns, so the pipeline
can be built and tested before any real client data is available.

Fault types modeled:
  - string_underperformance: one string reads consistently low
  - inverter_clipping: output flattens at a ceiling during peak sun
  - soiling: gradual, slow decline in output over days
  - comm_dropout: missing/null readings for a stretch of time
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


def _clear_sky_curve(hour: float, capacity_kw: float) -> float:
    """Simple bell-curve approximation of solar generation across a day."""
    if hour < 6 or hour > 19:
        return 0.0
    peak_hour = 12.5
    width = 3.2
    value = capacity_kw * np.exp(-((hour - peak_hour) ** 2) / (2 * width ** 2))
    return max(value, 0.0)


def generate_asset_timeseries(
    asset_id: str,
    capacity_kw: float,
    days: int = 14,
    interval_minutes: int = 15,
    fault: str | None = None,
    fault_start_day: int = 7,
    seed: int | None = None,
) -> pd.DataFrame:
    """Generate one asset's time series, optionally with a fault injected
    starting at `fault_start_day`."""
    rng = np.random.default_rng(seed)
    start = datetime(2026, 6, 1)
    steps = int(days * 24 * 60 / interval_minutes)
    rows = []

    for i in range(steps):
        ts = start + timedelta(minutes=i * interval_minutes)
        hour = ts.hour + ts.minute / 60
        day_index = i // (24 * 60 // interval_minutes)

        base = _clear_sky_curve(hour, capacity_kw)
        noise = rng.normal(0, capacity_kw * 0.02)
        value = max(base + noise, 0.0)

        fault_active = fault is not None and day_index >= fault_start_day
        comm_ok = True

        if fault_active:
            if fault == "string_underperformance":
                value *= 0.72
            elif fault == "inverter_clipping":
                ceiling = capacity_kw * 0.85
                value = min(value, ceiling)
            elif fault == "soiling":
                days_into_fault = day_index - fault_start_day
                decay = max(1 - 0.015 * days_into_fault, 0.6)
                value *= decay
            elif fault == "comm_dropout":
                if 10 <= hour <= 14 and rng.random() < 0.4:
                    value = np.nan
                    comm_ok = False

        rows.append(
            {
                "asset_id": asset_id,
                "timestamp": ts,
                "capacity_kw": capacity_kw,
                "generation_kw": round(value, 3) if not np.isnan(value) else np.nan,
                "comm_ok": comm_ok,
                "injected_fault": fault if fault_active else "none",
            }
        )

    return pd.DataFrame(rows)


def generate_portfolio(seed: int = 42) -> pd.DataFrame:
    """Generate a small demo portfolio: five assets, four with a distinct
    injected fault and one healthy control asset."""
    configs = [
        ("INV-01", 250, "string_underperformance"),
        ("INV-02", 250, "inverter_clipping"),
        ("INV-03", 500, "soiling"),
        ("INV-04", 250, "comm_dropout"),
        ("INV-05", 250, None),  # healthy control
    ]

    frames = [
        generate_asset_timeseries(asset_id, cap, fault=fault, seed=seed + idx)
        for idx, (asset_id, cap, fault) in enumerate(configs)
    ]
    return pd.concat(frames, ignore_index=True)


if __name__ == "__main__":
    df = generate_portfolio()
    df.to_csv("sample_portfolio.csv", index=False)
    print(f"Generated {len(df)} rows across {df['asset_id'].nunique()} assets")
    print(df.groupby(["asset_id", "injected_fault"]).size())
