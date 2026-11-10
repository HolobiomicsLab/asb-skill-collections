# docs-site/

Static GitHub Pages site for the ASB Skill Collections project. Pure HTML +
vanilla JS. No build step, no npm, no backend. Pages load no script, style or
font from another host: lunr.js is vendored under `vendor/` (MIT, licence in
`vendor/LICENSE-lunr.txt`) and the stylesheet uses locally installed or system
fonts.

## Pages

| File | What it shows |
| ---- | ------------- |
| `index.html` (+ `app.js`) | Catalogue of collections + new-release banner + ranked contributor leaderboard |
| `collections.html` (+ `collections.js`) | Browse a collection's skills, composite workflows (super-skills), and tools, with filters + per-item GitHub view/edit/suggest links |
| `corpus.html` (+ `corpus.js`) | Browse all source papers across collections, with filters |
| `paper.html` (+ `paper.js`) | Per-paper review: skills, tools, claims; verify/flag actions |
| `contribute.html` (+ `contribute.js`) | Package an anonymized skill/workflow improvement → pre-filled GitHub issue (mirrors `scripts/make_improvement_report.py`) |
| `propose.html` | Form to propose a new paper (submits via GitHub Issue URL params) |
| `search.html` (+ `search.js`) | Full-text search across papers / skills / workflows / tools of the selected domains (lunr.js) |

All write actions (verify, flag, propose, contribute) round-trip through GitHub
Issues or Pull Requests via prefilled URL params, with no server.

`collections.html` reads each collection's machine indexes from the domain
repository's raw files (`<domain checkout>/collections/<slug>/v<N>/skills_index.json`,
`workflows/workflows_index.json` and `tools_index.json` in that collection).
The domain repositories are private, so these raw files are not publicly readable.
`contribute.html` scrubs file paths, emails, IPs, and secrets in the browser
before building the issue body (same rules as the Python CLI).

## Search index

`search.html` performs client-side full-text search via
[lunr.js](https://lunrjs.com/) (2.3.9, vendored as `vendor/lunr-2.3.9.js`)
against a pre-built index in `docs-site/search_index/`: one `<slug>.json` per
registry domain and a small `manifest.json`. The files are checked into the
repository, so the site works on Pages without any CI step. The page reads
the manifest, shows one chip per domain with its download size and skill
count, and downloads only the selected domains, in parallel, before building
the lunr indices in the browser. The first selection is `default_domains`
from the manifest, or the domains named in `?domains=a,b`; the page keeps the
current selection in that parameter.

One file per domain keeps every file under GitHub's 100 MB limit as domains
are added, lets a registration rebuild only its own domain, and lets a reader
download only what they search.

### What a domain file holds

Each domain file indexes the latest published release of that domain plus its
legacy trees; `--include-superseded` adds every release the registry lists.
Trees under `staged-collections/` are not indexed: no registry row describes
them, so nothing could verify them.

### Regenerating a domain

After a registration changes a domain, rebuild that domain from a checkout of
its registered release. The master checkout holds no content trees: the
builder reads `collections.yaml` and the domain checkouts passed on its
command line.

```bash
python3 docs-site/build_search_index.py --checkout proteomics=<domain checkout>
```

Before indexing a checkout, the builder verifies every release it indexes
against the registry, as `scripts/check_collections_manifest.py --checkout`
does: the tree digest of the working tree and the counts must match the
registry row (a row without a tree digest is checked with git against its
commit instead). A checkout of another commit, or with edited or untracked
files in a release path, is refused.

Domains without a `--checkout` keep their existing file when the manifest
still records its sha256 and size and its `registry_digest` still matches the
registry. If any such domain has no file yet, or its registry rows changed,
the build is refused, names the domains that need a checkout, and writes
nothing. No domain is ever dropped. A domain removed from the registry loses
its file.

`--default-domain SLUG` (repeatable) sets the domains the page loads first;
without it the manifest keeps its current value (initially `metabolomics`).
`--output-dir` writes elsewhere than `docs-site/search_index/`.

The build records no timestamp, walks every tree in sorted path order and
sorts JSON keys, so two builds of the same trees are byte-identical.

Requirements: Python 3.9+ and `PyYAML`. No network access is needed. Commit
the changed domain files together with `manifest.json`. `scripts/release_domain.py
manifest --regen` runs the same build with the checkout of the domain being
registered and any `--checkout` passed to it.

### Checking the committed index

The domain repositories are private, so CI cannot rebuild the index. The
`search-index` job in `.github/workflows/validate.yml` runs

```bash
python docs-site/build_search_index.py --check-manifest docs-site/search_index
```

which reads no checkout. It fails when a registry domain has no entry, an
entry names a domain that left the registry, a file is missing or differs in
size or sha256 from the manifest, an unrecorded `.json` file sits in the
directory, `default_domains` names an unindexed domain, or a domain's
`registry_digest` no longer matches its rows in `collections.yaml`. It does
not prove that a file was built from the registered trees; the builder's
checkout verification does that at build time.

### Schema

`manifest.json`:

```json
{
  "schema_version": "1",
  "default_domains": ["metabolomics"],
  "domains": {
    "metabolomics": {
      "file": "metabolomics.json", "sha256": "...", "bytes": 34990781,
      "include_superseded": false,
      "registry_digest": "...",
      "collections": [{"label": "metabolomics/v3", "status": "released", "commit": "..."}, ...],
      "counts": {"papers": 575, "skills": 13315, "tools": 2281, "workflows": 20}
    }, ...
  }
}
```

`registry_digest` is the sha256 of a canonical JSON serialisation of the
domain slug, the `include_superseded` flag and, for each indexed release in
version order, its `path`, `version`, `status`, `commit` and `tree_digest`.
Other registry fields (DOIs, dates, counts, other domains) do not affect it.

A domain file, `<slug>.json`:

```json
{
  "schema_version": "0.2",
  "domain": "metabolomics",
  "collections": ["metabolomics/v1", "metabolomics/v3"],
  "collection_status": {"metabolomics/v1": "staged", "metabolomics/v3": "released"},
  "collection_commits": {"metabolomics/v1": "...", "metabolomics/v3": "..."},
  "papers": [{"doi": "...", "title": "...", "rationale": "...", "collection": "...",
              "status": "...", "access_type": "...", "derived_skills": N,
              "derived_tools": M, "search_text": "..."}, ...],
  "skills": [{"name": "...", "description": "...", "when_to_use_negative": "...",
              "edam_topics": [...], "collection": "...", "summary": "...",
              "source_dois": [...], "md_path": "...", "search_text": "..."}, ...],
  "workflows": [{"slug": "...", "name": "...", "description": "...", "techniques": [...],
                 "stage_count": N, "collection": "...", "summary": "...",
                 "md_path": "...", "search_text": "..."}, ...],
  "tools":  [{"slug": "...", "name": "...", "source_paper_repos": [...],
              "license_spdx": "...", "evidence_text": "...", "collection": "...",
              "source_doi": "...", "yaml_path": "...", "search_text": "..."}, ...]
}
```

`collection_status` marks the latest published release `released` and the
legacy trees `staged` (in the repository, not part of a release); the search
page labels results from staged collections. `search_text` is the
concatenated searchable text; all other fields are for display. The page
merges the selected domain files into one object of this shape (without
`domain`) before building the lunr indices.

## Local preview

```bash
cd docs-site
python3 -m http.server 8000
# open http://localhost:8000
```
