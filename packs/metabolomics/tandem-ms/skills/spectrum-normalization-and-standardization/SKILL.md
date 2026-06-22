---
name: spectrum-normalization-and-standardization
description: Use when you have raw MS2 spectra in common formats (mzML, mzXML, msp, MGF, JSON) from one or more metabolomics samples, and you need to prepare them for MS2 fingerprint generation, similarity scoring, or cross-sample comparison.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
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

# spectrum-normalization-and-standardization

## Summary

Normalize and standardize MS2 fragmentation spectra using matchms to parse, clean, and standardize spectral metadata and peak intensity values before downstream analysis. This ensures consistent data representation across samples acquired with different MS technologies, LC methods, or instrument configurations.

## When to use

You have raw MS2 spectra in common formats (mzML, mzXML, msp, MGF, JSON) from one or more metabolomics samples, and you need to prepare them for MS2 fingerprint generation, similarity scoring, or cross-sample comparison. This is especially important when combining data from different LC methods, mass spectrometer technologies (e.g., Q-ToF vs Orbitrap), or when performing RT-agnostic alignment.

## When NOT to use

- Input spectra are already normalized and validated in a downstream format (e.g., already processed feature tables or pre-computed similarity matrices).
- You are performing purely computational tasks that do not require spectral metadata standardization (e.g., matrix algebra on pre-computed scores).
- Your workflow operates entirely on retention-time aligned, feature-detected data and does not need to compare samples acquired under different LC or MS conditions.

## Inputs

- MS2 spectra in mzML, mzXML, msp, MGF, or JSON format
- Raw fragmentation spectra from metabolomics samples

## Outputs

- Cleaned and standardized MS2 spectra objects
- Spectra with validated metadata (precursor m/z, charge, compound info)
- Peak-filtered spectra ready for fingerprint or similarity analysis

## How to apply

Load MS2 spectra from input sample files using matchms parsers to import spectra in supported formats (mzML, mzXML, msp, MGF, JSON). Apply matchms metadata cleaning and validation functions to standardize fields such as precursor m/z, charge state, and compound metadata. Apply basic peak filtering to remove noise and ensure data integrity. The normalized spectra are then ready for peak extraction, neutral loss calculation, or feeding into downstream tools like spec2vec for spectral similarity scoring or fingerprint generation. Normalization reduces artifacts introduced by different acquisition protocols and improves reproducibility of cross-sample comparisons.

## Related tools

- **matchms** (Primary library for parsing, cleaning, and normalizing MS2 spectra; applies metadata validation and peak filtering) — https://github.com/matchms/matchms
- **Python** (Runtime environment and scripting language for invoking matchms workflows)
- **numpy** (Numerical computation library used by matchms for array operations on peak intensities and m/z values)
- **spec2vec** (Optional downstream tool that consumes normalized spectra for spectral similarity scoring based on fragment embeddings) — https://github.com/iomega/spec2vec

## Examples

```
from matchms.importing import load_from_msp
from matchms.processing import normalize_intensities, remove_losses, default_filters
spectra = list(load_from_msp('sample.msp'))
spectra = [normalize_intensities(s) for s in spectra]
spectra = [remove_losses(s) for s in spectra]
spectra = [default_filters(s) for s in spectra]
```

## Evaluation signals

- All spectra successfully parse without errors using matchms importers for the input file format (mzML, mzXML, msp, MGF, or JSON).
- Metadata fields (precursor m/z, charge state, compound name, inchikey) are populated and validated across all spectra; missing or invalid entries are flagged or set to default values.
- Peak lists are filtered to remove low-intensity noise; verify that peak count distributions are consistent and no spectra are empty after filtering.
- Normalized spectra can be compared across samples without RT-dependent artifacts; verify using RT-agnostic comparison (e.g., fingerprint or spec2vec similarity) that samples with different LC or MS acquisition methods now show expected chemical similarities.
- Output spectra conform to matchms Spectrum object schema and can be serialized without loss; spot-check by writing to MGF or JSON and re-importing to confirm round-trip integrity.

## Limitations

- Normalization does not recover information from spectra with missing or corrupted precursor m/z values; such spectra must be excluded or handled with imputation strategies not described in MEMO.
- Peak filtering thresholds are configurable but not explicitly specified in the MEMO paper; practitioners must select appropriate noise cutoffs based on their instrument sensitivity and sample characteristics.
- Standardization relies on consistent metadata encoding in input files; malformed or non-standard metadata annotations may not be caught by matchms validation and could propagate downstream errors.
- Different MS technologies (Q-ToF vs Orbitrap) produce different mass accuracies and fragmentation patterns; normalization standardizes representation but does not harmonize inherent instrumental biases, which may still affect peak/loss counts in fingerprints.

## Evidence

- [readme] matchms is described as a library for importing, processing, cleaning, and comparing mass spectrometry data, supporting formats including mzML, mzXML, msp, MGM, and JSON.: "Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data (MS/MS). It facilitates the implementation of straightforward,"
- [readme] Matchms provides metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity.: "Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity."
- [other] MEMO workflow step one involves loading MS2 spectra using matchms and normalizing fragmentation data.: "Load MS2 spectra from the input sample file using matchms to parse and normalize fragmentation data."
- [other] MEMO is built on matchms and spec2vec for handling MS2 spectra.: "MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2 spectra"
- [intro] MEMO's purpose includes enabling retention time agnostic alignment by using MS2 fragmentation spectra, which requires standardized spectral representation.: "MEMO is a method allowing a Retention Time (RT) agnostic alignment of metabolomics samples using the fragmentation spectra (MS2)"
- [intro] MEMO suits comparison of samples from different LC methods or MS technologies, implying that spectral normalization is essential for cross-platform comparisons.: "MEMO suits particularly well to compare chemodiverse samples, ie with a poor features overlap, or to compare samples with a strong RT shift, acquired using different LC methods or even different mass"
