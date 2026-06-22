---
name: compound-identification-from-ms-data
description: Use when you have raw GC-MS or LC-MS data in vendor format (NetCDF, .raw, .d) or generic mass lists, and you need to assign chemical identities to detected peaks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3647
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - Docker
  - CoreMS
  - pandas
  - numpy
  - MetaMS
  - EnviroMS
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
---

# compound-identification-from-ms-data

## Summary

Automated identification of small-molecule compounds from mass spectrometry data via spectral library matching and retention index calibration. This skill applies cosine similarity and retention-index proximity scoring to assign compound names, CAS numbers, and match ranks from low-resolution GC-MS or high-resolution LC-MS spectra.

## When to use

You have raw GC-MS or LC-MS data in vendor format (NetCDF, .raw, .d) or generic mass lists, and you need to assign chemical identities to detected peaks. Specifically, use this skill when you have retention time or retention index information available and access to a spectral reference library (e.g., PNNLMetV20191015.MSL, NIST MS library, or a custom spectral database).

## When NOT to use

- Input data lacks retention time or retention index information (RI matching is a key discrimination step; without it, false positives increase significantly).
- Spectral library is unavailable or does not cover the expected compound classes in your sample.
- Data is from high-resolution accurate-mass instruments where elemental formula assignment (rather than library matching) is more appropriate and efficient.

## Inputs

- Raw GC-MS data in ANDI NetCDF format (.cdf)
- Raw LC-MS data in mzML format (.mzml)
- Vendor raw files (Thermo .raw, Bruker .d)
- Generic mass list (CSV, Excel, tab-delimited with m/z, intensity, retention time)
- Reference spectral library (MSL, NIST format, or CoreMS-compatible database)

## Outputs

- Structured compound match table (CSV, Excel, HDF5 with columns: m/z, retention index, compound name, CAS number, spectral match score, match rank)
- Pandas DataFrame with annotated mass spectra
- CoreMS self-containing HDF5 file with raw data, processed spectra, and metadata

## How to apply

Load raw mass spectrometry data via ReadAndiNetCDF (GC-MS NetCDF) or equivalent vendor parser. Apply retention index calibration using reference alkane standards (get_rt_ri_pairs function) to align retention times and compute normalized retention indices for each detected peak. Extract mass spectra from each peak and perform spectral matching via LowResMassSpectralMatch class, scoring each candidate against the reference library by cosine similarity of peak m/z patterns and proximity of observed vs. reference retention indices. Aggregate results into a structured table reporting compound name, CAS number, retention index, spectral match score (typically 0–1 range), and match rank. Filter results by applying score thresholds (e.g., cosine similarity > 0.7 or user-defined cutoff) and inspect rank 1 hits as primary assignments.

## Related tools

- **CoreMS** (Python framework providing ReadAndiNetCDF, GC_RI_Calibration, LowResMassSpectralMatch, and data structures for GC-MS and LC-MS compound identification workflows) — https://github.com/EMSL-Computing/CoreMS
- **MetaMS** (Workflow repository for metabolomics and GC-MS data processing, wrapping CoreMS with standardized compound identification pipelines) — https://github.com/EMSL-Computing/MetaMS
- **EnviroMS** (Workflow for natural organic matter annotation using molecular formula assignment; complementary to spectral library matching for high-resolution MS data) — https://github.com/EMSL-Computing/EnviroMS
- **pandas** (Data aggregation and export of compound match results into CSV, Excel, and pickle formats)
- **numpy** (Numerical computation support for cosine similarity scoring and retention index calculations)
- **Docker** (Containerization for reproducible CoreMS execution with consistent library versions and database backends)

## Examples

```
from corems.encapsulation.factory.parameters import MSParameters; from corems.gcms.adapter import ReadAndiNetCDF; gc_ms = ReadAndiNetCDF('sample.cdf'); gc_ms.apply_tic_filter(min_abundance=100); gc_ms.run(); results = gc_ms.to_dataframe(); results.to_csv('compound_identifications.csv')
```

## Evaluation signals

- Verify that output compound table has no null values in mandatory columns (compound name, CAS number, retention index, spectral match score) and that match scores are in the expected range (0–1 for cosine similarity).
- Cross-check top-ranked compound assignments against external databases (PubChem, ChemSpider) to confirm plausibility of chemical names and CAS numbers.
- Inspect retention index deviations: observed RI should fall within ±5–10 index units of the reference library value for correct matches (acceptable tolerance depends on instrument and calibration quality).
- Compare spectral match scores for rank 1 vs. rank 2 candidates; a large gap (>0.2–0.3) indicates confident assignment; a small gap suggests ambiguity or presence of isomers.
- Validate a random subset of identifications by manual review of the raw mass spectrum vs. the reference spectrum in the library, assessing peak pattern agreement visually.

## Limitations

- Spectral library coverage is incomplete; compounds absent from the reference library will not be identified, even if present in the sample.
- Cosine similarity matching is sensitive to noise and baseline artifacts; low signal-to-noise ratio or poor peak deconvolution degrades match scores.
- Retention index calibration requires high-quality alkane standard data; missing or distorted RI peaks will introduce systematic errors in RI values and reduce match discrimination.
- Structural isomers often share identical or very similar mass spectra; RI alone may not resolve ambiguity; chemical context or orthogonal methods (e.g., GC×GC) may be needed.
- GC-MS compound identification is limited to thermally stable, low-molecular-weight compounds; polar, high-MW, or thermally labile analytes may not ionize or elute properly.

## Evidence

- [full_text] The CoreMS GC-MS processing pipeline successfully identify compounds from low-resolution mass spectrometry data using spectral library matching: "The CoreMS pipeline executes compound identification through sequential steps: data loading via ReadAndiNetCDF, retention index calibration using get_rt_ri_pairs, and spectral matching via"
- [full_text] Spectral matching and scoring methodology: "Extract low-resolution mass spectra from each peak and perform LowResMassSpectralMatch against the PNNLMetV20191015.MSL spectral library, scoring matches by cosine similarity and retention-index"
- [readme] Input data format for GC-MS: "ANDI NetCDF for GC-MS (.cdf)"
- [readme] Output data format and structure: "Self-containing Hierarchical Data Format (.hdf5) including raw data and time-series data-point for processed data-sets with all associated metadata stored as json attributes"
- [readme] GC-MS workflow feature set: "Baseline detection, subtraction, smoothing; m/z based Chromatogram Peak Deconvolution; Manual and automatic noise threshold calculation; First and second derivatives peak picking methods; Peak Area"
