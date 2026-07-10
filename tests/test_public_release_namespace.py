"""Every advertised (installable) plugin must be free of the dead ASB namespace.

The `asb:` term base moved to `https://w3id.org/asb#`; the old bases
(`holobiomicslab.eu/ns/asb`, the never-registered `asb.holobiomics.org`) resolve to
nothing. A shipped JSON-LD `@context` still binding them would send a consumer to a
dead domain. The public release is exactly what `marketplace.json` advertises
(metabolomics/v2 + its packs), so this guard derives the shipped dirs from there —
it stays correct as the marketplace changes, and it deliberately does NOT cover the
`*/v1/` collections, whose namespace migration is a separate human decision (they may
be frozen at a DOI'd snapshot). See `orphan-grounding`'s neighbour in HUMAN_REVIEW_GATE.md.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).parent.parent
OLD_BASES = ("holobiomicslab.eu/ns/asb", "asb.holobiomics.org")
TEXT_SUFFIXES = {".jsonld", ".json", ".yaml", ".yml", ".ttl", ".md", ".py"}
PROSE_EXEMPT = {"README.md", "CHANGELOG.md", "changelog.md"}  # historical mentions allowed


def _shipped_dirs():
    data = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
    dirs = []
    for p in data["plugins"]:
        src = (p.get("source") or p.get("path") or "").lstrip("./")
        if src:
            dirs.append(ROOT / src)
    return dirs


def test_marketplace_lists_shipped_dirs():
    dirs = _shipped_dirs()
    assert dirs, "marketplace.json advertises no plugins"
    for d in dirs:
        assert d.is_dir(), f"marketplace source dir missing on disk: {d}"


def test_no_advertised_plugin_binds_a_dead_namespace():
    offenders = []
    for d in _shipped_dirs():
        for path in d.rglob("*"):
            if path.suffix not in TEXT_SUFFIXES or path.name in PROSE_EXEMPT:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for base in OLD_BASES:
                if base in text:
                    offenders.append(f"{path.relative_to(ROOT)}: binds {base!r}")
                    break
    assert not offenders, (
        "advertised plugins still bind the dead ASB namespace (migrate to "
        "https://w3id.org/asb#):\n  " + "\n  ".join(offenders)
    )


if __name__ == "__main__":
    import sys

    import pytest

    sys.exit(pytest.main([__file__, "-q"]))
