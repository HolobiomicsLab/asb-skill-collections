---
name: peak-table-compilation
description: Use when after peak detection has been applied to untargeted or targeted mass spectrometry data and peaks have been matched against metabolite databases and reference spectra.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0092
  tools:
  - R
  - R GUI
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1021/acs.analchem.5c03225
  title: SMART 2.0
evidence_spans:
- SMART written in R and R GUI has been developed as user-friendly software
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_smart_2_0_cq
    doi: 10.1021/acs.analchem.5c03225
    title: SMART 2.0
  dedup_kept_from: coll_smart_2_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c03225
  all_source_dois:
  - 10.1021/acs.analchem.5c03225
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-table-compilation

## Summary

Compile detected and annotated peaks from mass spectrometry data into a structured peak table containing identifiers, mass-to-charge ratios, retention times, intensities, and metabolite annotations. This is the final step in SMART's peak analysis workflow that organizes results for downstream statistical and biological interpretation.

## When to use

After peak detection has been applied to untargeted or targeted mass spectrometry data and peaks have been matched against metabolite databases and reference spectra. Use this skill when you have a collection of detected peaks with assigned annotations and need to consolidate them into a single tabular format for quality control, statistical analysis, or post-analysis operations like peak identification and concentration calibration.

## When NOT to use

- Input is already a pre-compiled peak table or feature matrix (skip compilation and proceed to quality control or statistical analysis).
- Peak detection or annotation has not yet been completed (perform peak analysis and annotation first).
- Data is in an unsupported mass spectrometry format that cannot be processed by SMART's data import module (.raw, .d, mzXML formats are required).

## Inputs

- detected peaks from untargeted peak detection algorithm (m/z and retention time features with intensities)
- detected peaks from targeted peak analysis (known compound matches with intensities)
- peak annotations from metabolite database matching and reference spectra comparison

## Outputs

- peak table: tabular format with columns for peak identifier, m/z, retention time, intensity, and assigned annotation
- structured feature matrix suitable for downstream quality control and statistical analysis

## How to apply

Following peak detection (which identifies significant m/z and retention time features) and peak annotation (which matches detected peaks against metabolite databases), aggregate all detected peaks into a structured table. Each row represents a unique peak, with columns for peak identifier, m/z value, retention time, peak intensity, and assigned metabolite annotation. The compilation step ensures consistency of peak identifiers and annotation metadata across all samples, enabling downstream operations in SMART's quality control, statistical analysis, and post-analysis modules. Rationale: standardized peak tables facilitate batch effect analysis, multivariate statistical tests (ANCOVA, PLS-DA), and integrative pathway analysis by providing a uniform feature matrix.

## Related tools

- **R** (programming environment for implementing peak table compilation logic and data manipulation) — github.com/YuJenL/SMART
- **R GUI** (user-friendly interface to SMART for executing peak table compilation without direct R coding) — github.com/YuJenL/SMART

## Evaluation signals

- Peak table contains no missing values in required columns (peak identifier, m/z, retention time, intensity, annotation).
- All detected peaks from the analysis are present in the compiled table; row count matches total peaks output by detection and annotation modules.
- m/z values are numeric and within expected instrument mass range; retention time values are positive and in monotonic order within each chromatogram.
- Peak intensity values are positive numbers with no negative or zero entries (indicating successful quantification).
- Metabolite annotations are populated for all peaks; peaks without database match are explicitly marked (e.g., 'unknown') rather than left blank.
- Peak table structure is compatible with downstream SMART modules (Quality Control, Statistical Analysis, Post-analysis) as evidenced by successful import into subsequent workflow steps.

## Limitations

- Peak table compilation depends on the accuracy of prior peak detection and annotation steps; errors in peak calling or database matching will propagate into the table.
- Annotation coverage is limited by the scope of metabolite databases and reference spectral libraries used; novel or low-abundance metabolites may remain unannotated.
- Peak intensity values reflect raw detector response without normalization or standardization; data preprocessing (transformation, standardization) must be applied in subsequent SMART modules before statistical analysis.
- No changelog is available in the SMART repository to document changes in peak table structure across software versions, which may affect reproducibility or compatibility with external tools.

## Evidence

- [other] peak table containing peak identifiers, m/z, retention time, intensity, and assigned annotations: "Compile results into a peak table containing peak identifiers, m/z, retention time, intensity, and assigned annotations."
- [readme] peak analysis for both untargeted and targeted data with annotation: "Peak Analysis and annotation: Implement peak analysis for both untargeted and targeted data and peak annotation."
- [readme] complete analysis flow includes peak analysis as a module: "SMART streamlines the complete analysis flow from initial data preprocessing to advanced downstream data analysis, consisting of the following eight modules."
- [other] peak detection and annotation precede downstream quality control and statistical analysis: "Apply peak detection algorithm for untargeted data to identify significant m/z and retention time features. ... Annotate detected peaks by matching against metabolite databases and reference spectra."
