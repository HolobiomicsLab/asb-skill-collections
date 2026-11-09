#!/usr/bin/env python3
"""Render registry-backed GitHub Actions callers for one domain."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

import yaml


REPOSITORY = Path(__file__).resolve().parent.parent
SHA_PATTERN = re.compile(r"^[0-9a-fA-F]{40}$")
DOMAIN_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RELEASED_OUTPUTS = ("gates.yml", "plugin-validate.yml", "intake.yml", "retraction-watch.yml")
CANDIDATE_OUTPUTS = ("gates.yml", "intake.yml", "retraction-watch.yml")
CANDIDATE_COMMENT = "# candidate stage: rendered before the first registry release; re-render after registration"


def published_releases(manifest: Path, domain: str) -> list[dict]:
    """Return non-legacy releases for a declared domain."""
    document = yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
    entry = (document.get("domains") or {}).get(domain)
    if entry is None:
        raise ValueError(f"domain is not declared in {manifest}: {domain}")
    return [release for release in entry.get("releases") or [] if release.get("status") != "legacy"]


def matrix_rows(releases: list[dict]) -> str:
    """Render one explicit matrix entry per published release."""
    if not releases:
        raise ValueError("domain has no non-legacy releases; no content caller was rendered")
    lines = []
    for release in releases:
        receipt = release.get("receipts_path") or ""
        lines.extend(
            (
                f"            - domain: {release['domain']}",
                f"              collection_path: {release['path']}",
                f'              receipts_path: "{receipt}"',
            )
        )
    return "\n".join(lines)


def candidate_release(domain: str, collection_path: str | None) -> list[dict]:
    """Return one unreleased matrix row from an explicit collection path."""
    if not collection_path:
        raise ValueError("candidate stage requires --collection-path")
    if not collection_path or not re.fullmatch(
        rf"collections/{re.escape(domain)}/v[1-9][0-9]*", collection_path
    ):
        raise ValueError("collection path must have the form collections/<domain>/v<N>")
    return [{"domain": domain, "path": collection_path, "receipts_path": ""}]


def render_caller(template: str, domain: str, tooling_sha: str, releases: list[dict]) -> str:
    """Fill the SHA and release-matrix placeholders in the caller template."""
    rows = [dict(release, domain=domain) for release in releases]
    return template.replace("<TOOLING_SHA>", tooling_sha).replace("<MATRIX_ROWS>", matrix_rows(rows))


def render(manifest: Path, domain: str, tooling_sha: str, templates: Path, out: Path,
           receipts: dict[str, str] | None = None, stage: str = "released",
           collection_path: str | None = None) -> list[Path]:
    """Write the stage callers into one workflow directory.

    Candidate rendering omits plugin-validate.yml because its marketplace has no
    plugin yet; the released stage renders all four callers.
    """
    if not DOMAIN_PATTERN.fullmatch(domain):
        raise ValueError("domain must be a lowercase slug")
    if not SHA_PATTERN.fullmatch(tooling_sha):
        raise ValueError("tooling SHA must contain exactly 40 hexadecimal characters")
    if stage not in {"released", "candidate"}:
        raise ValueError("stage must be released or candidate")
    releases = (candidate_release(domain, collection_path) if stage == "candidate"
                else published_releases(manifest, domain))
    receipt_map = receipts or {}
    unknown = set(receipt_map) - {release["path"] for release in releases}
    if unknown:
        raise ValueError(f"receipt map names no current release: {', '.join(sorted(unknown))}")
    releases = [dict(release, receipts_path=receipt_map.get(release["path"], release.get("receipts_path", "")))
                for release in releases]
    caller = (templates / "domain-ci.yml").read_text(encoding="utf-8")
    intake = (templates / "domain-intake.yml").read_text(encoding="utf-8")
    retraction = (templates / "domain-retraction-watch.yml").read_text(encoding="utf-8")
    if stage == "candidate":
        caller = caller.replace("<MATRIX_ROWS>", CANDIDATE_COMMENT + "\n<MATRIX_ROWS>")
    gates = render_caller(caller, domain, tooling_sha, releases)
    outputs = list(CANDIDATE_OUTPUTS if stage == "candidate" else RELEASED_OUTPUTS)
    rendered = {
        "gates.yml": gates,
        "intake.yml": intake.replace("<TOOLING_SHA>", tooling_sha).replace("<DOMAIN>", domain),
        "retraction-watch.yml": retraction.replace("<TOOLING_SHA>", tooling_sha).replace("<DOMAIN>", domain),
    }
    if stage == "released":
        plugin = (templates / "domain-plugin-validate.yml").read_text(encoding="utf-8")
        rendered["plugin-validate.yml"] = plugin.replace("<TOOLING_SHA>", tooling_sha)
    out.mkdir(parents=True, exist_ok=True)
    stale_plugin = out / "plugin-validate.yml"
    if stage == "candidate" and stale_plugin.exists():
        stale_plugin.unlink()
    paths = [out / filename for filename in outputs]
    for path in paths:
        path.write_text(rendered[path.name], encoding="utf-8")
    return paths


def parser() -> argparse.ArgumentParser:
    """Declare the registry, domain, tooling pin and output options."""
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--manifest", type=Path, required=True)
    result.add_argument("--domain", required=True)
    result.add_argument("--tooling-sha", required=True)
    result.add_argument("--out", type=Path, default=Path(".github/workflows"))
    result.add_argument("--templates", type=Path, default=REPOSITORY / "scripts" / "templates")
    result.add_argument("--stage", choices=("released", "candidate"), default="released")
    result.add_argument("--collection-path")
    result.add_argument(
        "--receipts",
        type=Path,
        help="optional JSON object mapping collection_path to receipts_path",
    )
    return result


def main(argv: list[str] | None = None) -> int:
    """Render the workflow callers and report their destinations."""
    options = parser().parse_args(argv)
    try:
        receipts = json.loads(options.receipts.read_text(encoding="utf-8")) if options.receipts else None
        if receipts is not None and not isinstance(receipts, dict):
            raise ValueError("receipt map must be a JSON object")
        paths = render(
            options.manifest, options.domain, options.tooling_sha, options.templates, options.out,
            receipts, options.stage, options.collection_path,
        )
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as exc:
        parser().error(str(exc))
    for path in paths:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
