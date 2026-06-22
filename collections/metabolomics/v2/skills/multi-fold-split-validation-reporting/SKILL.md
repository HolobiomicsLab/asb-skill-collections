---
name: multi-fold-split-validation-reporting
description: Use when when evaluating a spectral embedding or compound identification model on a dataset where the training/test split has already been finalized (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3658
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - PyTorch
  - Python 3.12
  - PyTorch 2.6.0
  - figshare
  - SpecEmbedding
  - SpecEmbedding-Comparison
derived_from:
- doi: 10.1021/acs.analchem.5c02655
  title: SpecEmbedding
- doi: 10.6084/m9.figshare.28876751.v2
  title: ''
evidence_spans:
- Python：3.12
- PyTorch：2.6.0 + CUDA 12.4
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_specembedding_cq
    doi: 10.1021/acs.analchem.5c02655
    title: SpecEmbedding
  dedup_kept_from: coll_specembedding_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c02655
  all_source_dois:
  - 10.1021/acs.analchem.5c02655
  - 10.6084/m9.figshare.28876751.v2
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# multi-fold-split-validation-reporting

## Summary

A structured approach to partitioning spectral test sets into multiple random query/reference splits while preserving the original training set boundary, enabling robust evaluation with uncertainty quantification across folds. This skill ensures reproducibility and fair comparison by reporting results as mean and standard deviation across all partitions.

## When to use

When evaluating a spectral embedding or compound identification model on a dataset where the training/test split has already been finalized (e.g., by a prior team like MSBERT), and you need to assess model robustness and generalization by testing it against multiple independent query/reference partitions of the held-out test set, rather than a single fixed split.

## When NOT to use

- The training/test split has not yet been finalized or is not fixed — multi-fold splitting assumes a stable, upstream-defined training boundary.
- You are designing the initial train/test split for the dataset; this skill applies only after that split is locked.
- The test set is too small (e.g., < 100 samples) to yield k=10 meaningful partitions without excessive noise or statistical instability.

## Inputs

- Pre-cleaned spectral data (GNPS, MoNA, MTBLS1572 format) with original MSBERT training/test split already applied
- Test set partition from the original split
- Random seed(s) or pseudo-random number generator for reproducible partitioning
- Target split ratio (e.g., 80/20 query/reference) and fold count (typically 10)

## Outputs

- k=10 indexed query/reference partition pairs (e.g., 10 separate .msp files or JSON-keyed dictionaries)
- Metadata manifest (partition indices, random seeds, sample counts per fold)
- Model evaluation metrics per fold (e.g., accuracy, mean reciprocal rank)
- Aggregated results: mean and standard deviation of metrics across 10 folds
- Reproducibility archive (scripts, seed log, split ratio documentation) deposited to figshare or equivalent public repository

## How to apply

Fix the original training set and apply random partitioning only to the test set, generating k independent query/reference pairs (typically k=10). For each fold i, randomly split the test set (e.g., 80/20 or 50/50 query/reference ratio) using a distinct random seed, ensuring mutual exclusivity within each fold and no leakage to the training partition. Store each fold's query and reference spectra as separate indexed records (e.g., .msp files or JSON-keyed sets) with accompanying metadata (partition index, seed, sample counts). After running inference on all k folds and computing metrics (e.g., mean reciprocal rank, top-1 accuracy), compute fold-wise means and standard deviations and report both. Validate that all 10 partitions are mutually exclusive within the test set and confirm no test samples appear in the training set before final deposit.

## Related tools

- **Python 3.12** (Primary scripting language for implementing partitioning logic, random seed management, and fold iteration)
- **PyTorch 2.6.0** (Deep learning framework used to train and evaluate the model (SpecEmbedding) across folds)
- **figshare** (Public repository for depositing cleaned data, partitioning scripts, and 10-fold splits for reproducibility) — https://doi.org/10.6084/m9.figshare.28876751.v2
- **SpecEmbedding** (Reference implementation demonstrating multi-fold splitting and evaluation on spectral data) — https://github.com/sword-nan/SpecEmbedding
- **SpecEmbedding-Comparison** (Evaluation harness providing detailed benchmark results and metrics computation across folds) — https://github.com/sword-nan/SpecEmbedding-Comparison

## Examples

```
# Load test set, randomly partition 10 times, store splits with metadata, validate exclusivity, and report mean±std metrics across folds
from SpecEmbedding.utils.clean import read_raw_spectra
import numpy as np

test_data = read_raw_spectra('./test.msp')
for fold_idx in range(10):
    seed = 42 + fold_idx
    np.random.seed(seed)
    query_indices = np.random.choice(len(test_data), size=int(0.8*len(test_data)), replace=False)
    ref_indices = np.setdiff1d(np.arange(len(test_data)), query_indices)
    # Store fold_idx, seed, len(query_indices), len(ref_indices) in metadata
# After evaluation: results_mean = np.mean([fold_metrics]); results_std = np.std([fold_metrics])
```

## Evaluation signals

- All 10 query/reference partition pairs are mutually exclusive: no spectrum appears in more than one fold, and partition sizes sum to 100% of the test set.
- Training set samples are never present in any test partition: verify by checking that training IDs have zero intersection with each fold's query and reference sets.
- Reproducibility metadata (random seeds, split ratio) is correctly recorded and allows deterministic regeneration of the same 10 partitions.
- Metrics are computed for all 10 folds and standard deviation is non-zero (unless all folds yield identical results), indicating proper independent sampling.
- Mean and standard deviation of reported metrics fall within plausible ranges for the task (e.g., top-1 accuracy between 0–1, mean reciprocal rank between 0–1) and standard deviation is typically 1–5% of the mean for stable model performance.

## Limitations

- If the test set is small, 10 folds may result in insufficient samples per fold to produce stable per-fold metrics; consider reducing k or stratifying by compound class.
- Windows systems may encounter numerical instability in cosine similarity computation due to @njit decorators from numba; such decorators must be commented out on Windows platforms.
- The approach assumes the original MSBERT training/test split is valid and representative; if the upstream split is biased or overlaps between train and test, multi-fold splitting of the test set alone will not remedy it.
- Reporting only mean and standard deviation masks potential outlier folds; plotting per-fold distributions or reporting percentiles is recommended for robust interpretation.

## Evidence

- [other] Load the pre-cleaned spectral data (GNPS, MoNA, MTBLS1572) with the original MSBERT training/test split already applied. Extract only the test partition and confirm training split is held fixed.: "Load the pre-cleaned spectral data (GNPS, MoNA, MTBLS1572) with the original MSBERT training/test split already applied. Extract only the test partition and confirm training split is held fixed."
- [other] Randomly re-partition the test set 10 times, each time generating a new query set and reference set pair (e.g., 80/20 or 50/50 split depending on the design).: "Randomly re-partition the test set 10 times, each time generating a new query set and reference set pair (e.g., 80/20 or 50/50 split depending on the design)."
- [other] Store each of the 10 query/reference pairs as separate files (or indexed records) in a structured repository (e.g., separate .msp files or a JSON manifest). Record metadata (partition index, split seed, sample counts for each fold) alongside each partition.: "Store each of the 10 query/reference pairs as separate files (or indexed records) in a structured repository (e.g., separate .msp files or a JSON manifest). Record metadata (partition index, split"
- [other] Validate that all 10 partitions are mutually exclusive within the test set and that no test samples appear in the training set.: "Validate that all 10 partitions are mutually exclusive within the test set and that no test samples appear in the training set."
- [readme] we strictly retained the original training set split used by MSBERT and only applied random splitting to the test sets. Final results are reported as the average and standard deviation across the 10: "we strictly retained the original training set split used by MSBERT and only applied random splitting to the test sets. Final results are reported as the average and standard deviation across the 10"
- [readme] All cleaned data, along with the preprocessing scripts and 10-fold query/reference splits used for evaluation, are available on figshare: "All cleaned data, along with the preprocessing scripts and 10-fold query/reference splits used for evaluation, are available on figshare"
