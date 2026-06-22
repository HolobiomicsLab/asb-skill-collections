---
name: bayesian-meta-learning-projection
description: Use when you need to transfer retention time predictions from one chromatographic method to another, but have access to only a small number (≥10) of molecules with known retention times in both methods.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
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
  - build: coll_cmmrt
    doi: 10.1186/s13321-022-00613-8
    title: cmmrt
  dedup_kept_from: coll_cmmrt
schema_version: 0.2.0
---

# Bayesian Meta-Learning Projection

## Summary

A Bayesian meta-learning approach that projects retention times across different chromatographic methods using minimal calibration data (as few as 10 molecules), enabling probabilistic annotation scoring without extensive method-specific retraining. This skill integrates uncertainty quantification via Gaussian Process priors trained on small calibration sets to map predicted retention times from a reference chromatographic method to a target method.

## When to use

Apply this skill when you need to transfer retention time predictions from one chromatographic method to another, but have access to only a small number (≥10) of molecules with known retention times in both methods. Use it as the final step in a metabolite annotation workflow where DNN-predicted retention times and their uncertainties must be projected and converted into probabilistic likelihood scores for ranking candidates.

## When NOT to use

- Fewer than 10 calibration molecules with paired retention times in both methods are available — the meta-learner requires sufficient data to establish the chromatographic relationship.
- Retention times already exist in the target chromatographic method for all candidates — direct experimental values should be used instead of projections.
- The reference and target chromatographic methods operate under fundamentally incompatible conditions (e.g., orthogonal separation mechanisms) where a continuous RT transformation is not valid.

## Inputs

- DNN-predicted retention times with uncertainty bounds for candidate molecules (in reference chromatographic method)
- Calibration dataset: ≥10 molecules with experimentally measured retention times in both reference and target chromatographic methods
- Molecular descriptors or fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) for calibration molecules

## Outputs

- Projected retention times in target chromatographic method with propagated uncertainties
- Probabilistic likelihood scores (normalized Gaussian kernels or probability densities) for each candidate
- Ranked candidate metabolite list sorted by RT-based likelihood score in descending order

## How to apply

Train a Bayesian Gaussian Process meta-learner on a set of ≥10 calibration molecules that have measured retention times in both the reference (source) and target chromatographic methods. The meta-learned GP prior encodes the chromatographic relationship learned from this small calibration set. Apply the trained meta-learner to project DNN-predicted retention times (with point estimates and uncertainty bounds, typically MAE ~39.2±1.2 s) from the reference method to the target method. Convert the projected retention times and propagated prediction uncertainties into probabilistic likelihood scores using normalized Gaussian kernels or probability density functions. Rank candidate metabolites in descending order of likelihood score. The rationale is that meta-learning captures the chromatographic transformation with minimal calibration data by leveraging a flexible GP prior that adapts quickly to new method pairs.

## Related tools

- **alvaDesc** (Generates molecular descriptors (5,666) and fingerprints (MACCS166, Extended Connectivity, Path Fingerprints; 2,214 total) required as input features for the DNN model and meta-learner) — https://www.alvascience.com/alvadesc/
- **cmmrt** (Python package implementing the Bayesian meta-learning projection approach, DNN retention time prediction, and hyperparameter tuning via Optuna) — https://github.com/constantino-garcia/cmmrt

## Examples

```
# Meta-train a Gaussian Process for projections between chromatographic methods using calibration molecules
python cmmrt/rt/train_model.py --storage sqlite:///results/optuna/train.db --save_to saved_models

# Test projection performance on a target chromatographic method
python -m cmmrt.projections --cm_reference "FEM long" --cm_target "LIFE old" --calibration_molecules 10 --output_dir results/projection
```

## Evaluation signals

- Projected retention times fall within expected error bounds (MAE ≤ 39.2±1.2 s, MdAE ≤ 17.2±0.9 s) when compared against ground-truth experimental RTs in the target method.
- Likelihood scores are properly normalized (sum to 1.0 if treated as probabilities, or are bounded [0, 1] for kernel-based scores) and rank known correct metabolite annotations higher than decoys.
- Uncertainty propagation: projected RT uncertainty increases monotonically with input DNN prediction uncertainty; confidence intervals from projections contain ground-truth RTs at expected coverage rates.
- Meta-learning converges with ≥10 calibration molecules; increasing calibration set size beyond 10–20 molecules shows diminishing returns in projection error reduction.
- Projected RTs show consistent behavior across multiple chromatographic method pairs (test on ≥4 reference methods as in the paper's evaluation protocol).

## Limitations

- Requires ≥10 calibration molecules with paired retention time measurements in both chromatographic methods; performance degrades below this threshold.
- Assumes a smooth, continuous transformation between chromatographic methods; orthogonal or fundamentally incompatible methods may violate this assumption.
- Inherits DNN prediction uncertainty (MAE ~39.2±1.2 s); projection error adds to this baseline and is not reducible below the calibration error of the DNN model itself.
- Meta-learning performance depends on the representativeness of the 10 calibration molecules; if they do not span the chemical diversity of candidates, projection accuracy may be poor.
- The approach requires training a separate meta-learned GP for each target chromatographic method; computational cost scales with the number of target methods.

## Evidence

- [readme] A novel Bayesian meta-learning approach is proposed for RT projection between CMs from as few as 10 molecules while still obtaining competitive error rates compared with previous approaches.: "A novel Bayesian meta-learning approach is proposed for RT projection between CMs from as few as 10 molecules while still obtaining competitive error rates"
- [other] Can a Bayesian meta-learning approach achieve competitive retention time prediction error rates when calibrated with only 10 molecules across different chromatographic methods?: "Can a Bayesian meta-learning approach achieve competitive retention time prediction error rates when calibrated with only 10 molecules"
- [other] Apply the Bayesian meta-learning projection model (cond_meta_learning_10mol) trained with 10 calibration molecules to project retention times across chromatographic methods.: "Apply the Bayesian meta-learning projection model (cond_meta_learning_10mol) trained with 10 calibration molecules to project retention times"
- [other] Use the Bayesian meta-learning approach to project predicted RTs from reference chromatographic method to the target chromatographic method (with ≥10 calibration molecules).: "Use the Bayesian meta-learning approach to project predicted RTs from reference chromatographic method to the target chromatographic method (with ≥10 calibration molecules)"
- [other] Convert projected RTs and prediction uncertainties into RT-based likelihood scores (probability density or normalized Gaussian kernel).: "Convert projected RTs and prediction uncertainties into RT-based likelihood scores (probability density or normalized Gaussian kernel)"
- [readme] The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and 17.2 ± 0.9 s respectively: "The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and"
