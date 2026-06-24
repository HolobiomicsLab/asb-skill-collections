---
name: cross-software-feature-matching
description: Use when you have collected feature lists in CSV format from two or more
  MS acquisition methods (e.g., LC-MS vs. LC-IMS-MS), processing software packages
  (e.g., vendor-specific vs. open-source), or instrument platforms (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3258
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - IonToolPack
  - Comparador
  - Mirador
  - PeakQuant
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: open
derived_from:
- doi: 10.1021/jasms.4c00146
  title: PeakQC
evidence_spans:
- IonToolPack is a software suite housing tools for mass spectrometry data
- IonToolPack is a software suite housing tools for mass spectrometry data.
- 'Comparador: Tool to compare lists of features (CSV files) from different acquisition
  methods or processing software'
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cross-software-feature-matching

## Summary

Harmonize and compare feature lists (m/z, retention time, identifiers) exported as CSV from different mass spectrometry acquisition methods or processing software to identify overlapping and unique features across workflows. This skill is essential when evaluating consistency, reproducibility, or complementarity of features detected by different instruments or data processing pipelines.

## When to use

You have collected feature lists in CSV format from two or more MS acquisition methods (e.g., LC-MS vs. LC-IMS-MS), processing software packages (e.g., vendor-specific vs. open-source), or instrument platforms (e.g., Agilent vs. Thermo), and you need to reconcile naming conventions, match features on common fields (m/z, retention time, feature ID), and quantify overlap statistics to assess method agreement or identify method-specific detections.

## When NOT to use

- Input is already a unified or pre-harmonized feature table; use this skill only when starting from separate, independently generated CSV lists.
- Feature lists lack sufficient metadata (m/z and/or RT columns); the skill depends on these common fields for harmonization.
- You seek only visual comparison; if the goal is exploratory visualization of single-method features, use Mirador instead.

## Inputs

- CSV feature lists from different MS acquisition methods or processing software, each containing at minimum m/z, retention time (RT), and feature identifier columns
- User-specified tolerances for m/z and retention time matching (e.g., ±5 ppm, ±0.2 min)

## Outputs

- Harmonized feature table (CSV or tabular format) with unified feature IDs, m/z, RT, and source method tags
- Comparison report summarizing feature overlap statistics (total features per method, shared features, unique features, overlap percentages)
- Cross-method feature correspondence matrix or mapping document linking original feature IDs to harmonized IDs

## How to apply

Load multiple CSV feature lists using pandas or similar tabular I/O. Harmonize feature identifiers and metadata by aligning on common fields (e.g., m/z and retention time within user-specified tolerance windows) and resolving naming conflicts (e.g., different retention time formats or m/z decimal precision). Cross-reference all input lists pairwise or all-against-all to identify overlapping features (matches within tolerance) and unique features (no match across lists). Generate a structured comparison report documenting feature overlap statistics (count and percentage of shared vs. unique features per method), harmonized feature IDs, source method tags, and confidence metrics. The rationale is that features matching within m/z and RT tolerances across methods represent robust, reproducible signals, while method-specific features may indicate instrumental sensitivity differences, software parameter choices, or true biological variation.

## Related tools

- **Comparador** (Primary tool for harmonizing and comparing CSV feature lists across acquisition methods or processing software; ingests feature lists, applies matching logic on m/z and RT, resolves naming conflicts, and produces structured comparison reports.) — https://github.com/pnnl/IonToolPack
- **IonToolPack** (Parent software suite housing Comparador and providing omics-agnostic GUI for MS data processing across multiple instrument formats (Agilent, Thermo, Bruker, mzML).) — https://github.com/pnnl/IonToolPack
- **Mirador** (Complementary visualization and export tool for raw MS data (XIC, XIM heatmaps, MS/MS mirror plots) to CSV; can be used upstream to generate feature lists for subsequent cross-software comparison.) — https://github.com/pnnl/IonToolPack
- **PeakQuant** (Optional preprocessing tool for targeted MS1 peak abundance extraction; output peak tables can be formatted as CSV inputs to cross-software feature matching.) — https://github.com/pnnl/IonToolPack

## Evaluation signals

- Verify that all input CSV files are successfully loaded and contain non-null m/z and retention time columns with consistent numeric formats.
- Check that harmonized feature IDs are unique and traceable back to original feature IDs in source lists via the correspondence mapping.
- Confirm that overlap statistics sum correctly: (unique features per method + shared features) equals total features across all harmonized features for that method.
- Validate that matched features fall within the specified m/z and RT tolerance windows; spot-check a sample of matches manually or against known standards.
- Ensure the final comparison report includes source method tags for every feature, permitting reconstruction of feature provenance and filtering by method subset.

## Limitations

- Matching depends critically on accurate m/z and RT reporting; systematic calibration drift or retention time shift between methods can lead to false negatives (missed matches) if tolerances are too tight.
- The skill assumes features are comparable across methods; instrumental differences (e.g., different ionization modes, resolving power) may produce method-specific features that are genuine, not artifacts.
- No built-in handling of adducts, isotopes, or in-source fragments; if input lists report multiple charge states or adduct forms of the same compound, pre-processing or post-hoc deconvolution may be required.
- CSV format requires manual annotation of column headers and data types; malformed or ambiguous CSV input (e.g., missing headers, mixed delimiters) can cause parsing failures.

## Evidence

- [other] Comparador ingests feature lists in CSV format from different acquisition methods or processing software, applies harmonization procedures, and performs comparative analysis on the results.: "Comparador ingests feature lists in CSV format from different acquisition methods or processing software, applies harmonization procedures, and performs comparative analysis on the results."
- [other] Harmonize feature identifiers, retention time, m/z, and other metadata across lists by matching on common fields and resolving naming conflicts.: "Harmonize feature identifiers, retention time, m/z, and other metadata across lists by matching on common fields and resolving naming conflicts."
- [other] Identify overlapping and unique features across all input lists using cross-list comparison logic.: "Identify overlapping and unique features across all input lists using cross-list comparison logic."
- [other] Generate a structured comparison report (CSV or tabular format) documenting feature overlap statistics, harmonized feature IDs, source method tags, and analysis results.: "Generate a structured comparison report (CSV or tabular format) documenting feature overlap statistics, harmonized feature IDs, source method tags, and analysis results."
- [readme] Comparador: Tool to compare lists of features (CSV files) from different acquisition methods or processing software, by harmonizing and analyzing results.: "Comparador: Tool to compare lists of features (CSV files) from different acquisition methods or processing software, by harmonizing and analyzing results."
- [readme] It reads data from multiple instrument formats, requires no installation and provides omics agnostic functionalities (metabolomics, lipidomics, proteomics, etc.): "It reads data from multiple instrument formats, requires no installation and provides omics agnostic functionalities (metabolomics, lipidomics, proteomics, etc.)"
