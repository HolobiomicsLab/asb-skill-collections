---
name: feature-table-normalization
description: Use when you have peak/feature tables from one or more peak picking tools (MZmine, XCMS, MS-DIAL, Compound Discoverer) and need to ingest them into LipidMatch or combine results from multiple tools in a single lipidomics workflow.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-table-normalization

## Summary

Standardize and validate peak/feature tables exported from multiple upstream peak picking tools (MZmine, XCMS, MS-DIAL, Compound Discoverer) into a unified schema for downstream lipidomics matching. This skill detects the source tool, routes to the appropriate parser, extracts core columns (m/z, retention time, intensity, feature ID, MS/MS data), validates field ranges, and outputs a normalized table with standardized column names and source tool metadata.

## When to use

You have peak/feature tables from one or more peak picking tools (MZmine, XCMS, MS-DIAL, Compound Discoverer) and need to ingest them into LipidMatch or combine results from multiple tools in a single lipidomics workflow. The input files have different column names, metadata field structures, and data formats depending on their origin tool.

## When NOT to use

- Input is already a unified feature table in LipidMatch's standardized schema
- Input is raw MS data (mzML, mzXML, or vendor binary format) — use peak picking first
- Input is from Waters instruments — LipidMatch does not currently support Waters files

## Inputs

- MZmine feature table (CSV/TSV with columns: Feature ID, Best m/z, retention time, intensity)
- XCMS feature table (CSV/TSV with columns: mz, mzmin, mzmax, rt, intensity)
- MS-DIAL feature table (CSV/TSV with column: Alignment ID, m/z, retention time, intensity)
- Compound Discoverer feature table (CSV/TSV with columns: Mass, Retention Time, intensity)

## Outputs

- Unified normalized feature table (standardized schema with columns: feature_id, mz, retention_time, intensity, source_tool, ms_ms_data [if present])
- Validation report (counts of records, fields checked, range violations, missing values)

## How to apply

First, detect the upstream peak-picking tool by inspecting file headers, column names, or metadata fields (e.g., MZmine feature tables contain 'Feature ID' and 'Best m/z'; XCMS output contains 'mz', 'mzmin', 'mzmax'; MS-DIAL exports include 'Alignment ID'; Compound Discoverer produces 'Mass' and 'Retention Time' columns). Route the input table to the corresponding parser module (one for each of MZmine, XCMS, MS-DIAL, Compound Discoverer). Extract and normalize core columns: m/z, retention time (or scan number), intensity, feature/peak identifier, and MS/MS spectrum data (if present). Validate that all required fields are present and within expected ranges (m/z > 0, retention time ≥ 0, intensity ≥ 0). Output a unified feature table with standardized column names and metadata tags identifying the source tool, ready for downstream LipidMatch matching.

## Related tools

- **MZmine** (Peak picking tool; produces feature tables with Feature ID and Best m/z columns)
- **XCMS** (Peak picking tool; produces feature tables with mz, mzmin, mzmax, rt columns)
- **MS-DIAL** (Peak picking tool; produces feature tables with Alignment ID and retention time columns)
- **Compound Discoverer** (Peak picking tool; produces feature tables with Mass and Retention Time columns)
- **LipidMatch** (Downstream lipidomics matching software that accepts normalized feature tables) — https://github.com/GarrettLab-UF/LipidMatch

## Evaluation signals

- All required columns (mz, retention_time, intensity, feature_id) are present in output table
- m/z values are > 0, retention time values are ≥ 0, intensity values are ≥ 0 for all records
- Output table contains source_tool metadata field correctly identifying the origin peak picker
- No records are dropped during normalization; input row count equals output row count (or discrepancies are logged with reason)
- Output table successfully ingests into downstream LipidMatch matching without schema errors

## Limitations

- LipidMatch does not currently support Waters files, so Waters peak picker output cannot be normalized for LipidMatch integration
- Tool detection relies on column name inspection; non-standard or user-modified column headers may cause incorrect tool identification
- MS/MS spectrum data extraction depends on presence of these fields in the source tool output; some peak pickers may not export MS/MS annotations
- Validation checks enforce m/z > 0, retention_time ≥ 0, intensity ≥ 0, but do not detect biological implausibility (e.g., extreme retention times or intensity values)

## Evidence

- [other] Detect the upstream peak-picking tool by inspecting file headers, column names, or metadata fields (e.g., MZmine feature tables contain 'Feature ID' and 'Best m/z'; XCMS output contains 'mz', 'mzmin', 'mzmax'; MS-DIAL exports include 'Alignment ID'; Compound Discoverer produces 'Mass' and 'Retention Time' columns).: "Detect the upstream peak-picking tool by inspecting file headers, column names, or metadata fields (e.g., MZmine feature tables contain 'Feature ID' and 'Best m/z'; XCMS output contains 'mz',"
- [other] Extract and normalize core columns: m/z, retention time (or scan number), intensity, feature/peak identifier, and MS/MS spectrum data (if present). Validate that all required fields are present and within expected ranges (m/z > 0, retention time ≥ 0, intensity ≥ 0).: "Extract and normalize core columns: m/z, retention time (or scan number), intensity, feature/peak identifier, and MS/MS spectrum data (if present). Validate that all required fields are present and"
- [readme] LipidMatch is modular, allowing it to fit in various workflows you may have in your lab. For example LipidMatch can be used with various peak picking software (for example MZmine, XCMS, MS-DIAL, and Compound Discoverer), and combine results from other lipidomics software.: "LipidMatch is modular, allowing it to fit in various workflows you may have in your lab. For example LipidMatch can be used with various peak picking software (for example MZmine, XCMS, MS-DIAL, and"
- [readme] The software does not currently support Waters files.: "The software does not currently support Waters files."
- [other] Output a unified feature table with standardized column names and metadata tags identifying the source tool, ready for downstream LipidMatch matching.: "Output a unified feature table with standardized column names and metadata tags identifying the source tool, ready for downstream LipidMatch matching."
