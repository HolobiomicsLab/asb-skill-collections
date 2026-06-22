---
name: baseline-comparison-analysis
description: Use when when you have trained a candidate model (e.g., an ensemble, a new architecture) and need to demonstrate its advantage over published or reference implementations on the same test data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3809
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3375
  tools:
  - github.com/HassounLab/ESP
  - ESP (Ensembled Spectral Prediction)
  - MLP (NEIMS baseline)
  - GNN baseline
  - PyTorch
  techniques:
  - LC-MS
  - GC-MS
derived_from:
- doi: 10.1093/bioinformatics/btae490
  title: ESP
evidence_spans:
- github.com/HassounLab/ESP
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_esp_cq
    doi: 10.1093/bioinformatics/btae490
    title: ESP
  dedup_kept_from: coll_esp_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btae490
  all_source_dois:
  - 10.1093/bioinformatics/btae490
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# baseline-comparison-analysis

## Summary

Quantitatively compare a novel model's performance against established baseline methods on a standardized test dataset, using consistent evaluation metrics to measure percentage improvement. This skill isolates and validates the contribution of the proposed approach by isolating confounding factors and computing reproducible performance deltas.

## When to use

When you have trained a candidate model (e.g., an ensemble, a new architecture) and need to demonstrate its advantage over published or reference implementations on the same test data. Specifically when the goal is to measure ranking-based metabolite annotation performance or similar IR-style metrics where average rank and Rank@K are the primary signals, and a baseline model's predictions are already available or can be reproduced from published code.

## When NOT to use

- When test data has not been held out — using training or validation data for comparison introduces optimistic bias.
- When baseline and candidate models are evaluated with different hyperparameters, preprocessing pipelines, or data augmentations — this confounds architecture contribution with tuning choices.
- When the baseline model has not been independently reproduced or verified — relying on reported numbers without code verification risks propagating errors or misinterpretation of metrics.

## Inputs

- Baseline model checkpoint (e.g., best_model_mlp_can.pt)
- Candidate model checkpoint (e.g., ESP_can.pt)
- Test spectra dataset (ESI/LC-MS, e.g., NPLIB1 or NIST-20 subset)
- Test candidate set with NIST InChiKey targets

## Outputs

- Average rank metric for baseline model
- Average rank metric for candidate model
- Rank@K curves for both models (k=1 to 20)
- Percentage improvement table (((ESP_rank − MLP_rank) / MLP_rank) × 100)
- Comparison summary (e.g., 23.7% improvement as reported)

## How to apply

Load both the baseline model (e.g., MLP/NEIMS) and the candidate model (e.g., ESP ensemble) from their respective published checkpoints. Apply both models to identical test spectra (ESI/LC-MS dataset in this case) to generate separate prediction rankings. Compute the average rank metric for each model's outputs on the full NIST candidate set. Calculate the percentage improvement as ((ESP_rank − MLP_rank) / MLP_rank) × 100, where lower average rank indicates better performance. Generate a side-by-side comparison table showing both raw metrics (average rank ± std, Rank@K values for k=1 to 20) and the derived percentage gain. Validate that the comparison uses the same hyperparameters, data splits, and evaluation protocol for both models to ensure fair attribution of improvement to the model architecture rather than to configuration differences.

## Related tools

- **ESP (Ensembled Spectral Prediction)** (Candidate ensemble model combining MLP and GNN with multi-tasking and attention for metabolite annotation) — https://github.com/HassounLab/ESP
- **MLP (NEIMS baseline)** (Baseline multi-layer perceptron model for spectral ranking) — https://github.com/HassounLab/ESP
- **GNN baseline** (Graph neural network baseline model for spectral prediction) — https://github.com/HassounLab/ESP
- **PyTorch** (Model checkpoint loading and inference execution)

## Examples

```
python ens_train_canopus.py --cuda 0 --disable_two_step_pred --disable_fingerprint --disable_mt_fingerprint --disable_mt_ontology --correlation_mat_rank 100 --full_dataset --mode 'canopus'
```

## Evaluation signals

- Average rank for MLP baseline on test set matches published baseline performance (e.g., 339.350 ± 1264.715 for NPLIB1).
- Average rank for candidate model (ESP) shows lower rank than baseline, indicating better ranking performance.
- Percentage improvement calculation is mathematically correct: ((ESP_rank − MLP_rank) / MLP_rank) × 100 yields the claimed 23.7% or similar magnitude.
- Rank@K metrics (k=1–20) for candidate model are consistent with or superior to baseline across all k values, showing improved performance at all recall levels.
- Standard deviation and sample counts for average rank are reported, confirming statistical rigor; confidence intervals or significance tests may be employed to verify improvement is not due to random variation.

## Limitations

- Comparison is limited to NPLIB1 public data; models trained on NIST-20 cannot be published due to licensing restrictions, so reproducibility on that dataset is unavailable to external researchers.
- The 23.7% improvement is measured on ESI/LC-MS data only; improvement does not transfer to EI/GC-MS data (as explicitly noted in the README), limiting generalization claims.
- Average rank is sensitive to outliers (high-rank false candidates), so datasets with very large candidate pools may show inflated standard deviations; median rank or trimmed statistics may be more robust in such cases.
- The baseline MLP implementation is a generalized version of the NEIMS model adapted to the NPLIB1 dataset; direct reproduction of the original NEIMS model's performance on its native EI/GC-MS data is not provided for comparison.

## Evidence

- [other] Calculate the percentage improvement as ((ESP_rank − MLP_rank) / MLP_rank) × 100: "Calculate the percentage performance gain: ((ESP_rank − MLP_rank) / MLP_rank) × 100, targeting 23.7% improvement."
- [readme] 23.7% improvement on NPLIB1 test spectra with baseline model: "We have shown improvements with ESP over the MLP model (implementation of NEIMS model (Wei et al., 2019) with a generalized dataset ESI/LC-MS but not EI/GC-MS data in NEIMS), in terms of a 23.7%"
- [other] Load both models and apply to identical test spectra to generate predictions: "Generate predictions on test spectra using the MLP baseline model. 4. Generate predictions on the same test spectra using the ESP ensemble model"
- [other] Compute average rank and Rank@K metrics for both models: "Our results, measured in average rank and Rank@K for the test spectra, show remarkable performance gain over existing neural network approaches."
- [readme] Example baseline MLP output showing average rank 339.350: "Average rank 339.350 +- 1264.715
Rank at 1 0.230
Rank at 2 0.310"
- [readme] Limitation: improvement does not transfer to EI/GC-MS data: "We have shown improvements with ESP over the MLP model (implementation of NEIMS model (Wei et al., 2019) with a generalized dataset ESI/LC-MS but not EI/GC-MS data in NEIMS)"
