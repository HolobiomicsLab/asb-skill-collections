---
name: per-root-metabolite-profiling
description: Use when when you have deposited mass spectrometry imaging datasets for plant roots in CDF format paired with pre-computed Matlab workspaces, and you need to reproduce per-root linear-axis metabolite profiling outputs to validate reported genotype-level results (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3431
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - DIMPLE (Developmental Imaging Mass Spectrometry Pipeline for Linear Evaluation)
  - Matlab
  - batchcdfread
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# per-root-metabolite-profiling

## Summary

A workflow for reproducing linear-axis mass spectrometry imaging analysis on individual root samples using the DIMPLE computational pipeline, which processes NetCDF (CDF) files and associated Matlab workspaces to quantify metabolite distributions along the root axis.

## When to use

When you have deposited mass spectrometry imaging datasets for plant roots in CDF format paired with pre-computed Matlab workspaces, and you need to reproduce per-root linear-axis metabolite profiling outputs to validate reported genotype-level results (e.g., comparing B73 vs. Oaxacan Green root phenotypes).

## When NOT to use

- CDF imaging file lacks an associated Matlab workspace or calibration metadata — the pipeline requires pre-computed workspace parameters to align imaging dimensions to root anatomy.
- Root imaging data is from a different instrument vendor or uses a non-standard CDF encoding — DIMPLE is tailored to the specific CDF structure and workspace format used in Sama et al. 2025.
- Per-root output is already a feature table or summary statistic — this skill is for reproducing raw per-root profiles, not for aggregating or filtering existing summary metrics.

## Inputs

- CDF (NetCDF) mass spectrometry imaging file for a single root (e.g., OG1, OG5, OG2-P11-0)
- Associated Matlab workspace file (e.g., OG1-workspace-2.mat, OG5-workspace.mat)
- DIMPLE pipeline codebase (Matlab scripts)

## Outputs

- Per-root linear-axis metabolite intensity or abundance profile (e.g., metabolite signal as a function of axial position)
- Aggregated per-root metrics matching the genotype-level findings reported in Sama et al. 2025

## How to apply

Load the CDF root imaging data file and its corresponding Matlab workspace (.mat) into the DIMPLE pipeline environment. Execute the DIMPLE linear-axis analysis workflow on each root dataset sequentially to compute per-root mass spectrometry imaging metrics along the linear axis (e.g., metabolite intensity or abundance by axial position). Aggregate the three per-root outputs and validate that the computed metrics match the reported genotype-level results. The key rationale is that the workspace files contain pre-processed imaging metadata and calibration parameters necessary to correctly parse and align the CDF imaging dimensions to the root's biological axis.

## Related tools

- **DIMPLE (Developmental Imaging Mass Spectrometry Pipeline for Linear Evaluation)** (Primary computational pipeline for loading CDF imaging files, applying linear-axis analysis, and computing per-root metabolite profiles from mass spectrometry imaging data.) — https://github.com/dickinsonlab/DIMPLE-code
- **Matlab** (Execution environment for DIMPLE pipeline scripts; required to load CDF files via batchcdfread function and process Matlab workspace data.)
- **batchcdfread** (Matlab function (developed by Yifan Meng in Dr. Richard N. Zare's lab at Stanford) for reading and parsing CDF imaging files into Matlab array structures compatible with DIMPLE linear-axis analysis.)

## Evaluation signals

- Per-root metabolite intensity profiles are successfully computed for all three root datasets (OG1, OG5, OG2-P11-0) without CDF parsing errors or workspace loading failures.
- Aggregated per-root outputs for the Oaxacan Green genotype match the reported linear-axis metabolite distributions in Sama et al. 2025 (within measurement uncertainty or reported precision).
- Linear-axis alignment is correct: metabolite signal varies smoothly along the root axis (root apex to mature zone) without discontinuities or spatial inversions.
- Workspace-derived parameters (e.g., image registration offsets, mass calibration coefficients) are correctly applied during CDF import; verify by checking that computed m/z values align with expected metabolite masses.
- All three per-root datasets execute without requiring manual parameter tuning or re-annotation of workspace files, confirming reproducibility of the deposited workflow.

## Limitations

- DIMPLE is optimized for linear-axis root imaging; it may not be suitable for 2D spatial metabolomics analysis or non-linear root geometries without workflow modification.
- The pipeline depends critically on the pre-computed Matlab workspace files; loss or corruption of these files (especially OG1-workspace-2.mat, OG5-workspace.mat) will prevent successful reproduction.
- The README notes missing workspace information for OG2-P11-0 in the current documentation, potentially creating ambiguity about whether a workspace file exists or different processing steps are required.
- CDF file format and Matlab workspace structure are specific to the Sama et al. 2025 study; root imaging data from other labs or instruments may require adaptation of the batchcdfread function or workspace generation protocol.

## Evidence

- [other] Three Oaxacan Green root datasets are available for analysis: OG1 with OG1-workspace-2.mat, OG5 with OG5-workspace.mat, and OG2-P11-0, providing the cdf files and Matlab workspaces necessary to reproduce the linear-axis imaging mass spectrometry analysis.: "Three Oaxacan Green root datasets are available for analysis: OG1 with OG1-workspace-2.mat, OG5 with OG5-workspace.mat, and OG2-P11-0, providing the cdf files and Matlab workspaces necessary to"
- [readme] Computational pipeline for analyzing mass spectrometry imaginging data along a linear axis. Developmental Imaging Mass Spectrometry Pipeline for Linear Evaluation (DIMPLE) was first employed as described in Sama et al. 2025.: "Computational pipeline for analyzing mass spectrometry imaginging data along a linear axis. Developmental Imaging Mass Spectrometry Pipeline for Linear Evaluation (DIMPLE) was first employed as"
- [readme] cdf files and available Matlab workspaces are provided for the roots that were analyzed in Sama et al. 2025.: "cdf files and available Matlab workspaces are provided for the roots that were analyzed in Sama et al. 2025."
- [readme] batchcdfread function developed by Yifan Meng in Dr. Richard N. Zare's lab at Stanford University: "batchcdfread function developed by Yifan Meng in Dr. Richard N. Zare's lab at Stanford University"
- [other] Execute the DIMPLE linear-axis analysis workflow on each root dataset to compute per-root mass spectrometry imaging metrics along the linear axis.: "Execute the DIMPLE linear-axis analysis workflow on each root dataset to compute per-root mass spectrometry imaging metrics along the linear axis."
