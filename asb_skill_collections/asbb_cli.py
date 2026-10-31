"""asbb — utility CLI for asb-skill-collections.

Subcommands:
  search / get                : keyword-search skills/workflows/tools and print a
                                source file (offline, no API key; reads a local
                                checkout). The thin programmatic surface, also
                                exposed over MCP by asb_mcp_server.py.
  verify / doctor             : registry utilities (Phase 1.7 stubs).
  install / uninstall         : materialize packs, or a chosen set of skills
                                (--skills / --skills-file / --query), into
                                NON-Claude runtimes (Codex, Gemini, Copilot,
                                Cursor, Cline, VS Code Copilot, or any dir
                                via --dest).
  fetch                       : download chosen skills from the published
                                repository into a directory; no checkout.

For Claude Code the canonical install path remains the plugin marketplace::

    /plugin install <slug>@HolobiomicsLab/asb-skill-collections

`install` resolves packs from a LOCAL checkout (run from a clone or pass
--repo); the published wheel ships only this package, not the packs.

`registry` was removed on 2026-09-14. It was advertised in `--help` and
documented with two subcommands, `list` and `validate`, while doing neither:
a reader planned around a surface that answered nothing. What reconciles the
registry is `scripts/release_gate.py` (`catalogue_membership`, `layout`,
`unit_closure`), plus `scripts/regen_catalogue.py` and
`scripts/check_advertised_counts.py`.
"""
from __future__ import annotations

import argparse
import sys
from typing import Optional, Sequence

try:  # the installed distribution is the one source of the version
    from importlib.metadata import PackageNotFoundError, version as _dist_version
    __version__ = _dist_version("asb-skill-collections")
except (ImportError, PackageNotFoundError):  # running from a checkout
    __version__ = "0.0.0+source"

_TO_BUILD = "(Phase 1.7 stub — not yet implemented)"
#: What `--help` says of the two stubs, so no reader plans around them.
_STUB_HELP = "(not implemented; use scripts/release_gate.py --strict)"


def _cmd_verify(args: argparse.Namespace) -> int:
    """`asbb verify` — validate a collection / catalogue / marketplace."""
    target = getattr(args, "target", None) or "."
    print(f"asbb verify {target}: {_TO_BUILD}", file=sys.stderr)
    print(f"  use: python scripts/release_gate.py {target} --strict", file=sys.stderr)
    return 1


def _cmd_doctor(args: argparse.Namespace) -> int:
    """`asbb doctor` — health check (DOI resolution, KB reachability, manifest)."""
    # The exit code matters more here than in the others: a health check that
    # reports success having checked nothing is indistinguishable, to any script
    # or CI step, from a healthy system.
    print(f"asbb doctor: {_TO_BUILD}", file=sys.stderr)
    return 1


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


LICENCE_TIERS_URL = (
    "https://github.com/HolobiomicsLab/asb-skill-collections/blob/main/"
    "governance/LICENSE_TIERS.md"
)
SELECTION_FLAGS = ("skills", "skills_file", "query")


def _print_tiers(tiers: dict) -> None:
    """One line per skill with its licence tier, then where the tiers are defined."""
    width = max(len(slug) for slug in tiers)
    for slug, tier in tiers.items():
        print(f"  {slug:<{width}}  {tier}")
    print(f"licence tiers (open, noncommercial, restricted, unknown): {LICENCE_TIERS_URL}")


