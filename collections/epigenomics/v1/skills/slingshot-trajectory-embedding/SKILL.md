---
name: slingshot-trajectory-embedding
description: Use when you have an ArchR project with clustered single-cell ATAC-seq cells and want to reconstruct developmental or cellular transition trajectories. Use this skill when your research question requires ordering cells along a developmental continuum (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3945
  edam_topics:
  - http://edamontology.org/topic_0102
  - http://edamontology.org/topic_3676
  tools:
  - Slingshot
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

# slingshot-trajectory-embedding

## Summary

Use Slingshot trajectory analysis within ArchR to compute pseudotime and developmental lineage assignments for single-cell ATAC-seq data, inferring continuous developmental progressions from discrete cell clusters.

## When to use

You have an ArchR project with clustered single-cell ATAC-seq cells and want to reconstruct developmental or cellular transition trajectories. Use this skill when your research question requires ordering cells along a developmental continuum (e.g., to infer pseudotime) and you prefer Slingshot over Monocle3 for its minimal assumptions about trajectory topology.

## When NOT to use

- Your cells are not yet clustered or you lack a computed dimensionality reduction embedding — run addIterativeLSI and clustering steps first.
- You require trajectory analysis on RNA expression rather than ATAC chromatin accessibility — consider RNA-based trajectory tools or use paired scRNA-seq data with addGeneExpressionMatrix first.
- You need explicit comparison of multiple trajectory algorithms in a single analysis — use this skill for Slingshot only; pair it separately with addMonocleTrajectory if you want parallel Monocle3 results.

## Inputs

- ArchR project object with computed cluster assignments
- ArchR project object with dimensionality reduction embedding (e.g., iterativeLSI or combined dims)

## Outputs

- ArchR project object with Slingshot trajectory embedding and pseudotime assignments
- Trajectory lineage and pseudotime metadata per cell

## How to apply

Load a prepared ArchR project object containing computed cluster assignments and dimensionality reduction embeddings (e.g., from addIterativeLSI or addCombinedDims). Invoke addSlingShotTrajectories on the ArchR project, specifying the clustering and dimensionality reduction parameters. Slingshot will fit smooth spline curves through the cluster centers, inferring pseudotime and lineage assignments for each cell. The function returns the modified ArchR project with trajectory embeddings stored internally; inspect the trajectory results to validate that inferred lineages match your expected developmental stages or biological branching pattern.

## Related tools

- **ArchR** (Primary analysis framework; holds the project object and manages trajectory computation and storage) — https://github.com/GreenleafLab/ArchR
- **Slingshot** (Trajectory inference algorithm embedded in ArchR; computes pseudotime and lineage assignments via spline fitting through cluster centers)

## Examples

```
addSlingShotTrajectories(ArchRProject = projEx, name = 'Slingshot', groupBy = 'Clusters', embedding = 'UMAP')
```

## Evaluation signals

- ArchR project object is successfully modified and contains trajectory metadata accessible via project@trajectories or similar accessor; no warnings or errors during addSlingShotTrajectories execution.
- Inferred pseudotime values are continuous, non-negative, and span a meaningful range (e.g., 0–100 or 0–1) across cells; each cell is assigned to one or more lineages.
- Trajectory lineages correspond to expected biological transitions (e.g., early → intermediate → terminal differentiation states) based on prior clustering or marker gene knowledge.
- Pseudotime ordering of cells within each lineage is monotonic and consistent with the underlying biological process; cells with similar pseudotime values cluster together in the embedding space.
- Trajectory curves are smooth and pass through or near cluster centers without sharp kinks; visual inspection of trajectory overlays on dimensionality reduction plots (t-SNE, UMAP) shows sensible paths.

## Limitations

- Slingshot assumes smooth, tree-like or linear developmental trajectories; complex branching patterns with multiple simultaneous lineages may not be well-represented.
- Requires pre-computed cluster assignments; quality of trajectory inference depends critically on clustering resolution and dimensionality reduction accuracy.
- ArchR implementation currently lacks fine-grained control over Slingshot parameters (e.g., number of knots, smoothing penalty) via the high-level wrapper; advanced customization may require direct Slingshot package calls.
- Single-cell ATAC-seq data is inherently sparse; pseudotime inference may be less robust in rare cell populations or undersampled lineages.

## Evidence

- [other] ArchR supports trajectory analysis using both monocle3 and Slingshot: "ArchR now directly supports both monocle3 and Slingshot based trajectory analysis! See updates with getMonocleTrajectories, addMonocleTrajectory, addSlingShotTrajectories"
- [other] Slingshot is invoked via the addSlingShotTrajectories function: "If Slingshot selected, invoke addSlingShotTrajectories on the ArchR project to compute trajectory embedding using Slingshot algorithm."
- [readme] ArchR is a full-featured R package for scATAC-seq analysis: "ArchR is a full-featured R package for processing and analyzing single-cell ATAC-seq data."
