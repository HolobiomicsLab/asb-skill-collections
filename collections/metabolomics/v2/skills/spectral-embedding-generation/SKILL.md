---
name: spectral-embedding-generation
description: Use when you have a collection of pre-processed MS/MS spectra (binned, intensity-normalized) and a trained MS2DeepScore base network, and you need to compute structural similarity scores between spectrum pairs or visualize spectra in chemical space via dimensionality reduction (e.g., UMAP).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MS2DeepScore
  - Python
  - RDKit
  - NumPy
  - matchms
  - PyTorch
  - scikit-learn
  - Spec2Mol
  - CUDA
  - numba
  - read_raw_spectra
  - Tokenizer
  - load_tanimoto_supcon_aug_model
  - ModelTester
  - embedding function
  - CUDA 12.4
derived_from:
- doi: 10.1186/s13321-021-00558-4
  title: MS2DeepScore
- doi: 10.1038/s42004-023-00932-3
  title: ''
- doi: 10.1021/acs.analchem.5c02655
  title: ''
evidence_spans:
- Our MS2DeepScore Python library offers two types of data generators
- To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles
- Our MS2DeepScore Python library offers two types of data generators, one which iterates over all unique InChIKeys (DataGeneratorAllInchikeys) and one which iterates over all spectra and was used for
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities.
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities
- mean squared error (MSE) loss
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2deepscore_cq
    doi: 10.1186/s13321-021-00558-4
    title: MS2DeepScore
  - build: coll_spec2mol_cq
    doi: 10.1038/s42004-023-00932-3
    title: Spec2Mol
  - build: coll_specembedding_cq
    doi: 10.1021/acs.analchem.5c02655
    title: SpecEmbedding
  dedup_kept_from: coll_ms2deepscore_cq
schema_version: 0.2.0
---

# spectral-embedding-generation

## Summary

Generate low-dimensional vector embeddings (200-dimensional spectral embeddings) from pairs of binned MS/MS spectra using a trained Siamese neural network base, enabling downstream similarity prediction and spectral clustering without explicit molecular fingerprint computation.

## When to use

You have a collection of pre-processed MS/MS spectra (binned, intensity-normalized) and a trained MS2DeepScore base network, and you need to compute structural similarity scores between spectrum pairs or visualize spectra in chemical space via dimensionality reduction (e.g., UMAP). Embedding generation is the mandatory intermediate step before predicting Tanimoto scores or clustering spectra.

## When NOT to use

- Input spectra are not binned or have not been normalized (square-root transformed and intensity-filtered); pre-processing is required before embedding generation.
- You need to predict cross-ionization-mode similarities with the original 2021 MS2DeepScore model; the base model was trained on positive ionization only; later versions (2.0+) support both modes.
- You already have pre-computed molecular fingerprints and just need direct structural similarity scores; MS2DeepScore embedding generation adds latency and is unnecessary in this case.

## Inputs

- Pre-trained MS2DeepScore Siamese base network (PyTorch .pt model file)
- MS/MS spectra collection (binned, typically 52 bins per spectrum after filtering unused bins from training)
- Spectrum pairs (optional; if computing pairwise similarities)

## Outputs

- 200-dimensional spectral embedding vectors (one per spectrum)
- Predicted Tanimoto scores (if spectrum pairs provided)
- Embedding uncertainty estimates (if Monte-Carlo Dropout enabled at inference)
- Dimensionality-reduced coordinates (if UMAP or t-SNE applied downstream)

## How to apply

Load the pre-trained MS2DeepScore base network and the spectrum dataset (binned to 52 bins after filtering unused bins from training data). For each spectrum, pass it through the trained base network to compute a 200-dimensional embedding vector. If predicting similarity between pairs, compute cosine similarity between paired embeddings; convert cosine scores to predicted Tanimoto scores via a calibrated transformation (the paper uses this mapping for all test pairs). The embedding vectors themselves can be directly used for spectral clustering or visualization without further processing. Key decision: whether to apply uncertainty filtering (Monte-Carlo Dropout) at inference time; the paper shows that stricter uncertainty restrictions (higher interquartile range thresholds) improve accuracy (RMSE down to ~0.10) but reduce the number of usable predictions.

## Related tools

- **MS2DeepScore** (Pre-trained Siamese neural network base that computes spectral embeddings from binned MS/MS spectra) — https://github.com/matchms/ms2deepscore
- **matchms** (Spectrum metadata cleaning, binning, and data curation prior to embedding generation) — https://github.com/matchms/matchms
- **RDKit** (Computes reference Tanimoto scores from Daylight fingerprints for validation and training; used to generate structural similarity labels)
- **PyTorch** (Neural network inference engine for computing embeddings from spectrum pairs)
- **scikit-learn** (Dimensionality reduction (t-SNE) for visualization of embedding space)

