---
name: peak-calling-pseudo-bulk-aggregation
description: 'Use when after clustering single-cell ATAC-seq data (e.g., via Leiden clustering on spectral embeddings), use this skill to identify peaks within each cluster. Triggering conditions: (1) you have sparse, per-cell insertion counts organized in a tile matrix;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3222
  edam_topics:
  - http://edamontology.org/topic_0749
  - http://edamontology.org/topic_3169
  tools:
  - SnapATAC2
  - Python
  - tl.macs3
  - tl.merge_peaks
  - MACS3
  - Leiden
  - UMAP
derived_from:
- doi: 10.1038/s41592-023-02139-9
  title: snapatac2
evidence_spans:
- 'SnapATAC2: A Python/Rust package for single-cell epigenomics analysis'
- A Python/Rust package for single-cell epigenomics analysis
- tl.macs3
- tl.merge_peaks
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_snapatac2
    doi: 10.1038/s41592-023-02139-9
    title: snapatac2
  dedup_kept_from: coll_snapatac2
schema_version: 0.2.0
---

# peak-calling-pseudo-bulk-aggregation

## Summary

Aggregate single-cell ATAC-seq fragments into pseudo-bulk samples grouped by cluster assignment, then call peaks using MACS3 to identify chromatin-accessible regions that are consistent within cell populations. This approach recovers peaks from sparse single-cell data by leveraging population-level signal.

## When to use

After clustering single-cell ATAC-seq data (e.g., via Leiden clustering on spectral embeddings), use this skill to identify peaks within each cluster. Triggering conditions: (1) you have sparse, per-cell insertion counts organized in a tile matrix; (2) cells have been assigned to discrete clusters or cell-type annotations; (3) you want to call peaks that are reproducible within cell populations rather than in individual cells; (4) downstream analyses require cluster-specific peak lists for differential accessibility or motif enrichment.

## When NOT to use

- Input is already a pre-computed peak set or peak matrix; peak calling has been performed elsewhere.
- Cluster assignments are unreliable or highly fragmented (many clusters with <100 cells each), reducing pseudo-bulk signal below MACS3 detection threshold.
- You need single-cell resolution peaks (e.g., to study peak heterogeneity within a cluster); pseudo-bulk aggregation will obscure cell-to-cell variation.

## Inputs

- Single-cell ATAC-seq fragment file (imported and stored as paired-end insertions in AnnData)
- Cluster assignments for each cell (from tl.leiden or equivalent clustering method)
- Tile matrix or other sparse count matrix representing chromatin accessibility

## Outputs

- Per-cluster peak list (BED format or equivalent, called by MACS3)
- Merged peak set (union or consensus of all cluster-specific peaks)
- Peak matrix (annotation of cells by peak presence/absence, via pp.make_peak_matrix)

## How to apply

Group fragments by cluster assignment and aggregate them into a single pseudo-bulk BAM or fragment file per cluster. Pass each pseudo-bulk file to tl.macs3 with appropriate parameters (e.g., genome size, p-value threshold, minimum read count). MACS3 will perform peak calling on the aggregated signal from all cells within a cluster, improving signal-to-noise compared to single-cell calling. After calling peaks independently for each cluster, merge overlapping peaks across clusters using tl.merge_peaks to create a unified peak set. This strategy exploits the population-level chromatin accessibility pattern while avoiding the sparsity problem of individual-cell peak calling. Validate peak calls by comparing cluster assignments and UMAP coordinates before and after peak calling to ensure clustering quality is preserved.

## Related tools

- **SnapATAC2** (Provides tl.macs3 for pseudo-bulk peak calling and tl.merge_peaks for peak merging; orchestrates fragment import, tile matrix generation, clustering, and peak calling in a unified pipeline.) — https://github.com/scverse/SnapATAC2
- **MACS3** (Peak calling algorithm applied to pseudo-bulk aggregated fragments; detects chromatin-accessible regions from enriched read pileups.)
- **Leiden** (Clustering algorithm used to assign cells to populations before pseudo-bulk aggregation.)
- **UMAP** (Visualization of cell embeddings; used to validate that cluster quality and structure are preserved after peak calling.)

## Examples

```
import snapatac2 as snap; adata = snap.pp.import_fragments(fragments_file); snap.pp.add_tile_matrix(adata); snap.tl.spectral(adata); snap.tl.leiden(adata); snap.tl.macs3(adata, groupby='leiden'); snap.tl.merge_peaks(adata)
```

## Evaluation signals

- Cluster assignments and UMAP coordinates are stable and reproducible before and after peak calling (consistent with reference tutorial outcomes).
- Number of peaks per cluster is consistent with expected chromatin complexity (typically 10k–100k peaks for PBMC populations).
- Overlapping peaks across clusters are successfully merged; merged peak set size is reasonable relative to individual cluster peak counts.
- Peak calls are enriched at known regulatory regions (e.g., transcription start sites, enhancers); can be validated by motif enrichment or comparison to published ATAC-seq datasets.
- Per-cluster peak matrices can be generated successfully via pp.make_peak_matrix and have expected dimensions (cells × merged peaks).

## Limitations

- Pseudo-bulk aggregation requires sufficient cell counts per cluster; clusters with very few cells (<50–100) may have insufficient signal for robust peak calling.
- Peak merging strategy (overlap threshold, consensus vs. union) can affect downstream interpretation; choice depends on whether you want permissive or strict peak sets.
- MACS3 parameters (p-value, minimum read count, genome size) are critical; suboptimal tuning may yield false positives or false negatives. Default parameters may not suit all tissues or species.
- Pseudo-bulk averaging obscures within-cluster heterogeneity; cells with divergent chromatin states will be homogenized in the aggregated signal.

## Evidence

- [intro] End-to-end analysis pipeline for single-cell ATAC-seq data including preprocessing, dimension reduction, clustering, data integration, and peak calling: "End-to-end analysis pipeline for single-cell ATAC-seq data, including preprocessing, dimension reduction, clustering, data integration, peak calling"
- [other] Perform clustering using tl.leiden with default resolution parameter. Call peaks using tl.macs3 in pseudo-bulk mode grouped by cluster assignment. Merge overlapping peaks using tl.merge_peaks.: "Perform clustering using tl.leiden with default resolution parameter. Call peaks using tl.macs3 in pseudo-bulk mode grouped by cluster assignment. Merge overlapping peaks using tl.merge_peaks"
- [methods] Peak calling tools in SnapATAC2 support MACS3 and peak merging for single-cell ATAC-seq analysis: "tl.macs3, tl.merge_peaks for peak calling"
- [readme] Blazingly fast preprocessing tools for BAM to fragment files conversion and count matrix generation: "Blazingly fast preprocessing tools for BAM to fragment files conversion and count matrix generation"
