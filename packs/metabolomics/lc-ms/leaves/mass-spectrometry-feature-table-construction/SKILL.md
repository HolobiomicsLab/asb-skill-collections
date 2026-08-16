---
name: mass-spectrometry-feature-table-construction
description: Use when you have vendor-independent centroided mzML files from LC- or GC-HRMS data acquired in data-dependent acquisition (ddMS2) mode and need to extract detected features with m/z, retention time, and intensity attributes as input for non-target screening or PFAS prioritization workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - Python
  - pyOpenMS
  - OpenMS
  - MSConvert
  - PFΔScreen
  techniques:
  - LC-MS
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
  - build: coll_ncgtw_cq
    doi: 10.1093/bioinformatics/btaa037
    title: ncGTW
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

# mass-spectrometry-feature-table-construction

## Summary

Automated extraction of MS features (m/z, retention time, intensity) from centroided mzML files using pyOpenMS FeatureFinderCentroided, producing a structured feature table in mzTab or CSV format for downstream PFAS prioritization or metabolite screening.

## When to use

You have vendor-independent centroided mzML files from LC- or GC-HRMS data acquired in data-dependent acquisition (ddMS2) mode and need to extract detected features with m/z, retention time, and intensity attributes as input for non-target screening or PFAS prioritization workflows.

## When NOT to use

- Input is already a feature table (feature finding is redundant).
- Raw data is in profile mode (not centroided) — FeatureFinderCentroided requires centroided spectra; use profile-mode algorithms or convert first.
- mzML file lacks MS2 data and downstream analysis requires MS2 fragment information (custom feature lists without corresponding mzML will not provide MS2 spectra for MS/MS-based filtering).

## Inputs

- centroided mzML file (from data-dependent acquisition with MS2)
- optional: blank control mzML file
- optional: custom feature list (Excel format) with m/z, retention time, intensity columns

## Outputs

- feature table (mzTab or CSV format) with columns: m/z, retention time, intensity
- linked MS2 spectra metadata (when using native feature detection)

## How to apply

Load a centroided mzML file into pyOpenMS MSExperiment reader. Apply the FeatureFinderCentroided algorithm to identify MS features across the mass and retention-time dimensions; this algorithm is designed to handle centroided spectra and will extract m/z, retention time, and intensity for each detected feature. Extract detected features with their m/z, retention time, and intensity attributes. Write the feature list to a structured tabular output file (mzTab or CSV format). If custom feature lists from vendor software are preferred instead, load them alongside the corresponding mzML files to preserve MS2 data linkage for downstream analysis.

## Related tools

- **pyOpenMS** (Python interface to OpenMS C++ library; implements MSExperiment reader and FeatureFinderCentroided algorithm for centroided feature extraction) — https://pypi.org/project/pyopenms/
- **OpenMS** (C++ library underlying pyOpenMS; provides core feature detection and mass spectrometry data handling) — https://www.openms.de/
- **MSConvert** (converts vendor raw formats to vendor-independent mzML centroided format, prerequisite for pyOpenMS feature detection)
- **PFΔScreen** (end-to-end non-target screening tool that wraps pyOpenMS feature detection and provides GUI-driven feature extraction and PFAS prioritization) — https://github.com/JonZwe/PFAScreen

## Evaluation signals

- Output feature table contains at least m/z, retention time, and intensity columns with non-null values for all detected features.
- Number of detected features is reasonable relative to the mzML complexity (typically hundreds to thousands for real samples; zero features may indicate misconfiguration or very weak data).
- m/z values fall within expected instrument range (e.g., 50–1000 m/z for typical HRMS) and retain instrument mass accuracy (sub-ppm for Orbitrap/TOF).
- Retention time values are monotonically increasing or show expected chromatographic pattern (no negative or out-of-bounds values).
- When MS2 data is present, feature intensity correlates with MS2 precursor intensity; MS2 spectra are linked to detected features in downstream visualization tools.

## Limitations

- FeatureFinderCentroided is optimized for centroided spectra only; profile-mode data must be centroided before input (e.g., via MSConvert).
- Feature detection parameters (e.g., signal-to-noise ratio, feature width in m/z and retention-time dimensions) may require empirical tuning for different LC/GC methods or MS instruments.
- Custom feature lists from vendor software bypass the MS2 alignment step; MS2 data retrieval then depends on external mzML files being provided and correctly linked.
- The algorithm is sensitive to blank-level noise; blank correction should be applied downstream if blank control mzML is included, but automated blank subtraction is a separate workflow step.

## Evidence

- [other] Load centroided mzML file using pyOpenMS MSExperiment reader. Apply feature detection algorithm via pyOpenMS FeatureFinderCentroided to identify MS features across the mass and time dimensions. Extract detected features with m/z, retention time, and intensity attributes.: "Load centroided mzML file using pyOpenMS MSExperiment reader. 2. Apply feature detection algorithm via pyOpenMS FeatureFinderCentroided to identify MS features across the mass and time dimensions. 3."
- [other] pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection in MS raw data, accepting vendor-independent centroided mzML format files as input for automated feature extraction.: "pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection in MS raw data, accepting vendor-independent centroided mzML format files as input for automated feature extraction."
- [readme] Sample and blank for raw data input in PFΔScreen should have been measured under data-dependent acquisition (ddMS2) with centroided spectra, ideally with one collision energy per precursor.: "Sample and blank for raw data input in PFΔScreen should have been measured under data-dependent acquisition (ddMS2) with centroided spectra, ideally with one collision energy per precursor."
- [readme] In case another feature finding procedure (e.g., from vendor software) is desired, custom feature lists (see external_feature_list.xlsx) together with the respective mzML files can instead be included in PFΔScreen. Note that data evaluation only works when the corresponding mzML files are also given; otherwise MS2 data would be missing.: "custom feature lists (see external_feature_list.xlsx) together with the respective mzML files can instead be included in PFΔScreen. Note that data evaluation only works when the corresponding mzML"
- [intro] mzML files can be generated via the MSConvert software tool and are required in vendor-independent centroided format.: "mzML files can be generated via the MSConvert software tool"
