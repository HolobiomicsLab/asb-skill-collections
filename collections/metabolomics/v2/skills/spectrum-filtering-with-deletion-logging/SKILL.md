---
name: spectrum-filtering-with-deletion-logging
description: Use when processing heterogeneous mass spectrometry libraries (e.g., from OMSLs) where chemical identifiers are unevenly populated across records.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0637
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - FragHub
  - Python 3.12
  - spectra-hash (SPLASH)
derived_from:
- doi: 10.1021/acs.analchem.4c02219
  title: FragHub
evidence_spans:
- Python-3.12
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fraghub_cq
    doi: 10.1021/acs.analchem.4c02219
    title: FragHub
  dedup_kept_from: coll_fraghub_cq
schema_version: 0.2.0
---

# spectrum-filtering-with-deletion-logging

## Summary

This skill removes mass spectra that fail structural completeness checks (lacking all three of SMILES, InChI, and InChIKey simultaneously) while preserving detailed audit logs of each deletion decision. It standardizes spectral datasets by enforcing chemical identifier requirements and maintaining traceable records of quality control decisions.

## When to use

Apply this skill when processing heterogeneous mass spectrometry libraries (e.g., from OMSLs) where chemical identifiers are unevenly populated across records. Use it before downstream analysis or format conversion when you need both a cleaned dataset and an auditable record of which spectra were removed and why—particularly in collaborative or regulatory contexts where data curation decisions must be defensible.

## When NOT to use

- Input spectra are already known to be complete and curated (no structural identifier gaps expected).
- You require spectra without structural identifiers for analysis (e.g., instrument development or raw data preservation).
- Deletion logs are not required or acceptable due to data governance constraints.

## Inputs

- JSON spectral data file (ISO/IEC 20802-2:2016 compatible or non-standard format)
- Spectral records with SMILES, InChI, InChIKey fields (may be empty or absent)

## Outputs

- Filtered JSON spectral data file containing only spectra with ≥1 structural identifier
- DELETION_REASONS subdirectory containing detailed logs of each filtered spectrum with rationale

## How to apply

Iterate through each spectrum record in the input JSON file and check for the presence and non-emptiness of SMILES, InChI, and InChIKey fields. Retain a spectrum only if it possesses at least one of these three identifiers; delete it only when all three are absent or empty. For each deleted spectrum, write a detailed deletion record (spectrum metadata plus human-readable reason) to a DELETION_REASONS subdirectory, organized by deletion category. The filtering logic is conjunctive for deletion (AND clause: all three absent) but disjunctive for retention (OR clause: at least one present). Output the retained spectra to the same JSON format as input, ensuring compatibility with ISO/IEC 20802-2:2016 and non-standard formats.

## Related tools

- **FragHub** (Primary implementation framework; applies spectrum filtering workflow with deletion logging as part of standardization pipeline for open mass spectra libraries) — https://github.com/eMetaboHUB/FragHub
- **Python 3.12** (Execution environment for iterating records, checking identifier fields, writing logs, and serializing JSON output)
- **spectra-hash (SPLASH)** (Integrated for spectrum deduplication by SPLASH key; complements deletion logging by enabling post-filter duplicate removal) — https://github.com/berlinguyinca/spectra-hash

## Evaluation signals

- Retained spectrum count and deletion count match expected cardinality based on input structural identifier distribution.
- Every deleted spectrum has a corresponding record in DELETION_REASONS with non-empty reason field and correct metadata.
- All retained spectra contain at least one of {SMILES, InChI, InChIKey} and are non-empty.
- Output JSON validates against ISO/IEC 20802-2:2016 schema or original non-standard format specification.
- Spot-check a sample of deletion logs confirms accurate classification (e.g., spectrum with SMILES but no InChI is retained, not logged as deleted).

## Limitations

- Filtering logic is strict conjunctive (all three identifiers must be absent to trigger deletion); spectra with one identifier and two absent are retained even if structural information is sparse.
- Does not validate semantic correctness of retained identifiers (e.g., SMILES syntax, InChIKey format compliance); only checks presence and non-emptiness.
- Deletion logs are written to local filesystem; no built-in support for remote audit trail or append-only database storage.
- No explicit validation or reconciliation of identifier consistency (e.g., whether SMILES and InChI represent the same molecule); retains spectra with potentially conflicting identifiers.
- Windows and macOS are no longer supported as of FragHub 1.4.1; Linux x64 and original macOS arm64 builds are available but may not receive updates.

## Evidence

- [other] FragHub removes spectra that lack all three structural identifiers simultaneously—a spectrum is deleted only when it has no SMILES AND no InChI AND no InChIKey, retaining spectra that possess at least one of these identifiers.: "FragHub removes spectra that lack all three structural identifiers simultaneously—a spectrum is deleted only when it has no SMILES AND no InChI AND no InChIKey, retaining spectra that possess at"
- [other] Retain only spectra where all three identifiers (SMILES AND InChI AND InChIKey) are present and non-empty.: "Retain only spectra where all three identifiers (SMILES AND InChI AND InChIKey) are present and non-empty."
- [other] Log deletion reasons for each filtered spectrum to a DELETION_REASONS subdirectory with detailed rationale.: "Log deletion reasons for each filtered spectrum to a DELETION_REASONS subdirectory with detailed rationale."
- [discussion] improve spectrum deletion callback by writing deleted spectrum in DELETION_REASONS sub folder with a detailed reason.: "improve spectrum deletion callback by writing deleted spectrum in DELETION_REASONS sub folder with a detailed reason."
- [discussion] Now deleting spectrum with no SMILES no InChI **AND no inchikey**.: "Now deleting spectrum with no SMILES no InChI **AND no inchikey**."
- [other] Load the input spectral data file (JSON format compatible with ISO/IEC 20802-2:2016 and non-standard formats).: "Load the input spectral data file (JSON format compatible with ISO/IEC 20802-2:2016 and non-standard formats)."
- [readme] All spectra deemed inconsistent, i.e., those lacking SMILES and InChI, precursor m/z, and adduct information, are removed during the processing by FragHub.: "All spectra deemed inconsistent, i.e., those lacking SMILES and InChI, precursor m/z, and adduct information, are removed during the processing by FragHub."
