---
name: fragmentation-spectrum-extraction
description: Use when you have raw or peak-detected mass spectrometry data (mzXML, mzML, or netCDF format) from untargeted metabolomics or exposomics studies and need to separate composite fragmentation spectra into individual constituent spectra for annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - IDSL.CSA
  - R
  - IDSL.IPA
  - IDSL.FSA
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

# fragmentation-spectrum-extraction

## Summary

Extract and deconvolve individual fragmentation spectra from composite mass spectrometry data acquired via MS1-only CSA, DDA, or DIA methods (MS^E, AIF, SWATH-MS). This skill is essential for resolving co-eluting ions and preparing spectra for downstream chemical structure annotation in metabolomics and exposomics.

## When to use

Apply this skill when you have raw or peak-detected mass spectrometry data (mzXML, mzML, or netCDF format) from untargeted metabolomics or exposomics studies and need to separate composite fragmentation spectra into individual constituent spectra for annotation. Specifically use it when: (1) MS1 precursor m/z and retention time information is available from preprocessing (IDSL.IPA); (2) your acquisition method is MS1-only CSA, DDA, or a DIA variant (MS^E, AIF, or SWATH-MS); and (3) you aim to improve chemical structure annotation by disambiguating overlapping fragmentation patterns.

## When NOT to use

- Input mass spectrometry data has not been preprocessed with IDSL.IPA to generate chromatographic m/z-RT information — run IDSL.IPA first.
- Your acquisition method is not CSA, DDA, or one of the supported DIA variants (MS^E, AIF, SWATH-MS) — IDSL.CSA does not handle other fragmentation acquisition types.
- Fragmentation spectra have already been extracted and annotated by another tool — this skill is redundant if spectra are already deconvolved and assigned to individual compounds.

## Inputs

- Raw mass spectrometry data files (mzXML, mzML, netCDF format)
- Peaklists directory (output from IDSL.IPA preprocessing)
- Peak alignment directory (output from IDSL.IPA preprocessing)
- IDSL.CSA parameter spreadsheet (39 parameters across 5 sections)
- Precursor m/z and retention time coordinates

## Outputs

- Deconvoluted fragmentation spectra (mzML, mzXML, or CSV format)
- MSP files with chemical structure annotations
- Adduct-annotated peaklists
- Peak alignment subsets for major ions in each cluster
- Aligned spectra table with aggregated chemical structure metadata
- Batch extracted ion chromatogram (EIC) figures for DIA and CSA analyses

## How to apply

Load preprocessed mass spectrometry data (mzXML, mzML, or netCDF) and aligned peak tables with m/z and retention time coordinates into the IDSL.CSA R package environment. Select the appropriate analytical method module (CSA, DDA, or DIA with its variant: MS^E, AIF, or SWATH-MS) via the IDSL.CSA parameter spreadsheet. Configure 39 parameters across 5 sections, specifying input data location (HRMS MS1 level data), peaklists directory (from IDSL.IPA), peak alignment directory, and output location. Execute the deconvolution algorithm, which performs peak detection, chromatogram deconvolution, and spectral decomposition. Export deconvoluted fragmentation spectra to structured formats (mzML, mzXML, or CSV tables). Aggregate annotated chemical structures on the aligned peak table using meta-variables (InChIKey, SMILES, molecular formula) to produce final MSP files and aligned spectra tables.

## Related tools

- **IDSL.CSA** (Core R package for composite spectra deconvolution and fragmentation spectrum extraction via CSA, DDA, and DIA (MS^E, AIF, SWATH-MS) modules) — https://github.com/idslme/IDSL.CSA
- **IDSL.IPA** (Prerequisite preprocessing workflow to acquire chromatographic m/z-RT information from raw mass spectrometry data before IDSL.CSA fragmentation extraction) — https://github.com/idslme/IDSL.IPA
- **IDSL.FSA** (Downstream annotation workflow integrated with IDSL.CSA to annotate MSP files and generate fragmentation libraries from extracted spectra) — https://github.com/idslme/IDSL.FSA
- **R** (Programming environment in which IDSL.CSA is executed)

## Examples

```
library(IDSL.CSA); IDSL.CSA_workflow("/path/to/CSA_parameters.xlsx")
```

## Evaluation signals

- Deconvoluted spectra are exported in valid structured formats (mzML, mzXML, or CSV) and are parseable by downstream annotation tools or visualization software.
- MSP files contain matched precursor m/z, retention time, and fragmentation peaks that correspond to input peaklist coordinates within expected mass accuracy (typically ≤5 ppm for high-resolution instruments).
- Aligned peak tables show aggregated chemical structure metadata (InChIKey, SMILES, molecular formula) consistent with reference library entries, indicating successful spectrum-to-compound mapping.
- Peak alignment subsets for major ions in each CSA cluster show non-overlapping m/z ranges and separated retention times, confirming deconvolution separated co-eluting ions.
- Batch EIC figures visualize extracted ion traces at expected retention times and show resolved peak shapes, suggesting successful separation of composite spectra into individual fragmentation patterns.

## Limitations

- Requires prior preprocessing with IDSL.IPA to generate peaklist and peak alignment directories; raw data alone is insufficient input.
- Parameter selection is critical and requires domain knowledge; 39 parameters across 5 sections must be configured correctly for the specific acquisition method and study design.
- Suitable for untargeted population studies with n > 500 samples; computational scaling may be limited for smaller or very large cohorts depending on parallelization and system resources.
- No changelog is publicly documented, which may affect reproducibility across software versions.
- Deconvolution quality depends on peak detection accuracy from IDSL.IPA; poor chromatographic preprocessing will propagate into the fragmentation extraction step.

## Evidence

- [readme] MS1-only CSA, DDA, and DIA deconvolution support: "This package can be used for the deconvolution of fragmentation spectra obtained through various analytical methods such as MS1-only Composite Spectra deconvolution Analysis (CSA), Data Dependent"
- [readme] DIA method variants supported: "Data-Independent Acquisition (DIA) methods including MS^E, All-Ion Fragmentation (AIF), and SWATH-MS analyses"
- [readme] Input data formats required: "Prior to processing your mass spectrometry data (mzXML, mzML, netCDF) using the IDSL.CSA workflow, mass spectrometry data should be processed using the IDSL.IPA workflow"
- [readme] Output format and structure: "Export the deconvoluted fragmentation spectra to a structured output format (mzML, mzXML, or CSV table) for downstream annotation"
- [readme] Aggregation and meta-variable support: "Aggregating annotated chemical structures on the aligned peak table using meta-variables such as InChIKey, SMILES, precursor type, molecular formula"
- [readme] Purpose and application domain: "The aim of the IDSL.CSA package is to assist in streamlining the data analysis process and improving the overall chemical structure annotation in the fields of metabolomics and exposomics"
- [readme] Parameter configuration requirement: "The Composite Spectra Analysis requires 39 parameters distributed into 5 separate sections for a full scale analysis"
