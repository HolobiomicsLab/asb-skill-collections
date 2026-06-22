---
name: spectral-feature-consolidation
description: Use when when you have generated separate MemoMatrix objects from independent sample sets (e.g., sample set A and sample set B) and need to align and combine their MS2 fingerprint data into a single matrix for comparative analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
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

# Spectral Feature Consolidation

## Summary

Merge MS2 fingerprint matrices from multiple samples into a unified consolidated matrix that preserves all spectral feature information while maintaining structural consistency. This consolidation enables cross-sample comparison of MS2 peak and neutral loss patterns, particularly for chemodiverse or retention-time-shifted datasets.

## When to use

When you have generated separate MemoMatrix objects from independent sample sets (e.g., sample set A and sample set B) and need to align and combine their MS2 fingerprint data into a single matrix for comparative analysis. Use this skill when your analysis goal requires unified feature space across multiple independently processed metabolomics samples.

## When NOT to use

- MemoMatrix objects were generated from the same sample set or overlapping sample sets (consolidation introduces redundancy)
- Input matrices have conflicting or incompatible MS2 peak/loss definitions or different mass calibration standards
- Your analysis goal requires per-sample isolation rather than cross-sample feature alignment

## Inputs

- MemoMatrix object from sample set A (MS2 fingerprint matrix)
- MemoMatrix object from sample set B (MS2 fingerprint matrix)

## Outputs

- Merged MemoMatrix object (consolidated MS2 fingerprint matrix)
- Serialized merged MemoMatrix file (e.g., CSV or HDF5)

## How to apply

Load each separately generated MemoMatrix object (containing MS2 peak and neutral loss counts per sample) into the MEMO merge module. Execute the merged_memo() function, which combines the matrices while preserving all columns from both input objects and computing row/column dimensions as the union of both inputs. Validate the output by confirming: (1) all expected columns from both inputs are present, (2) row and column dimensions match the union set, (3) no data loss or inconsistent mapping has occurred. Finally, serialize and export the consolidated MemoMatrix to a structured file format (e.g., CSV or HDF5) for downstream filtering and visualization workflows.

## Related tools

- **MEMO** (Core package providing merged_memo() function and MemoMatrix data structure) — https://github.com/mandelbrot-project/memo
- **memo-ms** (PyPI-installable Python package distribution of MEMO)
- **matchms** (Underlying library for MS2 spectrum handling and peak management in MEMO) — https://github.com/matchms/matchms
- **spec2vec** (Spectral similarity scoring framework integrated with MEMO for fingerprint alignment) — https://github.com/iomega/spec2vec
- **Python 3.8+** (Runtime environment for executing merged_memo() and matrix serialization)

## Examples

```
from memo import MemoMatrix, merged_memo; memo_a = MemoMatrix.load('sample_set_a.h5'); memo_b = MemoMatrix.load('sample_set_b.h5'); merged = merged_memo(memo_a, memo_b); merged.to_csv('merged_fingerprints.csv')
```

## Evaluation signals

- Output MemoMatrix contains all columns present in both input MemoMatrix objects with no column loss or duplication
- Output row count equals the union of row indices across both input matrices (no row collisions or overwrites)
- Output column count equals the union of column indices across both input matrices
- Serialized merged file contains valid, non-null entries for all MS2 peak and neutral loss counts with consistent data types
- Spot-check: sample identifiers from both input matrices are preserved and traceable in the merged output

## Limitations

- Merging requires that both MemoMatrix objects use compatible MS2 peak definitions and neutral loss calculations; inconsistent mass calibration or peak filtering between inputs may produce semantically invalid merged matrices
- The merged_memo() function assumes disjoint sample sets; merging matrices with overlapping samples introduces redundancy and compromises statistical validity
- Memory constraints may apply when consolidating very large matrices (hundreds of thousands of peaks across thousands of samples); sparse matrix formats are recommended for such cases

## Evidence

- [other] Load the first MemoMatrix object (generated from sample set A) into the MEMO merge module. Load the second MemoMatrix object (generated from sample set B) into the MEMO merge module. Execute the merged_memo() function on both MemoMatrix objects to combine their MS2 fingerprint data into a single unified matrix.: "Load the first MemoMatrix object (generated from sample set A) into the MEMO merge module. Load the second MemoMatrix object (generated from sample set B) into the MEMO merge module. Execute the"
- [other] Validate that the output MemoMatrix contains all expected columns from both input matrices and that row/column dimensions are consistent with the union of both inputs.: "Validate that the output MemoMatrix contains all expected columns from both input matrices and that row/column dimensions are consistent with the union of both inputs."
- [other] MEMO enables alignment of MS2 fingerprints generated from separate samples to compare them in a second stage.: "MEMO enables alignment of MS2 fingerprints generated from separate samples to compare them in a second stage."
- [intro] The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an MS2 fingerprint of the sample.: "The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an MS2 fingerprint of the sample."
- [intro] These fingerprints can in a second stage be aligned to compare different samples.: "These fingerprints can in a second stage be aligned to compare different samples."
