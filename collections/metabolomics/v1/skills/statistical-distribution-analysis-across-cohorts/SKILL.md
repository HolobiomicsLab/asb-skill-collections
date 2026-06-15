---
name: statistical-distribution-analysis-across-cohorts
description: Use when when you have prediction scores (softmax probabilities, uncertainties) from a trained deep learning model evaluated on a heterogeneous dataset and you need to determine whether prediction confidence or accuracy varies systematically across structurally distinct or novel compound.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - Matplotlib or Seaborn for visualization
  - RDKit
  - PyTorch or TensorFlow
  - Pandas
  - Matplotlib or Seaborn
derived_from:
- doi: 10.1021/acs.analchem.3c05019
  title: ps2ms
evidence_spans:
- prediction confidence scores vary across
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ps2ms
    doi: 10.1021/acs.analchem.3c05019
    title: ps2ms
  dedup_kept_from: coll_ps2ms
schema_version: 0.2.0
---

# Statistical Distribution Analysis Across Cohorts

## Summary

Stratify a model's prediction outputs (confidence scores, uncertainties) by a categorical grouping variable (e.g., structural novelty, compound class) and compute and visualize distributional statistics to reveal how model behavior varies across cohorts. This skill enables detection of systematic prediction bias or confidence degradation in out-of-distribution or novel compound subsets.

## When to use

When you have prediction scores (softmax probabilities, uncertainties) from a trained deep learning model evaluated on a heterogeneous dataset and you need to determine whether prediction confidence or accuracy varies systematically across structurally distinct or novel compound subsets—particularly when the training set may underrepresent novel analogues or out-of-distribution samples.

## When NOT to use

- Input is a single homogeneous cohort with no meaningful stratification variable—stratification requires at least two distinct groups with meaningful separation.
- Prediction scores are already aggregated or binned; you need access to per-sample confidence values to compute distributional statistics.
- The evaluation dataset lacks structural annotations or similarity metrics needed to define cohort membership.

## Inputs

- Trained deep learning model with saved weights
- Evaluation dataset of compounds with mass spectrometry data and structural annotations
- Pre-computed prediction confidence scores or model output layer activations (softmax probabilities, logits, or uncertainty estimates)
- Molecular fingerprints (e.g., ECFP) or precomputed structural similarity metrics for test compounds relative to training set

## Outputs

- Stratification labels for each evaluation compound (cohort membership: structurally similar, structurally novel, etc.)
- Summary statistics table with per-cohort metrics (mean, median, std, min, max, quartiles of confidence scores)
- Distribution visualizations (box plots, violin plots) showing confidence score ranges by structural novelty stratum
- Statistical comparison results (e.g., effect size, p-values if comparing cohort means)

## How to apply

First, compute a stratification variable (e.g., Tanimoto similarity between each test compound and the training set) to classify compounds into cohorts (structurally similar, structurally novel, etc.). Second, extract prediction confidence scores (e.g., softmax probabilities or model uncertainties) for each compound in the evaluation set. Third, aggregate confidence scores within each cohort and compute distributional statistics (mean, median, standard deviation, quartiles, min/max). Fourth, visualize distributions using box plots or violin plots to compare cohort-level patterns. This approach reveals whether the model exhibits lower confidence or higher prediction uncertainty on truly novel structures, which is critical for assessing generalization to emerging novel psychoactive substance analogues.

## Related tools

- **RDKit** (Compute molecular fingerprints (ECFP) and Tanimoto similarity for structural stratification) — https://www.rdkit.org/docs/Install.html
- **PyTorch or TensorFlow** (Load trained model weights and extract prediction confidence scores (softmax probabilities, logits) from the deep learning model)
- **Pandas** (Aggregate confidence scores by cohort membership and compute stratified summary statistics)
- **Matplotlib or Seaborn** (Generate box plots and violin plots for cohort-wise distribution visualization)

