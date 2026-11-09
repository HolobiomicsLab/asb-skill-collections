# Paper and resource proposal corpus schema

Proposal and literature-watch queues use `schema: asb-corpus/1.0`. This document
describes the existing live wave files and the optional intake fields. A YAML
date must be quoted so it loads as the required `YYYY-MM-DD` string.

## Document fields

| Field | Type | Required | Meaning |
|---|---|---|---|
| `schema` | string | yes | Exactly `asb-corpus/1.0`. |
| `collection` | string | yes | Domain collection, for example `metabolomics`. |
| `version` | integer | yes | Collection version number, without the `v` prefix. |
| `generated_on` | date string | yes | Queue generation or last regeneration date. |
| `source` | string | yes | Human-readable origin of the queue. |
| `policy` | string | yes | Governing access and reuse policy. |
| `wave` | string | yes | Wave identifier shared with its rows. |
| `summary` | mapping | yes | Recomputed row counts; see below. |
| `papers` | list of row mappings | yes | Paper, software, data, and infrastructure proposals. |

`summary.total` is the required integer number of rows. Each status key,
`candidate`, `hold`, `included`, `rejected`, and `duplicate`, is an optional
integer count. Existing sparse summaries remain valid; writers emit `total`
followed by every status count. Counts are always recomputed from `papers`.

## Proposal row fields

| Field | Type | Required | Meaning |
|---|---|---|---|
| `name` | string | yes | Short resource or software name. |
| `doi` | string or null | no | Paper, software, or resource DOI; repository-only resources may omit it. |
| `title` | string | yes | Full paper or resource title. |
| `year` | integer or null | yes | Publication year; null when a repository-only resource has no established year. |
| `category` | string | yes | Curator-assigned functional category. |
| `repo_url` | string | yes | Canonical public repository URL. |
| `status` | string | yes | One of the five disposition values below. |
| `license_tier` | string | yes | Corpus reuse tier, independent of article access. |
| `wave` | string | yes | Proposing or landing wave identifier. |
| `resource_type` | string | yes | Paper, software, database, workflow, or other resource subtype. |
| `source_issue` | integer | yes | Originating issue number, not a repository URL. |
| `links` | list of strings | no | Context links that are not the primary grounding source. |
| `source_watch` | date string | no | Literature-watch run date. |
| `source_queries` | list of strings | no | Source and query provenance retained for the row. |
| `relevance` | string | no | Fixed-vocabulary relevance verdict, or `unjudged`. |
| `relevance_basis` | string | no | Evidence and method behind the relevance verdict. |
| `priority` | integer | no | Transparent deterministic ranking, not a quality score. |
| `priority_reasons` | list of strings | no | Ordered reasons for the priority value. |
| `receipt` | string | no | Intake or processing receipt reference. |
| `access` | mapping | yes | Article and code access evidence, detailed below. |
| `triage` | mapping | yes | Proposer, rationale, and curator disposition, detailed below. |

All seven watch and intake fields are optional. Their absence does not make an
existing community wave invalid.

### Access fields

| Field | Type | Required | Meaning |
|---|---|---|---|
| `type` | string | yes | Access classification, such as `gold-oa`, `repo-oa`, or `restricted`. |
| `license` | string | yes | Article or resource reuse licence, or its explicit restriction. |
| `is_oa` | boolean | yes | Whether open access was established; this is not a reuse-tier decision. |
| `provenance` | string | no | Publication stage, such as `preprint`. |
| `oa_status` | string | no | Resolver-specific open-access classification. |
| `verified_via` | string | yes | Method or resolver that supplied the evidence. |
| `verified_on` | date string | no | Date of the access evidence. |
| `code_license` | string | no | Repository code licence, recorded separately from the paper licence. |

### Triage fields

| Field | Type | Required | Meaning |
|---|---|---|---|
| `proposer` | string | yes | Contributor handle or `literature-watch`. |
| `authors` | string | no | Authorship or overlap context. |
| `conflict_declared` | boolean | no | Whether the proposer declared a conflict of interest. |
| `rationale` | string | yes | Why the proposal belongs in the collection. |
| `decision` | string | yes | `pending` initially, then a curator decision such as `accept`, `reject`, or `duplicate`; existing `defer-pending-info` remains valid. |
| `notes` | string | yes | Evidence, caveats, and the reason for rejection or duplication. |
| `curated_by` | string | no | Curator responsible for the latest status transition. |
| `curated_on` | date string | no | Date of that transition. |

## Status and transitions

`candidate` is machine-discovered and deduplicated, but not curator-selected.
`hold` is queued for a future build after review and normally has decision
`accept`. `included` records confirmed landing, never merely a merged proposal.
`rejected` and `duplicate` are explicit terminal dispositions.

Allowed forward transitions are `candidate` to `hold` by a curator and `hold` to
`included` at confirmed landing. Any nonidentical current status may move to
`rejected` or `duplicate`; every such transition requires nonempty
`triage.decision`, `triage.notes`, curator, and date. No other forward
transition is allowed. Status changes recompute the summary.

## Identity, ordering, and writing

DOI normalization strips resolver prefixes and `doi:`, translates typographic
dashes, lowercases, removes prose punctuation, maps arXiv identifiers to DOIs,
and removes only the bioRxiv/medRxiv date-DOI version suffix. Duplicate checks
use the corpus punctuation-folded key. Precedence is covered DOI, released
corpus DOI, then an earlier open proposal DOI. Equal normalized repository
identities are warnings only, because distinct papers can share a repository.

`add_row` rejects a duplicate DOI and sorts by normalized DOI, then
`source_issue`, with DOI-less rows last. `dump` preserves the live document and
row key order, uses block mappings, disables aliases, and emits a trailing
newline. It does not preserve comments or source scalar styling. The first
write is therefore a one-time canonical normalization of existing wave files;
thereafter `load` followed by `dump` is byte-for-byte stable. Validation and
read-only duplicate checks never rewrite a file.

## Commands

```bash
python scripts/proposal_corpus.py validate <wave.yaml> [...]
python scripts/proposal_corpus.py summary <wave.yaml> [--write]
python scripts/proposal_corpus.py check-duplicates \
  --covered <covered_dois.json> --corpus <corpus.yaml> <wave.yaml> [...]
```

Validation exits 1 on any violation. Duplicate errors exit 1; repository-only
warnings do not. Summary prints recomputed JSON and only changes the file with
`--write`.
