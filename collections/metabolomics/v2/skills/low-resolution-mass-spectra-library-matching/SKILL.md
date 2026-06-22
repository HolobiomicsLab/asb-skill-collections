---
name: low-resolution-mass-spectra-library-matching
description: Use when when processing low-resolution GC-MS data in NetCDF format where you have already performed retention-index calibration and peak deconvolution, and you need to assign compound identities by comparing experimental mass spectra to a curated reference library such as PNNLMetV20191015.MSL.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  tools:
  - Docker
  - CoreMS
  - pandas
  - numpy
derived_from:
- doi: 10.5281/zenodo.14009575
  title: corems
evidence_spans:
- from corems.encapsulation.factory.parameters import MSParameters
- CoreMS [section=results; evidence='from corems.encapsulation.factory.parameters import MSParameters']
- import pandas as pd
- pandas [section=results; evidence='import pandas as pd']
- import numpy as np
- numpy [section=results; evidence='import numpy as np']
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_corems
    doi: 10.5281/zenodo.14009575
    title: corems
  dedup_kept_from: coll_corems
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.5281/zenodo.14009575
  all_source_dois:
  - 10.5281/zenodo.14009575
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# low-resolution-mass-spectra-library-matching

## Summary

Identify unknown compounds in low-resolution GC-MS data by matching extracted mass spectra against a reference spectral library using cosine similarity and retention-index proximity scoring. This skill enables automated compound annotation when high-resolution mass accuracy is unavailable.

## When to use

When processing low-resolution GC-MS data in NetCDF format where you have already performed retention-index calibration and peak deconvolution, and you need to assign compound identities by comparing experimental mass spectra to a curated reference library such as PNNLMetV20191015.MSL.

## When NOT to use

- Input spectra are high-resolution (e.g., Orbitrap, FT-ICR) — use molecular formula assignment instead of spectral library matching.
- Reference library is absent or incompatible with your instrument or ionization mode.
- Peak deconvolution has not been performed; overlapping peaks will produce unreliable spectra and false matches.

## Inputs

- Raw GC-MS data in NetCDF format (ANDI-MS .cdf file)
- Calibrated retention indices for each detected peak
- Low-resolution mass spectra extracted from deconvolved peaks
- Reference spectral library (e.g., PNNLMetV20191015.MSL, SQLite or file-based format)

## Outputs

- Compound identification table (CSV or HDF5) with columns: m/z, retention index, compound name, CAS number, spectral match score, match rank
- Annotated mass spectrum objects with matched library entry metadata
- Match quality metrics (cosine similarity score, RI difference)

## How to apply

Extract the low-resolution mass spectrum from each detected chromatographic peak after baseline subtraction and peak deconvolution. Perform LowResMassSpectralMatch against a reference spectral library (e.g., PNNLMetV20191015.MSL), scoring each candidate match using cosine similarity of fragment ion patterns combined with retention-index proximity to the experimental peak's calibrated RI. Rank matches by combined score and retain the top candidate(s), filtering by a cosine similarity threshold (typically > 0.7) and RI match tolerance. Aggregate results into a structured table recording compound name, CAS number, retention index, spectral match score, and match rank for downstream validation and reporting.

## Related tools

- **CoreMS** (Provides LowResMassSpectralMatch class, retention-index calibration (get_rt_ri_pairs), and data I/O (ReadAndiNetCDF, CSV/HDF5 export)) — https://github.com/EMSL-Computing/CoreMS
- **pandas** (Aggregates and structures match results into tables for export and downstream analysis)
- **numpy** (Underlying numerical operations for cosine similarity calculation and score aggregation)
- **Docker** (Containerizes CoreMS with all dependencies for reproducible execution across platforms)

## Examples

```
from corems.data_structure.raw_data import ReadAndiNetCDF
from corems.encapsulation.factory.parameters import MSParameters
raw_data = ReadAndiNetCDF('sample.cdf')
raw_data.apply_gaussian_smoothing()
for spectrum in raw_data:
    matches = spectrum.LowResMassSpectralMatch('PNNLMetV20191015.MSL')
    print(f"Top match: {matches[0]['compound_name']} (score={matches[0]['cosine_similarity']})")
```

## Evaluation signals

- All peaks in the input dataset receive a match result (coverage check); verify no peaks are skipped due to missing or malformed spectra.
- Cosine similarity scores for top matches fall within the expected range (typically 0.5–1.0); verify no erroneous scores outside [0, 1].
- Retention-index differences between experimental and matched library entries are within the configured tolerance (e.g., ±100 RI units for GC-MS); check RI_difference column against tolerance threshold.
- Compound names, CAS numbers, and metadata fields are populated correctly and match the reference library format; spot-check a sample of rows for accuracy and against known standards if available.
- Output table schema matches expected columns (m/z, retention index, compound name, CAS number, spectral match score, match rank) and data types are consistent.

## Limitations

- Low-resolution mass spectra contain limited fragmentation detail; matches may be ambiguous or incorrect for structural isomers or compounds with very similar spectra.
- Spectral library coverage is incomplete; novel or rare compounds absent from the reference library will fail to match or produce low-confidence matches.
- Retention-index calibration quality directly affects match fidelity; poor RI calibration or uncalibrated data will increase false matches and false negatives.
- Cosine similarity alone does not account for instrument-specific ionization efficiency or peak intensity variations; preprocessing (normalization, baseline subtraction) affects reproducibility.
- Reference library may contain outdated, redundant, or incorrect entries; matches should be validated against independent confirmation methods (e.g., standards, GC-retention time databases, literature).

## Evidence

- [other] Extract low-resolution mass spectra from each peak and perform LowResMassSpectralMatch against the PNNLMetV20191015.MSL spectral library, scoring matches by cosine similarity and retention-index proximity.: "Extract low-resolution mass spectra from each peak and perform LowResMassSpectralMatch against the PNNLMetV20191015.MSL spectral library, scoring matches by cosine similarity and retention-index"
- [other] Load raw GC-MS data in NetCDF format using ReadAndiNetCDF, parsing instrument parameters and chromatographic signals. Apply GC_RI_Calibration to align retention times against reference alkane standards and compute retention indices for each detected peak.: "Load raw GC-MS data in NetCDF format using ReadAndiNetCDF, parsing instrument parameters and chromatographic signals. Apply GC_RI_Calibration to align retention times against reference alkane"
- [other] Aggregate results into a structured table with compound name, CAS number, retention index, spectral match score, and match rank.: "Aggregate results into a structured table with compound name, CAS number, retention index, spectral match score, and match rank."
- [readme] Automatic molecular match algorithm with all spectral similarity methods: "Automatic molecular match algorithm with all spectral similarity methods"
- [readme] ANDI NetCDF for GC-MS (.cdf): "ANDI NetCDF for GC-MS (.cdf)"
