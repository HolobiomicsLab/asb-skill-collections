---
name: dia-data-format-recognition
description: Use when you have raw mass spectrometry data from a DIA acquisition method and need to determine whether it is MS^E, All-Ion Fragmentation (AIF), or SWATH-MS before loading into IDSL.CSA for fragmentation spectra deconvolution.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - IDSL.CSA
  - R
  techniques:
  - LC-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c00376
  all_source_dois:
  - 10.1021/acs.analchem.3c00376
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# DIA Data Format Recognition

## Summary

Identify and classify Data-Independent Acquisition (DIA) mass spectrometry data formats (MS^E, AIF, SWATH-MS) to select the appropriate deconvolution algorithm and processing pipeline. This skill is essential for routing composite spectra to the correct analytical method within IDSL.CSA.

## When to use

You have raw mass spectrometry data from a DIA acquisition method and need to determine whether it is MS^E, All-Ion Fragmentation (AIF), or SWATH-MS before loading into IDSL.CSA for fragmentation spectra deconvolution. Metadata from the instrument acquisition log, file headers (mzXML, mzML, netCDF), or experimental protocol documentation should be available to classify the DIA variant.

## When NOT to use

- Data was acquired using Data Dependent Acquisition (DDA) or MS1-only methods — use DDA or CSA analytical workflows instead.
- Raw data file format is already pre-processed into extracted ion chromatograms or aligned peak tables — format recognition applies only to raw instrument output.
- Metadata or file headers are absent or corrupted and DIA variant cannot be determined from acquisition parameters.

## Inputs

- Raw DIA mass spectrometry data file (mzXML, mzML, or netCDF format)
- Instrument acquisition metadata or experimental protocol documentation
- IDSL.CSA parameter spreadsheet with DIA method selection

## Outputs

- Classified DIA data variant identifier (MS^E, AIF, or SWATH-MS)
- Routed data stream to appropriate IDSL.CSA deconvolution algorithm
- Deconvoluted fragmentation spectra (mzML, mzXML, or CSV table format)

## How to apply

Examine the raw data file format and metadata to identify the DIA acquisition scheme used. MS^E uses alternating low and high collision energy scans; AIF fragments all ions in a single acquisition; SWATH-MS uses sequential, overlapping mass windows with fixed isolation widths. Select the corresponding DIA analytical variant in IDSL.CSA (via parameter configuration in the IDSL.CSA parameter spreadsheet), which determines how composite spectra are parsed and deconvoluted. Load the classified DIA raw data (mzXML, mzML, or netCDF format) into the IDSL.CSA R package environment using the IDSL.CSA_workflow() function with the appropriate DIA method parameter. Verification occurs when the deconvolution algorithm successfully processes the composite spectra without format mismatch errors and produces structurally valid fragmentation spectra in the output format.

## Related tools

- **IDSL.CSA** (Executes DIA deconvolution algorithm after format is recognized; routes classified data to MS^E, AIF, or SWATH-MS specific processing pipeline) — https://github.com/idslme/IDSL.CSA
- **R** (Runtime environment for IDSL.CSA workflow and parameter configuration)

## Examples

```
library(IDSL.CSA); IDSL.CSA_workflow("path/to/CSA_parameters.xlsx")
```

## Evaluation signals

- DIA variant (MS^E, AIF, or SWATH-MS) is correctly identified from file metadata and instrument acquisition scheme matches expected characteristics for that method.
- Deconvolution algorithm executes without format mismatch or parsing errors specific to incorrect DIA variant selection.
- Output fragmentation spectra contain expected m/z and intensity distributions consistent with the deconvolution method for the identified DIA variant.
- Exported spectra can be successfully matched against reference libraries and produce chemical structure annotations with acceptable cosine similarity or other relevance metrics.
- No systematic gaps or artifacts in deconvoluted spectra that would indicate misclassification (e.g., missing low-mass fragments if SWATH window boundaries were not recognized).

## Limitations

- Format recognition depends on accurate file headers and metadata; corrupted or non-standard raw data files may not be correctly classified.
- IDSL.CSA requires prior processing of chromatographic information (m/z and retention time) using IDSL.IPA workflow before DIA deconvolution; format recognition alone is insufficient for complete analysis.
- Hybrid or instrument-specific DIA variants not explicitly listed (MS^E, AIF, SWATH-MS) may not be supported and require custom configuration.
- No automated format detection is described; user must manually specify the DIA method in the IDSL.CSA parameter spreadsheet based on metadata inspection.

## Evidence

- [other] DIA method selection: "This package can be used for the deconvolution of fragmentation spectra obtained through various analytical methods such as MS1-only Composite Spectra deconvolution Analysis (CSA), Data Dependent"
- [other] Workflow step — select DIA variant: "Select the appropriate DIA analytical variant (MSE, AIF, or SWATH-MS) based on the input data type. 3. Execute the DIA deconvolution algorithm within IDSL.CSA to process the composite spectra and"
- [readme] Supported file formats: "Prior to processing your mass spectrometry data (mzXML, mzML, netCDF) using the IDSL.CSA workflow, mass spectrometry data should be processed using the IDSL.IPA workflow"
- [readme] Parameter-driven variant selection: "download the IDSL.CSA parameter spreadsheet and select the parameters accordingly and then use this spreadsheet as the input for the IDSL.CSA workflow"
