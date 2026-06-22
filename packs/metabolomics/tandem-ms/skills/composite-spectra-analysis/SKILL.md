---
name: composite-spectra-analysis
description: Use when your untargeted LC/HRMS dataset contains Data-Independent Acquisition data (MS^E, AIF, or SWATH-MS) or MS1-only composite spectra where multiple precursor ions fragment simultaneously, and you need to deconvolve overlapping fragmentation spectra to enable accurate chemical structure.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3391
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

# composite-spectra-analysis

## Summary

Deconvolve fragmentation spectra from Data-Independent Acquisition (DIA) mass spectrometry methods (MS^E, AIF, SWATH-MS) and Composite Spectra Analysis (CSA) to extract individual ion signatures for chemical annotation. This skill resolves composite/multiplexed spectra into interpretable fragmentation patterns aligned with precursor m/z and retention time coordinates.

## When to use

Your untargeted LC/HRMS dataset contains Data-Independent Acquisition data (MS^E, AIF, or SWATH-MS) or MS1-only composite spectra where multiple precursor ions fragment simultaneously, and you need to deconvolve overlapping fragmentation spectra to enable accurate chemical structure annotation. Apply this skill after chromatographic peak detection and alignment (via IDSL.IPA) have established m/z–RT coordinates.

## When NOT to use

- Input data is already a feature table or aggregated intensity matrix without access to raw MS spectra — this skill requires raw spectral data (mzXML/mzML/netCDF).
- Your mass spectrometry data was acquired in Data Dependent Acquisition (DDA) mode with clear 1:1 precursor-to-fragment relationships — DDA typically requires the DDA-specific IDSL.CSA workflow branch, not DIA/CSA deconvolution.
- Chromatographic peak detection and m/z–RT alignment have not yet been performed — IDSL.CSA requires preprocessed alignment information from IDSL.IPA as input.

## Inputs

- DIA/CSA raw mass spectrometry data files (mzXML, mzML, or netCDF format)
- IDSL.IPA-generated peaklists directory (m/z–RT coordinates)
- IDSL.IPA-generated peak_alignment directory (aligned feature table)
- IDSL.CSA parameter spreadsheet (user-configured parameters)

## Outputs

- Deconvoluted fragmentation spectra (.msp files with fragmentation records)
- Aligned peak table with chemical structure annotation (CSV/tabular format)
- Adduct annotation peaklists
- Peak alignment subsets for major ions in each CSA cluster
- Aligned spectra table with aggregation metadata (InChIKey, SMILES, precursor type)
- Batch extracted ion chromatogram (EIC) figures for DIA and CSA analyses

## How to apply

Load preprocessed DIA or CSA raw data (mzXML, mzML, or netCDF format) and aligned peaklist coordinates from IDSL.IPA into the IDSL.CSA R package environment. Select the appropriate analytical method (CSA, DDA, or DIA variant) via the parameter spreadsheet (39 parameters across 5 sections). Execute the deconvolution algorithm, which applies peak detection and chromatogram deconvolution to extract individual fragmentation spectra from composite spectra. The algorithm leverages the known m/z–RT alignment information to resolve spectral overlap. Export deconvoluted spectra to MSP format and aligned peak tables with chemical structure aggregation (grouped by InChIKey, SMILES, molecular formula, or precursor type). Validate output by inspecting extracted ion chromatograms (EICs) and verifying that fragmentation patterns match expected adduct and neutral loss signatures.

## Related tools

- **IDSL.CSA** (Core R package that implements DIA/CSA deconvolution algorithm, peak detection, chromatogram deconvolution, and spectral aggregation for fragmentation spectra) — https://github.com/idslme/IDSL.CSA
- **IDSL.IPA** (Prerequisite workflow that generates m/z–RT peaklists and aligned peak tables required as input to IDSL.CSA deconvolution) — https://github.com/idslme/IDSL.IPA
- **IDSL.FSA** (Downstream integration tool for annotating MSP files and generating fragmentation libraries from IDSL.CSA deconvoluted spectra)
- **R** (Programming environment for executing IDSL.CSA workflow)

## Examples

```
library(IDSL.CSA)
IDSL.CSA_workflow("Address of the CSA parameter spreadsheet")
```

## Evaluation signals

- Deconvoluted MSP spectra contain fragment ions with non-zero abundances matching expected loss patterns (e.g., neutral loss of H₂O, CO₂) for the inferred chemical class.
- Aligned peak table aggregation successfully groups precursor ions by InChIKey or SMILES with consistent retention time and similar m/z (within instrument mass accuracy tolerance), indicating correct spectral separation.
- Extracted ion chromatograms (EICs) generated for major ions in each cluster show distinct peaks without unresolved overlaps, confirming deconvolution efficacy.
- Adduct annotation peaklists correctly identify [M+H]⁺, [M+Na]⁺, [M−H]⁻, or other expected adducts consistent with ionization mode and mass shift (within 5 ppm).
- Output MSP file validates against standard MSP schema (precursor m/z, retention time, fragment m/z–intensity pairs, metadata fields).

## Limitations

- Deconvolution accuracy depends critically on quality of input m/z–RT alignment from IDSL.IPA; poor peak detection upstream will propagate errors to CSA output.
- For highly complex samples (n > 500 population-scale studies), computational time increases substantially; parallel processing in Windows/Linux environments is supported but requires sufficient memory.
- Overlapping peaks with similar m/z and retention time may not be fully resolved; the deconvolution algorithm relies on chromatographic separation and cannot recover spectra below the instrument's mass and temporal resolution.
- No changelog provided in repository documentation; version compatibility and backward compatibility with older mzML/mzXML formats not explicitly documented.

## Evidence

- [intro] DIA deconvolution capability: "This package can be used for the deconvolution of fragmentation spectra obtained through various analytical methods such as MS1-only Composite Spectra deconvolution Analysis (CSA), Data Dependent"
- [readme] Workflow with m/z–RT input requirement: "Prior to processing your mass spectrometry data (mzXML, mzML, netCDF) using the IDSL.CSA workflow, mass spectrometry data should be processed using the IDSL.IPA workflow to acquire chromatographic"
- [readme] Output formats and aggregation: "Aggregating annotated chemical structures on the aligned peak table using meta-variables such as InChIKey, SMILES, precursor type, molecular formula,... depending on the information in the reference"
- [readme] Parameter-driven execution: "The Composite Spectra Analysis requires 39 parameters distributed into 5 separate sections for a full scale analysis."
- [readme] Batch figure generation: "Generating batch untargeted aligned extracted ion chromatograms (EIC) figures for the DIA and CSA analyses in addition to generating batch DDA spectra figures."
