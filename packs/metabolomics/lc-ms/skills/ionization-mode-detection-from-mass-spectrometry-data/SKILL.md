---
name: ionization-mode-detection-from-mass-spectrometry-data
description: Use when when you have raw LC-MS data in mzML format (converted from .raw or acquired directly in that format) and need to invoke Asari for feature extraction, but the ionization mode is not explicitly specified in your experimental metadata or pipeline configuration.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3630
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Asari
  - Python
  - ThermoRawFileParser
  techniques:
  - LC-MS
  - GC-MS
derived_from:
- doi: 10.1371/journal.pcbi.1011912
  title: pcpfm
evidence_spans:
- pcpfm asari -i ./my_experiment
- Python-Centric Pipeline for Metabolomics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pcpfm_cq
    doi: 10.1371/journal.pcbi.1011912
    title: pcpfm
  dedup_kept_from: coll_pcpfm_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1011912
  all_source_dois:
  - 10.1371/journal.pcbi.1011912
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ionization-mode-detection-from-mass-spectrometry-data

## Summary

Infer the ionization polarity (positive or negative) from mzML file headers prior to feature extraction, enabling correct parameterization of Asari processing. This is a prerequisite step that ensures downstream feature detection uses appropriate ion mass-to-charge calibration for the experimental acquisition mode.

## When to use

When you have raw LC-MS data in mzML format (converted from .raw or acquired directly in that format) and need to invoke Asari for feature extraction, but the ionization mode is not explicitly specified in your experimental metadata or pipeline configuration. The mode must be inferred from the mzML file headers before Asari processing begins.

## When NOT to use

- Ionization mode is already explicitly provided in your experiment metadata or configuration file — use the metadata value directly instead of re-inferring from headers.
- Input files are not in mzML format or do not contain properly formatted MS1 scan headers.
- You are working with GC-MS or other non-LC-MS data types (support under development; not yet fully integrated into PCPFM).

## Inputs

- centroid mzML files (from converted .raw acquisitions or native LC-MS output)
- mzML file headers containing MS1 scan metadata

## Outputs

- ionization mode (positive or negative)
- validated mode parameter ready for Asari invocation

## How to apply

Parse the mzML file headers (MS1 scan metadata) to identify the ionization polarity setting recorded during acquisition. The mzML format encodes the polarity (positive or negative ion mode) in the scan attributes. Extract this value programmatically before invoking Asari with the converted_acquisitions subdirectory. Pass the inferred mode as a parameter to Asari so that feature grouping, m/z tolerance (5 ppm default), and ion mass calculations operate under the correct polarity context. This inferred mode is then used consistently across all downstream feature extraction, annotation, and quality control steps.

## Related tools

- **Asari** (accepts inferred ionization mode to parameterize feature extraction with correct m/z tolerance and ion mass calculations) — https://github.com/shuzhao-li/asari
- **Python** (language for programmatically parsing mzML headers and extracting polarity metadata)
- **ThermoRawFileParser** (upstream tool that converts .raw to mzML, encoding polarity information in output headers)

## Evaluation signals

- mzML files successfully parsed and polarity attribute read without errors.
- Inferred ionization mode (positive or negative) is consistent across all files in the acquisition batch.
- Asari processes the mzML files using the inferred mode without reporting polarity-related warnings or errors.
- Generated feature tables (full and preferred) contain m/z and intensity values consistent with the inferred ionization polarity (e.g., positive mode should yield predominantly positive m/z features).
- Downstream annotation steps (MS1, MS2) produce sensible compound matches using the mode-appropriate mass calibration.

## Limitations

- Relies on correct encoding of polarity metadata in mzML headers; corrupted or non-standard headers may cause inference to fail.
- Does not validate whether the inferred mode matches the actual chemistry of the sample; a mislabeled acquisition will propagate incorrect mode inference.
- Support for mixed-mode or alternating-polarity acquisitions is not yet implemented in PCPFM (under development).
- GC-MS and other non-LC-MS data types are not yet fully supported in the pipeline.

## Evidence

- [other] Load the PCPFM experiment object and infer the ionization mode (positive or negative) from the mzML file headers.: "infer the ionization mode (positive or negative) from the mzML file headers"
- [other] Invoke Asari with the inferred ionization mode on the converted_acquisitions subdirectory containing centroid .mzML files, using default parameters (5 ppm m/z tolerance, 2 second retention time tolerance for feature grouping).: "Invoke Asari with the inferred ionization mode on the converted_acquisitions subdirectory containing centroid .mzML files"
- [readme] Inputs should include a set of raw files (.raw or .mzML) and a csv file for metadata (minimal sample names and file path).: "Inputs should include a set of raw files (.raw or .mzML) and a csv file for metadata"
