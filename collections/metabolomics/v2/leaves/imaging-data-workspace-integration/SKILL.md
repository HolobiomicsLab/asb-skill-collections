---
name: imaging-data-workspace-integration
description: Use when you have paired cdf files (raw mass spectrometry imaging data)
  and Matlab workspace (.mat) files for the same root sample, and you need to reproduce
  published linear-axis imaging analysis results (e.g., per-root mass spectrometry
  imaging metrics along a developmental or spatial axis).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3050
  - http://edamontology.org/topic_0092
  tools:
  - DIMPLE (Developmental Imaging Mass Spectrometry Pipeline for Linear Evaluation)
  - Matlab
  - batchcdfread function
  techniques:
  - MS-imaging
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1101/2025.09.22.677919v1
  title: DIMPLE
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dimple_cq
    doi: 10.1101/2025.09.22.677919v1
    title: DIMPLE
  dedup_kept_from: coll_dimple_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.09.22.677919v1
  all_source_dois:
  - 10.1101/2025.09.22.677919v1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# imaging-data-workspace-integration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Load and integrate mass spectrometry imaging (MSI) data from NetCDF files with their corresponding Matlab workspaces to enable reproducible linear-axis analysis in the DIMPLE computational pipeline. This skill bridges raw instrument output (cdf) with pre-computed analysis metadata (Matlab workspace variables) to ensure consistent per-root metric computation.

## When to use

You have paired cdf files (raw mass spectrometry imaging data) and Matlab workspace (.mat) files for the same root sample, and you need to reproduce published linear-axis imaging analysis results (e.g., per-root mass spectrometry imaging metrics along a developmental or spatial axis). Typical trigger: repository provides both data types and a published result to validate against.

## When NOT to use

- Input cdf and workspace files are from different root samples or genotypes — integration will produce misaligned axis mappings and invalid metrics.
- Workspace file is missing or corrupted — you cannot restore the analysis configuration; reload from raw parameters or skip workspace integration.
- Raw imaging data is already pre-processed into a feature table or summary matrix — use direct metric computation instead of re-integrating raw cdf data.

## Inputs

- NetCDF (cdf) file containing raw mass spectrometry imaging pixel data (m/z values and intensities)
- Matlab workspace (.mat) file containing pre-computed axis definitions, masks, calibration metadata, or prior analysis parameters for the same root
- DIMPLE pipeline codebase (Matlab functions and scripts)

## Outputs

- Integrated Matlab workspace with raw imaging data and metadata unified in memory
- Per-root linear-axis mass spectrometry imaging metrics (composition, intensity, or metabolite abundance along the root axis)
- Validation report confirming outputs match published genotype-specific results

## How to apply

Access and download the paired cdf and Matlab workspace files from the DIMPLE repository for your target root dataset (e.g., OG1 cdf + OG1-workspace-2.mat). Load both into Matlab using the DIMPLE pipeline environment: read the cdf file (likely using the batchcdfread function) to obtain raw m/z and intensity matrices, then load the workspace file to restore pre-computed axis definitions, ROI masks, or calibration parameters. Execute the DIMPLE linear-axis analysis workflow on the integrated data to compute per-root metrics. Validate outputs by comparing computed values against published results for that genotype and root ID; mismatches indicate either incomplete data integration or pipeline configuration drift.

## Related tools

- **DIMPLE (Developmental Imaging Mass Spectrometry Pipeline for Linear Evaluation)** (Orchestrates cdf file loading, workspace integration, and per-root linear-axis analysis workflow) — https://github.com/dickinsonlab/DIMPLE-code
- **Matlab** (Runtime environment for loading cdf files via batchcdfread and executing workspace-integrated analysis functions)
- **batchcdfread function** (Reads NetCDF (cdf) files to extract raw m/z and intensity matrices for imaging data)

## Evaluation signals

- Both cdf and workspace files load without errors; Matlab session contains expected variables (raw imaging matrix, axis vectors, ROI masks).
- Per-root metric outputs (intensity profiles, composition along axis) are numerically identical or within expected floating-point tolerance to published Sama et al. 2025 results for the matching genotype and root ID.
- Root ID, genotype, and axis definition from workspace metadata match the cdf file provenance and article supplementary documentation.
- No NaN or inf values appear in per-root metrics; pixel counts and axis lengths are consistent between cdf dimensions and workspace definitions.
- Aggregated outputs from all three Oaxacan Green roots (OG1, OG5, OG2-P11-0) can be compared side-by-side without schema or dimension mismatches.

## Limitations

- Workspace file structure and variable names are pipeline-specific; incorrect or outdated workspace files will silently produce misaligned analysis.
- No built-in version control for workspace metadata; if workspace was created with a different DIMPLE version, results may diverge from published outputs.
- README does not document workspace variable schema or provide checksums; manual inspection of loaded data is required to confirm integrity.
- Third Oaxacan Green root (OG2-P11-0) workspace file not explicitly mentioned in README — may not be available or may require separate acquisition.

## Evidence

- [readme] cdf files and available Matlab workspaces are provided for the roots that were analyzed in Sama et al. 2025.: "cdf files and available Matlab workspaces are provided for the roots that were analyzed in Sama et al. 2025."
- [other] Load the cdf files and workspace data into Matlab using the DIMPLE pipeline environment.: "Load the cdf files and workspace data into Matlab using the DIMPLE pipeline environment."
- [other] Execute the DIMPLE linear-axis analysis workflow on each root dataset to compute per-root mass spectrometry imaging metrics along the linear axis.: "Execute the DIMPLE linear-axis analysis workflow on each root dataset to compute per-root mass spectrometry imaging metrics along the linear axis."
- [other] Aggregate and validate the three per-root outputs to confirm they match the reported Oaxacan Green genotype results.: "Aggregate and validate the three per-root outputs to confirm they match the reported Oaxacan Green genotype results."
- [readme] batchcdfread function developed by Yifan Meng in Dr. Richard N. Zare's lab at Stanford University: "batchcdfread function developed by Yifan Meng in Dr. Richard N. Zare's lab at Stanford University"
