---
name: feature-detection-in-chromatographic-ms-data
description: Use when you have vendor-independent centroided DDA mzML files from LC- or GC-HRMS and need to delineate chromatographic peaks across the mass-to-charge and retention-time dimensions before applying mass defect analysis, diagnostic fragment matching, or other prioritization rules.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - pyOpenMS
  - OpenMS
  - Python
  - MSConvert
  - PFΔScreen
derived_from:
- doi: 10.1007/s00216-023-05070-2
  title: pfdeltascreen
evidence_spans:
- pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection in MS raw data
- pyOpenMS (Python interface to the C++ OpenMS library)
- pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection in MS raw data.
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
---

# feature-detection-in-chromatographic-ms-data

## Summary

Automated extraction of chromatographic features (m/z, retention time, intensity, charge state, isotope pattern) from centroided data-dependent acquisition mzML files using pyOpenMS, forming the input foundation for downstream PFAS prioritization and non-target screening workflows.

## When to use

You have vendor-independent centroided DDA mzML files from LC- or GC-HRMS and need to delineate chromatographic peaks across the mass-to-charge and retention-time dimensions before applying mass defect analysis, diagnostic fragment matching, or other prioritization rules. Apply this skill when raw spectra have not yet been converted into a structured feature table.

## When NOT to use

- Input is already a curated feature table (e.g., from vendor software or external tool); use external feature list pathway instead via 'Browse SampleFeatures.xlsx'
- Raw mzML data contain profile (non-centroided) spectra; centroiding must precede this skill
- MS data were acquired in data-independent (DIA/SWATH) or MS1-only mode without ddMS2; feature detection requires DDA scans for downstream MS2 analysis

## Inputs

- centroided data-dependent acquisition (DDA) mzML file from LC- or GC-HRMS
- optional: blank control mzML file (same format and acquisition mode)

## Outputs

- structured feature table (CSV or featureXML format) with columns: m/z, retention time, intensity, charge state, isotope pattern
- extracted features suitable for MS2 alignment and prioritization

## How to apply

Load the centroided DDA mzML file using pyOpenMS MSExperiment reader, then initialize the FeatureFinder algorithm with peak-picking parameters appropriate for high-resolution MS1 data (e.g., signal-to-noise thresholds, isotope pattern detection). Execute feature detection to identify and delineate peaks across both m/z and retention-time dimensions. Extract feature attributes (m/z, retention time, intensity, charge state, isotope pattern) and construct a feature table. Export the table to tabular format (CSV or featureXML) for downstream prioritization workflow. The overall runtime is typically short (e.g., <1 minute for 4000 spectra per sample), allowing convenient parameter adjustment.

## Related tools

- **pyOpenMS** (Python interface to OpenMS C++ library; performs centroided peak detection and feature delineation in m/z–RT space) — https://github.com/OpenMS/OpenMS
- **OpenMS** (Underlying C++ library providing FeatureFinder algorithm and MSExperiment I/O backend for mzML parsing) — https://github.com/OpenMS/OpenMS
- **MSConvert** (Upstream tool to convert vendor-proprietary raw mass spectrometry formats to vendor-independent mzML with centroiding) — https://proteowizard.sourceforge.io/
- **PFΔScreen** (Application wrapping pyOpenMS feature detection within a GUI, includes optional blank correction and MS2 alignment post-processing) — https://github.com/JonZwe/PFAScreen

## Evaluation signals

- Feature table contains expected columns (m/z, retention time, intensity, charge state) with no null values for core attributes; row count is reasonable (10s to 1000s of features, not 0 or >1M)
- m/z values fall within instrument range (typically 50–2000 m/z); retention times are monotonically increasing or show realistic chromatographic profile
- Intensity values are positive and show expected distribution (orders of magnitude variation across features, not all identical or all zero)
- Charge state assignments are consistent with isotope patterns (e.g., singly-charged features show ~1.0 m/z spacing between isotopologues; doubly-charged show ~0.5)
- Feature count in sample is significantly higher than in blank control (if blank provided), confirming ability to distinguish signal from noise

## Limitations

- Feature detection assumes centroided spectra; profile mode data will yield spurious or missed peaks and require external centroiding step (e.g. via MSConvert)
- FeatureFinder performance depends on appropriate selection of peak-picking parameters (signal-to-noise threshold, isotope pattern model); incorrect settings can cause mass bias or false positives
- Data-dependent acquisition mode is required; data-independent or targeted MS modes are not supported and will produce incomplete or invalid feature lists
- Complex chromatographic coelution or highly overlapped peaks may be incorrectly split into or merged as single features, particularly in high-complexity non-target screening samples
- No explicit changelog or version history provided; parameter defaults and algorithm behavior may vary between pyOpenMS releases without documentation

## Evidence

- [intro] pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection in MS raw data: "pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection in MS raw data"
- [intro] Raw data format and acquisition mode specification: "Raw mass spectrometric data can be included vendor-independently in the mzML format (data-dependent acquisition with centroided spectra"
- [other] Feature extraction workflow steps: "Load centroided DDA mzML file using pyOpenMS MSExperiment reader. 2. Initialize FeatureFinder algorithm in pyOpenMS with appropriate peak-picking parameters for high-resolution MS1 data. 3. Execute"
- [readme] Runtime performance characteristic: "The overall rather short runtime (e.g., less than one minute in case of 4000 spectra per sample for the whole workflow), allows a convenient adjustment of input parameters."
- [readme] Input specification and optional alternatives: "In case another feature finding procedure (e.g., from vendor software) is desired, custom feature lists (see external_feature_list.xlsx) together with the respective mzML files can instead be"
- [readme] Centroiding and DDA requirement: "Sample and blank for raw data input in PFΔScreen should have been measured under data-dependent acquisition (ddMS2) with centroided spectra, ideally with one collision energy per precursor."
