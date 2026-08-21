"""
Minimal feedback storage — appends to a local JSON file.
No database needed for a handful of pilot reviewers.
"""

import json
import os
from datetime import datetime

FEEDBACK_FILE = "feedback_log.json"


def save_feedback(entry: dict) -> None:
    entry["timestamp"] = datetime.now().isoformat()
    records = load_feedback()
    records.append(entry)
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(records, f, indent=2, default=str)


def load_feedback() -> list:
    if not os.path.exists(FEEDBACK_FILE):
        return []
    with open(FEEDBACK_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []
