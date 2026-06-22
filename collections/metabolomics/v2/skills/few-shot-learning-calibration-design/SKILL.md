---
name: few-shot-learning-calibration-design
description: Use when you have experimental retention times measured on a source chromatographic method and want to predict RTs on a target chromatographic method, but possess only a small set (10–100) of molecules with ground-truth measurements on both methods.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3375
  tools:
  - alvaDesc
  - cmmrt
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

# few-shot-learning-calibration-design

## Summary

A Bayesian meta-learning approach that projects retention times between chromatographic methods using minimal calibration data (≥10 molecules), enabling rapid method transfer without extensive experimental validation. This skill applies Gaussian Process meta-learning to learn transferable RT mappings from small reference molecule sets, achieving competitive accuracy against traditional regression baselines.

## When to use

You have experimental retention times measured on a source chromatographic method and want to predict RTs on a target chromatographic method, but possess only a small set (10–100) of molecules with ground-truth measurements on both methods. This situation arises during analytical method harmonization, platform migration, or when establishing calibration for newly acquired instruments where full re-validation is impractical.

## When NOT to use

- Calibration set is smaller than 10 molecules; meta-learning requires sufficient diversity to learn the projection manifold.
- Source and target chromatographic methods operate under fundamentally different physical principles (e.g., hydrophilic interaction vs. reversed-phase); molecular feature space may not bridge the gap.
- You have access to a large training dataset (>1000 molecules) with full experimental coverage; standard supervised regression is more efficient and interpretable than meta-learning.

## Inputs

- Calibration molecule set with known RTs on both source and target chromatographic methods (≥10 molecules)
- SMILES strings or structural files for calibration and test molecules
- Molecular descriptors and fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) generated via alvaDesc

## Outputs

- Trained Bayesian meta-learned Gaussian Process projection model
- Predicted retention times for test molecules on target chromatographic method
- Mean absolute error (MAE) and median absolute error (MedAE) metrics
- Uncertainty estimates for projected retention times

## How to apply

First, generate standardized molecular descriptors and fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) for the small calibration molecule set using alvaDesc software. Train a Bayesian Gaussian Process meta-learner on this calibration set to model the RT transformation function between source and target chromatographic methods. The meta-learner learns a distribution over projection functions rather than a single point estimate, enabling uncertainty quantification. Apply the trained meta-learner to project RTs for uncharacterized test molecules. Evaluate performance by computing mean absolute error (MAE) and median absolute error (MedAE) between predicted and ground-truth experimental RTs on a held-out validation set, comparing against linear regression and standard machine learning regressors (random forest, gradient boosting) as baselines. The meta-learning framework leverages the structure of the calibration molecules to generalize effectively despite the small sample size.

## Related tools

- **alvaDesc** (Generates 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) for calibration and test molecules prior to meta-learning training) — https://www.alvascience.com/alvadesc/
- **cmmrt** (Implements the Bayesian meta-learning approach, Gaussian Process projection training, and RT prediction pipelines for chromatographic method transfer) — https://github.com/constantino-garcia/cmmrt

## Examples

```
make test_projections  # Tests meta-trained GP projections on reference chromatographic methods using PredRet database; outputs CSV and figure summaries to results/projection/
```

## Evaluation signals

- MAE and MedAE of projected RTs fall within the range of published baselines (39.2±1.2 s and 17.2±0.9 s for best-performing DNN), confirming competitive accuracy.
- Projected RTs exhibit correlation with ground-truth experimental values on held-out test molecules; residuals should be approximately normally distributed with mean near zero.
- Meta-learned uncertainty estimates (posterior variance) are well-calibrated: confidence intervals should contain the true RT with the stated coverage probability.
- Performance remains stable across different random seeds and cross-validation folds, indicating the meta-learner has not overfit the small calibration set.
- Error rates do not degrade significantly when the number of calibration molecules is reduced from the full set to the minimum (≥10), validating the few-shot learning property.

## Limitations

- Bayesian meta-learning requires careful tuning of hyperparameters (kernel choice, prior specification, meta-training iterations); poorly tuned models may underperform simpler baselines on small calibration sets.
- The approach assumes the source and target chromatographic methods operate under related physical principles such that a smooth RT transformation exists; if methods differ fundamentally, learned projections may be unreliable.
- Fingerprint-based features (MACCS166, ECFP, PFP) capture 2D molecular structure only; they may not capture method-specific effects (e.g., surface silanols, column aging, buffer pH) that influence RT in practice.
- Generalization beyond the chemical space represented in the calibration set is limited; molecules with unprecedented structural features may have high prediction uncertainty.
- The code repository notes that the main branch is under active development for integration into the CEU Mass Mediator platform; users should refer to the 'paper' branch to reproduce published results.

## Evidence

- [intro] A novel Bayesian meta-learning approach is proposed for RT projection between CMs from as few as 10 molecules while still obtaining competitive error rates compared with previous approaches.: "A novel Bayesian meta-learning approach is proposed for RT projection between CMs from as few as 10 molecules while still obtaining competitive error rates compared with previous approaches."
- [intro] 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software: "5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software"
- [intro] The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and 17.2 ± 0.9 s, respectively.: "The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and"
- [intro] Train machine learning regressors on retention time data using experimental RTs from the METLIN small molecule dataset: "We have trained state-of-the-art machine learning regressors using the 80,038 experimental RTs from the METLIN small molecule dataset (SMRT)"
- [readme] Note that, to integrate the proposal into the CEU Mass Mediator platform, the code in this repository will continue to be developed. Hence, branch `paper` should be used as reference for reproducing the results of the paper.: "Note that, to integrate the proposal into the CEU Mass Mediator platform, the code in this repository will continue to be developed. Hence, branch `paper` should be used as reference for reproducing"
- [readme] Meta-train a Gaussian Process (GP) for computing projections between CMs using the PredRet database. The resulting GP is stored in the saved_models folder.: "Meta-train a Gaussian Process (GP) for computing projections between CMs using the PredRet database for a few epochs. The resulting GP is stored in the `saved_models` folder."
