---
name: bayesian-meta-learning-model-fitting
description: Use when you have a pre-trained DNN RT predictor (e.g., trained on METLIN
  SMRT with 80,038 experimental RTs) and need to adapt it to predict retention times
  in a new or external chromatographic method for which you have only 10–50 calibration
  molecules with known RTs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - alvaDesc
  - constantino-garcia/cmmrt
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1186/s13321-022-00613-8
  title: cmmrt
evidence_spans:
- 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity,
  and Path Fingerprints fingerprints) were generated with the alvaDesc software
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cmmrt
    doi: 10.1186/s13321-022-00613-8
    title: cmmrt
  dedup_kept_from: coll_cmmrt
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-022-00613-8
  all_source_dois:
  - 10.1186/s13321-022-00613-8
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Bayesian meta-learning model fitting

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Fit a Bayesian Gaussian Process meta-learning model to project retention times between different chromatographic methods using minimal calibration data (as few as 10 molecules). This approach learns a generalizable mapping from one chromatographic method's space to a pre-trained deep neural network's latent feature space, enabling accurate RT prediction with minimal reference measurements.

## When to use

You have a pre-trained DNN RT predictor (e.g., trained on METLIN SMRT with 80,038 experimental RTs) and need to adapt it to predict retention times in a new or external chromatographic method for which you have only 10–50 calibration molecules with known RTs. Use this skill when full retraining is infeasible and you want to leverage the DNN's learned representations via a lightweight Bayesian projection rather than retraining the entire model.

## When NOT to use

- You have >500 calibration molecules or sufficient data to retrain the full DNN—use supervised fine-tuning instead.
- You lack a pre-trained DNN model or cannot extract its latent representations—you must first train a base model on a large reference dataset.
- Your calibration molecules are from the same chromatographic method as the pre-trained model (no projection is needed); use direct DNN prediction instead.

## Inputs

- Pre-trained DNN model (trained on METLIN SMRT or similar large RT dataset with >80k molecules)
- Calibration molecules (≥10): SMILES, INCHI, or structure files (mol, SDF, mol2, hin format)
- Calibration molecule retention times (ground truth from target chromatographic method)
- Test molecules: SMILES, INCHI, or structure files
- Test molecule reference retention times (for evaluation)

## Outputs

- Fitted Bayesian Gaussian Process meta-learning model (projection mapping)
- Projected test molecule representations in DNN latent space
- Predicted retention times for test molecules
- Mean and median absolute error metrics comparing predictions to reference RTs

## How to apply

Extract molecular fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) for your small set of calibration molecules (≥10) using alvaDesc, generating the same fingerprint schemes as your pre-trained DNN. Extract feature representations from the penultimate layer of the pre-trained DNN for both calibration and test molecules. Fit a Bayesian Gaussian Process meta-learning model to learn the mapping from the calibration molecules' fingerprint space to the DNN's latent feature space, using the known RT values as supervision. Apply the fitted projection model to transform test molecules' fingerprints into the DNN's latent space, then generate RT predictions by passing the projected representations through the DNN's final regression layer. Evaluate using mean and median absolute error against reference RTs; competitive performance typically shows median absolute errors in the range of 17–20 seconds.

## Related tools

- **alvaDesc** (Generates molecular fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) from chemical structures for calibration and test molecules; required input for Bayesian projection fitting) — https://www.alvascience.com/alvadesc/
- **constantino-garcia/cmmrt** (Reference implementation of pre-trained DNN RT predictors and Bayesian meta-learning projection workflow; includes notebooks projections_to_different_cm.ipynb and train_with_rdkit.ipynb demonstrating the projection approach) — https://github.com/constantino-garcia/cmmrt

## Examples

```
python cmmrt/rt/train_model.py --storage sqlite:///results/optuna/train.db --save_to saved_models # followed by: from cmmrt import load_trained_dnn, fit_gp_projection; dnn = load_trained_dnn('saved_models'); gp = fit_gp_projection(dnn, calibration_fps, calibration_rts, n_calibration=10); predictions = gp.predict(test_fps)
```

## Evaluation signals

- Median absolute error (MAE_median) on test set is ≤20 seconds (competitive with previous methods on METLIN SMRT)
- Mean absolute error (MAE_mean) on test set is ≤45 seconds (aligned with reported 39.2±1.2 s for the base DNN)
- Bayesian GP posterior uncertainty estimates are finite and well-defined (no NaN or infinite variance in projected latent space)
- Projected test representations lie within the plausible range of the DNN's learned latent space (no extreme outliers in reconstruction error)
- Error distribution is symmetric and unimodal (no systematic bias toward over- or under-prediction across RT range)

## Limitations

- Requires a pre-trained DNN model; if the base model poorly captures RT behavior for your compound class or chromatographic chemistry, meta-learning cannot compensate.
- Performance depends on calibration molecule selection—molecules should span the RT range and chemical diversity of the test set; biased or clustered calibration samples may yield poor projections.
- Fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) are fixed feature representations; alvaDesc is proprietary software (under license).
- The approach assumes a smooth, learnable mapping between the source and target chromatographic spaces; highly non-linear or discontinuous RT relationships may require more calibration data.
- No statistical significance testing or confidence intervals for individual predictions are provided in the published approach; uncertainty is captured in the GP prior but not reported as prediction intervals.

## Evidence

- [other] A Bayesian meta-learning approach projects retention times between chromatographic methods using as few as 10 calibration molecules while maintaining competitive error rates relative to previous methods.: "A Bayesian meta-learning approach projects retention times between chromatographic methods using as few as 10 calibration molecules while maintaining competitive error rates relative to previous"
- [other] Extract feature representations from the penultimate layer of the pre-trained DNN for calibration and test molecules. Fit a Bayesian meta-learning projection model to learn the mapping from the external chromatographic method's space to the DNN's latent feature space using only the 10 calibration molecules and their known retention times.: "Extract feature representations from the penultimate layer of the pre-trained DNN for calibration and test molecules. Fit a Bayesian meta-learning projection model to learn the mapping from the"
- [readme] 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software: "5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software"
- [readme] The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and 17.2 ± 0.9 s respectively: "The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and"
- [readme] projections_to_different_cm.ipynb: map experimental retention times to the retention times predicted with a DNN (or viceversa). This is done by training a meta-learned GP prior on a small subset of known molecules.: "projections_to_different_cm.ipynb: map experimental retention times to the retention times predicted with a DNN (or viceversa). This is done by training a meta-learned GP prior on a small subset of"
