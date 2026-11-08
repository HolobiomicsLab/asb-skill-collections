"""Shared, compact fixtures for tests that operate on a collection checkout."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from scripts import collect_from_cut


FIXTURE_COLLECTION = Path(__file__).parent / "fixtures" / "router_collection"


@pytest.fixture
def collection_repo(tmp_path: Path) -> Path:
    """Return a temporary repository containing the router-shaped fixture."""
    root = tmp_path / "repository"
    collection = root / "collections" / "fixture" / "v1"
    collection.parent.mkdir(parents=True)
    shutil.copytree(FIXTURE_COLLECTION, collection)
    return root


@pytest.fixture(scope="session")
def tooling_checkout(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Build a temporary tooling checkout whose templates come from fixtures."""
    import asb_skill_collections

    root = tmp_path_factory.mktemp("tooling-repository")
    sources = {
        "scripts": Path(collect_from_cut.__file__).parent,
        "asb_skill_collections": Path(asb_skill_collections.__file__).parent,
    }
    for name, source in sources.items():
        shutil.copytree(source, root / name, ignore=shutil.ignore_patterns("__pycache__"))
    repository = Path(__file__).parent.parent
    shutil.copytree(repository / "governance", root / "governance")
    collection = root / "collections" / "metabolomics" / "v2"
    collection.parent.mkdir(parents=True)
    shutil.copytree(FIXTURE_COLLECTION, collection)
    return root


@pytest.fixture(scope="session")
def embedding_stub(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Provide deterministic vectors for the three-output assembly fixture."""
    root = tmp_path_factory.mktemp("embedding-stub")
    package = root / "sentence_transformers"
    package.mkdir()
    (package / "__init__.py").write_text(
        "import numpy as np\n"
        "class SentenceTransformer:\n"
        "    def __init__(self, *args, **kwargs):\n"
        "        pass\n"
        "    def encode(self, texts, **kwargs):\n"
        "        unique = list(dict.fromkeys(texts))\n"
        "        vectors = np.eye(len(unique), dtype=float)\n"
        "        return np.array([vectors[unique.index(text)] for text in texts])\n",
        encoding="utf-8",
    )
    return root


@pytest.fixture
def offline_environment(embedding_stub: Path) -> dict[str, str]:
    """Return an offline subprocess environment with deterministic embeddings."""
    import os

    environment = dict(os.environ)
    for key in ("OPENAI_API_KEY", "OPENROUTER_API_KEY", "ANTHROPIC_API_KEY"):
        environment.pop(key, None)
    environment.update(
        HF_HUB_OFFLINE="1",
        TRANSFORMERS_OFFLINE="1",
        ASB_EMBED_MODEL="bge-small-en-v1.5",
        PYTHONDONTWRITEBYTECODE="1",
        PYTHONPATH=str(embedding_stub),
    )
    return environment
