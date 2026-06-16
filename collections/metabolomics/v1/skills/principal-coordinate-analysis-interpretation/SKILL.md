---
name: principal-coordinate-analysis-interpretation
description: Use when when you have computed pairwise distances between MS2 fingerprint vectors from multiple metabolomics samples and need to visualize sample similarity relationships in low dimensions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - Python 3.8
  - numpy
  - scikit-bio
  - memo-ms
  - MEMO
derived_from:
- doi: 10.3389/fbinf.2022.842964
  title: memo
evidence_spans:
- conda create --name memo python=3.8
- pip install numpy
- conda install -c conda-forge scikit-bio
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_memo
    doi: 10.3389/fbinf.2022.842964
    title: memo
  dedup_kept_from: coll_memo
schema_version: 0.2.0
---

# Principal Coordinate Analysis (PCoA) Interpretation

## Summary

PCoA reduces pairwise sample distances from MS2 fingerprint vectors to 2D coordinates for visual comparison of metabolomics samples. It enables identification of sample clusters and compositional similarities when retention time alignment or feature overlap is poor.

## When to use

When you have computed pairwise distances between MS2 fingerprint vectors from multiple metabolomics samples and need to visualize sample similarity relationships in low dimensions. Particularly valuable when samples are chemically diverse (poor feature overlap), acquired across different LC methods or mass spectrometer platforms, or subject to strong retention time shifts that preclude traditional feature-based comparison.

## When NOT to use

- Input is already a 2D or lower-dimensional embedding—PCoA reduces dimensionality from pairwise distances, not from high-dimensional feature tables.
- Sample size is very small (n<3)—coordinate axes become unstable and visual patterns unreliable.
- Distance matrix violates the assumption of Euclidean or metric geometry—PCoA assumes metric distances; non-metric dissimilarity measures may produce misleading coordinates.

## Inputs

- MemoMatrix file (sample-by-fingerprint count matrix)
- Pairwise distance matrix computed from aligned MS2 fingerprints
- Optional: sample group labels or metadata for coloring/annotation

## Outputs

- 2D PCoA coordinate table (samples × 2 principal coordinates)
- 2D scatter plot visualization of sample positions
- Coordinate export file (CSV or similar) for downstream analysis

## How to apply

Load the sample-by-fingerprint matrix (MemoMatrix) using memo-ms and compute pairwise distances between fingerprint vectors. Apply PCoA (or equivalent MDS) to reduce the distance matrix to 2D coordinates using scikit-bio or equivalent. Plot samples as points in 2D space, optionally coloring or labeling by group identity or metadata. Examine clustering patterns: samples near each other in coordinate space share similar MS2 fragmentation signatures, indicating compositional similarity, while distant samples indicate distinct metabolite profiles. The quality of separation reflects the strength of group differentiation in MS2 fingerprint space.

## Related tools

- **memo-ms** (Load and parse MemoMatrix sample-by-fingerprint files; provides interface to fingerprint data structures) — https://github.com/mandelbrot-project/memo
- **scikit-bio** (Compute PCoA and reduce distance matrix to 2D coordinates)
- **numpy** (Numerical computation and array manipulation for distance and coordinate calculations)
- **MEMO** (Parent workflow: generates MS2 fingerprints and manages the full sample comparison pipeline including visualization options) — https://github.com/mandelbrot-project/memo

## Examples

```
from memo_ms import MemoMatrix; from skbio.diversity import beta_diversity; import numpy as np; mm = MemoMatrix.load('samples.memoMatrix'); dist = mm.compute_distances(metric='euclidean'); pca = beta_diversity('euclidean', mm.data, ids=mm.sample_ids); pca.plot(cmap='viridis').savefig('pcoA_plot.png')
```

## Evaluation signals

- Coordinate table contains exactly 2 columns (PCoA axes 1 and 2) with one row per sample; all values are finite numbers.
- Samples with known similar metabolite composition cluster visually in the 2D plot; visually distant samples show compositional differentiation.
- Replicate samples (technical or biological replicates of the same source) occupy nearby regions; if replicates scatter widely, fingerprinting or distance computation may be unreliable.
- The proportion of variance explained by the first two principal coordinates is reported and reasonable (>50% is typical; <30% suggests the dominant sample differences require >2 dimensions).
- Scatter plot axis labels clearly identify coordinates as 'PCoA1' and 'PCoA2' with variance explained (%) noted; legend identifies sample groups or metadata.

## Limitations

- PCoA assumes metric distances; if the distance metric violates triangle inequality or is non-Euclidean, coordinate positions may not accurately reflect true dissimilarity.
- MS2 fingerprint quality depends on spectral peak detection and neutral loss annotation; biased or noisy peak lists produce distorted distances and misleading coordinate patterns.
- Visualization of only the first 2 principal coordinates may obscure higher-dimensional structure; examine scree plot (variance per axis) to assess information loss.
- Sample grouping is inferred visually; no statistical test of cluster significance is inherent to PCoA plotting. Additional statistical testing (e.g., PERMANOVA, Adonis) is required to validate group separation.
- Retention time shifts between samples do not affect MS2 fingerprints, but if LC–MS runs have very different instrument tuning or acquisition parameters, MS2 peak intensities may vary systematically, biasing distance estimates.

## Evidence

- [other] Compute pairwise sample distances from the fingerprint vectors. Apply Multidimensional Scaling (MDS) or Principal Coordinate Analysis (PCoA) to reduce the distance matrix to 2D coordinates.: "Compute pairwise sample distances from the fingerprint vectors. Apply Multidimensional Scaling (MDS) or Principal Coordinate Analysis (PCoA) to reduce the distance matrix to 2D coordinates."
- [other] Generate a 2D scatter plot with samples as points, colored or labeled by group identity if provided.: "Generate a 2D scatter plot with samples as points, colored or labeled by group identity if provided."
- [other] MEMO applies MDS/PCoA visualization techniques to aligned MS2 fingerprints to generate low-dimensional embeddings that enable visual comparison of different samples.: "MEMO applies MDS/PCoA visualization techniques to aligned MS2 fingerprints to generate low-dimensional embeddings that enable visual comparison of different samples."
- [other] MEMO suits particularly well to compare chemodiverse samples, ie with a poor features overlap, or to compare samples with a strong RT shift, acquired using different LC methods or even different mass spectrometers technology: "MEMO suits particularly well to compare chemodiverse samples, ie with a poor features overlap, or to compare samples with a strong RT shift, acquired using different LC methods or even different mass"
- [intro] different filtering (remove peaks/losses from blanks for example) and visualization techniques (MDS/PCoA, TMAP, Heatmap, ...) can be used: "different filtering (remove peaks/losses from blanks for example) and visualization techniques (MDS/PCoA, TMAP, Heatmap, ...) can be used"
