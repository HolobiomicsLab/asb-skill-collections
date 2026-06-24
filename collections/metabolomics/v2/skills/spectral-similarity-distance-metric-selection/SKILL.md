---
name: spectral-similarity-distance-metric-selection
description: Use when when you have processed LC-MS/MS spectral data in .mgf format
  with feature identifiers and need to compute a pairwise similarity matrix to support
  interactive exploration.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2945
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3047
  tools:
  - ms2deepscore
  - specXplore
  - matchms
  - Jupyter notebooks
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.3c04444
  title: specxplore
evidence_spans:
- t-SNE embedding that serves as an overview representation of mass spectral similarities
  based on ms2deepscore
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-similarity-distance-metric-selection

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Select and apply an appropriate distance metric for computing pairwise mass spectral similarities, which serves as the foundation for downstream dimensionality reduction and interactive visualization in LC-MS/MS data exploration. This skill determines how spectral similarity scores are calculated and influences the geometry of the resulting t-SNE embedding.

## When to use

When you have processed LC-MS/MS spectral data in .mgf format with feature identifiers and need to compute a pairwise similarity matrix to support interactive exploration. Specifically, when preparing data for t-SNE embedding in specXplore or other spectral analysis dashboards where the choice of distance metric directly impacts the resulting 2-D overview representation and clustering patterns.

## When NOT to use

- Your input data is in a format other than .mgf with feature_id metadata; preprocessing and format conversion are required first.
- You need to compare similarity metrics quantitatively across different methods; this skill selects one metric and does not perform comparative benchmarking.
- You are working on a Windows system and require reliable ms2deepscore predictions; current versions have documented platform-specific reliability issues.

## Inputs

- .mgf-formatted mass spectral data file with feature_id metadata
- Processed specXplore session data object containing MS/MS spectra
- Optional: precomputed spectral features or fragmentation annotations

## Outputs

- Pairwise spectral similarity matrix (n_spectra × n_spectra)
- Corresponding distance matrix (1 − similarity) for t-SNE input
- specXplore session data object with embedded similarity scores

## How to apply

Load your processed spectral data (in .mgf format with feature_id metadata) into the specXplore importing pipeline within a Jupyter notebook. Select ms2deepscore as your primary distance metric for computing mass spectral similarities—this metric leverages deep learning to capture spectral relationships beyond simple dot product scoring. Precompute the full pairwise ms2deepscore similarity matrix and save it to the specXplore session data object. Verify that the similarity scores fall within expected ranges (typically 0–1 for normalized metrics) and that no NaN or infinite values are present. Pass the resulting matrix as the distance input to t-SNE dimensionality reduction; the metric choice directly determines the quality and interpretability of the resulting 2-D coordinate space. If using macOS arm64 systems, be aware that the current ms2deepscore package version may produce unreliable similarity predictions (see limitations); consider validation against external benchmark data.

## Related tools

- **ms2deepscore** (Computes deep-learning-based mass spectral similarity scores from fragmentation patterns) — https://github.com/matchms/ms2deepscore
- **specXplore** (Integrates similarity metric as input to t-SNE embedding and interactive dashboard visualization) — https://github.com/kevinmildau/specXplore
- **matchms** (Provides Spectrum module for adding and renaming metadata keys (e.g., feature_id) in .mgf files) — https://matchms.readthedocs.io
- **Jupyter notebooks** (Environment for executing the specXplore importing pipeline and computing similarity matrices)

## Examples

```
import jupyter_notebook; from specXplore.importing_pipeline import create_session_data_object; session_data = create_session_data_object(mgf_filepath='data.mgf', compute_ms2deepscore=True); session_data.save('specXplore_session.pkl')
```

## Evaluation signals

- Similarity matrix shape matches (n_spectra, n_spectra) and contains no NaN or infinite values.
- All similarity scores fall within the expected range for the chosen metric (typically 0–1 for normalized metrics like ms2deepscore).
- The resulting t-SNE embedding (2-D coordinates) clusters spectrally similar compounds spatially close together; verify by inspection of overlay views and network visualizations in the specXplore dashboard.
- No errors or warnings in the Jupyter notebook when loading the session data object and triggering t-SNE visualization.
- Hovering over nodes in the t-SNE panel displays node information and reveals sensible groupings of related chemical compounds or fragment families.

## Limitations

- ms2deepscore on macOS arm64 systems may produce unreliable similarity predictions that are not in accordance with results on other systems (Windows, Ubuntu, macOS Intel); this does not generate errors but makes results unreliable without external validation.
- The specXplore workflow currently requires .mgf-formatted input; other mass spectral formats (e.g., mzML, mzXML) must be converted first (e.g., via MZmine3).
- Feature identifiers in .mgf files must use the exact key 'feature_id' for specXplore to recognize them; manual renaming via matchms or text editors is required for non-standard keys.
- Pre-trained model files for ms2deepscore must be downloaded separately from Zenodo and organized by acquisition mode (positive/negative); the importing pipeline cannot function without the appropriate model files.

## Evidence

- [intro] t-SNE embedding that serves as an overview representation of mass spectral similarities based on ms2deepscore: "It joins a t-SNE embedding that serves as an overview representation of mass spectral similarities based on ms2deepscore"
- [other] Apply t-SNE algorithm with ms2deepscore distances as the input distance metric: "Apply t-SNE algorithm with ms2deepscore distances as the input distance metric to reduce the high-dimensional spectral similarity space into 2-D coordinates."
- [other] Load processed spectral data and precomputed ms2deepscore similarity matrix from the specXplore session data object: "Load processed spectral data and precomputed ms2deepscore similarity matrix from the specXplore session data object."
- [readme] Warning about ms2deepscore reliability on macOS arm64: "users making use of macos arm64 computers should be aware of issue 199 for ms2deepscore https://github.com/matchms/ms2deepscore/issues/199. The current ms2deepscore package version may lead to"
- [readme] Feature identifier requirement in .mgf files: "Feature lists should always contain some form of feature identifier, and specXplore expects the feature identifier key to be "feature_id"."
- [readme] Model files required for ms2deepscore functioning: "To run ms2query, ms2deepscore, and spec2vec, model and library files are required. Pre-trained models are available via ms2query for both [positive](https://zenodo.org/records/10527997) and"
