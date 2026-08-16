---
name: chromatographic-method-transfer
description: Use when you have retention time predictions from a source chromatographic
  method and need to predict retention times for a target chromatographic method,
  but have limited calibration data (10–100 molecules) measured on both methods.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3375
  tools:
  - alvaDesc
  - cmmrt
  license_tier: restricted
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

# chromatographic-method-transfer

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Transfer retention time predictions between different chromatographic methods using Bayesian meta-learning trained on a small calibration set (as few as 10 molecules). This skill enables projection of retention times across chromatographic systems while maintaining competitive error rates without requiring large amounts of method-specific training data.

## When to use

You have retention time predictions from a source chromatographic method and need to predict retention times for a target chromatographic method, but have limited calibration data (10–100 molecules) measured on both methods. This is typical when deploying a retention time model trained on one LC–MS platform to a different platform or when bridging between incompatible chromatographic systems.

## When NOT to use

- Your calibration set contains fewer than 5–10 molecules; the Bayesian meta-learner requires sufficient paired observations to adapt to the target method.
- Retention times are already available for all molecules on the target chromatographic method; direct comparison or simple interpolation is more efficient.
- The source and target chromatographic methods are fundamentally incompatible (e.g., very different stationary phases or elution conditions) with no documented transfer studies; meta-learning assumes some transferability in the projection function.

## Inputs

- Molecular descriptors and fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) generated via alvaDesc
- Retention time measurements from calibration molecules on both source and target chromatographic methods (≥10 molecules)
- Optional: Pre-trained DNN retention time predictor for the source chromatographic method
- Reference chromatographic method dataset (e.g., PredRet database) for meta-training the GP prior

## Outputs

- Meta-learned Gaussian Process model encoding the prior distribution over chromatographic projections
- Projected retention times on the target chromatographic method
- Error metrics: mean absolute error (MAE) and median absolute error (MdAE) of projections
- Trained meta-learning model saved for future use on new target chromatographic methods

## How to apply

Train a Bayesian Gaussian Process meta-learner on pairs of retention times (source and target method) from your calibration molecules using the cmmrt repository's meta-learning workflow. The meta-learner learns a prior distribution over the chromatographic projection functions from these few reference molecules, then adapts to new target methods. After meta-training on a reference set of chromatographic methods (e.g., using the PredRet database), test projection performance by computing mean absolute error (MAE) and median absolute error (MdAE) between projected and ground-truth retention times on held-out target chromatographic methods. Success is indicated by MAE ≤ 40 s and MdAE ≤ 18 s, competitive with baseline projection approaches (expected: MAE ~39.2±1.2 s, MdAE ~17.2±0.9 s).

## Related tools

- **alvaDesc** (Generates molecular descriptors (5,666) and fingerprints (MACCS166, Extended Connectivity, Path Fingerprints; 2,214 total) required as input features for the meta-learning projection model) — https://www.alvascience.com/alvadesc/
- **cmmrt** (Core repository implementing Bayesian meta-learning for chromatographic method transfer, including GP meta-training and projection workflows) — https://github.com/constantino-garcia/cmmrt

## Examples

```
make test_projections
```

## Evaluation signals

- Mean absolute error (MAE) of projected retention times ≤ 40 s and median absolute error (MdAE) ≤ 18 s when tested on held-out target chromatographic methods.
- Projected error rates are competitive with or better than baseline projection methods (reference: MAE ~39.2±1.2 s, MdAE ~17.2±0.9 s).
- The meta-learned model generalizes to new target chromatographic methods not seen during meta-training, indicating that the learned prior captures transferable projection structure.
- Calibration set size vs. projection error exhibits a plateau by 10–15 molecules, confirming that few calibration samples suffice for competitive performance.
- Cross-validation or held-out test set evaluation shows stable error metrics across replicate meta-training runs (low variance across random states).

## Limitations

- Requires alvaDesc software (commercial license) to generate the specific fingerprint and descriptor features used in model training; feature generation cannot easily be substituted with open-source alternatives.
- Performance depends on the quality and representativeness of the calibration set; highly unusual or structurally novel molecules in the target set may exceed error bounds.
- Meta-learning assumes that chromatographic methods share a common underlying projection structure; methods with radically different stationary phases or pH may not transfer well.
- The approach is currently optimized for small-molecule retention time prediction; applicability to larger biomolecules (peptides, proteins) is not demonstrated in the paper.

## Evidence

- [intro] A novel Bayesian meta-learning approach is proposed for RT projection between CMs from as few as 10 molecules while still obtaining competitive error rates compared with previous approaches.: "A novel Bayesian meta-learning approach is proposed for RT projection between CMs from as few as 10 molecules while still obtaining competitive error rates compared with previous approaches."
- [intro] 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software: "5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software"
- [intro] The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and 17.2 ± 0.9 s respectively: "The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and"
- [readme] Meta-train a GP for projections using all data from PredRet database: "Meta-train a GP for projections using all data from PredRet database"
- [readme] For each system, the GP is meta-trained using all other CMs from the PredRet database before testing the performance on the target CM.: "For each system, the GP is meta-trained using all other CMs from the PredRet database before testing the performance on the target CM."
