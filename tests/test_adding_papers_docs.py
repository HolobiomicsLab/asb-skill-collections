"""Keep the local pipeline commands in docs/adding-papers.md copy-paste safe."""

from __future__ import annotations

import ast
import pathlib
import re
import shlex


REPO = pathlib.Path(__file__).resolve().parent.parent
DOC = REPO / "docs" / "adding-papers.md"
CONTENT_DOCS = (
    DOC,
    REPO / "docs" / "CONTRIBUTION_LOOP.md",
    REPO / "docs" / "NEXT_WAVE.md",
)
FENCE = re.compile(r"^```(?:bash|sh)\n(.*?)^```", re.MULTILINE | re.DOTALL)
LOCAL_SCRIPT = re.compile(r"(?<![/\w.-])(scripts/[A-Za-z0-9_./-]+\.py)\b")
UNQUALIFIED_CONTENT_PATH = re.compile(r"(?<!<domain checkout>/)collections/<domain>/")


def _documented_local_commands() -> list[tuple[str, str]]:
    commands = []
    for block in FENCE.findall(DOC.read_text(encoding="utf-8")):
        for command in block.replace("\\\n", " ").splitlines():
            match = LOCAL_SCRIPT.search(command)
            if match:
                commands.append((match.group(1), command))
    return commands


def _argparse_flags(script: pathlib.Path) -> set[str]:
    tree = ast.parse(script.read_text(encoding="utf-8"), filename=str(script))
    flags: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        if node.func.attr != "add_argument":
            continue
        for argument in node.args:
            if isinstance(argument, ast.Constant) and isinstance(argument.value, str):
                if argument.value.startswith("--"):
                    flags.add(argument.value)
    return flags


def test_documented_local_pipeline_scripts_and_flags_exist():
    commands = _documented_local_commands()
    assert {script for script, _ in commands} == {
        "scripts/check_proposals.py",
        "scripts/promote_proposals.py",
        "scripts/assemble_candidate.py",
        "scripts/land_candidate.py",
    }
    failures = []
    for relative, command in commands:
        script = REPO / relative
        if not script.is_file():
            failures.append(f"missing {relative}")
            continue
        accepted = _argparse_flags(script)
        quoted = {token.split("=", 1)[0] for token in shlex.split(command)
                  if token.startswith("--")}
        unknown = sorted(quoted - accepted)
        if unknown:
            failures.append(f"{relative}: {unknown}")
    assert not failures, "documented argparse flags drifted:\n  " + "\n  ".join(failures)


def test_documented_version_gap_matches_both_candidate_parsers():
    from scripts import assemble_candidate, land_candidate

    text = DOC.read_text(encoding="utf-8")
    assert "They reject a minor directory such as `v3.1`" in text
    assert assemble_candidate.VERSION_RE.fullmatch("v3")
    assert land_candidate.VERSION_PATTERN.fullmatch("v3")
    assert not assemble_candidate.VERSION_RE.fullmatch("v3.1")
    assert not land_candidate.VERSION_PATTERN.fullmatch("v3.1")


def test_generic_content_paths_are_domain_checkout_relative():
    """The literal prefix <domain checkout>/ is the ownership marker."""
    offenders = []
    for document in CONTENT_DOCS:
        for line_number, line in enumerate(
            document.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if UNQUALIFIED_CONTENT_PATH.search(line):
                offenders.append(f"{document.relative_to(REPO)}:{line_number}")
    assert not offenders, (
        "generic content paths must start at the domain checkout: "
        + ", ".join(offenders)
    )
