---
name: bayesian-meta-learning-chromatographic-projection
description: Use when you have experimental retention times (RTs) for a small set
  of calibration molecules (≥10) measured on both a source chromatographic method
  and a target method, and you need to predict RTs for candidate metabolites on the
  target method to rank annotation candidates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3664
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3407
  tools:
  - alvaDesc
  - cmmrt (constantino-garcia/cmmrt)
  techniques:
  - LC-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Bayesian meta-learning chromatographic projection

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply a Bayesian meta-learning approach to project retention times between chromatographic methods using minimal calibration data (≥10 molecules), enabling confident metabolite annotation candidate ranking when switching between analytical platforms or instruments.

## When to use

You have experimental retention times (RTs) for a small set of calibration molecules (≥10) measured on both a source chromatographic method and a target method, and you need to predict RTs for candidate metabolites on the target method to rank annotation candidates. This is especially valuable when you lack large training datasets for the target chromatographic method or need to transfer RT knowledge between different analytical platforms (e.g., different columns, gradient methods, or instruments).

## When NOT to use

- You have fewer than 10 calibration molecules with paired measurements on both source and target methods; the meta-learning approach requires at least this minimum to estimate a meaningful prior.
- Your calibration molecules cover only a narrow range of the chemical space relevant to your unknowns; the projection will not extrapolate reliably beyond the calibration set's descriptor distributions.
- You are comparing retention times from fundamentally incompatible chromatographic methods (e.g., reversed-phase vs. hydrophilic interaction chromatography) where molecular descriptors cannot capture the mechanistic shift; the Bayesian approach assumes the RT shift is learnable from small data.

## Inputs

- Molecular structures in SMILES or SDF format
- Calibration molecules with experimentally measured retention times on source chromatographic method (≥10 molecules)
- Calibration molecules with experimentally measured retention times on target chromatographic method (same ≥10 molecules)
- Candidate metabolites for annotation (structures only, or structures + observed RTs)

## Outputs

- Projected retention times for candidate metabolites on target chromatographic method
- Prediction confidence intervals (uncertainty bounds) for each projected RT
- Ranked candidate metabolite table with annotation scores and RT prediction errors
- Trained Bayesian meta-learned GP model (for reuse on future projections)

## How to apply

First, generate molecular descriptors and fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) for all calibration molecules using alvaDesc software. Train a Bayesian meta-learned Gaussian Process prior on this small calibration set (minimum 10 molecules) to learn the nonlinear RT projection mapping from source to target chromatographic method. Apply the trained meta-learner to project RTs for test/candidate molecules, computing both point estimates and prediction confidence intervals (uncertainty bounds) for each projection. Score metabolite candidates by evaluating whether their observed RT falls within the projected uncertainty bounds; candidates with observed RTs inside the bounds receive higher confidence scores. Rank candidates by descending confidence score and filter out those falling outside the confidence intervals.

## Related tools

- **alvaDesc** (Generate molecular descriptors and fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) required as input features for the Bayesian meta-learner and RT projection model) — https://www.alvascience.com/alvadesc/
- **cmmrt (constantino-garcia/cmmrt)** (Reference implementation of Bayesian meta-learning for RT projection; includes notebooks (projections_to_different_cm.ipynb) for mapping experimental RTs between chromatographic methods and Makefile rules (make train_projections, make test_projections) for meta-training and testing the GP-based projector) — https://github.com/constantino-garcia/cmmrt

## Examples

```
python cmmrt/rt/train_model.py --storage sqlite:///results/optuna/train.db --save_to saved_models && python -c "from cmmrt.projection import meta_train_gp; meta_train_gp(calibration_molecules_source_rt, calibration_molecules_target_rt, descriptors, fingerprints, epochs=1000)"
```

## Evaluation signals

- Mean absolute error (MAE) and median absolute error (MedAE) of projected RTs on the target chromatographic method compared to ground-truth experimental values should be competitive with or better than baseline methods (traditional linear regression, standard ML regressors).
- Prediction confidence intervals should have appropriate coverage: observed RTs for test molecules fall within the projected uncertainty bounds at the expected frequency (e.g., ~68% within 1σ intervals for a well-calibrated Bayesian model).
- Ranked candidate metabolites with observed RTs inside the projected confidence intervals should have higher true positive identification rates compared to candidates outside the bounds or unranked pools.
- Meta-learned projections trained on only ≥10 calibration molecules should achieve comparable error rates to projections trained on larger calibration sets, demonstrating sample efficiency of the Bayesian approach.
- The projection model should generalize across multiple target chromatographic methods (e.g., FEM long, LIFE old, FEM orbitrap plasma, RIKEN from the PredRet database) when meta-trained on diverse source methods.

## Limitations

- The approach requires the alvaDesc software (under license) to generate molecular fingerprints and descriptors; an open-source alternative fingerprint generator would be needed for fully open workflows.
- Projection quality depends critically on the chemical similarity and descriptor overlap between calibration molecules and candidate metabolites; the model cannot reliably extrapolate beyond the calibration set's chemical space.
- The minimum calibration set size (≥10 molecules) is a practical lower bound; actual performance may improve substantially with 20–50 well-chosen calibration molecules spanning diverse compound classes.
- The Bayesian meta-learning approach assumes the RT shift between chromatographic methods is learnable from molecular descriptors; methods with fundamentally different selectivity mechanisms may not project well.
- Integration into the CEU Mass Mediator platform is ongoing; the branch 'paper' should be used as the reference for reproducing the published results, as the main branch may contain unreleased developments.

## Evidence

- [intro] A novel Bayesian meta-learning approach is proposed for RT projection between CMs from as few as 10 molecules while still obtaining competitive error rates compared with previous approaches.: "A novel Bayesian meta-learning approach is proposed for RT projection between CMs from as few as 10 molecules while still obtaining competitive error rates compared with previous approaches."
- [other] Generate molecular descriptors and fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) for calibration molecules using alvaDesc.: "Generate molecular descriptors and fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) for calibration molecules using alvaDesc."
- [readme] 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software: "5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software"
- [other] Train the Bayesian meta-learning model on the small calibration set (≥10 molecules) to learn the RT projection mapping between source and target chromatographic methods.: "Train the Bayesian meta-learning model on the small calibration set (≥10 molecules) to learn the RT projection mapping between source and target chromatographic methods."
- [other] Score candidate metabolites by computing RT prediction confidence intervals and comparing observed versus predicted RT values, filtering candidates where observed RT falls within the projected uncertainty bounds.: "Score candidate metabolites by computing RT prediction confidence intervals and comparing observed versus predicted RT values, filtering candidates where observed RT falls within the projected"
- [readme] Note that, to integrate the proposal into the CEU Mass Mediator platform, the code in this repository will continue to be developed. Hence, branch `paper` should be used as reference for reproducing the results of the paper.: "Note that, to integrate the proposal into the CEU Mass Mediator platform, the code in this repository will continue to be developed. Hence, branch `paper` should be used as reference for reproducing"
