# Workflow Challenge: `coll_snapatac2_workflow`


> SnapATAC2 is a flexible, scalable Python/Rust framework for single-cell epigenomics analysis that scales to over 10 million cells and provides an end-to-end ATAC-seq pipeline.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

Reproduces 2 reported results: SnapATAC2 is capable of scaling to more than 10 million cells, demonstrating its capacity to handle very large single-cell datasets. SnapATAC2 provides an end-to-end analysis pipeline for single-cell ATAC-seq data that includes preprocessing, dimension reduction, clustering, data integration, and peak calling steps. Reconstructs 3 described mechanisms (described in the paper but not separately evaluated there): SnapATAC2 provides pp.make_fragment_file as a preprocessing tool for converting BAM files to fragment files. SnapATAC2 provides a pp.add_tile_matrix function that generates count matrices from fragment data as part of its matrix operation workflow for single-cell ATAC-seq analysis. SnapATAC2 includes tl.motif_enrichment for motif analysis as part of its single-cell ATAC-seq analysis pipeline.

## Research questions

- Does the matrix-free spectral embedding algorithm (tl.spectral) in SnapATAC2 achieve linear time and space complexity when applied to datasets of 10 million or more cells?
- How does the pp.make_fragment_file function convert a coordinate-sorted BAM file into a compressed fragment file?
- How does the paired_insertion counting strategy in pp.add_tile_matrix process fragment data to generate a tile-based count matrix?
- Can the SnapATAC2 pipeline successfully process the pbmc10k_multiome dataset through fragment import, tile matrix generation, spectral embedding, leiden clustering, and peak calling to reproduce documented cluster assignments?
- What output does the motif enrichment function (tl.motif_enrichment) produce when applied to differentially accessible peaks?

## Methods overview

Load single-cell count matrix with ≥10 million cells into SnapATAC2-compatible format (CSR sparse matrix). Execute tl.spectral with default cosine similarity metric and capture wall-clock time using system timer. Monitor peak memory consumption throughout spectral decomposition using memory_profiler or psutil. Verify returned eigenvectors are weighted by eigenvalues (default Release 2.3.0 behavior). Analyze runtime and peak memory scaling behavior against cell count to validate claimed linear time and space complexity. Validation: runtime and memory usage scale sublinearly (slope <1) when plotted on log-log scale against cell count, confirming O(n) complexity for both metrics. References: source article (DOI: 10.1038/s41592-023-02139-9) Validate input BAM file is coordinate-sorted and properly formatted. Invoke pp.make_fragment_file with appropriate parameters (source='10x' for 10X BAM; default for standard BAM). Generate compressed fragment file with fragment coordinates (chrom, start, end), cell barcodes, and read counts. Extract and store QC metrics including duplication rate and read count statistics. Validation: confirm fragment file is non-empty, contains all expected BED fields, and QC metrics are accessible and within expected ranges for the dataset. References: source article (DOI: 10.1038/s41592-023-02139-9) Load backed AnnData object with fragment data stored in .obsm array Apply pp.add_tile_matrix with paired_insertion counting strategy to genomic tiles Extract count matrix dimensions and validate shape consistency with tile coordinates Compute sparsity and distribution statistics of paired-insertion counts across cells and tiles Validation: verify that matrix dimensions match expected tile count and that paired-insertion entries are non-zero and consistent with biological signal distribution References: source article (DOI: 10.1038/s41592-023-02139-9) Load the pbmc10k_multiome dataset from snapatac2.datasets public repository. Import ATAC fragments into AnnData using pp.import_fragments with paired-end mode and default paired-insertion counting. Generate tile-based count matrix using pp.add_tile_matrix across the genome. Apply matrix-free spectral embedding using tl.spectral with cosine similarity to obtain low-dimensional coordinates. Compute UMAP projection from spectral eigenvectors using tl.umap for visualization. Cluster cells using tl.leiden algorithm on spectral coordinates. Call peaks in pseudo-bulk mode grouped by cluster assignment using tl.macs3. Merge overlapping peaks using tl.merge_peaks to produce final consensus peak set. Validation: compare generated cluster labels and UMAP layout coordinates to reference tutorial output; report clustering purity and embedding correlation metrics. References: source article (DOI: 10.1038/s41592-023-02139-9) Load differentially accessible peaks from tl.diff_test output into SnapATAC2 data structure. Retrieve CIS-BP motif database using datasets.cis_bp, obtaining position-weight matrices and motif identifiers. Scan peak sequences for motif occurrences using SnapATAC2's integrated motif scanner. Compute enrichment statistics (scores and p-values) by comparing observed motif frequencies in peaks to background or genome-wide frequencies. Validation: verify output table contains all required columns (motif_id, enrichment_score, p_value) with no missing values, and that p-values are properly computed statistics between 0 and 1. References: source article (DOI: 10.1038/s41592-023-02139-9)

