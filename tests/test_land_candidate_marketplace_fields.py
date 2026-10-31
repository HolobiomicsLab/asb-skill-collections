"""A landed companion marketplace carries no field strict validation refuses.

``land_candidate`` wrote ``schema_version`` and ``publisher`` into every
companion marketplace it created, and refused to land into one without
``schema_version: "1.0"``. ``claude plugin validate --strict`` rejects both
fields, so every landed companion failed it, and a companion that dropped
them could no longer take a candidate. The writer now emits neither, the
``owner`` block names the publisher, and a marketplace without
``schema_version`` is accepted.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

from scripts import land_candidate

DOMAIN = "proteomics"
COLLECTION_PATH = f"collections/{DOMAIN}/v1"
MARKETPLACE = ".claude-plugin/marketplace.json"


def _plan() -> SimpleNamespace:
    return SimpleNamespace(
        inputs=SimpleNamespace(
            source={"domain": DOMAIN, "cut_id": "0123456789ab"},
            descriptor={"title": "ASB Proteomics", "skills_count": 12, "tools_count": 3},
        ),
        collection_path=COLLECTION_PATH,
    )


def test_a_new_marketplace_has_no_schema_version_or_publisher() -> None:
    marketplace = land_candidate._marketplace(_plan())

    assert "schema_version" not in marketplace
    assert "publisher" not in marketplace
    assert marketplace["owner"] == land_candidate.OWNER
    assert marketplace["name"] == f"asb-skills-{DOMAIN}"
    assert [p["source"] for p in marketplace["plugins"]] == [f"./{COLLECTION_PATH}"]


def _tracked_repo(tmp_path: Path, marketplace: dict) -> Path:
    repo = tmp_path / "repo"
    (repo / ".claude-plugin").mkdir(parents=True)
    (repo / MARKETPLACE).write_text(json.dumps(marketplace), encoding="utf-8")
    for argv in (["init", "-q"], ["add", MARKETPLACE]):
        subprocess.run(["git", "-C", str(repo), *argv], check=True, capture_output=True)
    return repo


def test_a_tracked_marketplace_without_schema_version_is_accepted(tmp_path: Path) -> None:
    existing = {
        "name": f"asb-skills-{DOMAIN}",
        "owner": dict(land_candidate.OWNER),
        "plugins": [{"name": f"{DOMAIN}-v1", "source": f"./collections/{DOMAIN}/v0"}],
    }
    repo = _tracked_repo(tmp_path, existing)

    read = land_candidate._validate_marketplace(repo, MARKETPLACE, DOMAIN, COLLECTION_PATH)

    assert read == existing
