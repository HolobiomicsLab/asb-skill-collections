---
name: spatial-coordinate-mapping
description: Use when after LC-MS feature detection, alignment, quantification, and optional filtering/normalization are complete, and you have intensity values for molecular features that correspond to spatial positions (e.g., tissue coordinates, imaging pixel locations).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3359
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - KNIME Analytics Platform
  - ili
  - OpenMS
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/nprot.2017.122
  title: 3D molecular cartography (Optimus / 'ili)
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_3d_molecular_cartography_optimus_ili_cq
    doi: 10.1038/nprot.2017.122
    title: 3D molecular cartography (Optimus / 'ili)
  dedup_kept_from: coll_3d_molecular_cartography_optimus_ili_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/nprot.2017.122
  all_source_dois:
  - 10.1038/nprot.2017.122
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spatial-coordinate-mapping

## Summary

Map detected LC-MS molecular features onto 2D or 3D spatial coordinates to visualize the spatial distribution of metabolites across samples. This skill transforms feature intensity matrices into spatially-indexed visualizations suitable for interactive exploration and publication.

## When to use

After LC-MS feature detection, alignment, quantification, and optional filtering/normalization are complete, and you have intensity values for molecular features that correspond to spatial positions (e.g., tissue coordinates, imaging pixel locations). Use this skill when your experimental design includes spatial metadata (sample locations, coordinates, or image registration) that you want to overlay with feature abundance patterns.

## When NOT to use

- Input samples lack spatial coordinate information or experimental design does not include position metadata.
- Feature table has not been aligned and quantified across all runs; spatial mapping requires consistent feature definitions across the sample set.
- Raw or unfiltered feature data is provided; spatial mapping should occur after optional filtering steps (blank removal, reproducibility filtering, retention-time range trimming) to avoid mapping noise artifacts.

## Inputs

- Normalized LC-MS feature intensity table (rows=features, columns=samples with quantified m/z-RT pairs)
- Experimental design file with spatial metadata (sample identifiers, 2D or 3D coordinates)

## Outputs

- Spatial feature maps in `ili`-compatible format for 2D or 3D interactive visualization
- Feature-to-coordinate index with intensity values
- Heat maps of feature intensities across spatially-indexed samples

## How to apply

Load the normalized feature intensity table and the experimental design file containing spatial coordinates into KNIME. Use the Optimus workflow nodes to execute the spatial mapping step, which associates each feature's quantified intensities with its corresponding spatial position. Validate that output files contain feature identifiers, intensity values, and correctly assigned coordinates matching the input experimental design schema. Export the mapped results in a format compatible with the `ili` web-application (a web-application for interactive visualization of spatial data mapped either on an image or a 3D model). Verify coordinate ranges and feature-to-position associations before final export.

## Related tools

- **KNIME Analytics Platform** (Workflow execution engine orchestrating feature-to-coordinate assignment and visualization export nodes) — https://www.knime.org
- **ili** (Web-application for interactive visualization of spatial data mapped either on an image or a 3D model) — https://github.com/ili-toolbox/ili
- **OpenMS** (Provides underlying LC-MS feature detection and quantification algorithms integrated into the Optimus workflow) — http://www.openms.de

## Evaluation signals

- Output coordinate ranges match the input experimental design file (no out-of-bounds or NaN coordinates).
- Every feature in the intensity table is assigned exactly one spatial position per sample; no orphaned or multiply-mapped features.
- Exported files conform to `ili` format schema and can be successfully loaded and rendered in the `ili` web-application without errors.
- Heat map visualization shows expected intensity gradients and clustering patterns consistent with the biological sample layout.
- Feature-to-coordinate associations are reproducible across workflow re-runs with identical inputs.

## Limitations

- Requires precise coordinate metadata in the experimental design file; missing or misaligned coordinates will cause spatial mapping to fail or produce misleading visualizations.
- Spatial resolution is limited by the granularity of the input coordinate system (e.g., pixel size in imaging, or discrete sample locations in metabolite cartography).
- The workflow does not perform coordinate transformation or registration; input coordinates must already be aligned to the intended spatial reference frame.
- 3D visualization quality depends on external `ili` application; Optimus generates the data but does not render interactive 3D views itself.

## Evidence

- [readme] Creating spatial maps of detected features that can be visualized in [`ili app](https://github.com/ili-toolbox/ili). It is a web-application for interactive visualization of spatial data mapped either on an image or a 3D model, also developed by Alexandrov Team.: "Creating spatial maps of detected features that can be visualized in [`ili app](https://github.com/ili-toolbox/ili). It is a web-application for interactive visualization of spatial data"
- [other] The workflow requires an experimental design file and a stub input file as inputs to process LC-MS feature tables for analysis and spatial mapping.: "The workflow requires an experimental design file and a stub input file as inputs to process LC-MS feature tables for analysis and spatial mapping."
- [other] Execute the Optimus workflow nodes in sequence to perform feature analysis and spatial mapping as defined by the workflow architecture.: "Execute the Optimus workflow nodes in sequence to perform feature analysis and spatial mapping as defined by the workflow architecture."
- [readme] Optimus is a workflow for LC-MS-based untargeted metabolomics. It can be used for feature detection, quantification, filtering (e.g. removing background features), annotation, normalization and, finally, for spatial mapping of detected molecular features in 2D and 3D: "spatial mapping of detected molecular features in 2D and 3D using the [`ili app](https://github.com/ili-toolbox/ili)"
- [other] Validate output files match expected formats and schema.: "Validate output files match expected formats and schema."
