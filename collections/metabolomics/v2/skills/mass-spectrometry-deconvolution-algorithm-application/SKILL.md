---
name: mass-spectrometry-deconvolution-algorithm-application
description: Use when you have raw DDA, DIA (MS^E, AIF, SWATH-MS), or MS1-only mass spectrometry data in mzML, mzXML, or netCDF format and need to deconvolute fragmentation spectra by linking precursor ions to their fragment ions based on retention time and m/z relationships.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
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

# mass-spectrometry-deconvolution-algorithm-application

## Summary

Apply deconvolution algorithms to fragmentation spectra from Data Dependent Acquisition (DDA), Data-Independent Acquisition (DIA), or MS1-only Composite Spectra Analysis (CSA) mass spectrometry data to group precursor ions with their corresponding fragment ions. This skill enables streamlined chemical structure annotation in metabolomics and exposomics workflows.

## When to use

You have raw DDA, DIA (MS^E, AIF, SWATH-MS), or MS1-only mass spectrometry data in mzML, mzXML, or netCDF format and need to deconvolute fragmentation spectra by linking precursor ions to their fragment ions based on retention time and m/z relationships. Apply this skill when you require structured deconvoluted spectra with aggregated fragment ion intensities for downstream chemical annotation.

## When NOT to use

- Input data has not been preprocessed with IDSL.IPA or equivalent chromatographic information extraction — m/z–RT alignment is mandatory.
- Data is already in processed feature table or aggregated peak matrix format; deconvolution is for raw fragmentation spectra linking, not peak summarization.
- Analysis goal is targeted proteomics or peptide sequencing rather than untargeted metabolomics/exposomics structure annotation.

## Inputs

- Raw mass spectrometry data files (mzML, mzXML, or netCDF format)
- IDSL.IPA-generated peaklists directory (m/z–RT chromatographic information)
- IDSL.IPA-generated peak_alignment directory (aligned peaklist data)
- IDSL.CSA parameter spreadsheet (xlsx with configured parameters for CSA, DDA, or DIA analysis type)

## Outputs

- Deconvoluted fragmentation spectra table (containing precursor m/z, retention time, and grouped fragment ion intensities)
- MSP files with composite spectra annotations
- Peaklists with adduct annotation information
- Aligned spectra table with aggregated chemical structure information (InChIKey, SMILES, molecular formula, precursor type, etc.)
- Batch-generated extracted ion chromatogram (EIC) figures for DIA and CSA analyses; batch DDA spectra figures

## How to apply

First, preprocess raw mass spectrometry data (mzML, mzXML, or netCDF) and extract chromatographic information (m/z–RT) using the IDSL.IPA workflow. Load the preprocessed data and aligned peaklists into the IDSL.CSA package. Select the appropriate analysis type (CSA, DDA, or DIA) via the parameter spreadsheet and configure method-specific parameters (39 total, distributed across 5 sections). The algorithm groups precursor ions with fragment ions by matching retention time and m/z values, then aggregates fragment ion intensities for each precursor to generate deconvoluted spectra. Run the workflow using the R command with your configured parameter spreadsheet; output includes structured fragmentation spectra tables (peaklists with adduct annotations, aligned spectra tables, and MSP files) ready for structure annotation.

## Related tools

- **IDSL.CSA** (R package that implements DDA, DIA, and CSA deconvolution algorithms to group precursor and fragment ions and generate composite fragmentation spectra) — https://github.com/idslme/IDSL.CSA
- **IDSL.IPA** (Prerequisite workflow to preprocess raw mass spectrometry data and extract m/z–RT chromatographic information for input to IDSL.CSA) — https://github.com/idslme/IDSL.IPA
- **IDSL.FSA** (Downstream integration workflow to annotate MSP files and generate fragmentation libraries from deconvoluted spectra output)
- **R** (Execution environment for the IDSL.CSA package and workflow orchestration)

## Examples

```
library(IDSL.CSA); IDSL.CSA_workflow("/path/to/CSA_parameters.xlsx")
```

## Evaluation signals

- Deconvoluted spectra output contains valid precursor m/z, retention time, and fragment ion m/z–intensity pairs for each spectrum.
- Fragment ions in each deconvoluted spectrum are correctly grouped by matching retention time windows and m/z proximity to the precursor ion.
- MSP files are generated without parsing errors and contain proper headers (precursor m/z, RT, number of fragments) and fragment ion records.
- Adduct-annotated peaklists show consistent precursor type assignments (e.g., [M+H]+, [M−H]−) with expected mass shifts relative to neutral molecular mass.
- Output aligned spectra table successfully aggregates chemical structures (InChIKey, SMILES) on the aligned peak table without duplicates for isomeric compounds.

## Limitations

- Requires prior execution of IDSL.IPA workflow; raw data without extracted m/z–RT information cannot be processed directly.
- Parameter selection requires domain knowledge; incorrect specification of analysis type (CSA vs. DDA vs. DIA) will produce misaligned deconvoluted spectra.
- Suitable for population-size untargeted studies (n > 500) as per design, but performance on smaller cohorts is not documented.
- Requires sufficient computational resources for parallel processing; no changelog available to track historical parameter behavior changes.
- DDA deconvolution assumes standard precursor–fragment ion relationship (adjacent scans); non-standard MS instrument acquisition modes may not deconvolute correctly.

## Evidence

- [other] Load the DDA raw mass spectrometry data file (mzML or mzXML format) into the IDSL.CSA R package. Apply the DDA-specific deconvolution algorithm to group precursor ions with their corresponding fragment ions based on retention time and m/z relationships.: "Load the DDA raw mass spectrometry data file (mzML or mzXML format) into the IDSL.CSA R package. Apply the DDA-specific deconvolution algorithm to group precursor ions with their corresponding"
- [readme] This package can be used for the deconvolution of fragmentation spectra obtained through various analytical methods such as MS1-only Composite Spectra deconvolution Analysis (CSA), Data Dependent Acquisition (DDA), and a various Data-Independent Acquisition (DIA) methods: "This package can be used for the deconvolution of fragmentation spectra obtained through various analytical methods such as MS1-only Composite Spectra deconvolution Analysis (CSA), Data Dependent"
- [readme] The aim of the IDSL.CSA package is to assist in streamlining the data analysis process and improving the overall chemical structure annotation in the fields of metabolomics and exposomics.: "The aim of the IDSL.CSA package is to assist in streamlining the data analysis process and improving the overall chemical structure annotation in the fields of metabolomics and exposomics."
- [readme] Prior to processing your mass spectrometry data (mzXML, mzML, netCDF) using the IDSL.CSA workflow, mass spectrometry data should be processed using the IDSL.IPA workflow to acquire chromatographic information of the peaks (m/z-RT).: "Prior to processing your mass spectrometry data (mzXML, mzML, netCDF) using the IDSL.CSA workflow, mass spectrometry data should be processed using the IDSL.IPA workflow to acquire chromatographic"
- [other] Generate deconvoluted fragmentation spectra by aggregating fragment ions associated with each precursor ion. Output the deconvoluted spectra as a structured table or composite spectrum object containing precursor m/z, retention time, and grouped fragment ion intensities.: "Generate deconvoluted fragmentation spectra by aggregating fragment ions associated with each precursor ion. Output the deconvoluted spectra as a structured table or composite spectrum object"
- [readme] Aggregating annotated chemical structures on the aligned peak table using meta-variables such as InChIKey, SMILES, precursor type, molecular formula,... depending on the information in the reference library.: "Aggregating annotated chemical structures on the aligned peak table using meta-variables such as InChIKey, SMILES, precursor type, molecular formula,... depending on the information in the reference"
