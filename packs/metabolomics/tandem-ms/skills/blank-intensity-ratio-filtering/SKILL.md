---
name: blank-intensity-ratio-filtering
description: Use when apply this filter after feature detection and before downstream statistical analysis when your experimental design includes blank samples (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - ThermoRawFileParser
  - Python
  - PCPFM
  - Asari
  techniques:
  - LC-MS
  - tandem-MS
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

# blank-intensity-ratio-filtering

## Summary

A quality control filter that removes low-abundance features from LC-MS metabolomics feature tables by comparing feature intensity in study samples to intensity in blank samples using a configurable ratio threshold. This step eliminates likely contaminants or instrument artifacts that appear at similar levels in blanks and unknowns.

## When to use

Apply this filter after feature detection and before downstream statistical analysis when your experimental design includes blank samples (e.g., solvent blanks, extraction blanks) and you want to retain only features with signal substantially higher in your study samples than in method blanks. This is particularly important for untargeted LC-MS/MS datasets where blank contamination can inflate the feature count and introduce noise.

## When NOT to use

- Your experimental design does not include blank samples or you lack sample type metadata to distinguish blanks from unknowns.
- You are working with targeted metabolomics data where all features are pre-validated authentic standards; blank filtering is redundant.
- Your blanks contain intentionally spiked internal standards or QC compounds that should not be removed.

## Inputs

- Feature table in TSV format with features as rows and samples as columns
- Sample metadata CSV with at least sample name, file path, and sample type (blank vs. unknown)
- Table moniker (name/ID for the feature table being filtered)

## Outputs

- Filtered feature table in TSV format with blank-masked features removed
- Metadata and feature annotations preserved from input table

## How to apply

Load the input feature table and sample metadata, then use the sample_type or similar query field to designate which samples are blanks (blank_value) and which are unknowns (sample_value). For each feature, calculate the median or mean intensity across blank samples and across unknown samples, excluding zero values. Compute the intensity ratio (unknown/blank) for each feature and compare against the blank_intensity_ratio threshold (default 3). Retain only features where the median/mean intensity in unknown samples exceeds that in blanks by at least the specified ratio; features that fail this test are dropped from the table. Save the filtered feature table with a new moniker in the feature_tables directory.

## Related tools

- **PCPFM** (Command-line pipeline interface that implements blank_masking as a filter step during feature table curation) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics
- **Asari** (Upstream feature detection and quality control tool that produces the feature table input to blank masking) — https://github.com/shuzhao-li/asari
- **Python** (Language used to implement the intensity ratio calculation and feature filtering logic)

## Evaluation signals

- Number of features retained should be substantially lower than input (typically 20–50% reduction depending on blank contamination severity).
- Verify that all retained features have (median unknown intensity / median blank intensity) ≥ blank_intensity_ratio threshold; spot-check a sample of filtered features.
- Check that the output feature table has the same number of samples and sample names as the input, with only features (rows) removed.
- Confirm that feature metadata and annotation columns (e.g., m/z, retention time, empirical compound ID) are preserved in the output.
- Compare the size and content of the output table to metadata in the experiment.json or QAQC logs to ensure filtering was applied as configured.

## Limitations

- The default threshold of 3× is empirically tuned for typical LC-MS/MS runs but may need adjustment if blank contamination is unusually high or if matrix effects make study samples appear lower than expected. No formal statistical test is applied; the ratio is deterministic.
- The filter assumes that blank samples are truly representative of contamination in your extraction/instrument workflow; misclassified blanks or blanks from a different batch/method than unknowns will produce incorrect results.
- Features with zero intensity in all blanks (clean features) will pass the filter regardless of unknown intensity, so extremely low-abundance features in unknowns may be retained if blanks are zero. Median/mean calculation excludes zeros, which can inflate ratios when blank replicates are sparse.
- The pipeline is currently optimized for LC-MS/MS data; support for GC and other data types is under development and blank masking has not been validated on those modalities.

## Evidence

- [other] The blank_masking command removes features by comparing feature intensity in study samples (designated by sample_value) to intensity in blanks (designated by blank_value) using a configurable blank_intensity_ratio parameter; features whose intensity in unknown samples is not at least the specified ratio times more than blank samples are dropped.: "blank_masking command removes features by comparing feature intensity in study samples (designated by sample_value) to intensity in blanks (designated by blank_value) using a configurable"
- [other] For each feature, calculate the median or mean intensity across blank samples and across unknown samples, excluding zero values. Compute the intensity ratio (unknown/blank) for each feature and compare against the blank_intensity_ratio threshold (default 3). Retain only features where unknown sample intensity exceeds blank intensity by at least the threshold ratio.: "For each feature, calculate the median or mean intensity across blank samples and across unknown samples, excluding zero values. Compute the intensity ratio (unknown/blank) for each feature and"
- [other] Load the input feature table and sample metadata using the specified table moniker and identify blank and unknown samples based on the query field (e.g., 'sample_type').: "Load the input feature table and sample metadata using the specified table moniker and identify blank and unknown samples based on the query field"
- [readme] This includes feature tables that are optionally blank masked, normalized, batch corrected, annotated or otherwise curated by PCPFM and empirical compounds as a JSON file representing putative metabolites that can be annotated with MS1, MS2, or authentic standards.: "feature tables that are optionally blank masked, normalized, batch corrected, annotated or otherwise curated by PCPFM"
- [readme] We are working to add supports of GC and other data types.: "We are working to add supports of GC and other data types."
