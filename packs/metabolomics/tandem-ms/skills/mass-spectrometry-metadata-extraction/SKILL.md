---
name: mass-spectrometry-metadata-extraction
description: Use when you have peak/feature tables from one or more of MZmine, XCMS, MS-DIAL, or Compound Discoverer and need to integrate them into a unified lipidomics workflow (e.g., LipidMatch).
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
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-metadata-extraction

## Summary

Extract and normalize metadata (m/z, retention time, intensity, feature identifiers, MS/MS spectrum data) from peak/feature tables produced by diverse upstream peak-picking tools (MZmine, XCMS, MS-DIAL, Compound Discoverer) to enable unified downstream lipidomics analysis. This skill detects the source tool by inspecting file headers and column signatures, then routes the table to a tool-specific parser that normalizes core columns and validates data integrity.

## When to use

You have peak/feature tables from one or more of MZmine, XCMS, MS-DIAL, or Compound Discoverer and need to integrate them into a unified lipidomics workflow (e.g., LipidMatch). The input tables have heterogeneous column names and metadata structures depending on their upstream tool, and you need a standardized representation with validated m/z, retention time, intensity, and feature identifiers before lipid matching or combination with results from other lipidomics software.

## When NOT to use

- Input is already a unified feature table from a single, standardized format (e.g., already normalized by LipidMatch or another downstream tool).
- Input data is from peak-picking tools not supported by the adapter (e.g., Waters files, which LipidMatch does not currently support).
- You need only tool-agnostic peak detection without integration into a multi-tool workflow.

## Inputs

- Peak/feature table in tool-native format (MZmine .csv, XCMS matrix, MS-DIAL .txt, Compound Discoverer export)
- File header and column name metadata

## Outputs

- Unified feature table with standardized column names (m/z, retention_time, intensity, feature_id, ms_ms_spectrum_data)
- Source tool identifier and metadata tags
- Validation report (fields present, value ranges, missing or out-of-range entries)

## How to apply

Inspect the input file header, column names, and any metadata fields to identify the source peak-picking tool (e.g., MZmine feature tables contain 'Feature ID' and 'Best m/z'; XCMS output contains 'mz', 'mzmin', 'mzmax'; MS-DIAL exports include 'Alignment ID'; Compound Discoverer produces 'Mass' and 'Retention Time' columns). Route the table to the corresponding parser module. Extract and normalize the core columns: m/z, retention time (or scan number), intensity, feature/peak identifier, and any MS/MS spectrum data. Validate that all required fields are present and within expected ranges (m/z > 0, retention time ≥ 0, intensity ≥ 0). Output a unified feature table with standardized column names and metadata tags identifying the source tool, ready for downstream LipidMatch matching or integration with other lipidomics results.

## Related tools

- **MZmine** (Source peak-picking tool; generates feature tables with 'Feature ID' and 'Best m/z' columns)
- **XCMS** (Source peak-picking tool; generates feature tables with 'mz', 'mzmin', 'mzmax' columns)
- **MS-DIAL** (Source peak-picking tool; generates exports with 'Alignment ID' column)
- **Compound Discoverer** (Source peak-picking tool; produces 'Mass' and 'Retention Time' columns)
- **LipidMatch** (Downstream consumer of normalized feature tables; matches experimental fragment m/z values with simulated library m/z values) — https://github.com/GarrettLab-UF/LipidMatch

## Evaluation signals

- All input rows are successfully assigned to a recognized peak-picking tool based on column signature detection; no rows are rejected as ambiguous or unrecognized.
- Normalized output table contains exactly the required columns (m/z, retention_time, intensity, feature_id, ms_ms_spectrum_data where applicable) with no missing or NaN values in mandatory fields.
- Validation checks pass: m/z > 0, retention_time ≥ 0, intensity ≥ 0 for all rows; report any out-of-range entries as errors.
- Metadata tags in output correctly identify the source tool (e.g., 'source_tool: MZmine') for each row.
- Downstream LipidMatch matching or multi-tool combination step runs without schema errors, confirming column standardization was successful.

## Limitations

- LipidMatch does not currently support Waters files, so metadata extraction cannot be applied to Waters peak-picking outputs.
- Adapter assumes peak-picking tools produce output in their standard, canonical format; non-standard or manually edited table structures may not be recognized.
- Retention time normalization assumes consistent units (minutes or scans) within each input file; cross-file alignment is not performed by this skill.
- MS/MS spectrum data presence and format vary by tool; extraction assumes tool-specific column naming conventions.

## Evidence

- [other] Tool detection logic: "Detect the upstream peak-picking tool by inspecting file headers, column names, or metadata fields (e.g., MZmine feature tables contain 'Feature ID' and 'Best m/z'; XCMS output contains 'mz',"
- [other] Normalization and validation steps: "Extract and normalize core columns: m/z, retention time (or scan number), intensity, feature/peak identifier, and MS/MS spectrum data (if present). Validate that all required fields are present and"
- [other] Output specification: "Output a unified feature table with standardized column names and metadata tags identifying the source tool, ready for downstream LipidMatch matching"
- [readme] Multi-tool integration motivation: "LipidMatch is modular, allowing it to fit in various workflows you may have in your lab. For example LipidMatch can be used with various peak picking software (for example MZmine, XCMS, MS-DIAL, and"
- [readme] Waters file limitation: "The software does not currently support Waters files"
