---
name: siamese-network-inference
description: Use when you have a collection of cleaned MS/MS spectra (in formats like mzML, mgf, msp, mzxml, or json) and need to predict molecular structural similarities between spectrum pairs without pre-computing RDKit fingerprints.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3680
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3473
  - http://edamontology.org/topic_0092
  tools:
  - MS2DeepScore
  - Python
  - RDKit
  - NumPy
  - ms2deepscore
  - matchms
  - PyTorch
  - CUDA
  - numba
  - SpecEmbedding
  techniques:
  - LC-MS
derived_from:
- doi: 10.1186/s13321-021-00558-4
  title: MS2DeepScore
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
  - build: coll_fiddle_cq
    doi: 10.1038/s41467-025-66060-9
    title: fiddle
  - build: coll_ms2deepscore_cq
    doi: 10.1186/s13321-021-00558-4
    title: MS2DeepScore
  - build: coll_specembedding_cq
    doi: 10.1021/acs.analchem.5c02655
    title: SpecEmbedding
  dedup_kept_from: coll_ms2deepscore_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-021-00558-4
  all_source_dois:
  - 10.1186/s13321-021-00558-4
  - 10.1021/acs.analchem.5c02655
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# siamese-network-inference

## Summary

Load a pre-trained Siamese neural network and use it to generate spectral embeddings and predict structural similarity scores (Tanimoto or Dice) from pairs of MS/MS spectra without requiring molecular fingerprint computation. This skill enables rapid, scalable chemical similarity assessment directly from mass spectrometry data.

## When to use

You have a collection of cleaned MS/MS spectra (in formats like mzML, mgf, msp, mzxml, or json) and need to predict molecular structural similarities between spectrum pairs without pre-computing RDKit fingerprints. Use this when you want fast, end-to-end predictions of Tanimoto scores or when you need spectral embeddings for clustering or visualization of 'chemical space'.

## When NOT to use

- Your spectra have not been cleaned (missing or malformed metadata, unchecked peak intensities) — apply matchms preprocessing first.
- You require interpretable molecular fingerprint information (e.g., which structural features drove the similarity) — this model predicts end-to-end similarity scores without explicit fingerprint output.
- Your spectra are from ionization modes or chemical classes not well-represented in the training data (>500,000 spectra from GNPS, MoNA, MassBank, MSnLib) — model generalization may be degraded.

## Inputs

- MS/MS spectra in MGF, MSP, mzML, mzXML, JSON, or USI format
- Pre-trained Siamese neural network checkpoint (PyTorch .pt file)
- Cleaned spectrum metadata (parent mass, precursor m/z, ionization mode)

## Outputs

- Predicted Tanimoto or Dice similarity scores for spectrum pairs
- 200-dimensional spectral embeddings per spectrum
- Uncertainty estimates (IQR values) for each prediction when Monte-Carlo Dropout applied
- Similarity matrix (numpy array) for all pairwise comparisons

## How to apply

Load the pre-trained MS2DeepScore model from the checkpoint file (e.g., ms2deepscore_model.pt from zenodo). Clean and prepare input spectra using matchms DEFAULT_FILTERS to ensure consistent metadata and peak intensity normalization. For each spectrum pair or spectrum collection, pass the cleaned spectra to the model's embedding function to generate 200-dimensional spectral embeddings. Compute pairwise cosine similarity between embeddings and convert to predicted Tanimoto scores. Optionally apply Monte-Carlo Dropout uncertainty quantification by sampling multiple forward passes through the model with dropout active, then filter predictions by interquartile range (IQR) thresholds to improve accuracy on high-confidence predictions. The model works across both positive and negative ionization modes simultaneously.

## Related tools

- **ms2deepscore** (Pre-trained Siamese model and inference API; loads embeddings and computes similarities from spectrum pairs) — https://github.com/matchms/ms2deepscore
- **matchms** (Spectrum data I/O, cleaning pipeline (DEFAULT_FILTERS), and metadata standardization before inference) — https://github.com/matchms/matchms
- **PyTorch** (Underlying deep learning framework for model loading and forward pass computation)
- **NumPy** (Numerical operations for cosine similarity computation and similarity matrix creation)
- **RDKit** (Optional: reference Tanimoto score computation from Daylight fingerprints for validation or benchmark)

## Examples

```
from ms2deepscore.models import load_model
from matchms.Pipeline import Pipeline, create_workflow
from matchms.filtering.default_pipelines import DEFAULT_FILTERS
from ms2deepscore import MS2DeepScore

model = load_model('ms2deepscore_model.pt')
pipeline = Pipeline(create_workflow(query_filters=DEFAULT_FILTERS, score_computations=[[MS2DeepScore, {'model': model}]]))
report = pipeline.run('pesticides.mgf')
similarity_matrix = pipeline.scores.to_array()
```

## Evaluation signals

- Predicted Tanimoto scores fall within the expected range [0.0, 1.0] with mean and distribution consistent with publication (mean ~0.15 RMSE on unseen compound test sets)
- Pairwise embeddings show meaningful clustering when visualized with UMAP or t-SNE—structurally similar compounds (high Tanimoto) should co-locate
- Root mean squared error on a held-out test set of 3600+ spectra from unseen compounds matches reported ~0.15 RMSE (or ~0.10 with IQR filtering)
- Uncertainty quantification (IQR) correlates with prediction error: high-uncertainty predictions are less accurate than low-IQR predictions
- Model recovers high structural similarity (Tanimoto > 0.7) for isomeric or very similar compounds, and low similarity for structurally distant compounds

## Limitations

- Model was trained on 109,734 MS/MS spectra representing 15,062 unique molecules; performance may degrade on novel chemical classes or rare compound types not in training distribution.
- Spectrum metadata such as parent mass and elemental formula were not used during training; metadata-only filtering cannot be applied by the model.
- Monte-Carlo Dropout uncertainty estimates require multiple forward passes (computational overhead); without dropout, only point predictions are available.
- Cross-ionization-mode predictions (e.g., positive to negative) are possible with MS2DeepScore 2.0+ but the original 2021 model (task_003) was trained primarily on single-ionization datasets.
- Spectra must be cleaned and binned to consistent peak representations; malformed or uncleaned input will produce unreliable embeddings and similarity scores.

## Evidence

- [methods] Load a pre-trained Siamese model and compute embeddings: "Load the pre-trained MS2DeepScore base network and the test set of 3601 binned spectra"
- [methods] Generate embeddings and compute cosine similarity: "compute 200-dimensional spectral embeddings for each spectrum using the trained base network. 3. Calculate cosine similarity between paired embeddings and convert to predicted Tanimoto scores"
- [methods] Apply uncertainty filtering via Monte-Carlo Dropout: "To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles [17]. At inference time, dropout was applied to all but the first layer of the base network"
- [abstract] Expected RMSE performance benchmark: "predict Tanimoto scores for spectra with a root mean squared error of about 0.15"
- [readme] Model supports multiple ionization modes: "The model works for spectra in both positive and negative ionization modes and even predictions across ionization modes can be made by this model"
- [readme] Data cleaning is prerequisite: "Please first ensure cleaning your spectra. We recommend using the cleaning pipeline in matchms"
