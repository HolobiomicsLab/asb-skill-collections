---
name: keras-regularizer-api-integration
description: Use when when extending an existing neural network class (e.g., SiameseModel) that lacks user-configurable regularization, and you need to prevent overfitting on moderate-sized training datasets (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3474
  tools:
  - ms2deepscore
  - GitHub
  - Keras/TensorFlow
  - Python unittest
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1101/2024.03.25.586580v5
  title: MS2DeepScore 2.0
evidence_spans:
- '`ms2deepscore` provides a Siamese neural network that is trained to predict molecular structural similarities'
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# keras-regularizer-api-integration

## Summary

Integrate L1 and L2 regularization parameters into Keras/TensorFlow neural network models by exposing them as constructor arguments and applying them to model layers via the keras.regularizers API. This skill enables practitioners to control overfitting in deep learning models (e.g., Siamese networks for similarity prediction) without modifying layer definitions post-hoc.

## When to use

When extending an existing neural network class (e.g., SiameseModel) that lacks user-configurable regularization, and you need to prevent overfitting on moderate-sized training datasets (e.g., 100,000–500,000 spectra) by allowing L1/L2 penalty strength to be tuned as a hyperparameter during model construction.

## When NOT to use

- The model class already exposes L1/L2 regularization parameters through its public API.
- The training dataset is very large (>1M spectra) and regularization is not a priority for the current use case.
- You need dynamic regularization adjustment during training; this skill is for static per-constructor regularization only.

## Inputs

- SiameseModel class definition (or equivalent neural network model)
- L1 regularization coefficient (float, e.g. 0.0–0.01)
- L2 regularization coefficient (float, e.g. 0.0–0.01)
- Existing unit test suite

## Outputs

- Modified model class with L1/L2 parameters in constructor
- Updated model docstring documenting regularization parameters
- Unit tests validating regularization parameter storage and application
- Test suite execution report confirming no regressions
- Updated CHANGELOG.md referencing the new feature

## How to apply

First, review the target model class to identify where layers are instantiated (typically in __init__ or build methods). Add L1 and L2 parameters to the constructor with sensible defaults (e.g., 0.0 for no regularization). Use the keras.regularizers.L1L2 API (or L1/L2 variants) to wrap the regularizer configuration and pass it to layer definitions (e.g., kernel_regularizer= argument in Dense or Conv layers). Verify integration by writing unit tests that confirm: (a) the constructor accepts L1/L2 arguments without error, (b) parameters are stored as model attributes, and (c) regularization penalties appear in the loss during training. Run the existing test suite (e.g., python setup.py test) to confirm no regressions, then update the model docstring and CHANGELOG to document the new parameters.

## Related tools

- **ms2deepscore** (Source model class (SiameseModel) to be extended with regularization parameters) — https://github.com/matchms/ms2deepscore
- **Keras/TensorFlow** (Provides regularizers.L1L2 API and layer kernel_regularizer argument)
- **Python unittest** (Framework for writing and running unit tests to validate regularization integration)

## Examples

```
from ms2deepscore.models import SiameseModel; model = SiameseModel(l1_reg=0.001, l2_reg=0.01); import subprocess; subprocess.run(['python', 'setup.py', 'test'], check=True)
```

## Evaluation signals

- Constructor accepts L1 and L2 keyword arguments without raising TypeError.
- Parameters are stored as model instance attributes and retrievable via model.__dict__ or property accessors.
- Regularization terms appear in the model's total loss during training (loss increases when L1/L2 > 0.0).
- Existing test suite runs without regressions (python setup.py test exits with status 0).
- Unit tests for regularization parameters pass (e.g., pytest tests/test_siamese_regularization.py).

## Limitations

- Regularization strength (L1/L2 coefficients) must be tuned empirically; no automated hyperparameter search is provided by this skill.
- Only applicable to layers that support kernel_regularizer (Dense, Conv1D/2D/3D); embedding layers or custom layers may require separate handling.
- The skill assumes familiarity with Keras API; integration errors may occur if layer definitions use non-standard regularizer syntax.
- Training dataset must be sufficiently diverse (>100,000 spectra recommended) for regularization benefits to manifest; small datasets may show diminishing returns.

## Evidence

- [other] The ms2deepscore library provides intuitive classes to train a Siamese model, which forms the foundation for implementing configurable regularization parameters.: "The ms2deepscore library provides intuitive classes to train a Siamese model, which forms the foundation for implementing configurable regularization parameters."
- [other] Add L1 and L2 regularization parameters to the SiameseModel constructor with sensible defaults (e.g., 0.0 for no regularization). Integrate the L1/L2 parameters into the model's layer definitions using the appropriate regularizer API (e.g., keras.regularizers.L1L2 or equivalent).: "Add L1 and L2 regularization parameters to the SiameseModel constructor with sensible defaults (e.g., 0.0 for no regularization). Integrate the L1/L2 parameters into the model's layer definitions"
- [other] Write unit tests in Python to verify that: (a) the constructor accepts L1 and L2 arguments without error, (b) the parameters are stored as model attributes, and (c) the regularization is applied to model weights during a forward pass or training step.: "Write unit tests in Python to verify that: (a) the constructor accepts L1 and L2 arguments without error, (b) the parameters are stored as model attributes, and (c) the regularization is applied to"
- [other] Run the existing test suite with `python setup.py test` to confirm no regressions.: "Run the existing test suite with `python setup.py test` to confirm no regressions."
- [readme] You can train a new model on a dataset of your choice. That, however, should contain a substantial amount of spectra to learn relevant features, say > 100,000 spectra of sufficiently diverse types.: "you can train a new model on a dataset of your choice. That, however, should  contain a substantial amount of spectra to learn relevant features, say > 100,000 spectra of sufficiently diverse types."
