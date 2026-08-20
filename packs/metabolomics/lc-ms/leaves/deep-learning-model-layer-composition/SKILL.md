---
name: deep-learning-model-layer-composition
description: Use when you have unpaired mass spectrometry spectra and need to predict Tanimoto-based molecular structural similarity scores between spectrum pairs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3634
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3511
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

# deep-learning-model-layer-composition

## Summary

Construct and validate the internal architecture of a Siamese neural network designed to process paired mass spectrometry spectra and predict molecular structural similarity scores. This skill bridges the gap between model specification and functional integration with spectral similarity prediction workflows.

## When to use

You have unpaired mass spectrometry spectra and need to predict Tanimoto-based molecular structural similarity scores between spectrum pairs. Apply this skill when you must understand or reconstruct the internal layer composition of a Siamese architecture that accepts preprocessed spectral data (peak intensities and m/z values) and outputs scalar similarity predictions in the range [0, 1].

## When NOT to use

- Input spectra are already encoded as pre-computed embeddings or feature vectors; use direct similarity metrics instead.
- You need only single-spectrum analysis or per-spectrum properties (use appropriate single-branch architectures or classifiers).
- Spectra are in raw, uncleaned format without peak intensity or m/z normalization; preprocess using matchms DEFAULT_FILTERS first.

## Inputs

- paired mass spectrometry spectra (peak intensities and m/z values)
- preprocessed spectral data compatible with ms2deepscore data preparation interface
- spectrum metadata (optional: ionization mode, precursor m/z for additional input layers)

## Outputs

- Siamese neural network model with twin branches and shared weights
- Tanimoto similarity scores in the range [0, 1] for spectrum pairs
- spectral embeddings (vectors representing each spectrum in chemical space)

## How to apply

Define twin branches in the Siamese architecture that process each spectrum in a pair through identical shared weights, ensuring symmetric feature extraction. Implement an input layer accepting preprocessed mass spectrometry spectral data with peak intensities and m/z values as features. Build shared feature extraction layers that learn spectral embeddings from these inputs. Implement a similarity computation layer that takes paired embeddings and outputs Tanimoto similarity scores. Integrate the model with the ms2deepscore library's training interface and data preparation workflows. Validate the model by confirming it accepts spectrum pairs, produces scalar outputs in [0, 1], and aligns with the ms2deepscore API for both similarity prediction and embedding extraction.

## Related tools

- **ms2deepscore** (provides pre-built Siamese architecture, training interface, model serialization, and similarity computation pipeline for MS/MS spectra) — https://github.com/matchms/ms2deepscore
- **matchms** (provides spectral data preparation, filtering, and pipeline orchestration for preprocessing spectra before layer composition) — https://github.com/matchms/matchms
- **Python** (runtime environment and API for model definition, integration, and validation within the ms2deepscore framework)

## Examples

```
from ms2deepscore.models import load_model
from ms2deepscore import MS2DeepScore
model = load_model("ms2deepscore_model.pt")
ms2ds = MS2DeepScore(model)
ms2ds_embeddings = ms2ds.get_embedding_array(cleaned_spectra)
```

## Evaluation signals

- Model accepts paired spectra and produces two symmetric forward passes through identical weight layers, confirmed via architecture inspection or gradient flow tracing.
- Output layer produces scalar Tanimoto similarity scores for each pair; verify range [0, 1] across a diverse test set of spectrum pairs.
- Similarity computation layer correctly integrates paired embeddings; embeddings from identical spectra should yield similarity near 1.0.
- Model integrates with ms2deepscore's training interface (SettingsMS2Deepscore, training_wrapper_functions) and accepts standard .mgf/.msp spectral formats.
- Embedding extraction produces consistent vector representations; identical spectra yield identical embeddings (deterministic forward pass on fixed weights).

## Limitations

- Model performance depends on sufficient training data (>100,000 spectra of diverse types recommended); smaller datasets may learn suboptimal features.
- Pair sampling quality during training must be validated and re-optimized for new datasets; poor pair sampling can severely degrade learned similarities.
- The architecture is specialized for MS/MS spectra; cross-ionization-mode predictions (positive/negative) require explicit metadata handling via additional input layers.
- Pretrained model weights are available from Zenodo but are trained on GNPS, Mona, MassBank, and MSnLib libraries; predictions may not generalize well to structurally unusual or novel compound classes.

## Evidence

- [other] MS2DeepScore implements a Siamese neural network architecture designed to take pairs of mass spectrometry spectra as input and output predicted molecular structural similarities expressed as Tanimoto scores.: "MS2DeepScore implements a Siamese neural network architecture designed to take pairs of mass spectrometry spectra as input and output predicted molecular structural similarities expressed as Tanimoto"
- [other] Define the Siamese neural network architecture with twin branches that process each spectrum in a pair identically through shared weights.: "Define the Siamese neural network architecture with twin branches that process each spectrum in a pair identically through shared weights"
- [other] Build the shared feature extraction layers that learn spectral embeddings. Implement the similarity computation layer that outputs Tanimoto similarity scores from paired embeddings.: "Build the shared feature extraction layers that learn spectral embeddings. Implement the similarity computation layer that outputs Tanimoto similarity scores from paired embeddings"
- [other] Integrate the model with the ms2deepscore library's training interface to ensure compatibility with data preparation and similarity prediction workflows.: "Integrate the model with the ms2deepscore library's training interface to ensure compatibility with data preparation and similarity prediction workflows"
- [other] Validate that the model can accept spectrum pairs and produce scalar similarity scores in the range [0, 1].: "Validate that the model can accept spectrum pairs and produce scalar similarity scores in the range [0, 1]"
- [readme] ms2deepscore provides a Siamese neural network that is trained to predict molecular structural similarities (Tanimoto scores) from pairs of mass spectrometry spectra.: "ms2deepscore provides a Siamese neural network that is trained to predict molecular structural similarities (Tanimoto scores) from pairs of mass spectrometry spectra"
- [readme] The library provides intuitive classes to prepare data, train a Siamese model, and compute similarities between pairs of spectra.: "The library provides intuitive classes to prepare data, train a Siamese model, and compute similarities between pairs of spectra"
- [readme] Training your own model is only recommended if you have some familiarity with machine learning. You can train a new model on a dataset of your choice. That, however, should contain a substantial amount of spectra to learn relevant features, say > 100,000 spectra of sufficiently diverse types.: "should contain a substantial amount of spectra to learn relevant features, say > 100,000 spectra of sufficiently diverse types"
- [readme] We recommend checking the pair sampling tutorial, since the quality of the pair sampling has to be checked and potentially re-optimized for new datasets.: "the quality of the pair sampling has to be checked and potentially re-optimized for new datasets"
- [readme] The model works for spectra in both positive and negative ionization modes and even predictions across ionization modes can be made by this model.: "The model works for spectra in both positive and negative ionization modes and even predictions across ionization modes can be made by this model"
