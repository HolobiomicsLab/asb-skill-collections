---
name: uncertainty-quantification-rt-prediction
description: 'Use when you have trained a DNN retention time predictor and need to rank candidate metabolites for an unknown compound: the DNN outputs both point estimates and uncertainty bounds for each candidate''s RT, and you need to convert these into probabilistic scores that reflect confidence in each.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3957
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
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cmmrt
    doi: 10.1186/s13321-022-00613-8
    title: cmmrt
  dedup_kept_from: coll_cmmrt
schema_version: 0.2.0
---

# uncertainty-quantification-rt-prediction

## Summary

Quantify prediction uncertainty in deep neural network retention time (RT) models and convert those uncertainty bounds into probabilistic likelihood scores for ranking metabolite candidates. This skill enables ranking of candidate annotations by RT-based probability density rather than point estimates alone, improving the reliability of metabolite identification in untargeted mass spectrometry workflows.

## When to use

Apply this skill when you have trained a DNN retention time predictor and need to rank candidate metabolites for an unknown compound: the DNN outputs both point estimates and uncertainty bounds for each candidate's RT, and you need to convert these into probabilistic scores that reflect confidence in each candidate's chromatographic elution position. Essential when integrating RT predictions into metabolite annotation pipelines where false positives must be penalized.

## When NOT to use

- Do not use this skill if you lack a pre-trained DNN or sufficient RT data to train one; the method requires 80,000+ experimental RTs for competitive performance.
- Do not apply this skill to compounds outside the training data's chemical space or RT range; extrapolation beyond the training distribution will yield unreliable uncertainty estimates.
- Do not use this skill as a standalone identification method; RT-based ranking is a filtering or re-ranking step within a broader annotation workflow, not a definitive identifier on its own.

## Inputs

- trained DNN regression model (with weights and architecture)
- candidate metabolite structures (SMILES or InChI format)
- molecular descriptors and fingerprints (MACCS166, Extended Connectivity, Path Fingerprints)
- reference retention times (for model training and validation)

## Outputs

- ranked candidate list with RT point predictions
- probabilistic RT likelihood scores (probability density or normalized Gaussian kernels)
- uncertainty bounds (mean absolute error ± standard error per candidate)

## How to apply

Train a heavily regularized DNN with cosine annealing warm restarts and stochastic weight averaging on a large RT dataset (e.g., METLIN's 80,038 experimental RTs). The trained model predicts both mean RT and uncertainty bounds (achieved mean absolute error 39.2±1.2 s on held-out data). For each candidate metabolite, extract the predicted RT and its associated uncertainty. Convert the prediction uncertainty into a probability density function (e.g., normalized Gaussian kernel centered at the predicted RT with width determined by the model's learned or empirical error distribution). Rank candidates by their RT-based likelihood scores in descending order. Validate that uncertainty estimates are well-calibrated by comparing predicted error bounds against actual residuals on test sets.

## Related tools

- **alvaDesc** (generates 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) for input metabolite structures) — https://www.alvascience.com/alvadesc/
- **cmmrt** (implements DNN training with cosine annealing and stochastic weight averaging, uncertainty quantification, and RT prediction pipeline) — https://github.com/constantino-garcia/cmmrt

## Examples

```
python cmmrt/rt/train_model.py --storage sqlite:///results/optuna/train.db --save_to saved_models; python -c "from cmmrt.rt.predictor import DNNPredictor; model = DNNPredictor.load('saved_models/dnn.pkl'); preds, uncertainties = model.predict_with_uncertainty(['SMILES_string']); scores = [(mu, sigma) for mu, sigma in zip(preds, uncertainties)]"
```

## Evaluation signals

- Calibration of uncertainty: compare predicted error bounds (mean absolute error 39.2±1.2 s) against actual residuals on independent test sets; uncertainty width should be neither overconfident nor overly conservative.
- Rank stability: verify that candidates with high RT probability scores are enriched in true metabolite identities when cross-validated against known standards or ground-truth identifications.
- Error distribution: confirm that median absolute errors (17.2 ± 0.9 s) are consistent with model development results, indicating stable uncertainty estimation across different query spectra.
- Probabilistic calibration: assess that the proportion of true candidates falling within predicted confidence intervals (e.g., 68% within 1σ) matches the expected frequency for well-calibrated Gaussian models.
- Feature attribution: validate that fingerprints (which perform better than descriptors alone) are consistently weighted higher in the DNN's uncertainty estimates.

## Limitations

- The method requires 80,038+ experimental RTs from a relevant database (METLIN SMRT) for training; smaller datasets or different ionization/separation modes may yield unstable uncertainty estimates.
- Uncertainty bounds assume the error distribution is approximately Gaussian (or can be modeled by normalized kernels); highly skewed or multimodal RT prediction errors may violate this assumption.
- The approach is sensitive to chromatographic method: cross-method projection requires ≥10 calibration molecules with known RTs in both source and target methods; sparse calibration data may inflate uncertainty propagation.
- Regularization hyperparameters (cosine annealing, stochastic weight averaging) must be tuned; generic or poorly chosen regularization reduces calibration quality and uncertainty reliability.
- The model is trained on retained molecules and unretained molecules together; performance on boundary cases (very early or very late eluters) is not separately characterized.

## Evidence

- [intro] The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and 17.2 ± 0.9 s respectively: "heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and 17.2 ± 0.9 s"
- [other] Convert projected RTs and prediction uncertainties into RT-based likelihood scores (probability density or normalized Gaussian kernel).: "Convert projected RTs and prediction uncertainties into RT-based likelihood scores (probability density or normalized Gaussian kernel)"
- [readme] A Bayesian meta-learning approach is proposed for RT projection between CMs from as few as 10 molecules while still obtaining competitive error rates compared with previous approaches.: "Bayesian meta-learning approach is proposed for RT projection between CMs from as few as 10 molecules"
- [intro] 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software: "5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints)"
- [readme] Results suggest that fingerprints tend to perform better.: "fingerprints tend to perform better"
