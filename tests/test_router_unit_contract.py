"""Router text follows the contract carried by a unit's sampled leaves."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from scripts import router_shape


REPO = Path(__file__).resolve().parent.parent
V2 = REPO / "collections" / "metabolomics" / "v2"

CURRENT_APPLY = """## 2. Apply

Read the chosen `leaves/<slug>/SKILL.md`. Its frontmatter carries `tools` (what
to install or invoke), `derived_from` (source paper DOIs) and `evidence_spans`
(verbatim anchors from the paper or repo). Follow the body.
"""
CURRENT_GROUNDING = """## 3. Ground (recommended)

Before trusting a parameter, threshold or default, verify it against the paper
the skill was built from. `kb_bundle.json` maps each skill to its source KBs:

```bash
python bin/perspicacite_kb_bind.py query --skill <slug> \\
  --question "<what you need to verify>"
```

See `GROUNDING.md` for the backends and tiers.
"""


def _write_plugin(unit: Path, name: str = "test-unit") -> None:
    plugin = unit / ".claude-plugin" / "plugin.json"
    plugin.parent.mkdir(parents=True)
    plugin.write_text(
        json.dumps({"name": name, "description": "Test Unit. Fixture corpus."}),
        encoding="utf-8",
    )


def _write_leaf(unit: Path, slug: str, frontmatter: str, body: str = "# Body\n") -> Path:
    skill = unit / "leaves" / slug / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text(f"---\n{frontmatter.rstrip()}\n---\n\n{body}", encoding="utf-8")
    return skill


def _rendered_router(unit: Path, count: int = 1) -> str:
    router_shape.write_router(unit, count)
    return (unit / "skills" / "_router" / "SKILL.md").read_text(encoding="utf-8")


def test_v2_contract_keeps_current_generic_sections_byte_for_byte(tmp_path):
    unit = tmp_path / "unit"
    _write_plugin(unit)
    _write_leaf(
        unit,
        "alpha",
        "tools:\n- Alpha\nderived_from:\n- doi: 10.1/alpha\nevidence_spans:\n- quote",
    )
    (unit / "bin").mkdir()
    (unit / "bin" / "perspicacite_kb_bind.py").write_text("", encoding="utf-8")
    (unit / "GROUNDING.md").write_text("grounding\n", encoding="utf-8")

    rendered = _rendered_router(unit)

    assert CURRENT_APPLY in rendered
    assert CURRENT_GROUNDING in rendered


def test_cut_contract_replaces_stale_sections_without_phantom_helpers(tmp_path):
    unit = tmp_path / "unit"
    _write_plugin(unit)
    _write_leaf(
        unit,
        "alpha",
        "metadata:\n  tools:\n  - Alpha\nprovenance:\n  source_papers:\n  - doi: 10.1/alpha",
        "# Body\n\n## Evidence\n\n- [methods] exact line\n",
    )
    (unit / "bin").mkdir()
    (unit / "bin" / "search_skills.py").write_text("", encoding="utf-8")
    stale = (
        "---\nname: hand-written\ndescription: keep me\n---\n\n"
        "# Hand-written router\n\nKeep this introduction byte-for-byte.\n\n"
        f"{CURRENT_APPLY}\n{CURRENT_GROUNDING}\n"
        "## Licence tiers\n\nKeep this ending byte-for-byte.\n"
    )
    target = unit / "skills" / "_router" / "SKILL.md"
    target.parent.mkdir(parents=True)
    target.write_text(stale, encoding="utf-8")

    rendered = _rendered_router(unit)

    assert rendered.startswith(
        "---\nname: hand-written\ndescription: keep me\n---\n\n"
        "# Hand-written router\n\nKeep this introduction byte-for-byte.\n\n"
    )
    assert rendered.endswith("## Licence tiers\n\nKeep this ending byte-for-byte.\n")
    assert "`metadata.tools`" in rendered
    assert "`provenance.source_papers`" in rendered
    assert "verbatim evidence lines in the body" in rendered
    assert "source-paper DOIs of the leaf" in rendered
    for phantom in (
        "`tools`",
        "perspicacite_kb_bind",
        "kb_bundle.json",
        "GROUNDING.md",
        "derived_from",
        "evidence_spans",
    ):
        assert phantom not in rendered


def test_mixed_leaf_contract_names_both_variants(tmp_path):
    unit = tmp_path / "unit"
    _write_plugin(unit)
    _write_leaf(
        unit,
        "alpha",
        "tools:\n- Alpha\nderived_from:\n- doi: 10.1/alpha\nevidence_spans:\n- quote",
    )
    _write_leaf(
        unit,
        "beta",
        "metadata:\n  tools:\n  - Beta\nprovenance:\n  source_papers:\n  - doi: 10.1/beta",
    )

    rendered = _rendered_router(unit, count=2)

    for key in (
        "`tools`",
        "`metadata.tools`",
        "`derived_from`",
        "`provenance.source_papers`",
        "`evidence_spans`",
    ):
        assert key in rendered


def test_existing_metabolomics_v2_router_is_byte_identical_in_a_copy(tmp_path):
    unit = tmp_path / "v2"
    shutil.copytree(V2 / ".claude-plugin", unit / ".claude-plugin")
    shutil.copytree(V2 / "skills" / "_router", unit / "skills" / "_router")
    leaves = sorted((V2 / "leaves").glob("*/SKILL.md"))[:20]
    for source in leaves:
        target = unit / "leaves" / source.parent.name / source.name
        target.parent.mkdir(parents=True)
        shutil.copy2(source, target)
    (unit / "bin").mkdir()
    shutil.copy2(
        V2 / "bin" / "perspicacite_kb_bind.py",
        unit / "bin" / "perspicacite_kb_bind.py",
    )
    shutil.copy2(V2 / "GROUNDING.md", unit / "GROUNDING.md")
    expected = (V2 / "skills" / "_router" / "SKILL.md").read_bytes()

    router_shape.write_router(unit, 5_859)

    assert (unit / "skills" / "_router" / "SKILL.md").read_bytes() == expected


def test_legacy_contract_uses_layout_slug_dirs(tmp_path, monkeypatch):
    unit = tmp_path / "legacy"
    skill = unit / "skills" / "alpha" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text(
        "---\ntools:\n- Alpha\nderived_from:\n- doi: 10.1/alpha\n---\n",
        encoding="utf-8",
    )
    calls = []
    real_slug_dirs = router_shape.layout.slug_dirs

    def recording_slug_dirs(path):
        calls.append(Path(path))
        return real_slug_dirs(path)

    monkeypatch.setattr(router_shape.layout, "slug_dirs", recording_slug_dirs)

    contract = router_shape.unit_contract(unit)

    assert calls == [unit]
    assert contract["tool_keys"] == "`tools`"
    assert contract["source_keys"] == "`derived_from`"


def test_unit_contract_reads_at_most_twenty_frontmatters(tmp_path, monkeypatch):
    unit = tmp_path / "unit"
    for number in range(25):
        _write_leaf(unit, f"leaf-{number:02d}", "tools:\n- Alpha")
    reads = []
    real_parse = router_shape.parse_frontmatter

    def recording_parse(path):
        reads.append(Path(path))
        return real_parse(path)

    monkeypatch.setattr(router_shape, "parse_frontmatter", recording_parse)

    router_shape.unit_contract(unit)

    assert len(reads) == 20
