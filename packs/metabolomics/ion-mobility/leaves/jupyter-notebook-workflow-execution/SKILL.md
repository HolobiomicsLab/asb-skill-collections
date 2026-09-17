---
name: jupyter-notebook-workflow-execution
description: Use when you have a curated training dataset of molecular structures
  with known CCS values, a target set of ≤10,000 molecules requiring CCS predictions,
  and need to apply a pre-configured Sklearn-based machine learning model within a
  reproducible, browser-accessible environment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3070
  tools:
  - Google Colaboratory
  - Jupyter Lab
  - Python
  - Sklearn V1.0.2+
  - CCSP 2.0
  techniques:
  - ion-mobility-MS
  license_tier: restricted
  provenance_tier: literature
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

# Jupyter Notebook Workflow Execution

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Execute a curated machine learning workflow for collision cross section (CCS) prediction within a Jupyter notebook environment, either cloud-hosted (Google Colab) or locally, to generate CCS predictions for molecular datasets without requiring local Python installation or package management.

## When to use

You have a curated training dataset of molecular structures with known CCS values, a target set of ≤10,000 molecules requiring CCS predictions, and need to apply a pre-configured Sklearn-based machine learning model within a reproducible, browser-accessible environment. Use Google Colab variant when predictions are small-scale and results need to be exported locally; use local Jupyter Lab when working with large training/target sets or integrating predictions into a larger analysis pipeline.

## When NOT to use

- Target dataset exceeds 10,000 molecules and you are using Google Colab (use local Jupyter Lab instead)
- You require continuous unattended operation exceeding 12 hours (Colab enforces hard 12-hour session limit)
- Your workflow requires real-time model retraining or integration with external APIs beyond the notebook environment (local Jupyter Lab with custom extensions needed)
- You lack a compatible web browser or stable internet connection (Colab is cloud-dependent; local Jupyter Lab requires only local connectivity)

## Inputs

- User-curated training dataset (molecular structures + known CCS values, format unspecified but compatible with Python/Sklearn ingestion)
- Target molecular dataset (≤10,000 molecules for Google Colab; arbitrary size for Jupyter Lab)
- CCSP 2.0 notebook file (.ipynb)
- Compatible web browser (Chrome, Firefox, or Safari recommended for Colab)

## Outputs

- CSV file containing predicted CCS values with molecular identifiers
- Trained Sklearn machine learning model (persisted within notebook state during session)

## How to apply

Download the appropriate CCSP 2.0 notebook variant (.ipynb file) from the facundof2016/CCSP2.0 repository. For Google Colab: upload the notebook through colab.research.google.com and follow embedded instructions; for Jupyter Lab: install Python 3 (e.g. via Anaconda) and open the notebook locally. Load your user-curated training dataset containing molecular structures and known CCS values into the notebook environment. Configure training parameters and confirm Sklearn V1.0.2 or later is available. Train the model on the curated training set, then load your target dataset (≤10,000 molecules for Colab; no upper limit for Jupyter Lab). Apply the trained model to generate CCS predictions. Export predictions (molecular identifiers and predicted CCS values) to CSV format. Verify predictions completed successfully and no idle timeouts occurred (Colab: monitor for ~20-minute idle disconnect; Jupyter Lab: monitor for local execution completion).

## Related tools

- **Google Colaboratory** (Cloud-hosted Jupyter notebook runtime for small-scale (<10,000 molecule) CCS prediction without local Python installation; provides 12-hour continuous operation limit and ~20-minute idle disconnect threshold) — https://colab.research.google.com/
- **Jupyter Lab** (Local Jupyter notebook environment for large-scale CCS prediction and integration into broader analysis pipelines; requires local Python 3 and package installation) — https://jupyter.org/
- **Python** (Core language for CCSP 2.0 notebook implementation and model execution)
- **Sklearn V1.0.2+** (Machine learning library providing the underlying model training and prediction algorithms for CCS estimation from molecular descriptors)
- **CCSP 2.0** (Open-source Jupyter notebook tool implementing Sklearn-based collision cross section prediction with user-curated training sets) — https://github.com/facundof2016/CCSP2.0

## Evaluation signals

- Training dataset is successfully loaded and parsed into the notebook memory without encoding/format errors
- Model training completes and produces a trained Sklearn model object with non-null parameters and loss/accuracy metrics
- Target dataset is loaded with all ≤10,000 molecules (Colab) or arbitrary count (Jupyter Lab) correctly ingested
- Predictions are generated for all target molecules with CCS values in scientifically plausible range (no NaN, inf, or negative values)
- CSV export completes successfully and contains matching count of molecular identifiers and predicted CCS values with proper column headers

## Limitations

- Google Colab variant enforces hard 12-hour continuous operation ceiling; workflows must complete within this window
- Google Colab automatically disconnects after ~20 minutes of idle time, requiring user intervention to resume; unattended long-running training not feasible
- Google Colab variant designed for small-scale predictions (<10,000 molecules); large training or target sets require local Jupyter Lab variant
- Notebook requires Sklearn V1.0.2 or later; older versions will fail; package compatibility frozen to specific versions as defined in requirements.txt
- Model predictions depend entirely on quality and representativeness of user-curated training dataset; notebook provides no built-in training set validation or cross-validation framework
- Google Colab depends on stable internet connection and Google-hosted infrastructure availability; local outages or quota exhaustion may interrupt execution

## Evidence

- [readme] Collision Cross Section Predictor 2.0 is an open source Python notebook intended to help ion-mobility scientists predict collision cross sections with user-curated training sets: "Collision Cross Section Predictor 2.0 is an open source Python notebook intended to help ion-mobility scientists predict collision cross sections with user-curated training sets"
- [readme] Google Colab will only allow continuous notebook operation for up to 12 hours and will disconnect after ~20 minutes if left idle: "Google Colab will only allow continuous notebook operation for up to 12 hours and will disconnect after ~20 minutes if left idle"
- [readme] This route does not require you to install Python or any of the packages required to run the code, as all calculations are performed through Google hosted services: "This route does not require you to install Python or any of the packages required to run the code, as all calculations are performed through Google hosted services"
- [readme] The current version of CCSP 2.0 requires Sklearn V1.0.2 or later. A full list of package requirements is available in the requirements.txt file.: "The current version of CCSP 2.0 requires Sklearn V1.0.2 or later. A full list of package requirements is available in the requirements.txt file"
- [readme] If you plan to use CCSP 2.0 only to make small scale predictions (<10,000 molecules) and export your results to your local computer, the Google Colab option is recommended.: "If you plan to use CCSP 2.0 only to make small scale predictions (<10,000 molecules) and export your results to your local computer, the Google Colab option is recommended"
- [readme] If you plan to predict CCS values using large training or target sets or if you plan to integrate the code into a larger analysis workflow, the locally hosted Jupyter Lab version is recommended.: "If you plan to predict CCS values using large training or target sets or if you plan to integrate the code into a larger analysis workflow, the locally hosted Jupyter Lab version is recommended"
- [other] Load the target dataset of ≤10,000 molecules for which predictions are required. Apply the trained model to generate collision cross section predictions for all target molecules. Export the predictions (molecular identifiers and predicted CCS values) to a CSV or compatible local file format.: "Load the target dataset of ≤10,000 molecules for which predictions are required. Apply the trained model to generate collision cross section predictions for all target molecules. Export the"
