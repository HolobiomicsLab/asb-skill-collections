"""asbb — registry utility CLI for asb-skill-collections.

SCOPE (locked, Phase 1.7): this CLI is a REGISTRY UTILITY only. It exposes
exactly three subcommands — ``registry``, ``verify``, and ``doctor``. It is
NOT the install surface: collections are installed via the Claude Code plugin
marketplace::

    /plugin install <slug>-v<N>@HolobiomicsLab/asb-skill-collections

resolved via ``.claude-plugin/marketplace.json``.

These are intentionally thin stubs (Phase 1.7 scaffold). They wire up the
argparse surface so ``asbb``, ``asbb --help``, and each subcommand's ``--help``
work today; the actual registry/verify/doctor logic is to-build.
"""
from __future__ import annotations

import argparse
import sys
from typing import Optional, Sequence

__version__ = "0.1.0"

_TO_BUILD = "(Phase 1.7 stub — not yet implemented)"


def _cmd_registry(args: argparse.Namespace) -> int:
    """`asbb registry` — inspect the published collection registry."""
    action = getattr(args, "registry_action", None) or "list"
    print(f"asbb registry {action}: {_TO_BUILD}")
    print(
        "Install collections via the plugin marketplace, NOT this CLI:\n"
        "  /plugin install <slug>-v<N>@HolobiomicsLab/asb-skill-collections"
    )
    return 0


def _cmd_verify(args: argparse.Namespace) -> int:
    """`asbb verify` — validate a collection / catalogue / marketplace."""
    target = getattr(args, "target", None) or "."
    print(f"asbb verify {target}: {_TO_BUILD}")
    return 0


def _cmd_doctor(args: argparse.Namespace) -> int:
    """`asbb doctor` — health check (DOI resolution, KB reachability, manifest)."""
    print(f"asbb doctor: {_TO_BUILD}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="asbb",
        description=(
            "asb-skill-collections registry utility (registry/verify/doctor only). "
            "NOT the install surface — use /plugin install for that."
        ),
    )
    parser.add_argument(
        "--version", action="version", version=f"asbb {__version__}"
    )
    sub = parser.add_subparsers(dest="command", metavar="{registry,verify,doctor}")

    # asbb registry [list|validate]
    p_registry = sub.add_parser(
        "registry", help="Inspect/validate the published collection registry."
    )
    p_registry.add_argument(
        "registry_action",
        nargs="?",
        choices=["list", "validate"],
        default="list",
        help="Registry action (default: list).",
    )
    p_registry.set_defaults(func=_cmd_registry)

    # asbb verify [target]
    p_verify = sub.add_parser(
        "verify", help="Validate a collection / catalogue / marketplace."
    )
    p_verify.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Path to the collection or repo root to verify (default: .).",
    )
    p_verify.set_defaults(func=_cmd_verify)

    # asbb doctor
    p_doctor = sub.add_parser(
        "doctor", help="Health check: DOI resolution, KB reachability, manifests."
    )
    p_doctor.set_defaults(func=_cmd_doctor)

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return 0
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
