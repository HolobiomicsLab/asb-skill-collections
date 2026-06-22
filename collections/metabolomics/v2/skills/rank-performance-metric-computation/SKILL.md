---
name: rank-performance-metric-computation
description: Use when when you have predictions from one or more metabolite annotation models (MLP baseline, GNN, or ESP ensemble) and need to quantify ranking performance on ESI/LC-MS test spectra.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - github.com/HassounLab/ESP
  - ESP ensemble model
  - MLP baseline model (NEIMS)
  - GNN baseline model
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# rank-performance-metric-computation

## Summary

Compute average rank and Rank@K metrics to quantify metabolite annotation model performance on mass spectra test sets. This skill enables comparison of neural network ensemble models (MLP, GNN, ESP) by measuring how highly the correct chemical identity ranks among candidate molecules.

## When to use

When you have predictions from one or more metabolite annotation models (MLP baseline, GNN, or ESP ensemble) and need to quantify ranking performance on ESI/LC-MS test spectra. Use this skill when your goal is to measure and compare the average rank position of the true compound among all candidate molecules, or to report the fraction of predictions where the correct compound appears within the top K positions.

## When NOT to use

- Input is classification scores or probability distributions rather than ranked candidate lists; use a ranking operation first.
- Test spectra do not have verified ground-truth metabolite annotations; metric cannot be computed without known correct identity.
- Candidate set is incomplete or differs between models being compared; results will not be directly comparable.

## Inputs

- Test spectral dataset (ESI/LC-MS spectra with ground-truth metabolite annotations)
- Model predictions on test spectra (ranked list of candidate metabolites per spectrum from one or more models: MLP, GNN, or ESP)
- Candidate set size (e.g., 100 candidate molecules per spectrum)

## Outputs

- Average rank metric (mean position of true compound across test spectra)
- Average rank standard deviation
- Rank@K metrics (fraction of spectra with correct compound in top K, for K=1 to 20)
- Percentage performance gain vs. baseline model ((ESP_rank − MLP_rank) / MLP_rank) × 100)
- Comparison table showing baseline and ensemble metrics side-by-side

## How to apply

After generating predictions from your model(s) on the test spectral dataset, compute the average rank metric by calculating the mean position of the true metabolite across all test spectra. Additionally compute Rank@K metrics for K values (1, 2, 3, ..., 20) by counting the fraction of test spectra where the correct compound ranked at position K or better. Use these metrics to establish baseline performance (e.g., MLP average rank) and then calculate percentage improvement for ensemble models as ((ESP_rank − MLP_rank) / MLP_rank) × 100. The rationale is that lower average rank and higher Rank@K values indicate better annotation performance; ensemble methods that combine MLP and GNN predictions should show measurable improvement over single-model baselines.

## Related tools

- **ESP ensemble model** (Generates weighted average predictions combining MLP and GNN models on test spectra for performance evaluation) — https://github.com/HassounLab/ESP
- **MLP baseline model (NEIMS)** (Generates baseline predictions used as reference for percentage improvement calculation) — https://github.com/HassounLab/ESP
- **GNN baseline model** (Generates alternative baseline predictions for comparison and ensemble aggregation) — https://github.com/HassounLab/ESP

## Examples

```
python train.py --cuda 0 --model mlp --model_file_suffix mlp_can --full_dataset | grep -E 'Average rank|Rank at'
```

## Evaluation signals

- Average rank value is a positive integer ≥ 1; verify it falls within plausible range (typically 1–1000 for full NIST candidate set).
- Average rank standard deviation is non-negative and less than or equal to maximum possible rank value.
- Rank@K metrics are monotonically increasing (Rank@1 ≤ Rank@2 ≤ ... ≤ Rank@20) and bounded in [0, 1].
- Percentage improvement calculation ((ESP_rank − MLP_rank) / MLP_rank) × 100 should be positive for ensemble models; ESP model demonstrates 23.7% improvement over MLP baseline on ESI/LC-MS data as published.
- Test set covers all 819 spectra (or reported test size) with no missing predictions or tied rank positions.

## Limitations

- Metric requires exact ground-truth metabolite identity; does not apply to unannotated or ambiguous spectra.
- Average rank and standard deviation can be heavily influenced by outlier spectra where correct compound ranks very low; median rank or robust statistics may be more interpretable for highly skewed distributions.
- Rank@K metrics depend on candidate set size and composition; results are not directly comparable between studies using different candidate databases (NIST vs. NPLIB1 vs. others).
- Performance gains reported are specific to ESI/LC-MS data; the paper notes that improvements do not generalize to EI/GC-MS spectra.

## Evidence

- [readme] Our results, measured in average rank and Rank@K for the test spectra, show remarkable performance gain over existing neural network approaches.: "Our results, measured in average rank and Rank@K for the test spectra, show remarkable performance gain"
- [other] ESP model achieves a 23.7% increase in average rank performance over the MLP model on ESI/LC-MS data.: "23.7% increase in average rank performance on the full NIST candidate set"
- [other] Calculate the percentage performance gain: ((ESP_rank − MLP_rank) / MLP_rank) × 100, targeting 23.7% improvement.: "((ESP_rank − MLP_rank) / MLP_rank) × 100"
- [readme] Average rank 339.350 +- 1264.715 ... Rank at 1 0.230 ... Rank at 20 0.609: "Average rank 339.350 +- 1264.715 [and] Rank at K metrics reported from 1 to 20"
- [readme] improvements with ESP over the MLP model (implementation of NEIMS model (Wei et al., 2019) with a generalized dataset ESI/LC-MS but not EI/GC-MS data in NEIMS): "improvements with ESP over the MLP model...ESI/LC-MS but not EI/GC-MS data"
