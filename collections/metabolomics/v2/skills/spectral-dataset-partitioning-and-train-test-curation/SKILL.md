---
name: spectral-dataset-partitioning-and-train-test-curation
description: Use when when you have a pre-cleaned spectral library (e.g., GNPS, MoNA, or MTBLS1572) with an existing training/test boundary established by prior work (e.g., MSBERT), and you need to report model performance with uncertainty quantification across multiple random partitions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3359
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - PyTorch
  - Python 3.12
  - PyTorch 2.6.0 with CUDA 12.4
  - numba
  - figshare
  - SpecEmbedding
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
---

# spectral-dataset-partitioning-and-train-test-curation

## Summary

Implements reproducible 10-fold cross-validation on MS/MS spectral test sets while preserving the original upstream training split, enabling robust evaluation with reported average and standard deviation metrics across partitions. This skill ensures fair comparison by decoupling data curation (which determines the training set) from evaluation methodology (which applies random splitting only to test data).

## When to use

When you have a pre-cleaned spectral library (e.g., GNPS, MoNA, or MTBLS1572) with an existing training/test boundary established by prior work (e.g., MSBERT), and you need to report model performance with uncertainty quantification across multiple random partitions. Use this skill when reproducibility and statistical rigor require you to hold the training set constant while varying only the test-set query/reference splits.

## When NOT to use

- The training/test split boundary is not already defined or trusted — curate and validate the upstream split first before applying this skill.
- You need to perform k-fold cross-validation that reshuffles the entire dataset (including training data) — this skill only re-partitions the test set.
- The spectral library lacks sufficient metadata (SMILES, compound identifiers) or quality — perform data cleaning and validation (e.g., removal of malformed SMILES) before invoking this skill.

## Inputs

- Pre-cleaned spectral library (MS/MS data) with original training/test split already applied (e.g., .msp or JSON format)
- Metadata defining the original training/test boundary (e.g., split seed, sample counts)
- Specification of desired query/reference split ratio (e.g., 80/20, 50/50)

## Outputs

- 10 indexed query/reference partition pairs (e.g., 10 × .msp file pairs or JSON manifest with 10 partition records)
- Partition metadata file (CSV or JSON) recording partition index, random seed, query sample count, reference sample count for each fold
- Reproducibility manifest (JSON or YAML) documenting random seeds, split ratios, validation checksums, and sample counts
- Deposited dataset on figshare (or equivalent) with all 10 partitions and metadata

## How to apply

Load the pre-cleaned spectral data with the original training/test split already applied (e.g., from MSBERT preprocessing). Extract only the test partition and confirm the training split is held fixed. Randomly re-partition the test set 10 times using a seeded random number generator, each time generating a new query set and reference set pair (e.g., 80/20 or 50/50 split). Store each of the 10 query/reference pairs as separate files (e.g., .msp files or indexed records) with metadata (partition index, random seed, sample counts per fold). Validate that all 10 partitions are mutually exclusive within the test set and that no test samples leak into the training set. Record random seeds and split ratios alongside each partition for reproducibility. Deposit the complete set of 10 partitions to a persistent repository (e.g., figshare) and report final model metrics as mean ± standard deviation across the 10 folds.

## Related tools

- **Python 3.12** (Primary scripting language for loading, partitioning, validating, and serializing spectral data)
- **PyTorch 2.6.0 with CUDA 12.4** (GPU acceleration for model inference and embedding generation during evaluation on partitioned test sets)
- **numba** (JIT compilation of cosine similarity and other numerical operations; @njit decorators may require tuning on Windows platforms)
- **figshare** (Persistent repository for depositing and versioning all 10 partitions, reproducibility metadata, and preprocessing scripts) — https://doi.org/10.6084/m9.figshare.28876751.v2
- **SpecEmbedding** (Reference implementation demonstrating 10-fold partitioning workflow and evaluation on GNPS, MoNA, MTBLS1572) — https://github.com/sword-nan/SpecEmbedding

## Examples

```
```python
from SpecEmbedding.utils.clean import read_raw_spectra
import random

# Load pre-cleaned data with original MSBERT training/test split
test_spectra = read_raw_spectra('./test_set.msp')
train_spectra = read_raw_spectra('./train_set.msp')

# Generate 10 random query/reference partitions
for fold in range(10):
    random.seed(fold)  # Ensure reproducibility
    shuffled = random.sample(test_spectra, len(test_spectra))
    split_idx = int(0.8 * len(shuffled))  # 80/20 split
    query_fold = shuffled[:split_idx]
    ref_fold = shuffled[split_idx:]
    # Save fold with metadata
    save_partition(query_fold, ref_fold, fold_index=fold, seed=fold)
```
```

## Evaluation signals

- All 10 partitions are mutually exclusive within the test set (no sample appears in multiple partitions), verified by checking union of all 10 partition indices equals full test set and pairwise intersections are empty.
- No test samples appear in the training set (i.e., training set sample IDs and test set sample IDs are disjoint).
- Random seeds are recorded and identical seeds reproducibly generate identical partitions when re-run.
- Sample counts per partition match expected split ratios (e.g., if split is 80/20, query count ≈ 0.8 × total test samples, reference count ≈ 0.2 × total test samples).
- Metadata files (partition manifest, reproducibility record) are human-readable and deposited alongside data, and figshare version history tracks all iterations.

## Limitations

- Skill assumes upstream training/test split is valid and trustworthy; if the original split was biased or contaminated, this skill will propagate that error.
- Random splitting is applied only to test data; training set remains fixed. If the training set is too small or imbalanced, this does not address that problem.
- On Windows platforms, @njit decorators from numba may introduce numerical errors in cosine similarity computation; users must manually comment out @njit decorators or run on Linux.
- Partitions must be stored and versioned carefully; loss of metadata (random seeds, split ratios) renders reproduction impossible.

## Evidence

- [other] The evaluation methodology retains the original training set split from MSBERT while applying random splitting only to test sets, generating 10 distinct query/reference partitions for evaluation and reporting results as average and standard deviation across the 10 splits.: "The evaluation methodology retains the original training set split from MSBERT while applying random splitting only to test sets, generating 10 distinct query/reference partitions for evaluation and"
- [readme] we strictly retained the original training set split used by MSBERT and only applied random splitting to the test sets. Final results are reported as the average and standard deviation across the 10: "we strictly retained the original training set split used by MSBERT and only applied random splitting to the test sets. Final results are reported as the average and standard deviation across the 10"
- [readme] All cleaned data, along with the preprocessing scripts and 10-fold query/reference splits used for evaluation, are available on figshare: "All cleaned data, along with the preprocessing scripts and 10-fold query/reference splits used for evaluation, are available on figshare"
- [other] Extract only the test partition and confirm training split is held fixed. Randomly re-partition the test set 10 times, each time generating a new query set and reference set pair (e.g., 80/20 or 50/50 split depending on the design).: "Extract only the test partition and confirm training split is held fixed. Randomly re-partition the test set 10 times, each time generating a new query set and reference set pair (e.g., 80/20 or"
- [other] Validate that all 10 partitions are mutually exclusive within the test set and that no test samples appear in the training set.: "Validate that all 10 partitions are mutually exclusive within the test set and that no test samples appear in the training set."
- [other] Record metadata (partition index, split seed, sample counts for each fold) alongside each partition.: "Record metadata (partition index, split seed, sample counts for each fold) alongside each partition."
- [readme] To further improve data quality, we removed entries with malformed or invalid SMILES strings.: "To further improve data quality, we removed entries with malformed or invalid SMILES strings."
