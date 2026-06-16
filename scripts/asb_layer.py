#!/usr/bin/env python
"""Select / materialize a single install-or-release LAYER from a collection.

Reads ``<collection>/MANIFEST.yaml`` (written by promote_benchmark_layer.py) and
resolves a layer's effective include-globs (following ``extends``), then either
lists the matching files or copies them into an output dir — proving the
"install only skills / skills+bundle / benchmark-only / full" capability.

Usage:
  asb_layer.py <collection-dir> --layer skills|bundle|benchmark|full --list
  asb_layer.py <collection-dir> --layer benchmark --out /tmp/epi-benchmark
"""
from __future__ import annotations
import argparse, shutil
from pathlib import Path

import yaml


def resolve_includes(manifest: dict, layer: str, _seen=None) -> list[str]:
    _seen = _seen or set()
    if layer in _seen:
        return []
    _seen.add(layer)
    spec = manifest["layers"].get(layer)
    if spec is None:
        raise SystemExit(f"ERROR: layer '{layer}' not in manifest (have: {list(manifest['layers'])})")
    inc = list(spec.get("include", []))
    for parent in spec.get("extends", []) or []:
        inc = resolve_includes(manifest, parent, _seen) + inc
    # dedupe, preserve order
    seen, out = set(), []
    for g in inc:
        if g not in seen:
            seen.add(g); out.append(g)
    return out


def match_files(collection_dir: Path, globs: list[str]) -> list[Path]:
    """Resolve include entries to files. An entry is either a literal file or a
    directory prefix (optionally ``<dir>/**``) → all files under it, recursively."""
    files: list[Path] = []
    seen = set()

    def _add_dir(root: Path) -> None:
        if root.is_dir():
            for q in sorted(root.rglob("*")):
                if q.is_file() and q not in seen:
                    seen.add(q); files.append(q)

    for g in globs:
        if g.endswith("/**"):
            _add_dir(collection_dir / g[:-3])
            continue
        p = collection_dir / g
        if p.is_file() and p not in seen:
            seen.add(p); files.append(p)
        elif p.is_dir():
            _add_dir(p)
    return files


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("collection_dir")
    ap.add_argument("--layer", required=True)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--out", default=None, help="copy the layer's files into this dir")
    args = ap.parse_args()
    cd = Path(args.collection_dir).expanduser().resolve()
    manifest = yaml.safe_load((cd / "MANIFEST.yaml").read_text(encoding="utf-8"))
    globs = resolve_includes(manifest, args.layer)
    files = match_files(cd, globs)
    total = sum(f.stat().st_size for f in files)
    print(f"layer '{args.layer}' of {manifest['collection']}/v{manifest['version']}: "
          f"{len(files)} files, {total/1e6:.2f} MB")
    if args.list:
        for f in files[:40]:
            print(f"  {f.relative_to(cd)}")
        if len(files) > 40:
            print(f"  … +{len(files) - 40} more")
    if args.out:
        out = Path(args.out).expanduser().resolve()
        for f in files:
            rel = f.relative_to(cd)
            (out / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, out / rel)
        print(f"  -> materialized to {out}")


if __name__ == "__main__":
    main()
