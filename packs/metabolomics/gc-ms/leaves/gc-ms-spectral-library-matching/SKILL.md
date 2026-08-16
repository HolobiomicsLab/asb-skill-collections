---
name: gc-ms-spectral-library-matching
description: Use when when you have GC-MS data with detected peaks that require structural annotation, retention index calibration has been applied (typically using FAMES standards), and you need to assign compound identities with confidence scores.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0599
  - http://edamontology.org/topic_3172
  tools:
  - CoreMS
  - LowResMassSpectralMatch
  - GC_RI_Calibration
  - MetaMS
  techniques:
  - GC-MS
derived_from:
- doi: 10.5281/zenodo.14009575
  title: corems
evidence_spans:
- from corems.transient.input.brukerSolarix import ReadBrukerSolarix
- '**CoreMS** is a comprehensive mass spectrometry framework for software development and data analysis of small molecules analysis.'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_corems_cq
    doi: 10.5281/zenodo.14009575
    title: corems
  dedup_kept_from: coll_corems_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.5281/zenodo.14009575
  all_source_dois:
  - 10.5281/zenodo.14009575
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# GC-MS Spectral Library Matching

## Summary

Automated compound identification in low-resolution GC-MS data by matching retention-index-calibrated mass spectra against a reference spectral library. This skill enables high-confidence structural assignment of detected peaks using retention index filtering and spectral similarity scoring.

## When to use

When you have GC-MS data with detected peaks that require structural annotation, retention index calibration has been applied (typically using FAMES standards), and you need to assign compound identities with confidence scores. Apply this skill after baseline correction, deconvolution, and RI calibration are complete but before final reporting of results.

## When NOT to use

- Input peaks have not been retention-index calibrated; apply GC_RI_Calibration first.
- Data is high-resolution GC-MS; use dedicated high-resolution spectral matching algorithms instead.
- Reference library is not suitable for your sample type (e.g., specialized metabolites not in general GCMS databases).

## Inputs

- GC-MS raw data (NetCDF ANDI format)
- Processed mass spectrum objects with peaks detected and baseline-corrected
- Retention index calibration parameters (FAMES standard mix)
- Reference spectral library (GCMS MSL database)

## Outputs

- Annotated peak table with compound identities
- Spectral match scores (cosine similarity or equivalent metric)
- Retention index values per peak
- Match confidence ratings and RI alignment scores

## How to apply

First, ensure your GC-MS dataset is loaded in NetCDF ANDI format via the CoreMS input module. Apply GC_RI_Calibration to compute retention indices for each detected peak using FAMES standards as internal reference. Initialize the LowResMassSpectralMatch algorithm with a reference spectral library (e.g., PNNLMetV20191015.MSL). Execute spectral matching by passing retention-index-calibrated peaks to the algorithm; it will filter and rank library candidates by spectral similarity and RI alignment confidence. Export results including compound identities, match scores, and RI alignment confidence metrics. Judge success by verifying that match scores are above consensus thresholds and that RI values fall within expected retention windows for identified compounds.

## Related tools

- **CoreMS** (Framework for GC-MS data import, peak processing, retention index calibration, and spectral matching algorithm execution) — https://github.com/EMSL-Computing/CoreMS
- **LowResMassSpectralMatch** (Spectral matching algorithm that ranks library candidates using RI-filtered mass spectral similarity) — https://github.com/EMSL-Computing/CoreMS
- **GC_RI_Calibration** (Retention index calibration routine using FAMES standards to normalize peak retention times) — https://github.com/EMSL-Computing/CoreMS
- **MetaMS** (Workflow repository providing GC/MS metabolomics pipelines that integrate spectral library matching) — https://github.com/EMSL-Computing/MetaMS

## Examples

```
from corems.gcms.input import andi_netcdf; from corems.gcms.calibration import gc_ri_calibration; from corems.gcms.matching import LowResMassSpectralMatch; ms_data = andi_netcdf.read('sample.cdf'); gc_ri_calibration.apply(ms_data, fames_range=(100, 700)); matcher = LowResMassSpectralMatch('PNNLMetV20191015.MSL'); results = matcher.match(ms_data.mass_spectra)
```

## Evaluation signals

- All detected peaks receive match scores; no unmatched peaks remain (or have documented reasons for non-matching).
- Match scores fall within expected confidence ranges (typically cosine similarity 0.7–1.0 for good matches).
- Retention index values for matched compounds align with literature RI ranges for the stationary phase and temperature program used.
- Exported result table contains non-null entries for compound name, match score, and RI alignment confidence.
- Visual comparison of experimental and library mass spectra shows fragment ion peaks aligned at expected m/z ratios.

## Limitations

- Performance is limited to compounds present in the reference spectral library; novel or rare compounds will not be identified.
- Low-resolution mass spectra may have overlapping peaks or insufficient fragment resolution to distinguish isomers.
- Retention index calibration accuracy depends on proper integration of FAMES standard peaks and correct temperature program metadata.
- Spectral match scores can be high for structurally similar compounds; RI filtering helps but may not fully resolve ambiguity.
- The method is designed for automated annotation and should be validated by secondary MS/MS or orthogonal methods for critical identifications.

## Evidence

- [other] LowResMassSpectralMatch performs spectral matching against a bundled GCMS spectral library after retention index calibration using FAMES standards, enabling automated compound identification in GC-MS data.: "LowResMassSpectralMatch performs spectral matching against a bundled GCMS spectral library after retention index calibration using FAMES standards"
- [other] Apply GC_RI_Calibration to compute retention indices for each detected peak. Initialize LowResMassSpectralMatch spectral matching algorithm with PNNLMetV20191015.MSL spectral library as reference database. Execute spectral matching using retention-index-calibrated peaks to filter and rank library candidates.: "Apply GC_RI_Calibration to compute retention indices for each detected peak. Initialize LowResMassSpectralMatch spectral matching algorithm with PNNLMetV20191015.MSL spectral library as reference"
- [readme] Retention Index Calibration and Automatic molecular match algorithm with all spectral similarity methods are available features.: "Retention Index Calibration, Automatic local (SQLite) or external (MongoDB or PostgreSQL) database check, generation, and search, Automatic molecular match algorithm with all spectral similarity"
- [readme] CoreMS supports direct access for almost all vendors' data formats, allowing for the centralization and automation of all data processing workflows from the raw signal to data annotation and curation.: "CoreMS supports direct access for almost all vendors' data formats, allowing for the centralization and automation of all data processing workflows from the raw signal to data annotation and curation."
- [readme] ANDI NetCDF for GC-MS (.cdf) is supported as a data input format.: "ANDI NetCDF for GC-MS (.cdf)"
