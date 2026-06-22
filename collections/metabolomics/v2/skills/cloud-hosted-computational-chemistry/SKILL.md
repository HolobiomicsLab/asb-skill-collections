---
name: cloud-hosted-computational-chemistry
description: Use when you have a curated dataset of ≤10,000 molecular structures with known collision cross section values for training, a target set of ≤10,000 molecules requiring CCS predictions, a compatible browser, and either lack local Python installation or prefer cloud-based execution to avoid.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  tools:
  - Google Colaboratory
  - Scikit-learn (Sklearn V1.0.2+)
  - Python
  - CCSP 2.0
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
---

# Cloud-hosted computational chemistry

## Summary

Execute collision cross section (CCS) prediction workflows on user-curated molecular training sets using Google Colaboratory, eliminating the need for local Python installation while constraining computation to <10,000 molecules and ≤12 hours continuous operation. This skill leverages Google-hosted services to train scikit-learn models and export predictions without local infrastructure.

## When to use

You have a curated dataset of ≤10,000 molecular structures with known collision cross section values for training, a target set of ≤10,000 molecules requiring CCS predictions, a compatible browser, and either lack local Python installation or prefer cloud-based execution to avoid dependency management. Ideal when predictions must be completed within a single session and results exported to CSV.

## When NOT to use

- Target dataset exceeds 10,000 molecules — use locally-hosted Jupyter Lab variant instead
- Analysis requires integration into a larger workflow or chaining with downstream analyses — use Jupyter Lab variant with Python environment
- Training or target set is very large or requires persistent storage across sessions — use locally-hosted Jupyter Lab variant

## Inputs

- User-curated training dataset containing molecular structures and known collision cross section values (CSV or compatible tabular format)
- Target dataset of ≤10,000 molecules requiring CCS predictions
- Scikit-learn model configuration parameters

## Outputs

- CSV file or compatible local file format containing molecular identifiers and predicted CCS values
- Trained collision cross section prediction model (in-session)

## How to apply

Download the 'CCSP 2.0 - CCS Prediction in Google Colab' notebook (.ipynb) from the facundof2016/CCSP2.0 repository, upload it to Google Colab (colab.research.google.com), and follow embedded instructions. Import your training dataset containing molecular structures and known CCS values, configure scikit-learn V1.0.2+ model parameters, train the model on the curated training set, load your target molecules (≤10,000), apply the trained model to generate predictions, and export results (molecular identifiers and predicted CCS values) to CSV. Monitor runtime against the 12-hour continuous operation limit and ~20-minute idle disconnection threshold; save work frequently to avoid loss during auto-disconnection.

## Related tools

- **Google Colaboratory** (Cloud-hosted Jupyter notebook runtime providing 12-hour continuous operation limit and ~20-minute idle disconnection for executing CCSP 2.0 prediction pipeline without local installation) — https://colab.research.google.com/
- **Scikit-learn (Sklearn V1.0.2+)** (Machine learning library performing model training and collision cross section prediction on molecular descriptors) — https://scikit-learn.org/
- **Python** (Programming language in which CCSP 2.0 notebook is written and executed)
- **CCSP 2.0** (Open-source Jupyter notebook implementing collision cross section prediction workflow for ion-mobility scientists) — https://github.com/facundof2016/CCSP2.0

## Evaluation signals

- CSV export file is present and contains molecular identifiers and predicted CCS values with no missing values
- Predicted CCS values are numeric, within physically plausible ranges for the molecules being analyzed, and match the cardinality of the target dataset (≤10,000 rows)
- Training completes without errors in Google Colab environment and model accuracy metrics (if reported) are comparable to local Jupyter Lab variant
- Session remains active for full prediction duration without triggering idle disconnection (monitor notebook for stale kernel indicators)
- File export to local computer succeeds without truncation or format corruption

## Limitations

- Google Colab enforces a 12-hour continuous operation limit; workflows exceeding this threshold will be interrupted
- Google Colab will auto-disconnect after ~20 minutes of idle time, requiring manual kernel restart and potential loss of in-memory state
- Skill is constrained to datasets with ≤10,000 molecules in either training or target set; larger datasets require locally-hosted Jupyter Lab variant
- Google Colab does not support persistent storage across sessions; all intermediate results must be exported before session ends
- Browser compatibility limited to recent versions of Chrome, Firefox, or Safari; older browsers may not support Google Colab interface

## Evidence

- [intro] Operational constraints of Google Colab runtime for CCSP 2.0: "Google Colab will only allow continuous notebook operation for up to 12 hours and will disconnect after ~20 minutes if left idle"
- [intro] No local installation requirement for Google Colab variant: "This route does not require you to install Python or any of the packages required to run the code, as all calculations are performed through Google hosted services"
- [intro] Scale constraint for Google Colab variant: "If you plan to use CCSP 2.0 only to make small scale predictions (<10,000 molecules) and export your results to your local computer, the Google Colab option is recommended"
- [readme] Scikit-learn version requirement: "The current version of CCSP 2.0 requires Sklearn V1.0.2 or later"
- [readme] Purpose and user base of CCSP 2.0: "Collision Cross Section Predictor 2.0 is an open source Python notebook intended to help ion-mobility scientists predict collision cross sections with user-curated training sets"
- [readme] Browser requirements for Google Colab: "it is recommended that you use the most recently released version of Chrome, Firefox or Safari"
