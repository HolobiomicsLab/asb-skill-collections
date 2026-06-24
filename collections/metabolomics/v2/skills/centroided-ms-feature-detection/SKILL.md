---
name: centroided-ms-feature-detection
description: Use when you have vendor-independent centroided mzML files from data-dependent
  acquisition (ddMS2) HRMS experiments and need to extract a reproducible feature
  list with mass, chromatographic, and intensity dimensions as input to PFAS prioritization,
  suspect screening, or other MS-based analyses.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0637
  tools:
  - Python
  - pyOpenMS
  - OpenMS
  - MSConvert
  - PFΔScreen
  techniques:
  - LC-MS
  - GC-MS
  license_tier: restricted
derived_from:
- doi: 10.1007/s00216-023-05070-2
  title: pfdeltascreen
evidence_spans:
- PFΔScreen is an open-source Python based non-target screening software tool
- pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection
  in MS raw data
- pyOpenMS (Python interface to the C++ OpenMS library)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# centroided-ms-feature-detection

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Automated extraction of mass spectrometry features (m/z, retention time, intensity) from centroided mzML files using the pyOpenMS FeatureFinderCentroided algorithm. This skill converts raw LC- or GC-HRMS data into a structured feature list suitable for downstream prioritization and annotation workflows.

## When to use

You have vendor-independent centroided mzML files from data-dependent acquisition (ddMS2) HRMS experiments and need to extract a reproducible feature list with mass, chromatographic, and intensity dimensions as input to PFAS prioritization, suspect screening, or other MS-based analyses. Use this skill when feature detection via commercial vendor software is unavailable or when reproducibility and open-source tooling are required.

## When NOT to use

- Input is already a feature table from vendor software or external feature finder — use the optional 'custom feature list' import pathway instead.
- mzML files contain profile (non-centroided) spectra — centroided spectra are required; convert using MSConvert with centroiding enabled.
- Data were acquired in data-independent acquisition (DIA) or MS1-only mode — FeatureFinderCentroided is designed for ddMS2 centroided data.

## Inputs

- centroided mzML file from ddMS2 acquisition
- optional blank control mzML file (same instrument, same acquisition parameters)
- feature detection parameters (mass tolerance, intensity thresholds, peak width ranges)

## Outputs

- feature list table (CSV, mzTab, or Excel format) with columns: m/z, retention time, intensity, charge state
- optional: blank-corrected feature list
- diagnostic logs or console output with feature detection statistics

## How to apply

Load a centroided mzML file using the pyOpenMS MSExperiment reader, then apply the FeatureFinderCentroided algorithm to identify MS features across the mass-to-charge and retention time dimensions. Extract detected features with their m/z, retention time, and intensity attributes. Write the resulting feature list to a structured tabular format (mzTab, CSV, or Excel) with configurable parameters for the feature finder (e.g., mass tolerance, intensity thresholds). The overall runtime is short (e.g., <1 minute for 4000 spectra per sample), allowing convenient parameter adjustment. Optionally include a blank control mzML file for blank correction during feature detection.

## Related tools

- **pyOpenMS** (Python interface to OpenMS C++ library; provides MSExperiment reader and FeatureFinderCentroided algorithm for automated feature detection in centroided MS data) — https://github.com/OpenMS/OpenMS
- **OpenMS** (Core C++ mass spectrometry processing library underlying pyOpenMS; implements the centroided feature detection algorithms)
- **MSConvert** (Vendor-independent tool to convert proprietary MS raw formats to mzML and optionally apply centroiding)
- **PFΔScreen** (Complete non-target screening pipeline integrating centroided MS feature detection with PFAS prioritization, KMD analysis, and MS2 fragment matching) — https://github.com/JonZwe/PFAScreen

## Evaluation signals

- Feature list contains all expected columns (m/z, retention time, intensity, charge state) with no null or malformed entries.
- Detected m/z values fall within the instrument's valid mass range and match expected analyte masses (within configured mass tolerance); retention times are monotonically increasing or match expected chromatographic behavior.
- Number of detected features is reasonable for the sample complexity and matches manual inspection of extracted ion chromatograms (EICs) for known compounds.
- Blank-corrected features show reduced or eliminated intensity for features present in blank control; remaining features in blank are below a configured threshold or removed entirely.
- Feature intensities are consistent with MS1 peak areas and visual inspection of raw data; no spurious peaks from noise or baseline artifacts.

## Limitations

- Requires data from data-dependent acquisition (ddMS2) with centroided spectra; cannot process profile data without prior centroiding.
- Feature detection performance depends critically on tuning of mass tolerance, intensity thresholds, and peak width parameters; suboptimal parameters may miss low-intensity features or introduce false positives.
- Vendor-specific metadata (e.g., collision energy, isolation window, instrument configuration) may be lost or inconsistently encoded in mzML, potentially affecting downstream MS2 interpretation.
- The algorithm is optimized for liquid chromatography (LC) and gas chromatography (GC) coupled HRMS; may not perform well on other separation modalities.
- No changelog is available for the pyOpenMS version used; reproducibility across versions or installations may be affected without explicit version pinning.

## Evidence

- [intro] pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection in MS raw data: "pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection in MS raw data"
- [readme] centroided mzML files from data-dependent acquisition with centroided spectra are the input format: "Raw mass spectrometric data can be included vendor-independently in the mzML format (data-dependent acquisition with centroided spectra, mzML files can be generated via the MSConvert software tool)."
- [other] Feature detection algorithm extracts m/z, retention time, and intensity values: "Apply feature detection algorithm via pyOpenMS FeatureFinderCentroided to identify MS features across the mass and time dimensions. 3. Extract detected features with m/z, retention time, and"
- [readme] Overall runtime is short, allowing convenient parameter adjustment: "The overall rather short runtime (e.g., less than one minute in case of 4000 spectra per sample for the whole workflow), allows a convenient adjustment of input parameters."
- [readme] Blank control files can be optionally provided for blank correction: "To load a MS raw datafile, click the "Browse Sample.mzML" button and choose the mzML file of a sample and an optional mzML file of a blank control (Browse Blank.mzML)."
- [other] Output is structured tabular format (mzTab or CSV): "Write feature list to output file in structured tabular format (mzTab or CSV)."
