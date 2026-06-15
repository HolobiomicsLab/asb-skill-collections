---
name: trajectory-inference-method-selection
description: Use when when you have an ArchR project object with processed single-cell ATAC-seq data and want to infer developmental or cell-state trajectories.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3178
  tools:
  - R
  - ArchR
  - monocle3
  - Slingshot
derived_from:
- doi: 10.1038/s41588-021-00790-6
  title: archr
evidence_spans:
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

# trajectory-inference-method-selection

## Summary

Selects and applies the appropriate trajectory inference method (Monocle3 or Slingshot) to an ArchR project object containing single-cell ATAC-seq data, enabling discovery of cell developmental or differentiation trajectories. Method selection is driven by user preference and the choice determines which embedding algorithm and downstream analysis functions are invoked.

## When to use

When you have an ArchR project object with processed single-cell ATAC-seq data and want to infer developmental or cell-state trajectories. Use this skill when your analysis design requires choosing between Monocle3's RNA velocity–inspired approach and Slingshot's clustering-based lineage inference, or when you need to compare trajectory results across both methods.

## When NOT to use

- Input ArchR project lacks sufficient cell diversity or clustering structure (Slingshot requires well-defined clusters; Monocle3 may fail on homogeneous cell populations).
- Data is unimodal (single cell state) with no indication of developmental progression or branching.
- You require trajectory analysis on non-ATAC-seq modalities without ArchR integration (e.g., raw RNA-seq FASTQ files).

## Inputs

- ArchR project object
- user trajectory method selection (Monocle3 or Slingshot)
- preprocessed single-cell ATAC-seq count matrix or embedding

## Outputs

- ArchR project object with trajectory embedding
- trajectory metadata (pseudotime, cell state assignments)
- trajectory visualization coordinates

## How to apply

Evaluate the user's selection parameter to determine whether Monocle3 or Slingshot trajectory analysis should be applied. If Monocle3 is selected, invoke addMonocleTrajectory on the prepared ArchR project object to compute trajectory embedding using the Monocle3 algorithm. If Slingshot is selected, invoke addSlingShotTrajectories on the ArchR project to compute trajectory embedding using the Slingshot algorithm. Both functions operate on the same ArchR project input and return a modified project object with trajectory metadata and embeddings attached. The choice should reflect whether you prioritize continuous cell-state transitions (Monocle3) or defined cluster-to-cluster lineages (Slingshot).

## Related tools

- **ArchR** (Container package providing project object infrastructure and integration layer for trajectory methods; implements addMonocleTrajectory and addSlingShotTrajectories wrapper functions) — https://github.com/GreenleafLab/ArchR
- **monocle3** (Trajectory inference engine invoked via ArchR's addMonocleTrajectory; computes pseudotime and cell-state transitions using graph-based reverse graph embedding)
- **Slingshot** (Trajectory inference engine invoked via ArchR's addSlingShotTrajectories; computes cluster-based lineages and pseudotime on reduced-dimension embeddings)
- **R** (Execution language and environment for ArchR and all trajectory analysis functions)

## Examples

```
# After loading ArchR project, conditionally apply trajectory method:
if (trajectory_method == "monocle3") {
  projTraj <- addMonocleTrajectory(ArchRProj = proj, name = "Monocle", groupBy = "Clusters")
} else if (trajectory_method == "slingshot") {
  projTraj <- addSlingShotTrajectories(ArchRProj = proj, name = "Slingshot", groupBy = "Clusters")
}
```

## Evaluation signals

- Returned ArchR project object contains trajectory embedding in the reductionUMAP or reductionTSNE slot without errors or missing values.
- Pseudotime values are continuous, monotonically ordered, and span the expected range (typically 0–100 or 0–1 normalized).
- Cell-state or lineage assignments are consistent with known developmental markers or cluster transitions.
- No NA or NaN values in trajectory metadata fields; all cells in the project receive a pseudotime assignment.
- Trajectory visualization (plotTrajectory or equivalent) shows connected paths through cell clusters without crossing or disconnected components (for Slingshot) or smooth gradient from start to end state (for Monocle3).

## Limitations

- ArchR's trajectory functions require prior clustering or dimensionality reduction (addIterativeLSI, addCombinedDims); results are sensitive to these upstream steps.
- Monocle3 integration depends on expression data; paired scRNA-seq input may be required for optimal trajectory inference from ATAC-seq alone.
- Slingshot assumes discrete cell clusters and may fail or produce spurious trajectories if cluster boundaries are weak or overlapping.
- Both methods compute pseudotime on reduced dimensions and may miss biological trajectories that are not well-separated in the embedding space.
- ArchR is currently in beta (as noted in README); breaking changes to trajectory function signatures or default parameters may occur.

## Evidence

- [readme] ArchR now directly supports both monocle3 and Slingshot based trajectory analysis!: "ArchR now directly supports both monocle3 and Slingshot based trajectory analysis!"
- [other] ArchR implements trajectory analysis through three functions: getMonocleTrajectories and addMonocleTrajectory for Monocle3-based analysis, and addSlingShotTrajectories for Slingshot-based analysis: "ArchR implements trajectory analysis through three functions: getMonocleTrajectories and addMonocleTrajectory for Monocle3-based analysis, and addSlingShotTrajectories for Slingshot-based analysis"
- [other] If Monocle3 selected, invoke addMonocleTrajectory on the ArchR project to compute trajectory embedding using Monocle3 algorithm: "If Monocle3 selected, invoke addMonocleTrajectory on the ArchR project to compute trajectory embedding using Monocle3 algorithm"
- [other] If Slingshot selected, invoke addSlingShotTrajectories on the ArchR project to compute trajectory embedding using Slingshot algorithm: "If Slingshot selected, invoke addSlingShotTrajectories on the ArchR project to compute trajectory embedding using Slingshot algorithm"
- [readme] See updates with getMonocleTrajectories, addMonocleTrajectory, addSlingShotTrajectories: "See updates with getMonocleTrajectories, addMonocleTrajectory, addSlingShotTrajectories"
