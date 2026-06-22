"""Parse a SKILL.md into (frontmatter dict, body str)."""
from __future__ import annotations

from pathlib import Path

import yaml


def parse_skill_md(path: Path) -> tuple[dict, str]:
    text = Path(path).read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            loaded = yaml.safe_load(parts[1])
            fm = loaded if isinstance(loaded, dict) else {}
            body = parts[2].lstrip("\n")
            return fm, body
    return {}, text
