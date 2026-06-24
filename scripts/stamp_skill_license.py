"""Stamp metadata.license_tier into every SKILL.md frontmatter and a one-line
license banner (for non-open tiers) just after the H1. Idempotent. Presentation
only — tiers come from skills_index.json; nothing here changes a tier."""
from __future__ import annotations
import json, pathlib, yaml

BANNER_MARKER = "<!-- asb-license-banner -->"
_NOTE = {
    "noncommercial": ("**License: noncommercial** — confirm your use is a permitted "
        "(noncommercial) purpose before applying; commercial use requires a separate "
        "license (see `metadata.tool_license`)."),
    "restricted": ("**License: restricted** — no clear open-source license detected for "
        "the underlying tool; verify licensing before commercial use or redistribution."),
}

def license_banner(tier: str) -> str | None:
    note = _NOTE.get(tier)
    return None if note is None else f"> {note} {BANNER_MARKER}"

def _split(text):
    parts = text.split("---\n", 2)
    return (parts[1], parts[2]) if text.startswith("---\n") and len(parts) == 3 else (None, None)

def _set_banner(body: str, banner: str | None) -> str:
    lines = body.splitlines(keepends=False)
    # drop any existing marked banner line
    lines = [ln for ln in lines if BANNER_MARKER not in ln]
    if banner is None:
        result = "\n".join(lines)
        if body.endswith("\n"):
            result += "\n"
        return result
    # insert after the first H1 (or at top if none), with blank line before banner
    idx = next((i for i, ln in enumerate(lines) if ln.lstrip().startswith("# ")), -1)
    at = idx + 1 if idx >= 0 else 0
    # insert blank line + banner, collapsing if there's already a blank line after H1
    if at < len(lines) and lines[at] == "":
        out = lines[:at+1] + [banner] + lines[at+1:]
    else:
        out = lines[:at] + ["", banner] + lines[at:]
    result = "\n".join(out)
    if body.endswith("\n"):
        result += "\n"
    return result

def stamp_skill(md_path, tier: str) -> bool:
    p = pathlib.Path(md_path)
    text = p.read_text(encoding="utf-8")
    fm_raw, body = _split(text)
    if fm_raw is None:
        return False
    fm = yaml.safe_load(fm_raw) or {}
    if not isinstance(fm.get("metadata"), dict):
        fm["metadata"] = {}
    fm["metadata"]["license_tier"] = tier
    new_body = _set_banner(body, license_banner(tier))
    new_text = "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True) + "---\n" + new_body
    if new_text == text:
        return False
    p.write_text(new_text, encoding="utf-8")
    return True

def stamp_all(skills_dir, index_path) -> dict:
    si = json.loads(pathlib.Path(index_path).read_text(encoding="utf-8"))
    base = pathlib.Path(skills_dir)
    changed = 0; tiers: dict[str, int] = {}
    for e in si:
        tier = e.get("license_tier")
        md = base / e["slug"] / "SKILL.md"
        if tier and md.is_file():
            changed += 1 if stamp_skill(md, tier) else 0
            tiers[tier] = tiers.get(tier, 0) + 1
    return {"changed": changed, "tiers": tiers}

def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--collection", required=True, help="dir containing skills/ + skills_index.json")
    a = ap.parse_args(argv)
    res = stamp_all(f"{a.collection}/skills", f"{a.collection}/skills_index.json")
    print(json.dumps(res, indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