**Domain:** multi-omics

**Techniques:** clustering, dimensionality-reduction, batch-correction, normalization

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** SnapATAC2 can scale to more than 10 million cells. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 features a matrix-free spectral embedding algorithm applicable to single-cell ATAC-seq, RNA-seq, Hi-C, and methylation data. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 provides an efficient and scalable co-embedding algorithm for single-cell multi-omics data integration. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 provides an end-to-end analysis pipeline for single-cell ATAC-seq data including preprocessing, dimension reduction, clustering, data integration, and peak calling. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.9.0 supports Python 3.13 and 3.14. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.9.0 improves the precision of p values in tl.motif_enrichment. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.9.0 adds pl.coverage for quick visualization of signal coverage. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.9.0 adds tl.leiden_sweep for optimizing the resolution parameter in Leiden clustering. _[grounded: snapatac2_system]_
- **(finding)** In SnapATAC2 version 2.9.0, pp.import_data is removed in favor of pp.import_fragments. _[grounded: snapatac2_system]_
- **(finding)** In SnapATAC2 version 2.9.0, h5ad files are compressed using zstandard by default. _[grounded: snapatac2_system]_
- **(finding)** In SnapATAC2 version 2.9.0, pp.import_fragments now treats fragment files as paired-end by default. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.8.0 implements BPM normalization in ex.export_coverage. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.8.0 adds include_for_norm and exclude_for_norm to ex.export_coverage. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.8.0 makes ex.export_coverage much faster. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.8.0 adds counting_strategy to ex.export_coverage. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.8.0 implements broad peak calling in tl.macs3. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.8.0 adds pp.import_values for importing single base pair values. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.8.0 adds metrics.summary_by_chrom. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.7.1 implements barcode correction algorithms. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.7.1 adds smooth_length to ex.export_coverage. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.7.0 makes pp.make_fragment_file return more QC metrics. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.7.0 computes library-level TSSe in metrics.tsse. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.7.0 adds pp.call_cells to identify nonempty barcodes from raw data. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.7.0 adds pp.recipe_10x_metrics to compute 10X metrics. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.7.0 adds pp.import_contacts to process scHi-C data. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.7.0 implements pseudo-bulk peak calling in tl.macs3. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.7.0 changes the default counting strategy from insertion to paired-insertion in pp.add_tile_matrix, pp.make_peak_matrix, and pp.make_gene_matrix. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.6.4 adds flexibility to pp.make_gene_matrix by allowing the user to change upstream and downstream distances for TSS calculation. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.6.2 adds exclude_chroms argument to metrics.tsse with default value chrM. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.6.1 adds inplace argument to AnnData subset function. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.6.1 changes tl.spectral to use only unique TSSs instead of all TSSs from GTF files. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.6.0 adds counting_strategy argument to pp.add_tile_matrix, pp.make_peak_matrix, and pp.make_gene_matrix. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.5.3 adds count_frag_as_reads argument to pp.make_tile_matrix, pp.make_peak_matrix, and pp.make_gene_matrix. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.5.2 supports anndata v0.10. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.5.2 adds ex.export_coverage to export coverage tracks as bedGraph or bigWig files. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.5.2 adds min_frag_size and max_frag_size parameters to pp.add_tile_matrix, pp.make_peak_matrix, and pp.make_gene_matrix. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.5.1 renames ex.export_bed to ex.export_fragments. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.5.0 breaks compatibility by storing fragments in .obsm['fragment_single'] or .obsm['fragment_paired']. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.5.0 renames tl.call_peaks to tl.macs3. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.5.0 adds tl.merge_peaks to perform peak merging. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.4.0 adds multiprocessing support to preprocessing functions like pp.import_data. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.4.0 adds pp.scanorama_integrate for batch correction using Scanorama. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.3.1 adds pp.add_frip to calculate the fraction of reads in peaks. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.3.0 changes the default similarity metric to cosine similarity in tl.spectral. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.3.0 significantly improves scalability of tl.spectral with cosine similarity having linear time and space complexity. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.3.0 weights returned eigenvectors by eigenvalues in tl.spectral. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.3.0 implements tl.multi_spectral for dimension reduction on multiple modalities simultaneously. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.3.0 removes pp.call_doublets and pl.scrublet, with pp.scrublet now automatically calling doublets. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.3.0 renames gff_file argument to gene_anno in pp.import_data and pp.make_gene_matrix. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.2.0 removes create_dataset function. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.2.0 renames storage argument to file in AnnData IO functions. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.2.0 renames mode to backed in .read(). _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.1.1 adds tl.motif_enrichment to perform motif enrichment analysis. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.1.0 renames pp.make_tile_matrix to pp.add_tile_matrix. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.1.0 redesigns snapatac2.genome with a new Genome class for automatic download of gene annotation files. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.1.0 renames group_by to groupby throughout the package. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.1.0 adds tl.diff_test to identify differentially accessible regions. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.1.0 adds tl.make_fragment_file to convert BAM files to fragment files. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 version 2.1.0 adds ex.export_bigwig to generate bigwig files. _[grounded: snapatac2_system]_
- **(finding)** SnapATAC2 was first officially released as version 2.0.0 on July 7, 2022. _[grounded: snapatac2_system]_

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- kd-tree as default algorithm in pp.knn instead of pynndescent

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- hdf5plugin is needed to read/write h5ad files if using the anndata python package when zstandard compression is used

