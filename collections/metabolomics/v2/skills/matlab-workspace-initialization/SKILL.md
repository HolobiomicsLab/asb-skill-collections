---
name: matlab-workspace-initialization
description: Use when when you have mass spectrometry imaging root datasets paired with accompanying .mat workspace files (as in the B73 and Oaxacan Green genotypes from Sama et al.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - DIMPLE code
  - MATLAB
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# matlab-workspace-initialization

## Summary

Load and initialize pre-computed MATLAB workspace files (.mat) containing mass spectrometry imaging datasets and their analysis state to enable reproducible linear-axis analysis of root developmental metabolomes. This skill bridges raw CDF data with downstream DIMPLE pipeline execution by restoring a known computational environment.

## When to use

When you have mass spectrometry imaging root datasets paired with accompanying .mat workspace files (as in the B73 and Oaxacan Green genotypes from Sama et al. 2025), and you need to reproduce or extend linear-axis quantitative analysis outputs (intensity profiles, feature distributions, spatial metrics) without re-initializing the data pipeline from raw CDF files.

## When NOT to use

- If the .mat file is corrupted, outdated, or incompatible with your MATLAB version — in that case, reconstruct the workspace by parsing the raw CDF file with batchcdfread.
- If you need to apply new preprocessing, filtering, or segmentation rules that differ from those embedded in the original .mat file — load the CDF directly and build a fresh workspace.
- If the analysis targets a genotype or root sample without a provided .mat file (e.g., some OG samples may lack accompanying workspaces) — load the CDF and initialize DIMPLE from scratch.

## Inputs

- CDF file (mass spectrometry imaging data, e.g., B73-root11)
- MATLAB workspace file (.mat, e.g., B73-root11-workspace.mat)
- DIMPLE pipeline code repository

## Outputs

- Loaded MATLAB workspace with parsed mass spectrometry data and calibration metadata
- Quantitative intensity profiles along the linear axis
- Feature distribution matrices and spatial metrics
- Structured result files (per-root analysis outputs)

## How to apply

In MATLAB, use the `load()` function to read the companion .mat workspace file for your root sample (e.g., B73-root11-workspace.mat). The workspace contains pre-parsed CDF data, calibration metadata, and any prior segmentation or preprocessing state. After loading, verify that key variables are present in the workspace (dataset identifiers, mass-to-charge arrays, intensity matrices, spatial coordinates). Then initialize the DIMPLE computational pipeline with these restored variables and execute the per-root linear-axis analysis module. This approach avoids redundant CDF parsing via the batchcdfread function and ensures consistency with the original analysis reported in the publication.

## Related tools

- **DIMPLE code** (Computational pipeline for mass spectrometry imaging analysis along a linear axis; executes after workspace initialization to perform per-root feature extraction and quantification) — github.com/dickinsonlab/DIMPLE-code
- **MATLAB** (Runtime environment for loading .mat workspace files, managing data structures, and executing the DIMPLE pipeline)

## Examples

```
load('B73-root11-workspace.mat'); % Restore workspace with parsed data and metadata
```

## Evaluation signals

- Workspace load succeeds without errors; no missing or corrupted variables reported by MATLAB.
- Restored mass-to-charge arrays and intensity matrices have expected dimensions and value ranges (non-negative intensities, m/z covering the profiled mass range).
- Spatial coordinate and segmentation metadata (if present) are consistent with the published dataset descriptions.
- Linear-axis analysis outputs (intensity profiles, feature counts, spatial metrics) match or closely reproduce the results reported in Sama et al. 2025 for the same root sample.
- Timestamps or version identifiers embedded in the .mat file match the publication date and DIMPLE code version used in the study.

## Limitations

- Workspace files are version-specific; loading a .mat file created in MATLAB R2018a in MATLAB R2024a may encounter compatibility issues with certain data structures.
- Pre-computed workspace files preserve only the state at the time they were saved; any upstream processing errors or parameter choices are locked in and cannot be easily revised without accessing raw CDF data.
- Not all provided root samples include .mat workspaces (e.g., OG2-P11-0 is mentioned in the README without an explicit workspace filename), requiring fallback to CDF parsing.
- The workspace format and variable naming conventions are specific to the DIMPLE pipeline; adaptation to other mass spectrometry imaging analysis frameworks will require re-initialization from raw data.

## Evidence

- [readme] cdf files and available Matlab workspaces are provided: "cdf files and available Matlab workspaces are provided for the roots that were analyzed in Sama et al. 2025."
- [intro] B73 root datasets with accompanying workspace files: "B73 root 1 data can be accessed in B73-root11 and B73-root11-workspace.mat. B73 root 2 data can be accessed in B73-root2-5 and B73-root2-5-workspace.mat"
- [intro] Initialize DIMPLE pipeline after loading workspace: "Initialize the DIMPLE computational pipeline for mass spectrometry imaging data analysis along the linear axis."
- [intro] Linear-axis analysis outputs and aggregation: "Aggregate and export the quantitative analysis outputs (intensity profiles, feature distributions, and spatial metrics) for each root into structured result files."
- [readme] batchcdfread function for CDF parsing: "batchcdfread function developed by Yifan Meng in Dr. Richard N. Zare's lab at Stanford University"
