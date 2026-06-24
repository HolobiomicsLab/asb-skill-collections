---
name: metabolomics-sample-comparison
description: Use when you have a MemoMatrix (sample-by-fingerprint matrix) from aligned
  MS2 spectra and need to visually compare sample similarity or clustering patterns,
  especially when samples show poor feature overlap, strong retention time shifts
  across different LC methods, or were acquired on different.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0092
  tools:
  - Python 3.8
  - numpy
  - scikit-bio
  - MEMO
  - memo-ms
  - Python 3.8+
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.3389/fbinf.2022.842964
  title: memo
evidence_spans:
- conda create --name memo python=3.8
- pip install numpy
- conda install -c conda-forge scikit-bio
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_memo
    doi: 10.3389/fbinf.2022.842964
    title: memo
  dedup_kept_from: coll_memo
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3389/fbinf.2022.842964
  all_source_dois:
  - 10.3389/fbinf.2022.842964
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-sample-comparison

## Summary

Apply MDS or PCoA dimensionality reduction to MS2 fingerprint vectors to generate low-dimensional sample comparison plots, enabling visual clustering and relationship assessment of chemodiverse metabolomics samples independent of retention time.

## When to use

You have a MemoMatrix (sample-by-fingerprint matrix) from aligned MS2 spectra and need to visually compare sample similarity or clustering patterns, especially when samples show poor feature overlap, strong retention time shifts across different LC methods, or were acquired on different mass spectrometer technologies (e.g., Maxis Q-ToF vs. Q-Exactive Orbitrap).

## When NOT to use

- Input is already a pre-computed distance matrix or coordinate table from a different method (e.g., from TMAP or Heatmap); skip to visualization.
- Sample set contains <3 unique samples; MDS/PCoA requires sufficient dimensionality to meaningfully reduce.
- All samples have identical or near-identical MS2 fingerprints (e.g., technical replicates with zero variance); dimensionality reduction will not reveal structure.

## Inputs

- MemoMatrix file (sample-by-fingerprint matrix from aligned MS2 spectra)
- Sample grouping/metadata (optional, for coloring/labeling points)

## Outputs

- 2D coordinate table (samples × 2D positions)
- 2D scatter plot visualization (SVG, PNG, or interactive HTML)
- Pairwise sample distance matrix (intermediate)

## How to apply

Load the MemoMatrix using memo-ms and compute pairwise sample distances from the aligned MS2 fingerprint vectors. Apply Multidimensional Scaling (MDS) or Principal Coordinate Analysis (PCoA) to reduce the distance matrix to 2D coordinates suitable for visualization. Generate a 2D scatter plot with samples as points, optionally colored or labeled by sample group identity. The resulting low-dimensional embedding preserves relative sample distances and reveals patterns in sample composition that would be obscured by retention time shifts or feature sparsity. Export both the coordinate table and the visualization for downstream interpretation and publication.

## Related tools

- **MEMO** (Core framework providing MS2 fingerprint alignment and sample vectorization that feeds into MDS/PCoA visualization) — https://github.com/mandelbrot-project/memo
- **memo-ms** (Python package for loading and parsing MemoMatrix files and aligned MS2 fingerprint data)
- **scikit-bio** (Provides PCoA (Principal Coordinate Analysis) implementation for dimensionality reduction of distance matrices)
- **numpy** (Numerical computation of pairwise sample distances from fingerprint vectors)
- **Python 3.8+** (Runtime environment (Python 3.8 minimum; ≥3.9 recommended for string methods))

## Examples

```
from memo_ms import load_memomatrix; from scipy.spatial.distance import pdist, squareform; from skbio.diversity import beta_diversity; import numpy as np; M = load_memomatrix('samples.memomatrix'); D = squareform(pdist(M, metric='euclidean')); coords = beta_diversity('pcoa', D); coords.plot(kind='scatter')
```

## Evaluation signals

- 2D coordinates are centered near origin with sensible variance (Euclidean distance between points matches input distance matrix).
- Visually distinct sample groups (if metadata provided) cluster together; technical replicates or closely related samples occupy nearby regions.
- Eigenvalue plot (if generated) shows that the first two principal coordinates capture sufficient variance (typically >50% combined for informative plots).
- Coordinate table has exactly N rows (one per sample) and 2 columns (PC1, PC2); no NaN or infinite values.
- Distance preservation: Euclidean distance between any two samples in the 2D plot is monotonically correlated with the original pairwise distance (Spearman ρ > 0.8).

## Limitations

- MDS/PCoA is sensitive to outlier samples with extreme fingerprints; consider filtering or blanks removal before dimensionality reduction.
- 2D representation discards higher-order structure; if variance in PC3+ is substantial (>20%), consider 3D visualization or alternative methods (TMAP).
- Sample grouping or visual patterns may be confounded by batch effects, sequencing/instrument drift, or environmental factors not captured in the fingerprint.
- Results depend on prior MS2 peak/neutral loss filtering and fingerprint alignment quality; garbage fingerprints produce uninterpretable plots.

## Evidence

- [other] MEMO applies MDS/PCoA visualization techniques to aligned MS2 fingerprints to generate low-dimensional embeddings that enable visual comparison of different samples.: "MEMO applies MDS/PCoA visualization techniques to aligned MS2 fingerprints to generate low-dimensional embeddings that enable visual comparison of different samples."
- [other] Apply Multidimensional Scaling (MDS) or Principal Coordinate Analysis (PCoA) to reduce the distance matrix to 2D coordinates.: "Apply Multidimensional Scaling (MDS) or Principal Coordinate Analysis (PCoA) to reduce the distance matrix to 2D coordinates."
- [other] The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an MS2 fingerprint of the sample. These fingerprints can in a second stage be aligned to compare different samples.: "The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an *MS2 fingerprint* of the sample. These fingerprints can in a second stage be aligned"
- [other] MEMO suits particularly well to compare chemodiverse samples, ie with a poor features overlap, or to compare samples with a strong RT shift, acquired using different LC methods or even different mass spectrometers technology (MaXis Q-ToF vs Q-Exactive).: "MEMO suits particularly well to compare chemodiverse samples, *i.e.* with a poor features overlap, or to compare samples with a strong RT shift, acquired using different LC methods or even different"
- [intro] different filtering (remove peaks/losses from blanks for example) and visualization techniques (MDS/PCoA, TMAP, Heatmap, ...) can be used: "different filtering (remove peaks/losses from blanks for example) and visualization techniques (MDS/PCoA, TMAP, Heatmap, ...) can be used"
- [other] Compute pairwise sample distances from the fingerprint vectors.: "Compute pairwise sample distances from the fingerprint vectors."
- [other] Generate a 2D scatter plot with samples as points, colored or labeled by group identity if provided.: "Generate a 2D scatter plot with samples as points, colored or labeled by group identity if provided."
