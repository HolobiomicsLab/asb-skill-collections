---
name: file-format-specification-compliance
description: Use when when preparing metabolomics data (feature tables, sample metadata)
  for ingestion into a SECIMTools standalone tool, or when validating that a tool
  has produced outputs in the correct format and location. Apply this skill when format
  ambiguity exists (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Galaxy Genomics Framework
  - SECIMTools suite
  license_tier: open
derived_from:
- doi: 10.1186/s12859-018-2134-1
  title: SECIMTools
evidence_spans:
- can be run in a standalone mode or via Galaxy Genomics Framework
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_secimtools_cq
    doi: 10.1186/s12859-018-2134-1
    title: SECIMTools
  dedup_kept_from: coll_secimtools_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s12859-018-2134-1
  all_source_dois:
  - 10.1186/s12859-018-2134-1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# file-format-specification-compliance

## Summary

Validate and ensure that metabolomics data inputs conform to the format specifications required by SECIMTools, and that outputs are produced in the expected structure and schema. This skill bridges raw or intermediate data representations to tool-compatible formats and verifies correctness of processing artifacts.

## When to use

When preparing metabolomics data (feature tables, sample metadata) for ingestion into a SECIMTools standalone tool, or when validating that a tool has produced outputs in the correct format and location. Apply this skill when format ambiguity exists (e.g., CSV vs. TSV, row/column orientation, required metadata columns) or when tool invocation has completed and you need to confirm the output artifact meets downstream requirements.

## When NOT to use

- Input data is already confirmed to be in the correct format and has been successfully ingested by the same tool in a prior run without error.
- Your downstream analysis does not depend on strict schema compliance (e.g., exploratory-only workflows that tolerate minor format variation).
- The tool is being run within Galaxy Genomics Framework, which typically handles format wrapping and validation automatically.

## Inputs

- Metabolomics feature table (CSV, TSV, or other delimited format)
- Sample metadata file with required headers and values
- Tool-specific documentation describing input format requirements

## Outputs

- Validated feature table conforming to tool input specification
- Normalized, QC'd, or transformed metabolomics data in tool-specified output format
- Metadata or log file documenting format compliance and transformation steps

## How to apply

Before invoking a SECIMTools tool in standalone mode, consult the tool's documentation to identify required input format (e.g., feature table with specific column structure, sample metadata file with required headers). Prepare or transform your metabolomics data to match that specification—paying attention to delimiters, data types, and mandatory columns. After execution, inspect the output file structure, schema, and location against the tool's documented output specification. Use schema validation or lightweight parsing (e.g., loading into a data frame and checking column/row counts, data types) to confirm compliance. This ensures downstream tools in the workflow can consume the artifact without format errors.

## Related tools

- **SECIMTools suite** (Source of format specifications and target for format-compliant data; provides normalization, quality-control, and feature-filtering tools that accept strictly formatted metabolomics feature tables and sample metadata.) — github.com/secimTools/SECIMTools
- **Galaxy Genomics Framework** (Optional execution environment; when used, abstracts format validation; when running SECIMTools in standalone mode, manual format compliance is required.)

## Evaluation signals

- Input file parses without encoding or delimiter errors and contains all required columns named exactly as documented.
- Output artifact exists at the documented location and has the documented file extension (e.g., '.csv', '.txt').
- Output file row and column counts are consistent with the transformation applied (e.g., feature table after filtering has fewer rows than input; after normalization has same dimensions).
- Data types in output columns match the tool's specification (e.g., numeric values for intensities, string identifiers for sample/feature names).
- Output can be successfully read and instantiated by the next tool in the workflow without format exceptions.

## Limitations

- SECIMTools documentation does not provide a centralized format schema; users must consult individual tool docstrings or code to determine exact input/output specifications.
- No changelog is published, so format changes across versions may not be explicitly documented.
- Standalone mode requires manual format compliance; errors in data preparation or output validation are not caught by Galaxy's wrapper layer.

## Evidence

- [other] Prepare input metabolomics data in the format required by the chosen tool (e.g., feature table, sample metadata).: "Prepare input metabolomics data in the format required by the chosen tool (e.g., feature table, sample metadata)."
- [other] Validate that the output artifact is produced in the expected format and location.: "Validate that the output artifact is produced in the expected format and location."
- [readme] SECIMTools project aims to develop a suite of tools for processing of metabolomics data, which can be run in a standalone mode or via Galaxy Genomics Framework.: "SECIMTools project aims to develop a suite of tools for processing of metabolomics data, which can be run in a standalone mode or via Galaxy Genomics Framework."
- [other] Execute the tool via command-line invocation in standalone mode, passing required arguments and parameters as documented.: "Execute the tool via command-line invocation in standalone mode, passing required arguments and parameters as documented."
