---
name: feature-pair-scoring-in-metabolomics
description: Use when use this skill after XCMS feature detection and alignment on
  non-targeted LC-MS or GC-MS metabolomics data, when you have aligned features with
  quantitative profiles across samples and need to group features that co-originate
  from the same compound (accounting for isotopic peaks, adducts.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0821
  tools:
  - R
  - XCMS
  - dynamicTreeCut
  - RAMClustR
  techniques:
  - LC-MS
  - GC-MS
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

# Reconstruct the total similarity score as the product of retention time and correlational similarity

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compute pairwise total similarity scores for metabolomics features by multiplying retention time similarity and correlational similarity metrics. This scoring approach identifies features likely derived from the same compound (score → 1) versus different compounds (score → 0), enabling unsupervised feature clustering in non-targeted LC-MS and GC-MS data.

## When to use

Use this skill after XCMS feature detection and alignment on non-targeted LC-MS or GC-MS metabolomics data, when you have aligned features with quantitative profiles across samples and need to group features that co-originate from the same compound (accounting for isotopic peaks, adducts, and fragments). Apply it as a precursor to hierarchical clustering-based deconvolution.

## When NOT to use

- Features have not yet been detected and aligned by XCMS or equivalent; use feature detection first.
- Dataset contains only a single sample or very few samples; Pearson correlation coefficients become unstable and unreliable.
- Input is already grouped or annotated as single compounds; the purpose of this skill is de novo grouping, not validation.
- Retention time correction (retcor) has not been applied; uncorrected RT drift will inflate false similarity scores.

## Inputs

- XCMS feature table with aligned m/z, retention time, and intensity values across samples (NetCDF, mzML, or CSV format)
- Feature quantification matrix (samples × features) with missing value imputation completed (e.g., via fillPeaks)

## Outputs

- Symmetric pairwise total similarity matrix (features × features)
- Retention time similarity matrix (intermediate)
- Correlational similarity matrix / Pearson correlation coefficient matrix (intermediate)

## How to apply

Extract retention time (RT) values and Pearson correlation coefficients for all feature pairs from XCMS-processed feature tables. Normalize RT differences into a similarity score (0–1 scale; e.g., Gaussian kernel or inverse distance function). Compute Pearson correlation coefficients between quantitative feature intensity profiles across all samples. Multiply the RT similarity and correlational similarity scores element-wise for each feature pair to produce a symmetric total similarity matrix. The product-based scoring is justified because both conditions (same RT and same quantitative trend) must hold simultaneously for features to originate from one compound; hence product captures this AND logic better than sum or other combinations. Output the resulting symmetric similarity matrix in a format suitable for hierarchical clustering (e.g., distance matrix or similarity matrix for input to dynamicTreeCut).

## Related tools

- **XCMS** (Detects aligned features (m/z, RT, intensity) and provides the input feature table with sample-wise quantification) — https://bioconductor.org/packages/xcms/
- **R** (Execution environment for Pearson correlation computation, matrix normalization, and element-wise multiplication)
- **dynamicTreeCut** (Receives the output similarity matrix and performs hierarchical clustering and dendrogram cutting to group features) — https://cran.r-project.org/package=dynamicTreeCut
- **RAMClustR** (Wraps this scoring workflow and hierarchical clustering into a unified unsupervised feature deconvolution pipeline) — https://github.com/cbroeckl/RAMClustR

## Examples

```
RC <- ramclustR(xcmsObj = xset, ExpDes=experiment)
```

## Evaluation signals

- Symmetry check: verify the output similarity matrix is symmetric (matrix[i,j] ≈ matrix[j,i]) to within numerical precision.
- Range check: all entries in the total similarity matrix must lie in [0, 1] (product of two [0,1] scores).
- High-confidence groupings: feature pairs with total similarity = 1.0 should exhibit both RT proximity (within instrument tolerance, typically <0.5 min for LC-MS) and Pearson r > 0.9 across samples.
- Low-confidence separation: feature pairs with total similarity = 0 or near-zero should show either significant RT divergence OR very weak correlation (|r| < 0.3).
- Dendrogram cluster coherence: after hierarchical clustering of the similarity matrix, cut clusters should yield features within each cluster that share near-identical MS/MS fragmentation patterns and molecular formulas when further analyzed.

## Limitations

- Pearson correlation assumes linear co-variation; non-linear abundance relationships or batch effects not corrected by QC normalization may inflate spurious correlations between unrelated features.
- Retention time tolerance is instrument- and column-dependent; the RT similarity normalization function (e.g., Gaussian kernel bandwidth) must be calibrated per platform and may require manual tuning.
- Features with very low intensity or sparse detection across samples may have unstable correlation estimates, inflating false similarities; pre-filtering by coefficient of variation (CV) is recommended.
- The product rule assumes independence of RT and correlation signals; strong confounding between retention time and sample batch effects can bias both metrics simultaneously.
- No changelog or version history documented; reproducibility across RAMClustR versions may be compromised.

## Evidence

- [intro] RT and correlational similarity product approach: "RAMClustR calculates a pairwise total similarity score as the product of retention time similarity and correlational similarity scores."
- [intro] Interpretation of score outcomes: "A score of 1×1=1 indicates features likely derive from one compound, while scores like 1×0=0 or 0×1=0 indicate features represent different compounds."
- [intro] Two necessary conditions for same-compound features: "two features derived from the same compound with have (approximately) the same retention time. The second is that two features derived from the same compound will have (approximately) the same"
- [intro] Product justification: AND logic: "Since both conditions must be met, the product of the two similarity scores provides the best approximatio of the total similarity score"
- [readme] Concrete workflow steps from README: "ramclustObj <- rc.ramclustr(ramclustObj = ramclustObj)"
- [intro] Feature detection and preprocessing pipeline: "xset <- fillPeaks(xset)  # 'fillPeaks' to remove missing values in final dataset"
