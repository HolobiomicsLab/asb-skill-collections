# Design: cross-paper citation graph

**Status:** design draft (v1.1+).
**Author:** Holobiomics Lab.
**Last revised:** 2026-05-25.

## Problem

`corpus.yaml` lists papers as a flat set. No relationships captured.

Concrete losses:
- Papers in a domain corpus heavily cite each other. We discard that structure.
- "Skill A from paper X is the conceptual predecessor of skill B from paper Y" — discoverable to a curator manually, invisible to users.
- Cite-graph clustering could identify foundational vs derivative papers; useful curation signal.

Perspicacité-AI MCP exposes `get_paper_references` (returns the Crossref + OpenAlex references list for a DOI). The data is available; we just don't pipe it into the release.

## Approach

Emit a `cite_graph.json` per collection alongside `corpus.yaml`, populated by Perspicacité MCP during `asb collection promote`. Surface in the static docs site (paper.html).

## Schema

```json
{
  "schema_version": "0.1",
  "collection": "metabolomics",
  "collection_version": 1,
  "generated_at": "2026-05-25T09:00:00Z",
  "perspicacite_source": "v0.x.y",
  "nodes": [
    { "doi": "10.1186/s13321-024-00878-1",
      "in_corpus": true,
      "n_references_in_corpus": 2 },
    { "doi": "10.1038/s41592-025-02660-z",
      "in_corpus": true,
      "n_references_in_corpus": 0 },
    { "doi": "10.1021/external-paper",
      "in_corpus": false,
      "external_citations_count": 1 }
  ],
  "edges": [
    { "from_doi": "10.1186/s13321-024-00878-1",
      "to_doi": "10.1128/msystems.00710-22",
      "edge_type": "cites",
      "source": "crossref" },
    { "from_doi": "10.1186/s13321-024-00878-1",
      "to_doi": "10.1021/external-paper",
      "edge_type": "cites",
      "external_target": true,
      "source": "crossref" }
  ],
  "stats": {
    "n_internal_edges": 12,
    "n_external_edges": 47,
    "max_external_per_paper": 50
  }
}
```

- `edge_type` ∈ {`cites`, `cited_by`}. `cited_by` is the inverse — useful for finding papers that build on a foundational reference.
- External targets capped to top-N most-cited (default N=50) to keep the file size bounded.

## UI surface

In `paper.html`:

- New section "References (in corpus)" — lists corpus-internal citations as clickable links to the cited paper's `paper.html`.
- New section "Cited by (in corpus)" — papers in the same corpus that reference this one.
- Optional "External references" — collapsed by default; expand reveals top-N external citations with DOI links.

In `corpus.html`:

- New filter "Show only papers with >0 internal citations" — surfaces the connected component of the corpus.
- Optional: graph view toggle (phase 3).

## Phased rollout

| Phase | When | What ships |
|---|---|---|
| 1 | v1.1 | `cite_graph.json` emitted by `asb collection promote`; no UI changes. |
| 2 | v1.2 | `paper.html` adds References / Cited-by sections. |
| 3 | v2.0 | `corpus.html` visual graph view (sigma.js or vis.js). |

## Open questions

1. **Preprint ↔ published version.** If a corpus has both the bioRxiv preprint and the published Nature Methods version of the same work, how do we link them? Recommendation: `equivalent_to` edges with a confidence score from Crossref's preprint-to-published linker.
2. **Citation context.** Knowing paper A cites paper B is weak signal. Knowing WHERE in paper A's text it cites (Methods? Discussion? Critical?) is strong signal but expensive to extract. Recommendation: phase 4+ feature, requires LLM extraction over paper full-text.
3. **Refresh cadence.** Citations grow over time. Recommendation: regenerate `cite_graph.json` on every `promote` (cheap) and on quarterly cron (`corpus-freshness.yml` extension).
4. **Privacy / paywall.** Crossref references are open; OpenAlex citations are open. Some publishers' full reference lists are paywalled (rare). Recommendation: use Crossref only for v1.1, augment with OpenAlex in v1.2.

## Tracking issue

(Placeholder — file when starting phase 1.)

## See also

- Perspicacité MCP `get_paper_references` tool.
- `corpus.yaml` schema 0.2 — natural sibling file.
