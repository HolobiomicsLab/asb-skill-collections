---
name: screening-performance-metric-computation
description: Use when after running inference with a pre-trained or fine-tuned NaFM model on a virtual screening dataset (compounds with known bioactivity labels or ground truth), compute screening-specific performance metrics to evaluate retrieval and ranking capability.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
  tools:
  - PyTorch
  - Git
  - NaFM inference.py
  - scikit-learn
derived_from:
- doi: 10.1002/anie.202507483
  title: NA
evidence_spans:
- github.com/TomAIDD/NaFM-Official
- Fork the repository
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nafm_cq
    doi: 10.1002/anie.202507483
    title: NA
  dedup_kept_from: coll_nafm_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/anie.202507483
  all_source_dois:
  - 10.1002/anie.202507483
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# screening-performance-metric-computation

## Summary

Compute ranking, retrieval accuracy, and hit rate metrics on virtual screening predictions from a pre-trained molecular foundation model to validate performance against published benchmarks. This skill quantifies how well NaFM-generated molecular embeddings and predictions identify bioactive compounds in screening tasks.

## When to use

After running inference with a pre-trained or fine-tuned NaFM model on a virtual screening dataset (compounds with known bioactivity labels or ground truth), compute screening-specific performance metrics to evaluate retrieval and ranking capability. Use this skill when you need to measure how effectively the model ranks or retrieves active compounds against decoys, as reported in the NaFM paper's virtual screening evaluation.

## When NOT to use

- Input dataset lacks ground truth bioactivity labels or activity assignments (unsupervised screening cannot compute ground-truth-based metrics).
- Model inference has not yet been run; use this skill only after generating embeddings and predictions via the inference.py script.
- Task is molecular property prediction (regression) rather than binary/multi-class virtual screening; use regression metrics (RMSE, MAE, Pearson r) instead.

## Inputs

- Pre-trained or fine-tuned NaFM model checkpoint (.ckpt file)
- Virtual screening dataset (CSV with SMILES column and bioactivity labels)
- Molecular embeddings or predictions from NaFM inference
- Ground truth bioactivity or activity class labels

## Outputs

- Screening performance metrics (ranking accuracy, AUC-ROC, precision@k, recall@k, hit rates)
- Ranked predictions CSV or JSON file (molecules sorted by predicted score with ground truth)
- Comparison report against published NaFM benchmarks

## How to apply

Load the NaFM model predictions (molecular embeddings and bioactivity scores) and the virtual screening dataset with ground truth labels. Compute metrics such as ranking accuracy (fraction of actives ranked above a threshold), retrieval metrics (e.g., AUC-ROC, precision@k, recall@k), and hit rates at early percentiles of ranked compound lists. The choice of metric depends on the screening task: ranking-based metrics assess how well compounds are ordered, while hit rate (actives recovered in top 1%, 5%, 10%) directly measures practical screening utility. Compare computed metrics against the reported results in the NaFM paper to validate reproduction; disagreement indicates inference pipeline or data processing issues. Save predictions and metrics to output files (CSV or JSON) for full traceability.

## Related tools

- **NaFM inference.py** (Generate molecular embeddings and bioactivity predictions on screening compounds prior to metric computation) — https://github.com/TomAIDD/NaFM-Official
- **PyTorch** (Compute prediction scores and organize embeddings for metric calculation)
- **scikit-learn** (Calculate ranking and retrieval metrics (AUC-ROC, precision, recall, hit rates))

## Examples

```
python inference.py --task classification --downstream-data virtual_screening.csv --checkpoint-path NaFM.ckpt && python -c "from sklearn.metrics import roc_auc_score; import pandas as pd; df = pd.read_csv('NaFM/predictions.csv'); auc = roc_auc_score(df['label'], df['pred_score']); print(f'AUC-ROC: {auc:.4f}')"
```

## Evaluation signals

- Computed metrics (e.g., AUC-ROC, hit rates at 1%, 5%, 10%) match or closely approximate those reported in NaFM paper's virtual screening results section.
- Output CSV/JSON files contain all predictions with compound identifiers, predicted scores, ground truth labels, and rank positions; spot-check that top-ranked compounds are labeled as active.
- Ranking is monotonically decreasing by prediction score; verify no ties or ordering errors in ranked list.
- Hit rate metric values are in valid ranges (e.g., hit_rate_1pct ≤ hit_rate_5pct ≤ hit_rate_10pct ≤ 1.0) and AUC-ROC ∈ [0, 1].
- Dataset size (N compounds tested) and number of actives match the published virtual screening benchmark specification for reproducibility.

## Limitations

- The provided test.py script is described as 'a minimal demonstration template rather than the exact production evaluation pipeline used to generate the benchmark results'; exact reproduction may require parameter tuning or custom metric implementations.
- Virtual screening metrics are task-dependent (ranking vs. retrieval); hit rates and precision@k thresholds must be chosen a priori and reported explicitly.
- Performance is sensitive to train/test data overlap and dataset composition (active/decoy ratio, structural diversity); comparisons across different screening sets may not be directly comparable.
- NaFM was pre-trained on natural product data; application to synthetic screening benchmarks may show reduced performance, as noted in the paper's comparison against models pre-trained on synthetic molecules.

## Evidence

- [other] Compute screening performance metrics (e.g., ranking, retrieval accuracy, or hit rates as reported in the paper).: "Compute screening performance metrics (e.g., ranking, retrieval accuracy, or hit rates as reported in the paper)."
- [readme] Finally, we apply NaFM to virtual screening tasks, showing its potential to provide meaningful molecular representations and facilitate the discovery of novel bioactive compounds.: "Finally, we apply NaFM to virtual screening tasks, showing its potential to provide meaningful molecular representations and facilitate the discovery of novel bioactive compounds."
- [readme] test.py should be regarded as a minimal demonstration template rather than the exact production evaluation pipeline used to generate the benchmark results reported in the paper.: "test.py should be regarded as a minimal demonstration template rather than the exact production evaluation pipeline used to generate the benchmark results reported in the paper."
- [other] Save predictions and metrics to output files for validation against reported results.: "Save predictions and metrics to output files for validation against reported results."
- [readme] most deep learning approaches in natural product research are based on supervised learning tailored to specific downstream tasks: "most deep learning approaches in natural product research are based on supervised learning tailored to specific downstream tasks"
