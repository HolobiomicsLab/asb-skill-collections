---
name: mass-recalibration-lock-mass-correction
description: Use when converting mzML files to imzML format for imaging mass spectrometry data and you have a known internal standard (lock mass) whose exact m/z value is available. Use it specifically during the metadata annotation stage (iw_utils.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - imzML Writer
  - imzML Scout
  - msconvert
derived_from:
- doi: 10.1021/acs.analchem.4c06520
  title: imzML Writer
evidence_spans:
- import os import imzml_writer.utils as iw_utils
- iw_utils.mzML_to_imzML_convert(PATH=mzML_path)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_imzml_writer_cq
    doi: 10.1021/acs.analchem.4c06520
    title: imzML Writer
  dedup_kept_from: coll_imzml_writer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c06520
  all_source_dois:
  - 10.1021/acs.analchem.4c06520
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-recalibration-lock-mass-correction

## Summary

Mass recalibration using lock mass correction is a method to correct mass measurement errors in MS imaging data by designating a known internal standard ion (lock mass) as a reference point and using it to retroactively recalibrate m/z values across all pixels in an imzML file. This ensures accurate mass assignment throughout the imaging dataset and improves compatibility with downstream analysis software.

## When to use

Apply this skill when converting mzML files to imzML format for imaging mass spectrometry data and you have a known internal standard (lock mass) whose exact m/z value is available. Use it specifically during the metadata annotation stage (iw_utils.imzML_metadata_process) after pixel alignment is complete, particularly when mass measurement drift or systematic error is suspected across the tissue or sample surface.

## When NOT to use

- Input data is already in a vendor instrument format (.raw) — perform RAW-to-mzML conversion first
- No internal standard or lock mass reference is available or detectable in the dataset
- Mass recalibration has already been applied during the initial msconvert or mzML generation step

## Inputs

- mzML files from prior RAW-to-mzML conversion
- imzML barebones structure with aligned pixels from prior mzML_to_imzML_convert step
- Lock mass m/z value (float; m/z of internal standard ion)
- Raw data path containing experimental metadata

## Outputs

- Recalibrated imzML files with corrected m/z values across all pixels
- imzML files annotated with lock mass and recalibration parameters
- Recalibrated files organized by scan filter and placed in output directory

## How to apply

During imzML metadata annotation, specify the m/z value of a known internal standard ion as the lock mass parameter. The imzML Writer processes this lock mass reference through iw_utils.imzML_metadata_process(), which uses it as a calibration point to correct mass measurement errors across all pixels in the dataset. The lock mass value serves as the reference for mass recalibration, allowing the algorithm to compute and apply systematic corrections to align observed m/z values with theoretical values. This corrected imzML file is then placed in the output directory with mass errors mitigated, improving downstream analysis accuracy.

## Related tools

- **imzML Writer** (Primary tool that orchestrates metadata annotation and lock mass recalibration via iw_utils.imzML_metadata_process() function) — https://github.com/VIU-Metabolomics/imzML_Writer
- **imzML Scout** (Downstream visualization and validation tool to inspect recalibrated mass images and verify lock mass correction effectiveness) — https://github.com/VIU-Metabolomics/imzML_Writer
- **msconvert** (Preceding tool that converts raw vendor files to mzML; lock mass recalibration is applied post-mzML generation) — https://proteowizard.sourceforge.io/

## Examples

```
import imzml_writer.iw_utils as iw_utils; iw_utils.imzML_metadata_process(model_files='data/sample.mzML', x_speed=500.0, y_step=100.0, path='data/raw/', lock_mass=829.5388)
```

## Evaluation signals

- Output imzML file contains lock mass metadata embedded in XML header and annotation records
- Mass accuracy of known ions in ion images matches theoretical m/z within expected tolerance (typically <5 ppm after recalibration)
- Lock mass ion m/z value observed in mass spectra extracted from individual pixels is within <0.005 Da of the input lock mass reference
- Output file is readable by imzML Scout and other certified imzML readers (Cardinal MSI, METASPACE, M2aia, MSIReader, etc.) without parsing errors
- Visual inspection of ion images for internal standards shows no systematic m/z drift across tissue surface post-recalibration

## Limitations

- Lock mass correction requires an internal standard to be present and detectable in the mass spectra; if the standard is absent or signal is weak, recalibration may be ineffective or noisy
- Mass recalibration is applied globally across all pixels; if lock mass is not present or varies spatially, correction may introduce systematic error rather than resolve it
- The skill is not applicable to raw vendor format files (.raw); RAW-to-mzML conversion via msconvert must precede this step
- Accuracy of recalibration depends on the precision of the input lock mass m/z value; typos or incorrect reference values will propagate as systematic error through the entire dataset

## Evidence

- [methods] Lock mass: m/z of a known ion (typically m/z of an internal standard). This serves as a reference point to correct any mass measurement errors: "Lock mass: m/z of a known ion (typically m/z of an internal standard). This serves as a reference point to correct any mass measurement errors"
- [other] iw_utils.imzML_metadata_process(model_files=mzML_path, x_speed=x_scan_speed, y_step=y_step_size, path=raw_data_path) to annotate imzML files with experimental parameters (lock mass for mass recalibration, imaging coordinates, and MS acquisition metadata): "iw_utils.imzML_metadata_process(model_files=mzML_path, x_speed=x_scan_speed, y_step=y_step_size, path=raw_data_path) to annotate imzML files with experimental parameters (lock mass for mass"
- [methods] imzML files generated with imzML_Writer are compatible with multiple imzML file readers both commercially and as open-source software: "imzML files generated with imzML_Writer are compatible with multiple imzML file readers both commercially and as open-source software"
- [readme] Using imzML Writer depends on msconvert for conversion of raw vendor files to the open format mzML.: "Using imzML Writer depends on msconvert for conversion of raw vendor files to the open format mzML."
