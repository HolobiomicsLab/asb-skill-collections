---
name: siamese-network-embedding-generation
description: Use when you have preprocessed MS/MS spectra binned into 10,000 equally-sized m/z bins (10–1000 m/z range) with square-root-transformed intensities, and you need to generate 200-dimensional spectral embeddings for structural similarity prediction, visualization via dimensionality reduction (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - matchms
  - MS2DeepScore
  - Python
  - RDKit
  - scikit-learn
  - TensorFlow/Keras or PyTorch
  techniques:
  - LC-MS
derived_from:
- doi: 10.1186/s13321-021-00558-4
  title: MS2DeepScore
evidence_spans:
- Metadata was cleaned and checked using matchms [18] version 0.8.2, which included cleaning compound names
- MS2DeepScore to predict structural similarity scores for spe
- we used the MS2DeepScore base network (Fig. 1) to compute the 200-dimensional spectral embeddings for all 3601 spectra in the test set
- Our MS2DeepScore Python library offers two types of data generators
- Our MS2DeepScore Python library
- we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2deepscore
    doi: 10.1186/s13321-021-00558-4
    title: MS2DeepScore
  dedup_kept_from: coll_ms2deepscore
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-021-00558-4
  all_source_dois:
  - 10.1186/s13321-021-00558-4
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Siamese Network Embedding Generation

## Summary

Transforms a binned MS/MS spectrum into a fixed-dimensional spectral embedding vector using a trained Siamese neural network base network, enabling downstream similarity prediction and spectral clustering. This skill is essential for converting raw mass spectra into learned representations that capture structural and chemical properties.

## When to use

Apply this skill when you have preprocessed MS/MS spectra binned into 10,000 equally-sized m/z bins (10–1000 m/z range) with square-root-transformed intensities, and you need to generate 200-dimensional spectral embeddings for structural similarity prediction, visualization via dimensionality reduction (e.g., t-SNE, UMAP), or spectral clustering analysis.

## When NOT to use

- Input spectra have not been binned into 10,000 equally-sized m/z bins (preprocessing required first).
- Peak intensities have not undergone square-root transformation (normalization required first).
- You require per-spectrum uncertainty estimates without Monte-Carlo Dropout ensemble inference (use embedding evaluator or uncertainty quantification separately).

## Inputs

- Binned MS/MS spectrum vector (9948-dimensional, m/z range 10–1000 in 10,000 equally-sized bins)
- Square-root-transformed peak intensities
- Trained Siamese base network model weights

## Outputs

- 200-dimensional spectral embedding vector
- Embedding suitable for similarity computation, dimensionality reduction, or clustering

## How to apply

Load a preprocessed binned spectrum vector (9948-dimensional, with peaks in the 10–1000 m/z range binned into 10,000 equally-spaced bins and square-root intensity transformation applied). Pass the vector through the first dense layer (500 nodes) with L1 (10⁻⁶) and L2 (10⁻⁶) regularization. Apply batch normalization and dropout (rate 0.2). Pass through a second dense layer (500 nodes) with batch normalization and dropout (0.2). Finally, pass through the output dense layer (200 nodes) without batch normalization or dropout to produce the 200-dimensional spectral embedding. The embedding encodes structural properties learned during training on 109,734 spectrum pairs with known Tanimoto similarity labels.

## Related tools

- **MS2DeepScore** (Provides the trained Siamese base network and orchestrates embedding generation from spectrum pairs) — https://github.com/matchms/ms2deepscore
- **matchms** (Handles spectrum preprocessing (cleaning, peak filtering, binning, intensity transformation) before embedding generation) — https://github.com/matchms/matchms
- **scikit-learn** (Used for dimensionality reduction (t-SNE) of generated embeddings for visualization)
- **TensorFlow/Keras or PyTorch** (Underlying deep learning framework for base network forward passes and layer operations)

## Examples

```
from ms2deepscore.models import load_model
from ms2deepscore import MS2DeepScore
model = load_model('ms2deepscore_model.pt')
ms2ds = MS2DeepScore(model)
embeddings = ms2ds.get_embedding_array(cleaned_spectra)
```

## Evaluation signals

- Output embedding vector has exactly 200 dimensions (no more, no less).
- Embedding vector contains real-valued numbers within a reasonable range (check for NaN, Inf, or extreme outliers indicative of training instability).
- Embeddings computed for the same spectrum multiple times are identical (deterministic forward pass after dropout is disabled).
- Spectral embeddings of structurally similar compounds (high Tanimoto score) cluster closely in embedding space, verifiable via t-SNE visualization or pairwise cosine/Euclidean distance analysis.
- Embedding computation time scales linearly with batch size and number of spectra, with negligible overhead compared to raw forward pass latency.

## Limitations

- The base network requires exactly 9948-dimensional input (10,000 bins with 52 bins outside the 10–1000 m/z range); spectra binned differently will cause shape mismatch errors.
- Embeddings are learned representations specific to the training dataset (109,734 spectra from GNPS) and may not generalize optimally to spectra from significantly different ionization modes, instrumentation, or compound classes not well-represented in training.
- The 200-dimensional embedding does not explicitly encode uncertainty; uncertainty quantification requires separate Monte-Carlo Dropout inference with N=10 forward passes and IQR-based filtering.
- Square-root intensity transformation is mandatory; spectra with untransformed or differently transformed intensities will produce invalid embeddings.
- No dimension reduction, feature selection, or interpretability analysis is performed on the 200 dimensions; individual dimensions do not correspond to interpretable chemical properties.

## Evidence

- [other] The base network accepts a binned spectrum (peaks binned into 10,000 equally-sized m/z bins from 10 to 1000) as input and produces a 200-dimensional spectral embedding vector through dense neural network layers.: "The base network accepts a binned spectrum (peaks binned into 10,000 equally-sized m/z bins from 10 to 1000) as input and produces a 200-dimensional spectral embedding vector"
- [other] Load a binned MS/MS spectrum vector (9948-dimensional, with peaks binned into 10–1000 m/z range at 10,000 equally-spaced bins, square-root-transformed intensities). Pass the input vector through the first dense layer (500 nodes) with L1 (10⁻⁶) and L2 (10⁻⁶) regularization applied. Apply batch normalization after the first dense layer. Apply dropout with rate 0.2 to regularize the layer. Pass through the second dense layer (500 nodes) followed by batch normalization and dropout (0.2). Pass through the final dense layer (200 nodes) to produce the spectral embedding without batch normalization or dropout.: "Load a binned MS/MS spectrum vector (9948-dimensional, with peaks binned into 10–1000 m/z range at 10,000 equally-spaced bins, square-root-transformed intensities). Pass the input vector through the"
- [methods] Spectrum peaks were binned in 10,000 equally-sized bins ranging from 10 to 1000 m/z: "Spectrum peaks were binned in 10,000 equally-sized bins ranging from 10 to 1000 m/z"
- [methods] Peak intensities were square root transformed to avoid a too strong focus on the highest intensity peaks only: "Peak intensities were square root transformed to avoid a too strong focus on the highest intensity peaks only"
- [methods] we used the MS2DeepScore base network (Fig. 1) to compute the 200-dimensional spectral embeddings for all 3601 spectra in the test set: "we used the MS2DeepScore base network (Fig. 1) to compute the 200-dimensional spectral embeddings for all 3601 spectra in the test set"
- [readme] To calculate chemical similarity scores, MS2DeepScore first calculates an embedding (vector) representing each spectrum. This intermediate product can also be used to visualize spectra in 'chemical space' by using a dimensionality reduction technique, like UMAP.: "To calculate chemical similarity scores, MS2DeepScore first calculates an embedding (vector) representing each spectrum. This intermediate product can also be used to visualize spectra in 'chemical"
