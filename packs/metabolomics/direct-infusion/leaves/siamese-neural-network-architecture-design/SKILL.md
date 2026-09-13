---
name: siamese-neural-network-architecture-design
description: Use when when you have pairs of mass spectrometry spectra and need to
  predict their molecular structural similarity as a scalar Tanimoto score in the
  range [0, 1].
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ms2deepscore
  - matchms
  - Python
  - PyTorch
  techniques:
  - direct-infusion-MS
  license_tier: open
  provenance_tier: literature
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

# siamese-neural-network-architecture-design

## Summary

Design and implement a Siamese neural network architecture with twin branches and shared weights to predict molecular structural similarities (Tanimoto scores) from paired mass spectrometry spectra. This skill applies deep learning to MS/MS spectral comparison by learning embeddings that capture chemical similarity.

## When to use

When you have pairs of mass spectrometry spectra and need to predict their molecular structural similarity as a scalar Tanimoto score in the range [0, 1]. Use this skill when you want to move beyond traditional spectrum similarity metrics and learn similarity patterns directly from spectral data, particularly when you have access to >100,000 diverse spectra for training or wish to leverage a pre-trained model.

## When NOT to use

- Input spectra are not preprocessed or lack m/z and intensity values; the model requires standardized peak lists.
- You have fewer than ~100,000 diverse training spectra and no pre-trained model available; training from scratch on small datasets risks poor feature learning.
- You need interpretable or rule-based similarity rather than a learned neural score; Siamese outputs are not easily decomposable into human-readable chemical rules.

## Inputs

- Pair of preprocessed mass spectrometry spectra (peak intensities and m/z values)
- Training corpus: >100,000 MS/MS spectra in mgf, msp, mzml, or json format
- Metadata fields: ionization mode, precursor m/z, or other categorical/continuous attributes

## Outputs

- Scalar Tanimoto similarity score per spectrum pair (range [0, 1])
- Spectral embedding vectors (for dimensionality reduction and chemical space visualization)
- Trained Siamese model checkpoint (.pt file)

## How to apply

Construct a Siamese neural network with two identical branches that process each spectrum in a pair through shared weight layers, learning spectral embeddings. The input layer accepts preprocessed mass spectrometry spectral data (peak intensities and m/z values). Build shared feature extraction layers that learn discriminative spectral representations, then implement a similarity computation layer that compares the paired embeddings and outputs a scalar Tanimoto similarity score. For a pre-trained model, load it via ms2deepscore.models.load_model() and wrap it in MS2DeepScore class; for custom training, prepare cleaned spectra in mgf or msp format, configure SettingsMS2Deepscore with metadata fields (e.g., ionization mode, precursor m/z), and invoke train_ms2deepscore_wrapper(). Validate that predictions fall within [0, 1] and that the model accepts spectrum pairs with compatible preprocessing (normalization, peak filtering).

## Related tools

- **ms2deepscore** (Library providing Siamese neural network model, training wrapper, and prediction interface for spectral similarity) — https://github.com/matchms/ms2deepscore
- **matchms** (Spectrum preprocessing, filtering, and data loading for ms2deepscore; provides DEFAULT_FILTERS and Pipeline interface) — https://github.com/matchms/matchms
- **Python** (Runtime environment for training and inference; required version 3.11 or 3.12)
- **PyTorch** (Underlying deep learning framework (implicit dependency of ms2deepscore))

## Examples

```
from ms2deepscore.models import load_model; from ms2deepscore import MS2DeepScore; model = load_model('ms2deepscore_model.pt'); ms2ds = MS2DeepScore(model); similarity_scores = ms2ds(spectrum_pairs); embeddings = ms2ds.get_embedding_array(cleaned_spectra)
```

## Evaluation signals

- Verify model accepts spectrum pairs and produces scalar outputs in range [0, 1]; check with test spectra from example dataset.
- Confirm shared weights: inspect model parameters to ensure twin branches share identical weight tensors before and after forward pass.
- Validate embedding dimensionality: confirm embedding_array output shape matches number of input spectra and embedding size (typically 256–512 dims).
- Cross-ionization predictions: if training with both ionization modes, verify model can score spectra across positive and negative modes without mode mismatch errors.
- Inspect training loss convergence: plot loss curves across epochs to confirm stable descent and no divergence; check validation loss plateau as sign of convergence.

## Limitations

- Model performance depends heavily on training data diversity and size; <100,000 spectra may yield suboptimal embeddings, particularly for rare chemical classes.
- Pre-trained models are optimized for spectra from GNPS, Mona, MassBank, and MSnLib; transfer to highly specialized or non-standard spectral libraries may degrade accuracy.
- Pair sampling strategy significantly affects training quality; inadequate or biased pair sampling can result in poor similarity learning regardless of architecture.
- Spectra must be preprocessed (noise removal, normalization, peak alignment) before input; the model does not handle raw, unfiltered spectra.
- No interpretability: Siamese embeddings are high-dimensional black-box representations; chemical insight requires downstream visualization (e.g., UMAP) and manual annotation.

## Evidence

- [other] MS2DeepScore implements a Siamese neural network architecture designed to take pairs of mass spectrometry spectra as input and output predicted molecular structural similarities expressed as Tanimoto scores.: "MS2DeepScore implements a Siamese neural network architecture designed to take pairs of mass spectrometry spectra as input and output predicted molecular structural similarities expressed as Tanimoto"
- [other] Build the shared feature extraction layers that learn spectral embeddings. Implement the similarity computation layer that outputs Tanimoto similarity scores from paired embeddings.: "Build the shared feature extraction layers that learn spectral embeddings. 4. Implement the similarity computation layer that outputs Tanimoto similarity scores from paired embeddings."
- [other] Validate that the model can accept spectrum pairs and produce scalar similarity scores in the range [0, 1].: "Validate that the model can accept spectrum pairs and produce scalar similarity scores in the range [0, 1]."
- [readme] ms2deepscore provides a Siamese neural network that is trained to predict molecular structural similarities (Tanimoto scores) from pairs of mass spectrometry spectra.: "ms2deepscore provides a Siamese neural network that is trained to predict molecular structural similarities (Tanimoto scores) from pairs of mass spectrometry spectra."
- [readme] The library provides intuitive classes to prepare data, train a Siamese model, and compute similarities between pairs of spectra.: "The library provides intuitive classes to prepare data, train a Siamese model, and compute similarities between pairs of spectra."
- [readme] MS2DeepScore first calculates an embedding (vector) representing each spectrum. This intermediate product can also be used to visualize spectra in chemical space by using a dimensionality reduction technique, like UMAP.: "MS2DeepScore first calculates an embedding (vector) representing each spectrum. This intermediate product can also be used to visualize spectra in chemical space by using a dimensionality reduction"
- [readme] You can train a new model on a dataset of your choice. That, however, should contain a substantial amount of spectra to learn relevant features, say > 100,000 spectra of sufficiently diverse types.: "You can train a new model on a dataset of your choice. That, however, should contain a substantial amount of spectra to learn relevant features, say > 100,000 spectra of sufficiently diverse types."
- [readme] The pair sampling has to be checked and potentially re-optimized for new datasets. Particularly for smaller training sets, the pair sampling can be suboptimal if not checked.: "The pair sampling has to be checked and potentially re-optimized for new datasets. Particularly for smaller training sets, the pair sampling can be suboptimal if not checked."
