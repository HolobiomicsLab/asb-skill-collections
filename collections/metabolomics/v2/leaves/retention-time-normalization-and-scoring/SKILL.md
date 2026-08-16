---
name: retention-time-normalization-and-scoring
description: Use when you have XCMS-aligned feature tables with retention time values
  and need to compute pairwise feature similarity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - R
  - XCMS
  - dynamicTreeCut
  - RAMClustR
  techniques:
  - mass-spectrometry
  license_tier: restricted
derived_from:
- doi: 10.1021/ac501530d
  title: RAMClust
evidence_spans:
- ramclustR function is built to use xcms data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ramclust_cq
    doi: 10.1021/ac501530d
    title: RAMClust
  dedup_kept_from: coll_ramclust_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/ac501530d
  all_source_dois:
  - 10.1021/ac501530d
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# retention-time-normalization-and-scoring

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Convert raw retention time differences between mass spectrometry features into normalized similarity scores (0–1 scale) suitable for hierarchical clustering. This preprocessing step enables fair combination of retention time proximity with correlational similarity to group features derived from the same compound.

## When to use

Apply this skill when you have XCMS-aligned feature tables with retention time values and need to compute pairwise feature similarity. Specifically, use it before multiplying retention time similarity with correlational similarity scores to identify compound clusters, or when retention time drift correction (retcor) has been applied and you need to standardize RT differences into a common metric for downstream clustering.

## When NOT to use

- Retention time correction (retcor) has not yet been applied to the XCMS object; apply retcor and regroup before computing RT similarity scores.
- Features are from different analytical platforms or chromatography methods with incompatible RT scales; normalize across platforms first.
- Input is already a pre-computed distance or similarity matrix; use it directly without re-normalizing RT values.

## Inputs

- XCMS feature table with retention time (RT) values per feature
- Feature pair list or all pairwise feature combinations
- XCMS-corrected retention time values (after retcor and regroup steps)

## Outputs

- Normalized retention time similarity matrix (0–1 scale, symmetric)
- Pairwise RT similarity scores per feature pair
- Total similarity matrix (product of RT similarity and correlational similarity)

## How to apply

Extract retention time values for all feature pairs from the XCMS-processed feature table. Normalize the absolute retention time differences into a similarity score on a 0–1 scale using a distance-based transformation (e.g., inverse distance weighting or Gaussian kernel). This normalization ensures that features with identical or very close retention times receive scores close to 1, while features far apart in RT receive scores close to 0. The normalized RT similarity score is then multiplied element-wise by the Pearson correlation coefficient (computed across sample profiles) to produce the total similarity matrix. Features from the same compound are expected to have approximately the same retention time, so high RT similarity combined with high correlational similarity (product near 1) indicates grouping; low values in either dimension (product near 0) indicate distinct compounds.

## Related tools

- **XCMS** (Detects and aligns features across samples; provides retention time values and performs RT drift correction (retcor) prior to RT similarity computation.)
- **dynamicTreeCut** (Performs hierarchical clustering on the total similarity matrix (product of RT and correlational similarity) to cut dendrograms into feature clusters.)
- **RAMClustR** (Main clustering function that combines RT normalization, correlational similarity, and hierarchical clustering to group features from the same compound.) — https://github.com/cbroeckl/RAMClustR
- **R** (Statistical computing environment for implementing RT normalization, matrix operations, and correlation calculations.)

## Examples

```
# Extract retention times and normalize; multiply with correlation scores in R
# rt_sim <- exp(-(abs(rt[i] - rt[j]) / rt_tolerance)^2)  # Gaussian normalization
# total_sim <- rt_sim * cor_coef  # element-wise product for clustering input
```

## Evaluation signals

- Normalized RT similarity scores lie between 0 and 1 for all feature pairs; inspect histogram or summary statistics of the RT similarity matrix.
- Features with identical or near-identical retention times (e.g., within instrument precision ~0.1 min) receive RT similarity scores ≥ 0.8 or higher.
- Features with large RT separation (e.g., > 2 min) receive RT similarity scores < 0.2 or lower.
- The resulting total similarity matrix (element-wise product of RT and correlational similarity) produces well-separated clusters via hierarchical clustering; visualize dendrogram structure and cluster purity.
- Compounds known to co-elute or have identical retention times appear in the same cluster; compounds with distinct retention times appear in different clusters.

## Limitations

- RT normalization assumes features from the same compound have approximately equal retention times; co-eluting isomers or features with significant RT drift within a compound may be incorrectly scored.
- The choice of normalization function (inverse distance, Gaussian kernel, etc.) is not explicitly specified in the article; different kernels may produce different clustering outcomes.
- Retention time correction (retcor) quality depends on alignment of QC standards across runs; poor RT correction propagates into incorrect normalization.
- RT similarity alone cannot distinguish isobars or features with identical retention times; correlational similarity must provide discrimination, but low correlation variance may yield ambiguous scores.

## Evidence

- [intro] two features derived from the same compound with have (approximately) the same retention time: "two features derived from the same compound with have (approximately) the same retention time. The second is that two features derived from the same compound will have (approximately) the same"
- [other] Normalize retention time differences into a similarity score on a scale of 0–1: "Normalize retention time differences into a similarity score (e.g., inverse distance or Gaussian kernel) on a scale of 0–1."
- [other] A score of 1×1=1 indicates features likely derive from one compound: "A score of 1×1=1 indicates features likely derive from one compound, while scores like 1×0=0 or 0×1=0 indicate features represent different compounds."
- [other] Extract retention time values and correlation coefficients for all feature pairs: "Extract retention time values and correlation coefficients for all feature pairs from the XCMS-processed feature table."
- [intro] correct for drive in retention time: "xset <- retcor(xset, family = "symmetric", plottype = NULL)  # correct for drive in retention time"
- [intro] the product of the two similarity scores provides the best approximatio of the total similarity score: "Since both conditions must be met, the product of the two similarity scores provides the best approximatio of the total similarity score"
