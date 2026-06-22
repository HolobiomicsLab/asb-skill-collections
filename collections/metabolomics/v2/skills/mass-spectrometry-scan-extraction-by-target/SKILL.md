---
name: mass-spectrometry-scan-extraction-by-target
description: Use when you have raw LC-MS/MS chromatogram files in mzML/mzXML format (converted from Thermo, Waters, or Bruker instruments) acquired in DDA or targeted MS/MS mode, and you need to isolate specific MS1 precursors and their corresponding MS2 fragments based on known m/z values and optional.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3637
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - meRgeION2
  - MergeION2
  - GNPS
  - MassBank
  - DrugBank
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
---

# Mass spectrometry scan extraction by target

## Summary

Extract MS1 and MS2 scans from raw chromatogram files (mzML/mzXML format) by matching user-specified m/z and retention time targets, enabling construction of local spectral libraries without data sharing. This skill is essential for building confidential spectral libraries in metabolomics and pharmaceutical workflows.

## When to use

You have raw LC-MS/MS chromatogram files in mzML/mzXML format (converted from Thermo, Waters, or Bruker instruments) acquired in DDA or targeted MS/MS mode, and you need to isolate specific MS1 precursors and their corresponding MS2 fragments based on known m/z values and optional retention time windows to build a local spectral library.

## When NOT to use

- Input files are already in processed or library format (e.g., .mgf, .msp, or pre-compiled spectral library) rather than raw chromatogram files
- Your workflow requires real-time or streaming analysis of incoming MS data rather than batch extraction from stored files
- Chromatogram files are in vendor-proprietary binary formats (.raw, .d) that have not been converted to mzML/mzXML

## Inputs

- One or multiple mzML/mzXML chromatogram files converted from Thermo, Waters, or Bruker data files
- User-provided m/z targets (numeric list or table)
- Optional retention time ranges (min/max in minutes or seconds)
- User-provided metadata (compound name, class, provenance)

## Outputs

- Extracted MS1 and MS2 scan spectra with metadata (m/z, retention time, scan number, intensity)
- GNPS-style spectral library in structured format with combined user-provided metadata
- Tabular or structured output file ready for library search and annotation

## How to apply

Load one or more mzML/mzXML files using a mass spectrometry data parser compatible with Thermo, Waters, or Bruker formats. Parse user-provided m/z targets and optional retention time ranges into a query specification. Scan the chromatogram data to identify MS1 scans matching the target m/z values within tolerance and retention time bounds. Extract corresponding MS2 fragment spectra for matched precursors. Compile extracted MS1 and MS2 scans into a structured output format with scan metadata (m/z, retention time, scan number, intensity), then merge them into a GNPS-style spectral library combining user-provided metadata.

## Related tools

- **MergeION2** (Primary R package for batch extraction of MS1/MS2 scans from mzML/mzXML files, spectral library construction, and library search) — https://github.com/daniellyz/MergeION2
- **GNPS** (Reference spectral library format and public database for library search, annotation, and molecular networking)
- **MassBank** (Public reference spectral database for unknown spectrum annotation and compound identification)
- **DrugBank** (Public database for drug structure search and annotation during library lookup)

## Examples

```
params.query.sp = list(prec_mz = 369.232, use_prec = T, polarity = "Positive", method = "Cosine", min_frag_match = 6, min_score = 0); search_result = library_query(input_library = library1c, query_spectrum = query.sp, params.query.sp = params.query.sp)
```

## Evaluation signals

- Extracted MS1 scans match the specified m/z targets within the declared tolerance and fall within the provided retention time bounds (if specified)
- All extracted MS2 scans are correctly paired to their precursor MS1 scans and contain non-empty fragment ion lists
- Output spectral library metadata schema matches GNPS format with all user-provided fields correctly populated
- Scan extraction output includes complete metadata columns (m/z, retention time, scan number, intensity) with no null values for successfully extracted scans
- Library search using extracted spectra against the pre-compiled GNPS_MASSBANK_PROCESSED_POS_CONSENSUS1 database returns expected compound hits with Cosine similarity ≥ 0.7 for known reference standards

## Limitations

- Currently, the pre-compiled spectral database contains only ESI-MS/MS spectra in positive ion mode; negative ion mode data requires alternative reference libraries
- Extraction accuracy depends on user-provided m/z precision and retention time bounds; incorrect or overly broad parameters may result in co-eluting contaminant peaks or missed scans
- Compatibility is limited to mzML/mzXML formats; vendor proprietary binary formats (.raw, .d, .raw) must be pre-converted by external software (e.g., ProteoWizard)
- No changelog available; version and update history tracking is not documented in the repository

## Evidence

- [readme] extracting MS1 and MS2 scans from one or multiple raw chromatogram files according to m/z (and retention time) provided by users: "It works by extracting MS1 and MS2 scans from one or multiple raw chromatogram files according to m/z (and retention time) provided by users"
- [other] MergeION performs scan extraction by reading mzML/mzXML format files converted from Thermo, Waters, or Bruker instruments and selects MS1 and MS2 scans matching user-specified m/z and optional retention time parameters: "MergeION performs scan extraction by reading one or multiple mzML/mzXML format files converted from Thermo, Water, or Bruker instruments and selects MS1 and MS2 scans matching user-specified m/z and"
- [readme] compatible with mzML/mzXML format converted from Thermo, Waters, or Bruker data files in either DDA or targeted MS/MS mode: "It is compatible with mzML/mzXML format converted from Thermo, Water or Bruker data files, in either DDA (Data-driven acquisition) or targeted MS/MS-mode"
- [readme] They are then merged into a GNPS-style spectral library combining user-provided metadata: "They are then merged into a GNPS-style spectral library combining user-provided metadata"
- [readme] Currently ESI-MS/MS spectra in our collection are all in positive ion mode: "Currently ESI-MS/MS spectra in our collection are all in positive ion mode"
- [intro] Building a local high quality spectral library is an essential step in metabolomics and pharmaceutical laboratories, often lacking due to data confidentiality concerns: "Building a local high quality spectral library is an essentiel step thus often lacking in metabolomics and pharmaceutical laboratories. This is often due to the data confidentiality"
