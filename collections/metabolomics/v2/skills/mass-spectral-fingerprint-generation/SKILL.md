---
name: mass-spectral-fingerprint-generation
description: Use when you have unaligned MS2 spectra from one or more samples (in
  formats like .mgf, .mzML, or .mzXML) and need to compare them in a retention-time-agnostic
  manner.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - matchms
  - spec2vec
  - Python 3.8
  - numpy
  - scikit-bio
  - MEMO
  - memo-ms
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.3389/fbinf.2022.842964
  title: memo
evidence_spans:
- MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2
  spectra
- conda create --name memo python=3.8
- pip install numpy
- conda install -c conda-forge scikit-bio
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

# mass-spectral-fingerprint-generation

## Summary

Generate MS2 fingerprints by counting occurrences of MS2 peaks and neutral losses across spectra in a sample, producing a vectorized representation suitable for retention-time-agnostic comparison of metabolomics samples. This approach is particularly effective for chemodiverse samples with poor feature overlap or strong retention time shifts across different LC/MS platforms.

## When to use

You have unaligned MS2 spectra from one or more samples (in formats like .mgf, .mzML, or .mzXML) and need to compare them in a retention-time-agnostic manner. Use this skill when samples exhibit poor feature overlap, strong RT shifts between acquisitions, or were acquired on different LC/MS platforms (e.g., Orbitrap vs. Q-ToF). Do NOT use if you have already-aligned feature tables or if RT alignment is reliable and preferred.

## When NOT to use

- Input data is already a processed feature table or abundance matrix aligned by retention time or m/z matching.
- MS/MS spectra contain only precursor m/z without fragmentation data.
- Your analytical goal requires retention-time-dependent metabolite annotation or chromatographic separation validation.

## Inputs

- MS2 spectra files in matchms-supported formats (.mgf, .mzML, .mzXML, .msp, or metabolomics-USI)
- Unaligned mass spectrometry data with precursor m/z and fragmentation patterns
- Sample grouping metadata (if comparing multiple samples)

## Outputs

- MemoMatrix object with sample-by-feature structure
- MS2 fingerprints (frequency vectors of MS2 peaks and neutral losses per sample)
- Sample vectorization suitable for downstream alignment, filtering, and visualization

## How to apply

Load MS2 spectra files using matchms to parse fragmentation data and precursor m/z values. For each sample, iterate through all spectra and count the occurrence of each distinct MS2 peak (m/z fragment) and neutral loss (mass difference between precursor and fragment). Accumulate these counts into a sample-level histogram or frequency table. The resulting MS2 fingerprint is a fixed-length vector where each element represents the count (or binary presence) of a specific peak or neutral loss across that sample. Execute the memo_from_unaligned function from the memo-ms package to align fingerprints across samples and construct the final MemoMatrix object with sample-by-feature dimensionality. Verify the MemoMatrix has the expected structure: rows = samples, columns = unique MS2 features (peaks/losses), cells = counts or presence/absence values.

## Related tools

- **MEMO** (Implements MS2-based sample vectorization and fingerprint alignment to construct the MemoMatrix) — https://github.com/mandelbrot-project/memo
- **matchms** (Parses MS2 spectra from common file formats and extracts fragmentation data and metadata) — https://github.com/matchms/matchms
- **memo-ms** (Python package providing the memo_from_unaligned function for fingerprint generation and alignment)
- **spec2vec** (Provides spectral embedding and similarity scoring based on MS2 fragmental relationships) — https://github.com/iomega/spec2vec
- **numpy** (Supports efficient array operations and counting of peak/loss occurrences)
- **scikit-bio** (Provides statistical and comparative genomics/metabolomics utilities for downstream analysis)

## Examples

```
from memo_ms import memo_from_unaligned; memo_matrix = memo_from_unaligned(['sample1.mgf', 'sample2.mgf']); print(memo_matrix.shape)
```

## Evaluation signals

- MemoMatrix dimensionality matches expected sample count (rows) and unique MS2 features (columns).
- All fingerprint values are non-negative counts or binary presence/absence indicators.
- MS2 fingerprint vectors are non-zero and exhibit expected sample-specific variation (e.g., samples from different sources show distinct peak/loss profiles).
- Metadata attributes in the MemoMatrix (sample IDs, feature m/z values, neutral loss definitions) are correctly populated and traceable to input spectra.
- Downstream alignment and visualization outputs (e.g., heatmaps, PCoA/MDS plots) show meaningful clustering that reflects known sample relationships or chemodiverse differences.

## Limitations

- MS2 fingerprinting is retention-time agnostic and loses chromatographic context; RT-dependent metabolite identification requires additional information.
- Neutral loss counting depends on accurate precursor m/z assignment; mass calibration errors propagate into the fingerprint.
- Samples with very different spectral complexity or depth may show biased fingerprints; subsampling or normalization may be needed.
- Peak/loss occurrence counting is sensitive to spectral quality and noise; filtering blanks and low-intensity peaks is essential (as mentioned in the MEMO workflow).
- Performance scales with the total number of unique MS2 peaks and losses across all samples; very large datasets may require sparse matrix representations.

## Evidence

- [intro] The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an *MS2 fingerprint* of the sample: "The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an *MS2 fingerprint*"
- [intro] These fingerprints can in a second stage be aligned to compare different samples: "These fingerprints can in a second stage be aligned to compare different samples"
- [intro] MEMO is particularly suited for comparing chemodiverse samples with poor feature overlap or strong RT shifts: "MEMO suits particularly well to compare chemodiverse samples, ie with a poor features overlap, or to compare samples with a strong RT shift"
- [methods] Load spectra using matchms to parse MS2 fragmentation and precursor data: "Load unaligned MS2 spectra files in a format supported by matchms (e.g., .mgf, .mzML, .mzXML). 2. Parse spectra using matchms to extract MS2 fragmentation data and precursor information."
- [methods] Execute memo_from_unaligned to construct the MemoMatrix: "Execute memo_from_unaligned function from memo-ms package to align fingerprints and construct the MemoMatrix object."
- [methods] Verify MemoMatrix structure and content: "Inspect the resulting MemoMatrix for correct dimensionality, sample-by-feature structure, and presence of metadata attributes."
- [other] MEMO is built on matchms and spec2vec: "MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2 spectra"
- [intro] Filtering blanks is part of the MEMO workflow: "different filtering (remove peaks/losses from blanks for example) and visualization techniques (MDS/PCoA, TMAP, Heatmap, ...) can be used"
- [readme] MEMO method definition and retention-time agnostic alignment: "MS2 basED saMple vectOrization (MEMO) is a method allowing a Retention Time (RT) agnostic alignment of metabolomics samples"
- [readme] Comparison across different MS platforms is supported: "to compare samples with a strong RT shift, acquired using different LC methods or even different mass spectrometers technology (Maxiis Q-ToF vs Q-Exactive Orbitrap)"
