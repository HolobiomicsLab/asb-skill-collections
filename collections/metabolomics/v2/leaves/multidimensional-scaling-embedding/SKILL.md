---
name: multidimensional-scaling-embedding
description: Use when after computing a pairwise sample distance matrix from aligned
  MS2 fingerprint vectors and you need to visualize sample relationships, clustering,
  or separation by group identity in 2D space.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3727
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - Python 3.8
  - numpy
  - scikit-bio
  - MEMO
  - memo-ms
  - scikit-learn
  - matchms
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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

# multidimensional-scaling-embedding

## Summary

Apply Multidimensional Scaling (MDS) or Principal Coordinate Analysis (PCoA) to a pairwise distance matrix derived from MS2 fingerprints to produce a low-dimensional (typically 2D) embedding suitable for visual sample comparison and grouping. This technique is essential for exploring chemodiverse metabolomics datasets where feature overlap is poor or retention time shifts are significant.

## When to use

After computing a pairwise sample distance matrix from aligned MS2 fingerprint vectors and you need to visualize sample relationships, clustering, or separation by group identity in 2D space. Particularly suited when comparing chemodiverse samples with poor feature overlap or strong retention time shifts across different LC methods or mass spectrometer technologies.

## When NOT to use

- Input is already a fully processed feature table or abundance matrix from standard metabolomics pipelines (OTU/ASV tables) — MDS/PCoA is designed specifically for MS2 fingerprint-derived distances, not count-based data
- Sample counts are very low (n < 3) — meaningful 2D embedding requires sufficient samples to establish robust pairwise relationships
- Distance metric is not defined or samples have not been pre-aligned to a common MS2 fingerprint space — embedding requires a valid, pre-computed distance matrix

## Inputs

- MemoMatrix file (sample-by-MS2-fingerprint matrix in tabular or HDF5 format)
- Pairwise sample distance matrix (symmetric n×n matrix, typically computed from fingerprint vectors)
- Optional: sample metadata or group assignments for coloring/labeling

## Outputs

- 2D coordinate table (sample identifiers and their x,y embedding coordinates)
- 2D scatter plot visualization (PNG, PDF, or interactive HTML format)
- Distance matrix used for embedding (for reproducibility)

## How to apply

Load the MemoMatrix (sample-by-fingerprint matrix) using memo-ms, then compute pairwise Euclidean or other suitable distances between all sample fingerprint vectors using numpy or scikit-bio. Apply either MDS (preserving overall pairwise distances) or PCoA (preserving distances via eigendecomposition of the distance matrix) to reduce the distance matrix to 2D coordinates. Generate a 2D scatter plot with samples as points, coloring or labeling by group identity if available. The choice between MDS and PCoA depends on the distance metric used: PCoA is appropriate for phylogenetic or ecological distance metrics, while MDS is more general. Verify that the resulting 2D projection preserves meaningful separation by inspecting stress values (for MDS) or the proportion of variance explained by the first two principal coordinates.

## Related tools

- **MEMO** (Core method for MS2-based sample vectorization and fingerprint generation; orchestrates the full workflow including MDS/PCoA embedding) — https://github.com/mandelbrot-project/memo
- **memo-ms** (Python package for loading and manipulating MemoMatrix files; handles fingerprint matrix I/O) — https://pypi.org/project/memo-ms/
- **scikit-bio** (Provides PCoA implementation and distance matrix utilities for metabolomics-style embeddings) — https://github.com/scikit-bio/scikit-bio
- **numpy** (Core numerical library for distance matrix computation and 2D coordinate manipulation)
- **scikit-learn** (Alternative source for MDS implementation (sklearn.manifold.MDS) for dimensionality reduction)
- **matchms** (Underlying package used by MEMO for MS2 spectrum handling and preprocessing) — https://github.com/matchms/matchms

## Examples

```
from memo_ms import load_memorix; from scipy.spatial.distance import pdist, squareform; from skbio.diversity import pcoa; import pandas as pd; matrix = load_memorix('fingerprints.txt'); distances = squareform(pdist(matrix.values, metric='euclidean')); coords = pcoa(distances); coords.samples[['PC1', 'PC2']].to_csv('embedding_2d.csv')
```

## Evaluation signals

- 2D scatter plot shows clear visual separation of sample groups (if group metadata is available), indicating that the fingerprint distances are meaningful
- Stress value (for MDS) or proportion of variance explained by the first two principal coordinates is acceptable (typically >50% for PCoA, or stress <0.1 for MDS)
- Distance matrix used for embedding is symmetric and all pairwise distances are non-negative
- Output coordinate table has exactly 2 columns (x, y) with one row per unique sample, matching the sample identifiers from the input MemoMatrix
- Samples that are expected to be similar (e.g., technical replicates or same organism grown under similar conditions) cluster together in 2D space

## Limitations

- MDS/PCoA reduction to 2D may obscure higher-dimensional structure present in the full fingerprint space; stress values or variance explained should be inspected to assess adequacy of 2D representation
- Results are sensitive to the choice of distance metric (Euclidean vs. other metrics); different metrics may yield substantially different embeddings
- Visualization quality depends on the degree of sample-to-sample variation; chemodiverse samples may produce widely scattered embeddings that are harder to interpret
- Blank filtering and other preprocessing steps applied to fingerprints before distance computation can substantially alter the resulting embedding; workflow reproducibility requires careful documentation of filtering thresholds
- PCoA requires non-negative eigenvalues and may fail or require correction if the distance matrix violates the triangle inequality or is non-Euclidean; MDS is more robust to such matrices

## Evidence

- [other] MEMO applies MDS/PCoA visualization techniques to aligned MS2 fingerprints to generate low-dimensional embeddings that enable visual comparison of different samples.: "MEMO applies MDS/PCoA visualization techniques to aligned MS2 fingerprints to generate low-dimensional embeddings that enable visual comparison of different samples"
- [intro] Fingerprint generation and alignment workflow steps with MDS/PCoA specified as a visualization technique.: "different filtering (remove peaks/losses from blanks for example) and visualization techniques (MDS/PCoA, TMAP, Heatmap, ...) can be used"
- [intro] MEMO suits particularly well to compare chemodiverse samples with poor feature overlap or strong RT shifts.: "MEMO suits particularly well to compare chemodiverse samples, ie with a poor features overlap, or to compare samples with a strong RT shift, acquired using different LC methods or even different mass"
- [intro] MS2 fingerprints are generated by counting MS2 peaks and neutral losses in each sample.: "The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an *MS2 fingerprint* of the sample"
- [other] Workflow step specifying loading of MemoMatrix, distance computation, and 2D coordinate generation.: "Load the MemoMatrix file (sample-by-fingerprint matrix) using memo-ms. 2. Compute pairwise sample distances from the fingerprint vectors. 3. Apply Multidimensional Scaling (MDS) or Principal"
- [other] Tools required include memo-ms, Python 3.8, numpy, and scikit-bio for the full workflow.: "tools: MEMO, memo-ms, Python 3.8, numpy, scikit-bio"
- [readme] Environment setup and package installation instructions from README.: "conda env create -f environment.yml"
