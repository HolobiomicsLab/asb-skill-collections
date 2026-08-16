---
name: siamese-network-architecture-modification
description: Use when when you need to reduce overfitting in a Siamese neural network
  trained on mass spectrometry spectral pairs by adding weight regularization, or
  when users require flexible control over L1 and L2 penalty coefficients rather than
  hard-coded defaults.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - ms2deepscore
  - GitHub
  - Python
  - keras.regularizers
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1101/2024.03.25.586580v5
  title: MS2DeepScore 2.0
evidence_spans:
- '`ms2deepscore` provides a Siamese neural network that is trained to predict molecular
  structural similarities'
- use the search functionality [here](https://github.com/matchms/ms2deepscore/issues)
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

# siamese-network-architecture-modification

## Summary

Extend a Siamese neural network model to accept user-configurable L1 and L2 regularization parameters and integrate them into layer definitions to reduce overfitting during training. This skill applies regularization constraints to model weights in ms2deepscore's SiameseModel class used for predicting molecular structural similarities from mass spectrometry spectra pairs.

## When to use

When you need to reduce overfitting in a Siamese neural network trained on mass spectrometry spectral pairs by adding weight regularization, or when users require flexible control over L1 and L2 penalty coefficients rather than hard-coded defaults. Apply this skill during model architecture definition before training begins, particularly when the training dataset is limited or when empirical validation shows the model is memorizing rather than generalizing.

## When NOT to use

- When the model is already demonstrating underfitting (high bias, poor training accuracy); regularization will worsen performance in this regime.
- When you lack sufficient training data (< 10,000 spectra) and need to use pre-trained weights without modification; adding regularization to frozen layers is redundant.
- When model architecture has already been validated and is performing well on held-out test data; unnecessary modification introduces risk of regression.

## Inputs

- SiameseModel class definition (Python source code)
- L1 regularization coefficient (float, default 0.0)
- L2 regularization coefficient (float, default 0.0)
- Pairs of mass spectrometry spectra with known structural similarity labels (training data)

## Outputs

- Extended SiameseModel class with L1/L2 regularization parameters
- Modified layer definitions integrating regularizers into weight constraints
- Unit test suite validating parameter acceptance and regularization application
- Updated docstring and CHANGELOG.md entries

## How to apply

Identify the SiameseModel class constructor in ms2deepscore and add L1 and L2 regularization parameters with sensible defaults (e.g., 0.0 for no regularization). Integrate these parameters into the model's layer definitions using the keras.regularizers.L1L2 API or equivalent framework-specific regularizer. Store the L1/L2 coefficients as model attributes for inspection and documentation. Write unit tests to verify that: (a) the constructor accepts L1 and L2 arguments without error, (b) parameters are stored as attributes, and (c) regularization is applied to model weights during a forward pass or training step. Run the existing test suite with `python setup.py test` to confirm no regressions. Document the new parameters in the model docstring and update CHANGELOG.md to reference the corresponding issue.

## Related tools

- **ms2deepscore** (Framework containing SiameseModel class to be extended with L1/L2 regularization parameters and layer integration logic) — https://github.com/matchms/ms2deepscore
- **Python** (Implementation language for modifying SiameseModel, writing unit tests, and running test suite with `python setup.py test`)
- **keras.regularizers** (API module providing L1L2 regularizer objects for integration into model layer definitions)
- **GitHub** (Version control and issue tracking for announcing plan, reaching consensus, and referencing issue #67 in CHANGELOG.md) — https://github.com/matchms/ms2deepscore

## Examples

```
from ms2deepscore.models import SiameseModel
model = SiameseModel(l1=0.01, l2=0.001)
model.fit(train_spectra_pairs, train_labels, epochs=10)
print(f'L1 coefficient: {model.l1_coefficient}, L2 coefficient: {model.l2_coefficient}')
```

## Evaluation signals

- Constructor accepts L1 and L2 arguments without raising TypeError or ValueError; test with `SiameseModel(l1=0.01, l2=0.001)`.
- Model attributes `self.l1_coefficient` and `self.l2_coefficient` are set and retrievable after instantiation.
- Model weights exhibit reduced magnitude during training compared to identical architecture without regularization, indicating regularization penalty is applied.
- All existing tests in `python setup.py test` pass without regression; no breaking changes to public API.
- Docstring and CHANGELOG.md contain clear parameter descriptions, default values, and reference to issue #67; documentation is discoverable via `help(SiameseModel)`.

## Limitations

- Regularization effectiveness depends on the choice of L1/L2 coefficient values; poor hyperparameter selection may worsen generalization instead of improving it.
- Integration with keras.regularizers API is framework-specific; migration to other deep learning frameworks (PyTorch, TensorFlow) may require rewrites.
- Regularization only constrains weights during training; it does not address data imbalance, poor feature engineering, or insufficient spectral diversity in the training set.
- The ms2deepscore library is trained on >500,000 spectra from GNPS, MoNA, MassBank, and MSnLib; regularization tuning on smaller datasets may not generalize to this production model.

## Evidence

- [other] Does the SiameseModel class accept user-configurable L1 and L2 regularization parameters and apply them during training?: "Does the SiameseModel class accept user-configurable L1 and L2 regularization parameters and apply them during training?"
- [other] Add L1 and L2 regularization parameters to the SiameseModel constructor with sensible defaults (e.g., 0.0 for no regularization). Integrate the L1/L2 parameters into the model's layer definitions using the appropriate regularizer API (e.g., keras.regularizers.L1L2 or equivalent).: "Add L1 and L2 regularization parameters to the SiameseModel constructor with sensible defaults (e.g., 0.0 for no regularization). Integrate the L1/L2 parameters into the model's layer definitions"
- [other] Write unit tests in Python to verify that: (a) the constructor accepts L1 and L2 arguments without error, (b) the parameters are stored as model attributes, and (c) the regularization is applied to model weights during a forward pass or training step.: "Write unit tests in Python to verify that: (a) the constructor accepts L1 and L2 arguments without error, (b) the parameters are stored as model attributes, and (c) the regularization is applied to"
- [other] Run the existing test suite with `python setup.py test` to confirm no regressions.: "Run the existing test suite with `python setup.py test` to confirm no regressions."
- [readme] ms2deepscore provides a Siamese neural network that is trained to predict molecular structural similarities (Tanimoto scores) from pairs of mass spectrometry spectra.: "ms2deepscore provides a Siamese neural network that is trained to predict molecular structural similarities (Tanimoto scores) from pairs of mass spectrometry spectra."
- [readme] The library provides intuitive classes to prepare data, train a Siamese model, and compute similarities between pairs of spectra.: "The library provides intuitive classes to prepare data, train a Siamese model, and compute similarities between pairs of spectra."
