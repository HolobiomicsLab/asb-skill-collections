---
name: feature-list-harmonization-across-methods
description: Use when you have feature lists in CSV format originating from different acquisition methods (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3761
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - IonToolPack
  - Comparador
  - Mirador
  - PeakQuant
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

# feature-list-harmonization-across-methods

## Summary

Harmonizes and compares feature lists (retention time, m/z, metadata) ingested from different mass spectrometry acquisition methods or processing software by resolving naming conflicts, matching common fields, and performing cross-list comparison to identify overlapping and unique features. This skill is essential when integrating results from multiple LC-MS, LC-IMS-MS, or direct infusion workflows that produce heterogeneous CSV feature tables.

## When to use

You have feature lists in CSV format originating from different acquisition methods (e.g., LC-MS vs. LC-IMS-MS), processing software variants, or DDA/DIA modes, and need to determine which features are consistently detected across methods, which are method-specific, and how identifiers and metadata align. This is particularly useful when validating feature detection robustness or comparing workflows during instrument or software upgrades.

## When NOT to use

- Input is already a pre-merged or normalized feature table from a single processing pipeline — harmonization is unnecessary
- Feature lists lack common identifiable fields (m/z, retention time) or metadata is too heterogeneous to reconcile
- You need spectral similarity or MS/MS matching rather than feature-level metadata alignment — use TandemMatch instead

## Inputs

- CSV feature list files from different acquisition methods or processing software, each containing at minimum m/z, retention time, and feature identifier columns

## Outputs

- Harmonized feature table (CSV) with unified identifiers and metadata across all input methods
- Comparison report documenting feature overlap statistics, source method tags, and analysis results
- Cross-list comparison matrix or mapping showing which features are shared vs. method-specific

## How to apply

Load all input feature list CSV files into a tabular format (e.g., pandas DataFrame) and identify common fields across lists (typically m/z, retention time, and feature identifier columns). Apply harmonization by standardizing field names, resolving numeric precision differences (e.g., m/z tolerance in ppm), and reconciling conflicting metadata values using defined matching logic. Perform cross-list comparison to flag overlapping features (matched on m/z and retention time within tolerance thresholds) and tag unique features by source method. Generate a structured comparison report (CSV or tabular format) that documents overlap statistics, harmonized feature IDs, source method tags, and any unresolved conflicts. Validate that the number and identity of harmonized features is consistent with expectations and that no features are silently dropped during the matching process.

## Related tools

- **Comparador** (Performs harmonization and cross-list comparison of CSV feature lists from different acquisition methods or processing software) — https://github.com/pnnl/IonToolPack
- **Mirador** (Generates raw MS data visualizations and exports feature data (including XIC, XIM heatmaps) in CSV format for input to harmonization) — https://github.com/pnnl/IonToolPack
- **PeakQuant** (Extracts targeted MS1 peak abundances that can be harmonized across methods for quantitative comparison) — https://github.com/pnnl/IonToolPack

## Evaluation signals

- Harmonized feature table contains all expected features from each input list, with no silent drops or duplicates
- Cross-list overlap statistics match manual spot-checks on a subset of features (e.g., count and identity of shared features between method pairs)
- Harmonized feature identifiers are consistent and unambiguous across all rows; no null or conflicting values in key fields
- All input CSV files are successfully parsed and loaded without encoding or column-name mismatches
- Comparison report documents the number and percentage of features shared, unique-to-method, and unresolved conflicts; ratios are reasonable given the acquisition method differences

## Limitations

- Harmonization quality depends on consistent or reconcilable field naming and numeric precision across input lists; highly divergent metadata schemas may lead to unresolved conflicts
- No automated spectral similarity or cosine-score matching is performed; feature overlap is determined solely on m/z and retention time proximity, which may conflate isobaric or co-eluting compounds
- Feature lists from very different acquisition methods (e.g., direct infusion vs. LC-MS) may have incompatible retention time or mobility fields, requiring manual preprocessing
- No changelog or versioning information is documented, so reproducibility across releases may be affected

## Evidence

- [other] Comparador ingests feature lists in CSV format from different acquisition methods or processing software, applies harmonization procedures, and performs comparative analysis on the results.: "Comparador ingests feature lists in CSV format from different acquisition methods or processing software, applies harmonization procedures, and performs comparative analysis on the results."
- [other] Harmonize feature identifiers, retention time, m/z, and other metadata across lists by matching on common fields and resolving naming conflicts.: "Harmonize feature identifiers, retention time, m/z, and other metadata across lists by matching on common fields and resolving naming conflicts."
- [other] Identify overlapping and unique features across all input lists using cross-list comparison logic.: "Identify overlapping and unique features across all input lists using cross-list comparison logic."
- [readme] Tool to compare lists of features (CSV files) from different acquisition methods or processing software, by harmonizing and analyzing results.: "Tool to compare lists of features (CSV files) from different acquisition methods or processing software, by harmonizing and analyzing results."
- [readme] It reads data from multiple instrument formats, requires no installation and provides omics agnostic functionalities (metabolomics, lipidomics, proteomics, etc.): "It reads data from multiple instrument formats, requires no installation and provides omics agnostic functionalities (metabolomics, lipidomics, proteomics, etc.)"
