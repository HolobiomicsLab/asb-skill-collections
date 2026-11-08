"""Report Crossref retractions without changing a collection or calling GitHub."""

from __future__ import annotations

import argparse
import datetime as dt
import functools
import json
import pathlib
import shlex
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable, Iterable

import yaml

CROSSREF_WORK_URL = "https://api.crossref.org/works/{doi}"
DEFAULT_STATUSES = ("included", "accepted")
DEFAULT_USER_AGENT = "asb-retraction-watch/1.0"
ISSUE_MARKER = "<!-- asb-retraction-watch: {collection}/{version} -->"
REQUEST_TIMEOUT_S = 20
RETRYABLE_STATUS = (429, 500, 502, 503, 504)
MAX_ATTEMPTS = 4
BACKOFF_BASE_S = 2.0
SOFT_CAP_DAYS = 30


def retry_delay(attempt: int, retry_after: str | None) -> float:
    """Return the server's delay or exponential backoff for one attempt."""
    if retry_after and retry_after.strip().isdigit():
        return float(retry_after.strip())
    return BACKOFF_BASE_S * (2 ** (attempt - 1))


def default_fetch_json(url: str, user_agent: str = DEFAULT_USER_AGENT) -> dict:
    """Fetch one Crossref response with a descriptive contact User-Agent."""
    request = urllib.request.Request(
        url, headers={"User-Agent": user_agent, "Accept": "application/json"}
    )
    with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_S) as response:
        return json.loads(response.read().decode("utf-8"))


def collection_key(
    path: pathlib.Path, root: pathlib.Path, document: dict
) -> tuple[str, str]:
    """Derive a stable domain/version key, preferring declared metadata."""
    collection = str(document.get("collection") or path.relative_to(root).parts[0])
    version = str(document.get("version") or path.parent.name)
    if not version.startswith("v"):
        version = f"v{version}"
    return collection, version


def corpus_paths(
    collections: pathlib.Path, staged: pathlib.Path
) -> Iterable[tuple[pathlib.Path, pathlib.Path]]:
    """Yield each corpus with its root, including missing roots as empty."""
    for root in (collections, staged):
        for path in sorted(root.rglob("corpus.yaml")) if root.is_dir() else []:
            yield root, path


def crossref_work_url(doi: str) -> str:
    """Quote a DOI as one URL path segment."""
    return CROSSREF_WORK_URL.format(doi=urllib.parse.quote(doi, safe=""))


def error_record(doi: str, title: str, exc: Exception) -> dict:
    """Preserve a registry failure so it cannot become a clean verdict."""
    is_timeout = (
        isinstance(exc, TimeoutError)
        or isinstance(exc, urllib.error.URLError)
        and isinstance(exc.reason, TimeoutError)
    )
    return {
        "doi": doi,
        "title": title,
        "kind": "http"
        if isinstance(exc, urllib.error.HTTPError)
        else "timeout"
        if is_timeout
        else "request",
        "status": exc.code if isinstance(exc, urllib.error.HTTPError) else None,
        "detail": str(exc),
    }


def fetch_with_retries(
    doi: str, fetch_json: Callable, sleep: Callable[[float], None]
) -> dict:
    """Fetch a work with bounded retries for transient service responses."""
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            return fetch_json(crossref_work_url(doi))
        except urllib.error.HTTPError as exc:
            if exc.code not in RETRYABLE_STATUS or attempt == MAX_ATTEMPTS:
                raise
            sleep(retry_delay(attempt, exc.headers.get("Retry-After")))
        except (urllib.error.URLError, TimeoutError):
            if attempt == MAX_ATTEMPTS:
                raise
            sleep(retry_delay(attempt, None))
    raise AssertionError("retry loop returned without a response")


