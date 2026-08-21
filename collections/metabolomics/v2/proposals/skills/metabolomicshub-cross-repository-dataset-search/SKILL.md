---
name: metabolomicshub-cross-repository-dataset-search
description: Use when assembling a reanalysis or meta-analysis cohort from public
  metabolomics studies held in MetaboLights, Metabolomics Workbench and GNPS/MassIVE,
  and the instrument, polarity or open-format filters have to be honest about which
  repositories they silently exclude.
license: CC-BY-4.0
status: hold
metadata:
  tools:
  - MetabolomicsHub
  techniques:
  - LC-MS
  - GC-MS
  repo_url: https://github.com/MetabolomicsHub/mhd-model
  service_url: https://www.metabolomicshub.org/api/submission
  related_skills: []
  license_tier: open
  provenance_tier: repository
  tool_license:
    tier: open
    requires_ack: false
    ref: Apache-2.0
    url: https://github.com/MetabolomicsHub/mhd-model/blob/main/LICENSE
  verified_against:
    api_version: v0.0.1
    observed: '2026-08-21'
schema_version: 0.2.0
---

# metabolomicshub-cross-repository-dataset-search

Find public metabolomics studies across repositories that do not share a search
interface, and know which studies your filters threw away for want of metadata
rather than for want of a match.

## When this applies

A reanalysis, a benchmark or a meta-analysis needs studies matching some
combination of organism, instrument, polarity and file format. Those studies sit
in MetaboLights (EBI), Metabolomics Workbench (NIH) and GNPS/MassIVE, each with
its own accession scheme, metadata vocabulary and API. MetabolomicsHub indexes
all three behind one query.

The index is not uniform, and that is the thing this skill exists to handle. Each
repository populates a different subset of the searchable fields, so a filter can
exclude an entire repository for having no value in a field rather than the wrong
value. The result still looks like a search result.

## The service

Base URL `https://www.metabolomicshub.org/api/submission/v0_1`. The bare
`/api/` path is not a route. The endpoints below need no credentials; the
submission and identifier endpoints on the same base do.

| endpoint | method | use |
| --- | --- | --- |
| `/search/fields` | GET | the searchable field list and, per field, the operators it accepts |
| `/search/datasets` | POST | keyword search |
| `/search/advanced/datasets` | POST | clause-based search, returns facets |
| `/search/advanced/datasets/example` | GET | a worked request body for every clause kind |
| `/search/advanced/datasets/export` | POST | the result set as a file |
| `/server-info` | GET | index version and the schema profiles in force |

## Procedure

1. **State the selection criteria before searching.** Organism, sample matrix,
   instrument or instrument family, polarity, and the file formats the downstream
   pipeline can read. They are the inclusion criteria of whatever you are
   building; deciding them after seeing the hits is how a convenience sample
   becomes a claim.

2. **Read `/search/fields` rather than guessing field names.** It returns each
   field's target (`DATASET` or `METABOLITE`), value type and permitted
   operators. The list is versioned with the index and is the only authority on
   what is filterable today.

3. **Express the query as clauses.** `POST /search/advanced/datasets` takes
   `{version, query_text, inter_field_combiner, clauses, where, page, sort}`,
   with `page` shaped `{current, size}`. The clause kinds are `terms`,
   `compare`, `parameter_pair`, `characteristic_pair` and `descriptor`.
   Polarity is not a top-level field: it arrives as a `parameter_pair` with
   `type_name: "scan polarity"`. `GET /search/advanced/datasets/example`
   returns a body exercising each kind, which is quicker to adapt than the
   schema.

4. **Filter on open raw formats after the query, not inside it.** No field
   indexes file format, so no clause can express it. Each returned study instead
   carries a `files` block with `extensions` — a list of `{extension, count}`
   pairs — and you filter on that client-side. A study whose raw data is
   vendor-only cannot be reprocessed without the vendor's converter, and on some
   platforms not at all; prefer `.mzml` and treat vendor-only as a study-level
   exclusion unless conversion has been verified.

5. **Measure what each filter excluded before trusting it.** Re-run the query
   with the filter removed, facet both runs by `dataset_repository`, and compare
   per repository. A filter that takes one repository to zero has selected on
   metadata availability, not on science. Record the comparison; it is part of
   the cohort's description.

6. **Record the accession, the repository and the MetabolomicsHub id for every
   retained study**, not just the count. A dataset list without accessions
   cannot be re-run by anyone else.

## Field coverage is repository-dependent

Facet totals for the whole index, observed 2026-08-21 against index v0.0.1
(6,796 datasets). Re-measure before relying on them; the index is growing.

| repository | datasets | MS instrument | chromatography | parameters | omics type |
| --- | --- | --- | --- | --- | --- |
| Metabolomics Workbench | 3,703 | populated | populated | populated | **none** |
| MetaboLights | 2,593 | populated | populated | populated | populated |
| GNPS/MassIVE | 500 | **none** | **none** | **none** | **none** |

Two consequences worth stating plainly, because both are silent:

- Any instrument or polarity filter drops all 500 GNPS/MassIVE studies, which
  carry no structured instrument or parameter metadata in this index.
- `facet_omics_types` is populated only by MetaboLights: filtering
  `facet_omics_types = Metabolomics` returned 2,331 studies, and adding
  `dataset_repository = metabolights` returned the same 2,331. The filter is a
  repository filter wearing an omics label.

Every dataset in the index is currently `legacy` profile, so the fields the MS
profile adds — `dataset_mhd_identifier`, `sample_runs_count`, `subjects_count` —
are not yet usable as filters.

## Metabolite-level search

Four fields target `METABOLITE` rather than `DATASET`: `metabolite_name`,
`metabolite_accession`, `metabolite_identifier_accession` and
`metabolite_identifier_source`. They answer "which public studies report this
compound", which is a different question from "which studies used this
instrument" and is not reachable from the repositories' own search interfaces.
The same coverage caveat applies: a study that reported no metabolite table is
absent from the answer.

## Verification

- Every retained study resolves at its home repository by accession.
- The instrument and polarity recorded by the hub agree with the study's own
  record; where they disagree, the repository is authoritative.
- The extensions counted in `files.extensions` are actually present in the
  study's file listing.
- Each filter's per-repository exclusion has been measured, not assumed.

## Limitations

- Coverage is bounded by what the participating repositories have submitted, so
  a negative result is not evidence of absence.
- The common model normalises heterogeneous metadata, and normalisation loses
  detail. For anything the analysis depends on, read the study's own record.
- Instrument strings originate as free text in the source repositories. The
  facet groups them, but two spellings of one instrument can remain two buckets.
- The index version is reported by `/server-info` and the field list moves with
  it. Pin both in the methods section of anything you publish from this.
