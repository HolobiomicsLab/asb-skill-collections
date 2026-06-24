---
name: random-seed-reproducibility-documentation
description: Use when you have generated multiple random partitions (e.g., 10-fold
  cross-validation splits) of a test set and need to deposit them in a shareable repository.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
  tools:
  - Python
  - PyTorch
  - Python 3.12
  - figshare
  - GitHub (sword-nan/SpecEmbedding)
  license_tier: restricted
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

# random-seed-reproducibility-documentation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Document random seeds, split ratios, and partition metadata alongside dataset partitions to enable exact reproduction of cross-validation splits and statistical reporting. This skill ensures that evaluation results reported as mean and standard deviation across multiple folds can be independently reconstructed.

## When to use

Apply this skill when you have generated multiple random partitions (e.g., 10-fold cross-validation splits) of a test set and need to deposit them in a shareable repository. Use it whenever evaluation results will be reported as aggregates (mean, standard deviation) across folds and reproducibility is required for peer review or downstream research.

## When NOT to use

- Your evaluation uses a fixed, non-random train/test split (e.g., a canonical benchmark split with no cross-validation); in that case, only record the split definition, not per-fold seeds.
- Your partitions are already fully specified in a published benchmark; do not re-document unless you are creating new splits.
- You are reporting results from a single, unreplicated experiment without statistical aggregation across folds; seed documentation is less critical but still recommended.

## Inputs

- 10 (or N) randomly-generated query/reference partition pairs (.msp files or indexed records)
- Python random generator state or seed values used to generate each partition
- Split ratio parameters (e.g., 80/20 test-query split ratio)
- Sample count per fold (query set size, reference set size, training set size)

## Outputs

- Structured metadata file (JSON manifest or CSV) recording seed, split ratio, and sample counts per partition
- Annotated partition files with embedded metadata (seed, split index, ratios)
- README or supplementary documentation listing all seeds and reproducibility parameters
- Deposited dataset with complete metadata on figshare or equivalent persistent repository

## How to apply

For each of the 10 (or N) random query/reference partitions, record the random seed used to generate that split, the split ratio (e.g., 80/20 or 50/50), and sample counts for each fold. Store this metadata alongside the partition files (e.g., in a JSON manifest or as header annotations in .msp files). Include the random seeds and split ratios in a README or supplementary table deposited alongside the partitions in a persistent repository (e.g., figshare). This allows future practitioners to either load your exact partitions or regenerate them deterministically. Validate that metadata is complete and machine-readable before deposit.

## Related tools

- **Python 3.12** (Execute random seed generation, partition creation, and metadata serialization logic)
- **figshare** (Persistent repository for depositing partitions and metadata for long-term reproducibility) — https://doi.org/10.6084/m9.figshare.28876751.v2
- **GitHub (sword-nan/SpecEmbedding)** (Source repository containing partition generation scripts and preprocessing logic) — https://github.com/sword-nan/SpecEmbedding

## Examples

```
import json; metadata = [{'fold': i, 'seed': 42 + i, 'split_ratio': '80/20', 'query_count': 500, 'reference_count': 2000} for i in range(10)]; json.dump(metadata, open('partition_metadata.json', 'w')); print('Recorded seeds and split ratios for 10 folds to partition_metadata.json')
```

## Evaluation signals

- Metadata file is valid JSON/CSV and contains exactly N entries (one per fold), each with seed, split ratio, and sample counts.
- Validation that all N partitions are mutually exclusive within the test set (no sample appears in multiple query or reference sets).
- Verification that reseeding Python's random generator with the recorded seed and split ratio regenerates the exact same partition.
- Confirmation that reported mean and standard deviation across folds match recalculated metrics when partitions are reloaded with correct metadata.
- Training set samples do not appear in any test partition (query or reference sets) — checked by comparing SMILES or spectral identifiers.

## Limitations

- Random seed reproducibility is platform and library version–dependent; NumPy, PyTorch, and Python random module versions must be recorded alongside seeds.
- If partitions are regenerated from seeds rather than stored directly, computational cost may increase; trade-off between storage and reproducibility must be chosen upfront.
- Seeds alone do not guarantee reproducibility if the order of operations or random generator initialization differs; complete workflow order must be documented.
- Cross-platform issues may arise (e.g., Windows vs. Linux) due to differences in floating-point arithmetic and random number generation; seeds should be validated on target OS.

## Evidence

- [methods] Retain original training split, apply random splitting only to test sets, report mean and standard deviation across 10 folds.: "we strictly retained the original training set split used by MSBERT and only applied random splitting to the test sets. Final results are reported as the average and standard deviation across the 10"
- [other] Record partition metadata including split seed and sample counts alongside partition files.: "Record metadata (partition index, split seed, sample counts for each fold) alongside each partition. 5. Deposit the complete set of 10 partitions, along with reproducibility metadata (random seeds,"
- [readme] All cleaned data, preprocessing scripts, and 10-fold splits are available on figshare.: "All cleaned data, along with the preprocessing scripts and 10-fold query/reference splits used for evaluation, are available on figshare"
- [readme] Hyperparameter search, training procedure, ablation studies, and full benchmark results are available on figshare for reproducibility.: "Details on the hyperparameter search space, training procedure, ablation studies, and full benchmark results across multiple tasks are also available on figshare for reproducibility and further"
- [other] Validate that all 10 partitions are mutually exclusive within the test set and that no test samples appear in the training set.: "Validate that all 10 partitions are mutually exclusive within the test set and that no test samples appear in the training set."
