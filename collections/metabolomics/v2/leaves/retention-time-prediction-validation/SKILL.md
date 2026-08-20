---
name: retention-time-prediction-validation
description: Use when after training a GNN-RT model on preprocessed molecular graph
  data (from Train.py) or after applying transfer learning to an in-house dataset
  (from Transferlearning.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3372
  tools:
  - Python
  - Anaconda
  - PyTorch
  - RDKit
  - Train.py
  - Transferlearning.py
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.0c04071
  title: GNN-RT
evidence_spans:
- Anaconda for python 3.6
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_gnn_rt_cq
    doi: 10.1021/acs.analchem.0c04071
    title: GNN-RT
  dedup_kept_from: coll_gnn_rt_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c04071
  all_source_dois:
  - 10.1021/acs.analchem.0c04071
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# retention-time-prediction-validation

## Summary

Validate a trained GNN-RT model's ability to predict liquid chromatography retention time for small molecules by evaluating prediction accuracy and loss metrics on a held-out validation set. This skill ensures the model generalizes to unseen molecular structures before deployment in structure identification workflows.

## When to use

After training a GNN-RT model on preprocessed molecular graph data (from Train.py) or after applying transfer learning to an in-house dataset (from Transferlearning.py), validate model performance on a held-out validation set drawn from the target database to confirm that predicted retention time values are sufficiently accurate for downstream small molecule structural identification.

## When NOT to use

- Input is a raw spectra file or unpreprocessed molecular database — run Preprocess.py first to generate molecular graphs and standardized labels.
- No held-out validation set is available — the validation set must be independent of the training data to avoid overfitting.
- The goal is to perform transfer learning on a new database — use Transferlearning.py first, then validate on the target database's validation split.
- Retention time prediction is not the intended use case — GNN-RT is specifically designed for LC retention time prediction; other chromatographic or spectroscopic targets require different models.

## Inputs

- Trained GNN-RT model checkpoint (PyTorch .pt or .pth file)
- Preprocessed molecular graph data (graphs with molecular features and topology)
- Held-out validation set with experimental LC retention time labels
- Model configuration file specifying architecture and hyperparameters

## Outputs

- Validation loss metric (e.g., MSE, MAE between predicted and experimental retention times)
- Prediction accuracy scores per sample or aggregate
- Per-sample prediction errors and residuals
- Convergence plot or loss trajectory across validation epochs
- Model performance report documenting suitability for structure identification

## How to apply

Load the trained GNN-RT model checkpoint in PyTorch and evaluate it on a held-out validation set of molecular graphs paired with experimental retention time labels. Compute prediction accuracy and loss metrics (e.g., mean squared error or mean absolute error) across the validation batch. Compare predicted retention time outputs against ground-truth chromatographic retention time measurements from the target dataset. Record both the aggregate loss and per-sample prediction errors to detect systematic bias or outliers. If validation loss is unacceptably high (threshold determined by domain expertise and downstream identification task requirements), retrain with adjusted hyperparameters or acquire additional training data. Validation should occur at each epoch during training to monitor convergence and prevent overfitting.

## Related tools

- **PyTorch** (Load and evaluate trained GNN-RT model checkpoint; compute validation loss and prediction metrics)
- **Python** (Execute validation loop, compute accuracy metrics, and generate performance reports)
- **RDKit** (Validate molecular graph representations and feature extraction in validation dataset)
- **Train.py** (Prerequisite script that produces the trained model checkpoint to be validated) — https://github.com/Qiong-Yang/GNN-RT
- **Transferlearning.py** (Produces fine-tuned model checkpoint on target database that requires validation) — https://github.com/Qiong-Yang/GNN-RT

## Evaluation signals

- Validation loss (MSE or MAE) is computed and reported for every epoch without errors or NaN values.
- Predicted retention time values fall within the plausible range of observed experimental retention times in the validation set (no extreme outliers or out-of-bounds predictions).
- Prediction error distribution is approximately symmetric around zero with no systematic bias (mean residual ≈ 0).
- Validation loss converges or plateaus by the final epoch, indicating the model has learned generalizable patterns; no significant divergence or increase in loss after epoch convergence.
- Per-sample prediction accuracy across the validation set meets domain-specific requirements for small molecule structural identification (threshold determined by application); documented in a performance summary.

## Limitations

- Validation accuracy depends on the quality and representativeness of the held-out validation set; if validation molecules are not chemically diverse or are biased toward the training distribution, reported metrics may not reflect true generalization.
- The GNN-RT model is trained for small molecule LC retention time prediction; validation on non-small-molecule targets or alternative chromatographic modalities may not be valid.
- No changelog is available for the GNN-RT repository, limiting visibility into model version changes and potential breaking changes between releases.
- Validation metrics (accuracy, loss) are task-specific; threshold values for 'acceptable' performance must be defined by the user based on downstream structural identification requirements and are not provided by the article.

## Evidence

- [other] Evaluate the adapted model on a held-out validation set from the target database and record prediction accuracy and loss metrics.: "Evaluate the adapted model on a held-out validation set from the target database and record prediction accuracy and loss metrics."
- [other] Validate model performance on held-out validation set at each epoch.: "Validate model performance on held-out validation set at each epoch."
- [readme] The GNN-RT can obtain the data-driven representations of molecules through the end-to-end learning with GNN, and predict the retention time with the GNN-learned representations.: "The GNN-RT can obtain the data-driven representations of molecules through the end-to-end learning with GNN, and predict the retention time with the GNN-learned representations."
- [readme] the predicted LC retention time of small molecule is not accurate enough for wide adoption in molecular structure: "the predicted LC retention time of small molecule is not accurate enough for wide adoption in molecular structure"
- [readme] GNN-RT method, which is proved to be an effective way to predict small molecule LC retention time and improve the accuracy of structural identification of small molecules: "GNN-RT method, which is proved to be an effective way to predict small molecule LC retention time and improve the accuracy of structural identification of small molecules"
