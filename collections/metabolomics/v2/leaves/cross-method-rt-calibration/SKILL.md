---
name: cross-method-rt-calibration
description: Use when when you have predicted retention times from a DNN model trained
  on one chromatographic method (CM) and need to rank or filter metabolite candidates
  on a different chromatographic method, but have only a small set of calibration
  molecules (≥10) with known RTs on both source and target.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0081
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3407
  tools:
  - alvaDesc
  - RDKit
  - cmmrt
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

# cross-method-rt-calibration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

A Bayesian meta-learning approach that projects retention times between different chromatographic methods using minimal calibration data (as few as 10 molecules), enabling accurate RT prediction and metabolite annotation scoring across LC-MS platforms without extensive retraining.

## When to use

When you have predicted retention times from a DNN model trained on one chromatographic method (CM) and need to rank or filter metabolite candidates on a different chromatographic method, but have only a small set of calibration molecules (≥10) with known RTs on both source and target methods.

## When NOT to use

- When you have fewer than 10 calibration molecules with paired RT measurements on both source and target methods—meta-learning requires a minimum viable calibration set.
- When the source and target chromatographic methods are fundamentally incompatible (e.g., reverse-phase vs. ion-exchange with no overlapping chemical space in the calibration set).
- When metabolite annotation is not your end goal—this skill is specifically designed to filter and rank candidates by RT plausibility, not to perform de novo structural elucidation.

## Inputs

- Molecular structures (SMILES, mol, SDF format)
- Pre-trained DNN retention time predictions from source chromatographic method with uncertainty estimates
- Calibration dataset: ≥10 molecules with known experimental retention times on both source and target chromatographic methods
- Target chromatographic method identifier
- Molecular descriptors and fingerprints (ECFP, MACCSFP, PFP)

## Outputs

- Ranked metabolite annotation candidates table
- Projected retention times on target chromatographic method with confidence intervals
- RT prediction errors (observed – predicted) for each candidate
- Annotation scores reflecting RT prediction confidence

## How to apply

Train a Bayesian Gaussian Process meta-learner on the available calibration molecules (minimum 10) to learn a probabilistic mapping between source and target chromatographic method retention times. The GP prior is conditioned on the molecular descriptors/fingerprints and observed RT pairs from the calibration set, enabling prediction of uncertainty-quantified RT values on the target CM. For each metabolite candidate, compute the projected RT and its confidence interval on the target method, then filter and rank candidates by comparing observed versus predicted RT values—retaining only candidates where observed RT falls within the projected uncertainty bounds. The ranking score reflects prediction confidence, with highest-confidence annotations listed first.

## Related tools

- **alvaDesc** (Generate molecular descriptors (5,666) and fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) required for meta-learned projection model training and inference) — https://www.alvascience.com/alvadesc/
- **RDKit** (Generate fingerprints and molecular features as input to DNN retention time predictor and meta-learning model)
- **cmmrt** (Reference implementation of the complete workflow including DNN training, Bayesian meta-learning for RT projection, and metabolite annotation scoring) — https://github.com/constantino-garcia/cmmrt

## Examples

```
python cmmrt/rt/train_model.py --storage sqlite:///results/optuna/train.db --save_to saved_models && python -c "from cmmrt.projections import meta_learn_gp; gp = meta_learn_gp(calibration_mols, source_rts, target_rts); projected_rt, ci = gp.predict(candidate_fingerprints); ranked = candidates[candidates['observed_rt'].between(projected_rt - ci, projected_rt + ci)].sort_values('confidence', ascending=False)"
```

## Evaluation signals

- Projected RT confidence intervals on the target chromatographic method should be narrower and more accurate when trained on larger calibration sets (>10 molecules); median absolute projection error should remain competitive (<60 s) relative to prior work.
- Filtering candidates by the criterion 'observed RT falls within projected confidence bounds' should yield high annotation specificity (low false-positive rate); candidates ranked by descending confidence score should place correct annotations near the top.
- Meta-learned projection should produce consistent RT mappings across multiple independent calibration sets of the same size drawn from the same source/target CM pair (reproducibility check).
- Ranked annotation tables should show monotonic decrease in RT prediction error (|observed – predicted| RT) as you descend the candidate ranking by confidence score.
- The learned GP prior should generalize to unseen molecules with similar chemical properties to the calibration set; out-of-distribution molecules (e.g., very polar or very lipophilic compounds absent from calibration data) should show degraded confidence estimates or wider uncertainty bounds.

## Limitations

- The meta-learning approach requires at least 10 molecules with reliable paired RT measurements on both source and target chromatographic methods; performance degrades below this threshold.
- Projection accuracy depends on the chemical diversity and representativeness of the calibration set; if calibration molecules span a narrow chemical space, projections for structurally dissimilar candidates may be unreliable.
- The DNN retention time predictor itself has a mean absolute error of 39.2±1.2 s on the METLIN dataset; this intrinsic uncertainty propagates into the projected RT and confidence intervals, limiting annotation resolution.
- The Bayesian meta-learning approach assumes that the RT transformation between chromatographic methods is smooth and learnable from the calibration data; incompatible or structurally misaligned methods may violate this assumption.
- Fingerprint and descriptor generation requires the alvaDesc software (under commercial license), which may not be accessible to all practitioners; open-source alternatives (RDKit) are available but were not extensively validated in the original workflow.

## Evidence

- [readme] A novel Bayesian meta-learning approach is proposed for RT projection between CMs from as few as 10 molecules while still obtaining competitive error rates compared with previous approaches.: "A novel Bayesian meta-learning approach is proposed for RT projection between CMs from as few as 10 molecules while still obtaining competitive error rates compared with previous approaches."
- [other] Apply meta-learned Bayesian RT projection to map retention times between source and target chromatographic methods using available calibration molecules (minimum 10 molecules). Score candidate metabolites by computing RT prediction confidence intervals and comparing observed versus predicted RT values, filtering candidates where observed RT falls within the projected uncertainty bounds.: "Apply meta-learned Bayesian RT projection to map retention times between source and target chromatographic methods using available calibration molecules (minimum 10 molecules). Score candidate"
- [readme] The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and 17.2 ± 0.9 s, respectively.: "The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and"
- [readme] We illustrate how the proposed DNN+meta-learned projections can be integrated into a metabolite annotation workflow.: "We illustrate how the proposed DNN+meta-learned projections can be integrated into a metabolite annotation workflow."
- [readme] 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software: "5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software"
