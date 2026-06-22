---
name: sample-type-stratified-feature-masking
description: Use when after feature detection but before statistical analysis, when your study includes blank samples (e.g., solvent or extraction blanks) and you want to remove features that fail to show meaningful enrichment in actual study samples relative to blank contamination.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3375
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
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pcpfm
    doi: 10.1371/journal.pcbi.1011912
    title: pcpfm
  dedup_kept_from: coll_pcpfm
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1011912
  all_source_dois:
  - 10.1371/journal.pcbi.1011912
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# sample-type-stratified-feature-masking

## Summary

Remove features from a metabolomics feature table whose intensity in study (unknown) samples is not sufficiently elevated above blank samples, using a configurable intensity ratio threshold. This quality-control step eliminates likely contaminants and noise that appear equally in blanks and unknowns.

## When to use

Apply this skill after feature detection but before statistical analysis, when your study includes blank samples (e.g., solvent or extraction blanks) and you want to remove features that fail to show meaningful enrichment in actual study samples relative to blank contamination. Typical trigger: presence of a 'sample_type' or analogous metadata field that designates some samples as blanks and others as unknowns or QC.

## When NOT to use

- Input study lacks blank samples or blank/unknown sample stratification is unavailable.
- Feature table is already post-QC and blanks have been removed; blank-masking requires the blank samples to be present in the input table.
- Blanks are QC or standard mixtures rather than true process blanks—intensity may legitimately exceed study samples.

## Inputs

- feature table (intensity matrix with features as rows, samples as columns)
- sample metadata / sequence file with sample_type or equivalent classification field

## Outputs

- filtered feature table (subset of input, retaining only features with unknown/blank intensity ratio ≥ threshold)
- optionally: masking report or QC visualization showing features retained vs. removed

## How to apply

Load the feature table and sample metadata, stratify samples into blank and unknown groups using a metadata query field (e.g., sample_type='blank' vs. sample_type='unknown'). For each feature, calculate median or mean intensity across blanks and across unknowns, excluding zero values to avoid inflation from missing features. Compute the intensity ratio (unknown / blank) for each feature and retain only features where this ratio meets or exceeds the blank_intensity_ratio threshold (default 3, meaning unknown intensity must be ≥ 3× blank intensity). Save the filtered table with a new moniker, preserving all metadata and feature annotations for downstream analysis.

## Related tools

- **PCPFM (Python-Centric Pipeline for Metabolomics)** (orchestrates blank_masking as a configurable QC step within the end-to-end LC-MS preprocessing workflow) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics
- **Python** (implementation language for blank_masking command and intensity ratio calculations)
- **Asari** (produces the initial feature table (via mzML processing) that serves as input to blank masking) — https://github.com/shuzhao-li/asari

## Evaluation signals

- Feature count decreases; verify that removed features have unknown/blank intensity ratios below the specified threshold (e.g., < 3).
- Retained features show elevated median intensity in unknown samples relative to blanks (ratio typically > 3); spot-check a sample of removed features to confirm they were contamination-like or noise.
- Sample metadata and feature annotations (m/z, retention time, etc.) are preserved in output table; verify schema and row/column structure match input.
- Output table row count equals input minus removed features; output column count (samples) is unchanged.
- Optionally compare PCA, t-SNE, or other exploratory plots before and after masking—blank samples should cluster separately from unknowns pre-masking; post-masking, unknowns should show clearer separation or reduced noise.

## Limitations

- Effectiveness depends on quality and representativeness of blank samples; if blanks do not reflect true process contamination, intensity ratio may be misleading.
- Default threshold (ratio = 3) is data-dependent and may not suit all metabolite classes or instrumental platforms; users should validate via domain knowledge or pilot experiments.
- Method assumes intensity scales linearly with contamination; non-linear instrumental responses or matrix effects could bias the ratio.
- Exclusion of zero values before computing mean/median avoids division-by-zero but may artificially inflate ratios if blanks contain many missing values and unknowns contain sparse detections.
- README notes that support for GC and other data types is under development; currently documented for LC-MS only.

## Evidence

- [other] The blank_masking command removes features by comparing feature intensity in study samples (designated by sample_value) to intensity in blanks (designated by blank_value) using a configurable blank_intensity_ratio parameter; features whose intensity in unknown samples is not at least the specified ratio times more than blank samples are dropped.: "blank_masking command removes features by comparing feature intensity in study samples (designated by sample_value) to intensity in blanks (designated by blank_value) using a configurable"
- [other] For each feature, calculate the median or mean intensity across blank samples and across unknown samples, excluding zero values. Compute the intensity ratio (unknown/blank) for each feature and compare against the blank_intensity_ratio threshold (default 3). Retain only features where unknown sample intensity exceeds blank intensity by at least the threshold ratio.: "For each feature, calculate the median or mean intensity across blank samples and across unknown samples, excluding zero values. Compute the intensity ratio (unknown/blank) for each feature and"
- [other] Load the input feature table and sample metadata using the specified table moniker and identify blank and unknown samples based on the query field (e.g., 'sample_type').: "Load the input feature table and sample metadata using the specified table moniker and identify blank and unknown samples based on the query field (e.g., 'sample_type')"
- [other] Save the filtered feature table with a new moniker, preserving metadata and feature annotations.: "Save the filtered feature table with a new moniker, preserving metadata and feature annotations"
- [readme] The Python-Centric Pipeline for Metabolomics is designed to take raw LC-MS metabolomics data and ready them for downstream statistical analysis. The pipeline can perform quality control, data normalization and batch correction.: "perform quality control, data normalization and batch correction"
