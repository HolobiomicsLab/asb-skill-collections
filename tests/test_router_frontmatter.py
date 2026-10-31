"""The generated router frontmatter parses, and the gate fails one that does not.

`router_shape.write_router` used to fill a string template, so a description
holding ": " (every collector description does: "ASB Genomics: 3246
evidence-grounded skills ...") produced frontmatter that YAML rejects with
"mapping values are not allowed here". The release gate read frontmatter
fail-soft and skipped `_`-prefixed directories, so it passed those routers.
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml

from scripts import release_gate, router_shape


DESCRIPTION_WITH_COLON = (
    "Use when a task needs a skill from ASB Genomics: 3246 evidence-grounded "
    "skills collected from a consolidated literature cut with local retrieval: "
    "search this unit's 3,246 evidence-grounded skills, then apply and "
    "optionally ground the one that fits."
)

# The frontmatter the string template wrote for the genomics router.
UNQUOTED_ROUTER = """---
name: genomics-router
description: Use when a task needs a skill from ASB Genomics: 3246 evidence-grounded skills
license: CC-BY-4.0
schema_version: 0.2.0
---

# ASB Genomics router
"""


def _frontmatter(text: str) -> dict:
    assert text.startswith("---\n")
    return yaml.safe_load(text.split("---\n", 2)[1])


def _unit(tmp_path: Path, description: str) -> Path:
    unit = tmp_path / "unit"
    plugin = unit / ".claude-plugin" / "plugin.json"
    plugin.parent.mkdir(parents=True)
    plugin.write_text(
        json.dumps({"name": "genomics", "description": description}), encoding="utf-8"
    )
    leaf = unit / "leaves" / "alpha" / "SKILL.md"
    leaf.parent.mkdir(parents=True)
    leaf.write_text(
        "---\nname: alpha\nderived_from:\n- doi: 10.1/alpha\n---\n\n# Alpha\n",
        encoding="utf-8",
    )
    return unit


def test_a_description_with_colon_space_round_trips() -> None:
    rendered = router_shape.router_frontmatter(
        "genomics-router", DESCRIPTION_WITH_COLON, 3246
    )

    parsed = yaml.safe_load(rendered)

    assert parsed["name"] == "genomics-router"
    assert parsed["description"] == DESCRIPTION_WITH_COLON
    assert parsed["metadata"]["skills_count"] == 3246
    assert parsed["schema_version"] == "0.2.0"


def test_written_router_frontmatter_parses_for_a_collector_description(
    tmp_path: Path,
) -> None:
    unit = _unit(
        tmp_path,
        "ASB Genomics: 3246 evidence-grounded skills collected from a "
        "consolidated literature cut with local retrieval.",
    )

    router_shape.write_router(unit, 3246)
    text = (unit / "skills" / "_router" / "SKILL.md").read_text(encoding="utf-8")
    frontmatter = _frontmatter(text)

    assert frontmatter["name"] == "genomics-router"
    assert frontmatter["description"].startswith(
        "Use when a task needs a skill from ASB Genomics: 3246 evidence-grounded"
    )
    assert release_gate._frontmatter_error(text) is None
    assert "# ASB Genomics: 3246 evidence-grounded skills" in text


def test_gate_fails_an_unparsable_router_frontmatter(tmp_path: Path) -> None:
    unit = _unit(tmp_path, "Genomics. Fixture.")
    router = unit / "skills" / "_router" / "SKILL.md"
    router.parent.mkdir(parents=True)
    router.write_text(UNQUOTED_ROUTER, encoding="utf-8")

    result = release_gate.check_skill_frontmatter(unit)

    assert result.status == release_gate.FAIL
    assert result.counts["checked"] == 2
    assert result.counts["failed"] == 1
    [finding] = [d for d in result.details if d["status"] == release_gate.FAIL]
    assert finding["file"] == "skills/_router/SKILL.md"
    assert "does not parse as YAML" in finding["message"]


def test_gate_passes_the_regenerated_router(tmp_path: Path) -> None:
    unit = _unit(tmp_path, "ASB Genomics: 3 skills. Fixture.")
    router_shape.write_router(unit, 1)

    result = release_gate.check_skill_frontmatter(unit)

    assert result.status == release_gate.PASS
    assert result.counts["checked"] == 2


def test_gate_fails_a_missing_or_non_mapping_frontmatter(tmp_path: Path) -> None:
    unit = _unit(tmp_path, "Genomics. Fixture.")
    for slug, text in (
        ("no-block", "# No frontmatter\n"),
        ("open-block", "---\nname: open\n"),
        ("scalar", "---\njust a string\n---\n# Body\n"),
    ):
        path = unit / "leaves" / slug / "SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text(text, encoding="utf-8")

    result = release_gate.check_skill_frontmatter(unit)

    failed = sorted(d["file"] for d in result.details if d["status"] == release_gate.FAIL)
    assert failed == [
        "leaves/no-block/SKILL.md",
        "leaves/open-block/SKILL.md",
        "leaves/scalar/SKILL.md",
    ]


def test_run_gate_blocks_a_strict_release_on_an_unparsable_router(tmp_path: Path) -> None:
    unit = _unit(tmp_path, "Genomics. Fixture.")
    router = unit / "skills" / "_router" / "SKILL.md"
    router.parent.mkdir(parents=True)
    router.write_text(UNQUOTED_ROUTER, encoding="utf-8")
    (unit / "corpus.yaml").write_text(
        yaml.safe_dump(
            {
                "papers": [
                    {
                        "doi": "10.1/alpha",
                        "status": "included",
                        "access": {"type": "gold-oa"},
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    report = release_gate.run_gate(unit, None, True)
    checks = {check["name"]: check for check in report["checks"]}

    assert checks["skill_frontmatter"]["status"] == release_gate.FAIL
    assert report["release_verified"] is False
