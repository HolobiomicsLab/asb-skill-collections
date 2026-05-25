"""
Generate HuggingFace Space skeleton (README.md + app.py) for a per-collection leaderboard.

Usage:
    python scripts/generate_hf_space_config.py \\
        --collection collections/metabolomics/v1/collection.yaml \\
        --leaderboard-url https://raw.githubusercontent.com/.../leaderboard.jsonld \\
        --output templates/hf-space/
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml


def generate_space_readme(collection: dict, leaderboard_url: str) -> str:
    """
    Generate HF Space README.md with YAML frontmatter.

    Parameters
    ----------
    collection : dict
        Parsed collection.yaml with title, slug, version, domain.
    leaderboard_url : str
        GitHub raw URL of leaderboard.jsonld for this collection.

    Returns
    -------
    str
        Full README.md for the HF Space.
    """
    title = collection["title"]
    slug = collection["slug"]
    version = collection["version"]
    space_title = f"ASB {title} v{version} Leaderboard"

    frontmatter = f"""---
title: {space_title}
emoji: \U0001f52c
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: "4.42.0"
app_file: app.py
pinned: false
license: apache-2.0
tags:
  - leaderboard
  - agentic-ai
  - scientific-agents
  - asb
  - {collection.get('domain', slug).lower()}
variables:
  LEADERBOARD_URL: "{leaderboard_url}"
---"""

    body = f"""
# {space_title}

