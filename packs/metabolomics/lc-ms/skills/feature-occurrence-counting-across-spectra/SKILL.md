---
name: feature-occurrence-counting-across-spectra
description: Use when when you have parsed MS2 spectra from a single metabolomics sample (via matchms or similar) and need to generate a sample-level feature vector that represents the chemical composition independently of chromatographic alignment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - matchms
  - spec2vec
  - Python
  - numpy
  - MEMO
  techniques:
  - LC-MS
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

# feature-occurrence-counting-across-spectra

## Summary

Count the occurrence of MS2 peaks and neutral losses across all spectra within a metabolomics sample to generate a sample-level MS2 fingerprint. This aggregation enables retention-time-agnostic sample comparison and is particularly useful for chemodiverse datasets with poor feature overlap or strong retention time shifts.

## When to use

When you have parsed MS2 spectra from a single metabolomics sample (via matchms or similar) and need to generate a sample-level feature vector that represents the chemical composition independently of chromatographic alignment. Use this when comparing samples acquired on different LC methods, mass spectrometers, or with significant retention time drift, or when features show poor overlap across samples.

## When NOT to use

- Input is already a pre-computed feature table or fingerprint (avoid double-counting).
- Spectra have not yet been parsed or normalized (use matchms preprocessing first).
- Sample contains only a single MS2 spectrum (occurrence counting requires multiple spectra for meaningful aggregation).

## Inputs

- MS2 spectra file (mzML, mzXML, msp, MGF, or JSON format)
- Sample identifier or batch of spectra from a single sample

## Outputs

- MS2 fingerprint: dictionary or feature vector mapping peak m/z values to occurrence counts
- MS2 fingerprint: dictionary or feature vector mapping neutral loss values to occurrence counts
- Serialized fingerprint (JSON or CSV file) with peak/loss identifiers and their frequencies

## How to apply

Load all MS2 spectra from the sample file using matchms to parse and normalize fragmentation data. Extract all m/z peak values from each spectrum and compute neutral losses by subtracting each peak m/z from its precursor m/z value. Iterate through all spectra in the sample and count the total occurrences of each unique peak m/z and neutral loss identifier, accumulating these counts in a dictionary or feature vector. Aggregate these counts such that each peak/loss identifier maps to its total frequency across the entire sample. Finally, serialize the resulting MS2 fingerprint (peak/loss identifiers with their occurrence counts) as a structured output (JSON or CSV) for downstream alignment and comparison steps.

## Related tools

- **matchms** (Parses, normalizes, and extracts m/z peaks and metadata from raw MS2 spectra files in multiple formats (mzML, mzXML, msp, MGF, JSON)) — https://github.com/matchms/matchms
- **spec2vec** (Provides spectral embedding and similarity measures that build on MS2 fingerprints and neutral loss relationships for downstream sample comparison) — https://github.com/iomega/spec2vec
- **MEMO** (Implements the full MS2 fingerprint generation and sample vectorization workflow, including occurrence counting and aggregation) — https://github.com/mandelbrot-project/memo
- **numpy** (Provides efficient array operations for counting and aggregating peak/loss frequencies into feature vectors)
- **Python** (Core language for scripting the occurrence counting workflow; MEMO requires Python >= 3.8)

## Examples

```
from matchms.importing_utils import load_from_json; from memo import fingerprint_from_spectra; spectra = load_from_json('sample.json'); fingerprint = fingerprint_from_spectra(spectra); import json; json.dump(fingerprint, open('ms2_fingerprint.json', 'w'))
```

## Evaluation signals

- Verify that the count for each peak m/z or neutral loss is a positive integer ≥ 1 (no zero-occurrence features should be present in the fingerprint).
- Confirm that the sum of all occurrence counts equals the total number of MS2 spectra in the sample (each spectrum contributes peaks and losses).
- Check that neutral loss values are all positive and less than or equal to the precursor m/z (no negative or out-of-range losses).
- Validate that peak m/z values fall within the expected mass range for the MS instrument (e.g., 50–2000 m/z for typical metabolomics).
- Ensure the serialized fingerprint contains only non-redundant (unique) peak and loss identifiers with no duplicate keys in the output dictionary or feature vector.

## Limitations

- Occurrence counting discards intensity and mass accuracy information from individual peaks, retaining only presence/absence and frequency.
- The method is retention-time agnostic by design but may conflate isobaric compounds that produce identical MS2 fragmentation patterns.
- Requires normalization and quality filtering of input spectra (e.g., removal of low-quality spectra) to avoid noise skewing fingerprint composition; filtering of peaks/losses from blank samples is recommended to reduce systematic background.
- Neutral loss calculation depends on accurate precursor m/z assignment; errors in precursor mass directly propagate to neutral loss counts.

## Evidence

- [intro] The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an *MS2 fingerprint*: "The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an *MS2 fingerprint*"
- [other] Extract all m/z peaks from each MS2 spectrum and compute neutral losses by subtracting each peak m/z from the precursor m/z. Count the total occurrences of each unique peak m/z and neutral loss value across all spectra in the sample.: "Extract all m/z peaks from each MS2 spectrum and compute neutral losses by subtracting each peak m/z from the precursor m/z. Count the total occurrences of each unique peak m/z and neutral loss value"
- [other] MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2 spectra: "MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2 spectra"
- [other] MEMO suits particularly well to compare chemodiverse samples, ie with a poor features overlap, or to compare samples with a strong RT shift: "MEMO suits particularly well to compare chemodiverse samples, *i.e.* with a poor features overlap, or to compare samples with a strong RT shift"
- [intro] different filtering (remove peaks/losses from blanks for example) and visualization techniques (MDS/PCoA, TMAP, Heatmap, ...) can be used: "different filtering (remove peaks/losses from blanks for example) and visualization techniques (MDS/PCoA, TMAP, Heatmap, ...) can be used"
