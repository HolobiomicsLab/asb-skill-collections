---
name: centroided-peak-extraction-from-hrms
description: Use when you have centroided data-dependent acquisition (DDA/ddMS2) mzML
  files from LC- or GC-HRMS measurements and need to systematically detect and characterize
  MS1 features across the mass-to-charge and retention-time dimensions prior to compound
  prioritization or suspect screening.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3634
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - pyOpenMS
  - OpenMS
  - Python
  - MSConvert
  - PFΔScreen
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1007/s00216-023-05070-2
  title: pfdeltascreen
evidence_spans:
- pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection
  in MS raw data
- pyOpenMS (Python interface to the C++ OpenMS library)
- pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection
  in MS raw data.
- PFΔScreen is an open-source Python based non-target screening software tool
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pfdeltascreen_cq
    doi: 10.1007/s00216-023-05070-2
    title: pfdeltascreen
  dedup_kept_from: coll_pfdeltascreen_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s00216-023-05070-2
  all_source_dois:
  - 10.1007/s00216-023-05070-2
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Centroided Peak Extraction from HRMS

## Summary

Automated detection and delineation of chromatographic peaks from vendor-independent mzML files containing centroided high-resolution mass spectrometry data using pyOpenMS. This skill extracts feature attributes (m/z, retention time, intensity, charge state, isotope pattern) and constructs tabular feature tables for downstream prioritization workflows.

## When to use

You have centroided data-dependent acquisition (DDA/ddMS2) mzML files from LC- or GC-HRMS measurements and need to systematically detect and characterize MS1 features across the mass-to-charge and retention-time dimensions prior to compound prioritization or suspect screening. This is the appropriate entry point when raw vendor data has been converted to vendor-independent mzML format but feature detection has not yet been performed.

## When NOT to use

- Input is profile (non-centroided) mzML data; profile spectra require distinct peak-picking steps prior to feature detection and may benefit from different FeatureFinder configurations.
- Input is already a pre-computed feature table or external feature list; use the external feature table import pathway instead.
- Input is not mzML format or lacks data-dependent acquisition metadata; the workflow assumes vendor-converted, DDA-structured data.

## Inputs

- centroided mzML file with data-dependent acquisition (DDA/ddMS2)
- FeatureFinder algorithm parameters (peak-picking settings for high-resolution MS1)
- optional: blank/control mzML file for comparison

## Outputs

- feature table (CSV or featureXML format)
- feature attributes table (m/z, retention time, intensity, charge state, isotope pattern per feature)
- MS1 feature boundaries and delineations

## How to apply

Load the centroided DDA mzML file using pyOpenMS MSExperiment reader. Initialize the FeatureFinder algorithm with parameters appropriate for high-resolution MS1 data (e.g., peak-picking settings tuned to the mass accuracy and chromatographic resolution of your instrument). Execute feature detection to identify and delineate peaks across both m/z and retention-time dimensions. Extract feature attributes including m/z, retention time, intensity, charge state, and isotope pattern from detected features. Construct a feature table and export to tabular format (CSV or featureXML) for downstream analysis. The rationale is that centroided spectra provide well-defined peak boundaries, enabling reliable feature boundary detection; the workflow preserves full MS1 information while reducing data volume.

## Related tools

- **pyOpenMS** (Python interface to OpenMS C++ library; executes FeatureFinder algorithm for peak detection and feature delineation on centroided MS1 data) — https://github.com/OpenMS/OpenMS
- **OpenMS** (C++ library providing the FeatureFinder algorithm and MSExperiment reader for mzML file I/O) — https://github.com/OpenMS/OpenMS
- **MSConvert** (Converts vendor mass spectrometry raw data formats to vendor-independent mzML format with centroiding and DDA preservation)
- **PFΔScreen** (Reference implementation wrapping pyOpenMS feature detection with GUI for automated PFAS feature prioritization workflow) — https://github.com/JonZwe/PFAScreen

## Evaluation signals

- Feature table contains expected number of rows (features detected) with no missing or null values in required columns (m/z, retention time, intensity, charge state).
- m/z values fall within expected instrument mass range and maintain instrument mass accuracy (e.g., < 5 ppm for typical HRMS); retention time values are monotonically increasing and within chromatographic run duration.
- Isotope pattern attributes are populated for multiply-charged or high-abundance features; charge state assignments are consistent with observed isotope spacing (Δm/z ≈ 1/z).
- Feature boundaries (start/end retention time, m/z min/max) do not overlap inappropriately; features are distinct across both m/z and retention-time dimensions.
- Output file format (CSV or featureXML) is valid and parseable by downstream prioritization software (e.g., PFΔScreen); schema matches expected column structure.

## Limitations

- Feature detection performance depends on appropriate FeatureFinder parameter tuning for the specific MS instrument and chromatographic method; incorrect parameters may miss weak features or over-call noise.
- Workflow requires centroided spectra; profile data will not yield reliable feature detection and must be pre-processed or converted.
- Data-dependent acquisition (DDA) structure is assumed; data-independent acquisition (DIA) or other acquisition modes may not produce expected feature tables.
- Custom feature lists can be provided as an alternative to automated detection, but this skill covers only automated pyOpenMS-based extraction.
- Blank/control correction is optional and must be explicitly applied; the skill itself produces features from the sample mzML without inherent blank subtraction.

## Evidence

- [other] Load centroided DDA mzML file using pyOpenMS MSExperiment reader. 2. Initialize FeatureFinder algorithm in pyOpenMS with appropriate peak-picking parameters for high-resolution MS1 data. 3. Execute feature detection to identify and delineate chromatographic peaks across the mass-to-charge and retention-time dimensions.: "Load centroided DDA mzML file using pyOpenMS MSExperiment reader. 2. Initialize FeatureFinder algorithm in pyOpenMS with appropriate peak-picking parameters for high-resolution MS1 data. 3. Execute"
- [other] Extract feature attributes (m/z, retention time, intensity, charge state, isotope pattern) and construct feature table. 5. Export feature table to tabular format (CSV or featureXML) for downstream prioritization workflow.: "Extract feature attributes (m/z, retention time, intensity, charge state, isotope pattern) and construct feature table. 5. Export feature table to tabular format (CSV or featureXML)"
- [readme] pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection in MS raw data from LC- or GC-HRMS measurements. The software accepts vendor-independent raw mass spectrometric data in mzML format containing data-dependent acquisition with centroided spectra: "pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection in MS raw data from LC- or GC-HRMS measurements. The software accepts vendor-independent raw mass spectrometric"
- [readme] Sample and blank for raw data input in PFΔScreen should have been measured under data-dependent acquisition (ddMS2) with centroided spectra, ideally with one collision energy per precursor.: "Sample and blank for raw data input should have been measured under data-dependent acquisition (ddMS2) with centroided spectra, ideally with one collision energy per precursor"
- [readme] The parameters for feature finding, MS2 alignment and blank correction can be specified and executed by pressing the 'Run FeatureFinding' button.: "The parameters for feature finding can be specified and executed by pressing the 'Run FeatureFinding' button"
