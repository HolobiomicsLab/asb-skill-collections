---
name: sample-relationship-visualization
description: Use when after generating aligned MS2 fingerprints (sample-by-fingerprint matrices) from metabolomics data when you need to visually inspect sample clustering, identify sample similarities, or detect batch effects and RT shifts across different LC methods or mass spectrometer technologies.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3727
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python 3.8
  - numpy
  - scikit-bio
  - MEMO
  - memo-ms
  - matchms
  techniques:
  - LC-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# sample-relationship-visualization

## Summary

Apply Multidimensional Scaling (MDS) or Principal Coordinate Analysis (PCoA) to MS2 fingerprint distance matrices to generate low-dimensional 2D scatter plots that enable visual comparison and clustering of metabolomics samples. This skill is essential for identifying sample relationships and compositional similarities in chemodiverse datasets.

## When to use

Apply this skill after generating aligned MS2 fingerprints (sample-by-fingerprint matrices) from metabolomics data when you need to visually inspect sample clustering, identify sample similarities, or detect batch effects and RT shifts across different LC methods or mass spectrometer technologies. Use it particularly when samples have poor feature overlap or strong retention time variations that make traditional feature-based alignment problematic.

## When NOT to use

- Input data is already a low-dimensional embedding (e.g., from a prior MDS/PCoA run) — skip dimensionality reduction and proceed directly to visualization.
- Sample size is very small (< 3 samples) — dimensionality reduction becomes unreliable; consider alternative visualization methods or increase sample count.
- Fingerprints have not been aligned or filtered — apply alignment and blank-removal filtering before computing distances.

## Inputs

- MemoMatrix file (sample-by-fingerprint matrix in CSV or HDF5 format)
- Sample metadata table (optional, for group labeling)
- Pairwise distance matrix computed from fingerprint vectors

## Outputs

- 2D coordinate table (samples × 2 dimensions)
- 2D scatter plot visualization (PNG/PDF)
- Distance matrix (optional, for downstream analysis)

## How to apply

Load the MemoMatrix file (sample-by-fingerprint matrix) containing aligned MS2 peak and neutral loss counts using memo-ms. Compute pairwise distances between samples using Euclidean or other appropriate metrics on the fingerprint vectors. Apply MDS or PCoA dimensionality reduction to project the distance matrix into 2D coordinates, preserving sample-to-sample relationships. Generate a 2D scatter plot with samples as individual points, optionally coloring or labeling by group identity, batch, or instrument type if metadata is available. Export both the coordinate table (for downstream statistical analysis) and the visualization (PNG/PDF) as separate files for integration into publications or interactive analysis platforms.

## Related tools

- **MEMO** (Core framework for MS2-based sample vectorization and fingerprint alignment) — https://github.com/mandelbrot-project/memo
- **memo-ms** (Command-line and Python interface for loading and manipulating MemoMatrix files)
- **scikit-bio** (Provides PCoA implementation and distance-based dimensionality reduction routines)
- **numpy** (Matrix operations and distance computation on fingerprint vectors)
- **matchms** (Underlying spectral processing and metadata handling for MS2 data) — https://github.com/matchms/matchms

## Evaluation signals

- 2D scatter plot displays visually distinct clusters or groupings corresponding to expected sample categories (e.g., treatment vs. control, different instruments, different LC methods).
- Coordinate table contains exactly N rows (number of samples) and 2 numeric columns with no NaN or infinite values; sum of variance explained by the first two dimensions should be reported.
- Samples from the same source or condition cluster together; high within-group coherence and low between-group overlap is expected for well-separated groups.
- Stress/goodness-of-fit metric for MDS (or proportion of variance explained for PCoA) is documented and acceptable for interpretation (e.g., MDS stress < 0.2 for adequate representation).
- Visualization file is readable and points are clearly distinguishable; metadata-driven coloring matches the provided group labels without gaps or misalignment.

## Limitations

- MDS and PCoA are lossy projections; information beyond the first two dimensions is discarded. High-dimensional structure may not be fully captured, especially if samples form tight clusters in higher dimensions.
- Results depend on the choice of distance metric and fingerprint normalization; different metrics (Euclidean, cosine, Bray-Curtis) may yield different apparent relationships.
- Visualization quality degrades with very small sample sizes (< 5) or highly imbalanced groups; interpretation should be paired with statistical testing.
- Batch effects and technical variations (instrument drift, solvent contamination) embedded in MS2 fingerprints will persist in the plot and may obscure biological signals.
- The skill assumes that MS2 fingerprints have already been properly aligned and filtered (blanks removed); garbage-in-garbage-out applies if upstream steps are incomplete.

## Evidence

- [other] 1. Load the MemoMatrix file (sample-by-fingerprint matrix) using memo-ms. 2. Compute pairwise sample distances from the fingerprint vectors. 3. Apply Multidimensional Scaling (MDS) or Principal Coordinate Analysis (PCoA) to reduce the distance matrix to 2D coordinates. 4. Generate a 2D scatter plot with samples as points, colored or labeled by group identity if provided.: "Apply Multidimensional Scaling (MDS) or Principal Coordinate Analysis (PCoA) to reduce the distance matrix to 2D coordinates. 4. Generate a 2D scatter plot with samples as points, colored or labeled"
- [intro] 2: "different filtering (remove peaks/losses from blanks for example) and visualization techniques (MDS/PCoA, TMAP, Heatmap, ...) can be used"
- [intro] 3: "MEMO suits particularly well to compare chemodiverse samples, ie with a poor features overlap, or to compare samples with a strong RT shift, acquired using different LC methods or even different mass"
- [other] 4: "The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an MS2 fingerprint of the sample"
- [readme] 5: "The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an MS2 fingerprint of the sample. These fingerprints can in a second stage be aligned"
