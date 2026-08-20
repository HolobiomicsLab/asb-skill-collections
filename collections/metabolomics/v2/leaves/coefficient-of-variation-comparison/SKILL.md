---
name: coefficient-of-variation-comparison
description: Use when after normalization of a metabolomic feature matrix but before
  statistical testing, when you have both QC (technical replicate) and non-QC (study)
  samples and need to remove features with unstable or poorly reproducible signal
  patterns.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - margheRita
  - notame
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1101/2024.06.20.599545v1
  title: MargheRita
- doi: 10.1101/2024.06.20.599545
  title: ''
evidence_spans:
- The R package margheRita addresses the complete workflow
- The R package margheRita
- The R package margheRita addresses the complete workflow for metabolomic profiling
  in untargeted studies based on liquid chromatography (LC) coupled with tandem mass
  spectrometry (MS/MS)
- The R package margheRita addresses the complete workflow for metabolomic profiling
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_margherita_cq
    doi: 10.1101/2024.06.20.599545v1
    title: MargheRita
  dedup_kept_from: coll_margherita_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.06.20.599545v1
  all_source_dois:
  - 10.1101/2024.06.20.599545v1
  - 10.1101/2024.06.20.599545
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# coefficient-of-variation-comparison

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Filter metabolomic features by comparing coefficient of variation (CV) between sample and quality control (QC) groups, retaining only features where the CV ratio (non-QC/QC) exceeds a threshold. This approach removes low-variance features that fail to differentiate between study samples and analytical controls, improving data quality for downstream statistical testing.

## When to use

After normalization of a metabolomic feature matrix but before statistical testing, when you have both QC (technical replicate) and non-QC (study) samples and need to remove features with unstable or poorly reproducible signal patterns. Use when QC samples are present in the dataset and you want to prioritize features with higher relative variability in the biological samples compared to technical replicates.

## When NOT to use

- When QC samples are absent or not adequately represented in the dataset — CV comparison requires both groups.
- When features are expected to have low variability in biological samples (e.g., tightly regulated housekeeping metabolites) — filtering may remove real, stable signals.
- When all samples are technical replicates or when no biological replication exists — CV comparison loses interpretability.

## Inputs

- Normalized feature abundance matrix (e.g., Urine_RP_NEG_norm.txt format)
- Sample metadata identifying QC vs. non-QC sample group membership

## Outputs

- Filtered feature abundance matrix containing only CV-ratio-passing features
- Summary statistics table: feature count before/after filtering, CV ratio distribution metrics (mean, median, quantiles)
- CV ratio distribution visualization (histogram or density plot)

## How to apply

First, stratify the normalized feature matrix by sample type (QC vs. non-QC) based on metadata. Calculate the coefficient of variation (standard deviation / mean × 100) separately for each feature within the QC sample group and within the non-QC sample group. Compute the CV ratio for each feature as (CV_non-QC / CV_QC). Apply a threshold filter (default: CV_ratio > 1.0) to retain only features where the ratio exceeds this cutoff. This ensures retained features show greater variability in the biological samples than in technical replicates, which is expected for true metabolomic signals. Generate summary statistics including the count of features before and after filtering, the distribution and median of retained CV ratios, and optional visualizations of the CV ratio distribution.

## Related tools

- **margheRita** (R package implementing CV_ratio() filtering function for metabolomic feature quality control) — https://github.com/emosca-cnr/margheRita
- **R** (Statistical computing environment used to calculate CV, CV ratio, and apply threshold filtering)
- **notame** (Alternative R package for non-targeted LC-MS metabolomics preprocessing; supports similar filtering workflows) — https://github.com/hanhineva-lab/notame

## Examples

```
# Load normalized feature matrix and sample metadata; calculate CV per feature within QC and non-QC groups; compute CV_ratio and filter
CV_ratio_filtered <- CV_ratio(norm_matrix, metadata, cv_threshold = 1.0)
```

## Evaluation signals

- Feature count decreases from initial total to filtered total (e.g., 539 → 303 in the example); verify no records are lost due to calculation errors.
- CV ratio distribution of retained features is centered ≥ 1.0 with median > threshold; features with CV_ratio ≤ threshold are completely absent.
- Retained features exhibit higher variability in non-QC samples relative to QC samples by definition; spot-check a sample of retained vs. removed features to confirm expected pattern.
- Summary statistics table is complete with no missing values for retained features; filtering is reproducible when re-applied to the same input.
- No features remain in the output with CV_ratio < threshold; filtering logic is correctly enforced.

## Limitations

- The default threshold (CV_ratio > 1.0) is arbitrary; the appropriate threshold may depend on the metabolite class, instrument stability, and study design. Thresholds tuned to a specific dataset may not generalize.
- CV calculation is sensitive to small mean values or zeroes, which may inflate ratios for low-abundance features; consider robust CV alternatives (e.g., using non-zero values only, median absolute deviation) if sparsity is high.
- This filter does not account for biological significance or pathway relevance; features passing CV filtering may still be uninformative or confounded by batch effects.
- If QC replicates are few (< 3–5), CV estimates for the QC group may be unstable, leading to unreliable CV ratios.

## Evidence

- [intro] filtering by coefficient of variation (samples vs QCs): "filtering by mass defects, filtering by coefficient of variation (samples vs QCs) and probabilistic quotient normalization"
- [other] CV_ratio() function retains features with CV ratio exceeding default threshold of 1: "The CV_ratio() function retains only features with a CV ratio (non-QC samples / QC samples) exceeding the default threshold of 1"
- [other] Feature retention results: 303 metabolites retained from 539 initial features: "producing a distribution with median 1.1032 and resulting in 303 metabolites retained out of 539 initial features"
- [other] Workflow: calculate CV separately for QC and non-QC groups, compute ratio, apply threshold: "Calculate the coefficient of variation (CV) for each feature separately within the non-QC sample group and within the QC sample group. 3. Compute the CV ratio (CV_non-QC / CV_QC) for each feature. 4."
- [readme] margheRita provides pre-processing functions with focus on metabolomic-specific methods: "a series of pre-processing functions (quality control, filtering and normalization) with a particular focus on methods specifically recommended for metabolomic profiles"
