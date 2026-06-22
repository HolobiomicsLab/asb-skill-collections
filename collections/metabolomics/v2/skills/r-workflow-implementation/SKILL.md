---
name: r-workflow-implementation
description: Use when you have raw mass spectrometry data in mzXML, mzML, or netCDF format from untargeted LC/HRMS analysis that has been pre-processed by IDSL.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - IDSL.CSA
  - R
  - IDSL.IPA
  - IDSL.FSA
  techniques:
  - tandem-MS
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

# r-workflow-implementation

## Summary

Implement an R-based metabolomics workflow that deconvolves fragmentation spectra from raw mass spectrometry data (mzXML, mzML, netCDF) through multiple analytical methods (MS1-only CSA, DDA, DIA) to produce annotated chemical structures and aligned peak tables. This skill bridges raw instrument data to chemical annotation through parameter-driven batch processing.

## When to use

You have raw mass spectrometry data in mzXML, mzML, or netCDF format from untargeted LC/HRMS analysis that has been pre-processed by IDSL.IPA to generate chromatographic peak information (m/z-RT coordinates), and you need to deconvolve composite or multiplexed fragmentation spectra into individual ion spectra to enable chemical structure annotation in metabolomics or exposomics studies.

## When NOT to use

- Raw MS data has not been pre-processed by IDSL.IPA to generate m/z-RT chromatographic information; IDSL.CSA requires this intermediate product as mandatory input.
- Input data is already in feature table or abundance matrix format (post-peak-picking); IDSL.CSA operates on raw instrument files, not derived features.
- Sample cohort size is very small (n < 3) or analytical scope is single-replicate; the workflow is optimized for untargeted population studies with n > 500 and requires sufficient replication for alignment and annotation quality.

## Inputs

- Raw mass spectrometry data files (mzXML, mzML, or netCDF format)
- IDSL.IPA-generated peaklists directory (peak list tables with m/z-RT)
- IDSL.IPA-generated peak_alignment directory (aligned peak tables)
- IDSL.CSA parameter spreadsheet (populated with analysis parameters)

## Outputs

- Deconvoluted fragmentation spectra (.msp files)
- Adduct-annotated peaklists
- Aligned peak table subsets for major ions in each cluster
- Aggregated spectra table with annotated chemical structures and meta-variables
- Batch extracted ion chromatogram figures (EIC)
- Chemical structure annotations (InChIKey, SMILES, molecular formula)

## How to apply

First, ensure your raw MS data has been processed through IDSL.IPA to generate peaklists and peak_alignment directories containing m/z-RT information. Download and populate the IDSL.CSA parameter spreadsheet (39 parameters across 5 sections), specifying: (1) analytical method (CSA, DDA, or DIA mode) via PARAM0001; (2) input paths for HRMS data (CSA0005), peaklists directory (CSA0008), and peak_alignment directory (CSA0009); (3) output directory for .msp files and extracted ion chromatogram figures (CSA0011); and (4) number of processing threads (CSA0004) matching your computational capacity. Execute the workflow via IDSL.CSA_workflow() in R, which will perform peak detection, chromatogram deconvolution, optional spectra aggregation by meta-variables (InChIKey, SMILES, molecular formula), and batch figure generation. The workflow produces structured outputs including deconvoluted .msp files, adduct-annotated peaklists, aligned peak table subsets for major ions, and aggregated spectra metadata enabling downstream chemical structure matching.

## Related tools

- **IDSL.IPA** (Prerequisite workflow to generate m/z-RT chromatographic peak information and aligned peak lists required as input to IDSL.CSA) — https://github.com/idslme/IDSL.IPA
- **IDSL.FSA** (Downstream integration for annotating MSP files and generating fragmentation libraries from IDSL.CSA outputs) — https://github.com/idslme/IDSL.FSA
- **IDSL.CSA** (Core R package implementing MS1-only Composite Spectra deconvolution, DDA, and DIA analytical methods for fragmentation spectrum deconvolution and chemical structure annotation) — https://github.com/idslme/IDSL.CSA

## Examples

```
library(IDSL.CSA)
IDSL.CSA_workflow("/path/to/CSA_parameters.xlsx")
```

## Evaluation signals

- All output directories (CSA_MSP, CSA_adduct_annotation, peak_alignment_subset, aligned_spectra_table) are generated with expected file structure and non-empty content.
- .msp files are valid, properly formatted MSP spectra libraries containing deconvoluted fragmentation spectra with mass, intensity, and metadata annotations.
- Adduct-annotated peaklists contain populated columns for adduct type, precursor m/z, and neutral mass; cross-validate a subset of m/z values against input peak lists to ensure alignment consistency.
- Aggregated spectra table contains meta-variable columns (InChIKey, SMILES, molecular formula) with non-null annotations for a majority of aligned features, indicating successful chemical structure matching.
- Extracted ion chromatogram (EIC) figures are generated in batch without errors and display distinct, resolvable peaks for major ions within each CSA cluster; inspect a sample EIC to verify deconvolution quality.

## Limitations

- Workflow requires pre-processing by IDSL.IPA; if this upstream step is not performed correctly, IDSL.CSA will fail or produce low-quality deconvolutions.
- Chemical structure annotation accuracy depends on the quality and completeness of the reference library used; no changelog is publicly documented, limiting tracking of annotation database updates.
- Parallel processing performance is limited by available computational threads (CSA0004); memory requirements scale with sample size (study cohorts with n > 500 require substantial RAM).
- Spectra aggregation by meta-variables (InChIKey, SMILES) is contingent on reference library format and information completeness; incomplete or non-standardized library entries will result in partial or missing annotations.

## Evidence

- [readme] Prior to processing your mass spectrometry data (mzXML, mzML, netCDF) using the IDSL.CSA workflow, mass spectrometry data should be processed using the IDSL.IPA workflow: "Prior to processing your mass spectrometry data (**mzXML**, **mzML**, **netCDF**) using the IDSL.CSA workflow, mass spectrometry data should be processed using the"
- [readme] The Composite Spectra Analysis requires 39 parameters distributed into 5 separate sections for a full scale analysis: "The **Composite Spectra Analysis** requires 39 parameters distributed into 5 separate sections for a full scale analysis."
- [intro] This package can be used for the deconvolution of fragmentation spectra obtained through various analytical methods such as MS1-only Composite Spectra deconvolution Analysis (CSA), Data Dependent Acquisition (DDA), and various Data-Independent Acquisition (DIA) methods: "This package can be used for the deconvolution of fragmentation spectra obtained through various analytical methods such as MS1-only Composite Spectra deconvolution Analysis (**CSA**), Data Dependent"
- [readme] Aggregating annotated chemical structures on the aligned peak table using meta-variables such as InChIKey, SMILES, precursor type, molecular formula, depending on the information in the reference library: "Aggregating annotated chemical structures on the aligned peak table using meta-variables such as InChIKey, SMILES, precursor type, molecular formula,... depending on the information in the reference"
- [intro] The aim of the IDSL.CSA package is to assist in streamlining the data analysis process and improving the overall chemical structure annotation in the fields of metabolomics and exposomics: "The aim of the **IDSL.CSA** package is to assist in streamlining the data analysis process and improving the overall chemical structure annotation in the fields of metabolomics and exposomics."
- [readme] Analyzing population size untargeted studies (n > 500): "Analyzing population size untargeted studies (n > 500)"
