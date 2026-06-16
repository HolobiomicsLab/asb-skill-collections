---
name: ms2-spectra-parsing-and-loading
description: Use when when beginning a MEMO analysis workflow with raw or unaligned MS2 spectra files and needing to extract fragmentation data and precursor information before counting MS2 peaks and neutral losses to generate sample fingerprints.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - matchms
  - spec2vec
  - Python 3.8
  - numpy
  - scikit-bio
  - memo-ms
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
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_memo
    doi: 10.3389/fbinf.2022.842964
    title: memo
  dedup_kept_from: coll_memo
schema_version: 0.2.0
---

# MS2 Spectra Parsing and Loading

## Summary

Load and parse tandem mass spectrometry (MS2) spectra files in standardized formats (mzML, mzXML, MGF) using the matchms library to extract MS2 fragmentation peaks, neutral losses, and precursor metadata for downstream sample vectorization and comparison.

## When to use

When beginning a MEMO analysis workflow with raw or unaligned MS2 spectra files and needing to extract fragmentation data and precursor information before counting MS2 peaks and neutral losses to generate sample fingerprints. Use this skill as the first step before constructing a MemoMatrix.

## When NOT to use

- Input spectra are already parsed as Python matchms Spectrum objects — pass them directly to memo_from_unaligned without re-parsing.
- Working with MS1-only or untargeted metabolomics data without tandem fragmentation spectra.
- Input is already a feature table or abundance matrix (e.g., from XCMS or MZmine) — use MEMO only on raw or library-matched MS2 spectra.

## Inputs

- MS2 spectra file in mzML format
- MS2 spectra file in mzXML format
- MS2 spectra file in MGF (Mascot Generic Format)
- MS2 spectra file in msp format
- MS2 spectra file in metabolomics-USI format
- MS2 spectra file in JSON format

## Outputs

- Parsed spectra objects (matchms Spectrum class instances)
- Spectrum metadata (precursor m/z, charge, retention time)
- MS2 peak lists with intensities

## How to apply

Import MS2 spectra files in formats supported by matchms (mzML, mzXML, MGF, msp, metabolomics-USI, or JSON) using the matchms library's import functions. Parse the spectra to extract MS2 fragmentation peak lists, precursor m/z and charge, and associated metadata. The parsed spectra objects retain both spectral data (peaks and intensities) and metadata needed for subsequent fingerprinting. Validate the loaded spectra by checking that peaks are present, precursor information is populated, and the number of loaded spectra matches expectations. The parsed spectra are then passed directly to the MEMO fingerprinting stage (memo_from_unaligned), which counts peak and neutral loss occurrences across the sample.

## Related tools

- **matchms** (Core library for importing, parsing, and handling MS2 spectra objects from multiple file formats) — https://github.com/matchms/matchms
- **memo-ms** (Downstream tool that accepts parsed spectra to generate MS2 fingerprints and MemoMatrix alignment) — https://github.com/mandelbrot-project/memo

## Examples

```
from matchms.importing import load_from_mgf; spectra = list(load_from_mgf('unaligned_spectra.mgf')); from memo import memo_from_unaligned; memo_matrix = memo_from_unaligned(spectra)
```

## Evaluation signals

- All spectra are successfully loaded into matchms Spectrum objects with non-null precursor m/z and charge state.
- Peak lists contain expected fragmentation patterns (e.g., presence of product ions, neutral losses relative to precursor m/z).
- Loaded spectra count matches the expected number of MS/MS scans in the input file.
- Metadata fields (precursor_mz, charge, retention_time, spectrum_id) are populated where present in the input file.
- Parsed spectra can be passed without error to memo_from_unaligned() and produce a valid MemoMatrix with correct sample-by-feature dimensionality.

## Limitations

- Parsing accuracy depends on file format compliance; malformed or corrupted MS2 files may fail to load or produce incomplete spectra.
- Retention time (RT) information is parsed but not used by MEMO, which is designed to be RT-agnostic; RT fields are retained only for reference.
- Large files (hundreds of thousands of spectra) may require memory optimization; matchms supports sparse array handling in recent versions but parsing time scales linearly with file size.
- File format support is limited to mzML, mzXML, MGF, msp, metabolomics-USI, and JSON; other vendor-specific formats (e.g., raw Thermo files) require prior conversion.

## Evidence

- [other] Load unaligned MS2 spectra files in a format supported by matchms (e.g., .mgf, .mzML, .mzXML): "Load unaligned MS2 spectra files in a format supported by matchms (e.g., .mgf, .mzML, .mzXML). 2. Parse spectra using matchms to extract MS2 fragmentation data and precursor information."
- [other] MEMO is mainly built on matchms and spec2vec packages for handling the MS2 spectra: "MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2 spectra"
- [readme] matchms is a versatile open-source Python package for importing, processing, cleaning, and comparing mass spectrometry data (MS/MS): "Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data (MS/MS)."
- [readme] matchms supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON: "The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON."
- [other] The occurrence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an MS2 fingerprint: "The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an *MS2 fingerprint* of the sample"
