---
name: spectral-library-record-structuring
description: Use when you have extracted MS1 and MS2 scans (in mzML/mzXML format)
  from raw chromatogram files and possess user-provided metadata (retention time,
  m/z, compound name, molecular weight, annotation fields) that you need to bind together
  into a queryable spectral library record for local compound.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - meRgeION2
  - MergeION2
  - GNPS
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.2c04343
  title: MeRgeION
evidence_spans:
- github.com__daniellyz__meRgeION2
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mergeion_cq
    doi: 10.1021/acs.analchem.2c04343
    title: MeRgeION
  dedup_kept_from: coll_mergeion_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.2c04343
  all_source_dois:
  - 10.1021/acs.analchem.2c04343
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Spectral library record structuring

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Combines extracted MS1 and MS2 scans with user-provided metadata into standardized GNPS-style spectral library records suitable for compound annotation and library search. This skill is essential for building confidential, institution-local spectral libraries from proprietary LC-MS/MS data without public data sharing.

## When to use

You have extracted MS1 and MS2 scans (in mzML/mzXML format) from raw chromatogram files and possess user-provided metadata (retention time, m/z, compound name, molecular weight, annotation fields) that you need to bind together into a queryable spectral library record for local compound annotation or analog search workflows.

## When NOT to use

- Input scans are in non-standard mass spectrometry formats (not mzML/mzXML); convert first using standard format conversion tools.
- Metadata file is incomplete or missing critical fields (m/z, retention time, or compound identifiers); validate and curate metadata before structuring.
- You intend to perform real-time online spectral matching against public databases (GNPS, MassBank); use library_query() on pre-built consensus libraries instead.

## Inputs

- Extracted MS1 and MS2 scans (mzML or mzXML format)
- User-provided metadata file (CSV, TSV, or structured text with retention time, m/z, compound name, molecular weight, annotation fields)
- User-specified m/z and retention time tolerance windows

## Outputs

- GNPS-compatible spectral library file (merged MS1/MS2 scan records with metadata headers)
- Structurally validated spectral library in GNPS standard format ready for library search queries

## How to apply

Load the extracted scan pairs in mzML/mzXML format from the preceding extraction step. Parse the user-provided metadata file using a structured format reader that captures retention time, m/z, compound name, molecular weight, and annotation fields. Match each extracted scan pair to metadata records by m/z and retention time within user-specified tolerance windows (tolerance values are user-configurable). Construct GNPS-style library entries by combining the matched scan data, metadata fields, and standardized GNPS headers. Finally, serialize the merged records into a GNPS-compatible spectral library output format. Correct matching depends on accurate tolerance specification—use tight windows (e.g., 0.01 m/z) for high-resolution data to avoid cross-contamination across adjacent compounds.

## Related tools

- **MergeION2** (R package that implements spectral library record structuring, including scan matching, metadata merging, and GNPS-style serialization) — https://github.com/daniellyz/MergeION2
- **GNPS** (Defines the spectral library record schema and standardized headers used for output serialization)

## Examples

```
# Load MergeION2, read extracted scans and metadata, then structure into GNPS library
# (Conceptual R pseudocode based on README workflow; exact function name not explicitly provided in README)
mzml_file <- "extracted_scans.mzML"
metadata_file <- "user_metadata.csv"
metadata <- read.csv(metadata_file)
# MergeION2 would call a merge function with scan data, metadata, and tolerance parameters
# library_output <- merge_scans_to_library(mzml_file, metadata, mz_tol=0.01, rt_tol=10)
```

## Evaluation signals

- All extracted scan pairs are matched to metadata records; no scans remain unassigned (100% match rate or user-acceptable partial match threshold achieved).
- Output spectral library conforms to GNPS schema: each record contains valid MS1 precursor m/z, MS2 fragment m/z-intensity pairs, retention time, compound name, molecular weight, and standardized header fields.
- Matched m/z values and retention times fall within user-specified tolerance windows (validate by sampling records and computing observed Δm/z and ΔRT).
- Library is readable and queryable by downstream tools (e.g., library_query() in MergeION2 executes without parsing errors).
- Metadata carryover is complete: no metadata fields are lost or corrupted during merge; spot-check a sample of output records against the source metadata file.

## Limitations

- Matching is sensitive to tolerance window specification; overly tight windows may leave scans unmatched, while overly loose windows may cause false matches across nearby compounds.
- The skill requires well-curated input metadata; missing or malformed m/z or retention time values will cause matching failures or skipped records.
- Currently supports mzML/mzXML formats; raw proprietary formats (Thermo .raw, Waters .raw, Bruker .d) must be converted first.
- MergeION2 library search algorithms work best on ESI-MS/MS spectra in positive ion mode; negative ion or other ionization modes may have reduced coverage in pre-built consensus libraries.

## Evidence

- [other] Defines the core structuring workflow: "Load extracted MS1 and MS2 scans (in mzML/mzXML format) from the preceding extraction step. Parse user-provided metadata file (retention time, m/z, compound name, molecular weight, and annotation"
- [readme] Motivates local library structuring: "Building a local high quality spectral library is an essentiel step thus often lacking in metabolomics and pharmaceutical laboratories. This is often due to the data confidentiality (e.g drug"
- [readme] Describes the output format standard: "They are then merged into a GNPS-style spectral library combining user-provided metadata"
- [readme] Specifies supported input formats: "It is compatible with mzML/mzXML format converted from Thermo, Water or Bruker data files, in either DDA (Data-driven acquisition) or targeted MS/MS-mode"
