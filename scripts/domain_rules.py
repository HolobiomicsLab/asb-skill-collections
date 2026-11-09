"""Resolve versioned tooling rules from a collection's declared domain."""

from __future__ import annotations

from pathlib import Path

import yaml


RULES_ROOT = Path(__file__).resolve().parent / "rules"


class DomainRulesError(ValueError):
    """The collection domain or its required rules cannot be resolved."""


def collection_domain(collection: Path) -> str:
    """Return the collection slug, using the existing domain fallback."""
    path = Path(collection) / "collection.yaml"
    try:
        document = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise DomainRulesError(f"cannot read collection domain from {path}: {exc}") from exc
    domain = document.get("domain") or document.get("slug")
    if not isinstance(domain, str) or not domain.strip():
        raise DomainRulesError(f"collection domain is missing from {path}: expected 'domain' or 'slug'")
    return domain.strip()


def domain_rules_path(collection: Path, filename: str) -> Path:
    """Return the rules path for a collection without requiring it to exist."""
    return RULES_ROOT / collection_domain(collection) / filename


def resolve_rules_path(collection: Path, filename: str, explicit: Path | None = None) -> Path:
    """Resolve an explicit rules file or the required per-domain default."""
    if explicit is not None:
        path = Path(explicit)
    else:
        path = domain_rules_path(collection, filename)
    if not path.is_file():
        raise DomainRulesError(f"rules file not found: {path}; add it for this domain or pass --rules")
    return path
