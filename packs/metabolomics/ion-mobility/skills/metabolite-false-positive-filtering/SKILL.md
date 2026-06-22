---
name: metabolite-false-positive-filtering
description: Use when you have ion-mobility mass spectrometry metabolomics data with putative metabolite identifications (e.g., from database matching) and want to reduce false positives by cross-validating compound identities against machine-learned CCS predictions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3960
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0821
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - Sklearn (scikit-learn) v1.0.2+
  - Jupyter Lab
  - Google Colaboratory
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

# metabolite-false-positive-filtering

## Summary

Use machine-learning-predicted collision cross section (CCS) values to filter false positive metabolite identifications in ion-mobility mass spectrometry datasets. This skill applies a trained CCS prediction model to experimentally detected compounds and compares predicted vs. observed CCS to remove low-confidence annotations.

## When to use

You have ion-mobility mass spectrometry metabolomics data with putative metabolite identifications (e.g., from database matching) and want to reduce false positives by cross-validating compound identities against machine-learned CCS predictions. Apply this skill when you have experimental CCS measurements paired with feature annotations and access to a curated training set of known metabolites.

## When NOT to use

- Your dataset lacks experimental CCS measurements or ion-mobility instrumentation data.
- You do not have a sufficiently large and representative curated training set of metabolites with validated CCS values; model accuracy depends critically on training set quality and diversity.
- You are working with small-scale predictions (<10,000 molecules) where deployment overhead outweighs benefit, or you require only rapid exploration rather than production filtering.

## Inputs

- Ion-mobility mass spectrometry dataset with experimental CCS measurements (float, m²/V·s)
- Metabolite feature annotations or database matches with compound identifiers
- Curated training set of known metabolites with validated CCS values and molecular descriptors
- Molecular feature matrix (e.g., mass-to-charge ratio, retention time, adduct type, or computed molecular properties)

## Outputs

- Filtered metabolite annotation table with false positives removed
- Predicted CCS values for each target compound
- Confidence scores or residuals (observed − predicted CCS) for each annotation
- Summary statistics on false positive removal and model performance metrics

## How to apply

Load your metabolomics dataset (experimental CCS values and tentative compound annotations) into CCSP 2.0 along with a user-curated training set of metabolites with known CCS values. Train an Sklearn machine-learning model (e.g., random forest or regression) on the training set to learn the relationship between molecular features and CCS. Execute the model on your target metabolites to predict their expected CCS values. Compare predicted CCS against observed CCS for each putative identification; filter out annotations where the discrepancy exceeds a user-defined tolerance threshold, thereby removing likely false positives while retaining high-confidence matches.

## Related tools

- **Python** (Core programming language for implementing CCS prediction and filtering logic)
- **Sklearn (scikit-learn) v1.0.2+** (Machine-learning library providing regression and classification algorithms to train CCS prediction models from training sets)
- **Jupyter Lab** (Interactive notebook environment hosting the locally executed CCSP 2.0 Tk interface for large-dataset processing) — https://github.com/facundof2016/CCSP2.0
- **Google Colaboratory** (Cloud-hosted Jupyter notebook for beginner-friendly, small-scale CCS predictions without local Python installation (up to 12 hr continuous operation)) — https://github.com/facundof2016/CCSP2.0
- **CCSP 2.0** (End-to-end open-source Python notebook tool implementing the complete workflow: model training, CCS prediction, and false positive filtering on user-curated metabolite datasets) — https://github.com/facundof2016/CCSP2.0

## Evaluation signals

- Predicted CCS values for training-set compounds match observed CCS within acceptable residual tolerance (user-defined, typically <5% relative error in original CCS units).
- Filtered annotation table shows reduced false positive rate compared to unfiltered database matches, validated against reference standards or orthogonal identification methods (e.g., fragmentation patterns, retention-index databases).
- Model generalization metrics (e.g., cross-validation RMSE, R²) on hold-out test compounds confirm that model performance is not degraded on unseen molecules.
- Output CCS predictions and residual distributions are consistent with expected physical properties of predicted compounds (e.g., larger/more complex molecules predict higher CCS).
- Number of retained high-confidence annotations is sufficient for downstream metabolomic or pathway analysis without introducing substantial bias.

## Limitations

- Model accuracy is limited by the quality, size, and chemical diversity of the user-curated training set; sparse or biased training data will produce unreliable predictions for out-of-domain metabolites.
- Google Colaboratory option supports only small-scale predictions (<10,000 molecules) and has session limits (12 hr continuous, ~20 min idle disconnect); large-scale or long-running workflows require local Jupyter Lab deployment.
- CCS prediction relies on computed molecular descriptors or explicit feature engineering; predictions are only as good as the feature representation and the underlying machine-learning algorithm, and may fail for novel metabolite classes not well-represented in training data.
- The skill assumes availability of experimental CCS measurements for validation; datasets lacking ion-mobility instrumentation cannot benefit from this filtering approach.
- Tk interface integration in local Jupyter Lab variant may have platform-specific dependencies or compatibility issues depending on Python distribution and operating system.

## Evidence

- [readme] CCSP 2.0 is written in Python and packaged into two notebook forms: (1) a Google Colaboratory Jupyter notebook that is well suited for beginners, and (2) a Jupyter Lab compatible notebook with a Tk interface for users more familiar with Python.: "CCSP 2.0 is written in Python and packaged into two notebook forms: (1) a Google Colaboratory Jupyter notebook that is well suited for beginners, and (2) a Jupyter Lab compatible notebook with a Tk"
- [readme] CCSP 2.0 requires Sklearn V1.0.2 or later; it is an open source Python notebook intended to help ion-mobility scientists predict collision cross sections with user-curated training sets.: "The current version of CCSP 2.0 requires Sklearn V1.0.2 or later"
- [readme] If you plan to predict CCS values using large training or target sets or if you plan to integrate the code into a larger analysis workflow, the locally hosted Jupyter Lab version is recommended.: "If you plan to predict CCS values using large training or target sets or if you plan to integrate the code into a larger analysis workflow, the locally hosted Jupyter Lab version is recommended"
- [readme] This route does not require you to install Python or any of the packages required to run the code, as all calculations are performed through Google hosted services. Google Colab will only allow continuous notebook operation for up to 12 hours and will disconnect after ~20 minutes if left idle.: "Google Colab will only allow continuous notebook operation for up to 12 hours and will disconnect after ~20 minutes if left idle"
- [intro] CCSP 2.0 is an open source Python notebook intended to help ion-mobility scientists predict collision cross sections with user-curated training sets.: "Collision Cross Section Predictor 2.0 is an open source Python notebook intended to help ion-mobility scientists predict collision cross sections with user-curated training sets"
