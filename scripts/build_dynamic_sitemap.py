"""Build a dynamic sitemap.xml that includes per-paper deep-link URLs.

Reads all `corpus.yaml` files under `collections/**` and `staged-collections/**`
and emits a sitemap entry for each paper of the form:
  https://holobiomicslab.github.io/asb-skill-collections/paper.html?doi=<doi>&collection=<slug>

Keeps the 5 static base entries (index, corpus, search, propose, paper itself).

Run as part of `pages.yml` after the search index is regenerated. Output is
written in-place to `docs-site/sitemap.xml`.

Usage:
    python scripts/build_dynamic_sitemap.py
        [--repo-root .] [--output docs-site/sitemap.xml]
        [--base-url https://holobiomicslab.github.io/asb-skill-collections]
"""
from __future__ import annotations

import argparse
import pathlib
import sys
from urllib.parse import quote
from xml.sax.saxutils import escape

import yaml


STATIC_ENTRIES = [
    ("/", "1.0", "weekly"),
    ("/corpus.html", "0.9", "weekly"),
    ("/search.html", "0.9", "weekly"),
    ("/propose.html", "0.7", "monthly"),
]


def _collect_paper_urls(repo_root: pathlib.Path, base_url: str) -> list[tuple[str, str, str]]:
    """Walk all corpus.yaml files and return (url, priority, changefreq) tuples."""
    urls: list[tuple[str, str, str]] = []
    seen: set[str] = set()
    for corpus_yaml in sorted(repo_root.glob("collections/**/corpus.yaml")) + sorted(
        repo_root.glob("staged-collections/**/corpus.yaml")
    ):
        try:
            data = yaml.safe_load(corpus_yaml.read_text(encoding="utf-8")) or {}
        except Exception as exc:
            print(f"WARNING: skipping {corpus_yaml}: {exc}", file=sys.stderr)
            continue
        collection = data.get("collection", "")
        version = data.get("collection_version", "")
        for paper in (data.get("papers") or []):
            if not isinstance(paper, dict):
                continue
            doi = paper.get("doi")
            if not doi:
                continue
            # Skip excluded papers — no review surface for them
            if paper.get("status") == "excluded":
                continue
            key = f"{collection}/{doi}"
            if key in seen:
                continue
            seen.add(key)
            url = (
                f"{base_url}/paper.html?"
                f"doi={quote(doi, safe='')}"
                f"&collection={quote(str(collection), safe='')}"
            )
            urls.append((url, "0.6", "monthly"))
    return urls


def build_sitemap(repo_root: pathlib.Path, base_url: str) -> str:
    """Render the full sitemap.xml string."""
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    base_url_clean = base_url.rstrip("/")

    # Static entries
    for path, priority, freq in STATIC_ENTRIES:
        loc = base_url_clean + (path if path != "/" else "/")
        lines.append("  <url>")
        lines.append(f"    <loc>{escape(loc)}</loc>")
        lines.append(f"    <changefreq>{freq}</changefreq>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append("  </url>")

    # Dynamic per-paper entries
    paper_urls = _collect_paper_urls(repo_root, base_url_clean)
    for url, priority, freq in paper_urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{escape(url)}</loc>")
        lines.append(f"    <changefreq>{freq}</changefreq>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append("  </url>")

    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--repo-root", default=".", help="Repo root path")
    parser.add_argument(
        "--output", default="docs-site/sitemap.xml", help="Output path"
    )
    parser.add_argument(
        "--base-url",
        default="https://holobiomicslab.github.io/asb-skill-collections",
        help="Base URL of the deployed site",
    )
    args = parser.parse_args()

    repo_root = pathlib.Path(args.repo_root).resolve()
    out_path = pathlib.Path(args.output)
    if not out_path.is_absolute():
        out_path = repo_root / out_path

    text = build_sitemap(repo_root, args.base_url)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")

    n_static = len(STATIC_ENTRIES)
    n_dynamic = text.count("<url>") - n_static
    print(
        f"sitemap.xml written to {out_path} "
        f"({n_static} static + {n_dynamic} dynamic = {n_static + n_dynamic} entries)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
