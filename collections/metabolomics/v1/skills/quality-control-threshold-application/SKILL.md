---
name: quality-control-threshold-application
description: Use when you have a feature table with intensity values across study (unknown) and blank control samples, and you need to remove features that may represent instrument artifacts, contamination, or noise rather than true biological signal.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - ThermoRawFileParser
  - Python
  - PCPFM (Python-Centric Pipeline for Metabolomics)
  - Asari
derived_from:
- doi: 10.1371/journal.pcbi.1011912
  title: pcpfm
evidence_spans:
- convert Thermo .raw to mzML (ThermoRawFileParser)
- Python-Centric Pipeline for Metabolomics
- The Python-Centric Pipeline for Metabolomics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pcpfm
    doi: 10.1371/journal.pcbi.1011912
    title: pcpfm
  dedup_kept_from: coll_pcpfm
schema_version: 0.2.0
---

# quality-control-threshold-application

## Summary

Apply intensity ratio thresholds to remove metabolomics features whose signal in study samples does not sufficiently exceed background noise in blank samples, a critical quality control step in LC-MS feature table curation. This skill implements the blank_masking filter to identify and retain only features with reproducible, robust signal relative to blank contamination.

## When to use

Apply this skill when you have a feature table with intensity values across study (unknown) and blank control samples, and you need to remove features that may represent instrument artifacts, contamination, or noise rather than true biological signal. Blank masking is typically applied after initial feature detection (e.g., from Asari) and before normalization or statistical analysis, especially when blank samples were run alongside study samples in the same batch or instrument sequence.

## When NOT to use

- Input data lacks blank control samples or blank/unknown sample classification — the skill requires explicit designation of which samples are blanks.
- Intensity values are missing or all zero for an entire sample class (blank or unknown), which will produce undefined or unreliable ratios.
- Study design uses only positive controls or standards without true procedural blanks, as the skill is designed specifically for blank–unknown comparison.

## Inputs

- Feature table (TSV or CSV format with features as rows, samples as columns, intensity values)
- Sample metadata file (CSV with at minimum sample identifiers and a sample_type or classification field)
- blank_intensity_ratio parameter (numeric threshold, typically 3)

## Outputs

- Filtered feature table (TSV/CSV with same structure as input, subset of features)
- Filtering report or log documenting the number and identity of features removed

## How to apply

Load the feature table and sample metadata, then identify which samples are blanks (designated by a metadata field such as sample_type='blank') and which are unknowns (sample_type='unknown'). For each feature, calculate the median or mean intensity across blank samples and across unknown samples, excluding zero values to avoid inflating ratios from absent features. Compute the intensity ratio (unknown/blank) for each feature and compare it against a configurable blank_intensity_ratio threshold (default value 3). Retain only features where the unknown sample intensity exceeds blank intensity by at least the specified ratio; drop all remaining features. The rationale is that true biological signals should be substantially more abundant in study samples than in procedural blanks, whereas contaminants and noise are typically present at similar levels in both. Save the filtered feature table with a new moniker, preserving all metadata and feature annotations for downstream analysis.

## Related tools

- **PCPFM (Python-Centric Pipeline for Metabolomics)** (Orchestrates the blank_masking filter step as part of the integrated quality-control workflow; accepts feature tables from Asari and applies configurable intensity ratio filtering before normalization and annotation) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics
- **Asari** (Upstream feature detection tool that generates the initial feature table (with intensity values across all samples) that serves as input to the blank_masking filter) — https://github.com/shuzhao-li/asari
- **Python** (Implementation language for the blank_masking command and intensity ratio calculations within PCPFM)

## Evaluation signals

- Feature count decreased after filtering (verify that the filtered table has fewer rows than the input table, corresponding to removed low-signal features)
- Intensity ratio distribution: all retained features have (median unknown intensity) / (median blank intensity) ≥ blank_intensity_ratio threshold; check a sample of retained features against raw intensities
- Metadata and feature annotations preserved: retained features maintain their m/z, retention time, and any pre-annotation columns from the input table
- Sample totals or library size: unknown samples retain substantially higher total intensity than blank samples after filtering (blanks should now contain minimal signal)
- Reproducibility: re-running the filter with identical parameters and threshold on the same input produces identical output (deterministic)

## Limitations

- The choice of blank_intensity_ratio (default 3) is application- and instrument-dependent; too stringent a cutoff may remove genuine low-abundance features; too permissive may retain noise. The article does not provide guidance for threshold tuning beyond the default.
- Mean or median calculations are sensitive to the presence of zero or near-zero values; the workflow excludes zeros but does not address quantification lower limits (LOD/LOQ), which may lead to biased ratio estimates if many features are near detection threshold.
- The skill assumes blanks and unknowns are comparable in terms of instrument response, injection volume, and analysis method; systematic differences in sample preparation or instrument sensitivity between blank and study samples can bias the ratio calculation.
- Features with very low intensity in both blanks and unknowns may be retained or removed unpredictably depending on the exact mean/median values; the skill does not incorporate absolute intensity or signal-to-noise thresholds.

## Evidence

- [other] The blank_masking command removes features by comparing feature intensity in study samples (designated by sample_value) to intensity in blanks (designated by blank_value) using a configurable blank_intensity_ratio parameter; features whose intensity in unknown samples is not at least the specified ratio times more than blank samples are dropped.: "blank_masking command removes features by comparing feature intensity in study samples (designated by sample_value) to intensity in blanks (designated by blank_value) using a configurable"
- [other] For each feature, calculate the median or mean intensity across blank samples and across unknown samples, excluding zero values. Compute the intensity ratio (unknown/blank) for each feature and compare against the blank_intensity_ratio threshold (default 3). Retain only features where unknown sample intensity exceeds blank intensity by at least the threshold ratio.: "For each feature, calculate the median or mean intensity across blank samples and across unknown samples, excluding zero values. Compute the intensity ratio (unknown/blank) for each feature and"
- [intro] perform quality control: "perform quality control"
- [other] Load the input feature table and sample metadata using the specified table moniker and identify blank and unknown samples based on the query field (e.g., 'sample_type').: "Load the input feature table and sample metadata using the specified table moniker and identify blank and unknown samples based on the query field (e.g., 'sample_type')"
- [other] Save the filtered feature table with a new moniker, preserving metadata and feature annotations.: "Save the filtered feature table with a new moniker, preserving metadata and feature annotations"
