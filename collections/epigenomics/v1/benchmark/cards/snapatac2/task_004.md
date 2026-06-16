# SciTask Card: Reproduce the end-to-end ATAC-seq analysis pipeline on the pbmc10k_multiome dataset

- Task ID: `task_004`
- Schema version: `0.18.0`
- Created at: `2026-06-15T19:32:53.712417+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_epigenomics/coll_snapatac2/synthesized_package`
- Domain: `bioinformatics`
- Subtask categories: `data-processing`, `data-analysis`, `benchmark-evaluation`
- DOI: `10.1038/s41592-023-02139-9`
- GitHub: `scverse/SnapATAC2`

## Classification

- Task kind: `reproduction`
- Article type: `software-tool`
- Primary domain: `multi-omics`
- Subdomains: `multi-omics-integration`
- Techniques: `clustering`, `dimensionality-reduction`, `batch-correction`, `normalization`
- Keywords: `single-cell atac-seq` · `single-cell epigenomics` · `spectral embedding` · `multi-omics integration` · `dimension reduction` · `clustering` · `peak calling` · `preprocessing` · `fragment file conversion` · `scalable analysis`

## Research Question
Can the SnapATAC2 pipeline successfully process the pbmc10k_multiome dataset through fragment import, tile matrix generation, spectral embedding, leiden clustering, and peak calling to reproduce documented cluster assignments?

## Connected Finding
SnapATAC2 provides an end-to-end analysis pipeline for single-cell ATAC-seq data that includes preprocessing, dimension reduction, clustering, data integration, and peak calling steps.

## Task Description
Execute the complete SnapATAC2 analysis pipeline on the pbmc10k_multiome dataset, from fragment import through peak calling with tl.macs3, and reproduce the reported cluster assignments and UMAP layout documented in the SnapATAC2 tutorial.

## Inputs
- pbmc10k_multiome dataset from snapatac2.datasets

## Expected Outputs
- AnnData object with imported fragments and filtered cells
- AnnData object with tile count matrix
- Spectral embedding coordinates saved in .obsm
- UMAP layout coordinates in .obsm['X_umap']
- Cluster labels in .obs['leiden']
- Peak coordinates and statistics table from tl.macs3
- Merged peak set with cluster reproducibility metrics

## Expected Output File

- `pbmc10k_multiome_processed.h5ad`

## Landmark Outputs

- `pbmc10k_multiome_imported.h5ad`
- `pbmc10k_multiome_tile_matrix.h5ad`
- `spectral_coordinates.csv`
- `umap_coordinates.csv`
- `leiden_clusters.csv`
- `merged_peaks.bed`

## Tools
- SnapATAC2
- Python
- pp.import_fragments
- pp.add_tile_matrix
- tl.spectral
- tl.umap
- tl.leiden
- tl.macs3
- tl.merge_peaks
- Leiden
- UMAP

## Skills
- single-cell-atac-fragment-import-processing
- tile-matrix-generation-counting-strategy-selection
- spectral-embedding-dimension-reduction-parameters
- leiden-clustering-resolution-optimization
- peak-calling-pseudo-bulk-aggregation
- cluster-umap-layout-reproducibility-benchmarking

