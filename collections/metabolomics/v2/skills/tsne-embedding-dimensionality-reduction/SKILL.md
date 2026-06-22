---
name: tsne-embedding-dimensionality-reduction
description: Use when when you have a precomputed similarity matrix of mass spectra (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - ms2deepscore
  - Python (scikit-learn or similar)
  - specXplore
  - Jupyter Notebooks
derived_from:
- doi: 10.1021/acs.analchem.3c04444
  title: specxplore
evidence_spans:
- t-SNE embedding that serves as an overview representation of mass spectral similarities based on ms2deepscore
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_specxplore
    doi: 10.1021/acs.analchem.3c04444
    title: specxplore
  dedup_kept_from: coll_specxplore
schema_version: 0.2.0
---

# tsne-embedding-dimensionality-reduction

## Summary

Applies t-SNE algorithm to a precomputed mass spectral similarity matrix (e.g., from ms2deepscore) to reduce high-dimensional spectral relationships into 2-D coordinates for interactive visualization and overview representation of LC-MS/MS data.

## When to use

When you have a precomputed similarity matrix of mass spectra (e.g., ms2deepscore-based similarities) and need to generate a low-dimensional (2-D) interactive overview representation that preserves local and global spectral relationships for exploratory dashboard visualization or feature clustering.

## When NOT to use

- Input spectral data is already in 2-D or lower-dimensional representation; t-SNE is unnecessary.
- Similarity matrix is sparse or contains many zero/missing values; t-SNE requires dense distance estimates.
- Real-time or streaming spectral data processing is required; t-SNE is computationally expensive and unsuitable for incremental updates.
- Quantitative interpretation of individual axis values is needed; t-SNE axes are arbitrary and not interpretable as physical or chemical scales.

## Inputs

- Processed spectral data object (specXplore session data format)
- Precomputed ms2deepscore similarity matrix (square, symmetric, float-valued)

## Outputs

- 2-D t-SNE coordinate array (spectrum_id, x-coordinate, y-coordinate)
- Structured output file with t-SNE coordinates (suitable for dashboard rendering)

## How to apply

Load the processed spectral data and precomputed ms2deepscore similarity matrix from the specXplore session data object. Apply the t-SNE algorithm using the ms2deepscore-derived distance metric (typically 1 − similarity) as input to reduce the high-dimensional spectral similarity space into 2-D coordinates. The algorithm iteratively minimizes the divergence between the high-dimensional similarity distribution and the low-dimensional point distribution. Extract the resulting 2-D coordinates (spectrum identifier paired with x, y positions) and save to a structured output file (e.g., CSV or JSON) for downstream dashboard rendering. Verify that the 2-D layout visually separates known spectral clusters and that all spectra are mapped without NaN or infinite values.

## Related tools

- **ms2deepscore** (Computes deep-learning-based similarity scores between mass spectra; output similarity matrix serves as input distance metric for t-SNE embedding) — https://github.com/matchms/ms2deepscore
- **Python (scikit-learn or similar)** (Implements t-SNE algorithm; reduces high-dimensional similarity space to 2-D coordinates)
- **specXplore** (Integrates t-SNE embedding within a complete workflow for interactive mass spectral data exploration; stores session data and renders dashboard visualization) — https://github.com/kevinmildau/specXplore
- **Jupyter Notebooks** (Interactive environment for preprocessing spectral data, computing embeddings, and launching the specXplore dashboard)

## Evaluation signals

- All spectra are successfully mapped to 2-D coordinates with no NaN, infinite, or duplicate values.
- 2-D layout visually clusters known or expected groups of similar spectra (verified by manual inspection or external class labels if available).
- Output file contains exactly as many entries as input spectra, with spectrum identifiers correctly preserved.
- t-SNE coordinates span reasonable ranges (no pathological clustering at a single point or extreme outliers that suggest convergence failure).
- Dashboard renders without errors and is interactive (nodes can be selected, hovered, and used to trigger overlay visualizations).

## Limitations

- t-SNE is computationally expensive; runtime scales poorly with increasing number of spectra (O(n²) or worse for exact implementations).
- t-SNE axes are not directly interpretable as physical or chemical quantities; the algorithm preserves local structure but not global scale or metric properties.
- Results are stochastic and depend on random initialization and hyperparameters (perplexity, learning rate, n_iter); rerunning may produce slightly different layouts.
- On macOS ARM64 systems, ms2deepscore may produce unreliable similarity predictions due to platform-specific issues (see README issue #199), directly affecting t-SNE input quality without warning.
- t-SNE requires a dense distance or similarity matrix; sparse or incomplete similarity data will cause failures or incorrect embeddings.

## Evidence

- [intro] t-SNE embedding that serves as an overview representation of mass spectral similarities based on ms2deepscore: "It joins a t-SNE embedding that serves as an overview representation of mass spectral similarities based on ms2deepscore"
- [other] Load precomputed similarity matrix and apply t-SNE with ms2deepscore distances to reduce high-dimensional spectral space to 2-D: "Load processed spectral data and precomputed ms2deepscore similarity matrix from the specXplore session data object. 2. Apply t-SNE algorithm with ms2deepscore distances as the input distance metric"
- [other] Save 2-D t-SNE coordinates (spectrum identifier and x, y positions) to structured output for downstream dashboard rendering: "Save the resulting 2-D t-SNE coordinates (spectrum identifier and x, y positions) to a structured output file for downstream dashboard rendering."
- [readme] specXplore workflow separates preprocessing in Jupyter notebooks (creating session data object) from dashboard visualization: "The specXplore workflow is separated into two stages. First, the user needs to process their spectral data in order to create a specxplore session data object. This is done in interactive Jupyter"
- [readme] macOS ARM64 systems have platform-specific issue affecting ms2deepscore reliability without error messages: "users making use of macos arm64 computers should be aware of issue 199 for ms2deepscore. The current ms2deepscore package version may lead to ms2deepscore similarity predictions that are not in"
