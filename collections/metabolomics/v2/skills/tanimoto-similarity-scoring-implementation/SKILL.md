---
name: tanimoto-similarity-scoring-implementation
description: Use when when you have paired mass spectrometry spectra (e.g., from GNPS,
  MoNA, MassBank, or MSnLib) and need to predict continuous structural similarity
  scores (0–1 range) between them, especially when traditional spectral-distance metrics
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0570
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - ms2deepscore
  - matchms
  - Python
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1101/2024.03.25.586580v5
  title: MS2DeepScore 2.0
evidence_spans:
- '`ms2deepscore` provides a Siamese neural network that is trained to predict molecular
  structural similarities'
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

# tanimoto-similarity-scoring-implementation

## Summary

Implement a Siamese neural network architecture that predicts molecular structural similarities as Tanimoto scores from pairs of mass spectrometry spectra. This skill enables deep-learning-based spectral comparison by training twin-branch networks with shared weights to embed and compare MS/MS data.

## When to use

When you have paired mass spectrometry spectra (e.g., from GNPS, MoNA, MassBank, or MSnLib) and need to predict continuous structural similarity scores (0–1 range) between them, especially when traditional spectral-distance metrics (e.g., cosine) are insufficient or when you want to leverage large reference libraries (>100,000 spectra) to learn generalizable molecular feature representations across ionization modes.

## When NOT to use

- Input spectra are not cleaned and normalized; ms2deepscore requires preprocessing via the matchms cleaning pipeline first.
- Training dataset contains <100,000 spectra; pair sampling quality will be suboptimal and model will not learn generalizable molecular features.
- You need exact structural identity (binary classification) rather than continuous similarity; Tanimoto scores are graded similarities, not binary decisions.

## Inputs

- Mass spectrometry spectral pairs (preprocessed m/z and intensity arrays)
- Spectrum metadata (precursor m/z, ionization mode, molecular fingerprints for ground truth similarity labels)
- Training dataset in common formats (mgf, msp, mzml, mzxml, json, usi) containing >100,000 spectra of diverse chemical types

## Outputs

- Trained Siamese neural network model file (.pt format)
- Tanimoto similarity scores in range [0, 1] for spectrum pairs
- Spectral embeddings (vectors representing chemical space)
- Per-spectrum embedding evaluator predictions (optional, confidence estimates)

## How to apply

Define a Siamese neural network with two identical branches that process each spectrum in a pair through shared weight layers, converting preprocessed peak intensities and m/z values into learned spectral embeddings. Pass paired embeddings through a similarity computation layer to produce scalar Tanimoto scores in the range [0, 1]. Train the model on spectrum pairs with known structural similarity labels (e.g., Tanimoto scores computed from molecular fingerprints) using the ms2deepscore library's training wrapper, which handles pair sampling and data augmentation. Validate by confirming that the model accepts spectrum pairs and outputs similarity scores within [0, 1], and optionally train an embedding evaluator to assess per-spectrum prediction confidence.

## Related tools

- **ms2deepscore** (Provides Siamese network architecture, training wrapper functions, embedding computation, and model inference for predicting Tanimoto scores from MS/MS spectrum pairs) — https://github.com/matchms/ms2deepscore
- **matchms** (Supplies spectrum filtering pipeline (DEFAULT_FILTERS), data loading, and spectral preprocessing required before training ms2deepscore models) — https://github.com/matchms/matchms
- **Python** (Execution environment for model training, data preparation, and similarity computation via SettingsMS2Deepscore and train_ms2deepscore_wrapper)

## Examples

```
from ms2deepscore.SettingsMS2Deepscore import SettingsMS2Deepscore, SettingsEmbeddingEvaluator
from ms2deepscore.wrapper_functions.training_wrapper_functions import train_ms2deepscore_wrapper

settings = SettingsMS2Deepscore(spectrum_file_path="./combined_libraries.mgf", additional_metadata=[("CategoricalToBinary", {"metadata_field": "ionmode"}), ("StandardScaler", {"metadata_field": "precursor_mz"})], ionisation_mode="both")
train_ms2deepscore_wrapper(settings, SettingsEmbeddingEvaluator())
```

## Evaluation signals

- Model accepts spectrum pairs and outputs scalar similarity scores in range [0, 1] with no NaN or out-of-range values.
- Trained model checkpoint (.pt file) can be reloaded via load_model() and produces consistent predictions on the same spectrum pairs.
- Cross-ionization mode predictions are produced correctly (positive/negative spectrum pairs scored without error).
- Pair sampling optimization check: examined via pair_sampling_tutorial to verify training pairs are sufficiently diverse and balanced, especially for datasets <100,000 spectra.
- Embedding evaluator confidence predictions correlate positively with model's Tanimoto prediction accuracy on held-out validation spectra.

## Limitations

- Training requires >100,000 spectra of sufficiently diverse chemical types; smaller datasets will produce suboptimal pair sampling and generalization.
- Model is trained on specific reference libraries (GNPS, MoNA, MassBank, MSnLib); out-of-distribution spectra (rare compound classes, unusual fragmentation) may have degraded performance.
- Pair sampling quality must be manually checked and re-optimized for new datasets; default settings are not guaranteed to be optimal for all chemical domains.
- Cross-ionization mode predictions are supported by the default model but not independently validated for all compound classes.

## Evidence

- [other] MS2DeepScore implements a Siamese neural network architecture designed to take pairs of mass spectrometry spectra as input and output predicted molecular structural similarities expressed as Tanimoto scores.: "Siamese neural network that is trained to predict molecular structural similarities (Tanimoto scores) from pairs of mass spectrometry spectra"
- [other] Build twin branches with shared weights that learn spectral embeddings from preprocessed peak intensities and m/z values, then compute similarity from paired embeddings.: "twin branches that process each spectrum in a pair identically through shared weights"
- [other] Integration with ms2deepscore library's training interface ensures compatibility with data preparation and similarity prediction workflows.: "Integrate the model with the ms2deepscore library's training interface to ensure compatibility with data preparation and similarity prediction workflows"
- [readme] Training dataset recommendations emphasize size and diversity requirements.: "should contain a substantial amount of spectra to learn relevant features, say > 100,000 spectra of sufficiently diverse types"
- [readme] Pair sampling quality must be verified for new datasets, especially smaller ones.: "the quality of the pair sampling has to be checked and potentially re-optimized for new datasets. Particularly for smaller training sets, the pair sampling can be suboptimal if not checked"
- [readme] The model supports both positive and negative ionization modes and cross-mode predictions.: "model works for spectra in both positive and negative ionization modes and even predictions across ionization modes can be made by this model"
