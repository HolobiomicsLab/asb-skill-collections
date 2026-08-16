---
name: mass-spectrometry-spectral-embedding-learning
description: Use when when you have preprocessed MS/MS spectral pairs (peak intensities and m/z values) and need to predict molecular structural similarity scores, or when you want to project spectra into a learned chemical embedding space for visualization (e.g., via UMAP) or downstream similarity searches.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0391
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3474
  tools:
  - ms2deepscore
  - matchms
  - Python
  techniques:
  - LC-MS
derived_from:
- doi: 10.1101/2024.03.25.586580v5
  title: MS2DeepScore 2.0
evidence_spans:
- '`ms2deepscore` provides a Siamese neural network that is trained to predict molecular structural similarities'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2deepscore_2_0_cq
    doi: 10.1101/2024.03.25.586580v5
    title: MS2DeepScore 2.0
  dedup_kept_from: coll_ms2deepscore_2_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.03.25.586580v5
  all_source_dois:
  - 10.1101/2024.03.25.586580v5
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-spectral-embedding-learning

## Summary

Train or apply a Siamese neural network to learn vector embeddings from pairs of mass spectrometry spectra, enabling prediction of molecular structural similarity (Tanimoto scores) and chemical space visualization. This skill bridges raw spectral data to learned feature representations suitable for similarity scoring and dimensionality reduction.

## When to use

When you have preprocessed MS/MS spectral pairs (peak intensities and m/z values) and need to predict molecular structural similarity scores, or when you want to project spectra into a learned chemical embedding space for visualization (e.g., via UMAP) or downstream similarity searches. Apply this skill if your goal is cross-ionization-mode comparisons or if pre-trained models do not generalize to your spectral library.

## When NOT to use

- Input spectra are raw, uncleaned, or lack mandatory metadata (e.g., precursor m/z, ionization mode) — apply spectral cleaning via matchms pipelines first.
- Your goal is cross-spectrum matching within a single ionization mode and a rule-based cosine similarity scorer suffices — this skill adds complexity without benefit.
- Training dataset contains <100,000 spectra and no transfer learning from pre-trained models is attempted — insufficient data for robust deep learning.
- Input is already a precomputed similarity matrix or feature table — the skill targets raw spectral pairs, not derived matrices.

## Inputs

- Preprocessed mass spectrometry spectra (peak intensities, m/z values)
- Spectrum pairs in common formats (MGF, MSP, mzML, mzXML, JSON, USI)
- Metadata annotations (ionization mode, precursor m/z, structural labels for training)
- Pre-trained Siamese model checkpoint file (.pt format) or training dataset (>100,000 spectra)

## Outputs

- Similarity matrix (numpy array of Tanimoto scores in [0, 1] range)
- Embedding vectors (intermediate spectrum representations)
- Trained Siamese model checkpoint and optional embedding evaluator model
- Confidence scores per spectrum (via embedding evaluator)

## How to apply

Load or instantiate a Siamese neural network with twin branches that process each spectrum in a pair through shared weights, outputting scalar Tanimoto similarity scores in the range [0, 1]. Prepare spectral data by cleaning via matchms default filters and extracting peak intensities and m/z values. For prediction, load a pre-trained model (e.g., from Zenodo) and pass spectrum pairs through the MS2DeepScore class; for training on custom data (>100,000 spectra recommended), use SettingsMS2Deepscore to configure hyperparameters, metadata fields (e.g., ionmode, precursor m/z), and pair sampling strategy, then invoke train_ms2deepscore_wrapper. Validate that the model accepts spectrum pairs and outputs similarity scores; optionally extract intermediate embeddings via get_embedding_array for visualization or embedding evaluator confidence scoring.

## Related tools

- **ms2deepscore** (Provides the Siamese neural network implementation, similarity computation layer, and wrapper functions for data preparation, training, and inference) — https://github.com/matchms/ms2deepscore
- **matchms** (Supplies default spectral filtering pipelines, spectrum I/O, and pipeline infrastructure for preprocessing and scoring workflows) — https://github.com/matchms/matchms
- **Python** (Runtime environment for executing training, inference, and embedding extraction code)

## Examples

