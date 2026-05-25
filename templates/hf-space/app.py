"""
ASB Collection Leaderboard — Gradio Space app.
Reads leaderboard.jsonld live from LEADERBOARD_URL env var.
"""
import os
import json

import gradio as gr
import pandas as pd
import requests

LEADERBOARD_URL = os.environ.get("LEADERBOARD_URL", "")
GITHUB_ISSUES_URL = os.environ.get(
    "GITHUB_ISSUES_URL",
    "https://github.com/HolobiomicsLab/asb-skill-collections/issues/new"
    "?template=submit-agent-result.md&labels=leaderboard-submission",
)

RESULT_TYPES = ["all", "agent", "rag_system", "hybrid"]

COLUMNS = [
    "system_name",
    "result_type",
    "overall_score",
    "task_score",
    "claim_score",
    "workflow_tier",
    "submitted_by",
    "date",
]


def fetch_leaderboard() -> list[dict]:
    if not LEADERBOARD_URL:
        return []
    try:
        resp = requests.get(LEADERBOARD_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            return data.get("@graph", data.get("results", []))
        return []
    except Exception as exc:
        print(f"WARNING: could not fetch leaderboard: {exc}")
        return []


def load_table(result_type_filter: str = "all") -> pd.DataFrame:
    entries = fetch_leaderboard()
    if not entries:
        return pd.DataFrame(columns=COLUMNS)
    rows = []
    for entry in entries:
        if result_type_filter != "all" and entry.get("result_type") != result_type_filter:
            continue
        rows.append({col: entry.get(col, "") for col in COLUMNS})
    df = pd.DataFrame(rows, columns=COLUMNS)
    if "overall_score" in df.columns and not df.empty:
        df = df.sort_values("overall_score", ascending=False).reset_index(drop=True)
    return df


with gr.Blocks(title="ASB Leaderboard") as demo:
    gr.Markdown("# ASB Collection Leaderboard")

    with gr.Row():
        result_type_dd = gr.Dropdown(
            choices=RESULT_TYPES, value="all", label="Filter by result_type"
        )
        refresh_btn = gr.Button("Refresh", variant="secondary")

    table = gr.DataFrame(value=load_table("all"), interactive=False, wrap=True)

    with gr.Row():
        submit_btn = gr.Button("Submit a result", variant="primary")
        submit_info = gr.Markdown("")

    result_type_dd.change(
        fn=lambda rt: load_table(rt), inputs=[result_type_dd], outputs=[table]
    )
    refresh_btn.click(
        fn=lambda rt: load_table(rt), inputs=[result_type_dd], outputs=[table]
    )

    def on_submit():
        return gr.Markdown(f"[Open GitHub Issue to submit]({GITHUB_ISSUES_URL})")

    submit_btn.click(fn=on_submit, inputs=[], outputs=[submit_info])


if __name__ == "__main__":
    demo.launch()