def format_date(entry: dict) -> str | None:
    """Format the partial ISO date carried by a Crossref update entry."""
    parts = (
        entry.get("updated") or entry.get("published") or entry.get("created") or {}
    ).get("date-parts") or []
    if not parts or not parts[0]:
        return None
    values = list(parts[0]) + [1, 1]
    return f"{values[0]:04d}-{values[1]:02d}-{values[2]:02d}"


def retraction_records(message: dict, doi: str, title: str) -> list[dict]:
    """Extract both Crossref retraction relation representations."""
    hits = []
    for entry in message.get("update-to") or []:
        if str(entry.get("type") or "").lower() != "retraction":
            continue
        hits.append(
            {
                "doi": doi,
                "title": title,
                "retraction_doi": entry.get("DOI") or entry.get("doi"),
                "retraction_date": format_date(entry),
                "source": "update-to",
            }
        )
    for entry in message.get("relation", {}).get("is-retracted-by") or []:
        notice_doi = entry.get("id") if isinstance(entry, dict) else str(entry)
        if isinstance(entry, dict) and entry.get("id-type") not in (None, "doi"):
            continue
        hits.append(
            {
                "doi": doi,
                "title": title,
                "retraction_doi": notice_doi,
                "retraction_date": format_date(entry)
                if isinstance(entry, dict)
                else None,
                "source": "relation.is-retracted-by",
            }
        )
    return hits


def check_collections(
    collections: pathlib.Path,
    staged: pathlib.Path,
    *,
    fetch_json=default_fetch_json,
    sleep=time.sleep,
    statuses=DEFAULT_STATUSES,
    dry_run: bool = False,
) -> dict:
    """Check eligible corpus rows and return per-version findings and errors."""
    selected_statuses = {status.lower() for status in statuses}
    rows = []
    for root, path in corpus_paths(collections, staged):
        document = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        collection, version = collection_key(path, root, document)
        row = {
            "collection": collection,
            "version": version,
            "corpus": str(path),
            "checked": [],
            "retracted": [],
            "errors": [],
            "skipped": [],
            "pending": [],
        }
        for paper in document.get("papers") or []:
            if str(paper.get("status") or "").lower() not in selected_statuses:
                continue
            doi = str(paper.get("doi") or "").strip()
            title = str(paper.get("title") or paper.get("name") or "")
            if not doi:
                row["skipped"].append(
                    {"name": paper.get("name"), "title": title, "reason": "no_doi"}
                )
                continue
            if dry_run:
                row["pending"].append(doi)
                continue
            try:
                payload = fetch_with_retries(doi, fetch_json, sleep)
                message = payload.get("message") if isinstance(payload, dict) else None
                if not isinstance(message, dict):
                    raise ValueError("Crossref response has no message object")
            except (urllib.error.URLError, TimeoutError, ValueError, OSError) as exc:
                row["errors"].append(error_record(doi, title, exc))
                continue
            row["checked"].append(doi)
            row["retracted"].extend(retraction_records(message, doi, title))
        rows.append(row)
    return finish_report(rows)


def finish_report(collections: list[dict]) -> dict:
    """Calculate the outcome, with incomplete answers taking precedence."""
    has_errors = any(row["errors"] for row in collections)
    has_retractions = any(row["retracted"] for row in collections)
    return {
        "collections": collections,
        "exit_code": 2 if has_errors else 1 if has_retractions else 0,
    }


def render_issue(
    collection: str, version: str, retracted: list[dict]
) -> tuple[str, str]:
    """Render a stable, human-reviewable issue without editing any content."""
    key = f"{collection}/{version}"
    title = f"[retraction-watch] {len(retracted)} retracted paper(s) in {key}"
    lines = [
        ISSUE_MARKER.format(collection=collection, version=version),
        f"Crossref reports {len(retracted)} retracted paper(s) in `{key}`.",
        "",
        "| Source DOI | Retraction DOI | Date | Title |",
        "|---|---|---|---|",
    ]
    for hit in retracted:
        lines.append(
            f"| `{hit['doi']}` | `{hit.get('retraction_doi') or 'not supplied'}` | "
            f"{hit.get('retraction_date') or 'not supplied'} | {hit.get('title') or ''} |"
        )
    lines.extend(
        [
            "",
            "A retraction hit requires a reviewed release action, never a silent removal or rewrite.",
        ]
    )
    return title, "\n".join(lines)


