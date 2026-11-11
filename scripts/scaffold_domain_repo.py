#!/usr/bin/env python3
"""Scaffold the shared repository surface for one ASB skill domain."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path, PurePosixPath
import re
import sys
import tempfile

import yaml

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts import render_domain_ci


REPOSITORY = Path(__file__).resolve().parent.parent
TEMPLATES = REPOSITORY / "scripts" / "templates"
MASTER_URL = "https://github.com/HolobiomicsLab/asb-skill-collections"
DOMAIN_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PLACEHOLDER_PATTERN = re.compile(r"<[A-Z][A-Z0-9_]+>")
GITHUB_URL_PATTERN = re.compile(r"https://github\.com/[A-Za-z0-9_.~:/?#@!$&'()*+,;=%-]+", re.IGNORECASE)


@dataclass(frozen=True)
class Options:
    """Validated inputs shared by the CLI and in-process proof runs."""

    domain: str
    title: str
    out: Path
    tooling_sha: str
    stage: str = "released"
    collection_path: str | None = None
    publication_drafts: Path | None = None
    manifest: Path = REPOSITORY / "collections.yaml"
    templates: Path = TEMPLATES
    force: bool = False
    dry_run: bool = False


def parser() -> argparse.ArgumentParser:
    """Declare domain identity, publication metadata and output controls."""
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--domain", required=True)
    result.add_argument("--title", required=True)
    result.add_argument("--out", required=True, type=Path)
    result.add_argument("--tooling-sha", required=True)
    result.add_argument("--stage", choices=("candidate", "released"), default="released")
    result.add_argument("--collection-path")
    result.add_argument("--publication-drafts", type=Path)
    result.add_argument("--manifest", type=Path, default=REPOSITORY / "collections.yaml")
    result.add_argument("--templates", type=Path, default=TEMPLATES, help=argparse.SUPPRESS)
    result.add_argument("--force", action="store_true")
    result.add_argument("--dry-run", action="store_true")
    return result


def domain_entry(manifest: Path, domain: str, required: bool) -> dict:
    """Read one domain entry without requiring registration at candidate stage."""
    document = yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
    entry = (document.get("domains") or {}).get(domain)
    if entry is None:
        if required:
            raise ValueError(f"domain is not declared in {manifest}: {domain}")
        return {}
    if not isinstance(entry, dict):
        raise ValueError(f"domain entry must be a mapping: {domain}")
    return entry


def current_releases(entry: dict, required: bool) -> list[dict]:
    """Return current registry releases, newest version first."""
    releases = [row for row in entry.get("releases") or [] if row.get("status") != "legacy"]
    if required and not releases:
        raise ValueError("released stage failed: domain has no non-legacy release")
    return sorted(releases, key=lambda row: int(row["version"]), reverse=True)


def collection_path(options: Options, releases: list[dict]) -> str:
    """Resolve the candidate path or newest released collection."""
    if options.stage == "candidate":
        return render_domain_ci.candidate_release(options.domain, options.collection_path)[0]["path"]
    return releases[0]["path"]


def substitute(text: str, values: dict[str, str]) -> str:
    """Replace uppercase template fields and reject an incomplete rendering."""
    for key, value in values.items():
        text = text.replace(f"<{key}>", value)
    unresolved = PLACEHOLDER_PATTERN.findall(text)
    if unresolved:
        raise ValueError(f"unsubstituted template placeholders: {', '.join(sorted(set(unresolved)))}")
    return text


def collection_title(options: Options, release: dict) -> str:
    """Build a stable registry-row title without requiring optional metadata."""
    return str(release.get("title") or f"ASB {options.title} Skill Collection v{release['version']}")


def doi_link(doi: object) -> str:
    """Render a version DOI link or an explicit absence."""
    return f"[{doi}](https://doi.org/{doi})" if doi else "not deposited"


def collections_table(options: Options, releases: list[dict]) -> str:
    """Render either current release rows or the candidate-stage status."""
    if options.stage == "candidate":
        return "No collection released yet; the candidate is reviewed on its `candidate/<cut-id>` branch."
    lines = ["| Path | Title | Skills | Tools | Released | DOI |", "|---|---|---|---|---|---|"]
    for release in releases:
        lines.append(
            f"| `{release['path']}` | {collection_title(options, release)} | {release.get('skills', 'not recorded')} "
            f"| {release.get('tools', 'not recorded')} | {release.get('released', 'not recorded')} "
            f"| {doi_link(release.get('version_doi'))} |"
        )
    return "\n".join(lines)


def citation_doi(entry: dict) -> str:
    """Link the domain concept DOI when registration has supplied one."""
    doi = entry.get("concept_doi")
    return f"Zenodo concept DOI: [{doi}](https://doi.org/{doi})." if doi else "The Zenodo DOI is added when the first release is deposited."


def render_readme(options: Options, entry: dict, releases: list[dict], selected_path: str) -> str:
    """Render the domain overview and its install and citation targets."""
    version = PurePosixPath(selected_path).name
    values = {
        "DOMAIN_TITLE": options.title,
        "DOMAIN": options.domain,
        "COLLECTIONS": collections_table(options, releases),
        "INSTALL_COLLECTION": f"{options.domain}/{version}",
        "REPOSITORY_URL": repository_url(options.domain),
        "CITATION_DOI": citation_doi(entry),
    }
    return substitute((options.templates / "domain-README.md").read_text(encoding="utf-8"), values)


def repository_url(domain: str) -> str:
    """Return the only domain repository URL permitted in generated files."""
    return f"https://github.com/HolobiomicsLab/asb-skills-{domain}"


def marketplace(options: Options, releases: list[dict]) -> str:
    """Render one local plugin entry per current release."""
    url = repository_url(options.domain)
    plugins = []
    for index, release in enumerate(releases):
        version = int(release["version"])
        plugins.append({
            "name": options.domain if index == 0 else f"{options.domain}-v{version}",
            "source": f"./{release['path']}",
            "description": f"{collection_title(options, release)}: {release.get('skills', 'not recorded')} evidence-grounded skills over {release.get('tools', 'not recorded')} tools.",
            "version": f"{version}.0.0",
            "author": {"name": "Holobiomics Lab", "url": "https://github.com/HolobiomicsLab"},
            "homepage": url,
            "repository": url,
            "license": "CC-BY-4.0",
            "keywords": [options.domain, "agentic-science", "skills"],
        })
    document = {
        "name": f"asb-skills-{options.domain}",
        "description": f"Evidence-grounded {options.title} skill and software-tool collections from the AgenticScienceBuilder pipeline.",
        "owner": {"name": "Holobiomics Lab", "url": "https://github.com/HolobiomicsLab"},
        "plugins": plugins,
    }
    return json.dumps(document, indent=2, ensure_ascii=False) + "\n"


def publication_file(options: Options, name: str) -> str:
    """Render a supplied publication draft with only permitted repository links."""
    draft = options.publication_drafts / options.domain / name if options.publication_drafts else None
    if draft is not None and draft.is_file():
        text = draft.read_text(encoding="utf-8")
        pipeline = "https://github.com/HolobiomicsLab/" + "AgenticScienceBuilder"
        if name == "CITATION.cff":
            document = yaml.safe_load(text)
            document["abstract"] = str(document.get("abstract", "")).replace(
                f"generating pipeline - {pipeline}", "generating pipeline - AgenticScienceBuilder"
            )
            document["references"] = [
                reference for reference in document.get("references") or []
                if reference.get("repository-code") != pipeline
            ]
            return yaml.safe_dump(document, sort_keys=False, allow_unicode=True, width=100)
        document = json.loads(text)
        document["description"] = str(document.get("description", "")).replace(
            f"generating pipeline - {pipeline}", "generating pipeline - AgenticScienceBuilder"
        )
        document["related_identifiers"] = [
            relation for relation in document.get("related_identifiers") or []
            if relation.get("identifier") != pipeline
        ]
        return json.dumps(document, indent=2, ensure_ascii=False) + "\n"
    template_name = "domain-CITATION.cff" if name == "CITATION.cff" else "domain-zenodo.json"
    values = {
        "DOMAIN_TITLE": options.title,
        "DOMAIN": options.domain,
        "REPOSITORY_URL": repository_url(options.domain),
    }
    return substitute((options.templates / template_name).read_text(encoding="utf-8"), values)


def issue_form(domain: str) -> str:
    """Fix the shared paper proposal form to one domain without changing labels."""
    text = (REPOSITORY / ".github/ISSUE_TEMPLATE/3-propose-paper.md").read_text(encoding="utf-8")
    fixed, count = re.subn(r"(?m)^(\*\*Target collection:\*\*) <!--.*-->$", rf"\1 <!-- {domain} -->", text)
    if count != 1:
        raise ValueError("propose-paper.md has no single 'Target collection' line to fix to the domain")
    return fixed


def licence_files(options: Options) -> tuple[str, str]:
    """Copy the released domain licence texts without external source URLs."""
    return (
        (REPOSITORY / "LICENSE").read_text(encoding="utf-8"),
        (options.templates / "domain-LICENSING.md").read_text(encoding="utf-8"),
    )


def validate_publication_files(citation: str, zenodo: str) -> None:
    """Check the structural CFF and JSON contracts before writing anything."""
    document = yaml.safe_load(citation)
    if not isinstance(document, dict) or document.get("cff-version") != "1.2.0":
        raise ValueError("CITATION.cff must be a CFF 1.2.0 mapping")
    for key in ("message", "title", "authors", "license"):
        if key not in document:
            raise ValueError(f"CITATION.cff lacks required field: {key}")
    metadata = json.loads(zenodo)
    if not isinstance(metadata, dict) or metadata.get("license", "").upper() != "CC-BY-4.0":
        raise ValueError(".zenodo.json must declare CC-BY-4.0")


def validate_urls(files: dict[str, str], domain: str) -> None:
    """Reject private-pipeline and other non-allowlisted GitHub links."""
    allowed = {repository_url(domain), repository_url(domain) + ".git", MASTER_URL, "https://github.com/HolobiomicsLab"}
    for name, text in files.items():
        for match in GITHUB_URL_PATTERN.finditer(text):
            url = match.group(0).rstrip(".,;:)")
            base = next((root for root in sorted(allowed, key=len, reverse=True)
                         if url == root or (root != "https://github.com/HolobiomicsLab" and url.startswith(root + "/"))), None)
            suffix = url[len(base):] if base else url
            if base is None or (suffix and suffix[0] not in "/#?"):
                raise ValueError(f"disallowed GitHub URL in {name}: {url}")


def output_files(options: Options) -> dict[str, str]:
    """Build the complete scaffold in memory before touching the destination."""
    if not DOMAIN_PATTERN.fullmatch(options.domain):
        raise ValueError("domain must be a lowercase slug")
    if not options.title.strip():
        raise ValueError("title must not be empty")
    entry = domain_entry(options.manifest, options.domain, options.stage == "released")
    releases = current_releases(entry, options.stage == "released")
    selected_path = collection_path(options, releases)
    citation = publication_file(options, "CITATION.cff")
    zenodo = publication_file(options, ".zenodo.json")
    validate_publication_files(citation, zenodo)
    licence, licensing = licence_files(options)
    values = {"DOMAIN": options.domain, "REPOSITORY_URL": repository_url(options.domain)}
    files = {
        "README.md": render_readme(options, entry, releases, selected_path),
        "LICENSE": licence,
        "LICENSING.md": licensing,
        "CITATION.cff": citation,
        ".zenodo.json": zenodo,
        ".claude-plugin/marketplace.json": marketplace(options, releases),
        f"collections/{options.domain}/proposals/.gitkeep": "",
        f"staged-collections/{options.domain}/.gitkeep": "",
        f"packs/{options.domain}/.gitkeep": "",
        "receipts/.gitkeep": "",
        ".github/ISSUE_TEMPLATE/propose-paper.md": issue_form(options.domain),
        "CONTRIBUTING.md": substitute((options.templates / "domain-CONTRIBUTING.md").read_text(encoding="utf-8"), values),
        ".github/CODEOWNERS": substitute((options.templates / "domain-CODEOWNERS").read_text(encoding="utf-8"), values),
    }
    for name, text in files.items():
        if PLACEHOLDER_PATTERN.search(text):
            raise ValueError(f"unsubstituted template placeholder in {name}")
    json.loads(files[".claude-plugin/marketplace.json"])
    with tempfile.TemporaryDirectory(prefix="asb-domain-workflows-") as directory:
        workflow_paths = render_domain_ci.render(
            options.manifest, options.domain, options.tooling_sha, options.templates, Path(directory),
            stage=options.stage, collection_path=options.collection_path,
        )
        for path in workflow_paths:
            files[f".github/workflows/{path.name}"] = path.read_text(encoding="utf-8")
    validate_urls(files, options.domain)
    return files


def write_files(out: Path, files: dict[str, str]) -> list[Path]:
    """Write text files and return their paths in deterministic order."""
    paths = []
    for name, text in sorted(files.items()):
        path = out / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        paths.append(path)
    return paths


def scaffold(options: Options) -> list[Path]:
    """Create or replace the scaffold and render its workflows in-process."""
    files = output_files(options)
    if options.out.exists() and any(options.out.iterdir()) and not options.force:
        raise ValueError(f"output directory is not empty; use --force to replace scaffold files: {options.out}")
    if options.dry_run:
        for name in sorted(files):
            print(options.out / name)
        return []
    options.out.mkdir(parents=True, exist_ok=True)
    return write_files(options.out, files)


def main(argv: list[str] | None = None) -> int:
    """Run the scaffold and report each generated file."""
    arguments = parser().parse_args(argv)
    try:
        paths = scaffold(Options(**vars(arguments)))
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError, json.JSONDecodeError) as exc:
        parser().error(str(exc))
    for path in paths:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
