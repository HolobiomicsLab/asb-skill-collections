"""asbb — utility CLI for asb-skill-collections.

Subcommands:
  registry / verify / doctor  — registry utilities (Phase 1.7 stubs).
  install / uninstall         — materialize packs into NON-Claude runtimes
                                (Codex, Gemini, Copilot, Cursor, Cline,
                                VS Code Copilot, or any dir via --dest).

For Claude Code the canonical install path remains the plugin marketplace::

    /plugin install <slug>@HolobiomicsLab/asb-skill-collections

`install` resolves packs from a LOCAL checkout (run from a clone or pass
--repo); the published wheel ships only these scripts, not the packs.
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


def _install_opts(args):
    from pathlib import Path
    from scripts.asbb.targets import InstallOpts
    home = Path(args.home) if args.home else Path.home()
    return InstallOpts(
        home=home,
        project=Path.cwd(),
        user=getattr(args, "user", False),
        copy=getattr(args, "copy", False) or bool(args.dest),
        force=getattr(args, "force", False),
        dry_run=getattr(args, "dry_run", False),
        dest_override=Path(args.dest) if args.dest else None,
    )


def _select_target(args):
    from scripts.asbb.targets import get_target, generic_dest_target
    if args.dest:
        return generic_dest_target()
    return get_target(args.runtime)


def _cmd_install(args) -> int:
    from scripts.asbb.targets import list_runtimes
    if getattr(args, "list_runtimes", False):
        print(list_runtimes())
        return 0
    from scripts.asbb.repo import find_repo_root, resolve_pack, list_pack_slugs
    from scripts.asbb.installer import install
    from pathlib import Path
    if not args.runtime and not args.dest:
        print("error: one of --runtime or --dest is required", file=sys.stderr)
        return 1
    try:
        target = _select_target(args)
    except KeyError:
        from scripts.asbb.targets import list_runtimes
        print(f"error: unknown runtime {args.runtime!r}\n{list_runtimes()}",
              file=sys.stderr)
        return 1
    try:
        repo = Path(args.repo).resolve() if args.repo else find_repo_root(Path.cwd())
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    try:
        pack = resolve_pack(repo, args.pack)
    except KeyError:
        slugs = ", ".join(list_pack_slugs(repo))
        print(f"error: unknown pack {args.pack!r}; valid: {slugs}", file=sys.stderr)
        return 1
    opts = _install_opts(args)
    try:
        written = install(pack, target, opts)
    except (FileExistsError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    where = opts.dest_override or target.dest(opts)
    verb = "would install" if opts.dry_run else "installed"
    print(f"{verb} {len(written)} skill(s) from {args.pack} -> {where}")
    return 0


def _cmd_uninstall(args) -> int:
    from scripts.asbb.targets import get_target, generic_dest_target
    from scripts.asbb.installer import uninstall
    try:
        target = generic_dest_target() if args.dest else get_target(args.runtime)
    except KeyError:
        print(f"error: unknown runtime {args.runtime!r}", file=sys.stderr)
        return 1
    if not args.runtime and not args.dest:
        print("error: one of --runtime or --dest is required", file=sys.stderr)
        return 1
    opts = _install_opts(args)
    removed = uninstall(args.pack, target, opts)
    print(f"removed {len(removed)} entry(ies) for {args.pack}")
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
    sub = parser.add_subparsers(dest="command", metavar="{registry,verify,doctor,install,uninstall}")

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

    # asbb install <pack> --runtime ... | --dest DIR
    p_install = sub.add_parser(
        "install", help="Install a pack into a non-Claude runtime.")
    p_install.add_argument("pack", nargs="?", help="Marketplace pack slug.")
    p_install.add_argument("--runtime", help="Target runtime id (see --list-runtimes).")
    p_install.add_argument("--dest", help="Install into an arbitrary directory (copy).")
    p_install.add_argument("--repo", help="Path to an asb-skill-collections checkout.")
    p_install.add_argument("--user", action="store_true",
                           help="For --runtime claude: use ~/.claude/skills.")
    p_install.add_argument("--copy", action="store_true",
                           help="Copy skill dirs instead of symlinking.")
    p_install.add_argument("--force", action="store_true",
                           help="Overwrite unmanaged files at the destination.")
    p_install.add_argument("--dry-run", action="store_true", dest="dry_run",
                           help="Print intended writes; change nothing.")
    p_install.add_argument("--list-runtimes", action="store_true", dest="list_runtimes",
                           help="List available runtimes and exit.")
    p_install.add_argument("--home", help=argparse.SUPPRESS)  # test hook
    p_install.set_defaults(func=_cmd_install)

    # asbb uninstall <pack> --runtime ... | --dest DIR
    p_uninstall = sub.add_parser(
        "uninstall", help="Remove a previously installed pack from a runtime.")
    p_uninstall.add_argument("pack", help="Marketplace pack slug.")
    p_uninstall.add_argument("--runtime", help="Target runtime id.")
    p_uninstall.add_argument("--dest", help="The directory it was installed into.")
    p_uninstall.add_argument("--repo", help=argparse.SUPPRESS)  # accepted for compat
    p_uninstall.add_argument("--home", help=argparse.SUPPRESS)
    p_uninstall.set_defaults(func=_cmd_uninstall)

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
