---
name: regression-performance-evaluation
description: Use when after training or fine-tuning a retention time prediction model
  on a source chromatographic method (e.g., SMRT dataset) and you need to verify prediction
  accuracy on a held-out test set or on a target chromatographic method from a different
  dataset (e.g., PredRet).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - torch
  - torch-scatter
  - torch-sparse
  - torch-cluster
  - scikit-learn
  - tqdm
  - pandas
  license_tier: restricted
derived_from:
- doi: 10.1093/bioinformatics/btae084
  title: RT-Transformer
- doi: 10.1038/s41467-019-13680-7
  title: ''
evidence_spans:
- Python 3.9
- torch
- torch-scatter
- torch-sparse
- torch-cluster
- scikit-learn
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rt_transformer_cq
    doi: 10.1093/bioinformatics/btae084
    title: RT-Transformer
  dedup_kept_from: coll_rt_transformer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btae084
  all_source_dois:
  - 10.1093/bioinformatics/btae084
  - 10.1038/s41467-019-13680-7
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# regression-performance-evaluation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Evaluate retention time prediction models by computing regression metrics (MAE, RMSE) on held-out test sets and cross-method datasets to assess generalization and scalability across different chromatographic conditions. This skill ensures that transfer-learned or fine-tuned models are validated with appropriate metrics before deployment.

## When to use

After training or fine-tuning a retention time prediction model on a source chromatographic method (e.g., SMRT dataset) and you need to verify prediction accuracy on a held-out test set or on a target chromatographic method from a different dataset (e.g., PredRet). Use this skill to quantify whether the model generalizes across chromatographic conditions or has learned dataset-specific artifacts.

## When NOT to use

- Model has not yet been trained or fine-tuned; use this skill only after training is complete.
- Test set is not held-out (i.e., molecules were used during training); this will yield overly optimistic metrics and mask overfitting.
- Input molecules lack experimental retention time ground truth; evaluation requires paired predictions and observations.

## Inputs

- trained PyTorch model checkpoint (.pth file)
- test dataset as CSV or PyTorch DataLoader (columns: molecule_id, InChI or SMILES, experimental_rt)
- molecular fingerprints or graph representations (rdkit or torch_geometric tensors)

## Outputs

- CSV table with columns: molecule_id, predicted_rt, experimental_rt, absolute_error
- scalar metrics: mean absolute error (MAE), root mean squared error (RMSE)
- optional: cross-method MAE/RMSE comparison table

## How to apply

Load the trained model checkpoint and the held-out test set (molecules with experimental retention times). Generate predictions for each test molecule using the model. Compute mean absolute error (MAE) and root mean squared error (RMSE) between predicted and experimental retention times using scikit-learn metrics. For cross-method evaluation, repeat this procedure on test molecules from the target chromatographic method to assess transfer learning efficacy. Export results as a CSV table with columns: molecule_id, predicted_rt, experimental_rt, absolute_error. Use MAE and RMSE to judge whether the model meets acceptable accuracy thresholds; values closer to zero indicate better generalization. If the model is being evaluated for transfer learning, compare metrics across source and target methods to detect domain shift.

## Related tools

- **scikit-learn** (compute mean absolute error and root mean squared error metrics; optional: additional regression diagnostics)
- **torch** (load trained model checkpoint and run inference on test set)
- **pandas** (construct and export results CSV table)

## Examples

```
from sklearn.metrics import mean_absolute_error, mean_squared_error; import numpy as np; mae = mean_absolute_error(y_test, y_pred); rmse = np.sqrt(mean_squared_error(y_test, y_pred)); results = pd.DataFrame({'molecule_id': mol_ids, 'predicted_rt': y_pred, 'experimental_rt': y_test, 'absolute_error': np.abs(y_pred - y_test)}); results.to_csv('predictions.csv', index=False); print(f'MAE: {mae:.2f}, RMSE: {rmse:.2f}')
```

## Evaluation signals

- MAE and RMSE values are in the range of 0–30 minutes (domain-typical retention time prediction error); values > 50 indicate poor generalization.
- Absolute error distribution is approximately symmetric around zero with no systematic bias (checked by computing mean of absolute_error column; should be close to MAE).
- Cross-method MAE/RMSE (target chromatographic method) is ≤ 2× source method MAE/RMSE; larger ratios indicate limited transfer learning effectiveness.
- Output CSV contains no NaN or infinite values; all molecule_ids are present and unique.
- Predicted retention times are within the plausible range observed in the training data (e.g., 0–150 minutes for typical LC methods).

## Limitations

- Different chromatographic conditions (column chemistry, mobile phase, temperature) may result in different retention times for the same metabolite, causing target-method metrics to be worse than source metrics even if the model is well-trained.
- Current retention time prediction methods lack sufficient scalability to transfer from one specific chromatographic method to another without fine-tuning; evaluation on a new method may reveal domain shift not captured by source-method metrics.
- MAE and RMSE are sensitive to outliers; a few molecules with very large prediction errors can inflate aggregate metrics. Consider reporting median absolute error or percentile-based intervals for robustness.
- Evaluation on small test sets (< 100 molecules) may yield high variance in metric estimates; bootstrap or k-fold cross-validation is recommended for stable uncertainty quantification.

## Evidence

- [other] Evaluate the transfer-learned model on a held-out test set from the PredRet data and compute cross-method prediction accuracy (e.g., mean absolute error between predicted and experimental retention times).: "Evaluate the transfer-learned model on a held-out test set from the PredRet data and compute cross-method prediction accuracy (e.g., mean absolute error between predicted and experimental retention"
- [other] Train the adapted model on the PredRet dataset using torch with a mean absolute error or root mean squared error loss function, monitoring validation performance with scikit-learn metrics.: "Train the adapted model on the PredRet dataset using torch with a mean absolute error or root mean squared error loss function, monitoring validation performance with scikit-learn metrics."
- [other] Export model weights and generate predictions for test molecules as a CSV table with columns: molecule_id, predicted_rt, experimental_rt, absolute_error.: "Export model weights and generate predictions for test molecules as a CSV table with columns: molecule_id, predicted_rt, experimental_rt, absolute_error."
- [readme] Current retention time prediction methods lack sufficient scalability to transfer from one specific chromatographic method to another: "Current retention time prediction methods lack sufficient scalability to transfer from one specific chromatographic method to another"
- [readme] different chromatographic conditions may result in different retention times for the same metabolite: "different chromatographic conditions may result in different retention times for the same metabolite"
