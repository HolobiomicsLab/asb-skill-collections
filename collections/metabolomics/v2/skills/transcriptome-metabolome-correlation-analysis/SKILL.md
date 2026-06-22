---
name: transcriptome-metabolome-correlation-analysis
description: Use when you have paired spatial transcriptome and metabolome feature matrices (e.g., from .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3463
  edam_topics:
  - http://edamontology.org/topic_3674
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3520
  tools:
  - haCCA
derived_from:
- doi: 10.1101/2024.08.20.608773v2
  title: haCCA
evidence_spans:
- haCCA, a workflow utilizing high Correlated feature pairs combined with a modified spatial morphological alignment
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_hacca_cq
    doi: 10.1101/2024.08.20.608773v2
    title: haCCA
  dedup_kept_from: coll_hacca_cq
schema_version: 0.2.0
---

# transcriptome-metabolome-correlation-analysis

## Summary

Identify and rank high-correlation feature pairs between spatial transcriptome and metabolome datasets by computing pairwise correlation coefficients and filtering by a correlation threshold. This skill enables spot-to-spot multi-omics integration by surfacing the strongest transcriptome–metabolome associations for downstream alignment and fusion.

## When to use

Apply this skill when you have paired spatial transcriptome and metabolome feature matrices (e.g., from .h5ad files with expression and spatial coordinates) and need to discover which transcriptome features co-vary most strongly with which metabolome features as a prerequisite for spatial multi-omics integration.

## When NOT to use

- Input feature matrices are already reduced to pre-selected feature pairs (e.g., from prior hypothesis-driven curation); this skill is designed for unbiased discovery.
- Metabolome and transcriptome samples are not spatially co-registered or do not share the same spot coordinates; spatial alignment presupposes spatial overlap.
- Only unimodal (single-omics) data is available; the skill requires paired transcriptome–metabolome measurements.

## Inputs

- Spatial transcriptome feature matrix (numpy array or scipy sparse matrix; X from .h5ad)
- Metabolome feature matrix (numpy array or scipy sparse matrix; X from .h5ad)
- Spatial coordinate matrix for transcriptome data (obsm['spatial'] from .h5ad)
- Spatial coordinate matrix for metabolome data (obsm['spatial'] from .h5ad)

## Outputs

- Ranked list of high-correlation feature pairs with absolute correlation coefficients
- Metadata table: transcriptome feature ID, metabolome feature ID, correlation score, p-value (if computed)
- Filtered feature pair indices or boolean masks for downstream alignment

## How to apply

Load the spatial transcriptome feature matrix X and metabolome feature matrix X from input .h5ad files. Compute pairwise Pearson or Spearman correlation coefficients between all transcriptome features and all metabolome features. Apply a correlation threshold (e.g., absolute value ≥ 0.7 or domain-specific cutoff) to retain only high-correlation pairs, filtering out noise and spurious associations. Rank the retained pairs by absolute correlation coefficient in descending order. Return a ranked feature pair list with correlation scores and metadata (feature names, p-values if applicable). This prioritized list of correlated pairs is then combined with modified spatial morphological alignment in haCCA to ensure high-resolution spot-to-spot data integration.

## Related tools

- **haCCA** (Multi-module workflow that integrates high-correlation feature pairs with modified spatial morphological alignment for spot-to-spot spatial transcriptome and metabolome fusion) — github.com/LittleLittleCloud/haCCA

## Examples

```
from hacca import *; a_h5ad = sc.read_h5ad('/path/to/transcriptome.h5ad'); b_h5ad = sc.read_h5ad('/path/to/metabolome.h5ad'); correlations = np.corrcoef(a_h5ad.X.toarray(), b_h5ad.X.toarray()); high_corr_pairs = np.argwhere(np.abs(correlations) >= 0.7); ranked_pairs = high_corr_pairs[np.argsort(-np.abs(correlations[high_corr_pairs[:, 0], high_corr_pairs[:, 1]]))]
```

## Evaluation signals

- Correlation coefficients fall within the valid range [−1, 1] and are correctly sorted in descending order by absolute value.
- Number of retained pairs after thresholding is reasonable (not empty; typically 1–30% of the full pairwise matrix depending on biological noise and threshold stringency).
- Top-ranked pairs exhibit biological plausibility (e.g., known metabolic enzymes correlate with their substrate/product metabolites, or validated pathway members co-occur).
- P-values (if computed) are consistent with correlation magnitudes: larger absolute correlations typically yield smaller p-values.
- Downstream spatial alignment using the ranked pairs produces better spot-to-spot integration accuracy (lower residual error, higher overlap of aligned spatial regions) compared to random or unfiltered pairs.

## Limitations

- Pearson and Spearman correlation assume linear relationships; non-linear associations may be missed.
- High correlation does not imply causation; strong pairs may reflect confounding by technical batch effects or shared cell-type composition rather than direct biochemical interaction.
- Threshold selection is data-dependent and user-specified; no universal cutoff is provided in the article. Overly stringent thresholds may lose true associations; permissive thresholds introduce noise.
- The workflow assumes complete feature matrices with no missing values; sparse or incomplete data may require imputation before correlation computation.
- No changelog or versioning strategy is provided for the haCCA tool, limiting reproducibility across releases.

## Evidence

- [other] Compute pairwise Pearson or Spearman correlation coefficients between all transcriptome features and all metabolome features.: "Compute pairwise Pearson or Spearman correlation coefficients between all transcriptome features and all metabolome features."
- [intro] haCCA, a workflow utilizing high Correlated feature pairs combined with a modified spatial morphological alignment to ensure high resolution and accuracy of spot-to-spot data integration of spatial transcriptomes and metabolomes.: "haCCA, a workflow utilizing high Correlated feature pairs combined with a modified spatial morphological alignment to ensure high resolution and accuracy of spot-to-spot data integration"
- [other] Filter feature pairs by correlation threshold to retain only high-correlation pairs. Rank filtered pairs by absolute correlation coefficient in descending order.: "Filter feature pairs by correlation threshold to retain only high-correlation pairs. Rank filtered pairs by absolute correlation coefficient in descending order."
- [readme] Data is a triplet of (X: np.ndarray, D: np.ndarray, Label: Optional[np.ndarray]), where X is the feature matrix, D is the spatial matrix that contains the location information: "Data is a triplet of (X: np.ndarray, D: np.ndarray, Label: Optional[np.ndarray]), where X is the feature matrix, D is the spatial matrix"
- [other] Load spatial transcriptome feature matrix and metabolome feature matrix from input files.: "Load spatial transcriptome feature matrix and metabolome feature matrix from input files."
