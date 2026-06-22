---
name: frame-metadata-extraction-and-export
description: Use when after completing multidimensional smoothing and saturation repair on Agilent MassHunter (.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - PNNL PreProcessor
  - Agilent MassHunter
  techniques:
  - ion-mobility-MS
derived_from:
- doi: 10.1021/jasms.4c00220
  title: PNNL PreProcessor
- doi: 10.1021/acs.jproteome.1c00425
  title: ''
evidence_spans:
- we have developed this user-friendly tool for Agilent MassHunter (.d) and UIMF mass spectrometry data files
- we have developed this user-friendly tool for Agilent MassHunter (.d) and UIMF mass spectrometry data files (MS-files) from drift tube (DT) and structure for lossless ion manipulations (SLIM) IM-MS
- Agilent MassHunter (.d) and UIMF mass spectrometry data files (MS-files)
- Agilent MassHunter (.d) and UIMF mass spectrometry data files
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pnnl_preprocessor_cq
    doi: 10.1021/jasms.4c00220
    title: PNNL PreProcessor
  dedup_kept_from: coll_pnnl_preprocessor_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00220
  all_source_dois:
  - 10.1021/jasms.4c00220
  - 10.1021/acs.jproteome.1c00425
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# frame-metadata-extraction-and-export

## Summary

Extract and export ion mobility frame metadata (field strength, pressure, temperature, MS actuals) from preprocessed IM-MS data files to structured text records for downstream analysis and instrumental parameter documentation.

## When to use

After completing multidimensional smoothing and saturation repair on Agilent MassHunter (.d) or UIMF IM-MS data files, when you need to capture and preserve the instrumental and physical conditions under which each ion mobility frame was acquired for reproducibility, calibration verification, or integration with external workflows.

## When NOT to use

- Input data has not undergone preprocessing (smoothing, saturation repair); metadata extraction should occur after, not before, quality-control steps.
- Metadata has already been extracted and exported in a prior pipeline run; re-exporting may create redundant records unless drift or recalibration is being tracked.
- Raw binary data from non-Agilent/non-UIMF instruments; the PNNL PreProcessor is vendor-specific and will not recognize other formats.

## Inputs

- Raw Agilent MassHunter (.d) data file
- Raw UIMF (Unified Ion Mobility Format) data file
- Preprocessed ion mobility frame data (after smoothing and saturation repair)

## Outputs

- Text file containing tabular frame metadata (field strength, pressure, temperature, MS actuals)
- Frame-level metadata records indexed by retention time and mobility
- Export log documenting metadata completeness and any missing or anomalous frames

## How to apply

Within the PNNL PreProcessor pipeline, invoke the metadata export utility after data preprocessing steps are complete. The utility scans the processed ion mobility frames and systematically extracts key instrumental parameters—field strength (V/cm), gas pressure (Torr), temperature (K), and MS acquisition settings—writing these to a structured text file. The metadata is generated per frame, allowing frame-by-frame condition tracking across the chromatographic/mobility separation. Verify that exported values are physically plausible (e.g., field strength within instrumental range, temperature stable across frames) and that no frames are missing records in the output log.

## Related tools

- **PNNL PreProcessor** (Host application that integrates metadata export as a utility within its preprocessing pipeline; provides UI or command-line entry point for extracting and writing frame metadata to disk.) — https://github.com/PNNL-Comp-Mass-Spec/PNNL-PreProcessor
- **Agilent MassHunter** (Data acquisition and file format provider; generates .d directory structure and embedded metadata that PNNL PreProcessor reads during extraction.)

## Evaluation signals

- Exported text file is non-empty, contains tabular headers (e.g., Frame_ID, Field_Strength_V_cm, Pressure_Torr, Temperature_K), and has one data row per ion mobility frame.
- All numeric metadata fields are physically plausible: field strength > 0 and within instrument specification (typically 50–600 V/cm for drift tubes), pressure in 0.5–4 Torr range for typical IM, temperature stable (±5 K) across the run.
- Export log or output summary shows no missing or dropped frames; frame count in metadata file matches frame count in preprocessed data.
- Spot-check: manually inspect 3–5 metadata rows and verify correspondence with known instrumental settings from the acquisition method file or instrument logbook.
- Metadata export completes without errors or warnings; if warnings appear (e.g., 'missing field strength in frame N'), investigate and document root cause.

## Limitations

- Metadata export is performed on a per-frame basis; if instrumental parameters drift during acquisition (e.g., temperature ramp, field strength adjustment), the export captures only the nominal or averaged value per frame, not continuous drift.
- The utility depends on complete and valid metadata being embedded in the source .d or UIMF file; corrupted or incomplete raw files may produce partial or missing metadata exports.
- Export format is fixed as text; users requiring machine-readable structured data (JSON, HDF5) must post-process the text output.
- Metadata accuracy is limited by the precision and calibration state of the Agilent instrument; field strength and temperature values are only as reliable as the instrument's onboard sensors at acquisition time.

## Evidence

- [other] PNNL-PreProcessor implements saturation repair as part of multidimensional smoothing of data, and provides metadata export functionality as separate utilities within its preprocessing pipeline for IM-MS workflows.: "provides metadata export functionality as separate utilities within its preprocessing pipeline"
- [other] Export ion mobility frame metadata (field strength, pressure, temperature, and MS actuals) to a text file.: "Export ion mobility frame metadata (field strength, pressure, temperature, and MS actuals) to a text file"
- [readme] data compression and interpolation, ion mobility demultiplexing, multidimensional smoothing, noise filtering by low intensity threshold and spike removal, saturation repair and metadata export: "saturation repair and metadata export"
- [methods] we have developed this user-friendly tool for Agilent MassHunter (.d) and UIMF mass spectrometry data files: "Agilent MassHunter (.d) and UIMF mass spectrometry data files"
- [methods] Multidimensional smoothing of data and repair of saturated peaks: "Multidimensional smoothing of data and repair of saturated peaks"
