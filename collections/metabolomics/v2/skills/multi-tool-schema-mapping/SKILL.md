---
name: multi-tool-schema-mapping
description: Use when you have peak/feature table outputs from one or more peak-picking
  tools (MZmine, XCMS, MS-DIAL, Compound Discoverer) with different column names and
  metadata structures, and you need to ingest them into LipidMatch or another unified
  lipidomics pipeline that requires consistent column.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
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

# multi-tool-schema-mapping

## Summary

Detect upstream peak-picking tool identity from file headers and column names, then route input feature tables through tool-specific parsers to extract, normalize, and validate core lipidomics columns (m/z, retention time, intensity, feature ID) into a unified schema. This skill enables LipidMatch to integrate peak tables from heterogeneous sources (MZmine, XCMS, MS-DIAL, Compound Discoverer) into a single standardized workflow.

## When to use

You have peak/feature table outputs from one or more peak-picking tools (MZmine, XCMS, MS-DIAL, Compound Discoverer) with different column names and metadata structures, and you need to ingest them into LipidMatch or another unified lipidomics pipeline that requires consistent column naming, data types, and validation ranges.

## When NOT to use

- Input is already a feature table in unified/standardized format (no tool detection needed)
- Input file is from a peak-picking tool not in the supported set (MZmine, XCMS, MS-DIAL, Compound Discoverer)
- Input is raw LC-MS/MS data (.mzML, .raw, .d) — run peak picking first to generate feature tables

## Inputs

- peak/feature table in tool-native format (MZmine .csv, XCMS .tsv, MS-DIAL .txt, Compound Discoverer export)
- file headers and column name metadata

## Outputs

- unified feature table with standardized columns (m/z, retention time, intensity, feature ID, MS/MS spectrum data)
- source tool identifier tag attached to output metadata

## How to apply

Inspect file headers, column names, and metadata fields to identify the source tool (e.g., MZmine tables contain 'Feature ID' and 'Best m/z'; XCMS output contains 'mz', 'mzmin', 'mzmax'; MS-DIAL exports include 'Alignment ID'; Compound Discoverer produces 'Mass' and 'Retention Time' columns). Route the table to the corresponding parser module for that tool. Extract core columns: m/z, retention time (or scan number), intensity, feature/peak identifier, and MS/MS spectrum data if present. Validate that all required fields are present and within expected ranges (m/z > 0, retention time ≥ 0, intensity ≥ 0). Output a unified feature table with standardized column names and metadata tags identifying the source tool for downstream LipidMatch matching.

## Related tools

- **MZmine** (upstream peak-picking tool; output feature tables inspected for 'Feature ID' and 'Best m/z' columns)
- **XCMS** (upstream peak-picking tool; output feature tables inspected for 'mz', 'mzmin', 'mzmax' columns)
- **MS-DIAL** (upstream peak-picking tool; output feature tables inspected for 'Alignment ID' column)
- **Compound Discoverer** (upstream peak-picking tool; output feature tables inspected for 'Mass' and 'Retention Time' columns)
- **LipidMatch** (downstream lipidomics identification tool that consumes unified feature tables from this schema mapper) — https://github.com/GarrettLab-UF/LipidMatch

## Evaluation signals

- Source tool correctly identified from header/column inspection; parser module route is appropriate for detected tool
- All required columns (m/z, retention time, intensity, feature ID) are present in output table with standardized names
- Numeric validation ranges hold: m/z > 0, retention time ≥ 0, intensity ≥ 0 for all rows
- Output metadata tag correctly identifies source tool and is carried through to downstream LipidMatch matching
- No data loss or truncation during column extraction; row count and intensity distribution match input

## Limitations

- Waters LC-MS/MS files are not currently supported by LipidMatch; feature tables from Waters peak-picking tools cannot be integrated
- Tool detection relies on heuristic inspection of column names and headers; ambiguous or malformed headers may fail to identify tool correctly
- Validation assumes standard numeric ranges for m/z and retention time; some specialized instruments or experiments may produce valid data outside these bounds

## Evidence

- [other] Detect upstream tool by inspecting headers, column names, or metadata; route to corresponding parser: "Detect the upstream peak-picking tool by inspecting file headers, column names, or metadata fields (e.g., MZmine feature tables contain 'Feature ID' and 'Best m/z'; XCMS output contains 'mz',"
- [other] Extract and validate core columns with numeric range checks: "Extract and normalize core columns: m/z, retention time (or scan number), intensity, feature/peak identifier, and MS/MS spectrum data (if present). 4. Validate that all required fields are present"
- [other] Output unified table with standardized columns and source metadata: "Output a unified feature table with standardized column names and metadata tags identifying the source tool, ready for downstream LipidMatch matching"
- [readme] LipidMatch is modular and fits various workflows with multiple peak-picking tools: "LipidMatch is modular, allowing it to fit in various workflows you may have in your lab. For example LipidMatch can be used with various peak picking software (for example MZmine, XCMS, MS-DIAL, and"
- [readme] Waters files not supported by LipidMatch: "The software does not currently support Waters files"
