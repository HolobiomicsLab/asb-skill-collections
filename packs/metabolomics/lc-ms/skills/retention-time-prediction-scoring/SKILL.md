---
name: retention-time-prediction-scoring
description: Use when you have a list of candidate metabolites for an unknown compound (from mass-to-structure search or library matching), experimental retention time(s) from one or more chromatographic methods, and access to a trained DNN RT predictor and meta-learned RT projection model.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - alvaDesc
  - cmmrt (CMM-RT)
  techniques:
  - LC-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-022-00613-8
  all_source_dois:
  - 10.1186/s13321-022-00613-8
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Retention Time Prediction Scoring

## Summary

Score and rank metabolite annotation candidates by comparing observed chromatographic retention times against DNN-predicted values with confidence intervals, filtering candidates whose observed RT falls within projected uncertainty bounds. This probabilistic scoring integrates predicted RTs (MAE 39.2±1.2 s) with meta-learned RT projections between chromatographic methods to increase annotation specificity.

## When to use

You have a list of candidate metabolites for an unknown compound (from mass-to-structure search or library matching), experimental retention time(s) from one or more chromatographic methods, and access to a trained DNN RT predictor and meta-learned RT projection model. Use this skill to rank candidates by how well their predicted RTs match observed RTs, prioritizing high-confidence matches and discarding outliers.

## When NOT to use

- Input is a single metabolite without alternatives to rank or score—use RT prediction alone instead.
- Observed retention times are from an unmapped chromatographic method and you have <10 calibration molecules—the meta-learned projection will not be reliable; collect more calibration data or use a baseline linear regression.
- The DNN model has not been retrained or validated on your specific chromatographic method or ionization mode—model generalization is limited; retrain on representative data from your platform.

## Inputs

- List of candidate metabolites with molecular structures (SMILES, SDF, or mol format)
- Observed retention time value(s) from liquid chromatography (numeric, in seconds)
- Pre-trained DNN retention time prediction model (serialized neural network weights)
- Meta-learned Bayesian GP prior for RT projection (if projecting between chromatographic methods)
- Calibration molecule set with known RTs in both source and target chromatographic methods (≥10 molecules, recommended for projection)

## Outputs

- Ranked annotation candidate table (CSV or similar format)
- Per-candidate RT prediction confidence intervals (lower and upper bounds)
- Per-candidate annotation scores (e.g., 0–1 scale based on RT agreement)
- Per-candidate RT prediction errors (MAE, median absolute error in seconds)
- Filtered candidate subset (candidates with observed RT outside confidence interval removed or flagged)

## How to apply

Load the pre-trained DNN model and compute predicted retention times for each candidate metabolite using its molecular structure (fingerprints: MACCS166, Extended Connectivity, Path Fingerprints). For each candidate, compute the RT prediction confidence interval (uncertainty bounds). If projecting between chromatographic methods, apply the meta-learned Bayesian GP prior (trained on ≥10 calibration molecules from the source method) to map observed RTs to the target method's scale. Score each candidate by checking whether the observed RT falls within the predicted confidence interval; candidates within bounds receive high scores (ranked first), while those outside bounds are filtered or ranked lower. Output a ranked table of annotation candidates sorted by descending score (highest confidence first), with annotation scores and RT prediction errors (MAE, MedAE) for each candidate.

## Related tools

- **alvaDesc** (Generates MACCS166, Extended Connectivity, and Path fingerprints required as input features to the DNN retention time predictor) — https://www.alvascience.com/alvadesc/
- **cmmrt (CMM-RT)** (Reference implementation of the DNN RT predictor, meta-learned Bayesian GP for RT projection, and scoring workflow from the paper) — https://github.com/constantino-garcia/cmmrt

## Examples

```
python cmmrt/rt/train_model.py --storage sqlite:///results/optuna/train.db --save_to saved_models; python -c "from cmmrt.rt import predict_and_score; candidates = predict_and_score(structures=['C1=CC=C(C=C1)C(=O)O', ...], observed_rt=[125.4, 128.1], model_path='saved_models/dnn.pkl')"
```

## Evaluation signals

- Ranked candidates with observed RT within predicted confidence interval receive higher scores than those outside bounds.
- Mean absolute error (MAE) of projected RTs matches paper benchmark (39.2±1.2 s) when evaluated on held-out test set.
- Median absolute error (MedAE) of projected RTs is ≤17.2±0.9 s on METLIN SMRT dataset or comparable external validation set.
- When meta-learning on ≥10 calibration molecules, RT projection error remains competitive with baseline methods (linear regression, standard ML regressors).
- Filtered candidates (removed because observed RT fell outside confidence interval) are confirmed to be true negatives or low-probability matches in independent validation.

## Limitations

- DNN generalization depends on feature representation (fingerprints vs. descriptors); fingerprints outperform descriptors alone, but cross-method and cross-platform transfer requires retraining or fine-tuning.
- Meta-learned RT projection is most reliable with ≥10 calibration molecules; fewer molecules may yield unreliable uncertainty estimates.
- Confidence intervals assume the DNN uncertainty estimates are well-calibrated; calibration should be validated on the target chromatographic method before filtering or ranking in production.
- The method requires alvaDesc (proprietary, under license) for fingerprint generation; open-source alternatives may degrade performance.
- Both retained and unretained molecules are included in the METLIN SMRT training set; RT predictions for unretained compounds may have higher error or different uncertainty properties.

## Evidence

- [other] Score candidate metabolites by computing RT prediction confidence intervals and comparing observed versus predicted RT values, filtering candidates where observed RT falls within the projected uncertainty bounds.: "Score candidate metabolites by computing RT prediction confidence intervals and comparing observed versus predicted RT values, filtering candidates where observed RT falls within the projected"
- [readme] A heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging achieved mean and median absolute errors of 39.2±1.2 s and 17.2 ± 0.9 s, respectively: "The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and"
- [readme] A Bayesian meta-learning approach enables RT projection between chromatographic methods using as few as 10 molecules with competitive error rates: "A novel Bayesian meta-learning approach is proposed for RT projection between CMs from as few as 10 molecules while still obtaining competitive error rates compared with previous approaches."
- [readme] 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software: "5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software."
- [readme] Results suggest that fingerprints tend to perform better than descriptors alone or in combination: "Results suggest that fingerprints tend to perform better."
- [other] Load molecular structures and their corresponding predicted retention times from the pre-trained DNN model (mean absolute error 39.2±1.2 s): "Load molecular structures and their corresponding predicted retention times from the pre-trained DNN model (mean absolute error 39.2±1.2 s)."
