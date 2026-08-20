---
name: background-ion-blank-comparison
description: Use when after generating an initial LC-MS feature table (from Asari
  or similar peak detection) and before normalization or statistical analysis, especially
  when blank samples (e.g., solvent-only or buffer-only runs) were acquired alongside
  study samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - Asari
  - PCPFM (Python-Centric Pipeline for Metabolomics)
  - metDataModel
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1371/journal.pcbi.1011912
  title: pcpfm
evidence_spans:
- Python-Centric Pipeline for Metabolomics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pcpfm_cq
    doi: 10.1371/journal.pcbi.1011912
    title: pcpfm
  dedup_kept_from: coll_pcpfm_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1011912
  all_source_dois:
  - 10.1371/journal.pcbi.1011912
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# background-ion-blank-comparison

## Summary

A quality control filter that removes LC-MS metabolomics features likely arising from background contamination or instrument noise by comparing feature intensity between study samples and blank control samples using a user-specified intensity ratio threshold. This step prevents false positive metabolite identifications caused by reagent or solvent contaminants.

## When to use

Apply this skill after generating an initial LC-MS feature table (from Asari or similar peak detection) and before normalization or statistical analysis, especially when blank samples (e.g., solvent-only or buffer-only runs) were acquired alongside study samples. Use it if you suspect background ions or solvent contaminants are inflating feature counts, or if your study design includes explicit blank controls that should be used to establish a signal-to-noise baseline.

## When NOT to use

- Input feature table has not yet been generated (i.e., you are still at raw mzML or .raw file stage); use peak detection (Asari) first.
- Study design does not include blank control samples; blank masking requires explicit blank acquisitions to establish a reference baseline.
- Blank samples are contaminated or unrepresentative of actual background; verify blank quality before applying this filter.

## Inputs

- Feature table (TSV or matrix format with features as rows, samples as columns, intensity values)
- Experiment metadata (JSON or CSV with sample names, sample types, and blank/study designations)
- Blank sample identifiers (via query_field name and blank_value string in metadata)

## Outputs

- Filtered feature table (TSV or matrix format, subset of input features)
- Updated experiment.json with reference to new filtered table moniker
- Summary statistics (optional: counts of features retained vs. dropped, median intensities per group)

## How to apply

Load the feature table and experiment metadata, then parse the metadata to identify samples marked as blanks (via query_field and blank_value) and study samples (sample_value). For each feature, calculate the median intensity (excluding zero values) across blank samples and across study samples separately. Retain only features where the median study-sample intensity is at least N times the median blank-sample intensity, where N is the blank_intensity_ratio parameter (default = 3). This multiplicative threshold is applied feature-by-feature and excludes zero-intensity entries from the ratio calculation to avoid division by zero and focus on genuine signal. Features failing this threshold are dropped from the table. The filtered table is saved under a new moniker and the reference is stored in the experiment.json metadata file for traceability.

## Related tools

- **Asari** (Generates initial LC-MS feature tables from mzML data; output is the input to blank masking) — https://github.com/shuzhao-li/asari
- **PCPFM (Python-Centric Pipeline for Metabolomics)** (Orchestrates the full preprocessing workflow including blank masking as a modular step) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics
- **metDataModel** (Provides standardized data structures and schema for feature tables and metadata used by blank masking) — https://github.com/shuzhao-li-lab/metDataModel

## Evaluation signals

- Feature count decreases from input to output; verify the ratio of retained/dropped features is reasonable (typically 10–70% of features are dropped depending on blank contamination severity).
- All retained features have study-sample intensity ≥ blank_intensity_ratio × blank-sample intensity; manually spot-check a sample of retained and dropped features to confirm threshold was applied correctly.
- Median intensity values for blanks are substantially lower than for study samples across the retained feature set; large overlap in intensity distributions suggests the threshold may be too lenient.
- No features with zero intensity in blanks are incorrectly excluded; verify the filter excludes zeros from the ratio calculation (dividing by zero should not occur).
- Experiment.json is updated with the new table moniker and the filtering parameters (blank_intensity_ratio, query_field, blank_value, sample_value) are logged for reproducibility and traceability.

## Limitations

- The filter assumes blank and study samples are acquired under identical or nearly identical instrument conditions; systematic differences in instrument sensitivity, ionization efficiency, or detector gain between blank and study batches will bias the threshold.
- Default ratio of 3 is a heuristic and may not be optimal for all metabolomics platforms, ionization modes, or matrices; users should validate the threshold against their QC samples or spike-in standards if available.
- The median is sensitive to the number of blank samples; studies with very few blanks (e.g., 1–2) may produce unstable ratio estimates; at least 3 replicate blanks are recommended.
- Features genuinely present at low abundance in study samples but absent (or near-zero) in blanks may be incorrectly retained if the ratio threshold is not carefully chosen; no statistical test (e.g., t-test, fold-change with confidence interval) is applied beyond the deterministic ratio.
- Zero-intensity exclusion from the ratio calculation means that if a feature has zero intensity in all blanks but non-zero in some study samples, the feature is automatically retained without a threshold check; this is intentional but may allow weak signals through if blanks are truly blank.

## Evidence

- [other] features are retained only if their intensity in unknown samples is at least N times higher than in blanks, with a default ratio of 3, and the operation excludes zero-intensity values from the ratio calculation: "features are retained only if their intensity in unknown samples is at least N times higher than in blanks, with a default ratio of 3, and the operation excludes zero-intensity values from the ratio"
- [other] For each feature, calculate the median intensity (excluding zeros) in blank samples and in study samples. 4. Retain only features where study-sample intensity ≥ blank_intensity_ratio × blank-sample intensity.: "For each feature, calculate the median intensity (excluding zeros) in blank samples and in study samples. 4. Retain only features where study-sample intensity ≥ blank_intensity_ratio × blank-sample"
- [other] Blank masking compares feature intensity between study samples and blank samples using a user-specified ratio threshold (blank_intensity_ratio): "Blank masking compares feature intensity between study samples and blank samples using a user-specified ratio threshold (blank_intensity_ratio)"
- [other] How does the blank masking step identify and remove features that are likely due to background contamination rather than true biological signal?: "How does the blank masking step identify and remove features that are likely due to background contamination rather than true biological signal?"
- [intro] Blank masking to remove features likely due to background ions and contaminants: "Blank masking to remove features likely due to background ions and contaminants"
- [readme] feature tables that are optionally blank masked, normalized, batch corrected, annotated or otherwise curated by PCPFM: "feature tables that are optionally blank masked, normalized, batch corrected, annotated or otherwise curated by PCPFM"
