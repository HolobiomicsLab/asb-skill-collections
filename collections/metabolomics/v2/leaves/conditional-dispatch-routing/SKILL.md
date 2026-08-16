---
name: conditional-dispatch-routing
description: Use when you have received a peak/feature table from an unknown or variable
  upstream peak-picking tool and need to ingest it into LipidMatch or a similar unified
  workflow. The input file format, column naming, or metadata structure is tool-specific
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0625
  tools:
  - MZmine
  - XCMS
  - MS-DIAL
  - Compound Discoverer
  - LipidMatch
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1186/s12859-017-1744-3
  title: lipidmatch
evidence_spans:
- LipidMatch can be used with various peak picking software (for example MZmine, XCMS,
  MS-DIAL, and Compound Discoverer)
- for example MZmine, XCMS, MS-DIAL, and Compound Discoverer
- LipidMatch identifications are obtained by matching experimental fragment m/z values
  with simulated library m/z values
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

# conditional-dispatch-routing

## Summary

Route peak/feature table inputs from heterogeneous upstream peak-picking tools (MZmine, XCMS, MS-DIAL, Compound Discoverer) to tool-specific parser modules by detecting file format signatures. This skill enables a unified lipidomics workflow to accept and normalize outputs from multiple vendors and software packages.

## When to use

You have received a peak/feature table from an unknown or variable upstream peak-picking tool and need to ingest it into LipidMatch or a similar unified workflow. The input file format, column naming, or metadata structure is tool-specific (e.g., MZmine feature tables contain 'Feature ID' and 'Best m/z'; XCMS output contains 'mz', 'mzmin', 'mzmax'; MS-DIAL exports include 'Alignment ID'; Compound Discoverer produces 'Mass' and 'Retention Time' columns), and you must normalize it to a common internal schema before downstream matching or analysis.

## When NOT to use

- Input is already a unified, pre-normalized feature table in a known internal schema — skip routing and proceed directly to matching.
- File format is from an unsupported peak-picking tool (e.g., Waters instruments are explicitly not supported by LipidMatch).
- Peak table is malformed, missing critical columns (m/z, intensity, retention time), or contains data outside expected ranges (negative m/z, negative intensity).

## Inputs

- peak/feature table from MZmine, XCMS, MS-DIAL, or Compound Discoverer (CSV, TSV, or vendor-native format)
- file header and column metadata

## Outputs

- unified feature table with standardized column names (m/z, retention time, intensity, feature ID, etc.)
- metadata tag indicating upstream tool source
- validated feature/peak records ready for LipidMatch lipid identification

## How to apply

Inspect the input file's header row, column names, and metadata fields to identify the upstream tool signature (e.g., presence of 'Feature ID' → MZmine; 'mzmin'/'mzmax' → XCMS; 'Alignment ID' → MS-DIAL; 'Mass'/'Retention Time' → Compound Discoverer). Route the file to the corresponding parser module designed for that tool. Extract and normalize core columns: m/z, retention time (or scan number), intensity, feature/peak identifier, and MS/MS spectrum data if present. Validate that all required fields are present and within expected value ranges (m/z > 0, retention time ≥ 0, intensity ≥ 0). Output a unified feature table with standardized column names and metadata tags identifying the source tool, ready for downstream LipidMatch matching.

## Related tools

- **MZmine** (Source peak-picking tool; outputs feature tables with 'Feature ID' and 'Best m/z' columns that must be detected and routed to MZmine parser module.)
- **XCMS** (Source peak-picking tool; outputs feature tables with 'mz', 'mzmin', 'mzmax' columns that must be detected and routed to XCMS parser module.)
- **MS-DIAL** (Source peak-picking tool; outputs feature tables with 'Alignment ID' column that must be detected and routed to MS-DIAL parser module.)
- **Compound Discoverer** (Source peak-picking tool; outputs feature tables with 'Mass' and 'Retention Time' columns that must be detected and routed to Compound Discoverer parser module.)
- **LipidMatch** (Downstream consumer of the unified feature table; performs lipid identification by matching experimental fragment m/z values with simulated library m/z values.) — https://github.com/GarrettLab-UF/LipidMatch

## Evaluation signals

- The input file is successfully classified to a single tool signature (MZmine, XCMS, MS-DIAL, or Compound Discoverer) based on column name inspection.
- All required core columns (m/z, retention time, intensity, feature/peak identifier) are present in the output unified feature table.
- Validation checks pass: m/z > 0, retention time ≥ 0, intensity ≥ 0 for all records.
- Output feature table column names and order are identical across all tool-specific inputs (standardization invariant).
- Metadata tag correctly identifies the source tool and is preserved through downstream LipidMatch processing.

## Limitations

- LipidMatch does not currently support Waters files, so Waters peak-picking outputs cannot be routed or ingested.
- The routing detection relies on heuristic inspection of column names and headers; ambiguous or non-standard naming conventions in vendor outputs may cause misclassification.
- Conditional routing assumes exactly one tool signature per file; mixed or hybrid feature tables combining outputs from multiple tools are not handled.
- User-defined or custom peak-picking tools not in the supported set (MZmine, XCMS, MS-DIAL, Compound Discoverer) will fail detection and require manual adapter development.

## Evidence

- [other] Detect the upstream peak-picking tool by inspecting file headers, column names, or metadata fields (e.g., MZmine feature tables contain 'Feature ID' and 'Best m/z'; XCMS output contains 'mz', 'mzmin', 'mzmax'; MS-DIAL exports include 'Alignment ID'; Compound Discoverer produces 'Mass' and 'Retention Time' columns).: "Detect the upstream peak-picking tool by inspecting file headers, column names, or metadata fields (e.g., MZmine feature tables contain 'Feature ID' and 'Best m/z'; XCMS output contains 'mz',"
- [other] Route the input table to the corresponding parser module (one for each of MZmine, XCMS, MS-DIAL, Compound Discoverer).: "Route the input table to the corresponding parser module (one for each of MZmine, XCMS, MS-DIAL, Compound Discoverer)."
- [other] Validate that all required fields are present and within expected ranges (m/z > 0, retention time ≥ 0, intensity ≥ 0).: "Validate that all required fields are present and within expected ranges (m/z > 0, retention time ≥ 0, intensity ≥ 0)."
- [readme] LipidMatch is modular, allowing it to fit in various workflows you may have in your lab. For example LipidMatch can be used with various peak picking software (for example MZmine, XCMS, MS-DIAL, and Compound Discoverer), and combine results from other lipidomics software.: "LipidMatch is modular, allowing it to fit in various workflows you may have in your lab. For example LipidMatch can be used with various peak picking software (for example MZmine, XCMS, MS-DIAL, and"
- [readme] The software does not currently support Waters files.: "The software does not currently support Waters files."
