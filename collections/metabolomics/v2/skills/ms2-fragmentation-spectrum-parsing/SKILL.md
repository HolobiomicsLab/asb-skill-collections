---
name: ms2-fragmentation-spectrum-parsing
description: Use when you have raw MS2 spectra in common formats (mzML, mzXML, msp, MGF, JSON) and need to convert them into normalized, queryable spectral objects for downstream analysis such as MS2 fingerprinting, spectral similarity scoring, or sample comparison.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3439
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - matchms
  - spec2vec
  - Python
  - numpy
  techniques:
  - tandem-MS
derived_from:
- doi: 10.3389/fbinf.2022.842964
  title: memo
evidence_spans:
- MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2 spectra
- MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2 spectra and converting them into documents.
- conda create --name memo python=3.8
- pip install numpy
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_memo_cq
    doi: 10.3389/fbinf.2022.842964
    title: memo
  dedup_kept_from: coll_memo_cq
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

# ms2-fragmentation-spectrum-parsing

## Summary

Parse and normalize MS2 fragmentation spectra from raw mass spectrometry files into structured spectral objects with validated metadata. This is the foundational step for any downstream MS2-based analysis, enabling extraction of peaks, neutral losses, and chemical metadata for fingerprinting or similarity scoring.

## When to use

You have raw MS2 spectra in common formats (mzML, mzXML, msp, MGF, JSON) and need to convert them into normalized, queryable spectral objects for downstream analysis such as MS2 fingerprinting, spectral similarity scoring, or sample comparison. Apply this skill when starting a metabolomics workflow where spectral data integrity, metadata consistency, and peak-loss extraction are prerequisites.

## When NOT to use

- Input is already a feature table or MS2 fingerprint (occurrence counts of peaks/losses across samples) — fingerprinting has already aggregated individual spectra.
- MS1 data only, without MS2 fragmentation spectra — this skill requires tandem MS data.
- Data from untargeted analyses where spectral parsing is not the bottleneck and generic import functions suffice.

## Inputs

- Raw MS2 spectra file (mzML, mzXML, msp, MGF, or JSON format)
- Sample metadata (precursor m/z, retention time, ionization mode, collision energy, polarity)

## Outputs

- Parsed and normalized Spectrum objects with metadata and peak lists
- Extracted m/z peaks per spectrum
- Computed neutral losses (precursor m/z − peak m/z) for each peak
- Validated spectral data ready for fingerprinting or similarity scoring

## How to apply

Load MS2 spectra from input sample files using matchms parsers that support mzML, mzXML, msp, MGF, and JSON formats. Apply matchms normalization functions to standardize metadata (precursor m/z, charge state, collision energy, ionization mode) and clean peak lists by removing artifacts and low-intensity noise. Extract all m/z peaks from each parsed MS2 spectrum and compute neutral losses by subtracting each peak m/z from the precursor m/z value. Validate that precursor masses and peak m/z values are within expected instrumental ranges and that no peaks exceed the precursor m/z. Serialize normalized spectra with their metadata and peak/neutral loss lists into structured formats (JSON or internal spectral objects) for downstream fingerprinting or comparison workflows.

## Related tools

- **matchms** (Primary parser and normalizer for MS2 spectra; handles multiple file formats (mzML, mzXML, msp, MGM, JSON) and standardizes metadata and peak lists) — https://github.com/matchms/matchms
- **Python** (Programming environment for script development and data manipulation during parsing workflow)
- **numpy** (Vectorized computation of neutral losses and peak statistics during spectrum processing)

## Examples

```
from matchms.importing_utils import load_from_msp; spectra = load_from_msp('sample.msp'); [print(s.precursor_mz, len(s.peaks)) for s in spectra[:5]]
```

## Evaluation signals

- All spectra have valid precursor m/z values and non-null peak lists after parsing.
- Neutral loss values (precursor m/z − peak m/z) are all non-negative and ≤ precursor m/z.
- Metadata fields (retention time, ionization mode, collision energy, charge state) are populated and consistent across all spectra.
- Output spectral objects can be serialized to JSON or CSV without errors and round-trip correctly.
- Peak m/z values are sorted in ascending order within each spectrum and match original raw spectra (within instrument precision).

## Limitations

- Parsing accuracy depends on correctness of the input file format and compliance with format specification; corrupted or non-standard files may fail to parse completely.
- Metadata cleaning and normalization heuristics in matchms may not handle all edge cases (e.g., missing precursor m/z, unrealistic charge states), potentially requiring manual curation.
- Very large spectra (thousands of peaks) may introduce computational overhead during neutral loss calculation; sparse peak filtering may be needed upstream.
- Different MS vendors and data acquisition softwares may produce non-standard metadata fields or peak representations that require vendor-specific preprocessing.

## Evidence

- [other] Load MS2 spectra from the input sample file using matchms to parse and normalize fragmentation data.: "Load MS2 spectra from the input sample file using matchms to parse and normalize fragmentation data."
- [readme] matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data (MS/MS).: "Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data (MS/MS)."
- [other] Extract all m/z peaks from each MS2 spectrum and compute neutral losses by subtracting each peak m/z from the precursor m/z.: "Extract all m/z peaks from each MS2 spectrum and compute neutral losses by subtracting each peak m/z from the precursor m/z."
- [readme] The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON.: "The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON."
- [readme] Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity.: "Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity."