Live leaderboard for the [ASB {title} v{version}](https://github.com/HolobiomicsLab/asb-skill-collections/tree/main/collections/{slug}/v{version}) collection.

Tracks agent (`result_type: agent`), RAG-system (`result_type: rag_system`), and hybrid (`result_type: hybrid`) results.

## Submit a result

Click **Submit a result** in the app to open a pre-filled GitHub Issue.
A maintainer will review and merge your PR to `leaderboard.jsonld`.

## Data source

Leaderboard data is fetched live from:
`{leaderboard_url}`
"""

    return frontmatter + "\n" + body


def generate_app_py(collection: dict, leaderboard_url: str) -> str:
    """
    Generate the Gradio app.py for a per-collection leaderboard Space.

    Parameters
    ----------
    collection : dict
        Parsed collection.yaml with title, slug, version.
    leaderboard_url : str
        GitHub raw URL of leaderboard.jsonld.

    Returns
    -------
    str
        Contents of app.py.
    """
    title = collection["title"]
    slug = collection["slug"]
    version = collection["version"]

    issue_url = (
        f"https://github.com/HolobiomicsLab/asb-skill-collections/issues/new"
        f"?template=submit-agent-result.md"
        f"&labels=leaderboard-submission,{slug}"
        f"&title=Result+submission:+ASB+{slug}+v{version}"
    )

    # Build the app.py source by direct string assembly so that Python
    # expressions (f-strings, dict comprehensions) inside the generated
    # code are not confused with format() placeholders.
    header = (
        f'"""\nGradio leaderboard for ASB {title} v{version}.\n'
        f"Reads leaderboard.jsonld live from GitHub raw URL.\n"
        f'"""\n'
        f"import os\n"
        f"import json\n"
        f"\n"
        f"import gradio as gr\n"
        f"import pandas as pd\n"
        f"import requests\n"
        f"\n"
        f"LEADERBOARD_URL = os.environ.get(\n"
        f'    "LEADERBOARD_URL",\n'
        f'    "{leaderboard_url}",\n'
        f")\n"
        f"\n"
        f'GITHUB_ISSUE_URL = "{issue_url}"\n'
        f"\n"
    )

    # These sections contain Python-level braces — built as plain strings.
    body_static = (
        'RESULT_TYPES = ["all", "agent", "rag_system", "hybrid"]\n'
        "\n"
        "COLUMNS = [\n"
        '    "system_name",\n'
        '    "result_type",\n'
        '    "overall_score",\n'
        '    "task_score",\n'
        '    "claim_score",\n'
        '    "workflow_tier",\n'
        '    "submitted_by",\n'
        '    "date",\n'
        "]\n"
        "\n"
        "\n"
        "def fetch_leaderboard(leaderboard_url: str = LEADERBOARD_URL) -> list[dict]:\n"
        '    """Fetch leaderboard.jsonld from GitHub raw URL."""\n'
        "    try:\n"
        "        resp = requests.get(leaderboard_url, timeout=10)\n"
        "        resp.raise_for_status()\n"
        "        data = resp.json()\n"
        "        if isinstance(data, list):\n"
        "            return data\n"
        "        if isinstance(data, dict):\n"
        '            return data.get("@graph", data.get("results", [data]))\n'
        "        return []\n"
        "    except Exception as exc:\n"
        "        print(f'WARNING: could not fetch leaderboard: {exc}')\n"
        "        return []\n"
        "\n"
        "\n"
        'def load_table(result_type_filter: str = "all") -> pd.DataFrame:\n'
        '    """Load leaderboard into a DataFrame, optionally filtered by result_type."""\n'
        "    entries = fetch_leaderboard()\n"
        "    if not entries:\n"
        "        return pd.DataFrame(columns=COLUMNS)\n"
        "    rows = []\n"
        "    for entry in entries:\n"
        '        if result_type_filter != "all":\n'
        '            if entry.get("result_type") != result_type_filter:\n'
        "                continue\n"
        '        row = {col: entry.get(col, "") for col in COLUMNS}\n'
        "        rows.append(row)\n"
        "    df = pd.DataFrame(rows, columns=COLUMNS)\n"
        '    if "overall_score" in df.columns and not df.empty:\n'
        '        df = df.sort_values("overall_score", ascending=False)'
        ".reset_index(drop=True)\n"
        "    return df\n"
        "\n"
        "\n"
        "def refresh_table(result_type_filter: str) -> pd.DataFrame:\n"
        "    return load_table(result_type_filter)\n"
        "\n"
        "\n"
    )

    blocks_header = (
        f'with gr.Blocks(title="ASB {title} v{version} Leaderboard") as demo:\n'
        f'    gr.Markdown("# ASB {title} v{version} Leaderboard")\n'
        f"    gr.Markdown(\n"
        f'        "Results for [asb-skill-collections/{slug}/v{version}]"\n'
        f"        \"(https://github.com/HolobiomicsLab/asb-skill-collections"
        f"/tree/main/collections/{slug}/v{version}). \"\n"
        f'        "Sorted by `overall_score` descending."\n'
        f"    )\n"
    )

    blocks_body = (
        "\n"
        "    with gr.Row():\n"
        "        result_type_dd = gr.Dropdown(\n"
        "            choices=RESULT_TYPES,\n"
        '            value="all",\n'
        '            label="Filter by result_type",\n'
        "        )\n"
        '        refresh_btn = gr.Button("Refresh", variant="secondary")\n'
        "\n"
        "    table = gr.DataFrame(\n"
        '        value=load_table("all"),\n'
        "        interactive=False,\n"
        "        wrap=True,\n"
        "    )\n"
        "\n"
        "    with gr.Row():\n"
        '        submit_btn = gr.Button("Submit a result", variant="primary")\n'
        '        submit_info = gr.Markdown("")\n'
        "\n"
        "    result_type_dd.change(\n"
        "        fn=refresh_table,\n"
        "        inputs=[result_type_dd],\n"
        "        outputs=[table],\n"
        "    )\n"
        "    refresh_btn.click(\n"
        "        fn=refresh_table,\n"
        "        inputs=[result_type_dd],\n"
        "        outputs=[table],\n"
        "    )\n"
        "\n"
        "    def on_submit():\n"
        "        return gr.Markdown(\n"
        '            "Open a GitHub Issue to submit your result: "\n'
        '            + f"[Click here](" + GITHUB_ISSUE_URL + ")"\n'
        "        )\n"
        "\n"
        "    submit_btn.click(fn=on_submit, inputs=[], outputs=[submit_info])\n"
        "\n"
        "\n"
        'if __name__ == "__main__":\n'
        "    demo.launch()\n"
    )

    return header + body_static + blocks_header + blocks_body


def generate_space_config(collection: dict, leaderboard_url: str) -> dict[str, str]:
    """
    Convenience wrapper returning both Space files as a dict.

    Returns
    -------
    dict with keys "readme" and "app_py".
    """
    return {
        "readme": generate_space_readme(collection=collection, leaderboard_url=leaderboard_url),
        "app_py": generate_app_py(collection=collection, leaderboard_url=leaderboard_url),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--collection", required=True, help="Path to collection.yaml")
    parser.add_argument(
        "--leaderboard-url",
        required=True,
        help="GitHub raw URL of leaderboard.jsonld",
    )
    parser.add_argument(
        "--output",
        default="templates/hf-space/",
        help="Output directory (default: templates/hf-space/)",
    )
    args = parser.parse_args(argv)

    collection_path = Path(args.collection)
    if not collection_path.exists():
        print(f"ERROR: collection.yaml not found: {collection_path}", file=sys.stderr)
        return 1

    sys.path.insert(0, str(Path(__file__).parent))
    import generate_hf_dataset_card as dc  # noqa: local import after path setup

    collection = dc.parse_collection_yaml(collection_path.read_text())
    config = generate_space_config(
        collection=collection,
        leaderboard_url=args.leaderboard_url,
    )

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "README.md").write_text(config["readme"])
    (out_dir / "app.py").write_text(config["app_py"])
    print(f"Written Space files to {out_dir}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
