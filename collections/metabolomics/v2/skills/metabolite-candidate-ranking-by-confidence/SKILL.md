---
name: metabolite-candidate-ranking-by-confidence
description: Use when you have a set of candidate metabolites for an unknown compound detected in a liquid chromatography–mass spectrometry (LC-MS) experiment, predicted RTs from a trained DNN model, and access to calibration molecules (minimum 10) that connect your observed chromatographic method to a source.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3680
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
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

# metabolite-candidate-ranking-by-confidence

## Summary

Rank and filter metabolite annotation candidates by computing retention time (RT) prediction confidence intervals and comparing observed versus predicted RT values using a Bayesian meta-learned approach. This skill integrates predicted RTs from a deep neural network with meta-learned chromatographic method projections to produce scored candidate lists suitable for prioritizing follow-up identification work.

## When to use

You have a set of candidate metabolites for an unknown compound detected in a liquid chromatography–mass spectrometry (LC-MS) experiment, predicted RTs from a trained DNN model, and access to calibration molecules (minimum 10) that connect your observed chromatographic method to a source method with known RT predictions. Use this skill to rank candidates by confidence and filter out those whose observed RT falls outside the projected uncertainty bounds.

## When NOT to use

- Calibration molecule set is smaller than 10 molecules; meta-learned RT projection requires minimum 10 molecules to achieve competitive error rates.
- No trained DNN model is available for the target LC-MS method; you must first train or source a pre-trained predictor on a representative dataset (e.g., METLIN SMRT with 80,038 experimental RTs).
- Observed retention time is not measured on the same chromatographic method as the candidate predictions; RT projections are method-specific and cannot reliably extrapolate across incompatible gradient systems or stationary phases.

## Inputs

- molecular structures (SMILES or SDF format) of candidate metabolites
- predicted retention times from pre-trained DNN model for candidates
- observed retention time from LC-MS experiment for unknown compound
- calibration molecule set with experimental RTs in both source and target chromatographic methods (≥10 molecules)
- meta-learned Gaussian Process model trained on PredRet database or local reference CMs

## Outputs

- ranked candidate metabolite table with annotation scores
- RT prediction errors and confidence intervals for each candidate
- filtered candidate list (candidates within projected RT uncertainty bounds)
- metadata on projection quality (number of calibration molecules used, GP posterior variance)

## How to apply

First, load molecular structures and their DNN-predicted retention times (mean absolute error 39.2±1.2 s) for all candidate metabolites. Apply meta-learned Bayesian RT projection to map retention times between source and target chromatographic methods using your calibration molecules. For each candidate, compute a RT prediction confidence interval by fitting a Gaussian Process prior trained on the calibration set. Score each candidate by testing whether the observed RT from your LC-MS experiment falls within the projected uncertainty bounds. Rank annotation candidates in descending order by confidence score (highest confidence first), filtering out candidates where observed RT falls outside the bounds. Output a ranked candidate table with annotation scores, RT prediction errors, and confidence intervals to guide manual validation or downstream MS/MS matching.

## Related tools

- **alvaDesc** (Generate molecular descriptors (5,666) and fingerprints (2,214 including MACCS166, Extended Connectivity, Path Fingerprints) used as input features for the DNN retention time predictor) — https://www.alvascience.com/alvadesc/
- **cmmrt** (Python package implementing the DNN retention time predictor, meta-learned Bayesian RT projection, and candidate ranking workflow; includes pre-trained models and Jupyter notebooks for reproducible integration into metabolite annotation pipelines) — https://github.com/constantino-garcia/cmmrt

## Examples

```
python cmmrt/rt/predict.py --candidates candidates.csv --observed_rt 45.3 --calibration_mols calibration.csv --model saved_models/dnn_blender.pkl --meta_gp saved_models/meta_gp.pkl --output ranked_candidates.csv
```

## Evaluation signals

- Ranked candidates have RT prediction errors within reported DNN performance envelope (mean absolute error 39.2±1.2 s, median absolute error 17.2 ± 0.9 s).
- Confidence intervals for RT projections narrow with increasing number of calibration molecules; variance should decrease monotonically from 10 to ~50 calibration molecules.
- Observed RT of true metabolite falls within top-ranked candidate's projected confidence interval; false positive candidates are filtered (observed RT outside bounds).
- Ranking order is consistent with descending Gaussian Process posterior variance or annotation score; ties or inversions indicate potential GP fitting issues or edge cases near projection boundaries.
- Cross-validation on held-out chromatographic methods (e.g., FEM long, LIFE old, FEM orbitrap plasma, RIKEN) shows that meta-training on other CMs produces error rates comparable to single-method models.

## Limitations

- Requires a pre-trained DNN model and meta-learned Gaussian Process; the approach is not applicable to entirely novel chromatographic methods without calibration data or transfer learning.
- Minimum 10 calibration molecules required for competitive RT projection error rates; sparse calibration scenarios may yield wide confidence intervals that fail to filter false candidates effectively.
- RT prediction accuracy (MAE 39.2 s) means some candidates will have overlapping projected RT windows; this skill ranks but cannot definitively disambiguate candidates with similar predicted retention times without additional orthogonal information (e.g., MS/MS spectra).
- Molecular fingerprints (MACCS166, ECFP, PFP) outperform descriptor-only models; if fingerprints cannot be computed (e.g., due to licensing constraints on alvaDesc), performance degrades substantially.
- Method-specificity of projections means the skill cannot be applied across incompatible chromatographic systems; source and target methods must share sufficient physicochemical correlation for the GP prior to generalize.

## Evidence

- [other] Score candidate metabolites by computing RT prediction confidence intervals and comparing observed versus predicted RT values, filtering candidates where observed RT falls within the projected uncertainty bounds.: "Score candidate metabolites by computing RT prediction confidence intervals and comparing observed versus predicted RT values, filtering candidates where observed RT falls within the projected"
- [other] A Bayesian meta-learning approach enables RT projection between chromatographic methods from as few as 10 molecules while obtaining competitive error rates compared with previous approaches.: "A Bayesian meta-learning approach enables RT projection between chromatographic methods from as few as 10 molecules while obtaining competitive error rates"
- [other] Load molecular structures and their corresponding predicted retention times from the pre-trained DNN model (mean absolute error 39.2±1.2 s).: "Load molecular structures and their corresponding predicted retention times from the pre-trained DNN model (mean absolute error 39.2±1.2 s)."
- [intro] The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and 17.2 ± 0.9 s, respectively: "heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and 17.2 ± 0.9 s"
- [readme] We illustrate how the proposed DNN+meta-learned projections can be integrated into a metabolite annotation workflow.: "We illustrate how the proposed DNN+meta-learned projections can be integrated into a metabolite annotation workflow."
