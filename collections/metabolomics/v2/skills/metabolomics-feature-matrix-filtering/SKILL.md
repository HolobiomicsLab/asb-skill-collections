---
name: metabolomics-feature-matrix-filtering
description: Use when you have an aligned MemoMatrix (sample-by-feature occurrence matrix where features are MS2 peaks and neutral losses) and need to remove background noise before applying visualization or clustering techniques (MDS/PCoA, TMAP, Heatmap).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - matchms
  - Python
  - numpy
  - pandas
derived_from:
- doi: 10.3389/fbinf.2022.842964
  title: memo
evidence_spans:
- MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2 spectra
- MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2 spectra and converting them into documents.
- conda create --name memo python=3.8
- pip install numpy
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_memo_cq
    doi: 10.3389/fbinf.2022.842964
    title: memo
  dedup_kept_from: coll_memo_cq
schema_version: 0.2.0
---

# metabolomics-feature-matrix-filtering

## Summary

Remove contaminant MS2 peaks and neutral losses originating from blank samples from an aligned MS2 fingerprint matrix prior to downstream visualization. This filtering step enables selective exclusion of background contamination to improve sample-to-sample comparisons in chemodiverse metabolomics datasets.

## When to use

Apply this skill when you have an aligned MemoMatrix (sample-by-feature occurrence matrix where features are MS2 peaks and neutral losses) and need to remove background noise before applying visualization or clustering techniques (MDS/PCoA, TMAP, Heatmap). Specifically, use this when blank sample metadata is available and you want to exclude peaks and losses present in any blank from the full matrix to improve signal-to-noise ratio in downstream analysis.

## When NOT to use

- Input data does not include blank samples or blank metadata is unavailable
- The MemoMatrix has already undergone blank filtering in an upstream step
- Analysis goal is to study contamination patterns or background composition rather than remove them

## Inputs

- Aligned MemoMatrix (sample-by-feature occurrence matrix, CSV or tabular format)
- Blank sample metadata (sample identifiers or indices annotating which samples are blanks)
- MS2 peaks and neutral losses data associated with each sample

## Outputs

- Filtered MemoMatrix with contaminant peaks/losses removed (CSV or tabular format)
- Feature set suitable for downstream visualization (MDS/PCoA, TMAP, Heatmap)

## How to apply

Load the aligned MemoMatrix and corresponding blank sample metadata using matchms or pandas. Scan the rows corresponding to blank samples and identify all MS2 peaks and neutral losses present in them. Remove (set to zero or delete columns for) all peaks and losses that occur in any blank sample from the full MemoMatrix. The rationale is that any peak or loss detected in a blank represents potential contamination or instrument background rather than true sample signal. Export the filtered MemoMatrix as a CSV or tabular format compatible with downstream visualization tools. Verify filtering by confirming that blank rows now contain zeros for previously detected features and that the matrix dimensions reflect removed features.

## Related tools

- **matchms** (Load and manipulate the aligned MemoMatrix and MS2 spectral metadata) — https://github.com/matchms/matchms
- **Python** (Primary language for implementing the filtering workflow, array operations, and I/O)
- **numpy** (Efficient matrix operations (masking, zeroing, column deletion) on the MemoMatrix)
- **pandas** (Alternative or complementary tabular data manipulation, indexing by sample/feature names)

## Examples

```
# After loading MemoMatrix and blank metadata with matchms/pandas:
filtered_matrix = memo_matrix.copy()
blank_features = memo_matrix.loc[memo_matrix.index.isin(blank_sample_ids)].sum(axis=0) > 0
filtered_matrix = memo_matrix.loc[:, ~blank_features]
filtered_matrix.to_csv('filtered_memo_matrix.csv')
```

## Evaluation signals

- Blank sample rows in the filtered matrix contain all zeros (no peaks or losses remain)
- Column count decreased compared to the input matrix (contaminant features removed)
- Non-blank samples retain their original peak/loss counts for features not present in any blank
- Filtered matrix is compatible with downstream visualization tools without import errors
- Comparison of feature overlap before/after filtering shows expected reduction in background-derived features

## Limitations

- Filtering assumes blanks are representative of true background; contamination present in multiple sample types may not be distinguished
- Removing all occurrences of a peak/loss present in any blank may discard legitimate sample signal if that peak is truly present in both blanks and samples
- No statistical threshold (e.g., presence in >N% of blanks) is explicitly mentioned; current method uses presence in any single blank as removal criterion
- The effectiveness depends on the quality and representativeness of blank sample preparation and acquisition

## Evidence

- [other] MEMO applies a filtering operation that removes peaks and neutral losses originating from blank samples from the aligned fingerprint matrix, enabling selective exclusion of background contamination before visualization techniques such as MDS/PCoA, TMAP, or Heatmap are applied.: "MEMO applies a filtering operation that removes peaks and neutral losses originating from blank samples from the aligned fingerprint matrix, enabling selective exclusion of background contamination"
- [other] 1. Load the aligned MemoMatrix (sample-by-feature occurrence matrix where features are MS2 peaks and neutral losses) and corresponding blank sample metadata using Python/matchms. 2. Identify all MS2 peaks and neutral losses present in blank samples by scanning their rows in the MemoMatrix. 3. Remove (set to zero or delete columns corresponding to) all peaks and losses that occur in any blank sample from the full MemoMatrix. 4. Export the filtered MemoMatrix as a CSV or tabular format compatible with downstream visualization tools (MDS/PCoA, TMAP, Heatmap).: "Load the aligned MemoMatrix (sample-by-feature occurrence matrix where features are MS2 peaks and neutral losses) and corresponding blank sample metadata using Python/matchms. Identify all MS2 peaks"
- [intro] different filtering (remove peaks/losses from blanks for example) and visualization techniques (MDS/PCoA, TMAP, Heatmap, ...) can be used: "different filtering (remove peaks/losses from blanks for example) and visualization techniques (MDS/PCoA, TMAP, Heatmap, ...) can be used"
- [other] The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an MS2 fingerprint of the sample. These fingerprints can in a second stage be aligned to compare different samples.: "The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an *MS2 fingerprint* of the sample. These fingerprints can in a second stage be aligned"
