---
name: mzml-mzxml-file-format-processing
description: Use when your raw LC-MS data are in vendor-specific binary formats (e.g., .raw, .d, .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MetCohort
  - ProteoWizard
derived_from:
- doi: 10.1021/acs.analchem.4c04906
  title: MetCohort
evidence_spans:
- MetCohort is an untargeted liquid chromatography-mass spectrometry (LC-MS) data processing tool for large-scale metabolomics and exposomics
- MetCohort is an untargeted liquid chromatography-mass spectrometry (LC-MS) data processing tool
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metcohort_cq
    doi: 10.1021/acs.analchem.4c04906
    title: MetCohort
  dedup_kept_from: coll_metcohort_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c04906
  all_source_dois:
  - 10.1021/acs.analchem.4c04906
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mzml-mzxml-file-format-processing

## Summary

Process centroided LC-MS raw data in mzML or mzXML format as the required input for automated retention time correction and peak detection workflows in untargeted metabolomics. This skill ensures data are in the correct open, vendor-neutral format and meet centroiding and organizational prerequisites before alignment and feature detection.

## When to use

Your raw LC-MS data are in vendor-specific binary formats (e.g., .raw, .d, .ms) or uncentroided mzML/mzXML files, and you need to process them through MetCohort or similar tools that require centroided mzML or mzXML input for retention time correction and feature detection in large-scale metabolomics studies.

## When NOT to use

- Input data are already processed into a feature table or intensity matrix—file format processing is only the first step before alignment.
- Data are in untargeted but already-aligned formats (e.g., NetCDF from other pipelines) that do not require re-conversion.
- Profile-mode (non-centroided) mzML/mzXML are acceptable for your downstream tool—MetCohort specifically requires centroided data.

## Inputs

- Vendor-specific LC-MS raw data files (.raw, .d, .ms, or other proprietary formats)
- Uncentroided mzML or mzXML files
- Centroided mzML or mzXML files (if already converted and requiring batch organization)

## Outputs

- Centroided mzML or mzXML files, organized in a single folder
- Metadata indicating which file(s) are designated as QC reference(s)
- Optional: retention time crop parameters (start and end times in seconds)

## How to apply

Convert vendor-specific LC-MS raw data to centroided mzML or mzXML format using ProteoWizard or equivalent conversion tools. Ensure all files are centroided (not profile mode), as this is a prerequisite for ROA (Region of Alignment) detection and accurate peak detection. Place all converted files in a single folder. Before processing, designate at least one file as a quality control (QC) reference file—this file will be used to extract the alignment template (TIC or BPC) and determine ROI ranges for the entire batch. Optionally, crop the retention time range to remove blank or undesired signal at the beginning or end of the chromatographic gradient by setting explicit retention time bounds in seconds rather than using auto-detection.

## Related tools

- **MetCohort** (LC-MS data processing pipeline that accepts processed mzML/mzXML files for retention time correction and peak detection) — https://github.com/JunYang2021/MetCohort
- **ProteoWizard** (Vendor-neutral LC-MS data conversion and centroiding tool to produce mzML or mzXML from proprietary formats)

## Evaluation signals

- All input files are in mzML or mzXML format (verify via file extension and XML declaration in header).
- All files are centroided, not profile mode (inspect mzML/mzXML headers for <cvParam> tags referencing 'centroided spectrum' or absence of 'profile spectrum').
- All files reside in a single folder with no subdirectories.
- At least one file is explicitly labeled as QC reference before processing begins.
- Optional retention time crop bounds, if applied, are numeric values in seconds and exclude only dead time or artifact regions at the gradient edges.

## Limitations

- Conversion from vendor formats requires external tools (e.g., ProteoWizard) and may introduce minor precision loss depending on converter fidelity.
- Profile-mode (non-centroided) data cannot be used; centroiding is mandatory and must be performed during conversion or as a preprocessing step.
- All files in the batch must be in the same format (mzML or mzXML); mixed formats are not supported.
- QC file selection is user-driven; choosing an unrepresentative or poor-quality QC file will compromise downstream alignment and feature detection.
- Retention time crop parameters are static; they apply uniformly to all files in the batch and may remove legitimate early or late-eluting features if set incorrectly.

## Evidence

- [readme] MetCohort now supports mzML or mzXML file format of LC-MS raw data.: "MetCohort now supports mzML or mzXML file format of LC-MS raw data."
- [readme] At least one file need to be specified as quality control (QC) file.: "At least one file need to be specified as quality control (QC) file."
- [readme] The files need to be centroided and in the same folder.: "The files need to be centroided and in the same folder."
- [readme] For some experiments having blank or undesired signal at the beginning or ending of chromatographic gradient, users can uncheck the box of Auto range and set the real retention time in Crop retention time in seconds.: "For some experiments having blank or undesired signal at the beginning or ending of chromatographic gradient, users can uncheck the box of Auto range and set the real retention time in Crop retention"
- [intro] Load the QC reference file (mzML or mzXML format) and extract its total ion chromatogram (TIC) or base peak chromatogram (BPC) as the alignment template.: "Load the QC reference file (mzML or mzXML format) and extract its total ion chromatogram (TIC) or base peak chromatogram (BPC) as the alignment template."
