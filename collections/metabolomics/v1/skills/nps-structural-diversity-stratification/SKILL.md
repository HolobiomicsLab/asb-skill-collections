---
name: nps-structural-diversity-stratification
description: Use when you have a trained PS2MS deep learning model, a set of evaluation compounds (especially novel NPS analogues), and want to understand whether prediction confidence (softmax probabilities, uncertainties) degrades gracefully or sharply as structural distance from the training set increases.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2945
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0091
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

# NPS Structural Diversity Stratification

## Summary

Stratify novel psychoactive substance (NPS) evaluation compounds by structural similarity to training data using molecular fingerprints, then aggregate prediction confidence scores by novelty stratum to assess how PS2MS model performance varies across structurally diverse or novel analogues. This reveals whether the deep learning system maintains prediction reliability on truly novel chemical scaffolds versus close structural neighbors.

## When to use

You have a trained PS2MS deep learning model, a set of evaluation compounds (especially novel NPS analogues), and want to understand whether prediction confidence (softmax probabilities, uncertainties) degrades gracefully or sharply as structural distance from the training set increases. Use this skill when you need to validate generalization across chemical space or to identify confidence blind spots in novelty detection.

## When NOT to use

- Training set is not available or fingerprints for training compounds cannot be computed — stratification requires a reference pool to measure similarity against.
- Evaluation compounds lack structural diversity or are all nearly identical to training data — stratification into 'novel' vs. 'similar' bins becomes meaningless.
- Model outputs are not probabilistic (e.g., hard class labels only, no confidence/uncertainty scores) — there is no confidence distribution to aggregate and visualize.

## Inputs

- Trained PS2MS deep learning model (weights and architecture)
- Evaluation dataset with NPS compound structures (SMILES or molecular objects)
- Evaluation dataset with prediction outputs from the model (logits or softmax probabilities)

## Outputs

- Molecular fingerprint representations (ECFP or similar) for all evaluation compounds
- Tanimoto similarity scores comparing each evaluation compound to training set compounds
- Stratification labels ('structurally similar' vs. 'structurally novel') for each compound
- Aggregated confidence score statistics per stratum (mean, median, std, quartiles, range)
- Box plots or violin plots showing confidence distribution by novelty category
- Summary table of score statistics stratified by structural diversity

## How to apply

Load the PS2MS model and evaluation dataset containing NPS analogues. Compute prediction confidence scores (e.g., softmax probabilities or model uncertainty estimates) for each compound using the trained model. Compute molecular fingerprints (e.g., ECFP, Morgan fingerprints) for all evaluation compounds and calculate pairwise Tanimoto similarity against training set compounds to identify the maximum similarity for each analogue. Stratify evaluation compounds into bins based on structural novelty: compounds with high maximum similarity (e.g., ≥0.7) are 'structurally similar'; those with lower similarity (e.g., <0.7) are classified as 'structurally novel'. Aggregate confidence scores within each stratum and compute distributional statistics (mean, median, standard deviation, quartiles, min/max). Visualize the distributions using box plots or violin plots stratified by novelty category to identify any systematic performance degradation on novel structures.

## Related tools

- **RDKit** (Compute molecular fingerprints (ECFP, Morgan) and Tanimoto similarity for stratifying compounds by structural novelty) — https://www.rdkit.org/docs/Install.html
- **PyTorch or TensorFlow** (Load the trained PS2MS deep learning model and extract prediction confidence scores (softmax probabilities or uncertainty estimates))
- **Pandas** (Organize evaluation compounds, fingerprints, similarity scores, and confidence metrics in tabular form; aggregate and group statistics by novelty stratum)
- **Matplotlib or Seaborn** (Generate box plots and violin plots visualizing confidence score distributions stratified by structural novelty category)

## Evaluation signals

- Stratification produces at least two non-empty novelty bins with clear separation in Tanimoto similarity distributions (e.g., median similarity >0.7 for 'similar', <0.5 for 'novel').
- Confidence score statistics are computed without missing values for each stratum; quartiles and extrema are reasonable (probabilities in [0,1], uncertainties non-negative).
- Visualization (box/violin plots) reveals clear visual contrast between strata — e.g., confidence scores lower or more dispersed for 'novel' compounds than 'similar' ones, or vice versa.
- Summary table contains all expected columns (stratum label, count, mean/median/std/min/max confidence) and row counts sum to total evaluation set size.
- No errors in fingerprint computation or Tanimoto similarity calculation; all evaluation and training compounds yield valid ECFP/fingerprint vectors.

## Limitations

- Fingerprint choice (ECFP, Morgan, Tanimoto threshold) is arbitrary; different fingerprints or similarity cutoffs may yield different strata and potentially different confidence profiles. Sensitivity analysis across fingerprint types is advisable.
- The PS2MS system is specifically trained and evaluated on NPS analogues; performance on structurally distant drug scaffolds may be poor regardless of stratification.
- Stratification assumes that structural similarity (via fingerprint Tanimoto) correlates with model confidence; if the model has learned spurious features or has high aleatoric uncertainty, confidence may not track structural novelty reliably.
- No changelog provided in the repository; version stability and reproducibility of model weights over time are unclear.

## Evidence

- [other] How do prediction confidence scores from the PS2MS deep learning model vary across structurally diverse or novel NPS analogues in the evaluation dataset?: "How do prediction confidence scores from the PS2MS deep learning model vary across structurally diverse or novel NPS analogues in the evaluation dataset?"
- [other] Stratify evaluation compounds by structural similarity to training set compounds using molecular fingerprints (e.g., Tanimoto similarity or ECFP) to classify analogues as structurally similar or novel.: "Stratify evaluation compounds by structural similarity to training set compounds using molecular fingerprints (e.g., Tanimoto similarity or ECFP) to classify analogues as structurally similar or"
- [other] Extract or compute prediction confidence scores (e.g., softmax probabilities, prediction uncertainties) for each compound in the evaluation set using the PS2MS model.: "Extract or compute prediction confidence scores (e.g., softmax probabilities, prediction uncertainties) for each compound in the evaluation set using the PS2MS model."
- [other] Aggregate confidence scores by structural novelty stratum and compute distributional statistics (mean, median, std, min, max, quartiles).: "Aggregate confidence scores by structural novelty stratum and compute distributional statistics (mean, median, std, min, max, quartiles)."
- [other] Visualize confidence score distributions across novelty categories using box plots or violin plots and produce a summary table of score statistics stratified by structural diversity.: "Visualize confidence score distributions across novelty categories using box plots or violin plots and produce a summary table of score statistics stratified by structural diversity."
- [readme] PS2MS is designed specifically to address the limitations of identifying the emergence of unidentified novel illicit drugs.: "PS2MS is designed specifically to address the limitations of identifying the emergence of unidentified novel illicit drugs."
- [readme] The system leverages two deep learning tools, NEIMS and DeepEI, to generate mass spectra and chemical fingerprints, respectively.: "The system leverages two deep learning tools, NEIMS and DeepEI, to generate mass spectra and chemical fingerprints, respectively."
