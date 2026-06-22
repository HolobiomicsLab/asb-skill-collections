---
name: ion-mobility-feature-engineering
description: Use when you have a set of metabolite structures (or their molecular descriptors) and need to construct training or target feature matrices for CCS prediction. Specifically, use it when you are preparing data to fit or apply a machine learning model (e.g., Sklearn v1.0.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0599
  tools:
  - Sklearn
  - Jupyter Lab
  - Tkinter
  - CCSP 2.0
  techniques:
  - ion-mobility-MS
derived_from:
- doi: 10.1021/acs.analchem.2c03491
  title: CCS Predictor 2.0
- doi: 10.1101/2022.08.09.503345
  title: ''
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ccs_predictor_2_0_cq
    doi: 10.1021/acs.analchem.2c03491
    title: CCS Predictor 2.0
  dedup_kept_from: coll_ccs_predictor_2_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.2c03491
  all_source_dois:
  - 10.1021/acs.analchem.2c03491
  - 10.1101/2022.08.09.503345
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ion-mobility-feature-engineering

## Summary

Feature engineering for ion-mobility mass spectrometry involves selecting and configuring molecular descriptor sets to train collision cross section (CCS) prediction models. This skill bridges raw metabolomics data and machine learning by curating input feature sets that encode molecular structure in a format compatible with Sklearn regressors.

## When to use

Apply this skill when you have a set of metabolite structures (or their molecular descriptors) and need to construct training or target feature matrices for CCS prediction. Specifically, use it when you are preparing data to fit or apply a machine learning model (e.g., Sklearn v1.0.2+) to predict collision cross sections from molecular properties, and you need to decide which descriptor features to include, how to normalize them, and how to validate that the feature set is compatible with your training set.

## When NOT to use

- Input dataset is already a validated CCS ground-truth reference library with no missing or low-confidence values—feature engineering is unnecessary if all CCS values are experimentally confirmed.
- You are working with a pre-trained CCSP 2.0 model and applying it unchanged to new data; feature engineering is already fixed in the model and should not be altered mid-analysis.
- Your target dataset has fundamentally different molecular classes, ionization modes, or mass ranges than your training set, such that descriptor distributions are non-overlapping; the model will extrapolate poorly regardless of feature selection.

## Inputs

- User-curated training set with molecular identifiers and experimental CCS values
- Molecular descriptor matrix or descriptor calculation pipeline
- Target metabolomics dataset with molecular structures or pre-computed descriptors
- Feature selection parameters (via Tk interface: which descriptor sets to use)

## Outputs

- Fitted Sklearn machine learning model (CCS predictor)
- Predicted CCS values for target metabolites
- Feature importance scores or coefficient weights (model-dependent)
- Filtered results with false positive annotations (low-confidence predictions)

## How to apply

Within the CCSP 2.0 workflow, feature engineering occurs in the model configuration step: (1) Load or define the set of molecular descriptors (e.g., structural, physicochemical properties) that will represent each metabolite. (2) Use the Tk graphical interface to select which input feature sets to include in the model—CCSP 2.0 allows users to choose among pre-defined descriptor collections. (3) Ensure that the feature set selected for training matches the feature set applied to the target metabolomics data; mismatched feature dimensions will cause prediction failure. (4) Validate that the number and names of features are consistent between the training dataset and the target dataset by inspecting the notebook's feature validation cells. (5) Execute the Sklearn model (typically a regressor such as RandomForest or Gradient Boosting) on the selected features to fit the CCS prediction model. The rationale is that CCS is a physical property dependent on molecular geometry and mass; descriptors must capture these properties without redundancy or missing dimensions.

## Related tools

- **Sklearn** (Machine learning library providing regression algorithms (e.g., RandomForest, GradientBoosting) to fit the CCS prediction model using the engineered feature sets) — https://scikit-learn.org/
- **Jupyter Lab** (Notebook environment for executing the CCSP 2.0 feature engineering and model training pipeline interactively) — https://jupyter.org/
- **Tkinter** (Graphical interface library providing dialogs and widgets for users to upload training data, configure model parameters, and select input feature sets)
- **CCSP 2.0** (End-to-end Jupyter notebook tool that encapsulates feature engineering, model training, CCS prediction, and false positive filtering) — https://github.com/facundof2016/CCSP2.0

## Examples

```
# In Jupyter Lab, after loading CCSP 2.0 notebook: features = notebook.select_features(['molecular_weight', 'polarity', 'rotatable_bonds']); model = notebook.fit_ccs_model(training_data, features); predictions = model.predict(target_data[features])
```

## Evaluation signals

- Feature matrix dimensions match between training and target datasets (same number of columns and column names/order); Sklearn fit() and predict() calls execute without shape mismatch errors.
- Predicted CCS values are physically reasonable (positive, within the expected range for the molecular mass and ionization mode of the target set) and do not contain NaN or inf values.
- Model predictions on held-out test data (or reference metabolites) exhibit lower prediction error and higher correlation with experimental CCS values compared to predictions using fewer or different feature sets (if cross-validation is performed).
- False positive filtering step (annotation confidence thresholding) correctly removes low-confidence CCS predictions while retaining high-confidence ones; compare filtered output against manual review or external validation dataset.
- Feature importance or coefficient weights (if the Sklearn model exposes them) are interpretable and correlate with known molecular properties that influence CCS (e.g., molecular weight, polarity, rotatable bonds).

## Limitations

- Google Colab deployment is limited to continuous operation for up to 12 hours and will disconnect after ~20 minutes if left idle, making it unsuitable for large-scale or long-running feature engineering workflows. The locally hosted Jupyter Lab version must be used for large training or target sets.
- Feature engineering success depends critically on the quality, diversity, and representativeness of the user-curated training set; if the training set does not cover the physicochemical or structural space of the target dataset, predictions will be unreliable.
- The Jupyter Lab version requires local Python 3 installation and manual management of dependencies (Sklearn v1.0.2 or later, listed in requirements.txt); environment setup errors can prevent model training.
- The current version of CCSP 2.0 is designed for ion-mobility mass spectrometry; applicability to other ionization modes, instruments, or molecular classes is not guaranteed without retraining on mode-specific data.

## Evidence

- [readme] Collision Cross Section Predictor 2.0 is an open source Python notebook intended to help ion-mobility scientists predict collision cross sections with user-curated training sets: "Collision Cross Section Predictor 2.0 is an open source Python notebook intended to help ion-mobility scientists predict collision cross sections with user-curated training sets"
- [other] CCSP 2.0 is packaged as a Jupyter Lab compatible notebook with a Tk interface, intended for users familiar with Python who plan to predict CCS values using large training or target sets in a local environment.: "CCSP 2.0 is packaged as a Jupyter Lab compatible notebook with a Tk interface, intended for users familiar with Python who plan to predict CCS values using large training or target sets in a local"
- [other] Integrate the Tk graphical interface components to allow users to upload training data, configure model parameters, and select input feature sets.: "Integrate the Tk graphical interface components to allow users to upload training data, configure model parameters, and select input feature sets"
- [other] Implement the collision cross section prediction model using Sklearn's machine learning algorithms on the user-provided training set.: "Implement the collision cross section prediction model using Sklearn's machine learning algorithms on the user-provided training set"
- [readme] The current version of CCSP 2.0 requires Sklearn V1.0.2 or later. A full list of package requirements is available in the requirements.txt file.: "The current version of CCSP 2.0 requires Sklearn V1.0.2 or later. A full list of package requirements is available in the requirements.txt file"
- [readme] If you plan to predict CCS values using large training or target sets or if you plan to integrate the code into a larger analysis workflow, the locally hosted Jupyter Lab version is recommended.: "If you plan to predict CCS values using large training or target sets or if you plan to integrate the code into a larger analysis workflow, the locally hosted Jupyter Lab version is recommended"
- [other] Execute predictions on target metabolomics data and output filtered results with false positive annotations.: "Execute predictions on target metabolomics data and output filtered results with false positive annotations"
