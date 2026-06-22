---
name: ms1-composite-spectra-deconvolution
description: Use when you have high-resolution MS1 data (mzXML, mzML, or netCDF format) from LC/HRMS analysis and need to deconvolve composite spectra into individual fragmentation patterns without DDA or DIA acquisition.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - IDSL.CSA
  - R
  - IDSL.IPA
  - IDSL.FSA
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MS1-only Composite Spectra deconvolution

## Summary

MS1-only Composite Spectra Analysis (CSA) deconvolves fragmentation spectra from precursor mass-to-charge and retention time information alone, without reliance on tandem MS/MS data. This method is implemented in IDSL.CSA to streamline chemical structure annotation in untargeted metabolomics and exposomics workflows.

## When to use

Apply this skill when you have high-resolution MS1 data (mzXML, mzML, or netCDF format) from LC/HRMS analysis and need to deconvolve composite spectra into individual fragmentation patterns without DDA or DIA acquisition. Use it particularly for large population studies (n > 500) where you want to improve chemical structure annotation by aggregating annotated structures across aligned peaks using metadata such as InChIKey, SMILES, precursor type, or molecular formula.

## When NOT to use

- Input data already includes DDA or DIA fragmentation spectra; use the appropriate DDA or DIA analysis mode in IDSL.CSA instead.
- Raw mass spectrometry data has not been pre-processed by IDSL.IPA; chromatographic m/z-RT information is a mandatory prerequisite.
- Study population size is very small (n < 10) where peak alignment and aggregation across samples may be unreliable.

## Inputs

- mzXML, mzML, or netCDF raw mass spectrometry data files
- peaklists directory (output from IDSL.IPA workflow)
- peak_alignment directory (output from IDSL.IPA workflow)
- IDSL.CSA parameter spreadsheet (CSA_parameters.xlsx) with configured parameters

## Outputs

- MSP files (deconvoluted fragmentation spectra with annotations)
- adduct_annotation peaklists (with predicted adduct information)
- peak_alignment_subset (aligned peak tables for major ions in each CSA cluster)
- aligned_spectra_table (CSA aggregation results on aligned peak table)
- batch EIC figures (extracted ion chromatograms for DIA and CSA analyses)

## How to apply

First, process raw mass spectrometry data using the IDSL.IPA workflow to obtain m/z-RT chromatographic information and generate aligned peaklists and peak_alignment directories. Next, download and configure the IDSL.CSA parameter spreadsheet (CSA_parameters.xlsx), setting PARAM0001 to YES to process only the CSA workflow. Populate required parameters: CSA0005 (path to MS1 HRMS data), CSA0008 (path to peaklists directory), CSA0009 (path to peak_alignment directory), and CSA0011 (output directory). Adjust CSA0004 (number of processing threads) based on computational resources. Execute the IDSL.CSA_workflow() function with the configured spreadsheet, which will perform peak detection, chromatogram deconvolution, and spectrum aggregation to produce MSP files, adduct annotations, and aligned spectra tables with chemical structure information.

## Related tools

- **IDSL.CSA** (R package that implements MS1-only Composite Spectra deconvolution and orchestrates peak detection, chromatogram deconvolution, spectrum aggregation, and chemical structure annotation) — https://github.com/idslme/IDSL.CSA
- **IDSL.IPA** (Prerequisite workflow that processes raw mass spectrometry data and generates chromatographic m/z-RT information, peaklists, and peak_alignment outputs required as input to IDSL.CSA)
- **IDSL.FSA** (Downstream integration for annotating MSP files and generating fragmentation libraries from IDSL.CSA output)
- **R** (Programming environment in which IDSL.CSA package is executed)

## Examples

```
library(IDSL.CSA)
IDSL.CSA_workflow("/path/to/CSA_parameters.xlsx")
```

## Evaluation signals

- Output MSP files contain fragmentation spectra with non-null m/z and intensity values consistent with precursor masses from the input peaklists.
- Adduct_annotation peaklists show predicted adduct types (e.g., [M+H]+, [M+Na]+, [M-H]-) aligned with input m/z values within instrument mass accuracy (typically < 5 ppm for Orbitrap data).
- aligned_spectra_table demonstrates successful aggregation by grouping peaks with identical or near-identical InChIKey, SMILES, or molecular formula across the study population.
- Peak_alignment_subset files contain fewer peaks than the input aligned peak table, confirming that major ions in each CSA cluster have been successfully extracted.
- Batch EIC figures show distinct, resolved chromatographic peaks with expected retention time ranges and m/z accuracy for the analyzed compound set.

## Limitations

- Method relies on high-resolution MS1 data; lower-resolution instruments (TOF, QQQ) may not provide sufficient mass accuracy for reliable deconvolution and chemical annotation.
- Performance depends critically on the quality of input m/z-RT information from IDSL.IPA; poor peak detection or misaligned peaks in the prerequisite workflow will propagate errors into CSA output.
- The approach does not generate fragmentation patterns de novo; it deconvolves composites of existing MS1 signals and requires reference libraries or external fragmentation data for chemical structure confirmation.
- Aggregation across multiple precursor types (adducts, isotopologues, in-source fragments) may produce ambiguous chemical annotations if reference metadata is incomplete or conflicts occur.

## Evidence

- [abstract] MS1-only Composite Spectra deconvolution Analysis (CSA): "This package can be used for the deconvolution of fragmentation spectra obtained through various analytical methods such as MS1-only Composite Spectra deconvolution Analysis (CSA)"
- [readme] IDSL.IPA prerequisite and parameter spreadsheet: "Prior to processing your mass spectrometry data (mzXML, mzML, netCDF) using the IDSL.CSA workflow, mass spectrometry data should be processed using the IDSL.IPA workflow to acquire chromatographic"
- [readme] Unique spectra aggregation feature: "Aggregating annotated chemical structures on the aligned peak table using meta-variables such as InChIKey, SMILES, precursor type, molecular formula,... depending on the information in the reference"
- [readme] Output format and purpose: "4.1. CSA_MSP includes .msp file 4.2. CSA_adduct_annotation includes peaklists with potential adduct information 4.3. peak_alignment_subset includes subsets of aligned peak tables for the major ions"
- [readme] Large population study capability: "Analyzing population size untargeted studies (n > 500)"
- [intro] Aim and scope of the skill: "The aim of the IDSL.CSA package is to assist in streamlining the data analysis process and improving the overall chemical structure annotation in the fields of metabolomics and exposomics"
