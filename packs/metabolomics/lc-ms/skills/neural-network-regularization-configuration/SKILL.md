---
name: neural-network-regularization-configuration
description: Use when implementing or modifying a Siamese model (such as SiameseModel in ms2deepscore) if you need to make regularization hyperparameters user-configurable rather than hard-coded, or when training on spectral datasets where overfitting risk is high due to limited training examples or high model.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - ms2deepscore
  - GitHub
  - keras.regularizers
  - Python unittest or pytest
  techniques:
  - LC-MS
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

# neural-network-regularization-configuration

## Summary

Extend a Siamese neural network model to accept user-configurable L1 and L2 regularization parameters and apply them during training to prevent overfitting. This skill is essential when training models on limited or specialized spectral datasets where weight decay regularization can improve generalization.

## When to use

Apply this skill when implementing or modifying a Siamese model (such as SiameseModel in ms2deepscore) if you need to make regularization hyperparameters user-configurable rather than hard-coded, or when training on spectral datasets where overfitting risk is high due to limited training examples or high model complexity.

## When NOT to use

- When training on very large, diverse spectral datasets where overfitting is not a concern and model capacity is the limiting factor.
- When the framework or model architecture does not support layer-level regularizer APIs (e.g., non-standard or legacy architectures without keras/PyTorch regularizer support).
- When regularization is already hard-coded into the model and the goal is performance tuning rather than exposing hyperparameters to users.

## Inputs

- SiameseModel class definition (Python source code)
- L1 regularization strength parameter (float, typically 0.0–0.01)
- L2 regularization strength parameter (float, typically 0.0–0.01)
- Training spectra pairs (mass spectrometry spectral data)
- Existing test suite

## Outputs

- Extended SiameseModel class with L1/L2 parameters in constructor
- Model instance with regularization parameters stored as attributes
- Trained model weights with applied L1/L2 regularization loss
- Unit test coverage for regularization parameter acceptance and application
- Updated docstring and CHANGELOG.md entry

## How to apply

First, review the SiameseModel class definition to identify where regularization parameters are currently handled and which layers accept regularizer objects. Add L1 and L2 regularization parameters to the model constructor with sensible defaults (typically 0.0 for no regularization). Integrate these parameters into the model's layer definitions using the appropriate regularizer API (e.g., keras.regularizers.L1L2 or equivalent framework-specific API). Write unit tests to verify that: (a) the constructor accepts L1 and L2 arguments without error, (b) the parameters are stored as model attributes, and (c) regularization loss terms are computed during a forward pass or training step. Run the existing test suite with `python setup.py test` to confirm no regressions, then document the new parameters in the model docstring and update CHANGELOG.md.

## Related tools

- **ms2deepscore** (Source Siamese model class (SiameseModel) to be extended with configurable L1/L2 regularization) — https://github.com/matchms/ms2deepscore
- **keras.regularizers** (Provides L1L2 regularizer API for applying regularization to model layers)
- **Python unittest or pytest** (Framework for writing and running unit tests to verify regularization parameter acceptance and application)
- **GitHub** (Repository hosting, issue tracking, and pull request workflow for announcing and managing regularization feature implementation) — https://github.com/matchms/ms2deepscore

## Examples

```
from ms2deepscore.models import SiameseModel; model = SiameseModel(l1_reg=0.001, l2_reg=0.01); model.train(spectra_pairs, labels, epochs=50)
```

## Evaluation signals

- Constructor successfully accepts L1 and L2 float arguments without raising TypeError or ValueError.
- Parameters are stored as model instance attributes (e.g., `model.l1_reg`, `model.l2_reg`) and are retrievable after instantiation.
- During training, regularization loss terms are added to the total loss; inspect loss logs or model.losses to confirm L1/L2 contributions are non-zero when parameters are non-zero.
- Existing test suite passes with `python setup.py test`; no regressions in prior model behavior.
- Model docstring and CHANGELOG.md clearly document the new L1/L2 parameters, defaults, and usage examples.

## Limitations

- Regularization effectiveness depends on dataset size and diversity; on very large or well-separated spectral datasets, L1/L2 penalties may have negligible effect on model performance.
- Excessively strong regularization (L1 or L2 > 0.1) can cause underfitting and degrade model accuracy on the training task.
- Regularization does not address other sources of overfitting such as insufficient training data or mismatched train/validation splits.
- Framework-specific API (e.g., keras vs. PyTorch) will differ; the implementation must match the underlying deep learning framework used by ms2deepscore.

## Evidence

- [methods] SiameseModel class accepts user-configurable L1 and L2 regularization: "Add L1 and L2 regularization parameters to the SiameseModel constructor with sensible defaults (e.g., 0.0 for no regularization). Integrate the L1/L2 parameters into the model's layer definitions"
- [methods] Regularization is applied during training via layer definitions: "the regularization is applied to model weights during a forward pass or training step"
- [methods] Testing strategy for verifying regularization parameters: "Write unit tests in Python to verify that: (a) the constructor accepts L1 and L2 arguments without error, (b) the parameters are stored as model attributes, and (c) the regularization is applied to"
- [methods] Regression testing and documentation requirements: "Run the existing test suite with `python setup.py test` to confirm no regressions. Document the new parameters in the model docstring and update CHANGELOG.md"
- [readme] Siamese model architecture for spectral similarity prediction: "ms2deepscore provides a Siamese neural network that is trained to predict molecular structural similarities (Tanimoto scores) from pairs of mass spectrometry spectra."
