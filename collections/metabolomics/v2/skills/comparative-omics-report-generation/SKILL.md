---
name: comparative-omics-report-generation
description: Use when when you have feature lists (in CSV format) from two or more different MS acquisition methods (e.g., LC-MS vs. LC-IMS-MS), different processing software (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - IonToolPack
  - Comparador
  - pandas
  techniques:
  - LC-MS
  - ion-mobility-MS
  - tandem-MS
derived_from:
- doi: 10.1021/jasms.4c00146
  title: PeakQC
evidence_spans:
- IonToolPack is a software suite housing tools for mass spectrometry data
- IonToolPack is a software suite housing tools for mass spectrometry data.
- 'Comparador: Tool to compare lists of features (CSV files) from different acquisition methods or processing software'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_peakqc_cq
    doi: 10.1021/jasms.4c00146
    title: PeakQC
  dedup_kept_from: coll_peakqc_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00146
  all_source_dois:
  - 10.1021/jasms.4c00146
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# comparative-omics-report-generation

## Summary

Generate structured comparison reports that harmonize and cross-tabulate feature lists from multiple mass spectrometry acquisition methods or processing software, documenting overlap statistics and source-specific identifiers. This skill enables multi-method validation and systematic comparison of omics results across different analytical pipelines.

## When to use

When you have feature lists (in CSV format) from two or more different MS acquisition methods (e.g., LC-MS vs. LC-IMS-MS), different processing software (e.g., vendor-specific peak detection vs. open-source alternatives), or different fragmentation strategies (DDA vs. DIA), and need to identify which features are reproducibly detected across methods, which are method-specific, and how identifiers and metadata map across pipelines.

## When NOT to use

- Input is already a unified feature table or has been pre-harmonized across methods; use this skill only when raw, separate feature lists require integration.
- Feature lists lack sufficient metadata (m/z, RT) to enable reliable matching across methods; harmonization requires at least one common numerical field.
- Analysis goal is method-specific optimization (e.g., tuning a single processing pipeline); this skill is for cross-method comparison, not within-method refinement.

## Inputs

- CSV files containing feature lists (rows=features, columns including feature ID, m/z, retention time, abundance or intensity, and metadata)
- Multiple feature list files from different acquisition methods or processing software
- Metadata file (optional) describing source method, instrument type, or processing parameters for each input

## Outputs

- Harmonized feature comparison report (CSV or tabular format)
- Feature overlap statistics (e.g., count and percentage of features shared across all methods, pairwise overlaps)
- Structured table with harmonized feature IDs, source method tags, and cross-method metadata mapping
- Analysis results documenting unique vs. shared features per method

## How to apply

Load multiple feature list CSV files using pandas, each containing columns such as feature identifiers, retention time (RT), m/z values, and acquisition method metadata. Apply harmonization procedures by matching features across lists on common fields (m/z and RT) within specified tolerances, resolving naming conflicts by tagging each feature with its source method. Identify overlapping features using cross-list comparison logic (e.g., m/z tolerance and RT window matching) and flag unique features present in only one method. Generate a structured output report (CSV or tabular format) that includes a harmonized feature ID space, overlap counts, source method tags, and per-method abundance or detection metrics. Validate the report by spot-checking a sample of matched features and verifying that overlap statistics sum correctly across all input lists.

## Related tools

- **Comparador** (Primary tool to ingest feature lists in CSV format from different acquisition methods or processing software, apply harmonization procedures, and perform comparative analysis on the results.) — https://github.com/pnnl/IonToolPack
- **IonToolPack** (Host software suite providing the Comparador tool; reads data from multiple instrument formats and provides omics-agnostic GUI for feature comparison workflows.) — https://github.com/pnnl/IonToolPack
- **pandas** (Python library used to load and manipulate multiple feature list CSV files.)

## Evaluation signals

- Output CSV report contains all expected columns: harmonized feature ID, source method tags, m/z, RT, and overlap count (number of methods detecting each feature).
- Overlap statistics are self-consistent: sum of features unique to each method plus features shared by all methods equals total unique features across all inputs.
- Spot-check: manually verify 5–10 matched features by confirming m/z and RT differences fall within specified tolerance thresholds across input methods.
- All input CSV files are represented in the source method tags with non-zero feature counts; no input file is silently dropped.
- Harmonized feature IDs are globally unique and traceable back to original feature identifiers in each input file via an audit trail or mapping column.

## Limitations

- Harmonization accuracy depends on the choice of m/z and RT tolerances; overly loose tolerances may merge features that are actually distinct, while overly strict tolerances may fragment true duplicates across methods.
- Feature lists must contain at least m/z and retention time (or equivalent temporal metadata) to enable reliable matching; lists lacking these fields cannot be harmonized.
- The skill does not perform statistical testing on overlap significance; high overlap may reflect genuine agreement or convergent artifacts depending on the methods' input data and parameters.
- No changelog or versioning information available for Comparador; reproducibility and version tracking should be documented manually.

## Evidence

- [other] Comparador ingests feature lists in CSV format from different acquisition methods or processing software, applies harmonization procedures, and performs comparative analysis on the results.: "Comparador ingests feature lists in CSV format from different acquisition methods or processing software, applies harmonization procedures, and performs comparative analysis on the results."
- [other] Load multiple feature list CSV files from different acquisition methods or processing software using pandas.: "Load multiple feature list CSV files from different acquisition methods or processing software using pandas."
- [other] Harmonize feature identifiers, retention time, m/z, and other metadata across lists by matching on common fields and resolving naming conflicts.: "Harmonize feature identifiers, retention time, m/z, and other metadata across lists by matching on common fields and resolving naming conflicts."
- [other] Identify overlapping and unique features across all input lists using cross-list comparison logic.: "Identify overlapping and unique features across all input lists using cross-list comparison logic."
- [other] Generate a structured comparison report (CSV or tabular format) documenting feature overlap statistics, harmonized feature IDs, source method tags, and analysis results.: "Generate a structured comparison report (CSV or tabular format) documenting feature overlap statistics, harmonized feature IDs, source method tags, and analysis results."
- [readme] Tool to compare lists of features (CSV files) from different acquisition methods or processing software, by harmonizing and analyzing results.: "Tool to compare lists of features (CSV files) from different acquisition methods or processing software, by harmonizing and analyzing results."
