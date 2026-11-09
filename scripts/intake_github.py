#!/usr/bin/env python3
"""Apply one intake receipt to a domain repository through git and gh.

The core (`intake_issue.py`) decides; this adapter only carries the decision
out. Every git and gh call goes through the injected runner, so tests never
touch a real repository or the GitHub API.

Exit 0 when the receipt was applied, 1 when the adapter refuses and prints why.
It never closes an issue, merges a pull request, pushes main or marks a row
included.
"""

from __future__ import annotations

import argparse
from collections.abc import Callable, Sequence
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from dataclasses import dataclass

SCHEMA = "asb-intake-receipt/1"
BRANCH_PATTERN = re.compile(r"^bot/intake-paper-[0-9]+$")
MARKER = "<!-- asb-intake {digest} -->"
RUN = Callable[[Sequence[str], str], tuple[int, str, str]]
ABSOLUTE_PATH = re.compile(r"(?<![\w:/.-])/(?:[^\s\"'`,;:)]+)")


class Refused(Exception):
    """The adapter will not perform the requested action."""


@dataclass(frozen=True)
class Config:
    """Bot identity used for the commit author and committer."""

    bot_name: str
    bot_email: str

    @classmethod
    def from_env(cls, env: dict[str, str]) -> "Config":
        """Read the identity from the environment, refusing a partial one."""
        name = (env.get("ASB_INTAKE_BOT_NAME") or "").strip()
        email = (env.get("ASB_INTAKE_BOT_EMAIL") or "").strip()
        if not name or not email:
            raise Refused(
                "bot identity is not configured: set ASB_INTAKE_BOT_NAME and ASB_INTAKE_BOT_EMAIL"
            )
        return cls(bot_name=name, bot_email=email)


def receipt_digest(receipt: dict) -> str:
    """Return a stable short digest over the receipt's decision.

    The wave path is reduced to its file name so the same decision reached from
    a different checkout directory keeps the same digest.
    """
    decision = dict(receipt)
    if isinstance(decision.get("wave_file"), str):
        decision["wave_file"] = Path(decision["wave_file"]).name
    canonical = json.dumps(decision, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]


def issue_number(receipt: dict) -> int:
    """Return the issue number as a bare integer."""
    value = receipt.get("issue")
    if isinstance(value, dict):
        value = value.get("number")
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise Refused("receipt does not name a positive issue number")
    return value


def scrub(text: str, repo: Path) -> str:
    """Remove local absolute paths from text destined for GitHub."""
    if not isinstance(text, str):
        text = str(text)
    for prefix in {str(repo), str(repo.resolve()), str(Path.home())}:
        text = text.replace(prefix, "<repo>")
    return ABSOLUTE_PATH.sub("<path>", text)


def repo_relative(path_text: str, repo: Path) -> str:
    """Return a repository-relative path or refuse a path outside the checkout."""
    if not isinstance(path_text, str) or not path_text.strip():
        raise Refused("receipt does not name a wave file")
    candidate = Path(path_text)
    if not candidate.is_absolute():
        candidate = repo / candidate
    root = repo.resolve()
    resolved = candidate.resolve()
    try:
        relative = resolved.relative_to(root)
    except ValueError as exc:
        raise Refused(f"wave file is outside the domain checkout: {path_text}") from exc
    return relative.as_posix()


def redact(value, repo: Path):
    """Rebuild a JSON value with local absolute paths removed from every string."""
    if isinstance(value, str):
        return scrub(value, repo)
    if isinstance(value, list):
        return [redact(item, repo) for item in value]
    if isinstance(value, dict):
        return {key: redact(item, repo) for key, item in value.items()}
    return value


def pr_body(receipt: dict, wave_relative: str, repo: Path) -> str:
    """Compose a pull-request body from the receipt without local paths."""
    lines = [
        f"Automated staging for issue #{issue_number(receipt)}. Queued for curator review, not built.",
        "",
        f"- Outcome: `{receipt.get('outcome', '')}`",
        f"- Domain: `{receipt.get('domain', '')}`",
        f"- DOI: `{receipt.get('doi') or 'unresolved'}`",
        f"- Title: {scrub(receipt.get('title') or '', repo)}",
        f"- Repository: `{receipt.get('repository') or 'none'}`",
        f"- Access: `{receipt.get('access') or 'unknown'}`",
        f"- Code licence: `{receipt.get('code_license') or 'unknown'}`",
        f"- Wave row: `{wave_relative}`",
    ]
    duplicate_of = receipt.get("duplicate_of")
    if duplicate_of:
        lines.append(f"- Duplicate of: `{scrub(str(duplicate_of), repo)}`")
    warnings = receipt.get("warnings") or []
    if warnings:
        lines.append("")
        lines.append("Warnings:")
        lines.extend(f"- {scrub(str(warning), repo)}" for warning in warnings)
    lines.extend(
        [
            "",
            "A curator reviews the row, the identity and the licences. This pull request "
            "only stages a proposal; it does not include the paper in a released collection.",
        ]
    )
    return "\n".join(lines) + "\n"


