"""asbb — utility CLI for asb-skill-collections.

Subcommands:
  search / get                — keyword-search skills/workflows/tools and print a
                                source file (offline, no API key; reads a local
                                checkout). The thin programmatic surface, also
                                exposed over MCP by asb_mcp_server.py.
  registry / verify / doctor  — registry utilities (Phase 1.7 stubs).
  install / uninstall         — materialize packs into NON-Claude runtimes
                                (Codex, Gemini, Copilot, Cursor, Cline,
                                VS Code Copilot, or any dir via --dest).

For Claude Code the canonical install path remains the plugin marketplace::

    /plugin install <slug>@HolobiomicsLab/asb-skill-collections

`install` resolves packs from a LOCAL checkout (run from a clone or pass
--repo); the published wheel ships only this package, not the packs.
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


def _cmd_search(args) -> int:
    """`asbb search` — keyword-search skills/workflows/tools in a local checkout."""
    import json
    from . import asb_skill_index as idx
    cols = idx.discover_collections(args.repo)
    if not cols:
        print("error: no collections found. Run from a checkout or set "
              "ASB_COLLECTIONS_ROOT / --repo.", file=sys.stderr)
        return 1
    if getattr(args, "list_collections", False):
        for c in cols:
            print(f"{c['id']}\t{c.get('skills_count') or '?'} skills"
                  f"\t{'+workflows' if c['has_workflows'] else ''}")
        return 0
    results = idx.search(args.collection, args.target, args.query,
                         technique=args.technique, k=args.k, root=args.repo)
    print(json.dumps({"target": args.target, "query": args.query,
                      "mode": "keyword", "results": results}, indent=2))
    return 0


def _cmd_get(args) -> int:
    """`asbb get` — print a skill/workflow/tool's source file."""
    from . import asb_skill_index as idx
    text = idx.get_item_text(args.collection, args.target, args.slug, root=args.repo)
    if text is None:
        print(f"error: {args.target[:-1]} {args.slug!r} not found in "
              f"{args.collection!r}", file=sys.stderr)
        return 1
    print(text)
    return 0


def _install_opts(args):
    from pathlib import Path
    from .asbb.targets import InstallOpts
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
    from .asbb.targets import get_target, generic_dest_target
    if args.dest:
        return generic_dest_target()
    return get_target(args.runtime)


def _cmd_install(args) -> int:
    from .asbb.targets import list_runtimes
    if getattr(args, "list_runtimes", False):
        print(list_runtimes())
        return 0
    from .asbb.repo import find_repo_root, resolve_pack, list_pack_slugs
    from .asbb.installer import install
    from pathlib import Path
    if not args.runtime and not args.dest:
        print("error: one of --runtime or --dest is required", file=sys.stderr)
        return 1
    try:
        target = _select_target(args)
    except KeyError:
        from .asbb.targets import list_runtimes
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
    from .asbb.targets import get_target, generic_dest_target
    from .asbb.installer import uninstall
    if not args.runtime and not args.dest:
        print("error: one of --runtime or --dest is required", file=sys.stderr)
        return 1
    try:
        target = generic_dest_target() if args.dest else get_target(args.runtime)
    except KeyError:
        print(f"error: unknown runtime {args.runtime!r}", file=sys.stderr)
        return 1
    opts = _install_opts(args)
    removed = uninstall(args.pack, target, opts)
    print(f"removed {len(removed)} entry(ies) for {args.pack}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="asbb",
        description=(
            "asb-skill-collections CLI: registry/verify/doctor utilities + "
            "install/uninstall for non-Claude runtimes "
            "(for Claude Code, use /plugin install)."
        ),
    )
    parser.add_argument(
        "--version", action="version", version=f"asbb {__version__}"
    )
    sub = parser.add_subparsers(dest="command", metavar="{search,get,registry,verify,doctor,install,uninstall}")

    # asbb search <query> [--collection ...] [--target skills|workflows|tools]
    p_search = sub.add_parser("search", help="Keyword-search skills/workflows/tools (offline, no key).")
    p_search.add_argument("query", nargs="?", default="", help="Free-text query.")
    p_search.add_argument("--collection", help="slug or slug/vN (default: all collections).")
    p_search.add_argument("--target", choices=["skills", "workflows", "tools"], default="skills")
    p_search.add_argument("--technique", help="Filter by technique tag (e.g. LC-MS).")
    p_search.add_argument("--k", type=int, default=10, help="Max results (default 10).")
    p_search.add_argument("--repo", help="Path to a checkout (else ASB_COLLECTIONS_ROOT / CWD).")
    p_search.add_argument("--list-collections", action="store_true", dest="list_collections",
                          help="List discovered collections and exit.")
    p_search.set_defaults(func=_cmd_search)

    # asbb get <slug> --collection slug/vN [--target ...]
    p_get = sub.add_parser("get", help="Print a skill/workflow/tool's source file.")
    p_get.add_argument("slug", help="Item slug.")
    p_get.add_argument("--collection", required=True, help="slug or slug/vN.")
    p_get.add_argument("--target", choices=["skills", "workflows", "tools"], default="skills")
    p_get.add_argument("--repo", help="Path to a checkout (else ASB_COLLECTIONS_ROOT / CWD).")
    p_get.set_defaults(func=_cmd_get)

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