def marker_for(collection: str, version: str) -> str:
    """Return the exact issue identity marker."""
    return ISSUE_MARKER.format(collection=collection, version=version)


def issue_age_days(issue: dict, reference_date: dt.datetime) -> int | None:
    """Return age for a gh-created-at value, or None when it is invalid."""
    try:
        created = dt.datetime.fromisoformat(issue["created_at"].replace("Z", "+00:00"))
        return (reference_date - created).days
    except (KeyError, TypeError, ValueError):
        return None


def issue_command(action: str, title: str, body: str, number: int | None = None) -> str:
    """Print a shell-safe gh command for the workflow to execute."""
    prefix = ["gh", "issue", action] + ([str(number)] if number is not None else [])
    options = ["--title", title] if action == "create" else []
    options += ["--body", body] + (
        ["--label", "retraction-watch"] if action == "create" else []
    )
    return shlex.join(prefix + options)


def recommend_issue_commands(
    collection: str,
    version: str,
    retracted: list[dict],
    existing_issues: list[dict],
    reference_date: dt.datetime,
) -> list[str]:
    """Recommend one issue creation or a comment within the 30-day soft cap."""
    if not retracted:
        return []
    title, body = render_issue(collection, version, retracted)
    marker = marker_for(collection, version)
    for issue in existing_issues:
        if marker not in str(issue.get("body") or ""):
            continue
        age = issue_age_days(issue, reference_date)
        if (
            age is not None
            and 0 <= age < SOFT_CAP_DAYS
            and issue.get("number") is not None
        ):
            return [
                issue_command(
                    "comment",
                    title,
                    f"Monthly retraction sweep:\n\n{body}",
                    issue["number"],
                )
            ]
        break
    return [issue_command("create", title, body)]


def parse_reference_date(value: str) -> dt.datetime:
    """Parse an ISO reference date and assume UTC when no offset is supplied."""
    reference = dt.datetime.fromisoformat(value)
    return (
        reference.replace(tzinfo=dt.timezone.utc)
        if reference.tzinfo is None
        else reference
    )


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--collections", type=pathlib.Path, required=True)
    parser.add_argument("--staged", type=pathlib.Path, required=True)
    parser.add_argument("--statuses", default=",".join(DEFAULT_STATUSES))
    parser.add_argument("--user-agent-mailto")
    parser.add_argument("--report", type=pathlib.Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--existing-issues", type=pathlib.Path)
    parser.add_argument("--reference-date", help=argparse.SUPPRESS)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the monitor and print only machine-readable output and gh recommendations."""
    args = build_parser().parse_args(argv)
    user_agent = DEFAULT_USER_AGENT + (
        f" (mailto:{args.user_agent_mailto})" if args.user_agent_mailto else ""
    )
    fetch_json = functools.partial(default_fetch_json, user_agent=user_agent)
    report = check_collections(
        args.collections,
        args.staged,
        fetch_json=fetch_json,
        statuses=args.statuses.split(","),
        dry_run=args.dry_run,
    )
    commands = []
    if report["exit_code"] == 1:
        issues = (
            json.loads(args.existing_issues.read_text(encoding="utf-8"))
            if args.existing_issues
            else []
        )
        reference_date = (
            parse_reference_date(args.reference_date)
            if args.reference_date
            else dt.datetime.now(dt.timezone.utc)
        )
        commands = [
            command
            for row in report["collections"]
            for command in recommend_issue_commands(
                row["collection"],
                row["version"],
                row["retracted"],
                issues,
                reference_date,
            )
        ]
    if commands:
        print("\n".join(commands))
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())
