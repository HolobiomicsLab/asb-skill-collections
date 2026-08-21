---
name: mass-spectrum-extraction-and-formatting
description: Use when you have raw GC-MS data in netCDF or vendor-specific binary
  format and need to separate co-eluting compounds and extract clean mass spectra
  for each individual chemical component prior to molecular networking, spectral matching,
  or metabolite identification workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - MSHub
  techniques:
  - LC-MS
  - GC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41587-020-0700-3
  title: mshub
evidence_spans:
- MSHub auto-deconvolution
- Auto-deconvolution and molecular networking of gas chromatography–mass spectrometry
  data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mshub
    doi: 10.1038/s41587-020-0700-3
    title: mshub
  dedup_kept_from: coll_mshub
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41587-020-0700-3
  all_source_dois:
  - 10.1038/s41587-020-0700-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrum-extraction-and-formatting

## Summary

Convert raw gas chromatography–mass spectrometry (GC-MS) data into standardized, deconvolved mass spectra suitable for downstream molecular networking and spectral library matching. This skill resolves overlapping peaks in complex chromatographic mixtures and exports individual component spectra in machine-readable formats.

## When to use

You have raw GC-MS data in netCDF or vendor-specific binary format and need to separate co-eluting compounds and extract clean mass spectra for each individual chemical component prior to molecular networking, spectral matching, or metabolite identification workflows.

## When NOT to use

- Input data is already in processed feature-matrix or consensus spectrum format (e.g., aligned feature table or library MGF without raw MS traces).
- GC-MS chromatography shows no evidence of co-elution or peak overlap; direct spectral extraction without deconvolution is sufficient.
- Analysis goal is quantitative peak integration or area-under-curve measurement rather than qualitative component separation and spectral identification.

## Inputs

- Raw GC-MS data files in netCDF format
- Raw GC-MS data files in vendor-specific binary format

## Outputs

- Deconvolved mass spectra in MGF format
- Deconvolved mass spectra in mzML format

## How to apply

Load raw GC-MS files (netCDF or vendor format) into the MSHub auto-deconvolution module. The algorithm processes the raw data to resolve overlapping peaks by deconvolving the mass spectra of co-eluting components. After deconvolution, export the resulting spectra to a standardized output format (MGF or mzML) that preserves spectral metadata (retention time, precursor m/z, intensity arrays) and is compatible with downstream molecular networking tools like GNPS. Verify that each exported spectrum corresponds to a single chemical component by examining peak purity metrics and the absence of spectral artifacts.

## Related tools

- **MSHub** (Auto-deconvolution engine that resolves overlapping GC-MS peaks and extracts individual component spectra from raw data) — https://github.com/bittremieux/GNPS_GC

## Evaluation signals

- Output spectra are in valid MGF or mzML XML schema with required fields (retention time, m/z array, intensity array) populated.
- Each exported spectrum represents a single chemical component with no evidence of spectral contamination or double peaks.
- Deconvolved spectra can be successfully uploaded to and processed by GNPS molecular networking workflows without format or metadata errors.
- Peak intensity distributions in deconvolved spectra are consistent with expected mass fragmentation patterns (e.g., base peak and characteristic isotope ratios preserved).
- Spectral purity or quality score (if reported by MSHub) is above the background noise threshold and consistent across replicate analyses.

## Limitations

- Auto-deconvolution success depends on the degree of peak overlap and the signal-to-noise ratio in the raw data; highly complex or noisy chromatograms may yield incomplete separation.
- The method is optimized for GC-MS data; applicability to other chromatography–MS platforms (e.g., LC-MS) is not demonstrated in the source article.
- Retention time and mass accuracy of the input instrument affect the precision of component assignment; results are instrument-dependent.
- Export to MGF or mzML may lose some raw-file-specific metadata (e.g., vendor-proprietary collision energy ramps or calibration coefficients).

## Evidence

- [other] Load raw GC-MS files (netCDF or vendor format) from the companion repository or deposited dataset. Apply MSHub auto-deconvolution algorithm to resolve overlapping peaks and extract individual component spectra.: "Load raw GC-MS files (netCDF or vendor format) from the companion repository or deposited dataset. 2. Apply MSHub auto-deconvolution algorithm to resolve overlapping peaks and extract individual"
- [other] Export deconvolved spectra to a standardized output format (MGF or mzML) suitable for downstream molecular networking analysis.: "Export deconvolved spectra to a standardized output format (MGF or mzML) suitable for downstream molecular networking analysis."
- [intro] Auto-deconvolution and molecular networking methods for gas chromatography–mass spectrometry data analysis: "Development of auto-deconvolution and molecular networking methods for gas chromatography–mass spectrometry data analysis"
- [readme] This is a companion repository to the following manuscript: Aksenov, A.A., Laponogov, I., Zhang, Z. _et al_. Auto-deconvolution and molecular networking of gas chromatography–mass spectrometry data.: "This is a companion repository to the following manuscript: Aksenov, A.A., Laponogov, I., Zhang, Z. _et al_. Auto-deconvolution and molecular networking of gas chromatography–mass spectrometry data."
