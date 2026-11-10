"""What one search call prints is what an agent needs to choose, cite and read.

Live sessions read the text output of `bin/search_skills.py`, not `--json`.
Each hit carries the licence tier and the source DOI on its first line and an
absolute `read:` path; the scoring explanation stays in `--json`. A search that
matches nothing says what to try next.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from scripts import router_shape


REPO = Path(__file__).resolve().parent.parent
FIXTURE = REPO / "tests" / "fixtures" / "router_collection"


@pytest.fixture()
def unit(tmp_path: Path) -> Path:
    built = tmp_path / "fixture"
    shutil.copytree(FIXTURE, built)
    index = built / "skills_index.json"
    rows = json.loads(index.read_text(encoding="utf-8"))
    for number, row in enumerate(rows):
        row["dois"] = [f"10.1000/fixture.{number}", "10.1000/second"]
    index.write_text(json.dumps(rows), encoding="utf-8")
    flows_index = built / "workflows" / "workflows_index.json"
    flows = json.loads(flows_index.read_text(encoding="utf-8"))
    for flow in flows:
        flow["stages"] = ["acquire", "annotate"]
    flows_index.write_text(json.dumps(flows), encoding="utf-8")
    tool = {"name": "AlignFixture", "slug": "alignfixture", "license_tier": "open",
            "license": "MIT", "used_by_skills": ["chromatographic-alignment"],
            "dois": ["10.1000/tool"]}
    (built / "tools").mkdir(exist_ok=True)
    (built / "tools" / "alignfixture.yaml").write_text("name: AlignFixture\n", encoding="utf-8")
    (built / "tools_index.json").write_text(json.dumps([tool]), encoding="utf-8")
    return built


def _search(unit: Path, *args: str, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(unit / "bin" / "search_skills.py"), *args],
        cwd=cwd, capture_output=True, text=True, timeout=120,
    )


def test_fixture_script_is_the_generated_template() -> None:
    generated = router_shape.embed_selector(router_shape.SEARCH_SCRIPT.read_bytes())
    assert (FIXTURE / "bin" / "search_skills.py").read_bytes() == generated


def test_skill_hits_carry_tier_doi_and_an_absolute_path(unit: Path, tmp_path: Path) -> None:
    result = _search(unit, "--query", "align retention time across samples", "-k", "3",
                     cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    out = result.stdout
    assert "explanation:" not in out
    heads = [line for line in out.splitlines() if line[:1].isdigit()]
    assert heads
    for head in heads:
        assert "| tier: " in head and "| doi: 10.1000/fixture." in head
        assert head.endswith("(+1 more)")
    reads = [line.split("read:", 1)[1].strip() for line in out.splitlines() if "read:" in line]
    assert reads and all(Path(path).is_absolute() and Path(path).is_file() for path in reads)


def test_json_keeps_the_scoring_explanation(unit: Path, tmp_path: Path) -> None:
    result = _search(unit, "--query", "align retention time", "-k", "1", "--json", cwd=tmp_path)
    hit = json.loads(result.stdout)["results"][0]
    assert hit["selector"]["name"] == "asb-keyword" and hit["matched_fields"]


def test_tool_hits_answer_the_licence_question(unit: Path, tmp_path: Path) -> None:
    result = _search(unit, "--query", "AlignFixture", "--target", "tools", "-k", "1",
                     cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    first, second, read = result.stdout.splitlines()[:3]
    assert first == "1. alignfixture | tier: open | licence: MIT"
    assert second == "   used by 1 skill | doi: 10.1000/tool"
    assert read.endswith("/tools/alignfixture.yaml")


def test_workflow_hits_list_their_stages(unit: Path, tmp_path: Path) -> None:
    result = _search(unit, "--query", "annotation", "--target", "workflows", "-k", "1",
                     cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    assert "   stages: acquire -> annotate" in result.stdout
    assert "/workflows/" in result.stdout and "tier:" not in result.stdout


def test_no_match_says_what_to_try_next(unit: Path, tmp_path: Path) -> None:
    result = _search(unit, "--query", "zzzunmatchable", cwd=tmp_path)
    assert result.returncode == 0
    assert result.stdout.startswith("no skills matched. Next: use fewer, plainer words")
    assert "--target workflows / --target tools" in result.stdout


def test_an_unknown_tool_filter_points_to_the_tool_search(unit: Path, tmp_path: Path) -> None:
    result = _search(unit, "--query", "align", "--tool", "NoSuchTool", cwd=tmp_path)
    assert result.returncode == 0
    assert '--target tools --query "NoSuchTool"' in result.stdout
