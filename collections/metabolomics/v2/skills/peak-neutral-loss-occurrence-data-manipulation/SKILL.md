---
name: peak-neutral-loss-occurrence-data-manipulation
description: Use when you have aligned MS2 spectra from multiple samples and need to create a matrix representation where rows are samples and columns are MS2 peaks or neutral losses (mass differences to the precursor), with counts of occurrences.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3563
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - matchms
  - Python
  - numpy
  - spec2vec
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

# peak-neutral-loss-occurrence-data-manipulation

## Summary

Count and tabulate occurrences of MS2 peaks and neutral losses across samples to generate MS2 fingerprints, which serve as sample vectorizations for retention-time-agnostic metabolomics alignment. This skill transforms raw MS2 spectra into a sample-by-feature occurrence matrix suitable for downstream filtering and visualization.

## When to use

You have aligned MS2 spectra from multiple samples and need to create a matrix representation where rows are samples and columns are MS2 peaks or neutral losses (mass differences to the precursor), with counts of occurrences. This is the prerequisite step before applying blank-sample filtering or dimensionality-reduction visualization techniques (MDS/PCoA, TMAP, Heatmap).

## When NOT to use

- Input is already a pre-computed feature table or count matrix—skip directly to filtering and visualization.
- MS2 spectra are not aligned across samples (e.g., spectra from different retention times or instruments without prior RT-agnostic preprocessing)—align spectra first using spec2vec or similar methods.
- You only have MS1 data or precursor masses without MS2 fragment lists—MS2 fingerprinting requires fragmentation spectra.

## Inputs

- Aligned MS2 spectra (mzML, mzXML, msp, MGF, or matchms Spectrum objects) from multiple samples
- Precursor ion masses and MS2 fragment peak lists per sample
- Sample metadata (e.g., sample identifiers, blank status)

## Outputs

- Aligned MemoMatrix (sample-by-feature occurrence matrix, CSV or tabular format)
- Feature dictionary mapping column indices to peak m/z values or neutral loss masses
- Sample metadata index (row labels) corresponding to matrix rows

## How to apply

Load MS2 spectra from matched samples using matchms or spec2vec. For each sample, iterate through its MS2 spectrum and identify all peaks and compute neutral losses (mass differences between the precursor ion and detected fragments). Increment a counter for each unique peak m/z or neutral loss mass observed in that sample. Assemble the per-sample occurrence counts into a 2D array (samples × unique peaks/losses), where entry [i,j] is the count of peak or loss j in sample i. This occurrence matrix becomes the aligned MemoMatrix—a sample-by-feature table where features are MS2 peaks and neutral losses, suitable for filtering or visualization downstream. Normalize or leave raw counts depending on the subsequent analysis step.

## Related tools

- **matchms** (Import, parse, and access MS2 spectrum data (peaks, precursor masses, metadata); provide Spectrum objects for iteration and feature extraction) — https://github.com/matchms/matchms
- **spec2vec** (Learn spectral embeddings and relationships between MS2 fragments and neutral losses; support vectorization of spectral similarity) — https://github.com/iomega/spec2vec
- **numpy** (Construct and manipulate the sample-by-feature occurrence matrix as a 2D array)
- **Python** (Primary programming language for scripting the counting and tabulation workflow)

## Examples

```
from matchms import importing; import numpy as np; spectra = list(importing.load_from_msp('samples.msp')); memo_matrix = np.zeros((len(spectra), 1000)); [memo_matrix.__setitem__((i, int(peak[0])), memo_matrix[i, int(peak[0])] + 1) for i, s in enumerate(spectra) for peak in s.peaks]
```

## Evaluation signals

- Matrix shape is (number_of_samples, number_of_unique_peaks_or_losses) with no NaN values
- All matrix entries are non-negative integers (counts); no negative or fractional occurrence values
- Row and column labels match sample IDs and feature m/z or neutral loss values without duplicates
- Sum of counts per sample is positive; no sample row is entirely zero (unless truly absent)
- Feature columns can be verified by spot-checking: manually count peaks/losses in a single sample's raw MS2 spectrum and confirm the matrix row matches

## Limitations

- Counting raw peak occurrences does not account for peak intensity or relative abundance; it treats all detections equally.
- Neutral loss calculation depends on accurate precursor ion mass assignment; errors propagate into the loss feature set.
- High-dimensional matrices with many unique peaks/losses may lead to sparsity, especially across chemodiverse or poorly-overlapping sample sets.
- No built-in handling of m/z tolerance or peak clustering; adjacent peaks are treated as distinct features unless post-processing is applied.

## Evidence

- [intro] The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an *MS2 fingerprint* of the sample.: "The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an *MS2 fingerprint* of the sample."
- [intro] These fingerprints can in a second stage be aligned to compare different samples.: "These fingerprints can in a second stage be aligned to compare different samples."
- [other] Load the aligned MemoMatrix (sample-by-feature occurrence matrix where features are MS2 peaks and neutral losses) and corresponding blank sample metadata using Python/matchms.: "Load the aligned MemoMatrix (sample-by-feature occurrence matrix where features are MS2 peaks and neutral losses) and corresponding blank sample metadata using Python/matchms."
- [other] MEMO is mainly built on `matchms` and `spec2vec` packages for handling the MS2 spectra: "MEMO is mainly built on `matchms` and `spec2vec` packages for handling the MS2 spectra"
- [other] different filtering (remove peaks/losses from blanks for example) and visualization techniques (MDS/PCoA, TMAP, Heatmap, ...) can be used: "different filtering (remove peaks/losses from blanks for example) and visualization techniques (MDS/PCoA, TMAP, Heatmap, ...) can be used"