## Workflow Description
1. Download the pbmc10k_multiome dataset using snapatac2.datasets.pbmc10k_multiome. 2. Import fragment files into AnnData using pp.import_fragments with paired-end mode. 3. Generate tile matrix using pp.add_tile_matrix with paired-insertion counting strategy. 4. Perform spectral embedding dimension reduction using tl.spectral with cosine similarity metric. 5. Generate UMAP visualization using tl.umap on spectral eigenvectors. 6. Perform clustering using tl.leiden with default resolution parameter. 7. Call peaks using tl.macs3 in pseudo-bulk mode grouped by cluster assignment. 8. Merge overlapping peaks using tl.merge_peaks and compare cluster assignments and UMAP coordinates to tutorial reference.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/docker-windows-tutorial-0.png` | figure | False |
| `figures/docker-windows-tutorial-1.png` | figure | False |
| `figures/docker-windows-tutorial-2.png` | figure | False |
| `figures/func+export_coverage.svg` | figure | False |
| `figures/func+import_data.svg` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog or version specification found
- No tutorial or reference results document cited in the provided section text

## Domain Knowledge
- Paired-end fragment counting requires importing ATAC fragments as coordinate pairs with both start and end positions; the default counting strategy in SnapATAC2 v2.9.0+ is paired-insertion mode, which counts each insertion site separately.
- Spectral embedding with cosine similarity in SnapATAC2 achieves linear time and space complexity and returns eigenvectors weighted by eigenvalues; the resulting coordinates are suitable for direct UMAP visualization without manual eigenvector selection.
- Leiden clustering in SnapATAC2 is resolution-sensitive; cluster numbers scale with resolution parameter and should be validated against known cell-type markers or reference annotations for PBMC datasets.
- Peak calling in pseudo-bulk mode aggregates fragments by cluster assignment before invoking tl.macs3; merged peaks from tl.merge_peaks represent consensus accessible regions and are the standard input for downstream differential accessibility testing.
- Tutorial reproducibility requires matching exact parameter defaults and dataset versions; pbmc10k_multiome dataset download is automated via snapatac2.datasets and includes both ATAC and RNA modalities.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: tl.macs3, tl.merge_peaks, Peak coordinates and statistics table from tl.macs3, Merged peak set with cluster reproducibility metrics.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] Can the SnapATAC2 pipeline successfully process the pbmc10k_multiome dataset through fragment import, tile matrix generation, spectral embedding, leiden clustering, and peak calling to reproduce documented cluster assignments?: 'End-to-end analysis pipeline for single-cell ATAC-seq data, including preprocessing, dimension reduction, clustering, data integration, peak calling'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] SnapATAC2 provides an end-to-end analysis pipeline for single-cell ATAC-seq data that includes preprocessing, dimension reduction, clustering, data integration, and peak calling steps.: 'End-to-end analysis pipeline for single-cell ATAC-seq data, including preprocessing, dimension reduction, clustering, data integration, peak calling'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] pbmc10k_multiome dataset from snapatac2.datasets: 'datasets.pbmc10k_multiome'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] AnnData object with imported fragments and filtered cells: 'pp.import_fragments'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] AnnData object with tile count matrix: 'pp.add_tile_matrix'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] Spectral embedding coordinates saved in .obsm: 'tl.spectral'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] UMAP layout coordinates in .obsm['X_umap']: 'tl.umap'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] Cluster labels in .obs['leiden']: 'tl.leiden'
- `ev_009` from `agent2_synthesis` (agent2_traced): [methods] Peak coordinates and statistics table from tl.macs3: 'tl.macs3'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] Merged peak set with cluster reproducibility metrics: 'tl.merge_peaks'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] SnapATAC2: 'SnapATAC2: A Python/Rust package for single-cell epigenomics analysis'
- `ev_012` from `agent2_synthesis` (agent2_traced): [methods] Python: 'A Python/Rust package for single-cell epigenomics analysis'
- `ev_013` from `agent2_synthesis` (agent2_traced): [methods] pp.import_fragments: 'pp.import_fragments'
- `ev_014` from `agent2_synthesis` (agent2_traced): [methods] pp.add_tile_matrix: 'pp.add_tile_matrix'
- `ev_015` from `agent2_synthesis` (agent2_traced): [methods] tl.spectral: 'tl.spectral'
- `ev_016` from `agent2_synthesis` (agent2_traced): [methods] tl.umap: 'tl.umap'
- `ev_017` from `agent2_synthesis` (agent2_traced): [methods] tl.leiden: 'tl.leiden'
- `ev_018` from `agent2_synthesis` (agent2_traced): [methods] tl.macs3: 'tl.macs3'
- `ev_019` from `agent2_synthesis` (agent2_traced): [methods] tl.merge_peaks: 'tl.merge_peaks'
- `ev_020` from `agent2_synthesis` (agent2_traced): [methods] Leiden: 'tl.leiden for clustering'
- `ev_021` from `agent2_synthesis` (agent2_traced): [methods] UMAP: 'tl.umap for embeddings'
- `ev_022` from `agent2_synthesis` (agent2_traced): [discussion] No changelog or version specification found: 'No changelog found.'
- `ev_023` from `agent2_synthesis` (agent2_traced): [discussion] No tutorial or reference results document cited in the provided section text: 'No changelog found.'

## Evaluation Strategy
### Direct Checks
- verify file exists: pbmc10k_multiome dataset accessible via snapatac2.datasets.pbmc10k_multiome
- script_runs: SnapATAC2 pipeline execution script completes without errors (fragment import → tile matrix → spectral embedding → leiden clustering → macs3 peak calling)
- file_exists: output AnnData object (.h5ad) or equivalent structured artifact generated after full pipeline
- field_present: cluster assignments present in output object (e.g., .obs['leiden'] or equivalent clustering annotation column)
- file_format_is: output object in HDF5-backed AnnData format or native SnapATAC2 format
- output_matches_reference: UMAP layout coordinates byte-for-byte or robust to random seed variation — clarify whether tutorial provides fixed reference embeddings or multiple valid outcomes
- value_in_range: cluster count (number of distinct leiden clusters) falls within expected range documented in tutorial (if range is specified)
- contains_substring: peak calling output (BED or equivalent) contains expected genomic coordinates and peak statistics fields

### Expert Review
- biological plausibility of cluster assignments: do recovered clusters correspond to expected cell types (e.g., T cells, B cells, monocytes, etc.) as described in tutorial or original pbmc10k_multiome analysis?
- quality of spectral embedding and UMAP visualization: do clusters show expected separation and structure consistent with tutorial figures or reference publication?
- peak calling quality: are called peaks consistent with known open chromatin regions and do they show expected enrichment patterns (e.g., TSS proximity, motif content)?
- parameter sensitivity: does pipeline produce substantially different cluster assignments or peak calls under reasonable parameter variations (e.g., n_components, resolution, min_peak_size)? — note if reproducibility is brittle or robust

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** heavy

## Methodology Summary
1. Load the pbmc10k_multiome dataset from snapatac2.datasets public repository.
2. Import ATAC fragments into AnnData using pp.import_fragments with paired-end mode and default paired-insertion counting.
3. Generate tile-based count matrix using pp.add_tile_matrix across the genome.
4. Apply matrix-free spectral embedding using tl.spectral with cosine similarity to obtain low-dimensional coordinates.
5. Compute UMAP projection from spectral eigenvectors using tl.umap for visualization.
6. Cluster cells using tl.leiden algorithm on spectral coordinates.
7. Call peaks in pseudo-bulk mode grouped by cluster assignment using tl.macs3.
8. Merge overlapping peaks using tl.merge_peaks to produce final consensus peak set.
9. Validation: compare generated cluster labels and UMAP layout coordinates to reference tutorial output; report clustering purity and embedding correlation metrics.
10. References: source article (DOI: 10.1038/s41592-023-02139-9)

## Workflow Ports

**Inputs:**

- `pbmc10k_multiome_raw` — pbmc10k_multiome dataset

**Outputs:**

- `anndata_with_clusters` — AnnData with cluster assignments and embeddings
- `peak_table` — Merged peak coordinates and statistics
- `reproduction_metrics` — Cluster and UMAP reproducibility evaluation

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:scverse__SnapATAC2`
- **Synthesized at:** 2026-06-15T19:40:50+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
