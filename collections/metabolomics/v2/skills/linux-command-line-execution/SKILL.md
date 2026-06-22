---
name: linux-command-line-execution
description: Use when you have vendor-specific raw mass spectrometry data (ThermoFisher .raw, Agilent .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MSThunder
  - Ubuntu
  - MSConvert
  - Ubuntu 20.04
  techniques:
  - LC-MS
derived_from:
- doi: 10.1016/j.enceco.2025.07.022
  title: MSThunder
evidence_spans:
- MSThunder provide a deep learning-based nontargeted analytical framework for the accurate and rapid identification of unknown organic pollutants in water
- available through our experiments conducted on an Ubuntu 20.04 environment
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msthunder_cq
    doi: 10.1016/j.enceco.2025.07.022
    title: MSThunder
  dedup_kept_from: coll_msthunder_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1016/j.enceco.2025.07.022
  all_source_dois:
  - 10.1016/j.enceco.2025.07.022
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# linux-command-line-execution

## Summary

Execute MSConvert on a Linux system (Ubuntu 20.04 or compatible) to convert vendor-specific raw mass spectrometry data (ThermoFisher .raw, Agilent .d) into MSThunder-compatible formats. This skill bridges raw instrument output and downstream deep-learning-based pollutant identification.

## When to use

You have vendor-specific raw mass spectrometry data (ThermoFisher .raw, Agilent .d, or equivalent) that must be converted to a format compatible with MSThunder analysis for nontargeted identification of unknown organic pollutants in water, and you have access to a Linux environment (Ubuntu 20.04 or compatible).

## When NOT to use

- Raw data is already in mzML, mzXML, or another format already compatible with MSThunder — skip conversion and proceed directly to analysis.
- You do not have access to a Linux environment or cannot install MSConvert; alternative preprocessing workflows or vendor-supplied converters may be required.
- Input data is from an unsupported vendor or instrument type for which MSConvert does not provide conversion support.

## Inputs

- Raw mass spectrometry data file (ThermoFisher .raw, Agilent .d, or vendor-equivalent format)
- Linux environment with MSConvert installed (Ubuntu 20.04 or compatible)
- Target output format specification (mzML or equivalent MSThunder-compatible format)

## Outputs

- Converted mass spectrometry data file in MSThunder-compatible format (mzML or equivalent)
- Converted file ready for batch processing or interactive analysis in MSThunder

## How to apply

Install and configure MSConvert on Ubuntu 20.04 or a compatible Linux system. Obtain the vendor-specific raw data file(s) (ThermoFisher .raw, Agilent .d, or equivalent format) and place them in an accessible directory. Execute the MSConvert command-line tool, targeting an output format compatible with MSThunder (typically mzML or mzXML). Validate the converted file for integrity and format compliance (e.g., presence of MS1/MS2 spectra, correct precursor/retention time metadata). Return the converted file to the host system for subsequent analysis using MSThunder's interface or batch-processing pipeline.

## Related tools

- **MSConvert** (Command-line tool that performs the conversion of vendor-specific raw mass spectrometry data into MSThunder-compatible output formats)
- **MSThunder** (Deep learning-based nontargeted analytical framework that receives the converted data for identification of unknown organic pollutants) — https://github.com/LQZ0123/MSThunder
- **Ubuntu 20.04** (Operating system environment in which MSConvert and the raw data conversion workflow are executed)

## Evaluation signals

- Converted file is present on the file system and has a valid MSThunder-compatible format extension (.mzML, .mzXML, or documented equivalent).
- File integrity check: converted file can be opened and parsed by MSThunder without format errors or corruption.
- Metadata preservation: precursor m/z values, retention times, MS1 and MS2 spectra, and ion mode (positive/negative) are correctly transferred from the original vendor format.
- File size and content comparison: converted file contains expected number and types of spectra relative to the original raw data (no major loss of data during conversion).
- Downstream validation: MSThunder successfully ingests the converted file and produces candidate compound matches without parsing or schema violations.

## Limitations

- Current MSThunder version does not support offline processing of raw data; conversion must occur followed by return and analysis of the converted file.
- Conversion workflow is limited to vendors whose raw formats are supported by MSConvert (ThermoFisher, Agilent, and others); unsupported formats will fail conversion.
- Linux environment setup (Ubuntu 20.04 or compatible) and MSConvert installation are prerequisites; platform-specific configuration issues may arise.
- Online processing capability for raw UPLC-HRMS data is under development; alternative workaround is to send raw files to the MSThunder maintainers or upload to Zenodo/GNPS for processing.

## Evidence

- [other] Raw data from ThermoFisher, Agilent, and other vendors is processed in a Linux system and converted via MSConvert: "Raw data from ThermoFisher, Agilent, and other vendors is processed in a Linux system and converted via MSConvert, after which the converted file is returned for subsequent analysis"
- [other] Install and configure MSConvert on a Linux system (Ubuntu 20.04 or compatible) and execute conversion targeting MSThunder-compatible output format: "1. Install and configure MSConvert on a Linux system (Ubuntu 20.04 or compatible). 2. Obtain vendor-specific raw data file(s) (ThermoFisher .raw, Agilent .d, or equivalent format). 3. Execute"
- [other] Validate converted file integrity and format compliance before returning for downstream MSThunder analysis: "4. Validate converted file integrity and format compliance. 5. Return the converted file for downstream MSThunder analysis."
- [readme] MSThunder version does not yet support offline processing of raw data; raw data must be processed in Linux and returned as converted file: "Due to environment configuration issues, the current version does not yet support offline processing of raw data."
- [readme] MSThunder is compatible with ThermoFisher, Agilent, and other vendors whose raw data can be converted via MSConvert: "The current version is compatible with ThermoFisher, Agilent, and other vendors whose raw data can be converted via MSConvert."
