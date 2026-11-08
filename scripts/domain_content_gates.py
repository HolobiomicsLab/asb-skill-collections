"""Run the content gates against one collection in a domain checkout."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from urllib import error, request

import yaml

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

DOI_SAMPLE_SIZE = 10
DOI_TIMEOUT_SECONDS = 10
EDAM_BASE = "http://edamontology.org/"
GATE_NAMES = (
    "Every skill is in every index its collection publishes",
    "Lint skill descriptions",
    "Check derived_from DOIs resolve (sample)",
    "Check EDAM IRIs",
    "Advertised counts",
    "License tiers",
    "Provenance tiers",
    "Tool catalogue",
    "Related skills",
    "Proposals",
    "Release surface",
    "Release gate",
    "Receipt re-verification",
)


@dataclass(frozen=True)
class GateResult:
    """One gate outcome, retained while the rehearsal continues."""

    name: str
    returncode: int


def frontmatter(path: Path) -> dict:
    """Return a skill's parsed frontmatter, or an empty mapping."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    try:
        parsed = yaml.safe_load(text.split("---", 2)[1])
    except (IndexError, yaml.YAMLError):
        return {}
    return parsed if isinstance(parsed, dict) else {}


def validate_relative_path(path: str, *, optional: bool = False) -> None:
    """Reject absolute or parent-traversing content paths."""
    if optional and not path:
        return
    candidate = Path(path)
    if not path or candidate.is_absolute() or ".." in candidate.parts or path.startswith("~"):
        raise ValueError(f"path must be relative to the domain checkout: {path!r}")


def doi_status(doi: str) -> tuple[bool, str]:
    """Classify one DOI resolution without treating bot blocks as orphans."""
    req = request.Request(
        f"https://doi.org/{doi}",
        method="HEAD",
        headers={"User-Agent": "asb-skill-collections/0.1"},
    )
    try:
        with request.urlopen(req, timeout=DOI_TIMEOUT_SECONDS):
            return True, "verified"
    except error.HTTPError as exc:
        if exc.code in (404, 410):
            return False, f"DOI {doi} does not resolve (HTTP {exc.code})"
        return True, f"DOI {doi} reachable, target blocked HEAD (HTTP {exc.code})"
    except (OSError, error.URLError) as exc:
        return True, f"DOI {doi} check inconclusive ({exc})"


def check_dois(collection: Path) -> list[str]:
    """Check the first DOI of up to ten skills, as the legacy gate did."""
    failures = []
    unverified = []
    for path in sorted(collection.rglob("SKILL.md"))[:DOI_SAMPLE_SIZE]:
        derived = frontmatter(path).get("derived_from") or []
        if not derived:
            failures.append(f"{path}: no derived_from DOIs")
            continue
        entry = derived[0]
        doi = entry.get("doi") if isinstance(entry, dict) else entry
        resolved, message = doi_status(str(doi))
        if not resolved:
            failures.append(f"{path}: {message}")
        elif message != "verified":
            unverified.append(message)
    for message in unverified:
        print(f"NOTE: {message}")
    print(f"DOI sample: {len(unverified)} unverified target(s)")
    return failures


def check_edam(collection: Path) -> list[str]:
    """Require canonical EDAM IRIs on every skill in the collection."""
    failures = []
    checked = set()
    for path in sorted(collection.rglob("SKILL.md")):
        metadata = frontmatter(path).get("metadata") or {}
        iris = ([metadata["edam_operation"]] if metadata.get("edam_operation") else [])
        iris.extend(metadata.get("edam_topics") or [])
        for iri in iris:
            checked.add(iri)
            if not isinstance(iri, str) or not iri.startswith(EDAM_BASE):
                failures.append(f"{path}: EDAM IRI {iri} does not start with {EDAM_BASE}")
    print(f"PASS candidate: {len(checked)} unique EDAM IRIs checked")
    return failures


def gate_commands(tooling: Path, content: Path, relative_collection: str) -> list[tuple[str, list[str]]]:
    """Return the static gates in their documented execution order."""
    scripts = tooling / "scripts"
    collection = content / relative_collection
    return [
        (GATE_NAMES[0], [sys.executable, "-m", "scripts.skill_index", "--collections", relative_collection]),
        (GATE_NAMES[1], [sys.executable, str(scripts / "lint_skill_descriptions.py"), str(collection)]),
        (GATE_NAMES[3], [sys.executable, str(Path(__file__).resolve()), "--edam-only", str(collection)]),
        (GATE_NAMES[4], [sys.executable, str(scripts / "check_advertised_counts.py"), "--repo-root", str(content)]),
        (GATE_NAMES[5], [sys.executable, str(scripts / "check_license_tiers.py"), str(collection)]),
        (GATE_NAMES[6], [sys.executable, str(scripts / "check_provenance_tiers.py"), str(collection)]),
        (GATE_NAMES[7], [sys.executable, str(scripts / "check_tools_index.py"), str(collection)]),
        (GATE_NAMES[8], [sys.executable, str(scripts / "check_related_skills.py"), str(collection)]),
        (GATE_NAMES[9], [sys.executable, str(scripts / "check_proposals.py"), str(collection)]),
        (GATE_NAMES[10], [sys.executable, str(scripts / "check_release_surface.py"), str(collection)]),
    ]


