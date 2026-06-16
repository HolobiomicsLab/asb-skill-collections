---
name: mass-spectrometry-data-parsing
description: Use when you have raw mass spectrometry files in standard formats (mzML, mzXML, msp, MGF, JSON) and need to extract precursor m/z values, fragment peaks, neutral losses, retention times, and compound metadata into a structured, queryable spectrum object representation before performing MS/MS.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - matchms
  - spec2vec
  - Python 3.8
  - numpy
  - MEMO
  - memo-ms
derived_from:
- doi: 10.3389/fbinf.2022.842964
  title: memo
evidence_spans:
- MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2 spectra
- conda create --name memo python=3.8
- pip install numpy
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

# mass-spectrometry-data-parsing

## Summary

Parse raw MS/MS spectral data from common file formats (mzML, mzXML, msp, MGF, JSON) into spectrum objects with validated metadata and fragmentation peaks. This is the foundational step for all downstream MS/MS analysis workflows including fingerprinting, similarity scoring, and sample alignment.

## When to use

You have raw mass spectrometry files in standard formats (mzML, mzXML, msp, MGF, JSON) and need to extract precursor m/z values, fragment peaks, neutral losses, retention times, and compound metadata into a structured, queryable spectrum object representation before performing MS/MS fingerprinting, spectral alignment, or similarity comparisons.

## When NOT to use

- Input is already a processed feature table or peak intensity matrix — use parsing only on raw spectral data
- You have only MS1 (precursor ion) data without MS/MS fragmentation spectra — MEMO and downstream fingerprinting require MS2 fragment data
- Spectra have already been processed, aligned, and converted to sample-level fingerprint vectors — parsing is redundant at that stage

## Inputs

- Raw mass spectrometry files in mzML, mzXML, msp, MGF, or JSON format
- File paths or batch directory containing multiple spectra files
- Optional: noise threshold parameter (m/z intensity cutoff)

## Outputs

- Parsed Spectrum objects with precursor m/z, fragment m/z values, intensities, and metadata
- List or indexed collection of Spectrum objects organized by sample
- Validated spectrum metadata including retention time (if available) and compound identifiers

## How to apply

Use matchms to import and parse MS/MS spectra files, automatically extracting precursor m/z, fragment m/z values, intensity information, and available metadata. Apply metadata cleaning and validation to ensure consistency. Filter spectra by noise thresholds (removing low-intensity peaks below a defined signal level) to reduce spurious fragments. For each parsed spectrum, extract the precursor m/z to enable subsequent neutral loss calculations (fragment m/z subtracted from precursor m/z). Organize parsed spectra into a list or array structure indexed by sample origin for subsequent fingerprinting or alignment. Validation is successful when all spectra contain non-null precursor m/z, at least one fragment peak above noise threshold, and metadata fields required by downstream steps (e.g., sample identifier, scan number).

## Related tools

- **matchms** (Primary tool for importing, parsing, and validating MS/MS spectra from multiple file formats; extracts fragmentation data and metadata into Spectrum objects) — https://github.com/matchms/matchms
- **MEMO** (Orchestrates the overall MS2-based sample vectorization workflow; builds on matchms for spectrum parsing as a prerequisite step) — https://github.com/mandelbrot-project/memo
- **memo-ms** (Python package distribution of MEMO; wraps matchms parsing and spectrum processing utilities) — https://pypi.org/project/memo-ms/
- **spec2vec** (Consumes parsed Spectrum objects from matchms to compute spectral embeddings and similarity scores based on fragment relationships) — https://github.com/iomega/spec2vec

## Examples

```
from matchms.importing_utils import load_from_msp; spectra = list(load_from_msp('spectra.msp'))
```

## Evaluation signals

- All parsed Spectrum objects contain non-null precursor m/z and at least one fragment peak with m/z and intensity values above the specified noise threshold
- Spectrum metadata fields (retention time, compound name, scan number, sample identifier) are populated and consistent with input file content
- Fragment m/z values are strictly less than precursor m/z (neutral losses = precursor m/z − fragment m/z are positive and reasonable)
- Spectra are successfully indexed and retrievable by sample identifier for subsequent fingerprinting
- File import completes without parsing errors or dropped spectra; total spectrum count matches expected count from input file directory

## Limitations

- Parsing accuracy depends on file format compliance; malformed or non-standard spectral files may fail to import or produce incomplete metadata
- Metadata cleaning and intensity filtering thresholds must be tuned per instrument type and LC-MS method; no universal noise cutoff is appropriate for all data
- MEMO and downstream fingerprinting are designed for LC-MS/MS data and assume retention time variability across samples; direct MS analysis (no chromatography) is not addressed in the published examples
- Large-scale parsing of hundreds of thousands of spectra may require sparse or streaming approaches; memory footprint grows with spectrum count

## Evidence

- [readme] Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data (MS/MS).: "Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data (MS/MS)"
- [readme] Matchms supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON.: "The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON"
- [other] Load MS2 spectra files using matchms to parse fragmentation data. Iterate through spectra in each sample and extract precursor m/z values.: "1. Load MS2 spectra files using matchms to parse fragmentation data. 2. Iterate through spectra in each sample and extract precursor m/z values"
- [other] Count occurrences of all MS2 peaks (m/z values above noise threshold) in each spectrum. Calculate neutral losses by subtracting observed fragment m/z from precursor m/z for each peak.: "3. Count occurrences of all MS2 peaks (m/z values above noise threshold) in each spectrum. 4. Calculate neutral losses by subtracting observed fragment m/z from precursor m/z for each peak"
- [readme] Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity.: "Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity"
