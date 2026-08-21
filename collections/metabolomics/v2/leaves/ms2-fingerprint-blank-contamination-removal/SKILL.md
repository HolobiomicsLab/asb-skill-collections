---
name: ms2-fingerprint-blank-contamination-removal
description: Use when after aligning MS2 fingerprints across samples (generating a
  sample-by-feature occurrence matrix) and before applying visualization techniques
  (MDS/PCoA, TMAP, Heatmap) or statistical comparisons.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - matchms
  - Python
  - numpy
  - MEMO
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.3389/fbinf.2022.842964
  title: memo
evidence_spans:
- MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2
  spectra
- MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2
  spectra and converting them into documents.
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3389/fbinf.2022.842964
  all_source_dois:
  - 10.3389/fbinf.2022.842964
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ms2-fingerprint-blank-contamination-removal

## Summary

Remove MS2 peaks and neutral losses originating from blank samples from an aligned MS2 fingerprint matrix (MemoMatrix) to eliminate background contamination prior to downstream visualization or statistical analysis. This filtering step ensures that only sample-specific spectral features are retained for comparative analysis.

## When to use

Apply this skill after aligning MS2 fingerprints across samples (generating a sample-by-feature occurrence matrix) and before applying visualization techniques (MDS/PCoA, TMAP, Heatmap) or statistical comparisons. Use it when blank/control samples are present in the aligned fingerprint matrix and you need to exclude background noise, contamination, or instrumental artifacts that appear in blanks from affecting downstream interpretation.

## When NOT to use

- Input MemoMatrix has not yet been aligned across samples; perform alignment first.
- No blank or negative control samples are present in the dataset; blank removal is not applicable.
- Peaks and neutral losses from blanks are of analytical interest (e.g., studying contamination sources); consider retaining them or analyzing them separately.

## Inputs

- Aligned MemoMatrix (sample-by-feature occurrence matrix; CSV or tabular format)
- Sample metadata identifying blank/control samples
- MS2 peak and neutral loss feature list with identifiers

## Outputs

- Filtered MemoMatrix (blank-corrected sample-by-feature occurrence matrix)
- List of removed features (peaks and neutral losses from blanks)
- Filtered matrix in CSV or tabular format ready for visualization (MDS/PCoA, TMAP, Heatmap)

## How to apply

Load the aligned MemoMatrix (sample-by-feature occurrence matrix where rows are samples and columns are MS2 peaks or neutral losses) along with metadata identifying which rows correspond to blank samples. Scan the blank sample rows to identify all peaks and neutral losses present in any blank. Remove (set to zero or delete columns for) all MS2 peaks and neutral losses that occur in one or more blank samples from the full MemoMatrix. Export the filtered matrix in CSV or tabular format compatible with downstream visualization tools. The rationale is that any peak or loss appearing in a blank sample is considered background contamination and should be excluded from comparative analysis, leaving only features genuinely associated with biological or chemical samples.

## Related tools

- **matchms** (Core library for loading, processing, and manipulating aligned MS2 fingerprint matrices (MemoMatrix) and metadata) — https://github.com/matchms/matchms
- **Python** (Programming language for implementing the filtering workflow (row/column indexing, set operations))
- **numpy** (Array operations for efficiently identifying and masking features (peaks/losses) present in blank samples)
- **MEMO** (End-to-end method and package that produces the aligned fingerprint matrix and integrates blank-removal filtering) — https://github.com/mandelbrot-project/memo

## Examples

```
from matchms import Spectrum
import numpy as np
# Load aligned MemoMatrix and blank metadata
memo_matrix = np.loadtxt('aligned_memo_matrix.csv', delimiter=',')
blank_indices = [0, 1]  # rows corresponding to blanks
blank_mask = np.zeros(memo_matrix.shape[1], dtype=bool)
for idx in blank_indices:
    blank_mask |= (memo_matrix[idx, :] > 0)
filtered_matrix = memo_matrix[:, ~blank_mask]
np.savetxt('filtered_memo_matrix.csv', filtered_matrix, delimiter=',')
```

## Evaluation signals

- Verify that the filtered matrix has fewer or equal columns (features) than the input matrix; confirm that all removed columns correspond to peaks/losses identified in blank samples.
- Check that sample-by-feature occurrence values in the filtered matrix are non-negative integers (or zero after removal).
- Confirm that no peak or neutral loss appearing exclusively in blank samples remains in the filtered matrix.
- Validate that downstream visualizations (MDS/PCoA, TMAP, Heatmap) show improved separation or clarity between sample groups after blank removal compared to unfiltered data.
- Cross-check the removed features list against blank sample metadata to ensure only features from true blank/negative control samples were removed.

## Limitations

- If a peak or neutral loss appears in both blank and non-blank samples, the entire feature is removed, potentially discarding real signal present in genuine samples; consider quantitative thresholding (e.g., sample/blank ratio > 3) as an alternative for borderline cases.
- Removal is binary (all-or-nothing per feature); no partial or weighted removal based on blank intensity or frequency is applied in the standard MEMO workflow.
- Assumes blank sample metadata is accurate and complete; misclassified or missing blank samples will lead to incomplete contamination removal or accidental loss of genuine features.
- The method does not account for differences in blank intensity, injection volume, or instrumental variability; all blanks are treated equally regardless of their MS2 signal magnitude.

## Evidence

- [other] MEMO applies a filtering operation that removes peaks and neutral losses originating from blank samples from the aligned fingerprint matrix, enabling selective exclusion of background contamination before visualization techniques such as MDS/PCoA, TMAP, or Heatmap are applied.: "MEMO applies a filtering operation that removes peaks and neutral losses originating from blank samples from the aligned fingerprint matrix, enabling selective exclusion of background contamination"
- [other] different filtering (remove peaks/losses from blanks for example) and visualization techniques (MDS/PCoA, TMAP, Heatmap, ...) can be used: "different filtering (remove peaks/losses from blanks for example) and visualization techniques (MDS/PCoA, TMAP, Heatmap, ...) can be used"
- [other] Identify all MS2 peaks and neutral losses present in blank samples by scanning their rows in the MemoMatrix. Remove (set to zero or delete columns corresponding to) all peaks and losses that occur in any blank sample from the full MemoMatrix.: "Identify all MS2 peaks and neutral losses present in blank samples by scanning their rows in the MemoMatrix. Remove (set to zero or delete columns corresponding to) all peaks and losses that occur in"
- [intro] The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an *MS2 fingerprint*: "The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an *MS2 fingerprint*"
- [readme] These fingerprints can in a second stage be aligned to compare different samples: "These fingerprints can in a second stage be aligned to compare different samples"
