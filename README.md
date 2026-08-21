# Green Solutions — Solar Reporting Copilot MVP

A validation-stage Streamlit application for solar O&M teams. It generates synthetic solar asset performance data, runs a LangGraph diagnostic workflow, and drafts three audience-specific outputs:

- Field work order
- Asset-owner report
- Compliance summary

## Streamlit Community Cloud deployment

1. Push this entire folder to a GitHub repository.
2. In Streamlit Community Cloud, create an app from that repository.
3. Set the main file to `app.py`.
4. Deploy.

The app intentionally works in **Demo Mode without an API key**, so the first validation can be run at zero model/API cost.

### Optional Gemini mode

If you later want live Gemini responses, add `GOOGLE_API_KEY` in the Streamlit app's Secrets settings. Do not commit API keys to GitHub.

Example secret:

```toml
GOOGLE_API_KEY = "your-key"
```

### Local run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Project structure

```text
app.py                  # Streamlit entry point
agents.py               # Data normalization, diagnosis, report drafting
state.py                # LangGraph state schema
graph.py                # LangGraph orchestration
synthetic_data.py       # Synthetic SCADA/DAS data generator
feedback_store.py       # MVP local feedback storage
mcp_server.py           # Optional MCP interface
requirements.txt        # Streamlit Cloud dependencies
```

## Important MVP limitation

`feedback_log.json` is local/ephemeral storage. Streamlit Community Cloud is not a durable database, so feedback should later move to Google Sheets, Supabase, SQLite/DuckDB with appropriate persistence, or another database before a real pilot.

The current human-review node is also an MVP stub: it logs low-confidence findings and continues to report drafting. A production version should use a real approval/interrupt workflow.

## Validation goal

Use the app to validate whether solar O&M managers, asset owners, and technicians find the diagnosis and report-generation workflow useful before introducing paid AWS/Azure infrastructure.
