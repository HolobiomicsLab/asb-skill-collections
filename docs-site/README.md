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
| `search.html` (+ `search.js`) | Full-text search across papers / skills / tools (lunr.js) |

All write actions (verify, flag, propose, contribute) round-trip through GitHub
Issues or Pull Requests via prefilled URL params, with no server.

`collections.html` reads each collection's machine indexes from the domain
repository's raw files (`<domain checkout>/collections/<slug>/v<N>/skills_index.json`,
`workflows/workflows_index.json` and `tools_index.json` in that collection).
Private domain content is not publicly readable until its repository opens.
`contribute.html` scrubs file paths, emails, IPs, and secrets in the browser
before building the issue body (same rules as the Python CLI).

## Search index

`search.html` performs client-side full-text search via
[lunr.js](https://lunrjs.com/) (2.3.9, vendored as `vendor/lunr-2.3.9.js`)
against a pre-built index at `docs-site/search_index.json`. The index is
checked into the repo so the site works offline / on Pages without any CI
step.

### Regenerating `search_index.json`

After a domain promotion changes papers, SKILL.md frontmatter or tool YAMLs,
make the relevant domain checkout available to the builder. The master checkout
holds no content trees: the builder reads `collections.yaml` and the domain
checkouts passed on its command line.

```bash
python3 docs-site/build_search_index.py --checkout metabolomics=<domain checkout> --checkout epigenomics=<domain checkout> --checkout transcriptomics=<domain checkout>
```

The index covers the latest published release of each domain and the legacy
trees; `--include-superseded` adds every release the registry lists. The
payload records the manifest digest it was built from, and CI compares that
digest with the committed `collections.yaml` (`--check-manifest`), since the
domain repositories are private.

Requirements: Python 3.9+ and `PyYAML` (already pinned in `pyproject.toml`).
The script walks the domain checkouts given on the command line. No network
access is needed.

Stdout prints a one-line summary like:

```
Indexed 5 papers, 106 skills, 38 tools across 1 collections. Wrote docs-site/search_index.json (327,303 bytes).
```

Commit the updated `search_index.json` alongside the content change.

The build records no timestamp and walks every tree in sorted path order, so
two builds of the same tree are byte-identical. The `search-index` job in
`.github/workflows/validate.yml` relies on that: it rebuilds the index with
`--output "$RUNNER_TEMP/search_index.json"` and fails when the result differs
from the committed file. To check locally without touching the committed file:

```bash
python docs-site/build_search_index.py --checkout metabolomics=<domain checkout> --output /tmp/search_index.json
cmp /tmp/search_index.json docs-site/search_index.json
```

### Schema

The index is a single JSON object with the shape:

```json
{
  "schema_version": "0.1",
  "collections": ["metabolomics/v1", ...],
  "collection_status": {"metabolomics/v1": "staged", "metabolomics/v2": "released", ...},
  "papers": [{"doi": "...", "title": "...", "rationale": "...", "collection": "...",
              "status": "...", "access_type": "...", "derived_skills": N,
              "derived_tools": M, "search_text": "..."}, ...],
  "skills": [{"name": "...", "description": "...", "when_to_use_negative": "...",
              "edam_topics": [...], "collection": "...", "summary": "...",
              "source_dois": [...], "md_path": "...", "search_text": "..."}, ...],
  "tools":  [{"slug": "...", "name": "...", "source_paper_repos": [...],
              "license_spdx": "...", "evidence_text": "...", "collection": "...",
              "source_doi": "...", "yaml_path": "...", "search_text": "..."}, ...]
}
```

`collection_status` says which collections are released (served by the plugin
marketplace) and which are staged, with the rule `scripts/regen_catalogue.py`
applies to `catalogue.jsonld`; the search page labels results from staged
collections. `search_text` is the concatenated searchable text; all other fields are for
display. The lunr index itself is built client-side from this JSON on page
load (a few hundred ms for the current corpus).

## Local preview

```bash
cd docs-site
python3 -m http.server 8000
# open http://localhost:8000
```
