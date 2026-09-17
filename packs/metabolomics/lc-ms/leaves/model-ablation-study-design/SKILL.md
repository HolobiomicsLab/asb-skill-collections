---
name: model-ablation-study-design
description: Use when you need to measure how much a specific model capability or
  architectural feature contributes to prediction performance, especially when that
  capability is non-obvious or orthogonal to baseline methods.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - MIST
  - MIST-CF
  - SIRIUS
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jcim.3c01082
  title: mistcf
evidence_spans:
- an extension of MIST for annotating MS1 precursor masses from MS/MS data
- MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum
  using an end-to-end energy based modeling approach
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mistcf
    doi: 10.1021/acs.jcim.3c01082
    title: mistcf
  dedup_kept_from: coll_mistcf
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jcim.3c01082
  all_source_dois:
  - 10.1021/acs.jcim.3c01082
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# model-ablation-study-design

## Summary

Design and execute controlled ablation studies to isolate the contribution of individual model components (e.g., multi-adduct support, architectural features, input modalities) to overall prediction accuracy. This skill enables quantification of feature importance by comparing performance metrics under systematically restricted model configurations.

## When to use

Apply this skill when you need to measure how much a specific model capability or architectural feature contributes to prediction performance, especially when that capability is non-obvious or orthogonal to baseline methods. Use it to justify design choices, prioritize engineering effort, or validate claims about which components drive accuracy improvements—particularly relevant when integrating multiple novel features (multi-adduct typing, sinusoidal embeddings, instrument covariates) and you must disentangle their individual effects.

## When NOT to use

- Input dataset is small or unbalanced such that metrics are dominated by noise rather than signal—ablation deltas will not be reliable.
- The feature under test cannot be cleanly toggled without retraining the model; if disabling a feature requires retraining, the reported delta conflates the feature's direct contribution with training-time effects.
- Ground truth labels are missing or unreliable, preventing accurate computation of ranking accuracy metrics.

## Inputs

- Published benchmark dataset with MS/MS spectra
- Ground truth annotations (chemical formula, adduct type)
- Trained MIST-CF model with feature flag or configuration to toggle target capability
- Configuration files specifying inference modes (e.g., [M+H]+-only vs. multi-adduct)

## Outputs

- Ranked formula-adduct pair predictions (full mode)
- Ranked formula-adduct pair predictions (restricted/baseline mode)
- Ranking accuracy metrics for each mode (top-1 and top-k accuracy)
- Performance delta report (multi-adduct accuracy minus baseline accuracy)
- Comparison report with metrics and isolated feature contribution

## How to apply

Create two or more model configurations: one with the target feature enabled (full mode) and one or more with it disabled or restricted (baseline modes). Load an identical benchmark dataset with ground-truth annotations (formula, adduct type, or other relevant labels). Run inference on both configurations without retraining, recording identical ranking accuracy metrics (e.g., top-1 and top-k correct formula-adduct pair identification). Compute the performance delta by subtracting baseline accuracy from full-mode accuracy to isolate the contribution of the target feature. Generate a comparison report showing both absolute metrics and the delta; ensure both runs use the same hyperparameters, data splits, and evaluation protocol to ensure fair comparison.

## Related tools

- **MIST-CF** (Neural network model implementing formula ranking and adduct assignment; supports toggling multi-adduct support vs. [M+H]+-only mode for ablation) — https://github.com/samgoldman97/mist-cf
- **SIRIUS** (Baseline tool for formula enumeration; used in comparative benchmarking to contextualize MIST-CF ablation results)

## Examples

```
python src/mist_cf/mist_cf_score/predict.py --model_checkpoint model.pt --test_data data/canopus/test_spectra.mgf --config configs/mist_cf_canopus.yaml --multi_adduct_mode true > full_predictions.json && python src/mist_cf/mist_cf_score/predict.py --model_checkpoint model.pt --test_data data/canopus/test_spectra.mgf --config configs/mist_cf_canopus.yaml --multi_adduct_mode false > baseline_predictions.json && python analysis/evaluate_pred.py --pred_full full_predictions.json --pred_baseline baseline_predictions.json --ground_truth data/canopus/test_labels.json
```

## Evaluation signals

- Both full and restricted model configurations produce predictions on 100% of the test dataset with no errors or missing values.
- Ranking accuracy metrics (top-1, top-k) for the full configuration equal or exceed those of the restricted configuration, confirming the feature provides non-negative contribution.
- Performance delta is consistent across different test splits or cross-validation folds, indicating the contribution is not an artifact of data leakage or overfitting.
- The magnitude of the delta is interpretable and commensurate with the feature's expected impact (e.g., multi-adduct support on a natural products dataset where multiple adduct types are prevalent should show measurable improvement).
- Ablation results are reproducible: re-running the same comparison on the same dataset and model checkpoint yields identical or near-identical deltas.

## Limitations

- Ablation cannot isolate feature interactions—if two features are co-dependent, disabling one may not reflect the true contribution of the other when both are present.
- Inference-only ablation (toggling features without retraining) assumes the model learned to ignore disabled features; this assumption breaks if training involved that feature heavily or if disabled features affect downstream computations.
- Metrics are relative to the chosen benchmark dataset; contributions measured on NPLIB1 may differ on NIST20 or other datasets with different chemical space or instrument characteristics.
- MIST-CF in the paper supports only positive-mode ionization; ablations of negative-mode or other ionization types are not addressed.

## Evidence

- [other] research_question: "What is the performance improvement in chemical formula ranking accuracy when MIST-CF incorporates support for multiple adduct types compared to restricting predictions to [M+H]+ only?"
- [other] methodology_overview: "Run MIST-CF inference in [M+H]+-only mode, restricting the model to rank formulas without multi-adduct support, and record ranked formula predictions and adduct assignments."
- [other] full_configuration_run: "Run MIST-CF inference in full multi-adduct mode using the complete energy-based modeling approach, allowing ranking across multiple positive-mode adduct types, and record ranked predictions."
- [other] metric_computation: "Compute ranking accuracy metrics (top-1 and top-k correct formula-adduct pair identification) for both modes."
- [other] delta_calculation: "Calculate the performance delta (multi-adduct accuracy minus [M+H]+-only accuracy) to isolate MULTI_ADDUCT_SUPPORT contribution and generate a comparison report."
- [readme] architectural_advances: "Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees), Considering multiple adduct types beyond [M+H]+ (still only positive mode), Utilizing"
- [readme] energy_based_approach: "MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases"
