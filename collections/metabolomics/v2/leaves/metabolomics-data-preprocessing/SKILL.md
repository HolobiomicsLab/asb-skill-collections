---
name: metabolomics-data-preprocessing
description: Use when you have raw LC/HRMS data files in mzXML, mzML, or netCDF format
  and need to identify individual and aggregated aligned peaks with their retention
  time and m/z values before applying spectral deconvolution or chemical annotation.
  This is the obligatory first step when using IDSL.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0639
  tools:
  - IDSL.CSA
  - R
  - IDSL.IPA
  - Lilikoi v2.0
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.3c00376
  title: IDSL.CSA
- doi: 10.1093/gigascience/giaa162
  title: ''
evidence_spans:
- The **Composite Spectra Analysis (IDSL.CSA)** R package for the analysis of mass
  spectrometry data
- The **Composite Spectra Analysis (IDSL.CSA)** R package
- The new Lilikoi v2.0 R package has implemented a deep-learning method for classification,
  in addition to popular machine learning methods.
- Lilikoi v2.0 is a modern, comprehensive package to enable metabolomics analysis
  in R programming environment.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_asics_cq
    doi: 10.1021/acs.analchem.0c04232
    title: ASICS
  - build: coll_idsl_csa_cq
    doi: 10.1021/acs.analchem.3c00376
    title: IDSL.CSA
  - build: coll_lilikoi_v2_0_cq
    doi: 10.1093/gigascience/giaa162
    title: Lilikoi V2.0
  dedup_kept_from: coll_idsl_csa_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c00376
  all_source_dois:
  - 10.1021/acs.analchem.3c00376
  - 10.1093/gigascience/giaa162
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-data-preprocessing

## Summary

Preprocess raw mass spectrometry data (mzXML, mzML, netCDF) to extract chromatographic peak information (m/z–RT coordinates) and generate aligned peaklists and peak tables suitable for fragmentation spectra deconvolution. This step is mandatory upstream of composite spectra analysis, DDA, and DIA fragmentation workflows.

## When to use

You have raw LC/HRMS data files in mzXML, mzML, or netCDF format and need to identify individual and aggregated aligned peaks with their retention time and m/z values before applying spectral deconvolution or chemical annotation. This is the obligatory first step when using IDSL.CSA or IDSL.IPA for untargeted metabolomics studies, especially for population-scale analyses (n > 500).

## When NOT to use

- Input data are already in processed peaklist or feature table format (aligned m/z–RT–intensity); skip directly to spectral deconvolution.
- Your goal is targeted analysis of known metabolites with pre-specified transitions; use targeted extraction instead.
- Raw data are in vendor-proprietary binary formats (.raw, .d, .ms) that have not been converted to mzXML/mzML; convert first using vendor tools (e.g., ProteoWizard).

## Inputs

- Raw mass spectrometry data files (mzXML, mzML, or netCDF format)
- Instrument metadata (e.g., Thermo Q Exactive HF Orbitrap, ionization mode: HILIC-ESI-POS/NEG)

## Outputs

- peaklists directory (individual per-sample peak calls with m/z and retention time)
- peak_alignment directory (cross-sample aligned peak table with aggregated features)
- Aligned peaklist with m/z–RT coordinates and intensity values

## How to apply

Process raw mass spectrometry data using the IDSL.IPA workflow to generate chromatographic peak information (m/z–RT) and produce individual peaklists and aligned peak tables. The IDSL.IPA workflow performs peak detection and chromatogram deconvolution on MS1-level HRMS data, generating a `peaklists` directory (per-sample peak calls) and `peak_alignment` directory (cross-sample aligned features). These outputs are then used as inputs to the IDSL.CSA parameter spreadsheet (fields CSA0008 and CSA0009). Configure parallel processing threads (CSA0004) according to available computational resources. Validation occurs through inspection of aligned peak table structure and verification that m/z–RT coordinates are populated and non-redundant.