```
from ms2deepscore.models import load_model
from ms2deepscore import MS2DeepScore
model = load_model('ms2deepscore_model.pt')
ms2ds = MS2DeepScore(model)
similarity_scores = ms2ds.pair(spectrum1, spectrum2)
embeddings = ms2ds.get_embedding_array(cleaned_spectra)
```

## Evaluation signals

- Model accepts pairs of spectra without error and outputs scalar Tanimoto scores constrained to [0, 1].
- Similarity matrix dimensions match (n_spectra, n_spectra) and are symmetric or appropriately asymmetric depending on pair direction.
- Embedding vectors extracted via get_embedding_array have consistent shape (n_spectra, embedding_dim) and are suitable for dimensionality reduction (UMAP produces interpretable clusters).
- On held-out test set, Tanimoto predictions correlate with ground-truth structural similarity (e.g., molecular fingerprint-based similarity) with Pearson r > 0.7 (for pre-trained) or higher for custom-trained models.
- Cross-ionization-mode predictions produce non-trivial similarity scores (not collapsed to a single value) for spectra of the same and different molecules.

## Limitations

- Pre-trained model trained on >500,000 spectra from GNPS, MoNA, MassBank, and MSnLib — generalization to very different spectral libraries (e.g., under-sampled compound classes) not guaranteed.
- Training custom models requires >100,000 spectra; pair sampling quality must be checked and re-optimized per dataset, particularly for smaller training sets.
- Embedding evaluator confidence scores are optional and require separate training; their reliability depends on the diversity and size of the training set.
- Siamese architecture assumes twin branches with shared weights; non-symmetric or hierarchical architectures not supported by the library.
- Model outputs Tanimoto-like scores but does not guarantee true Tanimoto similarity (based on molecular fingerprints); it is a learned proxy trained on structural similarity labels.

## Evidence

- [readme] Siamese neural network that is trained to predict molecular structural similarities (Tanimoto scores) from pairs of mass spectrometry spectra: "Siamese neural network that is trained to predict molecular structural similarities (Tanimoto scores) from pairs of mass spectrometry spectra"
- [readme] intuitive classes to prepare data, train a Siamese model, and compute similarities between pairs of spectra: "intuitive classes to prepare data, train a Siamese model, and compute similarities between pairs of spectra"
- [other] Define the Siamese neural network architecture with twin branches that process each spectrum in a pair identically through shared weights: "Define the Siamese neural network architecture with twin branches that process each spectrum in a pair identically through shared weights"
- [other] Implement the similarity computation layer that outputs Tanimoto similarity scores from paired embeddings: "Implement the similarity computation layer that outputs Tanimoto similarity scores from paired embeddings"
- [other] Validate that the model can accept spectrum pairs and produce scalar similarity scores in the range [0, 1]: "Validate that the model can accept spectrum pairs and produce scalar similarity scores in the range [0, 1]"
- [readme] To calculate chemical similarity scores, MS2DeepScore first calculates an embedding (vector) representing each spectrum. This intermediate product can also be used to visualize spectra in "chemical space" by using a dimensionality reduction technique, like UMAP.: "To calculate chemical similarity scores, MS2DeepScore first calculates an embedding (vector) representing each spectrum. This intermediate product can also be used to visualize spectra in "chemical"
- [readme] Training your own model is only recommended if you have some familiarity with machine learning. You can train a new model on a dataset of your choice. That, however, should contain a substantial amount of spectra to learn relevant features, say > 100,000 spectra: "Training your own model is only recommended if you have some familiarity with machine learning. That, however, should contain a substantial amount of spectra to learn relevant features, say > 100,000"
- [readme] We recommend checking the pair sampling tutorial, since the quality of the pair sampling has to be checked and potentially re-optimized for new datasets. Particularly for smaller training sets, the pair sampling can be suboptimal if not checked.: "the quality of the pair sampling has to be checked and potentially re-optimized for new datasets. Particularly for smaller training sets, the pair sampling can be suboptimal"
- [readme] The model works for spectra in both positive and negative ionization modes and even predictions across ionization modes can be made by this model.: "The model works for spectra in both positive and negative ionization modes and even predictions across ionization modes can be made"
