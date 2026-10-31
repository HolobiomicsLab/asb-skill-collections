"""A selection drawn from a checkout older than the installed package is refused.

`asbb install --skills/--skills-file/--query` derives the selection with the
checkout's own ``scripts/build_packs.py``. A package newer than the checkout
(an older clone, or an archived release) used to reach
``PackSpec(slugs=...)`` and stop with a TypeError traceback. The checkout's API
is now checked first, and a mismatch is a message and exit 2.
"""

from __future__ import annotations

import json
import pathlib
import sys

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from asb_skill_collections.asbb import manifest, subset  # noqa: E402
from asb_skill_collections.asbb_cli import main  # noqa: E402

COLLECTION = "astronomy/v3"
SLUG = "stellar-photometry"

#: ``build_packs`` as it stood before selections: a pack is a technique tag only.
OLD_BUILD_PACKS = '''
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PackSpec:
    directory: Path
    tag: str
    map_path: Path


def build_pack(spec, collection_dir, **kwargs):
    raise AssertionError("an old checkout must be refused before any build")
'''


def _stub_checkout(root: pathlib.Path, build_packs: str | None) -> pathlib.Path:
    """A checkout with one collection and the given ``scripts/build_packs.py``."""
    collection = root / "collections" / "astronomy" / "v3"
    leaf = collection / "leaves" / SLUG / "SKILL.md"
    leaf.parent.mkdir(parents=True)
    leaf.write_text(f"---\nname: {SLUG}\ndescription: Use when measuring.\n---\n", encoding="utf-8")
    index = [{"slug": SLUG, "name": SLUG, "description": "Use when measuring stars.",
              "techniques": ["optical"], "license_tier": "open"}]
    (collection / "skills_index.json").write_text(json.dumps(index), encoding="utf-8")
    marketplace = root / ".claude-plugin" / "marketplace.json"
    marketplace.parent.mkdir(parents=True)
    marketplace.write_text(json.dumps({"name": "demo", "plugins": [
        {"name": "astronomy", "source": "./collections/astronomy/v3"}]}), encoding="utf-8")
    scripts = root / "scripts"
    scripts.mkdir()
    (scripts / "__init__.py").write_text("", encoding="utf-8")
    for name in ("build_grounding_bundle", "router_shape"):
        (scripts / f"{name}.py").write_text("", encoding="utf-8")
    if build_packs is not None:
        (scripts / "build_packs.py").write_text(build_packs, encoding="utf-8")
    return root


@pytest.fixture
def isolated_scripts(monkeypatch):
    """Import ``scripts`` from the stub checkout, then restore this checkout's."""
    monkeypatch.setattr(sys, "path", list(sys.path))
    saved = {name: module for name, module in sys.modules.items()
             if name == "scripts" or name.startswith("scripts.")}
    for name in saved:
        del sys.modules[name]
    yield
    for name in [name for name in sys.modules if name == "scripts" or name.startswith("scripts.")]:
        del sys.modules[name]
    sys.modules.update(saved)


@pytest.mark.parametrize(
    "build_packs", (OLD_BUILD_PACKS, None), ids=("packspec-without-slugs", "no-build-packs"))
@pytest.mark.parametrize("dry_run", ((), ("--dry-run",)), ids=("install", "dry-run"))
def test_an_older_checkout_exits_2_with_the_pull_message(
    tmp_path, capsys, isolated_scripts, build_packs, dry_run
):
    repo = _stub_checkout(tmp_path / "old-clone", build_packs)
    home = tmp_path / "home"

    rc = main(["install", "--skills", SLUG, "--collection", COLLECTION, "--runtime", "agents",
               "--repo", str(repo), "--home", str(home), *dry_run])

    err = capsys.readouterr().err
    assert rc == 2
    assert f"checkout at {repo.resolve()} predates selection support" in err
    assert "git pull" in err
    assert "Traceback" not in err and "TypeError" not in err
    assert not (home / ".agents").exists()
    assert manifest.load(home) == {}


def test_this_checkout_passes_the_check():
    from scripts import build_packs

    assert subset.check_checkout(build_packs, REPO_ROOT) is None
