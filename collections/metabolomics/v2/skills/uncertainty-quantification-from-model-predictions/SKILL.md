---
name: uncertainty-quantification-from-model-predictions
description: Use when when you have a trained neural network (e.g., a Siamese model
  predicting molecular structural similarity) and need to identify and filter unreliable
  predictions before using them in downstream analysis. Apply this skill when raw
  model performance is suboptimal (~0.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3474
  - http://edamontology.org/topic_0091
  tools:
  - MS2DeepScore
  - RDKit
  - Python
  - scikit-learn
  - Monte-Carlo Dropout
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1186/s13321-021-00558-4
  title: MS2DeepScore
evidence_spans:
- Our MS2DeepScore Python library offers two types of data generators
- To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints
  (2048 bits) to compute structural similarities.
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints
  (2048 bits) to compute structural similarities
- Our MS2DeepScore Python library offers two types of data generators, one which iterates
  over all unique InChIKeys (DataGeneratorAllInchikeys) and one which iterates over
  all spectra and was used for
- Using the t-SNE [28] implementation from scikit-learn [29] we computed two-dimensional
  coordinates
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2deepscore_cq
    doi: 10.1186/s13321-021-00558-4
    title: MS2DeepScore
  dedup_kept_from: coll_ms2deepscore_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-021-00558-4
  all_source_dois:
  - 10.1186/s13321-021-00558-4
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# uncertainty-quantification-from-model-predictions

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Quantify prediction uncertainty for individual neural network outputs using Monte-Carlo Dropout ensemble sampling, enabling selective filtering of low-confidence predictions to improve downstream accuracy metrics. This approach generates multiple stochastic forward passes through a model with dropout enabled at inference time, then aggregates the ensemble predictions to estimate confidence intervals and uncertainty bounds per prediction.

## When to use

When you have a trained neural network (e.g., a Siamese model predicting molecular structural similarity) and need to identify and filter unreliable predictions before using them in downstream analysis. Apply this skill when raw model performance is suboptimal (~0.15 RMSE) and you want to trade recall (discarding ~75% of predictions) for precision (achieving ~0.10 RMSE on retained predictions) by removing high-uncertainty outputs.

## When NOT to use

- When computational budget is extremely constrained; Monte-Carlo Dropout requires N forward passes (10× inference cost in the task example), which scales poorly for real-time prediction at scale.
- When you have no ability to discard predictions; if all inputs must receive a prediction (e.g., in a live diagnostic system without rejection option), uncertainty filtering is not applicable.
- When the model was not trained with dropout enabled; enabling dropout at inference on models without regularization during training may produce unreliable uncertainty estimates.

## Inputs

- Pre-trained neural network model (PyTorch or compatible format)
- Input data (spectrum pairs, molecular graphs, embeddings, etc.) for which predictions are needed
- Reference labels or ground-truth values (e.g., Tanimoto scores from RDKit fingerprints) for validation

## Outputs

- Ensemble of N prediction values per input (e.g., 10 similarity scores per spectrum pair)
- Median prediction per input
- Interquartile range (IQR) per input as uncertainty estimate
- Filtered prediction set after applying IQR threshold
- Evaluation metric (e.g., RMSE, retrieval rate) as a function of IQR threshold
- Plot of RMSE and retention rate versus IQR threshold

## How to apply

Load the pre-trained neural network and enable dropout during inference. For each input (spectrum pair, molecule, etc.), perform N forward passes (e.g., N=10) through the network with dropout active (e.g., dropout rate 0.2) to generate an ensemble of N predictions. Compute the median and interquartile range (IQR) across the ensemble for each input. Apply an IQR threshold (e.g., 0.05–0.15) to filter out predictions where IQR exceeds the threshold, retaining only high-confidence predictions. Compute your evaluation metric (e.g., RMSE against reference labels) on the filtered subset. Incrementally adjust the IQR threshold to find the operating point that balances accuracy gain versus retention rate. This approach converts point predictions into uncertainty-weighted scores that enable adaptive filtering.

## Related tools

- **MS2DeepScore** (Pre-trained Siamese neural network for predicting structural similarity from tandem MS spectra; the model being subjected to Monte-Carlo Dropout uncertainty quantification) — https://github.com/matchms/ms2deepscore
- **Monte-Carlo Dropout** (Inference-time dropout technique enabling stochastic forward passes to approximate Bayesian uncertainty without retraining; core method for generating ensemble predictions)
- **RDKit** (Compute reference Tanimoto scores from Daylight fingerprints (2048 bits) for validation and performance benchmarking against filtered predictions)
- **scikit-learn** (Statistical utilities for aggregating ensemble predictions and computing evaluation metrics (e.g., RMSE))
- **Python** (Programming environment for implementing ensemble sampling loops, IQR calculations, and filtering workflows)

## Examples

```
from ms2deepscore.models import load_model; import numpy as np; model = load_model('ms2deepscore_model.pt'); spectrum_pairs = [...]; predictions = np.array([[model(pair).item() for _ in range(10)] for pair in spectrum_pairs]); iqr = np.percentile(predictions, 75, axis=1) - np.percentile(predictions, 25, axis=1); filtered = predictions[iqr < 0.10]; rmse = np.sqrt(np.mean((filtered - ground_truth) ** 2))
```

## Evaluation signals

- Verify that IQR values increase monotonically or are distributed across a reasonable range (e.g., 0.01–0.20) when computed from 10 ensemble members; IQR should capture dispersion in predictions.
- Check that RMSE improves (decreases) monotonically as IQR threshold is tightened (e.g., RMSE ~0.17 → ~0.11 as threshold increases from 0 to 0.15), confirming that higher uncertainty predictions are indeed lower quality.
- Confirm that retention rate (fraction of predictions not filtered out) decreases as IQR threshold tightens (e.g., 100% retention at threshold 0.0 → ~25% retention at threshold 0.15), validating the filtering mechanism.
- Validate that ensemble predictions converge as N increases; spot-check a subset of predictions with N=10 vs. N=20 to ensure the 10-pass ensemble adequately captures uncertainty.
- Cross-validate that reference labels (e.g., Tanimoto scores from RDKit fingerprints) are correctly computed and aligned to predictions before RMSE calculation; a sanity check is that baseline RMSE without filtering matches the paper's reported ~0.15.

## Limitations

- Monte-Carlo Dropout requires enabling dropout at inference time; this assumes the model was regularized with dropout during training, otherwise dropout layers may not encode meaningful uncertainty.
- Computational cost scales linearly with ensemble size (N); the task example uses N=10 forward passes, multiplying inference latency ~10-fold, which limits applicability to real-time or large-scale batch scenarios.
- IQR-based filtering is a crude proxy for uncertainty; it assumes that dispersion across stochastic forward passes correlates with prediction error, which may not hold for all model architectures or data domains.
- The choice of IQR threshold (e.g., 0.05 vs. 0.15) is task-specific and must be tuned empirically; there is no universal threshold, and overfitting to a validation set is a risk.
- The paper does not explore uncertainty calibration; there is no guarantee that predicted IQR matches actual prediction error rates, so miscalibration could lead to overconfident filtering decisions.
- Filtering predictions reduces the available dataset for downstream analysis (e.g., ~75% discarded in the task example), which may bias results if discarded spectra have systematic properties (e.g., rarer compounds, lower-intensity MS/MS patterns).

## Evidence

- [other] For each spectrum pair, enable dropout during inference and generate N=10 forward passes through the network with dropout rate 0.2 to create an ensemble of 200-dimensional spectral embeddings.: "For each spectrum pair, enable dropout during inference and generate N=10 forward passes through the network with dropout rate 0.2 to create an ensemble"
- [other] Compute the median and interquartile range (IQR) across the 10 predictions for each pair.: "Compute the median and interquartile range (IQR) across the 10 predictions for each pair."
- [other] Filter predictions by incrementally raising the IQR threshold (e.g., discarding predictions with IQR above 0.05, 0.10, 0.15, etc.) and compute RMSE against reference Tanimoto scores for each threshold.: "Filter predictions by incrementally raising the IQR threshold (e.g., discarding predictions with IQR above 0.05, 0.10, 0.15, etc.) and compute RMSE"
- [other] Monte-Carlo Dropout ensemble predictions with IQR-based filtering reduce average RMSE from ~0.17 to ~0.11 by discarding ~75% of predictions with highest uncertainty, demonstrating that strong uncertainty restrictions achieve near 0.1 RMSE on the test set.: "Monte-Carlo Dropout ensemble predictions with IQR-based filtering reduce average RMSE from ~0.17 to ~0.11 by discarding ~75% of predictions with highest uncertainty"
- [methods] To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles. At inference time, dropout was applied to all but the first layer of the base network: "To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles. At inference time, dropout was applied to all but the first layer"
- [intro] MS2DeepScore achieves a root mean squared error for predicted Tanimoto scores of about 0.15 when run without uncertainty restrictions, and down to 0.1 with stronger restrictions on model uncertainty: "MS2DeepScore achieves a root mean squared error for predicted Tanimoto scores of about 0.15 when run without uncertainty restrictions, and down to 0.1"
- [readme] In addition to the prediction of a structural similarity, MS2DeepScore can also make use of an embedding evaluator predict the models accuracy for each spectrum.: "MS2DeepScore can also make use of an embedding evaluator predict the models accuracy for each spectrum."
