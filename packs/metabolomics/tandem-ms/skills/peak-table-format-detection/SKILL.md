---
name: peak-table-format-detection
description: Use when when receiving a peak or feature table output from an unknown or variable upstream peak-picking tool, and you need to route it to the correct ingestion adapter (e.g., in LipidMatch) to normalize and validate it before lipid identification.
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

# peak-table-format-detection

## Summary

Automated detection of the upstream peak-picking tool (MZmine, XCMS, MS-DIAL, Compound Discoverer) from which a feature/peak table originated, enabling conditional routing to the appropriate parser module in a unified lipidomics workflow.

## When to use

When receiving a peak or feature table output from an unknown or variable upstream peak-picking tool, and you need to route it to the correct ingestion adapter (e.g., in LipidMatch) to normalize and validate it before lipid identification. Typical trigger: user provides a CSV or tabular file without explicit tool provenance metadata.

## When NOT to use

- Input is already a pre-validated unified feature table with standardized columns and source tool metadata tag
- Input is from a peak-picking tool not in the supported list (MZmine, XCMS, MS-DIAL, Compound Discoverer)
- Input file is corrupted, missing headers, or lacks sufficient diagnostic column signatures to distinguish tool origin

## Inputs

- Peak or feature table in tabular format (CSV, TSV, or proprietary text export)
- Table headers and column names
- Metadata or file header text indicating upstream processing

## Outputs

- Tool source identifier (one of: MZmine, XCMS, MS-DIAL, Compound Discoverer)
- Routing instruction to appropriate parser module
- Unified feature table with standardized column names and source tool metadata

## How to apply

Inspect the input table's file headers, column names, and metadata fields to identify diagnostic signatures unique to each tool. MZmine tables contain 'Feature ID' and 'Best m/z' columns; XCMS output contains 'mz', 'mzmin', 'mzmax'; MS-DIAL exports include 'Alignment ID'; Compound Discoverer produces 'Mass' and 'Retention Time' columns. Once identified, route the table to the corresponding tool-specific parser module. The parser then extracts and normalizes core columns (m/z, retention time or scan number, intensity, feature/peak identifier, and optional MS/MS spectrum data) and validates that all required fields are present and within expected ranges (m/z > 0, retention time ≥ 0, intensity ≥ 0). Output a unified feature table with standardized column names and metadata tags identifying the source tool.

## Related tools

- **LipidMatch** (Host workflow that conditionally ingests and normalizes peak tables from multiple upstream peak-picking tools) — https://github.com/GarrettLab-UF/LipidMatch
- **MZmine** (Upstream peak-picking tool; produces feature tables with diagnostic 'Feature ID' and 'Best m/z' columns)
- **XCMS** (Upstream peak-picking tool; produces feature tables with diagnostic 'mz', 'mzmin', 'mzmax' columns)
- **MS-DIAL** (Upstream peak-picking tool; produces feature tables with diagnostic 'Alignment ID' column)
- **Compound Discoverer** (Upstream peak-picking tool; produces feature tables with diagnostic 'Mass' and 'Retention Time' columns)

## Evaluation signals

- Detected tool identifier matches the known source tool (ground truth validation against metadata or user confirmation)
- All required normalized columns (m/z, retention time, intensity, feature ID) are present and non-empty in the output table
- Validated column values fall within expected ranges: m/z > 0, retention time ≥ 0, intensity ≥ 0
- Output unified feature table can be ingested without error by the downstream LipidMatch lipid matching module
- Source tool metadata tag is correctly appended to the output table header or metadata section

## Limitations

- Detection relies on heuristic column name and header inspection; files with non-standard naming conventions or manually edited headers may fail to match diagnostic signatures
- Currently supports only four upstream tools (MZmine, XCMS, MS-DIAL, Compound Discoverer); other peak pickers are not routable
- Waters instrument output is not currently supported by LipidMatch, so Waters peak tables cannot be processed end-to-end

## Evidence

- [other] Diagnostic column signatures for tool identification: "Detect the upstream peak-picking tool by inspecting file headers, column names, or metadata fields (e.g., MZmine feature tables contain 'Feature ID' and 'Best m/z'; XCMS output contains 'mz',"
- [other] Tool-specific parser routing and output normalization: "Route the input table to the corresponding parser module (one for each of MZmine, XCMS, MS-DIAL, Compound Discoverer). Extract and normalize core columns: m/z, retention time (or scan number),"
- [other] Validation of normalized feature table: "Validate that all required fields are present and within expected ranges (m/z > 0, retention time ≥ 0, intensity ≥ 0). Output a unified feature table with standardized column names and metadata tags"
- [readme] Modular workflow integration across multiple peak pickers: "LipidMatch is modular, allowing it to fit in various workflows you may have in your lab. For example LipidMatch can be used with various peak picking software (for example MZmine, XCMS, MS-DIAL, and"
