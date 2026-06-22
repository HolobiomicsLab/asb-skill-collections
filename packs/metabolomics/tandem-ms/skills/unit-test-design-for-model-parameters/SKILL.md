---
name: unit-test-design-for-model-parameters
description: Use when you have extended a neural network model class (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3474
  tools:
  - ms2deepscore
  - GitHub
  - Python
  - keras.regularizers
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

# unit-test-design-for-model-parameters

## Summary

Design and implement unit tests to verify that newly added model parameters (e.g., L1/L2 regularization in neural networks) are correctly accepted, stored, and applied during training. This skill ensures parameter functionality is validated before integration into a shared codebase.

## When to use

You have extended a neural network model class (e.g., SiameseModel) with new hyperparameter arguments and need to verify that the parameters are accepted by the constructor, stored as model attributes, and actually applied to the model's layers or loss computation during forward passes or training steps.

## When NOT to use

- The parameter is purely cosmetic or decorative and does not affect model computation or training behavior.
- The model class is read-only or is a frozen/released artifact that does not accept modifications.
- You are only adding documentation without changing the actual model code — testing may be unnecessary if no functional change occurs.

## Inputs

- SiameseModel class definition (or equivalent neural network model)
- New parameter specification (name, type, default value, integration point)
- Existing test suite structure and conventions

## Outputs

- Unit test module with test cases for parameter acceptance, storage, and application
- Test execution report confirming all new tests pass and no regressions occur

## How to apply

Write unit tests covering three key areas: (1) Constructor acceptance — verify the model accepts the new parameter without raising errors; (2) Attribute storage — confirm the parameter is stored and retrievable as a model attribute; (3) Functional application — verify the parameter is integrated into the model's layer definitions (using appropriate APIs like keras.regularizers.L1L2) and actually affects model behavior during a training step. Run the full test suite using `python setup.py test` to confirm no regressions. Tests should be written in Python using a standard testing framework (e.g., pytest or unittest) and cover both default and user-supplied parameter values.

## Related tools

- **ms2deepscore** (Host library containing the SiameseModel class to be extended with new parameters and tested) — https://github.com/matchms/ms2deepscore
- **Python** (Language for writing and running unit tests; test execution via `python setup.py test`)
- **keras.regularizers** (API for integrating L1/L2 regularization into model layers; must be verified in tests to confirm correct application)

## Examples

```
# After adding L1/L2 parameters to SiameseModel constructor
from ms2deepscore.models import SiameseModel
model = SiameseModel(l1_reg=0.001, l2_reg=0.01)
assert hasattr(model, 'l1_reg') and model.l1_reg == 0.001
assert hasattr(model, 'l2_reg') and model.l2_reg == 0.01
```

## Evaluation signals

- Constructor accepts L1 and L2 arguments without raising TypeError or ValueError.
- Model instance stores parameter values as retrievable attributes (e.g., model.l1_reg, model.l2_reg).
- Regularization is integrated into layer definitions and model weights are penalized during a forward pass or training step (verified by inspecting model loss or weight updates).
- Existing test suite passes without regressions when run via `python setup.py test`.
- Unit tests cover both default parameter values (e.g., 0.0) and user-supplied values to ensure no silent failures.

## Limitations

- Tests verify parameter acceptance and storage but may not exhaustively validate that regularization strength produces expected generalization improvements — that requires empirical validation on held-out data.
- The specific regularizer API (e.g., keras.regularizers.L1L2) is framework-dependent; tests must be tailored to the underlying deep learning framework (Keras, PyTorch, TensorFlow).
- Tests do not guarantee that regularization parameters are optimal for all datasets or use cases — only that they are correctly implemented.

## Evidence

- [other] Write unit tests in Python to verify that: (a) the constructor accepts L1 and L2 arguments without error, (b) the parameters are stored as model attributes, and (c) the regularization is applied to model weights during a forward pass or training step.: "Write unit tests in Python to verify that: (a) the constructor accepts L1 and L2 arguments without error, (b) the parameters are stored as model attributes, and (c) the regularization is applied to"
- [other] Integrate the L1/L2 parameters into the model's layer definitions using the appropriate regularizer API (e.g., keras.regularizers.L1L2 or equivalent).: "Integrate the L1/L2 parameters into the model's layer definitions using the appropriate regularizer API (e.g., keras.regularizers.L1L2 or equivalent)."
- [other] Run the existing test suite with `python setup.py test` to confirm no regressions.: "Run the existing test suite with `python setup.py test` to confirm no regressions."
- [methods] make sure the existing tests still work by running ``python setup.py test``: "make sure the existing tests still work by running ``python setup.py test``"
