---
name: dda-precursor-fragment-ion-grouping
description: Use when when you have raw DDA mass spectrometry data (mzML, mzXML, or netCDF format) where precursor ions have been fragmented and you need to associate each fragment ion back to its parent precursor ion to generate coherent, precursor-specific fragmentation spectra for chemical annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0625
  tools:
  - IDSL.CSA
  - R
  - IDSL.IPA
derived_from:
- doi: 10.1021/acs.analchem.3c00376
  title: IDSL.CSA
evidence_spans:
- The **Composite Spectra Analysis (IDSL.CSA)** R package for the analysis of mass spectrometry data
- The **Composite Spectra Analysis (IDSL.CSA)** R package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_idsl_csa_cq
    doi: 10.1021/acs.analchem.3c00376
    title: IDSL.CSA
  dedup_kept_from: coll_idsl_csa_cq
schema_version: 0.2.0
---

# DDA Precursor-Fragment Ion Grouping

## Summary

Groups precursor ions with their corresponding fragment ions in Data Dependent Acquisition mass spectrometry data by linking them through retention time and m/z relationships. This deconvolution step is essential for reconstructing composite fragmentation spectra from DDA experiments in untargeted metabolomics.

## When to use

When you have raw DDA mass spectrometry data (mzML, mzXML, or netCDF format) where precursor ions have been fragmented and you need to associate each fragment ion back to its parent precursor ion to generate coherent, precursor-specific fragmentation spectra for chemical annotation.

## When NOT to use

- Input data is already in MS1-only (non-fragmentation) format or lacks fragmentation scans — use CSA (Composite Spectra Analysis) instead.
- Mass spectrometry data was acquired using Data-Independent Acquisition (DIA) methods (MS/E, AIF, SWATH-MS) — use the DIA-specific deconvolution workflow.
- The raw data file is not in a supported format (mzML, mzXML, or netCDF) or chromatographic peak information has not been pre-processed by IDSL.IPA.

## Inputs

- Raw DDA mass spectrometry data file (mzML format)
- Raw DDA mass spectrometry data file (mzXML format)
- Chromatographic information (m/z–RT) from prior IDSL.IPA workflow processing

## Outputs

- Deconvoluted fragmentation spectra table (precursor m/z, retention time, grouped fragment ion intensities)
- Composite spectrum object with aggregated fragment ions per precursor
- .msp files containing deconvoluted spectra

## How to apply

Load the DDA raw mass spectrometry data file in mzML or mzXML format into the IDSL.CSA R package. Apply the DDA-specific deconvolution algorithm, which uses retention time and m/z relationships as the linking criterion to group fragment ions with their precursor ions. The algorithm aggregates all fragment ion intensities observed for each unique precursor ion across the chromatographic dimension. Output the result as a structured table containing precursor m/z, retention time, and the full set of grouped fragment ion intensities. Validate by checking that all fragment ions are correctly associated with their parent precursor based on temporal co-elution and charge state consistency.

## Related tools

- **IDSL.CSA** (R package that implements the DDA deconvolution algorithm; groups precursor and fragment ions and outputs structured composite spectra) — https://github.com/idslme/IDSL.CSA
- **IDSL.IPA** (Prerequisite workflow that generates chromatographic peak information (m/z–RT) required as input to IDSL.CSA DDA analysis) — https://github.com/idslme/IDSL.IPA
- **R** (Runtime environment for executing IDSL.CSA package and DDA deconvolution workflow)

## Examples

```
library(IDSL.CSA)
IDSL.CSA_workflow("path/to/CSA_parameters.xlsx")
```

## Evaluation signals

- All fragment ions are correctly time-aligned with their precursor ion (no orphaned fragments or false associations across retention time boundaries).
- Precursor m/z, retention time, and fragment ion intensities are present and numerically valid in output tables (no NaN or missing values for linked spectra).
- Fragment ion m/z values are less than or equal to the precursor m/z (fragments cannot be heavier than their parent).
- Aggregated fragment intensities sum to non-zero values and are consistent across repeated analyses of the same raw data file.
- Output .msp files conform to the MSP spectral library format with correctly populated metadata (precursor m/z, RT, fragment m/z–intensity pairs).

## Limitations

- DDA deconvolution relies on accurate retention time and m/z alignment; significant chromatographic peak tailing or m/z calibration drift can lead to incorrect precursor–fragment associations.
- Overlapping precursor ions that co-elute at the same retention time may result in ambiguous or mixed fragmentation spectra.
- The method requires prior processing with IDSL.IPA to obtain chromatographic information (m/z–RT); it is not a standalone preprocessing step.
- Very large population studies (n > 500) may require parallel processing configuration to complete within reasonable computational time.

## Evidence

- [other] DDA deconvolution definition and grouping criterion: "Apply the DDA-specific deconvolution algorithm to group precursor ions with their corresponding fragment ions based on retention time and m/z relationships."
- [readme] Supported input file formats: "mass spectrometry data (**mzXML**, **mzML**, **netCDF**)"
- [other] Output structure and content: "Output the deconvoluted spectra as a structured table or composite spectrum object containing precursor m/z, retention time, and grouped fragment ion intensities."
- [readme] IDSL.CSA scope and analytical methods supported: "This package can be used for the deconvolution of fragmentation spectra obtained through various analytical methods such as MS1-only Composite Spectra deconvolution Analysis (**CSA**), Data Dependent"
- [readme] IDSL.IPA prerequisite requirement: "Prior to processing your mass spectrometry data using the IDSL.CSA workflow, mass spectrometry data should be processed using the [IDSL.IPA](https://github.com/idslme/IDSL.IPA) workflow to acquire"
