---
name: ms-data-preprocessing
description: Use when you have received raw CE-MS or LC-MS output files in vendor-specific formats from a mass spectrometry instrument and need to process them through an untargeted metabolomics workflow (e.g., AriumMS) that requires standardized, interoperable file formats.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3650
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - msconvert
  - ProteoWizard
  - AriumMS
  techniques:
  - LC-MS
  - CE-MS
derived_from:
- doi: 10.1007/s00216-023-04715-6
  title: AriumMS
evidence_spans:
- For MS Data conversion to .mzXML or .mzML file format use msconvert, distributed with the ProteoWizard Project
- msconvert, distributed with the ProteoWizard Project
- msconvert, distributed with the ProteoWizard Project http://proteowizard.sourceforge.net/download.html
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ariumms_cq
    doi: 10.1007/s00216-023-04715-6
    title: AriumMS
  dedup_kept_from: coll_ariumms_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s00216-023-04715-6
  all_source_dois:
  - 10.1007/s00216-023-04715-6
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ms-data-preprocessing

## Summary

Convert raw mass spectrometry data from vendor-native formats (.raw, .d, .ms) to standardized open formats (.mzXML or .mzML) using msconvert, enabling downstream processing by untargeted metabolomics pipelines such as AriumMS. This preprocessing step is mandatory before region-of-interest detection and data augmentation can proceed.

## When to use

You have received raw CE-MS or LC-MS output files in vendor-specific formats from a mass spectrometry instrument and need to process them through an untargeted metabolomics workflow (e.g., AriumMS) that requires standardized, interoperable file formats. This skill is the entry point whenever raw instrument data must be converted before ROI search, centroiding, or multi-dataset augmentation.

## When NOT to use

- Input data is already in .mzXML or .mzML format — skip directly to ROI detection or downstream analysis.
- Analysis requires vendor-specific metadata or proprietary peak picking that is lost in standard format conversion.
- Raw instrument output is unavailable and only processed vendor software output (e.g., .txt peak lists) is on hand — conversion will fail or produce incomplete metadata.

## Inputs

- Raw mass spectrometry data file in vendor-native format (.raw, .d, .ms, or equivalent CE-MS/LC-MS instrument output)

## Outputs

- Converted mass spectrometry data file in .mzXML format
- Converted mass spectrometry data file in .mzML format
- Metadata validation report (scan count, mass range, retention time range)

## How to apply

Obtain raw MS data files in vendor-native format (e.g., .raw, .d, .ms) from CE-MS or LC-MS instruments. Run msconvert (distributed with ProteoWizard) with output format set to .mzXML or .mzML, applying default centroiding and compression settings as appropriate for the data type and downstream analysis needs. After conversion, verify that the output files are valid .mzXML or .mzML by confirming metadata integrity: check that scan count, mass range, and retention time range match expectations from the instrument log or raw file inspection. This validation ensures the converted data is suitable for ROI detection and augmentation workflows.

## Related tools

- **msconvert** (Executes the vendor format → .mzXML/.mzML conversion with centroiding and compression options.) — http://proteowizard.sourceforge.net/download.html
- **ProteoWizard** (Project and suite that distributes msconvert and related MS data manipulation tools.) — http://proteowizard.sourceforge.net/download.html
- **AriumMS** (Downstream untargeted metabolomics pipeline that accepts .mzXML/.mzML as input for ROI detection and data augmentation.) — https://github.com/AdrianHaun/AriumMS

## Examples

```
msconvert input_raw_file.raw --mzXML --zlib --filter "peakPicking cwt snr=1.0 prefilterLength=15 prefilterSmoothingType=gaussian prefilterSmoothingWindow=4.32"
```

## Evaluation signals

- Output files have the correct .mzXML or .mzML file extension and are readable by XML/mzML parsers.
- Metadata header contains expected scan count, mass range (m/z min–max), and retention time (RT) range consistent with instrument configuration and sample run duration.
- Centroided peaks (or profile data, as specified) are present and peak intensities are non-negative and within expected dynamic range for the instrument.
- Downstream AriumMS ROI detection and augmentation steps execute without format errors and produce expected region-of-interest features.

## Limitations

- Conversion fidelity depends on ProteoWizard support for the specific vendor instrument and raw file format; unsupported formats will fail or produce incomplete output.
- Centroiding and compression settings during conversion are applied uniformly; instrument-specific optimization (e.g., signal-to-noise thresholds, deisotoping) may require custom parameters not exposed in default msconvert.
- Metadata from vendor software (e.g., instrument serial number, calibration details, sample comments) may be omitted or stripped during conversion to the standardized format.
- Large raw files can require significant disk space during conversion; temporary workspace and output directory sizing must accommodate 2–3× the raw file size.

## Evidence

- [other] Raw MS data must be converted to .mzXML or .mzML file format using msconvert: "Raw MS data must be converted to .mzXML or .mzML file format using msconvert, a tool distributed with the ProteoWizard Project, as a prerequisite for AriumMS processing."
- [other] Workflow steps for conversion and validation: "1. Obtain raw MS data files in vendor-native format (e.g., .raw, .d, .ms) from CE-MS or LC-MS instruments. 2. Run msconvert (ProteoWizard) with output format set to .mzXML or .mzML, applying default"
- [readme] ProteoWizard distribution and tool location: "For MS Data conversion to .mzXML or .mzML file format use msconvert, distributed with the ProteoWizard Project http://proteowizard.sourceforge.net/download.html"
- [readme] AriumMS application context and requirements: "All in one tool for untargeted Metabolomics by ROI and augmentation of multiple Data sets."
