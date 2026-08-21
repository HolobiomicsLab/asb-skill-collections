---
name: metabolomicshub-cross-repository-dataset-search
description: Use when locating public metabolomics datasets across MetaboLights, Metabolomics
  Workbench and GNPS/MassIVE in one query, or when filtering candidate studies by
  instrument, ionisation mode or the availability of open raw formats before committing
  to a reanalysis.
license: CC-BY-4.0
status: hold
metadata:
  tools:
  - MetabolomicsHub
  techniques:
  - LC-MS
  - GC-MS
  repo_url: https://github.com/MetabolomicsHub/mhd-model
  related_skills: []
  license_tier: open
  provenance_tier: repository
  tool_license:
    tier: open
    requires_ack: false
    ref: Apache-2.0
    url: https://github.com/MetabolomicsHub/mhd-model/blob/main/LICENSE
schema_version: 0.2.0
---

# metabolomicshub-cross-repository-dataset-search

Find public metabolomics studies across repositories that do not share a search
interface, and filter them down to the ones a reanalysis can actually use.

## When this applies

A reanalysis, a benchmark or a meta-analysis needs studies matching some
combination of organism, instrument, ionisation mode and file format. Those
studies are spread across MetaboLights (EBI), Metabolomics Workbench (NIH) and
GNPS/MassIVE, each with its own accession scheme, metadata vocabulary and API.
Searching them one at a time misses cross-repository duplicates and makes the
instrument and format filters — the ones that decide whether the data is usable —
impossible to apply uniformly.

MetabolomicsHub publishes a common model (MHD) over those repositories and an
API that answers a single query across all of them.

## Procedure

1. **State the selection criteria before searching.** Organism, sample matrix,
   instrument or instrument family, polarity, and the file formats the downstream
   pipeline can read. Write them down; they are the inclusion criteria of
   whatever you are building, and deciding them after seeing the hits is how a
   convenience sample becomes a claim.
2. **Query the announcement API** at `https://www.metabolomicshub.org/api/` for
   the criteria that the common model expresses directly. Consult
   `https://metabolomicshub.github.io/mhd-model/` for the field names — the model
   is versioned, and a field that existed in one release may be renamed in the
   next.
3. **Filter on open raw formats.** A study whose raw data is vendor-only cannot
   be reprocessed without the vendor's converter, and on some platforms not at
   all. Prefer mzML; treat the presence of vendor-only formats as a study-level
   exclusion unless conversion has been verified.
4. **Resolve duplicates across repositories.** One study can be deposited in more
   than one repository, sometimes under different accessions. Match on title,
   submitter and sample count before treating two hits as independent.
5. **Record the accession and the repository for every retained study**, not just
   the count. A dataset list without accessions cannot be re-run by anyone else.

## Verification

- Every retained study resolves at its home repository by accession.
- The instrument and polarity recorded by the hub agree with the study's own
  metadata; where they disagree, the repository is authoritative.
- The declared file formats are actually present in the study's file listing.

## Limitations

- Coverage is bounded by what the participating repositories announce; a study
  that was never announced through the hub will not appear, so a negative result
  is not evidence of absence.
- The common model normalises heterogeneous metadata, and normalisation loses
  detail. For anything the analysis depends on, read the study's own record.
- Instrument strings are free text in the source repositories, so instrument
  filtering is best-effort and should be confirmed per study.
