---
name: ms2-fingerprint-matrix-merging
description: Use when you have two MemoMatrix objects generated from separate sample cohorts (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0089
  tools:
  - Python 3.8
  - MEMO
  - memo-ms
  - matchms
  - spec2vec
  - Python 3.8+
  techniques:
  - LC-MS
derived_from:
- doi: 10.3389/fbinf.2022.842964
  title: memo
evidence_spans:
- conda create --name memo python=3.8
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_memo
    doi: 10.3389/fbinf.2022.842964
    title: memo
  dedup_kept_from: coll_memo
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

# ms2-fingerprint-matrix-merging

## Summary

Merge two independently generated MemoMatrix objects containing MS2 fingerprint data into a unified matrix that preserves all spectral features from both sample sets. This enables comparative analysis of chemodiverse or separately acquired metabolomics samples by aligning their MS2-based vectorizations.

## When to use

You have two MemoMatrix objects generated from separate sample cohorts (e.g., sample set A and sample set B, or samples acquired on different instruments/LC methods) and need to combine their MS2 fingerprint data to perform unified downstream filtering, visualization (TMAP, MDS/PCoA, heatmap), or statistical comparison. This is particularly valuable when samples exhibit poor feature overlap or strong retention time shifts across LC/MS conditions.

## When NOT to use

- Input matrices are already feature-aligned or de-duplicated across MS2 identities; merge would create redundant columns.
- One or both MemoMatrix objects contain unprocessed or uncleaned raw spectra (e.g., no blank subtraction or peak filtering applied); merge should occur after individual sample-level quality control.
- The research question requires retention-time aligned data; MEMO's RT-agnostic nature may not address temporal/chromatographic covariance if that is critical.

## Inputs

- MemoMatrix object (sample set A) — matrix of MS2 peak and neutral loss counts per sample
- MemoMatrix object (sample set B) — matrix of MS2 peak and neutral loss counts per sample

## Outputs

- Merged MemoMatrix object — unified matrix containing union of all MS2 peaks/losses from both inputs
- Serialized merged matrix file (JSON, CSV, HDF5, or equivalent structured format)

## How to apply

Load both pre-generated MemoMatrix objects into the MEMO merge module and execute the merged_memo() function, which unions the MS2 peak and neutral loss counts from both matrices into a single output object. Validate that the merged matrix preserves all expected columns from both inputs and that its dimensions correspond to the union of rows and columns from both source matrices. The merge operation maintains the RT-agnostic nature of MEMO, allowing fingerprints generated under different LC or instrumental conditions to be combined without alignment preprocessing. After merging, serialize and export the result to a structured output file (e.g., JSON, CSV, or HDF5 format) for downstream filtering (e.g., blank subtraction) and visualization.

## Related tools

- **MEMO** (Main library providing merged_memo() function and MemoMatrix data structure for merging MS2 fingerprint matrices) — https://github.com/mandelbrot-project/memo
- **memo-ms** (PyPI-distributed Python package version of MEMO; installed via pip install memo-ms) — https://pypi.org/project/memo-ms/
- **matchms** (Underlying library for MS/MS spectrum handling, metadata cleaning, and spectral data I/O used by MEMO) — https://github.com/matchms/matchms
- **spec2vec** (Spectral embedding and similarity scoring module integrated into MEMO for fingerprint representation) — https://github.com/iomega/spec2vec
- **Python 3.8+** (Runtime environment; MEMO requires Python ≥3.8 (tested up to 3.8–3.9, compatible with >3.7 for TMAP support))

## Examples

```
from memo_ms import MemoMatrix; mm_A = load_memoMatrix('sample_set_A.json'); mm_B = load_memoMatrix('sample_set_B.json'); mm_merged = merged_memo([mm_A, mm_B]); mm_merged.to_json('merged_matrix.json')
```

## Evaluation signals

- Merged matrix dimensions equal the union of input matrix dimensions (no rows or columns lost or duplicated)
- All column headers from both input matrices are present in the merged output
- Row indices (sample identifiers) from both inputs appear correctly in the merged matrix without collision or overwriting
- Row and column totals (MS2 peak/loss occurrence counts) sum correctly without artifacts or negative values
- Serialized output file is valid JSON/CSV/HDF5 and can be re-imported by downstream MEMO filtering and visualization functions

## Limitations

- Merge operation is symmetric (union-based) and does not deduplicate MS2 peaks/losses that appear in both matrices; peaks counted in both sample sets will be summed rather than reconciled by identity.
- No explicit handling of peak mass tolerance or peak identity matching during merge; if the same neutral loss or fragment m/z is represented with slight variation across the two MemoMatrix objects, they will be treated as distinct features.
- MEMO is optimized for chemodiverse samples with poor feature overlap or strong RT shifts; merging matrices from highly similar samples or identical instruments may not yield insight beyond feature-based alignment methods.

## Evidence

- [other] What is the output format and structure when two separately generated MemoMatrix objects are merged using the merged_memo() function?: "research_question: What is the output format and structure when two separately generated MemoMatrix objects are merged using the merged_memo() function?"
- [other] MEMO enables alignment of MS2 fingerprints generated from separate samples to compare them in a second stage.: "MEMO enables alignment of MS2 fingerprints generated from separate samples to compare them in a second stage."
- [intro] The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an *MS2 fingerprint* of the sample. These fingerprints can in a second stage be aligned to compare different samples.: "The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an *MS2 fingerprint* of the sample. These fingerprints can in a second stage be aligned"
- [intro] MEMO suits particularly well to compare chemodiverse samples, ie with a poor features overlap, or to compare samples with a strong RT shift, acquired using different LC methods or even different mass spectrometers technology: "MEMO suits particularly well to compare chemodiverse samples, ie with a poor features overlap, or to compare samples with a strong RT shift, acquired using different LC methods or even different mass"
- [intro] different filtering (remove peaks/losses from blanks for example) and visualization techniques (MDS/PCoA, TMAP, Heatmap, ...) can be used: "different filtering (remove peaks/losses from blanks for example) and visualization techniques (MDS/PCoA, TMAP, Heatmap, ...) can be used"
- [other] MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2 spectra: "MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2 spectra"
- [readme] conda env create -f environment.yml: "Use the following line for environment creation `conda env create -f environment.yml`"
