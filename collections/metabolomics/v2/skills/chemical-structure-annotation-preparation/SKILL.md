---
name: chemical-structure-annotation-preparation
description: Use when you have acquired composite fragmentation spectra from DIA experiments (MS^E, AIF, or SWATH-MS) that have been deconvoluted by IDSL.CSA, and you need to export the resolved spectra in a format suitable for chemical structure identification against reference libraries or spectral databases.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - IDSL.CSA
  - R
  - IDSL.FSA
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

# chemical-structure-annotation-preparation

## Summary

Prepare deconvoluted fragmentation spectra from Data-Independent Acquisition (DIA) methods for downstream chemical structure annotation by extracting and exporting individual MS/MS spectra into standardized formats. This skill bridges spectral deconvolution and structure database matching workflows.

## When to use

You have acquired composite fragmentation spectra from DIA experiments (MS^E, AIF, or SWATH-MS) that have been deconvoluted by IDSL.CSA, and you need to export the resolved spectra in a format suitable for chemical structure identification against reference libraries or spectral databases.

## When NOT to use

- Input spectra are from Data Dependent Acquisition (DDA) experiments—use DDA-specific annotation pathways instead
- Fragmentation spectra have not yet been deconvoluted—run IDSL.CSA deconvolution first
- You require only MS1 precursor ion peaks without fragmentation patterns—CSA is designed for composite spectra analysis and fragmentation

## Inputs

- DIA raw data file (MSE, AIF, or SWATH-MS format; e.g., mzXML, mzML, or netCDF)
- Deconvoluted fragmentation spectra table (output from IDSL.CSA DIA deconvolution module)

## Outputs

- Deconvoluted fragmentation spectra in mzML format
- Deconvoluted fragmentation spectra in mzXML format
- Deconvoluted fragmentation spectra in CSV table format
- Structured MSP file (for integration with IDSL.FSA annotation workflow)

## How to apply

After executing the DIA deconvolution algorithm within IDSL.CSA (step 3 of the DIA workflow), export the deconvoluted fragmentation spectra to a structured output format—mzML, mzXML, or CSV table—depending on your downstream annotation tool's input requirements. The export step preserves both precursor m/z and fragmentation patterns resolved by the deconvolution process, enabling accurate matching against reference spectra. Select the output format that your chemical annotation pipeline (e.g., spectral library matching, in silico fragmentation prediction) expects. Verify that exported spectra retain both MS1 precursor information and resolved MS/MS fragment peaks with intensity values.

## Related tools

- **IDSL.CSA** (Performs DIA deconvolution and generates the fragmentation spectra tables that are exported in this skill) — https://github.com/idslme/IDSL.CSA
- **IDSL.FSA** (Downstream tool for annotating MSP files and generating fragmentation libraries from deconvoluted spectra) — https://github.com/idslme/IDSL.FSA
- **IDSL.IPA** (Prerequisite workflow that generates chromatographic peak information (m/z-RT) required before IDSL.CSA processing) — https://github.com/idslme/IDSL.IPA
- **R** (Programming environment in which IDSL.CSA workflow is executed)

## Examples

```
library(IDSL.CSA); IDSL.CSA_workflow("path/to/CSA_parameters.xlsx")
```

## Evaluation signals

- Exported spectra retain both precursor m/z and resolved fragment m/z values with non-zero intensities
- Output file schema conforms to selected format specification (mzML/mzXML XML structure or CSV column headers)
- Fragmentation patterns differ between spectra exported from the same composite precursor—confirming successful deconvolution
- Exported spectra can be successfully parsed by downstream annotation tools (e.g., spectral library search engines, IDSL.FSA)
- Number of exported spectra matches or exceeds the number of resolved components from IDSL.CSA deconvolution step

## Limitations

- IDSL.CSA deconvolution quality depends on appropriate parameter selection in the CSA parameter spreadsheet; poorly tuned parameters may yield incomplete or incorrect fragmentation pattern separation
- DIA methods inherently produce composite spectra with overlapping fragments; deconvolution assumes sufficient chromatographic separation and m/z resolution to resolve individual components
- CSV table export may lose hierarchical MS/MS scan metadata preserved in mzML/mzXML formats; choose export format based on downstream annotation tool requirements
- Requires prior execution of IDSL.IPA workflow to generate the m/z-RT chromatographic information needed by IDSL.CSA

## Evidence

- [other] Export the deconvoluted fragmentation spectra to a structured output format (mzML, mzXML, or CSV table) for downstream annotation and chemical structure identification.: "Export the deconvoluted fragmentation spectra to a structured output format (mzML, mzXML, or CSV table) for downstream annotation and chemical structure identification."
- [readme] This package can be used for the deconvolution of fragmentation spectra obtained through various analytical methods such as MS1-only Composite Spectra deconvolution Analysis (CSA), Data Dependent Acquisition (DDA), and various Data-Independent Acquisition (DIA) methods: "This package can be used for the deconvolution of fragmentation spectra obtained through various analytical methods such as MS1-only Composite Spectra deconvolution Analysis (CSA), Data Dependent"
- [readme] The aim of the IDSL.CSA package is to assist in streamlining the data analysis process and improving the overall chemical structure annotation in the fields of metabolomics and exposomics.: "The aim of the IDSL.CSA package is to assist in streamlining the data analysis process and improving the overall chemical structure annotation in the fields of metabolomics and exposomics."
- [readme] Integration with IDSL.FSA workflow to annotate various types of MSP files and generating fragmentation libraries.: "Integration with IDSL.FSA workflow to annotate various types of MSP files and generating fragmentation libraries."
