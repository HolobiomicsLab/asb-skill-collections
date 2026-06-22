---
name: file-format-parsing-and-validation
description: Use when you have peak/feature tables from one or more of MZmine, XCMS, MS-DIAL, or Compound Discoverer and need to ingest them into LipidMatch for lipid identification. The input files are in tabular format (CSV, TSV, or Excel) and their upstream tool origin may be unknown or mixed.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MZmine
  - XCMS
  - MS-DIAL
  - Compound Discoverer
  - LipidMatch
  techniques:
  - LC-MS
derived_from:
- doi: 10.1186/s12859-017-1744-3
  title: lipidmatch
evidence_spans:
- LipidMatch can be used with various peak picking software (for example MZmine, XCMS, MS-DIAL, and Compound Discoverer)
- for example MZmine, XCMS, MS-DIAL, and Compound Discoverer
- LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidmatch_cq
    doi: 10.1186/s12859-017-1744-3
    title: lipidmatch
  dedup_kept_from: coll_lipidmatch_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s12859-017-1744-3
  all_source_dois:
  - 10.1186/s12859-017-1744-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# file-format-parsing-and-validation

## Summary

Detect, parse, and validate peak/feature table outputs from multiple upstream mass spectrometry peak-picking tools (MZmine, XCMS, MS-DIAL, Compound Discoverer) by inspecting headers and column signatures, then normalize them into a unified feature table schema for downstream lipidomics analysis. This skill enables LipidMatch to accept heterogeneous tool outputs and integrate them into a single workflow.

## When to use

You have peak/feature tables from one or more of MZmine, XCMS, MS-DIAL, or Compound Discoverer and need to ingest them into LipidMatch for lipid identification. The input files are in tabular format (CSV, TSV, or Excel) and their upstream tool origin may be unknown or mixed. Use this skill when you need to standardize column names, validate numeric ranges, and tag metadata provenance before matching against lipid libraries.

## When NOT to use

- Input is already in LipidMatch's unified feature table format or from an unsupported peak-picking tool (e.g., Waters)
- Input file is not tabular or does not contain recognizable peak-picking tool headers
- The analysis requires Waters instrument data, which LipidMatch does not currently support

## Inputs

- Peak/feature table from MZmine (CSV/TSV with 'Feature ID', 'Best m/z' columns)
- Peak/feature table from XCMS (CSV/TSV with 'mz', 'mzmin', 'mzmax' columns)
- Peak/feature table from MS-DIAL (CSV/TSV with 'Alignment ID' column)
- Peak/feature table from Compound Discoverer (CSV/TSV with 'Mass', 'Retention Time' columns)

## Outputs

- Unified feature table with standardized columns: m/z, retention time, intensity, feature identifier, source tool metadata
- Validation report (presence/absence of required fields, numeric range violations)

## How to apply

Inspect the input file's header row and column names to identify the source tool: MZmine files contain 'Feature ID' and 'Best m/z'; XCMS output includes 'mz', 'mzmin', 'mzmax'; MS-DIAL exports include 'Alignment ID'; Compound Discoverer produces 'Mass' and 'Retention Time' columns. Route the file to the corresponding parser module. Extract and normalize core columns: m/z, retention time (or scan number), intensity, feature/peak identifier, and MS/MS spectrum data if present. Validate that all required fields are present and within expected ranges (m/z > 0, retention time ≥ 0, intensity ≥ 0). Output a unified feature table with standardized column names and metadata tags identifying the source tool, ready for LipidMatch lipid matching.

## Related tools

- **MZmine** (Source peak-picking tool; produces feature tables with 'Feature ID' and 'Best m/z' column signatures)
- **XCMS** (Source peak-picking tool; produces feature tables with 'mz', 'mzmin', 'mzmax' columns)
- **MS-DIAL** (Source peak-picking tool; produces feature tables with 'Alignment ID' column)
- **Compound Discoverer** (Source peak-picking tool; produces feature tables with 'Mass' and 'Retention Time' columns)
- **LipidMatch** (Downstream tool that ingests and processes normalized feature tables for lipid identification) — https://github.com/GarrettLab-UF/LipidMatch

## Evaluation signals

- All required columns (m/z, retention time, intensity, feature identifier) are present in the output table after parsing
- All m/z values are > 0, retention times are ≥ 0, and intensities are ≥ 0
- Source tool is correctly identified from header inspection and metadata tag is added to output
- Column names are standardized (e.g., all 'Best m/z' renamed to 'm/z'; all 'Mass' renamed to 'm/z')
- No rows are lost during parsing and normalization; row count remains constant

## Limitations

- LipidMatch does not currently support Waters instrument files
- Parser assumes standard column naming conventions; non-standard headers from custom tool exports may not be detected
- Validation checks only verify field presence and numeric range; they do not assess chemical plausibility (e.g., whether m/z matches expected lipid species)
- MS/MS spectrum data extraction depends on consistent formatting across tools; missing or malformed MS/MS blocks may be silently skipped

## Evidence

- [other] Detect the upstream peak-picking tool by inspecting file headers, column names, or metadata fields (e.g., MZmine feature tables contain 'Feature ID' and 'Best m/z'; XCMS output contains 'mz', 'mzmin', 'mzmax'; MS-DIAL exports include 'Alignment ID'; Compound Discoverer produces 'Mass' and 'Retention Time' columns).: "Detect the upstream peak-picking tool by inspecting file headers, column names, or metadata fields (e.g., MZmine feature tables contain 'Feature ID' and 'Best m/z'; XCMS output contains 'mz',"
- [other] Extract and normalize core columns: m/z, retention time (or scan number), intensity, feature/peak identifier, and MS/MS spectrum data (if present).: "Extract and normalize core columns: m/z, retention time (or scan number), intensity, feature/peak identifier, and MS/MS spectrum data (if present)."
- [other] Validate that all required fields are present and within expected ranges (m/z > 0, retention time ≥ 0, intensity ≥ 0).: "Validate that all required fields are present and within expected ranges (m/z > 0, retention time ≥ 0, intensity ≥ 0)."
- [readme] LipidMatch is modular, allowing it to fit in various workflows you may have in your lab. For example LipidMatch can be used with various peak picking software (for example MZmine, XCMS, MS-DIAL, and Compound Discoverer), and combine results from other lipidomics software.: "LipidMatch can be used with various peak picking software (for example MZmine, XCMS, MS-DIAL, and Compound Discoverer)"
- [readme] The software does not currently support Waters files.: "The software does not currently support Waters files."
