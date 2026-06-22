---
name: deep-neural-network-latent-space-mapping
description: Use when you have a pre-trained DNN model for retention time prediction and need to adapt it to a new chromatographic method or instrument where you have only 10–20 calibration molecules with known retention times;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
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

# deep-neural-network-latent-space-mapping

## Summary

Extract intermediate feature representations from a pre-trained deep neural network and use them as a latent space onto which external data can be projected via Bayesian meta-learning, enabling rapid calibration-free or minimal-calibration transfer between chromatographic methods.

## When to use

You have a pre-trained DNN model for retention time prediction and need to adapt it to a new chromatographic method or instrument where you have only 10–20 calibration molecules with known retention times; extracting latent representations allows you to learn a lightweight projection mapping rather than retraining the entire network.

## When NOT to use

- No pre-trained model exists or domain-specific fingerprints differ significantly from training data (MACCS166, Extended Connectivity, Path Fingerprints)
- Fewer than 10 calibration molecules are available (meta-learning requires minimum sample complexity)
- Target method is fundamentally incompatible with training data source (e.g., very different stationary phase, mobile phase pH, or temperature regimes)

## Inputs

- Pre-trained DNN model (with architecture and weights)
- Calibration molecule set (10–20 SMILES or molecular structures with experimental retention times from target method)
- Test molecule set (SMILES or SDF/mol structures)
- Fingerprint feature specifications (MACCS166, Extended Connectivity, Path Fingerprints)

## Outputs

- Projected feature vectors in DNN latent space (numeric arrays, one per molecule)
- Predicted retention times for test molecules (seconds)
- Mean and median absolute error metrics

## How to apply

Load a pre-trained DNN (e.g., trained on 80,038 METLIN retention times) and extract feature vectors from its penultimate layer for both calibration molecules (10+ examples with known RTs from the target method) and test molecules. Generate molecular fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) using alvaDesc for all molecules in identical format to training data. Fit a Bayesian meta-learning model (e.g., Gaussian Process with meta-trained prior) on the small calibration set to learn a projection from the external method's space into the DNN's latent feature space. Apply the learned projection to transform test molecules' representations, then pass projected vectors through the DNN's final regression layer to predict retention times. Evaluate by comparing predicted RTs against reference values, computing mean and median absolute errors (expect ~39 s mean absolute error, ~17 s median absolute error if properly calibrated).

## Related tools

- **alvaDesc** (Generate molecular fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) for input molecules prior to latent-space projection) — https://www.alvascience.com/alvadesc/
- **cmmrt** (Reference implementation of DNN training, latent-space extraction, and Bayesian meta-learning for RT projection) — https://github.com/constantino-garcia/cmmrt

## Examples

```
# Using the cmmrt repository workflow:
# 1. Extract latent features and train projection on 10 calibration molecules
from cmmrt.rt.build_data_cmm import generate_vector_fingerprints
from cmmrt.models import load_pretrained_dnn
model = load_pretrained_dnn()
latent_features = model.get_layer('penultimate').predict(fingerprints)
# 2. Fit Bayesian GP meta-learner on calibration set
from cmmrt.projection import BayesianMetaLearner
projector = BayesianMetaLearner()
projector.fit(latent_features[:10], calibration_rts[:10])
# 3. Project test molecules and predict RTs
test_projected = projector.transform(latent_features[10:])
test_rts = model.predict(test_projected)
```

## Evaluation signals

- Latent feature vectors extracted from penultimate DNN layer have consistent dimensionality across all molecules (no NaN or dimension mismatch)
- Projected test molecules lie within the convex hull or principal component variance of calibration molecule projections (no extreme extrapolation)
- Mean absolute error on test set is within ±10 s of the pre-trained model's baseline error (~39.2 s) for well-matched methods
- Median absolute error is ≤20 s, indicating robust central tendency despite outliers
- Bayesian meta-learning posterior uncertainty quantiles narrow as calibration set size increases from 10 to 20+ molecules

## Limitations

- Requires access to pre-trained DNN and alvaDesc (commercial software); fingerprint generation is not trivial without proper molecular structure input
- Bayesian meta-learning assumes that the 10–20 calibration molecules are representative of the test set distribution; poor selection will degrade projections
- Latent-space projection is most effective when source (training) and target (new method) chromatographic spaces are reasonably similar; extreme differences in selectivity or pH may violate transfer assumptions
- Mean absolute error of ~39 s is appropriate for seconds-scale RTs; applicability to very fast (sub-second) or very slow (>1000 s) methods untested
- The method integrates into CEU Mass Mediator but code continues to be developed; reproducibility requires pinning to the 'paper' branch

## Evidence

- [other] Extract feature representations from the penultimate layer of the pre-trained DNN for calibration and test molecules: "Extract feature representations from the penultimate layer of the pre-trained DNN for calibration and test molecules."
- [other] Fit a Bayesian meta-learning projection model to learn the mapping from the external chromatographic method's space to the DNN's latent feature space using only the 10 calibration molecules: "Fit a Bayesian meta-learning projection model to learn the mapping from the external chromatographic method's space to the DNN's latent feature space using only the 10 calibration molecules and their"
- [readme] 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints) were generated with the alvaDesc software: "5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software"
- [readme] The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving mean and median absolute errors of 39.2±1.2 s and 17.2 ± 0.9 s: "The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and"
- [readme] A Bayesian meta-learning approach enables retention time projection between chromatographic methods from as few as 10 molecules while obtaining competitive error rates: "A novel Bayesian meta-learning approach is proposed for RT projection between CMs from as few as 10 molecules while still obtaining competitive error rates compared with previous approaches."
