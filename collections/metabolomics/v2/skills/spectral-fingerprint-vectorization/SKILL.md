---
name: spectral-fingerprint-vectorization
description: Use when you have MS2 fragmentation spectra from multiple metabolomics
  samples and need to compare them in a retention time-agnostic manner, especially
  when samples are chemically diverse, acquired with different LC methods or mass
  spectrometer technologies (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - matchms
  - spec2vec
  - Python 3.8
  - numpy
  - MEMO
  - Python 3.8+
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

# spectral-fingerprint-vectorization

## Summary

Generate numeric fingerprint vectors from MS2 spectra by counting occurrences of fragment peaks and neutral losses per sample, enabling retention time-agnostic comparison of metabolomics samples. This skill is essential when samples have poor feature overlap, strong retention time shifts, or were acquired on different LC-MS platforms.

## When to use

Apply this skill when you have MS2 fragmentation spectra from multiple metabolomics samples and need to compare them in a retention time-agnostic manner, especially when samples are chemically diverse, acquired with different LC methods or mass spectrometer technologies (e.g., Q-ToF vs Orbitrap), or exhibit strong chromatographic shifts that prevent traditional feature alignment.

## When NOT to use

- Input data is already a processed feature abundance table (e.g., from untargeted metabolomics peak picking); use fingerprinting only on raw or lightly processed spectra.
- Samples have been aligned by retention time and you need to preserve compound identity from external libraries; fingerprinting is agnostic to compound annotation.
- You require high-resolution mass accuracy matching; fingerprinting counts occurrence rather than scoring similarity, so it is robust to ppm-level shifts but does not exploit them.

## Inputs

- MS2 spectra files in standard formats (mzML, mzXML, MGF, msp)
- Precursor m/z values and fragment m/z lists per spectrum
- Sample-level grouping metadata

## Outputs

- Per-sample MS2 fingerprint vectors (numeric, normalized by sample size)
- Peak occurrence count matrix across samples
- Neutral loss occurrence count matrix across samples

## How to apply

Load MS2 spectra files (mzML, mzXML, MGF, or msp formats) using matchms to parse fragmentation data and extract precursor m/z values for each spectrum. Iterate through all spectra within each sample and count occurrences of MS2 peaks (m/z values above the noise threshold) and calculate neutral losses by subtracting each fragment m/z from its precursor m/z. Aggregate peak and neutral loss occurrence counts across all spectra within each sample using spec2vec document conversion to handle spectral-to-vector transformation. Normalize counts by sample size to account for differences in spectral depth, producing a numeric fingerprint vector per sample that combines relative frequencies of peaks and neutral losses. The resulting fingerprint is dimensionless and comparable across samples regardless of acquisition parameters.

## Related tools

- **MEMO** (Core method implementing MS2-based sample vectorization via peak and neutral loss counting and fingerprint generation) — https://github.com/mandelbrot-project/memo
- **matchms** (Parses MS2 spectra from standard file formats and extracts precursor/fragment m/z metadata) — https://github.com/matchms/matchms
- **spec2vec** (Converts aggregated spectral peaks and neutral losses into document-like vectors for fingerprint representation) — https://github.com/iomega/spec2vec
- **Python 3.8+** (Execution environment for MEMO pipeline and numpy-based vector operations)
- **numpy** (Numeric array operations for peak/loss count aggregation and vector normalization)

## Examples

```
from memo import MEMO
from matchms.importing_utils import load_from_msp
spectra = load_from_msp('samples.msp')
memo = MEMO()
fingerprints = memo.fit_transform(spectra)
```

## Evaluation signals

- Fingerprint vector length equals the total number of unique MS2 peaks and neutral losses observed across the entire sample cohort.
- Sum of normalized fingerprint values per sample equals 1.0 (or close, depending on normalization scheme), confirming occurrence counts were normalized by sample size.
- Fingerprints from blank/negative control samples contain primarily low-abundance peaks; after blank filtering, comparison of sample fingerprints should show increased separation.
- Samples acquired on different LC-MS platforms or with strong retention time offsets produce fingerprints that cluster by chemistry, not by instrument or RT drift.
- Pairwise sample distance or similarity computed from fingerprints (e.g., via MDS/PCoA or TMAP visualization) reflects known chemical relationships or biological groupings in the sample set.

## Limitations

- Fingerprinting discards temporal and structural information (retention time, exact m/z, peak intensity rank); it counts only presence/absence or frequency of fragment patterns, not their properties.
- Neutral loss calculation requires accurate precursor m/z assignment; errors in precursor selection propagate to incorrect neutral loss values.
- Samples with very different total spectral counts (e.g., one sample has 10× more MS2 scans than another) may be biased during normalization if sample size weighting is not carefully applied.
- The method is most effective for chemodiverse or poorly overlapping samples; samples with near-identical chemistry will produce nearly identical fingerprints, offering little discriminatory power.
- No inherent quality control on spectral noise; peaks below the noise threshold must be filtered prior to fingerprinting using external thresholds (e.g., relative intensity cutoffs).

## Evidence

- [other] MS2 fingerprints are generated by counting the occurrence of MS2 peaks and neutral losses (relative to the precursor ion) in each sample, producing a numeric fingerprint representation.: "The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an *MS2 fingerprint* of the sample"
- [other] Fingerprint generation workflow includes loading spectra, extracting precursor m/z, counting peaks and neutral losses, and aggregating via spec2vec document conversion.: "1. Load MS2 spectra files using matchms to parse fragmentation data. 2. Iterate through spectra in each sample and extract precursor m/z values. 3. Count occurrences of all MS2 peaks (m/z values"
- [readme] Fingerprints enable retention time-agnostic alignment of metabolomics samples.: "**M**\ s2 bas\ **E**\ d sa\ **M**\ ple vect\ **O**\ rization (**MEMO**) is a method allowing a Retention Time (RT) agnostic alignment of metabolomics samples using the fragmentation spectra (MS2) of"
- [readme] MEMO suits for comparing chemodiverse samples with poor feature overlap or strong retention time shift across different LC methods and instruments.: "MEMO suits particularly well to compare chemodiverse samples, ie with a poor features overlap, or to compare samples with a strong RT shift, acquired using different LC methods or even different mass"
- [other] Filtering and visualization of fingerprints can follow vectorization.: "different filtering (remove peaks/losses from blanks for example) and visualization techniques (MDS/PCoA, TMAP, Heatmap, ...) can be used"
- [other] matchms is the primary tool for parsing MS2 spectra and spec2vec is used for vectorization.: "MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2 spectra"