## Examples

```
from ms2deepscore.models import load_model; from ms2deepscore import MS2DeepScore; model = load_model('ms2deepscore_model.pt'); ms2ds = MS2DeepScore(model); embeddings = ms2ds.get_embedding_array(cleaned_spectra)
```

## Evaluation signals

- Each spectrum produces exactly one 200-dimensional embedding vector with no NaN or Inf values.
- Cosine similarity between paired embeddings falls in the range [−1, 1]; after conversion to Tanimoto scores, predicted scores fall in [0, 1].
- When compared against reference Tanimoto scores (from RDKit Daylight fingerprints), root mean squared error (RMSE) should be approximately 0.15 without uncertainty filtering, or ≤0.10 with stricter interquartile range (IQR) thresholds applied.
- Embeddings from spectra of the same compound or very similar compounds cluster together in 2D UMAP/t-SNE space; embeddings from structurally dissimilar compounds are well-separated.
- When Monte-Carlo Dropout uncertainty is enabled, predicted Tanimoto scores with lower interquartile range values correlate with lower prediction error; filtering by IQR threshold should monotonically improve RMSE as threshold decreases.

## Limitations

- The base network was trained exclusively on spectra in positive ionization mode; predictions on negative ionization spectra or cross-ionization comparisons are not validated in the original 2021 model (addressed in MS2DeepScore 2.0+).
- Embedding quality depends critically on spectrum preprocessing: peaks must be binned into 10,000 equally-sized bins (10–1000 m/z range), intensity-normalized via square-root transformation, filtered to remove peaks <0.1% of maximum intensity, and capped at 1000 highest-intensity peaks. Non-standard preprocessing will degrade embeddings.
- No spectrum metadata (parent mass, elemental formula, retention time) is incorporated into embeddings; structural similarity predictions are computed from spectral peaks alone.
- Computational cost scales with the number of unique spectrum pairs: generating embeddings for 3601 spectra and computing all 6.5M pairwise similarities is feasible but computationally intensive; no explicit runtime benchmarks are provided.
- Monte-Carlo Dropout uncertainty estimates require multiple forward passes at inference time; stricter uncertainty filtering (lower IQR thresholds) reduces the proportion of spectrum pairs with usable predictions.

## Evidence

- [other] Generate all possible spectrum pairs from the test set (n=6,485,401 unique pairs) and compute 200-dimensional spectral embeddings for each spectrum using the trained base network.: "compute 200-dimensional spectral embeddings for each spectrum using the trained base network"
- [other] Calculate cosine similarity between paired embeddings and convert to predicted Tanimoto scores (no uncertainty filtering applied).: "Calculate cosine similarity between paired embeddings and convert to predicted Tanimoto scores"
- [intro] MS2DeepScore can create mass spectral embeddings that can be used for additional spectral clustering: "can create mass spectral embeddings that can be used for additional spectral clustering"
- [methods] Spectrum peaks were binned in 10,000 equally-sized bins ranging from 10 to 1000 m/z: "Spectrum peaks were binned in 10,000 equally-sized bins ranging from 10 to 1000 m/z"
- [methods] Peak intensities were square root transformed to avoid a too strong focus on the highest intensity peaks only: "Peak intensities were square root transformed to avoid a too strong focus on the highest intensity peaks only"
- [methods] To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles. At inference time, dropout was applied to all but the first layer of the base network: "To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles. At inference time, dropout was applied to all but the first layer of the base network"
- [results] filtered out scores, according to increasingly stringent interquartile range (IQR) thresholds: "filtered out scores, according to increasingly stringent interquartile range (IQR) thresholds"
- [readme] To calculate chemical similarity scores, MS2DeepScore first calculates an embedding (vector) representing each spectrum. This intermediate product can also be used to visualize spectra in 'chemical space' by using a dimensionality reduction technique, like UMAP.: "To calculate chemical similarity scores, MS2DeepScore first calculates an embedding (vector) representing each spectrum"
- [readme] cleaned_spectra = pipeline.spectra_queries; ms2ds_model = MS2DeepScore(model); ms2ds_embeddings = ms2ds_model.get_embedding_array(cleaned_spectra): "ms2ds_embeddings = ms2ds_model.get_embedding_array(cleaned_spectra)"