## Examples

```
# Load model, extract softmax confidence scores, compute Tanimoto similarity to training set, stratify evaluation compounds, and visualize:
import torch; import pandas as pd; from rdkit import Chem; from rdkit.DataStructs import TanimotoSimilarity; import matplotlib.pyplot as plt; model.eval(); scores = torch.softmax(model(test_data), dim=1).max(dim=1).values.numpy(); similarities = [max([TanimotoSimilarity(fp_test, fp_train) for fp_train in training_fps]) for fp_test in test_fps]; cohorts = pd.DataFrame({'score': scores, 'tanimoto_max': similarities, 'cohort': ['novel' if s <= 0.7 else 'similar' for s in similarities]}); stats = cohorts.groupby('cohort')['score'].describe(); plt.figure(); cohorts.boxplot(column='score', by='cohort'); plt.show()
```

## Evaluation signals

- Summary statistics table is non-empty and contains per-cohort metrics (mean, median, std, min, max, quartiles); check that row count matches number of cohorts and column names match requested metrics.
- Box plot or violin plot displays visually distinct distribution shapes across cohorts; verify that cohort labels on x-axis match stratification variable and confidence scores on y-axis fall within model output range (e.g., 0–1 for softmax probabilities).
- Distributional statistics show measurable differences (e.g., mean confidence in novel cohort is lower than in training-similar cohort), supporting the hypothesis that model confidence degrades on out-of-distribution samples.
- No missing or NaN values in confidence score columns after stratification; verify that all evaluation compounds were assigned a cohort label and have valid predictions.
- Stratification variable (e.g., Tanimoto similarity thresholds) is clearly documented and reproducible; confirm that threshold choices (e.g., > 0.7 = similar, ≤ 0.7 = novel) are justified and applied consistently.

## Limitations

- Stratification accuracy depends on the choice of molecular fingerprint (ECFP, Morgan fingerprints, etc.) and similarity threshold; suboptimal choices may misclassify structurally novel compounds as similar or vice versa.
- Confidence scores (softmax probabilities) can be poorly calibrated, especially on out-of-distribution data; low confidence in the novel cohort may reflect dataset bias rather than true model uncertainty.
- Small sample sizes in the novel cohort may yield unstable summary statistics and limit statistical power for cohort comparisons.
- The skill assumes prediction scores are available; if the model does not expose confidence estimates (e.g., only hard class labels), uncertainty must be inferred via alternative methods (e.g., ensemble disagreement, dropout-based MC dropout).

## Evidence

- [other] Extract or compute prediction confidence scores (e.g., softmax probabilities, prediction uncertainties) for each compound in the evaluation set using the PS2MS model.: "Extract or compute prediction confidence scores (e.g., softmax probabilities, prediction uncertainties) for each compound in the evaluation set using the PS2MS model."
- [other] Stratify evaluation compounds by structural similarity to training set compounds using molecular fingerprints (e.g., Tanimoto similarity or ECFP) to classify analogues as structurally similar or novel.: "Stratify evaluation compounds by structural similarity to training set compounds using molecular fingerprints (e.g., Tanimoto similarity or ECFP) to classify analogues as structurally similar or"
- [other] Aggregate confidence scores by structural novelty stratum and compute distributional statistics (mean, median, std, min, max, quartiles).: "Aggregate confidence scores by structural novelty stratum and compute distributional statistics (mean, median, std, min, max, quartiles)."
- [other] Visualize confidence score distributions across novelty categories using box plots or violin plots and produce a summary table of score statistics stratified by structural diversity.: "Visualize confidence score distributions across novelty categories using box plots or violin plots and produce a summary table of score statistics stratified by structural diversity."
- [readme] PS2MS is designed specifically to address the limitations of identifying the emergence of unidentified novel illicit drugs.: "PS2MS is designed specifically to address the limitations of identifying the emergence of unidentified novel illicit drugs."
