---
name: memomatrix-object-handling
description: Use when you have generated one or more MemoMatrix objects (MS2 fingerprint
  matrices from separate sample sets) and need to combine them for cross-cohort alignment,
  validate structural consistency after merging, or prepare merged matrices for downstream
  filtering and visualization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3033
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_3520
  tools:
  - Python 3.8
  - MEMO
  - memo-ms
  - matchms
  - spec2vec
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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

# MemoMatrix Object Handling

## Summary

Load, manipulate, and merge MemoMatrix objects—the unified matrix representations of MS2 fingerprints generated from metabolomics samples—to enable alignment and comparative analysis across separate sample cohorts. This skill supports both single-matrix serialization and multi-matrix union operations required for chemodiverse sample comparison.

## When to use

You have generated one or more MemoMatrix objects (MS2 fingerprint matrices from separate sample sets) and need to combine them for cross-cohort alignment, validate structural consistency after merging, or prepare merged matrices for downstream filtering and visualization. Use this skill when comparing samples with poor feature overlap, strong retention time shifts, or acquired across different LC methods or mass spectrometers.

## When NOT to use

- Input samples are already aligned and filtered in a single MemoMatrix; merging would introduce redundant or conflicting data.
- MS2 fingerprints have not yet been generated from raw mass spectrometry data; generate fingerprints first via peak/neutral loss counting.
- MemoMatrix objects were generated using fundamentally incompatible MS2 peak definitions or neutral loss thresholds; structural validation will fail.

## Inputs

- MemoMatrix object (generated from sample set A)
- MemoMatrix object (generated from sample set B)
- Structured input file(s) in MEMO-compatible format

## Outputs

- Merged MemoMatrix object
- Serialized merged MemoMatrix (structured output file)
- Validation report (column/row union dimensions and consistency check)

## How to apply

Load the first MemoMatrix object (generated from sample set A) and the second MemoMatrix object (generated from sample set B) into the MEMO merge module. Execute the merged_memo() function on both MemoMatrix objects to combine their MS2 fingerprint data into a single unified matrix. Validate that the output MemoMatrix contains all expected columns from both input matrices and that row and column dimensions are consistent with the union of both inputs—that is, rows correspond to the union of detected MS2 peaks and neutral losses across both cohorts, and columns represent all samples from both sets. Finally, serialize and export the merged MemoMatrix to a structured output file for use in subsequent filtering (e.g., blank removal) and visualization steps (MDS/PCoA, TMAP, Heatmap).

## Related tools

- **MEMO** (Core framework for MS2-based sample vectorization and MemoMatrix generation, merging, and manipulation) — https://github.com/mandelbrot-project/memo
- **memo-ms** (Python package providing command-line and programmatic interface to MEMO functions including merged_memo())
- **matchms** (Underlying library for importing, processing, and comparing MS/MS spectra; handles MS2 spectrum representation and metadata) — https://github.com/matchms/matchms
- **spec2vec** (Spectral similarity scoring based on MS2 fragment relationships; used within MEMO for advanced spectrum comparisons) — https://github.com/iomega/spec2vec
- **Python 3.8** (Runtime environment for executing MEMO and memo-ms functions)

## Examples

```
from memo import MemoMatrix, merged_memo; mm1 = MemoMatrix.load('sample_set_A.pkl'); mm2 = MemoMatrix.load('sample_set_B.pkl'); merged = merged_memo([mm1, mm2]); merged.save('merged_output.pkl')
```

## Evaluation signals

- Merged MemoMatrix column count equals the union (non-overlapping sum) of columns from both input matrices; no duplicate sample identifiers.
- Merged MemoMatrix row count equals the union of unique MS2 peaks and neutral losses from both input matrices; all rows from either input are present.
- Serialized output file is valid and deserializable back into a MemoMatrix object with no structural loss.
- Validation report explicitly confirms row/column dimensions are consistent with the union of both inputs.
- Downstream filtering and visualization steps (MDS/PCoA, TMAP, Heatmap) execute without schema errors on the merged matrix.

## Limitations

- Merging MemoMatrix objects with incompatible or inconsistently defined MS2 peak/neutral loss thresholds may produce invalid union matrices; ensure both input matrices used the same peak detection and loss definition parameters.
- Large merged matrices (hundreds of thousands of samples or peaks) may incur memory overhead and slow down subsequent filtering and visualization; sparse data formats are recommended for very large datasets.
- The merged_memo() function is retention-time agnostic by design; it does not preserve or align RT information across samples, limiting its utility for RT-based validation or recalibration.

## Evidence

- [other] Load the first MemoMatrix object (generated from sample set A) into the MEMO merge module. Load the second MemoMatrix object (generated from sample set B) into the MEMO merge module. Execute the merged_memo() function on both MemoMatrix objects to combine their MS2 fingerprint data into a single unified matrix.: "Load the first MemoMatrix object (generated from sample set A) into the MEMO merge module. 2. Load the second MemoMatrix object (generated from sample set B) into the MEMO merge module. 3. Execute"
- [other] Validate that the output MemoMatrix contains all expected columns from both input matrices and that row/column dimensions are consistent with the union of both inputs.: "Validate that the output MemoMatrix contains all expected columns from both input matrices and that row/column dimensions are consistent with the union of both inputs."
- [other] Serialize and export the merged MemoMatrix to a structured output file.: "Serialize and export the merged MemoMatrix to a structured output file."
- [other] MEMO enables alignment of MS2 fingerprints generated from separate samples to compare them in a second stage.: "MEMO enables alignment of MS2 fingerprints generated from separate samples to compare them in a second stage."
- [other] MEMO is mainly built on `matchms` and `spec2vec` packages for handling the MS2 spectra: "MEMO is mainly built on `matchms` and `spec2vec` packages for handling the MS2 spectra"
- [readme] These fingerprints can in a second stage be aligned to compare different samples. Once obtained, different filtering (remove peaks/losses from blanks for example) and visualization techniques (MDS/PCoA, TMAP, Heatmap, ...) can be used.: "These fingerprints can in a second stage be aligned to compare different samples. Once obtained, different filtering (remove peaks/losses from blanks for example) and visualization techniques"
