---
name: sample-vectorization-via-spectral-features
description: Use when you have unaligned MS2 spectra from multiple metabolomics samples
  (in mzML, mzXML, or MGF format) and need to compare them without relying on retention
  time or aligned m/z features.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - matchms
  - spec2vec
  - Python 3.8
  - numpy
  - scikit-bio
  - memo-ms
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

# sample-vectorization-via-spectral-features

## Summary

Transform unaligned MS2 spectra into sample-level feature vectors (MemoMatrix) by counting MS2 peaks and neutral losses across all spectra in each sample, enabling retention-time agnostic comparison of metabolomics samples. This skill is essential when samples acquired on different LC–MS platforms or with strong retention-time drift need to be compared despite poor feature overlap.

## When to use

Apply this skill when you have unaligned MS2 spectra from multiple metabolomics samples (in mzML, mzXML, or MGF format) and need to compare them without relying on retention time or aligned m/z features. Use it especially for chemodiverse samples (poor feature overlap), samples acquired on different LC methods or mass spectrometers (e.g. Maxiis Q-ToF vs Q-Exactive Orbitrap), or when strong retention-time shifts between runs make traditional feature alignment unreliable.

## When NOT to use

- Input spectra are already aligned and feature-extracted (use a peak-picking and alignment tool instead)
- You require retention-time information to distinguish isobaric compounds (MEMO is RT-agnostic and may conflate isomers)
- Samples have very low spectral complexity or few MS2 events per sample (resulting matrix may be too sparse for statistical power)

## Inputs

- Unaligned MS2 spectra files (.mgf, .mzML, .mzXML format)
- Sample metadata (optional: sample identifiers, blank/control indicators)

## Outputs

- MemoMatrix object (sample-by-feature matrix of MS2 fingerprint counts)
- Metadata attributes (sample names, feature identities as m/z or neutral losses)

## How to apply

Load and parse unaligned MS2 spectra using matchms to extract fragmentation data and precursor information. For each sample, count the occurrence of each MS2 peak (m/z fragment) and neutral loss (mass difference to precursor ion) across all spectra within that sample. Execute the memo_from_unaligned function from the memo-ms package to align these counts across samples and construct a MemoMatrix object with dimensions sample-by-feature. The resulting matrix represents each sample as a vector of MS2 fingerprint counts. Optionally apply filtering (e.g., remove peaks/losses detected in blank samples) before downstream visualization or statistical analysis using techniques such as MDS/PCoA, TMAP, or heatmaps.

## Related tools

- **memo-ms** (Implements memo_from_unaligned function and MemoMatrix construction; core algorithm for fingerprint alignment) — https://github.com/mandelbrot-project/memo
- **matchms** (Imports, parses, and extracts MS2 spectra metadata (precursor m/z, fragmentation peaks) from mzML, mzXML, MGF files) — https://github.com/matchms/matchms
- **spec2vec** (Provides spectral similarity scoring based on learned fragment relationships; used alongside MEMO for sample comparison) — https://github.com/iomega/spec2vec
- **Python 3.8+** (Runtime environment (MEMO requires Python ≥3.8 for syntax compatibility))
- **numpy** (Numerical operations for matrix construction and manipulation)
- **scikit-bio** (Statistical and biological data analysis support (optional for downstream PCoA/MDS))

## Examples

```
from memo import memo_from_unaligned; from matchms.importing_utils import load_from_mgf; spectra = list(load_from_mgf('sample.mgf')); memo_matrix = memo_from_unaligned(spectra, output='MemoMatrix')
```

## Evaluation signals

- MemoMatrix dimensionality is (number_of_samples, number_of_unique_peaks+losses); verify by inspecting shape and sample-by-feature structure
- All entries in the MemoMatrix are non-negative integer counts (no negative values or NaN); spot-check matrix content
- Metadata attributes are preserved and correctly associated with rows (samples) and columns (m/z or neutral losses)
- Filtering step (if applied) reduces matrix width by removing peaks/losses present in blank samples without affecting non-blank samples; verify count reduction and blank absence
- Downstream visualization (MDS/PCoA/TMAP) produces sensible clustering or separation that reflects known sample groupings (e.g., by plant family, extraction method, or organism)

## Limitations

- MEMO is retention-time agnostic; it cannot distinguish isobaric or co-eluting compounds that fragment identically, leading to conflation of signals
- MS2 fingerprints are effective for chemodiverse samples but may lose sensitivity for sample sets with high feature overlap (signals will be dominated by shared peaks/losses)
- Requires adequate number of MS2 spectra per sample to generate robust fingerprints; sparse or low-complexity samples may produce uninformative vectors
- TMAP visualization is only available on MacOS and Linux (Windows users must use WSL or alternative visualization tools like MDS/PCoA)
- Filtering step (removal of blank-derived peaks/losses) assumes blanks are correctly labeled; mislabeled or contaminated blanks will lead to incorrect filtering

## Evidence

- [readme] MEMO is a method allowing a Retention Time (RT) agnostic alignment of metabolomics samples using the fragmentation spectra (MS2) of their constituents.: "a method allowing a Retention Time (RT) agnostic alignment of metabolomics samples using the fragmentation spectra (MS2) of their consituents"
- [readme] MS2 fingerprints are generated by counting occurrences of MS2 peaks and neutral losses in each sample.: "The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an *MS2 fingerprint* of the sample"
- [readme] MEMO suits particularly well to compare chemodiverse samples with poor feature overlap or strong RT shifts across different LC methods and mass spectrometer technologies.: "MEMO suits particularly well to compare chemodiverse samples, ie with a poor features overlap, or to compare samples with a strong RT shift, acquired using different LC methods or even different mass"
- [other] Workflow step: count occurrences of MS2 peaks and neutral losses to generate MS2 fingerprint, align fingerprints to compare samples.: "The occurrence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an *MS2 fingerprint* of the sample. These fingerprints can in a second stage be"
- [readme] Filtering and visualization techniques are applied after fingerprint alignment.: "different filtering (remove peaks/losses from blanks for example) and visualization techniques (MDS/PCoA, TMAP, Heatmap, ...) can be used"
- [readme] Matchms is used for importing and processing mass spectrometry data in multiple file formats.: "The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON."
- [readme] Python 3.8 is the minimum version required for MEMO.: "conda create --name memo python=3.8"
