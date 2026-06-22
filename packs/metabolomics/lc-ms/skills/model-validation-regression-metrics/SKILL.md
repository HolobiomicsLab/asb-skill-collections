---
name: model-validation-regression-metrics
description: Use when after training a deep-learning model on paired MS/MS spectra with annotated structural similarity labels, use this skill to assess whether predicted similarity scores correlate with ground-truth reference similarities on data the model has never seen.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - DeepMASS
  - Keras
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.8b05405
  title: Deep MS/MS similarity
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deep_ms_ms_similarity_cq
    doi: 10.1021/acs.analchem.8b05405
    title: Deep MS/MS similarity
  dedup_kept_from: coll_deep_ms_ms_similarity_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.8b05405
  all_source_dois:
  - 10.1021/acs.analchem.8b05405
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Model Validation via Regression Metrics

## Summary

Evaluating deep-learning models trained to predict continuous structural similarity scores between unknown and reference metabolites by computing regression metrics (e.g., Pearson correlation) on held-out test spectra. This skill validates whether the model has learned meaningful structural relationships from MS/MS spectral features.

## When to use

After training a deep-learning model on paired MS/MS spectra with annotated structural similarity labels, use this skill to assess whether predicted similarity scores correlate with ground-truth reference similarities on data the model has never seen. Apply when you need to decide whether the model is ready for ranking candidate metabolite structures in a known-to-unknown identification workflow.

## When NOT to use

- The test set was not held out before model training (use cross-validation instead to avoid data leakage).
- Structural similarity labels are categorical or ordinal rather than continuous (use classification or ranking metrics instead).
- The training and test sets are drawn from the same source database or contain spectrum pairs with identical precursor masses (violates independence assumption).

## Inputs

- held-out test set of paired MS/MS spectra (unknown and known metabolite spectra with metadata)
- annotated structural similarity labels (ground-truth reference scores) for test pairs
- trained deep-learning model weights

## Outputs

- predicted structural similarity scores for each test spectrum pair
- Pearson correlation coefficient between predicted and reference similarities
- regression metrics (e.g., MSE, R², RMSE) quantifying model performance

## How to apply

Partition your annotated MS/MS spectrum pairs into training and held-out test sets before model training. After training, run inference on the test set to generate predicted similarity scores for each unknown–reference spectrum pair. Compute Pearson correlation coefficient between predicted and reference similarity values to quantify the strength of linear agreement. Report the correlation alongside other regression metrics (e.g., mean squared error, R² coefficient of determination) to assess both predictive accuracy and generalization. A high Pearson correlation (typically r > 0.7–0.8 for metabolomics applications) indicates the model has learned robust spectral-to-similarity mappings; lower values suggest the model may be underfitting or the spectral features may be insufficient for reliable similarity prediction.

## Related tools

- **DeepMASS** (trained deep-learning model that predicts structural similarity between unknown and known metabolites from MS/MS spectra; used as the inference engine to generate predicted similarity scores on the test set) — https://github.com/hcji/DeepMASS
- **Keras** (deep learning framework for loading trained model weights and running inference on test spectra)

## Examples

```
from sklearn.metrics import pearsonr; import numpy as np; predicted = model.predict(test_spectra); correlation, pvalue = pearsonr(predicted, test_labels); print(f'Pearson r: {correlation:.3f}, p-value: {pvalue}')
```

## Evaluation signals

- Pearson correlation coefficient between predicted and reference similarities is statistically significant (p < 0.05) and typically > 0.7 for a well-trained model.
- Test-set regression metrics (R², RMSE) are comparable to or better than cross-validation metrics computed during model selection, indicating absence of overfitting.
- Distribution of residuals (predicted − reference) is approximately normal and centered near zero, with no systematic bias across the similarity score range.
- Predicted similarity scores respect expected metabolite chemistry: structurally similar compounds yield higher predictions; unrelated compounds yield lower predictions.
- No catastrophic failure modes: predicted scores remain within the valid range [0, 1] or match the annotation scheme used during training (e.g., 0–100).

## Limitations

- Pearson correlation assumes a linear relationship between predicted and reference scores; non-linear patterns may be missed.
- High correlation on the test set does not guarantee the model will generalize to metabolites from entirely new chemical classes or spectra acquired on different MS/MS instruments.
- The quality of structural similarity labels in the training and test sets directly constrains model performance; noisy or inconsistent annotations will inflate apparent error.
- The README notes that the original experimental spectra (MetDNA dataset) have been removed; validation metrics are therefore difficult to reproduce unless you train on your own in-house database.

## Evidence

- [other] Evaluate model performance on a held-out test set using similarity prediction metrics (e.g., Pearson correlation between predicted and reference similarities).: "Evaluate model performance on a held-out test set using similarity prediction metrics (e.g., Pearson correlation between predicted and reference similarities)."
- [readme] DeepMASS includes a deep-learning based model to predict structural similarity between unknown and known metabolites based on their MS/MS spectra: "DeepMASS includes a deep-learning based model to predict structural similarity between the unknown metabolites and the known ones based on their MS/MS spectra"
- [intro] The deep-learning based model in DeepMASS predicts structural similarity between unknown metabolites and known reference metabolites using MS/MS spectra as input.: "How does the deep-learning based model in DeepMASS predict structural similarity between unknown metabolites and known reference metabolites using MS/MS spectra?"
- [other] Train the model on annotated spectrum pairs with structural similarity labels using supervised learning.: "Train the model on annotated spectrum pairs with structural similarity labels using supervised learning."
- [readme] If you want to train a model based on your in-house database, please put your spectra files into data/spectra directory and run test.py.: "If you want to train a model based on your in-house database, please put your spectra files into data/spectra directory and run test.py."
