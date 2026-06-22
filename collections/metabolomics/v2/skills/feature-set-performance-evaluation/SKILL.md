---
name: feature-set-performance-evaluation
description: Use when when deciding which molecular representation to use for retention time prediction or similar regression tasks on small molecules, and you have access to multiple feature generation options (e.g., alvaDesc can generate both molecular descriptors and multiple fingerprint types).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0199
  tools:
  - alvaDesc
  - RDKit
derived_from:
- doi: 10.1186/s13321-022-00613-8
  title: cmmrt
evidence_spans:
- 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cmmrt_cq
    doi: 10.1186/s13321-022-00613-8
    title: cmmrt
  dedup_kept_from: coll_cmmrt_cq
schema_version: 0.2.0
---

# feature-set-performance-evaluation

## Summary

Systematically compare the predictive performance of alternative molecular feature representations (descriptors, fingerprints, or their combination) by training independent machine learning regressors on each and measuring prediction errors on held-out test data. This skill identifies which feature type or combination yields the lowest error for a given regression task.

## When to use

When deciding which molecular representation to use for retention time prediction or similar regression tasks on small molecules, and you have access to multiple feature generation options (e.g., alvaDesc can generate both molecular descriptors and multiple fingerprint types). Apply this skill early in model development to avoid investing in downstream optimization of suboptimal feature sets.

## When NOT to use

- If only one feature representation is available (e.g., only descriptors or only fingerprints can be generated with your tools) — comparison requires multiple candidates.
- If the dataset is very small (< 100–200 molecules with experimental labels) — models may not converge reliably, making error comparisons unreliable.
- If retention time labels are categorical or sparse rather than continuous — this skill is designed for regression; classification or imputation tasks require different evaluation.

## Inputs

- Molecular structures (SMILES, SDF, mol, inchi, or mol2 format)
- Experimental retention time labels (continuous numeric values)
- Train/test split specification

## Outputs

- Trained regressor models (one per feature set)
- Prediction error metrics per feature set (MAE, median AE, with uncertainty estimates)
- Comparative error distributions or rankings across feature sets
- Feature importance or diagnostic logs indicating which set dominates

## How to apply

Generate candidate feature sets from your molecular structure data using a tool such as alvaDesc: create one set containing only molecular descriptors (e.g., 5,666 descriptors), another containing only fingerprints (e.g., MACCS166, Extended Connectivity, Path Fingerprints; 2,214 total), and a third combining both. Train independent machine learning regressors (e.g., deep neural networks, gradient boosting) on each feature set using identical train/test split ratios and hyperparameter tuning procedures. Compute prediction errors (mean absolute error, median absolute error) for each trained model on the held-out test set. Compare error distributions across the three feature sets; fingerprints typically outperform descriptors alone for retention time prediction, but empirical validation is essential before committing to a single representation.

## Related tools

- **alvaDesc** (Generate molecular descriptors and fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) for input molecules prior to model training) — https://www.alvascience.com/alvadesc/
- **RDKit** (Alternative tool for fingerprint generation; used in notebook examples in the cmmrt repository) — https://www.rdkit.org/

## Examples

```
python cmmrt/rt/train_model.py --storage sqlite:///results/optuna/train.db --save_to saved_models && python cmmrt/rt/test_predictor.py --compare_features descriptors fingerprints combined
```

## Evaluation signals

- All three models (descriptors-only, fingerprints-only, combined) successfully train and produce predictions on the test set without NaN or divergence errors.
- Error metrics (MAE, median AE) are reported with uncertainty estimates (e.g., ±std) indicating reproducibility across cross-validation folds.
- Fingerprints-only and/or combined models achieve lower median/mean absolute error than descriptors-only model; a fingerprint advantage of ≥5–10 s in median AE is notable in retention time prediction.
- Feature set sizes and model architectures are held constant across comparisons (same hyperparameters, same train/test proportions, same random seed) to isolate the effect of feature choice.
- Error distributions can be visualized (e.g., box plots, histograms) to confirm consistency: fingerprint-based errors should show lower central tendency and not substantially higher variance.

## Limitations

- Feature generation with alvaDesc requires a commercial license, limiting reproducibility and accessibility of the preprocessing step.
- The skill compares only three fixed feature configurations; intermediate combinations (e.g., descriptor subset + subset of fingerprints) are not systematically explored.
- Performance ranking may be task- and dataset-specific: results from METLIN (80,038 molecules) may not generalize to smaller, domain-specific chromatographic methods or to different molecular property prediction tasks.
- The evaluation is restricted to regression error metrics (MAE, median AE); interpretability, computational cost, and feature dimensionality trade-offs are not addressed here.

## Evidence

- [other] research_question: "Do fingerprints outperform molecular descriptors alone or in combination with descriptors for machine learning-based retention time prediction?"
- [other] workflow_descriptor: "Train machine learning regressors independently on three feature sets: (a) descriptors only, (b) fingerprints only, (c) both descriptors and fingerprints combined. Compute prediction errors (mean"
- [readme] feature_generation_scale: "5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software"
- [readme] key_finding: "The models were trained using only the descriptors, only the fingerprints, and both types of features simultaneously. Results suggest that fingerprints tend to perform better."
- [readme] dataset_scale: "We have trained state-of-the-art machine learning regressors using the 80,038 experimental RTs from the METLIN small molecule dataset (SMRT)"