## Steps

### Step `task_001`
- Title: Reproduce the scalability benchmark of spectral embedding to 10M+ cells
- Task kind: `reproduction`
- Task: Run SnapATAC2's matrix-free spectral embedding algorithm (tl.spectral) on a large-scale dataset of 10 million or more cells and measure wall-clock execution time and peak memory consumption to validate the reported linear time and space complexity.
- Inputs:
  - Single-cell count matrix (≥10 million cells, any supported format: .h5ad, .mtx, or generated from raw fragment/BAM files)
- Expected outputs:
  - Wall-clock execution time (in seconds) for tl.spectral on ≥10 million cell dataset
  - Peak memory usage (in GB) during spectral embedding computation
  - Computational complexity analysis report (text or figure) confirming linear time and space behavior
- Tools: SnapATAC2, Python, Rust
- Landmark output files: time_measurements.csv, memory_profile.txt, complexity_plot.png
- Primary expected artifact: `spectral_complexity_report.txt`

### Step `task_002`
- Title: Reconstruct the BAM-to-fragment-file preprocessing step using pp.make_fragment_file
- Task kind: `component_reconstruction`
- Task: Convert a coordinate-sorted BAM file to a compressed fragment file using SnapATAC2's pp.make_fragment_file function, producing a valid BED or BED.gz file with proper fragment coordinates and metadata.
- Inputs:
  - Coordinate-sorted BAM file
- Expected outputs:
  - Compressed fragment file (BED.gz or .bed.zst) with fragment coordinates, barcodes, and QC metrics
- Tools: SnapATAC2, Python, Rust
- Landmark output files: fragments.bed.gz, qc_metrics.txt
- Primary expected artifact: `fragments.bed.gz`

### Step `task_003`
- Depends on: `task_002`
- Title: Reconstruct tile-matrix generation with paired-insertion counting strategy using pp.add_tile_matrix
- Task kind: `component_reconstruction`
- Task: Starting from a backed AnnData object containing single-cell ATAC-seq fragment data, generate a tile-based count matrix using paired-insertion counting strategy and verify the output matrix has the expected dimensions and non-zero entries.
- Inputs:
  - Backed AnnData object with fragment data in .obsm
- Expected outputs:
  - Count matrix with tile coordinates and paired-insertion counts
  - Matrix dimensions (n_cells × n_tiles) and sparsity statistics
- Tools: SnapATAC2, Python
- Landmark output files: tile_coordinates.bed, count_matrix_shape.txt, nonzero_entries_distribution.csv
- Primary expected artifact: `tile_matrix_metrics.csv`

### Step `task_004`
- Title: Reproduce the end-to-end ATAC-seq analysis pipeline on the pbmc10k_multiome dataset
- Task kind: `reproduction`
- Task: Execute the complete SnapATAC2 analysis pipeline on the pbmc10k_multiome dataset, from fragment import through peak calling with tl.macs3, and reproduce the reported cluster assignments and UMAP layout documented in the SnapATAC2 tutorial.
- Inputs:
  - pbmc10k_multiome dataset from snapatac2.datasets
- Expected outputs:
  - AnnData object with imported fragments and filtered cells
  - AnnData object with tile count matrix
  - Spectral embedding coordinates saved in .obsm
  - UMAP layout coordinates in .obsm['X_umap']
  - Cluster labels in .obs['leiden']
  - Peak coordinates and statistics table from tl.macs3
  - Merged peak set with cluster reproducibility metrics
