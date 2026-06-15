---
name: monocle3-trajectory-embedding
description: Use when you have an ArchR project object with dimensionality reduction results (LSI or combined dimensions from scATAC-seq ± scRNA-seq) and want to infer pseudotime trajectories and cell-state transitions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3565
  edam_topics:
  - http://edamontology.org/topic_0654
  - http://edamontology.org/topic_3169
  tools:
  - monocle3
  - R
  - ArchR
derived_from:
- doi: 10.1038/s41588-021-00790-6
  title: archr
evidence_spans:
- ArchR now directly supports both monocle3 and Slingshot based trajectory analysis
- ArchR is a full-featured R package for processing and analyzing single-cell ATAC-seq data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_archr
    doi: 10.1038/s41588-021-00790-6
    title: archr
  dedup_kept_from: coll_archr
schema_version: 0.2.0
---

# monocle3-trajectory-embedding

## Summary

Compute pseudotime-ordered cell-state trajectories from single-cell ATAC-seq data using Monocle 3 within ArchR. This skill reconstructs developmental or differentiation trajectories by embedding cells along learned paths of gene regulatory change.

## When to use

Use this skill when you have an ArchR project object with dimensionality reduction results (LSI or combined dimensions from scATAC-seq ± scRNA-seq) and want to infer pseudotime trajectories and cell-state transitions. Appropriate when your biological question involves understanding developmental progression, cell fate decisions, or temporal ordering of cell populations within a single-cell ATAC-seq experiment.

## When NOT to use

- Your ArchR project has not yet been processed with LSI or combined dimensionality reduction (addIterativeLSI or addCombinedDims must precede this skill).
- Your biological question does not require pseudotime ordering or trajectory inference (e.g., static cell-type annotation, snapshot comparisons).
- You prefer an alternative trajectory method; use addSlingShotTrajectories instead if Slingshot is your chosen algorithm.

## Inputs

- ArchR project object with computed LSI or combined dimensions
- Cell metadata (optional: cell type or batch annotations to guide trajectory direction)

## Outputs

- ArchR project object with embedded trajectory (pseudotime, cell state assignments)
- Monocle 3 trajectory object (CDS) containing manifold and pseudotime coordinates

## How to apply

Load the prepared ArchR project object containing computed LSI or combined dimensions. Call getMonocleTrajectories to extract trajectory information, or directly invoke addMonocleTrajectory to compute and embed trajectory data using the Monocle 3 algorithm. Monocle 3 will learn a reduced-dimensional manifold within the ArchR project's existing embedding space, order cells by pseudotime, and identify branch points. The resulting ArchR project object will contain trajectory metadata (pseudotime values, cell state assignments) that can be visualized and used for downstream differential accessibility analysis along the trajectory.

## Related tools

- **ArchR** (Container framework for scATAC-seq analysis; hosts getMonocleTrajectories and addMonocleTrajectory functions and manages the project object.) — https://github.com/GreenleafLab/ArchR
- **monocle3** (Underlying algorithm for trajectory learning, pseudotime computation, and manifold embedding; invoked by ArchR wrapper functions.)

## Examples

```
addMonocleTrajectory(ArchRProj = proj, trajectory = "trajectory_name", groupBy = "Clusters", reducedDims = "LSI_Combined")
```

## Evaluation signals

- ArchR project object returned contains a new 'trajectory' metadata column with numeric pseudotime values (range typically 0–max pseudotime); values should be monotonically non-decreasing along inferred paths.
- Visualization of cells on the trajectory embedding (e.g., plotTrajectory or ArchR's plotting functions) shows smooth ordering of cells without major jumps or reversals in pseudotime.
- Monocle 3 object (CDS) is successfully integrated into the ArchR project; getMonocleTrajectories returns non-NULL trajectory information with cell-state graph structure.
- Cells in biologically early or undifferentiated states (e.g., stem cells or progenitors) cluster toward low pseudotime; terminally differentiated states toward high pseudotime (consistent with known biology).
- Number of cells assigned to trajectory is close to total cell count; few cells dropped or unassigned suggests robust trajectory learning.

## Limitations

- Monocle 3 trajectory learning depends on sufficient dimensionality reduction quality; poor LSI or combined dimensions will yield uninformative trajectories.
- Pseudotime is a relative ordering; absolute biological time cannot be inferred without independent temporal data or experimental design.
- Branching trajectories may be ambiguous if biological cell states are not well-separated in the embedding space; interpretation requires complementary validation (e.g., RNA-seq or ChIP-seq).
- ArchR is currently in beta; active development may introduce breaking changes to function signatures or trajectory metadata structure.

## Evidence

- [readme] ArchR supports Monocle 3 trajectory analysis with getMonocleTrajectories and addMonocleTrajectory functions: "ArchR now directly supports both monocle3 and Slingshot based trajectory analysis! See updates with getMonocleTrajectories, addMonocleTrajectory, addSlingShotTrajectories"
- [other] Workflow: invoke addMonocleTrajectory to compute trajectory embedding using Monocle3 algorithm: "If Monocle3 selected, invoke addMonocleTrajectory on the ArchR project to compute trajectory embedding using Monocle3 algorithm."
- [readme] ArchR is an R package for processing single-cell ATAC-seq data with extensive analysis tools: "ArchR is a full-featured R package for processing and analyzing single-cell ATAC-seq data."
- [readme] ArchR supports paired scATAC-seq and scRNA-seq analysis with multi-modal functions: "ArchR now supports paired scATAC-seq and scRNA-seq Analysis! See updates with importFeatureMatrix, addGeneExpressionMatrix, addIterativeLSI, addCombinedDims"
