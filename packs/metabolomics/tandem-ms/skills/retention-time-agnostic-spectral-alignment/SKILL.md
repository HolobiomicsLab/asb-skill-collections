---
name: retention-time-agnostic-spectral-alignment
description: Use when you have MS2 fragmentation spectra from multiple samples (in .mgf, .mzML, or .mzXML format) and want to compare them despite poor feature overlap, strong RT shifts between acquisitions, or use of different LC-MS platforms (e.g., Orbitrap vs. Q-ToF).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3932
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - matchms
  - spec2vec
  - Python 3.8
  - numpy
  - scikit-bio
  - memo-ms
  - TMAP
  techniques:
  - LC-MS
  - tandem-MS
derived_from:
- doi: 10.3389/fbinf.2022.842964
  title: memo
evidence_spans:
- MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2 spectra
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# retention-time-agnostic-spectral-alignment

## Summary

Generate MS2-based sample fingerprints by counting MS2 peaks and neutral losses, then align these fingerprints to enable cross-sample comparison without requiring retention time (RT) alignment. This approach is particularly suited for comparing chemically diverse samples acquired across different LC methods or mass spectrometer technologies.

## When to use

You have MS2 fragmentation spectra from multiple samples (in .mgf, .mzML, or .mzXML format) and want to compare them despite poor feature overlap, strong RT shifts between acquisitions, or use of different LC-MS platforms (e.g., Orbitrap vs. Q-ToF). RT-dependent alignment is infeasible or unnecessary for your research question.

## When NOT to use

- Input spectra are already in a pre-aligned feature table or sample-by-feature matrix format.
- Retention time is a critical classifier in your analysis and must be preserved as a dimension.
- You are working exclusively with MS1-level (precursor ion) data without MS2 fragmentation spectra available.

## Inputs

- MS2 spectra files (mzML, mzXML, or MGF format)
- Sample metadata (sample identifiers, class labels, or batch information)
- Blank/control sample data (optional, for filtering contaminant peaks)

## Outputs

- MemoMatrix object (sample-by-feature matrix with MS2 fingerprints)
- Aligned MS2 peak and neutral loss feature table
- Sample distance/similarity matrix (for downstream visualization or clustering)

## How to apply

First, load unaligned MS2 spectra files using matchms to parse and extract fragmentation peak data and precursor mass information. Count the occurrence of each distinct MS2 peak (m/z value) and neutral loss (mass difference from precursor ion) within each sample to generate a binary or count-based MS2 fingerprint. Execute the memo_from_unaligned function from the memo-ms package to align fingerprints across samples into a MemoMatrix object with sample-by-feature dimensionality. Optionally apply filtering steps (e.g., remove peaks/losses present in blank samples) and then visualize using MDS/PCoA, TMAP, or heatmap techniques to assess sample similarities.

## Related tools

- **memo-ms** (Executes memo_from_unaligned function to construct MemoMatrix objects by aligning MS2 fingerprints across samples) — https://github.com/mandelbrot-project/memo
- **matchms** (Parses MS2 spectra files, extracts fragmentation peaks and precursor information, supports multiple spectral formats (mzML, mzXML, MGF)) — https://github.com/matchms/matchms
- **spec2vec** (Provides spectral similarity scoring based on fragmental relationships; optional advanced metric for post-alignment comparison) — https://github.com/iomega/spec2vec
- **TMAP** (Visualization tool for interactive 2D/3D projection of aligned MemoMatrix samples)
- **numpy** (Numerical computation and matrix operations for fingerprint counting and aggregation)
- **scikit-bio** (Beta diversity and distance metric calculations for sample comparison post-alignment)

## Examples

```
from memo_ms import memo_from_unaligned; memo_matrix = memo_from_unaligned(mzml_files=['sample1.mzML', 'sample2.mzML'], output_format='MemoMatrix')
```

## Evaluation signals

- MemoMatrix object has expected dimensionality: number of rows equals number of samples, number of columns equals total unique MS2 peaks and neutral losses across all samples.
- All sample identifiers and metadata attributes are correctly preserved and mapped in the MemoMatrix.
- Peak count distributions show reasonable ranges (no samples with zero peaks, no extreme outliers suggesting parsing errors).
- Downstream distance/similarity metrics (e.g., Bray–Curtis, Jaccard) computed from the MemoMatrix separate known biological or technical groups appropriately, or show expected structure in TMAP/PCoA plots.
- Filtering step (e.g., removal of blank-associated peaks) demonstrably reduces noise, visible as improved clustering or reduced background features in visualizations.

## Limitations

- MEMO requires MS2 spectra; samples with poor fragmentation or very low intensity peaks may yield sparse, uninformative fingerprints.
- Alignment is agnostic to RT but does not exploit RT information if present; a sample with identical chemistry but different RT values is treated equivalently.
- Peak counting is sensitive to mass calibration; significant calibration drift (>10 ppm) across samples can lead to fragmentation of m/z features and inflation of feature dimensionality.
- TMAP visualization is available only on macOS and Linux; Windows users require WSL (Windows Subsystem for Linux).
- Performance scales with total number of unique peaks and samples; very large datasets (>10,000 samples or >100,000 unique features) may require memory optimization or sparse matrix implementations.

## Evidence

- [readme] a method allowing a Retention Time (RT) agnostic alignment of metabolomics samples using the fragmentation spectra (MS2) of their consituents: "**M**\ s2 bas\ **E**\ d sa\ **M**\ ple vect\ **O**\ rization (**MEMO**) is a method allowing a Retention Time (RT) agnostic alignment of metabolomics samples"
- [readme] The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an MS2 fingerprint: "The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an *MS2 fingerprint* of the sample"
- [readme] These fingerprints can in a second stage be aligned to compare different samples: "These fingerprints can in a second stage be aligned to compare different samples"
- [readme] MEMO suits particularly well to compare chemodiverse samples, ie with a poor features overlap, or to compare samples with a strong RT shift, acquired using different LC methods or even different mass spectrometers: "MEMO suits particularly well to compare chemodiverse samples, ie with a poor features overlap, or to compare samples with a strong RT shift, acquired using different LC methods or even different mass"
- [other] Load unaligned MS2 spectra files in a format supported by matchms, then parse using matchms to extract MS2 fragmentation data and precursor information: "Load unaligned MS2 spectra files in a format supported by matchms (e.g., .mgf, .mzML, .mzXML). 2. Parse spectra using matchms to extract MS2 fragmentation data and precursor information"
- [other] Count occurrences of MS2 peaks and neutral losses across all spectra in each sample to generate MS2 fingerprints, then execute memo_from_unaligned to align fingerprints: "Count occurrences of MS2 peaks and neutral losses (mass differences to precursor) across all spectra in each sample to generate MS2 fingerprints. 4. Execute memo_from_unaligned function from memo-ms"
- [readme] Filtering (remove peaks/losses from blanks for example) and visualization techniques (MDS/PCoA, TMAP, Heatmap) can be used: "different filtering (remove peaks/losses from blanks for example) and visualization techniques (MDS/PCoA, TMAP, Heatmap, ...) can be used"
- [other] MEMO is mainly built on matchms and spec2vec packages for handling the MS2 spectra: "MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2 spectra"
