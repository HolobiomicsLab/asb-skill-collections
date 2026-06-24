---
name: gnps-library-format-assembly
description: Use when you have extracted MS1 and MS2 scans (in mzML/mzXML format)
  from raw chromatogram files and possess user-provided metadata (retention time,
  m/z, compound name, molecular weight, annotation fields) that must be combined into
  a single structured library entry suitable for spectral library.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3347
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - GNPS
  - meRgeION2
  - MergeION2
  - MassBank
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.2c04343
  title: MeRgeION
evidence_spans:
- merged into a GNPS-style spectral library
- search and annotate an unknown spectrum in their local database or public databases
  (i.e. drug structures in GNPS, MASSBANK and DrugBANK)
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

# GNPS-Library-Format Assembly

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Merge extracted MS1 and MS2 scans with user-provided metadata into a GNPS-style spectral library record. This skill enables construction of shareable, standardized spectral library entries compatible with GNPS and other public repositories while preserving local data confidentiality.

## When to use

You have extracted MS1 and MS2 scans (in mzML/mzXML format) from raw chromatogram files and possess user-provided metadata (retention time, m/z, compound name, molecular weight, annotation fields) that must be combined into a single structured library entry suitable for spectral library search or public deposition.

## When NOT to use

- Raw chromatogram files have not yet been converted to mzML/mzXML format; extraction must precede assembly.
- Metadata file lacks required fields (m/z, retention time, or compound identifiers); assembly cannot proceed without matching criteria.
- Input scans are from Data-Independent Acquisition (DIA) mode where MS1 and MS2 pairing cannot be reliably established without additional precursor information.
- You intend to build a public spectral library without data confidentiality constraints; direct deposition to GNPS or MassBank may be more appropriate than local assembly.

## Inputs

- Extracted MS1 and MS2 scans (mzML/mzXML format)
- User-provided metadata file (CSV or structured format with retention time, m/z, compound name, molecular weight, annotation fields)
- m/z tolerance window (ppm or Da)
- Retention time tolerance window (seconds or minutes)

## Outputs

- GNPS-style spectral library file (merged MS1/MS2 scans with standardized metadata)
- Spectral library record with standardized headers and compound annotations

## How to apply

Load the extracted MS1 and MS2 scans in mzML/mzXML format alongside a structured metadata file. Parse the metadata using a format reader that recognizes retention time, m/z, compound name, molecular weight, and annotation fields. Match each extracted scan pair to metadata records by m/z and retention time using user-specified tolerance windows (typically within specified m/z and RT precision). Construct GNPS-style library entries by combining scan data with matched metadata fields and applying standardized GNPS headers. Serialize the complete merged library into GNPS-compatible spectral library output format. Validate that precursor m/z, retention time windows, and metadata fields align across matched records.

## Related tools

- **MergeION2** (Core R package implementing MS1/MS2 scan merging, metadata parsing, m/z/RT matching, and GNPS-format serialization.) — https://github.com/daniellyz/MergeION2
- **GNPS** (Target spectral library format standard and optional destination for public library sharing.)
- **MassBank** (Reference spectral library used for validation and quality control of merged entries.)

## Examples

```
# In R, after loading MergeION2 and extracted MS1/MS2 scans:
merged_library <- merge_ms_metadata(ms1_scans = scans_ms1, ms2_scans = scans_ms2, metadata = user_metadata, mz_tol = 0.005, rt_tol = 30, output_format = 'GNPS')
```

## Evaluation signals

- Each extracted scan pair is successfully matched to exactly one metadata record within user-specified m/z and retention time tolerance windows.
- All GNPS-format headers are present and populated in output library entries (precursor m/z, retention time, compound name, INCHIKEY or equivalent structure identifier).
- Serialized library file is readable by GNPS library search tools and returns expected spectral similarity scores (e.g., cosine similarity > 0.5) when queried against reference spectra.
- Metadata fields do not contain null or missing values for required fields in matched records; unmatched scans are logged separately.
- Output file validates against GNPS spectral library schema (format, field order, data types).

## Limitations

- Matching relies on m/z and retention time tolerances; ambiguous matches (multiple metadata records within tolerance) may require manual review or stricter tolerance settings.
- Compatible only with mzML/mzXML formats converted from Thermo, Waters, or Bruker instruments; other vendor formats require prior conversion.
- Metadata file must be manually provided and pre-formatted; incomplete or inconsistent metadata will result in unmatched scans or malformed library entries.
- Current implementation focuses on ESI-MS/MS spectra in positive ion mode; negative ion mode support may be limited or absent.
- Data confidentiality depends on the output destination; sharing the assembled library to public databases will expose the combined metadata.

## Evidence

- [other] Assembly workflow overview: "Match each extracted scan pair to metadata records by m/z and retention time within user-specified tolerance windows. Construct GNPS-style library entries by combining scan data, metadata fields, and"
- [readme] Input file formats and metadata structure: "Load extracted MS1 and MS2 scans (in mzML/mzML format) from the preceding extraction step. Parse user-provided metadata file (retention time, m/z, compound name, molecular weight, and annotation"
- [other] Output serialization standard: "Serialize the merged library into a GNPS-compatible spectral library output format."
- [readme] Supported instrument platforms: "It is compatible with mzML/mzXML format converted from Thermo, Water or Bruker data files, in either DDA (Data-driven acquisition) or targeted MS/MS-mode"
- [readme] GNPS library construction rationale: "Building a local high quality spectral library is an essentiel step thus often lacking in metabolomics and pharmaceutical laboratories. This is often due to the data confidentiality"
