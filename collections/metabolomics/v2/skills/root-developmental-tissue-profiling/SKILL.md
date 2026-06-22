---
name: root-developmental-tissue-profiling
description: Use when you have CDF-format mass spectrometry imaging files from plant roots with accompanying MATLAB workspace files (.mat), and your research goal is to reproduce linear-axis intensity profiles, feature distributions, and spatial metrics reported in a prior publication (e.g., Sama et al. 2025).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3630
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - DIMPLE code
  - MATLAB
  - batchcdfread
  techniques:
  - MS-imaging
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

# root-developmental-tissue-profiling

## Summary

Reproduce and execute mass spectrometry imaging analysis of plant root developmental tissues along a linear axis using DIMPLE (Developmental Imaging Mass Spectrometry Pipeline for Linear Evaluation). This skill enables quantitative profiling of spatial metabolite and ion intensity distributions across root zones.

## When to use

You have CDF-format mass spectrometry imaging files from plant roots with accompanying MATLAB workspace files (.mat), and your research goal is to reproduce linear-axis intensity profiles, feature distributions, and spatial metrics reported in a prior publication (e.g., Sama et al. 2025). Apply this skill when you need to aggregate quantitative analysis outputs across multiple root samples and export structured result files for downstream comparison.

## When NOT to use

- Input data is not in CDF format or lacks accompanying MATLAB workspace files—preprocessing and file format conversion will be required first.
- Your analysis goal is non-linear or involves 2D/3D spatial imaging rather than linear-axis profiling (DIMPLE is specialized for linear evaluation).
- Root samples have not been prepared and scanned using the same mass spectrometry imaging protocol and instrument settings as the reference publication.

## Inputs

- CDF mass spectrometry imaging files (root tissue samples)
- MATLAB workspace files (.mat) containing preprocessed data and parameters
- Root sample identifiers and replicate groupings

## Outputs

- Intensity profiles (per-root, per-feature, along linear axis)
- Feature distribution matrices (spatial and compositional)
- Spatial metrics and quantitative analysis summaries
- Aggregated result files (structured, exportable formats)

## How to apply

Load each root dataset (CDF file) and its corresponding workspace.mat file into MATLAB. Initialize the DIMPLE computational pipeline, which is designed specifically for mass spectrometry imaging data analyzed along a linear axis. Execute the per-root linear-axis analysis module sequentially for each root sample (e.g., B73-root11, B73-root2-5, B73-root-3-3). The pipeline will compute intensity profiles, feature distributions, and spatial metrics for each root. Aggregate the quantitative outputs from all root replicates and export them into structured result files for statistical comparison and validation against published results.

## Related tools

- **DIMPLE code** (Computational pipeline that initializes, executes, and aggregates per-root linear-axis analysis modules for mass spectrometry imaging data) — github.com/dickinsonlab/DIMPLE-code
- **MATLAB** (Runtime environment for loading CDF files, workspace files (.mat), and executing DIMPLE analysis modules)
- **batchcdfread** (Function (developed by Yifan Meng, Stanford) for batch reading and loading multiple CDF files into MATLAB)

## Evaluation signals

- All three B73 root workspace files load without error and contain expected variables and preprocessing parameters.
- Per-root linear-axis analysis completes for each of the three B73 samples (B73-root11, B73-root2-5, B73-root-3-3) without exceptions or warnings.
- Exported intensity profiles and feature distributions match the published results reported in Sama et al. 2025 (e.g., peak locations, relative magnitudes, spatial metric ranges).
- Aggregated result files contain non-empty and valid intensity profiles, feature counts, and spatial metrics for all root replicates.
- Output schemas and data types are consistent across all three root samples and conform to the structured result file format specification.

## Limitations

- DIMPLE is specialized for linear-axis analysis and is not suitable for full 2D or 3D spatial imaging reconstruction of root tissues.
- Reproduction requires exact versions of CDF and workspace files from the reference publication; differences in preprocessing parameters or instrument calibration may yield different results.
- The pipeline does not include statistical hypothesis testing or multivariate comparison workflows; users must implement downstream statistical analysis separately.
- Workspace files (.mat) are tied to specific MATLAB versions and may require conversion or re-preprocessing if compatibility issues arise.

## Evidence

- [readme] CDF files and MATLAB workspace files are the required inputs for this skill.: "cdf files and available Matlab workspaces are provided for the roots that were analyzed in Sama et al. 2025"
- [readme] DIMPLE is a computational pipeline designed specifically for linear-axis analysis of mass spectrometry imaging data.: "Computational pipeline for analyzing mass spectrometry imaginging data along a linear axis"
- [other] Execution proceeds sequentially through per-root modules and produces quantitative output files.: "Execute the per-root linear-axis analysis module for each of the three B73 root samples in sequence. 4. Aggregate and export the quantitative analysis outputs (intensity profiles, feature"
- [readme] The three B73 root datasets with their workspace file pairings are the concrete reference implementation.: "B73 root 1 data can be accessed in B73-root11 and B73-root11-workspace.mat. B73 root 2 data can be accessed in B73-root2-5 and B73-root2-5-workspace.mat. B73 root 3 data can be accessed in"
