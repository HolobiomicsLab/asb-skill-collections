# docs-site/

Static GitHub Pages site for the ASB Skill Collections project. Pure HTML +
vanilla JS + CDN-loaded libraries. No build step, no npm, no backend.

## Pages

| File | What it shows |
| ---- | ------------- |
| `index.html` (+ `app.js`) | Catalogue of collections + contributor leaderboard |
| `corpus.html` (+ `corpus.js`) | Browse all source papers across collections, with filters |
| `paper.html` (+ `paper.js`) | Per-paper review: skills, tools, claims; verify/flag actions |
| `propose.html` | Form to propose a new paper (submits via GitHub Issue URL params) |
| `search.html` (+ `search.js`) | Full-text search across papers / skills / tools (lunr.js) |

All write actions (verify, flag, propose) round-trip through GitHub Issues or
Pull Requests via prefilled URL params — no server.

## Search index

`search.html` performs client-side full-text search via
[lunr.js](https://lunrjs.org/) (loaded from CDN, pinned to `lunr@2.3.9`)
against a pre-built index at `docs-site/search_index.json`. The index is
checked into the repo so the site works offline / on Pages without any CI
step.

### Regenerating `search_index.json`

Run after any promote (i.e. anytime `collections/**` or `staged-collections/**`
changes in a way that affects papers, SKILL.md frontmatter, or tool YAMLs):

```bash
python3 docs-site/build_search_index.py
```

Requirements: Python 3.9+ and `PyYAML` (already pinned in `pyproject.toml`).
The script walks the local filesystem from the repo root — no network access
is needed.

Stdout prints a one-line summary like:

```
Indexed 5 papers, 106 skills, 38 tools across 1 collections. Wrote docs-site/search_index.json (327,303 bytes).
```

Commit the updated `search_index.json` alongside the content change.

### Schema

The index is a single JSON object with the shape:

```json
{
  "schema_version": "0.1",
  "generated_at": "2026-05-25T...Z",
  "collections": ["metabolomics/v1", ...],
  "papers": [{"doi": "...", "title": "...", "rationale": "...", "collection": "...",
              "status": "...", "access_type": "...", "derived_skills": N,
              "derived_tools": M, "search_text": "..."}, ...],
  "skills": [{"name": "...", "description": "...", "when_to_use_negative": "...",
              "edam_topics": [...], "collection": "...", "summary": "...",
              "source_dois": [...], "md_path": "...", "search_text": "..."}, ...],
  "tools":  [{"slug": "...", "name": "...", "canonical_url": "...",
              "license_spdx": "...", "evidence_text": "...", "collection": "...",
              "source_doi": "...", "yaml_path": "...", "search_text": "..."}, ...]
}
```

`search_text` is the concatenated searchable text — all other fields are for
display. The lunr index itself is built client-side from this JSON on page
load (a few hundred ms for the current corpus).

## Local preview

```bash
cd docs-site
python3 -m http.server 8000
# open http://localhost:8000
```