## Related tools

- **IDSL.IPA** (Upstream workflow that performs peak detection, chromatogram deconvolution, and m/z–RT extraction from raw LC/HRMS data; generates peaklists and peak_alignment directories required as inputs to IDSL.CSA) — https://github.com/idslme/IDSL.IPA
- **IDSL.CSA** (Downstream tool that accepts preprocessed peaklists and peak_alignment directories to perform fragmentation spectra deconvolution for CSA, DDA, and DIA analyses) — https://github.com/idslme/IDSL.CSA
- **R** (Runtime environment for executing IDSL.IPA workflow scripts)

## Examples

```
# Run IDSL.IPA workflow on raw LC/HRMS data to generate peaklists and peak_alignment directories
# (See IDSL.IPA quick example at https://github.com/idslme/IDSL.IPA#quick-batch-example)
# Then configure IDSL.CSA parameter spreadsheet with:
# CSA0008 = path/to/peaklists
# CSA0009 = path/to/peak_alignment
# CSA0011 = output_directory
```

## Evaluation signals

- peaklists directory contains one file per sample with columns for m/z, retention time, and intensity; no null or duplicate m/z–RT pairs within a sample.
- peak_alignment directory contains an aligned feature table with consistent m/z and retention time values across samples, with appropriate missing-value handling (NAs for undetected features).
- Aligned peaklist row count is substantially fewer than the sum of individual peaklist rows, indicating successful aggregation across samples; feature count scales appropriately with sample complexity and instrumental resolution.
- Retention time values are monotonically increasing and fall within the expected chromatographic window (e.g., 0–20 min for typical LC methods); m/z values are positive and fall within instrument range (e.g., 50–1200 for Orbitrap).
- Intensity values are non-negative and have been normalized or log-transformed if required by downstream analysis (verified in parameter settings CSA0008/CSA0009).

## Limitations

- Requires upstream conversion of raw vendor formats (.raw, .d) to open formats (mzXML, mzML); this step may introduce minor m/z or intensity artifacts depending on converter fidelity.
- Peak detection and deconvolution quality depend on instrument resolution, ionization efficiency, and chromatographic separation; poor separation or low-abundance features may be missed or split across multiple aligned features.
- Untargeted studies with n > 500 samples require substantial computational resources and parallel processing; wall-clock time scales with sample count and data complexity.
- The preprocessing workflow does not automatically handle instrumental drift, batch effects, or systematic RT shifts across acquisition batches; these may require post-hoc alignment or normalization in downstream analysis.

## Evidence

- [readme] Prior to processing your mass spectrometry data (mzXML, mzML, netCDF) using the IDSL.CSA workflow, mass spectrometry data should be processed using the IDSL.IPA workflow to acquire chromatographic information of the peaks (m/z-RT).: "Prior to processing your mass spectrometry data (**mzXML**, **mzML**, **netCDF**) using the IDSL.CSA workflow, mass spectrometry data should be processed using the"
- [readme] When the chromatographic information of individual and aggregated aligned peaklists were generated using the IDSL.IPA workflow, download the IDSL.CSA parameter spreadsheet and select the parameters accordingly and then use this spreadsheet as the input for the IDSL.CSA workflow: "When the chromatographic information of individual and aggregated aligned peaklists were generated using the [IDSL.IPA](https://github.com/idslme/IDSL.IPA) workflow, download the [IDSL.CSA parameter"
- [readme] Analyzing population size untargeted studies (n > 500): "Analyzing population size untargeted studies (n > 500)"
- [readme] Process raw mass spectrometry data and chromatographic information using the method described for IDSL.IPA: "Process raw mass spectrometry data and chromatographic information using the method described for [IDSL.IPA](https://github.com/idslme/IDSL.IPA#quick-batch-example)"
- [readme] You may increase the number of processing threads using CSA0004 according to your computational power: "You may also increase the number of processing threads using **CSA0004** according to your computational power"