class Adapter:
    """Apply a receipt with a runner that returns (code, stdout, stderr)."""

    def __init__(self, run: RUN, repo: Path, domain: str, config: Config,
                 dry_run: bool = False, out: Callable[[str], None] = print) -> None:
        self.run = run
        self.repo = Path(repo)
        self.domain = domain
        self.config = config
        self.dry_run = dry_run
        self.out = out
        self.calls: list[tuple[list[str], str]] = []

    def call(self, argv: Sequence[str], cwd: Path | None = None) -> tuple[int, str, str]:
        """Run one command, or print it in dry-run mode."""
        command = [str(part) for part in argv]
        workdir = str(cwd or self.repo)
        if self.dry_run:
            self.out(self.format(command, workdir))
            return 0, "", ""
        self.calls.append((command, workdir))
        return self.run(command, workdir)

    def format(self, command: Sequence[str], workdir: str) -> str:
        """Render a command for dry-run output without shell quoting tricks."""
        return f"[{workdir}] " + json.dumps(list(command), ensure_ascii=False)

    def check(self, argv: Sequence[str], cwd: Path | None = None) -> str:
        """Run a command and refuse when it fails."""
        code, stdout, stderr = self.call(argv, cwd)
        if code != 0:
            raise Refused(f"command failed ({code}): {' '.join(map(str, argv))}: {stderr.strip()}")
        return stdout

    def apply(self, receipt: dict) -> None:
        """Dispatch on the receipt outcome."""
        if receipt.get("schema") != SCHEMA:
            raise Refused(f"unsupported receipt schema: {receipt.get('schema')!r}")
        if receipt.get("domain") != self.domain:
            raise Refused(
                f"receipt domain {receipt.get('domain')!r} does not match --domain {self.domain!r}"
            )
        outcome = receipt.get("outcome")
        number = issue_number(receipt)
        if outcome == "staged":
            self.apply_staged(receipt, number)
        elif outcome in {"blocked", "duplicate"}:
            self.apply_nonstaged(receipt, number, outcome)
        else:
            raise Refused(f"unsupported receipt outcome: {outcome!r}")

    def apply_staged(self, receipt: dict, number: int) -> None:
        """Create or rewrite the issue branch, then open or update its pull request."""
        wave_relative = repo_relative(receipt.get("wave_file"), self.repo)
        wave_path = self.repo / wave_relative
        if not self.dry_run and not wave_path.is_file():
            raise Refused(f"staged wave file is missing: {wave_relative}")
        branch = f"bot/intake-paper-{number}"
        if branch == "main" or not BRANCH_PATTERN.fullmatch(branch):
            raise Refused(f"refusing to write branch {branch!r}")
        self.git(["fetch", "origin", "main"])
        self.git(["checkout", "-B", branch, "origin/main"])
        receipt_relative = self.write_receipt_copy(receipt, number)
        staged = [wave_relative] + ([receipt_relative] if receipt_relative else [])
        self.git(["add", "--", *staged])
        code, _, stderr = self.call(
            [
                "git",
                "-c", f"user.name={self.config.bot_name}",
                "-c", f"user.email={self.config.bot_email}",
                "commit",
                f"--author={self.config.bot_name} <{self.config.bot_email}>",
                "-m", f"Intake: issue #{number} staged for curator review",
            ]
        )
        if code != 0 and self.dry_run:
            raise Refused(f"commit failed ({code}): {stderr.strip()}")
        unchanged = code != 0 and (
            "nothing to commit" in stderr or "no changes added" in stderr
        )
        if not unchanged:
            code, _, stderr = self.call(["git", "push", "--force", "origin", branch])
            if code != 0 and not self.dry_run:
                raise Refused(
                    f"push failed ({code}); the local branch {branch} is left in place: {stderr.strip()}"
                )
        title = f"Intake: {scrub(receipt.get('title') or 'paper', self.repo)} (issue #{number})"
        body = pr_body(receipt, wave_relative, self.repo)
        existing = self.open_pr_number(branch)
        if existing is None:
            self.check(
                ["gh", "pr", "create", "--base", "main", "--head", branch,
                 "--title", title, "--body", body]
            )
        else:
            self.check(
                ["gh", "pr", "edit", str(existing), "--title", title, "--body", body]
            )
        self.post_comment_once(receipt, number)
        self.apply_labels(receipt, number)

    def apply_nonstaged(self, receipt: dict, number: int, outcome: str) -> None:
        """Comment and label without creating a branch."""
        self.post_comment_once(receipt, number)
        add = list(receipt.get("labels_add") or [])
        if outcome == "duplicate" and "duplicate" not in add:
            add.append("duplicate")
        self.apply_labels(dict(receipt, labels_add=add), number)

    def write_receipt_copy(self, receipt: dict, number: int) -> str:
        """Write a receipt copy only when the receipt names one."""
        named = receipt.get("receipt_copy")
        if named is True:
            relative = f"collections/{self.domain}/proposals/receipts/intake-{number}.json"
        elif isinstance(named, str) and named.strip():
            relative = repo_relative(named, self.repo)
        else:
            return ""
        target = self.repo / relative
        if not self.dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            copy = redact(receipt, self.repo)
            copy["wave_file"] = repo_relative(receipt.get("wave_file"), self.repo)
            target.write_text(json.dumps(copy, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return relative

    def git(self, args: Sequence[str]) -> str:
        """Run one git command in the checkout."""
        return self.check(["git", *args])

    def open_pr_number(self, branch: str) -> int | None:
        """Return the open pull request number for this branch, if any."""
        stdout = self.check(
            ["gh", "pr", "list", "--head", branch, "--state", "open", "--json", "number"]
        )
        try:
            rows = json.loads(stdout or "[]")
        except json.JSONDecodeError as exc:
            raise Refused(f"gh pr list returned unreadable JSON: {exc}") from exc
        if not rows:
            return None
        return int(rows[0]["number"])

    def comment_exists(self, number: int, digest: str) -> bool:
        """Return whether the issue already carries this receipt's marker."""
        if self.dry_run:
            self.out(self.format(
                ["gh", "issue", "view", str(number), "--json", "comments"], str(self.repo)
            ))
            return False
        stdout = self.check(["gh", "issue", "view", str(number), "--json", "comments"])
        try:
            document = json.loads(stdout or "{}")
        except json.JSONDecodeError as exc:
            raise Refused(f"gh issue view returned unreadable JSON: {exc}") from exc
        marker = MARKER.format(digest=digest)
        return any(marker in (comment.get("body") or "") for comment in document.get("comments", []))

    def post_comment_once(self, receipt: dict, number: int) -> None:
        """Post the core's comment unless this digest was already posted."""
        digest = receipt_digest(receipt)
        if self.comment_exists(number, digest):
            return
        comment = receipt.get("comment_markdown") or ""
        if not isinstance(comment, str) or not comment.strip():
            raise Refused("receipt has no comment_markdown to post")
        body = scrub(comment, self.repo).rstrip() + "\n\n" + MARKER.format(digest=digest) + "\n"
        self.check(["gh", "issue", "comment", str(number), "--body", body])

    def apply_labels(self, receipt: dict, number: int) -> None:
        """Apply the receipt's label additions and removals in one call each."""
        add = [str(label) for label in receipt.get("labels_add") or [] if str(label).strip()]
        remove = [str(label) for label in receipt.get("labels_remove") or [] if str(label).strip()]
        if not add and not remove:
            return
        argv = ["gh", "issue", "edit", str(number)]
        if add:
            argv.extend(["--add-label", ",".join(add)])
        if remove:
            argv.extend(["--remove-label", ",".join(remove)])
        self.check(argv)


def load_receipt(path: Path) -> dict:
    """Read the receipt as a JSON object."""
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise Refused(f"cannot read receipt: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise Refused(f"receipt is not valid JSON: {exc}") from exc
    if not isinstance(document, dict):
        raise Refused("receipt must be a JSON object")
    return document


def parser() -> argparse.ArgumentParser:
    """Declare the receipt, checkout, domain and dry-run options."""
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--receipt", type=Path, required=True)
    result.add_argument("--repo", type=Path, default=Path("."))
    result.add_argument("--domain", required=True)
    result.add_argument("--dry-run", action="store_true")
    return result


def main(argv: list[str] | None = None, env: dict[str, str] | None = None,
         run: RUN | None = None) -> int:
    """Apply one receipt and report refusals on stderr."""
    options = parser().parse_args(argv)
    try:
        config = Config.from_env(dict(os.environ) if env is None else env)
        receipt = load_receipt(options.receipt)
        Adapter(run=run or subprocess_run, repo=options.repo, domain=options.domain,
                config=config, dry_run=options.dry_run).apply(receipt)
    except Refused as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 1
    return 0


def subprocess_run(argv: Sequence[str], cwd: str) -> tuple[int, str, str]:
    """Run one command for real; the default runner outside tests."""
    import subprocess

    completed = subprocess.run(list(argv), cwd=cwd, text=True, capture_output=True, check=False)
    return completed.returncode, completed.stdout, completed.stderr


if __name__ == "__main__":
    raise SystemExit(main())
