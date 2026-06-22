---
name: multi-sample-metabolomics-data-integration
description: Use when you have two or more independently processed MemoMatrix objects (each generated from a separate sample set) and your analysis goal requires direct comparison of MS2 fingerprint profiles across those samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# multi-sample-metabolomics-data-integration

## Summary

Merges separately generated MS2 fingerprint matrices (MemoMatrix objects) from multiple metabolomics samples into a single unified matrix, enabling retention-time-agnostic comparative analysis across chemodiverse or cross-platform datasets. This skill is essential when aligning MS2 fragmentation data from samples acquired under different LC–MS conditions or on different instrument platforms.

## When to use

Apply this skill when you have two or more independently processed MemoMatrix objects (each generated from a separate sample set) and your analysis goal requires direct comparison of MS2 fingerprint profiles across those samples. Typical triggers include: comparing samples acquired on different mass spectrometer technologies (e.g., MaXis Q-ToF vs Q-Exactive), reconciling data from different LC methods with strong retention-time shifts, or unifying chemodiverse sample sets with poor feature overlap that would fail alignment at the feature level.

## When NOT to use

- Input matrices are from the same LC–MS run or cohort and have already been aligned at the feature level; use within-batch normalization instead.
- You need to retain retention-time information for peak matching; MEMO is explicitly RT-agnostic and discards RT data.
- Samples have extreme differences in total ion abundance and you require abundance-normalized or probabilistic similarity scores; the merged fingerprint is a raw count matrix.

## Inputs

- MemoMatrix object (from sample set A)
- MemoMatrix object (from sample set B)
- Additional MemoMatrix objects (optional, for multi-way merges)

## Outputs

- Merged MemoMatrix object (unified matrix containing all samples and all MS2 peaks/neutral losses)
- Serialized merged MemoMatrix (exported to structured output file, e.g., JSON, HDF5, or CSV)

## How to apply

Load each independently generated MemoMatrix object (containing MS2 peak and neutral loss occurrence counts for a sample set) into the MEMO merge module. Execute the merged_memo() function to combine all input matrices into a single unified matrix. The merge operation aligns the MS2 fingerprint data across samples by taking the union of all rows (samples) and columns (MS2 peaks/neutral losses), preserving occurrence counts from each input matrix. After merging, validate dimensional consistency (output rows = union of input rows; output columns = union of input columns) and verify that all expected columns from both inputs are present in the merged output. Finally, serialize and export the unified MemoMatrix to a structured output file for downstream filtering and visualization.

## Related tools

- **MEMO** (Core library providing merged_memo() function and MemoMatrix data structure for multi-sample MS2 fingerprint integration) — https://github.com/mandelbrot-project/memo
- **memo-ms** (Python package distribution of MEMO; installed via pip to access merged_memo() and related APIs) — https://pypi.org/project/memo-ms/
- **matchms** (Underlying library for MS2 spectrum handling, metadata cleaning, and spectral format I/O that MEMO depends on) — https://github.com/matchms/matchms
- **spec2vec** (Optional downstream tool for computing MS2 spectral similarity scores on merged fingerprints) — https://github.com/iomega/spec2vec
- **Python 3.8+** (Runtime environment for executing MEMO merge workflows and serialization)

## Examples

```
from memo import MemoMatrix, merged_memo; memo1 = MemoMatrix.load('sample_set_A.memo'); memo2 = MemoMatrix.load('sample_set_B.memo'); merged = merged_memo([memo1, memo2]); merged.to_file('merged_output.memo')
```

## Evaluation signals

- Merged MemoMatrix has correct dimensions: row count equals union of input sample counts; column count equals union of unique MS2 peaks and neutral losses across all inputs.
- All columns present in input matrices appear in the merged output; no loss of peak or neutral loss features during merge.
- Occurrence counts are preserved: spot-check a known MS2 peak or neutral loss value in input and verify it appears with the same count in the corresponding sample row of the merged matrix.
- Serialized output file validates against expected schema (if using JSON) or loads successfully with memo-ms deserialization functions without format errors.
- Merged matrix can be successfully passed to downstream MEMO filtering or visualization functions (e.g., blank peak removal, TMAP, MDS/PCoA) without shape mismatches or missing-value errors.

## Limitations

- Merging assumes all input MemoMatrix objects were generated using the same MS2 peak detection and neutral loss definition parameters; inconsistency in preprocessing may lead to incomparable fingerprints.
- The merged matrix retains only occurrence counts; absolute intensity or area under the curve (AUC) data are lost if they were not baked into the fingerprint generation step.
- No built-in handling of batch effects, systematic retention-time shifts, or instrument-specific peak calibration offsets; such effects must be addressed before or after merging using external normalization or filtering.
- Merged matrices can become high-dimensional (many columns) when combining very diverse sample sets, potentially increasing sparsity and memory footprint.
- Performance on merging >10 large MemoMatrix objects is not explicitly benchmarked in the publication; scalability beyond typical two-to-three-sample merges is unclear.

## Evidence

- [other] MEMO enables alignment of MS2 fingerprints generated from separate samples to compare them in a second stage.: "MEMO enables alignment of MS2 fingerprints generated from separate samples to compare them in a second stage."
- [intro] The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an *MS2 fingerprint* of the sample.: "The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an *MS2 fingerprint*"
- [other] These fingerprints can in a second stage be aligned to compare different samples.: "These fingerprints can in a second stage be aligned to compare different samples"
- [intro] MEMO suits particularly well to compare chemodiverse samples, ie with a poor features overlap, or to compare samples with a strong RT shift, acquired using different LC methods or even different mass spectrometers technology.: "MEMO suits particularly well to compare chemodiverse samples, ie with a poor features overlap, or to compare samples with a strong RT shift, acquired using different LC methods or even different mass"
- [intro] a method allowing a Retention Time (RT) agnostic alignment of metabolomics samples using the fragmentation spectra (MS2) of their consituents: "a method allowing a Retention Time (RT) agnostic alignment of metabolomics samples using the fragmentation spectra (MS2) of their consituents"
- [intro] different filtering (remove peaks/losses from blanks for example) and visualization techniques (MDS/PCoA, TMAP, Heatmap, ...) can be used: "different filtering (remove peaks/losses from blanks for example) and visualization techniques (MDS/PCoA, TMAP, Heatmap, ...) can be used"
