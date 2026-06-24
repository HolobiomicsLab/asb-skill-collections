---
name: ion-mobility-machine-learning-training
description: Use when you have a curated dataset of molecular structures (or molecular
  descriptors) paired with experimentally measured or reference collision cross section
  values, and you need to predict CCS values for a set of ≤10,000 novel molecules
  to filter or prioritize metabolomics identifications.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3373
  tools:
  - Google Colaboratory
  - scikit-learn
  - Jupyter Lab
  - CCSP 2.0
  techniques:
  - ion-mobility-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.2c03491
  title: CCS Predictor 2.0
- doi: 10.1101/2022.08.09.503345
  title: ''
evidence_spans:
- a Google Colaboratory Jupyter notebook that is well suited for beginners
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ion-mobility-machine-learning-training

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Train a scikit-learn machine learning model on user-curated collision cross section (CCS) reference data to enable predictive CCS value estimation for novel ion-mobility molecules. This skill bridges experimental CCS measurements with supervised learning to support metabolomics false positive filtering.

## When to use

You have a curated dataset of molecular structures (or molecular descriptors) paired with experimentally measured or reference collision cross section values, and you need to predict CCS values for a set of ≤10,000 novel molecules to filter or prioritize metabolomics identifications. Use this skill when local computational resources are unavailable or when predictions must be completed within a single session (<12 hours).

## When NOT to use

- Target dataset contains >10,000 molecules or requires continuous retraining; use the locally hosted Jupyter Lab variant instead.
- Training dataset contains fewer than ~50 reference CCS measurements or is highly imbalanced; insufficient training data will degrade model generalization.
- Your workflow requires integration with external analysis pipelines or local compute resources; the Google Colab variant is isolated and disconnects after ~20 minutes of idle time.

## Inputs

- User-curated training dataset (CSV or compatible format) with molecular structure identifiers and experimentally measured or reference collision cross section values
- Target dataset (CSV or compatible format) containing molecular identifiers and structures for ≤10,000 molecules requiring CCS predictions
- Machine learning model selection (e.g. Random Forest, Support Vector Regression, Neural Network via scikit-learn)

## Outputs

- Trained scikit-learn machine learning model (persisted in notebook memory or exported)
- CSV file containing molecular identifiers and predicted collision cross section values for the target dataset

## How to apply

Load a user-curated training dataset containing molecular structures and corresponding known CCS values into the CCSP 2.0 notebook environment. Configure scikit-learn V1.0.2 or later as the machine learning backend and select an appropriate regression or classification model. Train the model on the training set, then load the target dataset of molecules requiring CCS predictions (up to 10,000 molecules). Apply the trained model to generate predictions for all target molecules. Export the molecular identifiers and predicted CCS values to CSV format for downstream metabolomics filtering workflows. The rationale is that CCS is a physicochemical property that can be learned from empirical reference data, allowing rapid computational prediction without ion-mobility mass spectrometry analysis.

## Related tools

- **scikit-learn** (Provides supervised learning models (regression/classification) for CCS prediction from training data; version V1.0.2 or later required.) — https://scikit-learn.org/
- **Google Colaboratory** (Hosted Jupyter notebook environment executing Python code and scikit-learn model training via Google services; supports up to 12 hours continuous operation and ~20 minute idle timeout.) — https://colab.research.google.com/
- **Jupyter Lab** (Local Python notebook environment for running CCSP 2.0 with persistent compute and larger dataset handling; requires local Python 3 installation.) — https://jupyter.org/
- **CCSP 2.0** (Reference implementation of the ion-mobility machine learning training workflow; provides pre-built notebook with integrated data import, model training, and export steps.) — https://github.com/facundof2016/CCSP2.0

## Evaluation signals

- Training converges without errors and model is successfully instantiated; check scikit-learn model summary and training loss/accuracy metrics reported in notebook output.
- Predicted CCS values for target molecules are numeric, fall within expected physicochemical ranges for ion-mobility CCS (typically 100–500 Ų for small organic molecules), and match the dimensionality of the target dataset.
- CSV export file contains exactly two columns: molecular identifiers (matching input target dataset) and predicted CCS values with no missing or invalid entries.
- Cross-validation or holdout validation on training set (if performed) shows acceptable prediction accuracy (e.g., R² > 0.70 or mean absolute error within experimental CCS measurement reproducibility, typically 2–5%).
- Notebook execution completes within 12-hour session limit for Google Colab or within reasonable time for local Jupyter Lab; no premature disconnection or memory overflow errors occur.

## Limitations

- Google Colab sessions disconnect after ~20 minutes of inactivity and are limited to 12 hours continuous operation; large or iterative training workflows may require local Jupyter Lab.
- Model accuracy depends critically on training dataset quality and representativeness; CCS values for molecules outside the chemical space of the training set will have reduced predictive reliability.
- CCSP 2.0 requires scikit-learn V1.0.2 or later; older versions will fail. Full package requirements must be satisfied as listed in requirements.txt.
- Small training datasets (<50 reference CCS measurements) or highly imbalanced molecular classes may result in overfitting or poor generalization to target molecules.
- Predictions are computational estimates and are most reliable for prioritization or filtering workflows; confirmation by experimental ion-mobility analysis is recommended for high-stakes identifications.

## Evidence

- [other] training dataset with molecular structures and known CCS: "Collision Cross Section Predictor 2.0 is an open source Python notebook intended to help ion-mobility scientists predict collision cross sections with user-curated training sets"
- [readme] scikit-learn version requirement: "The current version of CCSP 2.0 requires Sklearn V1.0.2 or later"
- [readme] Google Colab operational limits: "Google Colab will only allow continuous notebook operation for up to 12 hours and will disconnect after ~20 minutes if left idle"
- [readme] target dataset size constraint: "If you plan to use CCSP 2.0 only to make small scale predictions (<10,000 molecules) and export your results to your local computer, the Google Colab option is recommended"
- [readme] no local installation required in Google Colab: "This route does not require you to install Python or any of the packages required to run the code, as all calculations are performed through Google hosted services"
- [other] CSV export workflow: "Export the predictions (molecular identifiers and predicted CCS values) to a CSV or compatible local file format"
