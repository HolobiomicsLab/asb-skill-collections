---
name: spectral-overview-representation-generation
description: Use when you have processed LC-MS/MS spectral data (as a .mgf file with feature identifiers) and computed pairwise ms2deepscore similarity scores, and you need to create a 2-D projection suitable for dashboard visualization or high-level pattern discovery without losing similarity structure.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - ms2deepscore
  - specXplore
  - scikit-learn / t-SNE
  - Jupyter notebooks
  techniques:
  - LC-MS
  - NMR
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

# spectral-overview-representation-generation

## Summary

Generate a 2-D overview representation of mass spectral data by applying t-SNE dimensionality reduction to ms2deepscore-computed similarity matrices. This skill enables interactive visual exploration of LC-MS/MS spectral relationships in a condensed, interpretable format.

## When to use

You have processed LC-MS/MS spectral data (as a .mgf file with feature identifiers) and computed pairwise ms2deepscore similarity scores, and you need to create a 2-D projection suitable for dashboard visualization or high-level pattern discovery without losing similarity structure.

## When NOT to use

- Input spectral data is already in a 2-D or lower-dimensional projected form (e.g., previously embedded PCA or UMAP coordinates) — you would be applying redundant dimensionality reduction.
- You lack precomputed ms2deepscore similarity scores; the skill requires a distance or similarity metric as input, not raw spectral peak lists.
- Your workflow operates on non-MS/MS data (e.g., pure LC-UV, NMR, or other modalities) where ms2deepscore is not applicable.

## Inputs

- precomputed ms2deepscore similarity matrix (dense or sparse form)
- spectral metadata including spectrum identifiers and feature_id keys
- specXplore session data object (.mgf-derived intermediate)

## Outputs

- 2-D t-SNE coordinate array (spectrum identifier, x position, y position)
- structured output file suitable for dashboard rendering (JSON or NumPy)

## How to apply

Load the precomputed ms2deepscore similarity matrix and associated spectral metadata into a specXplore session data object. Apply the t-SNE algorithm (from scikit-learn or equivalent) using the ms2deepscore distance metric as the input distance measure to reduce the high-dimensional similarity space into 2-D coordinates. The algorithm preserves local and global structure, placing spectrally similar compounds near one another in the 2-D plane. Save the resulting spectrum identifiers paired with x, y coordinate pairs to a structured output file (typically JSON or NumPy format) for integration into the specXplore dashboard. The choice of t-SNE hyperparameters (e.g., perplexity, learning rate) should balance computational cost with preservation of similarity neighborhood structure.

## Related tools

- **ms2deepscore** (computes deep learning-based similarity scores between mass spectra; output used as distance metric for t-SNE) — https://github.com/matchms/ms2deepscore
- **specXplore** (hosts the t-SNE embedding computation, manages session data object, and integrates 2-D coordinates into interactive dashboard) — https://github.com/kevinmildau/specXplore
- **scikit-learn / t-SNE** (provides the t-SNE algorithm implementation for non-linear dimensionality reduction)
- **Jupyter notebooks** (environment for executing t-SNE computation and managing workflow stages interactively)

## Evaluation signals

- Verify that output coordinate file contains one row per spectrum with three columns (spectrum_id, x, y) and no missing or NaN values.
- Check that 2-D coordinates fall within a bounded range (e.g., typically [−50, 50] or [0, 100] depending on t-SNE initialization); unbounded or extreme values suggest algorithm failure.
- Visually inspect the t-SNE plot in the dashboard: spectra with high ms2deepscore similarity should cluster together; isolated points indicate outliers or dissimilar spectra.
- Confirm that the resulting 2-D representation preserves local neighborhood structure by sampling a few high-similarity pairs from the original matrix and verifying they are proximal in 2-D space.
- Validate that the output file format matches the expected schema for downstream dashboard ingestion (e.g., JSON structure or NumPy serialization format expected by specXplore renderer).

## Limitations

- t-SNE is a stochastic algorithm; multiple runs with the same input may produce different 2-D orientations (but preserve relative distances). Seed the random state for reproducibility.
- t-SNE computational cost scales roughly as O(n²) in the number of spectra; for very large datasets (>10,000 spectra), runtime and memory may become prohibitive; consider subsampling or alternative methods (e.g., UMAP).
- On macOS arm64 systems, ms2deepscore version constraints and model file compatibility issues may cause unreliable similarity predictions that propagate into the t-SNE embedding. Users on affected systems should verify model consistency against reference systems.
- t-SNE does not preserve global distances well; the absolute scale and spacing of distant clusters should not be interpreted as quantitatively meaningful. Only local neighborhood proximity is reliable.
- The skill requires .mgf input files with feature_id metadata keys correctly named; missing or incorrectly named identifiers will cause workflow failure or data loss.

## Evidence

- [other] Apply t-SNE algorithm with ms2deepscore distances as the input distance metric to reduce the high-dimensional spectral similarity space into 2-D coordinates.: "Apply t-SNE algorithm with ms2deepscore distances as the input distance metric to reduce the high-dimensional spectral similarity space into 2-D coordinates."
- [readme] It joins a t-SNE embedding that serves as an overview representation of mass spectral similarities based on ms2deepscore with interactive add-on and overlay representations.: "It joins a t-SNE embedding that serves as an overview representation of mass spectral similarities based on ms2deepscore with interactive add-on and overlay representations"
- [other] Load processed spectral data and precomputed ms2deepscore similarity matrix from the specXplore session data object.: "Load processed spectral data and precomputed ms2deepscore similarity matrix from the specXplore session data object."
- [other] Save the resulting 2-D t-SNE coordinates (spectrum identifier and x, y positions) to a structured output file for downstream dashboard rendering.: "Save the resulting 2-D t-SNE coordinates (spectrum identifier and x, y positions) to a structured output file for downstream dashboard rendering."
- [readme] The current ms2deepscore package version may lead to ms2deepscore similarity predictions that are not in accordance with results on other systems (windows, ubuntu, macos intel).: "The current ms2deepscore package version may lead to ms2deepscore similarity predictions that are not in accordance with results on other systems"
- [readme] specXplore currently requires a .mgf formatted file with MS/MS spectral data. Feature lists should always contain some form of feature identifier, and specXplore expects the feature identifier key to be 'feature_id'.: "specXplore currently requires a .mgf formatted file with MS/MS spectral data. Feature lists should always contain some form of feature identifier, and specXplore expects the feature identifier key to"
