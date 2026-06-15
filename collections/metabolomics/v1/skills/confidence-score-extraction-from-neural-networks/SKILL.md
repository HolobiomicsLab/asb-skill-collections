---
name: confidence-score-extraction-from-neural-networks
description: Use when when you have a trained deep learning model (e.g., PS2MS) and an evaluation dataset of compounds, and you need to assess how prediction confidence varies across structural novelty classes (e.g., training-similar vs. structurally novel NPS analogues).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3474
  - http://edamontology.org/topic_0091
  tools:
  - Matplotlib or Seaborn for visualization
  - PyTorch or TensorFlow
  - RDKit
  - Pandas
  - Matplotlib or Seaborn
  - PS2MS
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

# confidence-score-extraction-from-neural-networks

## Summary

Extract prediction confidence scores (softmax probabilities, prediction uncertainties) from a trained deep learning model to quantify model certainty across test compounds. This enables downstream stratification and statistical assessment of prediction reliability, especially for novel or out-of-distribution analogues.

## When to use

When you have a trained deep learning model (e.g., PS2MS) and an evaluation dataset of compounds, and you need to assess how prediction confidence varies across structural novelty classes (e.g., training-similar vs. structurally novel NPS analogues). Use this skill when your analysis goal is to understand model generalization or detect compounds for which the model has low confidence.

## When NOT to use

- Input is already a feature table or pre-computed confidence score matrix—skip directly to stratification and visualization.
- The evaluation dataset is small (< 10 samples) or lacks structural diversity; stratification by novelty will be unreliable.
- The model is non-probabilistic or does not expose confidence/uncertainty estimates (e.g., deterministic distance metrics without calibration).

## Inputs

- trained deep learning model weights (PyTorch or TensorFlow checkpoint)
- evaluation dataset of chemical compounds (formatted for model input, e.g., mass spectra, molecular fingerprints, or SMILES strings)
- optional: molecular fingerprints (ECFP, RDKit) or SMILES for structural novelty computation

## Outputs

- prediction confidence scores (softmax probabilities or model-specific uncertainty estimates) for each compound
- confidence score statistics aggregated by structural novelty stratum (mean, median, std, quartiles, min, max)
- visualization (box plots, violin plots) of confidence distributions across novelty classes
- summary table of score statistics stratified by structural diversity

## How to apply

Load the trained deep learning model weights and evaluation dataset. Pass each compound through the model's forward inference pipeline (without backpropagation) to obtain raw logits or softmax outputs. For classification tasks, extract the softmax probability vector; for regression or embedding-based similarity tasks (like PS2MS fingerprint matching), extract model-specific confidence measures such as prediction uncertainty or integrated similarity scores. Compute distributional statistics (mean, median, standard deviation, quartiles, min/max) of confidence scores. Optionally stratify compounds by structural novelty using molecular fingerprints (e.g., Tanimoto similarity to training set) and aggregate confidence statistics by novelty stratum to reveal whether the model exhibits systematic under- or over-confidence on novel structures.

## Related tools

- **PyTorch or TensorFlow** (deep learning framework for model loading, inference, and softmax probability extraction)
- **RDKit** (cheminformatics library for computing molecular fingerprints (ECFP, Tanimoto similarity) to stratify compounds by structural novelty) — https://www.rdkit.org/
- **Pandas** (tabular data manipulation and aggregation of confidence scores by structural novelty stratum)
- **Matplotlib or Seaborn** (visualization of confidence score distributions (box plots, violin plots) across novelty categories)
- **PS2MS** (source deep learning model for NPS detection; provides trained weights and evaluation dataset) — https://github.com/jhhung/PS2MS

## Evaluation signals

- Confidence scores lie in the expected range (0–1 for softmax probabilities; verify no NaN or infinite values)
- Score distributions show lower mean confidence for structurally novel compounds vs. training-similar compounds (monotonic or bimodal pattern indicates model learned meaningful novelty signal)
- Summary statistics table is complete and matches the shape of the evaluation dataset (no missing rows)
- Visualization reveals no pathological patterns (e.g., all scores near 1.0 or 0.0, which suggest uncalibrated or degenerate models)
- Stratification by structural similarity (Tanimoto threshold) cleanly separates novelty classes with non-overlapping or well-separated quartile ranges

## Limitations

- Softmax probabilities alone do not quantify true uncertainty; model may be overconfident on out-of-distribution data. Consider ensemble methods or calibration techniques for more robust uncertainty.
- Structural novelty is measured by molecular fingerprint similarity (e.g., Tanimoto on ECFP); novelty definitions are relative to training set and fingerprint choice. Different fingerprints or similarity metrics may yield different stratifications.
- Confidence scores reflect training data distribution and model architecture; poor generalization or inadequate training data for novel NPS analogues will produce unreliable confidence signals.
- No changelog or version tracking is available for the PS2MS model weights in the README, making reproducibility and cross-study comparison difficult.

## Evidence

- [other] Extract or compute prediction confidence scores (e.g., softmax probabilities, prediction uncertainties) for each compound in the evaluation set using the PS2MS model.: "Extract or compute prediction confidence scores (e.g., softmax probabilities, prediction uncertainties)"
- [other] Stratify evaluation compounds by structural similarity to training set compounds using molecular fingerprints (e.g., Tanimoto similarity or ECFP) to classify analogues as structurally similar or novel.: "Stratify evaluation compounds by structural similarity to training set compounds using molecular fingerprints (e.g., Tanimoto similarity or ECFP)"
- [other] Aggregate confidence scores by structural novelty stratum and compute distributional statistics (mean, median, std, min, max, quartiles).: "Aggregate confidence scores by structural novelty stratum and compute distributional statistics (mean, median, std, min, max, quartiles)"
- [readme] PS2MS is designed specifically to address the limitations of identifying the emergence of unidentified novel illicit drugs.: "PS2MS is designed specifically to address the limitations of identifying the emergence of unidentified novel illicit drugs"
- [readme] The system will compare the spectrum and chemical fingerprint between compounds and generate a list of the hundred most similar compounds which are ranked by similarity score.: "The system will compare the spectrum and chemical fingerprint between compounds and generate a list of the hundred most similar compounds which are ranked by similarity score"
