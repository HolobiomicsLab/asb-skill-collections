---
name: mass-spectrometry-data-coordinate-system-construction
description: Use when when you have processed LC-MS/MS spectral data in .mgf format with precomputed ms2deepscore similarity matrices and need a 2-D overview representation that preserves local spectral relationships for interactive exploration and visualization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ms2deepscore
  - scikit-learn t-SNE
  - specXplore
  - Jupyter notebooks
  techniques:
  - LC-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c04444
  all_source_dois:
  - 10.1021/acs.analchem.3c04444
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-data-coordinate-system-construction

## Summary

Construct a 2-D coordinate system from LC-MS/MS spectral data by applying t-SNE dimensionality reduction to ms2deepscore-computed pairwise similarity scores. This coordinate system serves as the foundation for interactive dashboard visualization and exploratory analysis of mass spectral relationships.

## When to use

When you have processed LC-MS/MS spectral data in .mgf format with precomputed ms2deepscore similarity matrices and need a 2-D overview representation that preserves local spectral relationships for interactive exploration and visualization. Use this skill after data preprocessing produces a specXplore session data object but before instantiating the dashboard for visual analysis.

## When NOT to use

- Input spectral data is in raw vendor format (.raw, .d) rather than converted to .mgf — perform data format conversion and feature detection first.
- ms2deepscore similarity scores have not been precomputed — compute similarity matrix before t-SNE embedding.
- You need to preserve 3 or more dimensions of spectral relationship information — t-SNE reduces to 2-D by design; consider alternative methods (UMAP, PCA) if higher dimensionality is required.

## Inputs

- processed spectral data object from specXplore session
- precomputed ms2deepscore similarity matrix (spectrum-to-spectrum distance matrix)
- spectrum metadata including feature identifiers

## Outputs

- 2-D t-SNE coordinate file mapping spectrum identifiers to (x, y) positions
- coordinate system metadata (e.g., t-SNE hyperparameters, distance metric used)

## How to apply

Load the processed spectral data and precomputed ms2deepscore similarity matrix from the specXplore session data object created in the Jupyter preprocessing stage. Apply the t-SNE algorithm using the ms2deepscore distances as the input distance metric to reduce the high-dimensional spectral similarity space into 2-D coordinates. The t-SNE embedding preserves local neighborhood structure of mass spectral similarities while rendering a viewable 2-D representation. Save the resulting 2-D coordinates (spectrum identifier paired with x, y positions) to a structured output file format compatible with the specXplore dashboard renderer. Verify that all spectrum identifiers from the input spectral data are represented in the coordinate output and that x, y values fall within reasonable bounds for the chosen t-SNE configuration.

## Related tools

- **ms2deepscore** (computes pairwise similarity scores between mass spectra, which serve as the input distance metric for t-SNE embedding) — https://github.com/matchms/ms2deepscore
- **scikit-learn t-SNE** (implements the t-SNE dimensionality reduction algorithm applied to ms2deepscore distance matrix)
- **specXplore** (orchestrates the full LC-MS/MS data exploration workflow including t-SNE coordinate generation and dashboard visualization) — https://github.com/kevinmildau/specXplore
- **Jupyter notebooks** (interactive environment for running the specXplore importing pipeline and t-SNE coordinate generation)

## Examples

```
from sklearn.manifold import TSNE; tsne = TSNE(n_components=2, random_state=42, metric='precomputed'); coords = tsne.fit_transform(ms2deepscore_similarity_matrix); output_df = pd.DataFrame({'spectrum_id': spectrum_ids, 'x': coords[:, 0], 'y': coords[:, 1]}); output_df.to_csv('tsne_coordinates.csv', index=False)
```

## Evaluation signals

- All spectrum identifiers from the input spectral data are present in the output coordinate file with no missing or duplicate entries.
- X and Y coordinates are numeric, finite values (not NaN or infinite) and span a reasonable range consistent with t-SNE output (typically [−100, 100] after typical scaling).
- Spectra with high ms2deepscore similarity are clustered proximal in 2-D space; spectra with low similarity are spatially separated.
- The coordinate file follows the expected schema (spectrum_id, x, y columns or equivalent structured format) and is parseable by the specXplore dashboard importer.
- Reproducibility check: re-running t-SNE with the same random seed and hyperparameters produces identical or near-identical coordinate assignments.

## Limitations

- t-SNE output is stochastic and depends on initialization and random seed; coordinates may vary between runs even with identical input. Users should fix the random seed for reproducibility.
- t-SNE is computationally expensive and may be slow for very large spectral datasets (>10,000 spectra); consider subsampling or alternative methods (UMAP) for large-scale exploration.
- t-SNE distorts global distances and is optimized for local structure; long-range spectral relationships may not be faithfully represented. Use only as an overview tool, not for quantitative distance inference.
- On macOS ARM64 systems, the current ms2deepscore package version may produce unreliable similarity predictions (GitHub issue #199) that propagate into incorrect t-SNE embeddings. Users should verify results on other systems or await a ms2deepscore patch.
- t-SNE requires a full pairwise distance matrix as input; if the similarity matrix is incomplete or sparse, imputation or alternative distance metrics may be needed.

## Evidence

- [intro] specXplore uses a t-SNE embedding approach that takes ms2deepscore-computed mass spectral similarities as input and produces a 2-D overview representation: "specXplore uses a t-SNE embedding approach that takes ms2deepscore-computed mass spectral similarities as input and produces a 2-D overview representation"
- [intro] Apply t-SNE algorithm with ms2deepscore distances as the input distance metric to reduce the high-dimensional spectral similarity space into 2-D coordinates: "Apply t-SNE algorithm with ms2deepscore distances as the input distance metric to reduce the high-dimensional spectral similarity space into 2-D coordinates"
- [intro] Save the resulting 2-D t-SNE coordinates (spectrum identifier and x, y positions) to a structured output file for downstream dashboard rendering: "Save the resulting 2-D t-SNE coordinates (spectrum identifier and x, y positions) to a structured output file for downstream dashboard rendering"
- [readme] It joins a t-SNE embedding that serves as an overview representation of mass spectral similarities based on ms2deepscore: "It joins a t-SNE embedding that serves as an overview representation of mass spectral similarities based on ms2deepscore"
- [readme] users making use of macos arm64 computers should be aware of issue 199 for ms2deepscore ... The current ms2deepscore package version may lead to ms2deepscore similarity predictions that are not in accordance with results on other systems: "The current ms2deepscore package version may lead to ms2deepscore similarity predictions that are not in accordance with results on other systems (windows, ubuntu, macos intel)"
