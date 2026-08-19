"""Registry of install targets: skill-native dirs and rules-format adapters."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional


@dataclass
class InstallOpts:
    home: Path
    project: Path
    user: bool = False
    copy: bool = False
    force: bool = False
    dry_run: bool = False
    dest_override: Optional[Path] = None


@dataclass(frozen=True)
class Target:
    id: str
    kind: str  # "skill" or "rules"
    dest: Callable[[InstallOpts], Path]
    help: str
    filename: Optional[Callable[[str], str]] = None
    render: Optional[Callable[[dict, str, str], str]] = None


def _skill_dir(sub: str) -> Callable[[InstallOpts], Path]:
    return lambda o: o.home / sub / "skills"


def _claude_dest(o: InstallOpts) -> Path:
    base = o.home if o.user else o.project
    return base / ".claude" / "skills"


# --- rules adapters ------------------------------------------------------

def _render_cursor(fm: dict, body: str, name: str) -> str:
    desc = fm.get("description", "")
    return (
        "---\n"
        f"description: {desc}\n"
        "globs:\n"
        "alwaysApply: false\n"
        "---\n\n"
        f"{body}"
    )


def _render_vscode(fm: dict, body: str, name: str) -> str:
    return (
        "---\n"
        "applyTo: '**'\n"
        "---\n\n"
        f"{body}"
    )


def _render_cline(fm: dict, body: str, name: str) -> str:
    desc = fm.get("description", "")
    header = f"# {name}\n\n" if not body.lstrip().startswith("#") else ""
    note = f"> {desc}\n\n" if desc else ""
    return f"{header}{note}{body}"


TARGETS: dict[str, Target] = {
    "agents": Target("agents", "skill", _skill_dir(".agents"),
                     "Codex + Copilot CLI + Gemini CLI (shared ~/.agents/skills)"),
    "codex": Target("codex", "skill", _skill_dir(".codex"), "Codex (~/.codex/skills)"),
    "copilot": Target("copilot", "skill", _skill_dir(".copilot"),
                      "Copilot CLI (~/.copilot/skills)"),
    "gemini": Target("gemini", "skill", _skill_dir(".gemini"),
                     "Gemini CLI (~/.gemini/skills)"),
    "claude": Target("claude", "skill", _claude_dest,
                     "Claude Code project ./.claude/skills (or ~/.claude/skills with --user)"),
    "cursor": Target("cursor", "rules", lambda o: o.project / ".cursor" / "rules",
                     "Cursor project rules (./.cursor/rules/*.mdc)",
                     filename=lambda n: f"{n}.mdc", render=_render_cursor),
    "cline": Target("cline", "rules", lambda o: o.project / ".clinerules",
                    "Cline project rules (./.clinerules/*.md)",
                    filename=lambda n: f"{n}.md", render=_render_cline),
    "vscode-copilot": Target(
        "vscode-copilot", "rules", lambda o: o.project / ".github" / "instructions",
        "VS Code Copilot instructions (./.github/instructions/*.instructions.md)",
        filename=lambda n: f"{n}.instructions.md", render=_render_vscode),
}


def get_target(runtime: str) -> Target:
    return TARGETS[runtime]


def generic_dest_target() -> Target:
    return Target("dest", "skill", lambda o: Path(o.dest_override),
                  "Generic directory (--dest)")


def list_runtimes() -> str:
    lines = ["Available runtimes:"]
    for rid, t in TARGETS.items():
        lines.append(f"  {rid:<16} [{t.kind}]  {t.help}")
    lines.append(f"  {'--dest DIR':<16} [skill]  any directory")
    return "\n".join(lines)
