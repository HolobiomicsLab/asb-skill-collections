---
name: spectral-library-query-reference-pairing
description: Use when when evaluating a trained spectral embedding model on publicly available datasets (GNPS, MoNA, MTBLS1572, MassBank, or MassSpecGym) and you need to report averaged performance metrics with standard deviation to demonstrate robustness and reproducibility.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - Python
  - PyTorch
  - Python 3.12
  - PyTorch 2.6.0
  - figshare
  - numba
  techniques:
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-library-query-reference-pairing

## Summary

Construct reproducible 10-fold query/reference test set partitions from pre-cleaned MS/MS spectral libraries while preserving the original training split, enabling robust evaluation of spectral embedding models across multiple random splits.

## When to use

When evaluating a trained spectral embedding model on publicly available datasets (GNPS, MoNA, MTBLS1572, MassBank, or MassSpecGym) and you need to report averaged performance metrics with standard deviation to demonstrate robustness and reproducibility. Use this skill if the original MSBERT training/test split must be retained for consistency with prior work.

## When NOT to use

- The original MSBERT training/test split is unavailable or already modified; random splitting of the test set requires knowledge of which samples were originally held out.
- Your evaluation goal does not require cross-validation or multiple random splits (e.g., single hold-out evaluation is sufficient); the 10-fold procedure adds computational cost and complexity.
- Input spectral data has not undergone SMILES validation or removal of malformed entries; apply data cleaning (removal of invalid SMILES, format errors) before constructing partitions.

## Inputs

- Pre-cleaned MS/MS spectral library (GNPS, MoNA, MTBLS1572, MassBank, or MassSpecGym) in .msp format
- Original MSBERT training/test split metadata or indices
- Random seed value(s) for reproducibility
- Desired query/reference split ratio (e.g., 80/20, 50/50)

## Outputs

- 10 query/reference paired partition sets (each as indexed .msp files or JSON records)
- Partition metadata manifest (partition index, split seed, query sample count, reference sample count)
- Reproducibility documentation (random seeds used, split ratios, sample counts per fold)
- Validation report confirming mutual exclusivity and no training/test leakage

## How to apply

Load the pre-cleaned spectral data with the original MSBERT training/test split already applied. Extract only the test partition and confirm the training split is held fixed. Randomly re-partition the test set 10 times using a controlled random seed, each time generating a new query set and reference set pair (e.g., 80/20 or 50/50 split). Store each of the 10 query/reference pairs as separate structured files (.msp or JSON) with metadata including partition index, split seed, and sample counts. Validate that all 10 partitions are mutually exclusive within the test set and that no test samples leak into the training set. Deposit the complete set of 10 partitions along with reproducibility metadata to a persistent repository (e.g., figshare).

## Related tools

- **Python 3.12** (Primary programming language for partition generation, validation, and metadata tracking)
- **PyTorch 2.6.0** (Required runtime environment for loading and testing spectral embedding models during evaluation) — https://github.com/sword-nan/SpecEmbedding
- **figshare** (Long-term deposit and retrieval of 10-fold partition sets and reproducibility metadata) — https://doi.org/10.6084/m9.figshare.28876751.v2
- **numba** (Numerical acceleration for cosine similarity computation (note: @njit decorators may cause Windows compatibility issues)) — https://github.com/sword-nan/SpecEmbedding

## Evaluation signals

- Confirm that all 10 partitions sum to 100% of the test set with no sample overlap (set intersection = ∅).
- Verify that no test set sample ID appears in the training split metadata or indices.
- Validate that each partition metadata record contains non-null partition_index, split_seed, query_count, and reference_count fields.
- Reproduce a partition using the stored random seed and confirm exact match of query/reference sample assignments.
- Confirm that average metric ± std_dev across 10 folds can be computed from the partition results without missing or malformed fold data.

## Limitations

- Windows users may encounter numerical errors during cosine similarity computation due to @njit decorators from numba; workaround requires commenting out @njit decorators in the code.
- The procedure is designed for test set partitioning only; the original training split is retained and not re-randomized, limiting exploration of training set variation.
- Reproducibility depends critically on correct capture and logging of random seeds; loss or transcription error of seeds will prevent future exact reproduction of partitions.
- Storage and management of 10 separate partition files or indexed records can introduce I/O overhead and requires careful bookkeeping to avoid accidental deletion or corruption.

## Evidence

- [readme] we strictly retained the original training set split used by MSBERT and only applied random splitting to the test sets. Final results are reported as the average and standard deviation across the 10: "we strictly retained the original training set split used by MSBERT and only applied random splitting to the test sets. Final results are reported as the average and standard deviation across the 10"
- [readme] All cleaned data, along with the preprocessing scripts and 10-fold query/reference splits used for evaluation, are available on figshare: "All cleaned data, along with the preprocessing scripts and 10-fold query/reference splits used for evaluation, are available on figshare"
- [other] Randomly re-partition the test set 10 times, each time generating a new query set and reference set pair (e.g., 80/20 or 50/50 split depending on the design). Store each of the 10 query/reference pairs as separate files (or indexed records) in a structured repository (e.g., separate .msp files or a JSON manifest). Record metadata (partition index, split seed, sample counts for each fold) alongside each partition.: "Randomly re-partition the test set 10 times, each time generating a new query set and reference set pair (e.g., 80/20 or 50/50 split depending on the design). Store each of the 10 query/reference"
- [other] Extract only the test partition and confirm training split is held fixed.: "Extract only the test partition and confirm training split is held fixed."
- [other] Validate that all 10 partitions are mutually exclusive within the test set and that no test samples appear in the training set. Deposit the complete set of 10 partitions, along with reproducibility metadata (random seeds, split ratios), to figshare.: "Validate that all 10 partitions are mutually exclusive within the test set and that no test samples appear in the training set. Deposit the complete set of 10 partitions, along with reproducibility"
- [readme] To further improve data quality, we removed entries with malformed or invalid SMILES strings.: "To further improve data quality, we removed entries with malformed or invalid SMILES strings."
