---
name: dimple-pipeline-execution
description: Use when when you have deposited mass spectrometry imaging data in NetCDF
  (CDF) format paired with MATLAB workspace files (.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MATLAB
  - batchcdfread function
  techniques:
  - MS-imaging
  license_tier: restricted
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

# dimple-pipeline-execution

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Execute the DIMPLE (Developmental Imaging Mass Spectrometry Pipeline for Linear Evaluation) computational pipeline to process mass spectrometry imaging datasets along a linear axis and generate per-root quantitative analysis outputs. This skill is essential when reproducing published linear-axis imaging mass spectrometry analyses on root tissues.

## When to use

When you have deposited mass spectrometry imaging data in NetCDF (CDF) format paired with MATLAB workspace files (.mat) for root samples, and you need to reproduce or generate per-root linear-axis analysis metrics (intensity profiles, feature distributions, spatial metrics) as reported in peer-reviewed imaging mass spectrometry studies.

## When NOT to use

- Input CDF file lacks a corresponding MATLAB workspace file, as the pipeline requires both paired files for reproducibility.
- Data was collected using non-linear sampling geometry or does not have a clearly defined linear axis of interest, since DIMPLE is specifically designed for linear-axis analysis.
- The root sample has not been preprocessed through the same mass spectrometry imaging acquisition and initial workspace-generation steps as the deposited datasets, as workspace parameters are genotype and instrument-specific.

## Inputs

- Mass spectrometry imaging CDF file (NetCDF format)
- MATLAB workspace file (.mat) containing preprocessing data and parameters
- DIMPLE pipeline source code (MATLAB)

## Outputs

- Per-root intensity profiles (linear-axis)
- Per-root feature distributions
- Per-root spatial metrics
- Aggregated quantitative analysis result files

## How to apply

Load the CDF file and its accompanying MATLAB workspace file into the MATLAB environment where DIMPLE is installed. Initialize the DIMPLE computational pipeline and select the per-root linear-axis analysis module. Execute the analysis sequentially for each root dataset (e.g., B73-root11, B73-root2-5, B73-root-3-3 for B73 genotype or OG1, OG5, OG2-P11-0 for Oaxacan Green). The pipeline will compute mass spectrometry imaging metrics along the predefined linear axis for each root. Aggregate the per-root outputs into structured result files containing intensity profiles and spatial metrics, then validate that outputs match the expected genotype-level results by comparing against published findings.

## Related tools

- **MATLAB** (Runtime environment for loading CDF files, workspace data, and executing DIMPLE pipeline modules for linear-axis analysis)
- **batchcdfread function** (Utility developed in Dr. Richard N. Zare's lab for batch reading NetCDF files within the DIMPLE pipeline)

## Evaluation signals

- All three root datasets for a given genotype load without error and pass workspace initialization checks.
- Per-root output files are generated for each input dataset with non-empty intensity profiles and spatial metric tables.
- Aggregated genotype-level results (mean/median intensity, feature counts, spatial distribution summaries) match published values reported in Sama et al. 2025 within expected numerical precision.
- Output structure and naming conventions (e.g., intensity_profile_B73-root11.mat) conform to DIMPLE's documented output schema.
- No missing or NaN values in critical output fields (linear-axis coordinates, intensity values, feature identifiers) for any root in the batch.

## Limitations

- DIMPLE version used must match the version described in Sama et al. 2025; code updates or parameter changes in later releases may produce different outputs.
- Pipeline is optimized for root tissue mass spectrometry imaging; application to other tissue types or non-linear spatial sampling may require modification.
- Reproducibility depends on exact MATLAB version, installed toolboxes, and batchcdfread function version from Dr. Zare's lab; environmental differences may introduce numerical drift.
- Workspace files (.mat) may contain hard-coded genotype-specific parameters (e.g., normalization constants, feature thresholds) that are not transferable to new datasets without manual recalibration.

## Evidence

- [readme] Computational pipeline for analyzing mass spectrometry imaginging data along a linear axis: "Computational pipeline for analyzing mass spectrometry imaginging data along a linear axis"
- [intro] B73-root11 with B73-root11-workspace.mat, B73-root2-5 with B73-root2-5-workspace.mat, and B73-root-3-3 with B73-root2-3-worskpace.mat: "Three B73 root datasets with accompanying Matlab workspace files are available for reproduction: B73-root11 with B73-root11-workspace.mat, B73-root2-5 with B73-root2-5-workspace.mat, and B73-root-3-3"
- [other] Load the B73-root11, B73-root2-5, and B73-root-3-3 datasets and their corresponding workspace.mat files into MATLAB. Initialize the DIMPLE computational pipeline for mass spectrometry imaging data analysis along the linear axis. Execute the per-root linear-axis analysis module for each of the three B73 root samples in sequence. Aggregate and export the quantitative analysis outputs (intensity profiles, feature distributions, and spatial metrics) for each root into structured result files.: "Load the B73-root11, B73-root2-5, and B73-root-3-3 datasets and their corresponding workspace.mat files into MATLAB. Initialize the DIMPLE computational pipeline for mass spectrometry imaging data"
- [readme] cdf files and available Matlab workspaces are provided for the roots that were analyzed in Sama et al. 2025: "cdf files and available Matlab workspaces are provided for the roots that were analyzed in Sama et al. 2025"
- [readme] batchcdfread function developed by Yifan Meng in Dr. Richard N. Zare's lab at Stanford University: "batchcdfread function developed by Yifan Meng in Dr. Richard N. Zare's lab at Stanford University"
