---
name: isotope-pattern-annotation-in-feature-detection
description: Use when when performing feature detection on centroided DDA mzML files from LC- or GC-HRMS and you need to confirm the elemental composition or differentiate between candidate features—particularly for PFAS screening where isotopic signatures (chlorine, bromine, fluorine) are diagnostic.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - pyOpenMS
  - OpenMS
  - Python
  - PFΔScreen RawDataVisualization tool
  - MSConvert
  techniques:
  - LC-MS
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

# Isotope-Pattern Annotation in Feature Detection

## Summary

Extraction and validation of isotope pattern information (m/z, intensity, charge state) from high-resolution MS1 features during pyOpenMS-based feature detection in centroided DDA mzML data. This enriches feature tables with isotopic signatures necessary for elemental composition inference and PFAS suspect confirmation.

## When to use

When performing feature detection on centroided DDA mzML files from LC- or GC-HRMS and you need to confirm the elemental composition or differentiate between candidate features—particularly for PFAS screening where isotopic signatures (chlorine, bromine, fluorine) are diagnostic. Apply this skill when feature detection has been executed and you are constructing the feature table prior to prioritization workflows.

## When NOT to use

- Input is already a manually curated or vendor-supplied feature list without raw mzML data—isotope annotation requires access to raw MS1 spectra.
- Low-resolution or profile-mode (non-centroided) MS1 data where isotope peaks cannot be reliably resolved or delineated.
- mzML files from data-independent acquisition (DIA) or untargeted MS1-only acquisition where MS2 fragment data is unavailable for later diagnostic confirmation.

## Inputs

- Centroided DDA mzML file (LC- or GC-HRMS, ESI or APCI ionization)
- pyOpenMS FeatureFinder algorithm output (feature objects with isotope cluster information)
- High-resolution MS1 spectra (typically <5 ppm mass accuracy)

## Outputs

- Feature table (CSV or featureXML format) with isotope pattern attributes per feature
- Isotope cluster m/z, intensity, and charge state annotations
- Validated feature list ready for downstream PFAS prioritization

## How to apply

During pyOpenMS feature detection on high-resolution MS1 data, the FeatureFinder algorithm automatically identifies and delineates chromatographic peaks across mass-to-charge and retention-time dimensions. As part of this process, extract the isotope pattern attributes—including individual isotopologue m/z values, relative intensities, and charge state—from each detected feature. These attributes are stored in the feature object and must be transferred into the tabular feature table (CSV or featureXML format) during export. The isotope patterns can then be compared against theoretical isotope distributions (e.g., via the RawDataVisualization tool in PFΔScreen) to validate feature identity and support fragment mass difference analysis in MS2 data. Rationale: isotope patterns are mass-spectrometry-intrinsic signatures that reduce false positives by confirming that detected peaks are chemically coherent and not noise or contaminants.

## Related tools

- **pyOpenMS** (Python interface to OpenMS C++ library used to execute FeatureFinder algorithm and extract feature and isotope pattern attributes from MS1 data) — https://github.com/OpenMS/OpenMS
- **OpenMS** (Underlying C++ library providing FeatureFinder algorithm and feature detection/isotope clustering implementation) — https://github.com/OpenMS/OpenMS
- **PFΔScreen RawDataVisualization tool** (Post-detection visualization and validation of theoretical isotope patterns against experimental MS1 isotope clusters) — https://github.com/JonZwe/PFAScreen
- **MSConvert** (Vendor-neutral conversion tool to generate centroided mzML input files from vendor raw formats)

## Evaluation signals

- Feature table contains isotope pattern columns (m/z, relative intensity, charge state) for each feature with no missing values for features with signal intensity above the instrument baseline.
- Exported isotope m/z values match the expected mass difference for common isotopes (e.g., Δm/z ≈ 1.003 for 13C, ≈ 0.998 for 37Cl) within instrument mass accuracy tolerance (<5 ppm for HRMS).
- Isotope relative intensity ratios align with theoretical distributions (e.g., 13C/12C ≈ 1.1% per carbon; 37Cl/35Cl ≈ 32% for chlorine) within ±20% measurement uncertainty.
- Feature table can be successfully loaded into PFΔScreen or equivalent downstream tool without schema errors or missing isotope attribute warnings.
- Theoretical isotope patterns displayed in RawDataVisualization overlay closely with experimental MS1 traces, confirming that detected isotope clusters are genuine and not deconvolution artifacts.

## Limitations

- Isotope annotation accuracy depends on MS resolution and mass accuracy; low-resolution MS1 spectra (<50,000 FWHM) may fail to separate adjacent isotopologues, leading to loss or conflation of isotope cluster information.
- Features with very low signal intensity or high background noise may yield unreliable isotope intensity ratios that do not match theoretical expectations.
- FeatureFinder algorithm parameters (peak-picking thresholds, charge state range, isotope cluster tolerance) must be pre-tuned for the specific instrument and compound class; suboptimal settings can cause isotope peaks to be missed or incorrectly clustered.
- Centroided (not profile-mode) mzML data is required; if input is profile-mode, centroiding must be performed first (e.g., via MSConvert), which may introduce bias or artifacts in isotope intensity ratios.
- PFΔScreen documentation does not explicitly specify the mass tolerance or intensity threshold used by pyOpenMS FeatureFinder for isotope cluster assignment, making reproducibility across different instrument vendors challenging.

## Evidence

- [other] Extract feature attributes (m/z, retention time, intensity, charge state, isotope pattern) and construct feature table.: "Extract feature attributes (m/z, retention time, intensity, charge state, isotope pattern) and construct feature table."
- [readme] pyOpenMS is used for feature detection in MS raw data from LC- or GC-HRMS measurements on centroided DDA mzML files.: "pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection in MS raw data... Raw mass spectrometric data can be included vendor-independently in the mzML format"
- [other] Feature detection identifies and delineates chromatographic peaks across mass-to-charge and retention-time dimensions.: "Execute feature detection to identify and delineate chromatographic peaks across the mass-to-charge and retention-time dimensions."
- [readme] Theoretical isotope patterns can be displayed over experimental isotope patterns in MS1 data for validation.: "the theoretical isotope patterns of suspect hits can be displayed over the experimental isotope patterns (MS1)"
- [other] Initialize FeatureFinder algorithm in pyOpenMS with appropriate peak-picking parameters for high-resolution MS1 data.: "Initialize FeatureFinder algorithm in pyOpenMS with appropriate peak-picking parameters for high-resolution MS1 data."
