---
name: chromatographic-feature-extraction
description: Use when you have centroided mzML files from LC- or GC-HRMS instruments (acquired in data-dependent mode with ddMS2) and need to systematically identify chromatographic peaks, measure their mass and retention time coordinates, and quantify their intensities before applying PFAS-specific.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3370
  tools:
  - Python
  - pyOpenMS
  - OpenMS
  - MSConvert
  - PFΔScreen
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1007/s00216-023-05070-2
  title: pfdeltascreen
evidence_spans:
- PFΔScreen is an open-source Python based non-target screening software tool
- pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection in MS raw data
- pyOpenMS (Python interface to the C++ OpenMS library)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_bioactivity_based_molecular_networking_cq
    doi: 10.1021/acs.jnatprod.7b00737
    title: Bioactivity-Based Molecular Networking
  - build: coll_pfdeltascreen
    doi: 10.1007/s00216-023-05070-2
    title: pfdeltascreen
  dedup_kept_from: coll_pfdeltascreen
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s00216-023-05070-2
  all_source_dois:
  - 10.1007/s00216-023-05070-2
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chromatographic-feature-extraction

## Summary

Automated detection and extraction of mass spectrometry features (m/z, retention time, intensity) from centroided mzML raw data using pyOpenMS FeatureFinderCentroided. This skill converts vendor-neutral LC/GC-HRMS instrument output into structured feature tables suitable for downstream prioritization and annotation workflows.

## When to use

You have centroided mzML files from LC- or GC-HRMS instruments (acquired in data-dependent mode with ddMS2) and need to systematically identify chromatographic peaks, measure their mass and retention time coordinates, and quantify their intensities before applying PFAS-specific prioritization or other compound screening logic.

## When NOT to use

- Input is already a validated feature table from vendor software — skip to PFAS prioritization
- Raw data is in profile (non-centroided) format — centroid first using MSConvert or equivalent
- Sample was acquired in MS1-only or full-scan mode without MS2 data — feature detection will run but downstream MS2-dependent filters cannot be applied

## Inputs

- centroided mzML file (data-dependent acquisition, ddMS2 mode)
- optional blank/control mzML file for background subtraction
- feature detection parameters (mass tolerance, RT window, intensity threshold)

## Outputs

- structured feature table (mzTab or CSV format)
- tabular data with columns: m/z, retention time, intensity, feature ID
- optional: MS2 spectral associations per feature

## How to apply

Load a centroided mzML file using the pyOpenMS MSExperiment reader, then apply the FeatureFinderCentroided algorithm with user-tunable parameters (e.g., mass tolerance in ppm, RT window width, intensity threshold) to identify peaks across the mass and time dimensions. The algorithm locates local maxima in the 2D mass-time space and extracts their m/z, retention time, and intensity attributes. Output the resulting feature list to tabular format (mzTab or CSV) with one row per detected feature. Validate success by inspecting feature count, m/z distribution (should span expected range for the analyte class), and intensity distribution (should show reasonable dynamic range without saturation artifacts).

## Related tools

- **pyOpenMS** (Python interface to OpenMS C++ library; executes FeatureFinderCentroided algorithm on centroided spectra to detect and extract chromatographic features) — https://pypi.org/project/pyopenms/
- **OpenMS** (Core C++ library providing the FeatureFinderCentroided algorithm and mzML I/O) — https://www.openms.de/
- **MSConvert** (Vendor data format conversion to mzML and centroiding of profile-mode spectra) — http://proteowizard.sourceforge.net/
- **PFΔScreen** (End-to-end application that wraps feature detection via pyOpenMS and follows with PFAS-specific prioritization) — https://github.com/JonZwe/PFAScreen

## Evaluation signals

- Feature table is non-empty and contains expected number of features (typically 100s–1000s for complex HRMS samples); absence may indicate wrong parameter settings or corrupted input
- m/z values span the expected analytical range without obvious clustering artifacts; histograms should show reasonable distribution across the measured mass window
- Retention time values are monotonically increasing and fall within the chromatographic gradient duration; gaps or duplicates suggest algorithmic failure
- Intensity values show log-normal distribution with no saturation (values capped at detector max); extreme outliers or flat distributions suggest detection threshold miscalibration
- Feature reproducibility: same sample measured twice produces feature lists with >80% m/z–RT overlap within instrument mass accuracy (typically <5 ppm) and retention time drift tolerance (typically <30 s)

## Limitations

- Algorithm assumes input is centroided; profile-mode data will not be processed correctly and must be converted first with MSConvert or equivalent
- Feature detection quality depends on tuning of mass tolerance (ppm), RT window width, and intensity threshold; no universal default parameters suit all analyte classes or instrument configurations
- Coeluting features with similar m/z are merged into a single peak; separation requires higher chromatographic resolution and cannot be recovered from mzML alone
- MS2 spectral association requires data-dependent acquisition; data-independent (DIA) or high-resolution accurate mass (HRAM) MS1-only modes provide no fragmentation data for downstream prioritization
- Runtime is fast (< 1 minute for ~4000 spectra per sample) but scales with file size; very large cohorts benefit from batch processing

## Evidence

- [intro] pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection in MS raw data: "pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection in MS raw data"
- [readme] Centroided mzML is the required input format; vendor independence is achieved via this interchange standard: "Raw mass spectrometric data can be included vendor-independently in the mzML format (data-dependent acquisition with centroided spectra, mzML files can be generated via the MSConvert software tool)"
- [other] FeatureFinderCentroided algorithm is applied after loading mzML to extract m/z, retention time, and intensity: "Apply feature detection algorithm via pyOpenMS FeatureFinderCentroided to identify MS features across the mass and time dimensions. 3. Extract detected features with m/z, retention time, and"
- [other] Output is a structured feature list in tabular format (mzTab or CSV): "Write feature list to output file in structured tabular format (mzTab or CSV)"
- [readme] Data must be acquired in data-dependent (ddMS2) mode with centroided spectra for full workflow support: "Sample and blank for raw data input in PFΔScreen should have been measured under data-dependent acquisition (ddMS2) with centroided spectra, ideally with one collision energy per precursor"
- [readme] Runtime is fast, allowing convenient parameter iteration: "The overall rather short runtime (e.g., less than one minute in case of 4000 spectra per sample for the whole workflow), allows a convenient adjustment of input parameters"
- [readme] Custom feature lists from other software can be included as an alternative to built-in detection: "In case another feature finding procedure (e.g., from vendor software) is desired, custom feature lists (see external_feature_list.xlsx) together with the respective mzML files can instead be"