def _cmd_install(args) -> int:
    from .asbb.targets import list_runtimes
    if getattr(args, "list_runtimes", False):
        print(list_runtimes())
        return 0
    from .asbb.repo import find_repo_root, resolve_pack, list_pack_slugs
    from pathlib import Path
    if not args.runtime and not args.dest:
        print("error: one of --runtime or --dest is required", file=sys.stderr)
        return 1
    selecting = any(getattr(args, flag, None) for flag in SELECTION_FLAGS)
    if bool(args.pack) == selecting:
        both = ", not both" if selecting else ""
        print("error: name a pack, or select skills with --skills, --skills-file or "
              f"--query{both}", file=sys.stderr)
        return 1
    try:
        target = _select_target(args)
    except KeyError:
        print(f"error: unknown runtime {args.runtime!r}\n{list_runtimes()}",
              file=sys.stderr)
        return 1
    try:
        repo = Path(args.repo).resolve() if args.repo else find_repo_root(Path.cwd())
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    if selecting:
        return _install_selection(args, repo, target)
    try:
        pack = resolve_pack(repo, args.pack)
    except KeyError:
        slugs = ", ".join(list_pack_slugs(repo))
        print(f"error: unknown pack {args.pack!r}; valid: {slugs}", file=sys.stderr)
        return 1
    except ValueError as e:
        # resolve_pack refuses a marketplace source that leaves the checkout
        # (absolute, parent-relative, or through a symlink). The refusal was
        # reaching the user as a traceback: install() already converts the same
        # class of refusal into a message and exit 1, and so must this.
        print(f"error: {e}", file=sys.stderr)
        return 1
    written = _run_install(pack, target, args)
    if written is None:
        return 1
    print(f"{_verb(args)} {len(written)} skill(s) from {args.pack} -> {_where(target, args)}")
    return 0


def _verb(args) -> str:
    return "would install" if args.dry_run else "installed"


def _where(target, args):
    opts = _install_opts(args)
    return opts.dest_override or target.dest(opts)


