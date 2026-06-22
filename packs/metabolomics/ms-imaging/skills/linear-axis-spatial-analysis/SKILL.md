---
name: linear-axis-spatial-analysis
description: Use when you have deposited mass spectrometry imaging datasets in NetCDF (CDF) format with accompanying MATLAB workspace files (.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - DIMPLE
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

# linear-axis-spatial-analysis

## Summary

A workflow for analyzing mass spectrometry imaging (MSI) data along a defined linear axis through the DIMPLE computational pipeline, extracting spatial intensity profiles, feature distributions, and quantitative metrics that vary with position along the root developmental gradient.

## When to use

You have deposited mass spectrometry imaging datasets in NetCDF (CDF) format with accompanying MATLAB workspace files (.mat) containing preprocessed spectra and metadata for plant root or similar linear developmental structures, and you need to reproduce or generate per-sample intensity profiles and spatial metrics along the linear axis as reported in peer-reviewed analysis.

## When NOT to use

- Input datasets are in non-NetCDF formats (e.g., mzML, mzXML) without prior conversion to CDF via appropriate tools.
- No linear axis has been defined or segmented for the sample; the analysis requires explicit positional coordinates.
- MATLAB is not available or the DIMPLE pipeline has not been installed in your computational environment.

## Inputs

- CDF (NetCDF) files containing raw mass spectrometry imaging data
- MATLAB workspace files (.mat) with preprocessed spectra and experimental metadata
- DIMPLE pipeline configuration and analysis code (from repository)
- Linear axis coordinate system or segmentation for the root sample

## Outputs

- Per-root intensity profiles along the linear axis
- Feature distribution matrices indexed by position
- Spatial metrics (e.g., intensity gradients, feature prevalence by zone)
- Aggregated quantitative result files (structured tables or figures)

## How to apply

Load the CDF files and corresponding MATLAB workspace files into MATLAB using the DIMPLE pipeline environment. Initialize the DIMPLE computational pipeline and execute the per-root linear-axis analysis module sequentially for each sample. The pipeline computes mass spectrometry imaging metrics (intensity profiles, feature distributions, and spatial metrics) parameterized by position along the linear axis. Aggregate the per-root quantitative outputs into structured result files. Validate outputs by comparing intensity profile shapes, feature count distributions, and spatial metrics against the published reference outputs for your genotype (e.g., B73 or Oaxacan Green).

## Related tools

- **DIMPLE** (Primary computational pipeline for loading CDF files, preprocessing spectra, and executing per-root linear-axis analysis with intensity and spatial metric extraction) — https://github.com/dickinsonlab/DIMPLE-code
- **MATLAB** (Execution environment and scripting language for running DIMPLE pipeline, loading workspace files (.mat), and aggregating analysis outputs)
- **batchcdfread** (Function for batch reading of CDF mass spectrometry imaging data files into MATLAB)

## Evaluation signals

- All three per-root CDF files and workspace files load without I/O errors in MATLAB via the DIMPLE pipeline environment.
- Intensity profiles for each root show coherent spatial variation (not NaN, Inf, or uniformly zero) along the linear axis.
- Aggregated per-genotype outputs (e.g., B73 or Oaxacan Green) match the reported results in Sama et al. 2025 in terms of number of features detected, intensity ranges, and spatial distribution patterns.
- Feature distributions and spatial metrics are symmetric or asymmetric as expected from developmental biology (e.g., root tip vs. mature zones).
- Structured result files can be parsed and contain the expected columns (position, intensity, feature ID, metric value).

## Limitations

- The pipeline requires pre-existing CDF and MATLAB workspace files; raw MSI data in other formats must be converted beforehand.
- Linear-axis segmentation must be defined and embedded in the workspace or provided separately; ambiguous or missing axis definitions will cause analysis to fail or produce invalid metrics.
- Reproducibility depends on matching MATLAB version and DIMPLE code version; results may differ with updated dependencies.
- The batchcdfread function requires that CDF files follow the expected structure and naming convention; malformed or incomplete files will not load.

## Evidence

- [readme] cdf files and available Matlab workspaces are provided for the roots that were analyzed in Sama et al. 2025: "cdf files and available Matlab workspaces are provided for the roots that were analyzed in Sama et al. 2025"
- [other] Execute the per-root linear-axis analysis module for each of the three B73 root samples in sequence: "Execute the per-root linear-axis analysis module for each of the three B73 root samples in sequence"
- [other] Aggregate and export the quantitative analysis outputs (intensity profiles, feature distributions, and spatial metrics) for each root into structured result files: "Aggregate and export the quantitative analysis outputs (intensity profiles, feature distributions, and spatial metrics) for each root into structured result files"
- [readme] Computational pipeline for analyzing mass spectrometry imaging data along a linear axis: "Computational pipeline for analyzing mass spectrometry imaging data along a linear axis"
- [other] Load the cdf files and workspace data into Matlab using the DIMPLE pipeline environment: "Load the cdf files and workspace data into Matlab using the DIMPLE pipeline environment"
