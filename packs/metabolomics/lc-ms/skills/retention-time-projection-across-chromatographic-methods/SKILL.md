---
name: retention-time-projection-across-chromatographic-methods
description: Use when when you have retention times measured on one chromatographic method and need to predict or map them to another method with minimal or no overlap in measured molecules.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - alvaDesc
  - cmmrt
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# retention-time-projection-across-chromatographic-methods

## Summary

Project retention times between different chromatographic methods using a Bayesian meta-learning approach that learns a mapping from minimal calibration data (as few as 10 molecules) to a pre-trained DNN's latent feature space. This enables metabolite annotation and cross-method RT prediction with competitive accuracy relative to larger calibration sets.

## When to use

When you have retention times measured on one chromatographic method and need to predict or map them to another method with minimal or no overlap in measured molecules. Specifically, use this skill when you have: (1) a small set (10–100) of calibration molecules with known RTs on both source and target chromatographic methods, (2) access to a pre-trained DNN RT predictor trained on a large reference dataset (e.g. METLIN SMRT with 80,038 experimental RTs), and (3) need to avoid extensive re-calibration across different LC–MS platforms or instrument configurations.

## When NOT to use

- Calibration set contains fewer than ~5–10 molecules; meta-learning requires sufficient examples to fit a Bayesian prior and may overfit or fail to converge on extremely sparse data.
- Target chromatographic method is fundamentally different in chemistry (e.g., hydrophilic interaction liquid chromatography vs. reverse-phase) such that the DNN's latent space learned on one method does not generalize; in such cases, method-specific retraining may be necessary.
- No pre-trained DNN model is available and generating one from scratch is not feasible; the approach relies on transfer learning from a large reference dataset.

## Inputs

- Molecular structures (SMILES, SDF, mol, mol2, or hin format) for calibration molecules
- Experimental retention times for calibration molecules on source and/or target chromatographic method
- Molecular structures for test/query molecules
- Pre-trained DNN model checkpoint (trained on reference RT dataset with fingerprint features)
- alvaDesc software instance configured for fingerprint generation (MACCS166, Extended Connectivity, Path Fingerprints)

## Outputs

- Predicted retention times for test molecules on target chromatographic method
- Projection mapping (learned Bayesian meta-model) from source to DNN latent space
- Feature representations (penultimate layer activations) for calibration and test molecules
- Mean and median absolute error metrics comparing predictions to reference RTs

## How to apply

First, generate molecular fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints) for both calibration and test molecules using alvaDesc software. Extract feature representations from the penultimate layer of a pre-trained DNN model trained on the reference chromatographic dataset. Fit a Bayesian meta-learning model (typically a Gaussian Process with a meta-learned prior) on the small set of calibration molecules and their known RTs, learning the mapping from the source chromatographic method's molecular descriptors to the DNN's latent space. Apply the learned projection to transform test set molecules' representations and pass them through the DNN's final regression layer to generate RT predictions. Assess performance by comparing predicted RTs against reference RTs, computing mean and median absolute errors as primary metrics.

## Related tools

- **alvaDesc** (Generates 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) for input compounds; used to produce feature vectors for both calibration and test molecules.) — https://www.alvascience.com/alvadesc/
- **cmmrt** (Python package implementing the full retention time prediction and Bayesian meta-learning projection workflow, including DNN training, hyperparameter tuning, and projection meta-training.) — https://github.com/constantino-garcia/cmmrt

## Examples

```
python cmmrt/rt/train_model.py --storage sqlite:///results/optuna/train.db --save_to saved_models; python -c "from cmmrt.projections import meta_learn_projection; gp_prior = meta_learn_projection(calibration_fps, calibration_rts, dnn_model, n_epochs=100); predictions = gp_prior.predict(test_fps, dnn_model)"
```

## Evaluation signals

- Mean absolute error (MAE) and median absolute error (MdAE) of predicted RTs against reference RTs; expected range ~17–40 s depending on method complexity (paper reports 39.2±1.2 s MAE and 17.2±0.9 s MdAE for best DNN model).
- Projection error should remain competitive with methods trained on larger calibration sets; verify by comparing MAE curves across different calibration set sizes (5, 10, 20, 50 molecules).
- Feature representations extracted from the penultimate DNN layer should cluster calibration molecules by their true chromatographic properties; visualize via t-SNE or UMAP to verify latent space structure.
- Bayesian posterior uncertainty estimates from the meta-learned GP should be well-calibrated: predictions with higher uncertainty should correlate with higher actual errors.
- Cross-validation results on held-out reference chromatographic methods should show consistent performance across different target CMs (e.g., FEM long, LIFE old, FEM orbitrap plasma, RIKEN).

## Limitations

- The approach requires access to alvaDesc software (commercial license) for fingerprint generation; open-source alternatives (e.g., RDKit) may produce different fingerprints and may not reproduce the exact accuracy reported.
- Projection performance degrades when the source and target chromatographic methods differ substantially in retention mechanism or stationary phase chemistry; the meta-learned mapping assumes sufficient distributional overlap.
- The pre-trained DNN must be trained on a large, representative reference dataset (METLIN SMRT: 80,038 RTs); if the pre-trained model's domain does not overlap with the user's compounds, accuracy may suffer.
- Minimal calibration (10 molecules) risks overfitting in the meta-learned GP prior, especially if the 10 molecules are atypical or clustered in chemical space; larger calibration sets (50–100 molecules) are recommended for robust projections.

## Evidence

- [readme] A novel Bayesian meta-learning approach is proposed for RT projection between CMs from as few as 10 molecules while still obtaining competitive error rates compared with previous approaches.: "A novel Bayesian meta-learning approach is proposed for RT projection between CMs from as few as 10 molecules while still obtaining competitive error rates"
- [other] Extract feature representations from the penultimate layer of the pre-trained DNN for calibration and test molecules. Fit a Bayesian meta-learning projection model to learn the mapping from the external chromatographic method's space to the DNN's latent feature space using only the 10 calibration molecules.: "Extract feature representations from the penultimate layer of the pre-trained DNN for calibration and test molecules. Fit a Bayesian meta-learning projection model to learn the mapping"
- [readme] 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software: "5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints) were generated with the alvaDesc software"
- [readme] The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and 17.2 ± 0.9 s: "heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and 17.2 ± 0.9 s"
- [readme] We have trained state-of-the-art machine learning regressors using the 80,038 experimental RTs from the METLIN small molecule dataset (SMRT): "trained state-of-the-art machine learning regressors using the 80,038 experimental RTs from the METLIN small molecule dataset (SMRT)"