def _run_install(pack, target, args):
    """Install one pack-shaped unit; print a refusal and return None instead of raising."""
    from .asbb.installer import install
    try:
        return install(pack, target, _install_opts(args))
    except (FileExistsError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return None


def _selection(args, repo):
    """Resolve the selection flags against one collection of the checkout."""
    from pathlib import Path
    from . import asb_skill_index as idx
    from .asbb import subset
    from .asbb.repo import list_pack_slugs
    if not args.collection:
        raise subset.SelectionError("a selection needs --collection <slug> or <slug>/vN")
    collection_dir = idx.resolve_collection_dir(args.collection, repo)
    if collection_dir is None:
        raise subset.SelectionError(f"unknown collection {args.collection!r}")
    requested = subset.parse_slugs(args.skills or [])
    if args.skills_file:
        requested += subset.read_slugs_file(Path(args.skills_file))
    if args.query:
        requested += subset.query_slugs(collection_dir, args.query, args.top)
    rows = idx.load_rows(collection_dir, "skills")
    slugs = subset.check_slugs(requested, rows)
    name = args.name or subset.default_name(collection_dir, slugs)
    subset.check_name(name, list_pack_slugs(repo))
    tiers = {row["slug"]: row.get("license_tier") or "unrecorded"
             for row in rows if row.get("slug") in slugs}
    selection = subset.Selection(repo, collection_dir, name, tuple(slugs))
    return selection, {slug: tiers[slug] for slug in slugs}


def _install_selection(args, repo, target) -> int:
    """`asbb install --skills/--skills-file/--query`: derive the subset, install it."""
    import tempfile
    from pathlib import Path
    from . import asb_skill_index as idx
    from .asbb import subset
    try:
        selection, tiers = _selection(args, repo)
    except subset.SelectionError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    collection = idx.collection_id(selection.collection_dir)
    print(f"selection {selection.name}: {len(tiers)} skill(s) from {collection}")
    _print_tiers(tiers)
    with tempfile.TemporaryDirectory(prefix="asbb-selection-") as stage:
        try:
            pack = subset.derive(selection, Path(stage))
        except (OSError, ValueError) as e:
            print(f"error: cannot derive the selection: {e}", file=sys.stderr)
            return 1
        written = _run_install(pack, target, args)
    if written is None:
        return 1
    print(f"{_verb(args)} {selection.name} ({len(tiers)} skill(s), "
          f"{len(written)} advertised entry(ies)) -> {_where(target, args)}")
    place = f"--dest {args.dest}" if args.dest else f"--runtime {args.runtime}"
    print(f"remove with: asbb uninstall {selection.name} {place}")
    return 0


def _cmd_fetch(args) -> int:
    """`asbb fetch`: download chosen leaves from the published repository."""
    from pathlib import Path
    from .asbb import fetch
    from .asbb.subset import parse_slugs
    request = fetch.FetchRequest(args.collection, tuple(parse_slugs(args.slugs)), args.ref)
    dest = Path(args.dest)
    try:
        provenance = fetch.fetch(request, dest)
    except (fetch.FetchError, OSError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    tiers = provenance["license_tiers"]
    print(f"fetched {len(tiers)} skill(s) from {args.collection} at {args.ref} -> {dest}")
    _print_tiers(tiers)
    print(f"provenance: {dest / fetch.PROVENANCE_FILE}")
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
    try:
        removed = uninstall(args.pack, target, opts)
    except (FileExistsError, ValueError) as e:
        # Same contract as _cmd_install above: a refusal is a message and exit 1,
        # never a traceback. The commonest way to reach here is a moved install —
        # the recorded dest_root no longer matches --dest — so name the recovery.
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(f"removed {len(removed)} entry(ies) for {args.pack}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    from .asbb.fetch import DEFAULT_REF
    parser = argparse.ArgumentParser(
        prog="asbb",
        description=(
            "asb-skill-collections CLI: offline search and get, install and "
            "uninstall for non-Claude runtimes (for Claude Code, use /plugin "
            "install), and fetch without a checkout. verify and doctor are not "
            "implemented; use scripts/release_gate.py --strict."
        ),
    )
    parser.add_argument(
        "--version", action="version", version=f"asbb {__version__}"
    )
    sub = parser.add_subparsers(dest="command", metavar="{search,get,verify,doctor,install,uninstall,fetch}")

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

    # asbb verify [target]
    p_verify = sub.add_parser(
        "verify", help=f"Validate a collection / catalogue / marketplace {_STUB_HELP}."
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
        "doctor",
        help=f"Health check: DOI resolution, KB reachability, manifests {_STUB_HELP}.",
    )
    p_doctor.set_defaults(func=_cmd_doctor)

    # asbb install <pack> --runtime ... | --dest DIR
    p_install = sub.add_parser(
        "install",
        help="Install a pack, or a chosen set of skills, into a non-Claude runtime.")
    p_install.add_argument("pack", nargs="?", help="Marketplace pack slug.")
    p_install.add_argument("--skills", action="append",
                           help="Install these skills instead of a pack: slug[,slug...]."
                                " Repeatable.")
    p_install.add_argument("--skills-file", dest="skills_file",
                           help="File with one skill slug per line; # starts a comment.")
    p_install.add_argument("--query",
                           help="Select the --top hits `asbb search` ranks for this text.")
    p_install.add_argument("--top", type=int, default=10,
                           help="How many --query hits to select (default 10).")
    p_install.add_argument("--collection",
                           help="Collection a selection is drawn from: slug or slug/vN.")
    p_install.add_argument("--name",
                           help="Name of the installed selection "
                                "(default <collection>-subset-<8 hex of the slugs>).")
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

    # asbb fetch slug[,slug...] --collection slug/vN --dest DIR [--ref REF]
    p_fetch = sub.add_parser(
        "fetch", help="Download chosen skills from the published repository (no checkout).")
    p_fetch.add_argument("slugs", nargs="+", help="Skill slugs: slug[,slug...].")
    p_fetch.add_argument("--collection", required=True, help="Collection as slug/vN.")
    p_fetch.add_argument("--dest", required=True, help="Directory to write the skills into.")
    p_fetch.add_argument("--ref", default=DEFAULT_REF,
                         help=f"Branch, tag or commit of the repository (default {DEFAULT_REF}).")
    p_fetch.set_defaults(func=_cmd_fetch)

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