def run_step(name: str, command: list[str], cwd: Path, environment: dict[str, str]) -> GateResult:
    """Run one gate and identify it in the log."""
    print(f"\n==> {name}\n$ {' '.join(command)}", flush=True)
    completed = subprocess.run(command, cwd=cwd, env=environment, check=False)
    return GateResult(name, completed.returncode)


def release_arguments(collection: Path, receipts: str, strict: bool, content: Path | None = None) -> list[str]:
    """Build either a read-only receipt check or a temporary-report gate run."""
    command = [sys.executable, str(Path(__file__).with_name("release_gate.py")), str(collection)]
    if receipts:
        if content is None:
            raise ValueError("the content root is required to locate the receipts directory")
        report = content / receipts / "gate_report.json"
        return [*command, "--verify", "--report", str(report)]
    report = Path(tempfile.mkdtemp(prefix="asb-release-gate-")) / "gate_report.json"
    return [*command, "--strict" if strict else "--advisory", "--report", str(report)]


def run_all(options: argparse.Namespace) -> int:
    """Run local static, DOI, release and optional receipt gates."""
    tooling = options.tooling.resolve()
    content = options.content.resolve()
    validate_relative_path(options.collection)
    validate_relative_path(options.receipts, optional=True)
    collection = content / options.collection
    if not collection.is_dir():
        raise ValueError(f"collection is not a directory: {collection}")
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONPATH=str(tooling))
    results = []
    for name, command in gate_commands(tooling, content, options.collection):
        cwd = content if name == GATE_NAMES[0] else tooling
        results.append(run_step(name, command, cwd, environment))
    if not options.offline:
        failures = check_dois(collection)
        if failures:
            raise ValueError("DOI resolution failures:\n" + "\n".join(failures))
    else:
        print("\n==> DOI resolution skipped: --offline")
    mode = "strict" if options.strict else "advisory"
    release = release_arguments(collection, "", options.strict)
    results.append(run_step(GATE_NAMES[11], release, tooling, environment))
    if options.receipts:
        mode = f"{mode}, with receipt verification"
        receipt = release_arguments(collection, options.receipts, options.strict, content)
        results.append(run_step(GATE_NAMES[12], receipt, tooling, environment))
    failed = [result for result in results if result.returncode != 0]
    for result in failed:
        print(f"FAIL: {result.name} exited {result.returncode}")
    print(f"\nDomain content gates completed in {mode} mode: {len(results) - len(failed)} passed, {len(failed)} failed.")
    return 1 if failed else 0


def parser() -> argparse.ArgumentParser:
    """Declare the local runner and its two focused inline-check modes."""
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--tooling", type=Path, default=Path(__file__).resolve().parent.parent)
    result.add_argument("--content", type=Path)
    result.add_argument("--collection")
    result.add_argument("--receipts", default="")
    result.add_argument("--strict", action=argparse.BooleanOptionalAction, default=True)
    result.add_argument("--offline", action="store_true")
    result.add_argument("--edam-only", type=Path)
    result.add_argument("--doi-only", type=Path)
    result.add_argument("--list", action="store_true")
    result.add_argument("--validate-paths", nargs=2, metavar=("COLLECTION", "RECEIPTS"))
    return result


def main(argv: list[str] | None = None) -> int:
    """Run the requested gate set without changing collection content."""
    options = parser().parse_args(argv)
    if options.list:
        print("\n".join(GATE_NAMES))
        return 0
    if options.validate_paths:
        collection, receipts = options.validate_paths
        validate_relative_path(collection)
        validate_relative_path(receipts, optional=True)
        return 0
    if options.edam_only:
        failures = check_edam(options.edam_only)
        print("\n".join(failures))
        return 1 if failures else 0
    if options.doi_only:
        failures = check_dois(options.doi_only)
        print("\n".join(failures))
        return 1 if failures else 0
    if not options.content or not options.collection:
        parser().error("--content and --collection are required for the full gate run")
    return run_all(options)


if __name__ == "__main__":
    raise SystemExit(main())
