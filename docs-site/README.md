# docs-site/

Static GitHub Pages site for the ASB Skill Collections project. Pure HTML +
vanilla JS. No build step, no npm, no backend. Pages load no script, style or
font from another host: lunr.js is vendored under `vendor/` (MIT, licence in
`vendor/LICENSE-lunr.txt`) and the stylesheet uses locally installed or system
fonts.

## Pages

| File | What it reads | What it shows |
| ---- | ------------- | ------------- |
| `index.html` (+ `app.js`) | `catalogue.jsonld` and `leaderboard/career.jsonld` from this repository's raw files on `main` | Registry of collections with status, counts and version DOI (a released collection links to its Browse page), new-release banner, contributor leaderboard |
| `collections.html` (+ `site-data.js`, `collections.js`) | `catalogue.jsonld` (raw), `search_index/manifest.json`, `search_index/<domain>.json` | Skills, workflows and tools of one released collection, with a text filter and an EDAM topic filter on skills; registry counts and version DOI |
| `corpus.html` (+ `site-data.js`, `corpus.js`) | `search_index/manifest.json`, `search_index/<domain>.json` | Source papers of one domain, filtered by collection, status, access type and text |
| `paper.html` (+ `site-data.js`, `paper.js`) | `search_index/manifest.json`, `search_index/<domain>.json`, `catalogue.jsonld` (raw) | One paper and the skills that cite it; request-review and flag buttons |
| `search.html` (+ `search.js`) | `search_index/manifest.json`, `search_index/<domain>.json` | Full-text search across papers, skills, workflows and tools of the selected domains (lunr.js) |
| `contribute.html` (+ `contribute.js`) | nothing | Anonymized skill, workflow or tool improvement report as a pre-filled GitHub issue (mirrors `scripts/make_improvement_report.py`) |
| `propose.html` (+ `propose.js`) | nothing | Form to propose a paper for one of the released collections, submitted as a pre-filled GitHub issue in the fields of the intake parser |

The collection trees (each `SKILL.md`, tool record, `corpus.yaml` and machine
index) are in the private domain repositories `HolobiomicsLab/asb-skills-<domain>`
and in the Zenodo record of each release. No page requests them and no page
links to a domain repository. What a page shows of an item is what the public
index holds: name, description, summary, EDAM topics and source DOIs of a skill;
name, description, summary and stage count of a workflow; name, slug, licence,
code repositories cited by the source paper and evidence text of a tool; DOI,
title, status, access type and collection of a paper. Each page that shows
items says that the full text is in the Zenodo record of the release (the
version DOI from the registry) and in the private domain repository for people
with access.

A domain file is downloaded only for the domain on screen. Browse and Paper
load the domain of the collection or paper asked for, Corpus and Browse
default to the manifest's `default_domains` and show the download size in
their selector. All pages fetch a domain file with the same URL
(`search_index/<file>?v=<first 16 hex of its sha256>`), so the browser cache
serves it once to every page. All paths are relative, so the same code works
on `localhost` and under `/asb-skill-collections/` on GitHub Pages.

Browse offers the released collections that the index holds. Registry entries
it cannot show (a staged tree, or an earlier release that the index does not
hold, such as `metabolomics/v2`) are listed as not browsable here, with their
DOI when they have one. Search labels the rows of staged trees, links them to
their source paper page, and links rows of released collections to Browse
filtered to that item.

All write actions (request a review, flag, propose, contribute) open a
pre-filled issue on this public repository through URL parameters. Each names
its issue template (`template=`) and the labels of the vocabulary of
`scripts/skill_feedback.py`: `propose,paper-intake,needs-triage,auto-report`
(`3-propose-paper.md`), `review-requested,needs-triage` (`request-paper-review.md`)
and `usage-feedback,needs-triage,auto-report`, with `propose` for kind `gap` or
`composition` (`1-skill-feedback.md`, `2-request-skill.md`). GitHub applies
labels from the URL only for people with triage access to the repository; the
template's own labels are meant to cover the others (not verified against
GitHub). The paper form writes the fields that `scripts/intake_issue.py` reads.
`contribute.html` scrubs file paths, emails, IPs, and secrets in the browser
before building the issue body (same rules as the Python CLI).

## EDAM topic labels

Browse (chart, topic filter, skill cards) and the catalogue show an EDAM topic
by its label, with the id in parentheses or as a tooltip. The labels come from
`edam_topic_labels.json`: the EDAM version, the source and licence
(CC-BY-SA-4.0) and an `id -> label` map of every topic term in
`scripts/data/edam_labels.json`. Regenerate it with

```bash
python3 docs-site/build_edam_topic_labels.py
```

and check it with `--check`, which also fails when a topic of the search index
has no label (`tests/test_docs_site.py` runs it). A page loads the file once and
shows the id when a label is missing or the file cannot be read.

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
legacy trees `staged` (in a domain repository, not part of a release); the search
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