- Tools: SnapATAC2, Python, pp.import_fragments, pp.add_tile_matrix, tl.spectral, tl.umap, tl.leiden, tl.macs3, tl.merge_peaks, Leiden, UMAP
- Landmark output files: pbmc10k_multiome_imported.h5ad, pbmc10k_multiome_tile_matrix.h5ad, spectral_coordinates.csv, umap_coordinates.csv, leiden_clusters.csv, merged_peaks.bed
- Primary expected artifact: `pbmc10k_multiome_processed.h5ad`

### Step `task_005`
- Depends on: `task_004`
- Title: Reconstruct motif enrichment analysis using tl.motif_enrichment with the CIS-BP dataset
- Task kind: `component_reconstruction`
- Task: Perform motif enrichment analysis on a set of differentially accessible peaks using SnapATAC2's tl.motif_enrichment function with the CIS-BP motif database, generating an output table with motif identifiers, enrichment scores, and p-values.
- Inputs:
  - Differentially accessible peaks (BED format or AnnData object with peak annotations)
  - CIS-BP motif database
  - Reference genome sequence (for motif scanning context)
- Expected outputs:
  - Motif enrichment table with columns: motif_id, motif_name, enrichment_score, p_value, and adjusted_p_value
- Tools: SnapATAC2, tl.motif_enrichment, tl.diff_test, datasets.cis_bp, Python
- Landmark output files: peaks_loaded.log, motif_database_summary.txt, motif_enrichment_results.csv
- Primary expected artifact: `motif_enrichment_results.csv`

## Final expected outputs

- `Wall-clock execution time (in seconds) for tl.spectral on ≥10 million cell dataset` (type: file, tolerance: hash)
- `Peak memory usage (in GB) during spectral embedding computation` (type: file, tolerance: hash)
- `Computational complexity analysis report (text or figure) confirming linear time and space behavior` (type: file, tolerance: hash)
- `Count matrix with tile coordinates and paired-insertion counts` (type: file, tolerance: hash)
- `Matrix dimensions (n_cells × n_tiles) and sparsity statistics` (type: file, tolerance: hash)
- `Motif enrichment table with columns: motif_id, motif_name, enrichment_score, p_value, and adjusted_p_value` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: open — validity-first.** The deterministic match-rubrics above are demoted to *informational*. The binding evaluator is **SCIENTIFIC_VALIDITY** (below). Any scientifically sound method that addresses the research question is valid, and novel findings or unexplored aspects can score positively — **different is not wrong**.

## SCIENTIFIC_VALIDITY (binding for open / mixed tasks)
Open/mixed steps are graded at **EvalTier** granularity by the shared card judge (`runner_checks` llm_judge), not by exact match. The judge assigns one of `reproduced` / `replicated` / `re_analyzed` / `consistent` / `improved`; `consistent` and `re_analyzed` earn partial credit per the tier multipliers (0.60 / 0.75), so a scientifically sound but different result is credited rather than failed. Exact-match rubrics (INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT) are **informational** for these tasks. Three axes the judge weighs:

1. **Addresses the research question** — does the attempt answer it?
2. **Defensible method** — sound, and respects the *Invariants* above?
3. **Results validity** — consistent with the claims, or a valid, evidenced extension? New supported claims earn credit, not penalty.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** loose

- **Composition modularity:** hierarchical

- **Abstraction level:** implicit

- **Orchestration planning:** static

- **Data transport:** file

- **Characterisation confidence:** inferred


## Submission

Produce two artifacts in your output directory:

1. The output files at the paths declared under **Final expected outputs**.
2. An `attempt.json` matching the schema below.
3. _(Optional)_ `attempt_metrics.json` with `wall_time_s`, `total_tokens`, `cost_usd` for the EFFICIENCY rubric.

### `attempt.json` schema

```json
{
  "workflow_id": "coll_snapatac2_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003",
    "task_004",
    "task_005"
  ],
  "intermediate_outputs": {
    "task_001": {
      "<output_name>": "<locator>"
    },
    "task_002": {
      "<output_name>": "<locator>"
    },
    "task_003": {
      "<output_name>": "<locator>"
    },
    "task_004": {
      "<output_name>": "<locator>"
    },
    "task_005": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "Wall-clock execution time (in seconds) for tl.spectral on \u226510 million cell dataset": "<locator>",
    "Peak memory usage (in GB) during spectral embedding computation": "<locator>",
    "Computational complexity analysis report (text or figure) confirming linear time and space behavior": "<locator>",
    "Count matrix with tile coordinates and paired-insertion counts": "<locator>",
    "Matrix dimensions (n_cells \u00d7 n_tiles) and sparsity statistics": "<locator>",
    "Motif enrichment table with columns: motif_id, motif_name, enrichment_score, p_value, and adjusted_p_value": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>",
    "task_004": "<tool_name>",
    "task_005": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
