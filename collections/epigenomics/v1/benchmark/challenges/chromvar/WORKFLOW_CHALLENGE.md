# Workflow Challenge: `coll_chromvar_workflow`


> chromVAR is an R package that computes bias-corrected deviation scores to identify motifs and genomic annotations associated with variability in chromatin accessibility across cells or samples from ATAC-seq or DNAse-seq data.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

chromVAR takes aligned fragments from ATAC-seq or DNAse-seq experiments and genomic annotations such as motif positions as inputs, then computes for each annotation and each cell or sample a bias-corrected deviation in accessibility from the expected accessibility based on the average of all cells or samples. The package returns a SummarizedExperiment object containing deviation scores and Z-scores that quantify motif-associated variability in chromatin accessibility after preprocessing with filterSamples, filterPeaks, addGCBias, computeExpectations, and getBackgroundPeaks. chromVAR enables ranking and differential analysis of motif usage, supports kmer-based annotation approaches for analyzing chromatin accessibility variability, and provides functions for analyzing annotation relationships such as synergy and correlation within chromatin data. The package was evaluated for single-cell clustering, where kmers+PCA represents the best chromVAR variant for clustering, though SnapATAC outperforms chromVAR for clustering tasks.

## Research questions

- What is the structure and composition of a chromVARDeviations object produced by applying the standard chromVAR preprocessing and motif deviation workflow to the example_counts dataset?
- How can motifs be ranked by their variability in chromatin accessibility across cell populations, and which motifs show statistically significant differential deviation between distinct cell types?
- Does kmer size (6-mer vs 7-mer) affect the magnitude of chromatin accessibility variability scores computed by chromVAR?
- How do getAnnotationCorrelation and getAnnotationSynergy quantify redundancy and synergy between two annotation sets in a chromVARDeviations object?
- How does SnapATAC's clustering performance compare to chromVAR variants (especially kmers+PCA) according to the Huidong Chen et al. benchmark study?

## Methods overview

Load chromVAR ecosystem packages (chromVAR, motifmatchr, SummarizedExperiment, Matrix, BiocParallel) and register serial processing backend. Load bundled example_counts dataset and human genome reference; initialize GC bias calculations using addGCBias(). Filter low-quality samples (min_depth=1500, min_in_peaks=0.15) and reduce peak set to non-overlapping regions using filterPeaks(). Retrieve JASPAR motifs and match to filtered peaks using motifmatchr to generate peak-motif overlap matrix. Compute expected accessibility distribution and generate GC-accessibility-matched background peak sets for normalization. Execute computeDeviations() to produce bias-corrected accessibility deviations and Z-scores for each motif-sample pair. Validation: verify chromVARDeviations object has two assays (deviations, deviationScores), row count equals motif count, column count equals sample count, and deviation score values fall within expected numeric ranges. Load chromVARDeviations object containing bias-corrected motif deviations and z-scores from filtered example ATAC-seq data (10 GM + 10 H1 cells). Apply computeVariability to rank motifs by standard deviation of z-scores across samples; compute bootstrap confidence intervals by resampling cells and test against null hypothesis of variability = 1. Visualize ranked motif variability using plotVariability to identify high-variability motifs across the cell population. Apply differentialDeviations to test for statistically significant differences in bias-corrected deviations between GM and H1 cell types using cell-type annotations in colData. Validation: Verify that variability rankings match expected high-variability motifs (e.g., cell-type-specific TFs) and that differential-deviation p-values are properly computed and < 0.05 for true positives reported in the paper. Load and preprocess example_counts: apply GC bias annotation, filter samples (min_depth=1500, min_in_peaks=0.15), and filter peaks to remove overlaps. Generate 6-mer and 7-mer kmer annotation matrices by scanning all peak sequences against all possible kmers of each length using matchKmers. Compute bias-corrected deviations for each kmer set using computeDeviations, which normalizes against background peak sets matched for GC content and mean accessibility. Compute variability (standard deviation of deviation Z-scores across all samples) for each kmer using computeVariability. Extract and compare summary statistics (mean, median, standard deviation) of variability distributions for 6-mers vs. 7-mers. Validation: confirm that 7-mer variability distribution exhibits higher mean and median scores than 6-mer distribution, consistent with the reported finding that 7-mers provide greater sequence specificity and superior signal for de novo motif assembly. Load chromVARDeviations object containing precomputed bias-corrected deviations and z-scores from prior computeDeviations run Subset annotation matrices to isolate the two annotation sets to be compared (e.g., JASPAR motifs and kmers) Apply getAnnotationCorrelation to compute pairwise Pearson correlations between annotation sets, filtering out low-variability and highly correlated annotations first Apply getAnnotationSynergy to compute z-scores for variability synergy, comparing observed variance for dual-annotated peaks against random subsamples of single-annotation peaks Export correlation matrix and synergy score table as named CSV files with annotation identifiers and statistical measures Validation: Verify correlation matrix is symmetric with values in range [−1, 1], synergy z-scores are real-valued, and all annotation pairs are named and present in both output tables Locate and download the Huidong Chen et al. bioRxiv 739011 preprint and identify the clustering benchmark results table or supplementary data file. Extract clustering accuracy metrics (NMI, ARI, purity, or equivalent) for chromVAR kmers+PCA, SnapATAC, and all other methods across each reported dataset. Construct a method-by-dataset matrix where rows are methods (chromVAR kmers+PCA, SnapATAC, others), columns are datasets, and cells contain accuracy scores. Calculate summary statistics per method: mean accuracy, median accuracy, and per-dataset rank order to quantify relative performance. Validation: Verify that the table confirms the two key findings: (1) SnapATAC achieves higher mean clustering accuracy than chromVAR variants, and (2) chromVAR kmers+PCA achieves higher accuracy than other chromVAR configurations (motifs, cis-regions, etc.).

**Domain:** genomics

**Techniques:** dimensionality-reduction, clustering, enrichment-analysis

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** chromVAR is an R package for the analysis of sparse chromatin accessibility data from single cell or bulk ATAC or DNAse-seq data. _[grounded: chromVAR_system]_
- **(finding)** The chromVAR package aims to identify motifs or other genomic annotations associated with variability in chromatin accessibility between individual cells or samples. _[grounded: chromVAR_system]_
- **(finding)** Using kmers plus PCA appears to be the best variant of chromVAR for clustering. _[grounded: chromVAR_system]_
- **(finding)** SnapATAC outperforms chromVAR for the clustering tasks evaluated in the paper. _[grounded: chromVAR_system]_
- **(finding)** The main computeDeviations function from chromVAR requires an object storing what peaks overlap what motifs or other annotations. _[grounded: chromVAR_system]_
- **(finding)** chromVAR includes functions for creating annotation objects from a set of motifs or kmers. _[grounded: chromVAR_system]_
- **(finding)** chromVAR has a function to make it easy to read in motifs from the JASPAR database. _[grounded: chromVAR_system]_
- **(finding)** The companion package chromVARmotifs includes PWMs from a couple different sources that can be used with motifmatchr and chromVAR. _[grounded: chromVAR_system]_
- **(finding)** The matchMotifs method returns a SummarizedExperiment with a matrix indicating what peaks contain what motifs. _[grounded: comp_matchMotifs]_
- **(finding)** The matchKmers function in chromVAR can be used to make an annotation matrix for all kmers of a given length. _[grounded: chromVAR_system]_
- **(finding)** The getCisGroups function annotates peaks based on chromosomal location. _[grounded: comp_getCisGroups]_
- **(finding)** With default parameters, getCisGroups takes the first 25 peaks in a chromosome and considers those a group, then moves 10 peaks down and groups 25 peaks together. _[grounded: comp_getCisGroups]_
- **(finding)** The getAnnotations function can be used to read annotations in BED files into the appropriate SummarizedExperiment with matrix. _[grounded: tool_SummarizedExperiment]_
- **(finding)** chromVAR includes a function getCounts for reading in fragment counts from bam or bed files. _[grounded: chromVAR_system]_
- **(finding)** With paired end data, fragments are counted once if either or both ends of the fragment map to a peak.
- **(finding)** For single end data, a fragment is counted if the 5 prime end maps to the peak.
- **(finding)** The addGCBias function returns an updated RangedSummarizedExperiment with a new rowData column named bias. _[grounded: comp_addGCBias]_
- **(finding)** The filterSamples function filters out samples with insufficient reads or a low proportion of reads in peaks. _[grounded: comp_filterSamples]_
- **(finding)** Two parameters used for filtering are min_in_peaks and min_depth.
- **(finding)** The min_in_peaks parameter is set to 0.5 times the median proportion of fragments in peaks when not provided.
- **(finding)** The min_depth parameter is set to the maximum of 500 or 10 percent of the median library size when not provided.
- **(finding)** The filterPeaks function reduces the peak set to non-overlapping peaks keeping the peak with higher counts for peaks that overlap. _[grounded: comp_filterPeaks]_
- **(finding)** The computeDeviations function has two required inputs: object and annotations. _[grounded: comp_computeDeviations]_
- **(finding)** The first argument to computeDeviations should be a RangedSummarizedExperiment with a counts assay storing fragment counts per peak per cell or sample. _[grounded: comp_computeDeviations]_
- **(finding)** The second argument to computeDeviations should be a RangedSummarizedExperiment with a motif_matches or annotation_matches assay. _[grounded: comp_computeDeviations]_
- **(finding)** The output from computeDeviations is a chromVARDeviations object that inherits from RangedSummarizedExperiment. _[grounded: comp_computeDeviations]_
- **(finding)** The deviations are the bias corrected deviations in accessibility.
- **(finding)** The deviationScores are the Z-scores for each bias corrected deviation.
- **(finding)** Background peaks are peaks that are similar to a peak in GC content and average accessibility.
- **(finding)** The computeExpectations function calculates the expectation in alternate ways. _[grounded: comp_computeExpectations]_
- **(finding)** By default, computeExpectations computes the expected fraction of reads per peak as the total fragments per peak across all samples divided by total reads in peaks in all samples. _[grounded: comp_computeExpectations]_
- **(finding)** When norm is set to TRUE, the expectation will be the average fraction of reads in a peak across the cells.
- **(finding)** Setting norm to TRUE is not recommended for single cell applications as cells with very few reads will have a large impact.
- **(finding)** chromVAR computes for each annotation and each cell or sample a bias corrected deviation in accessibility from the expected accessibility. _[grounded: chromVAR_system]_
- **(finding)** It is recommended to use fixed-width, non-overlapping peaks for chromVAR. _[grounded: chromVAR_system]_
- **(finding)** A peak width of 250 to 500 bp is recommended for chromVAR. _[grounded: chromVAR_system]_
- **(finding)** For single cell data analysis, it can make sense to use peaks derived from bulk ATAC or DNAse-seq data.
- **(finding)** The getPeaks function reads in peaks as a GenomicRanges object.
- **(finding)** The readNarrowpeaks function reads in peak files, resizes peaks to a given size, and removes overlapping peaks. _[grounded: chromVAR_system]_
- **(finding)** The getCounts function returns a chromVARCounts object with a Matrix of fragment counts per sample or cell for each peak. _[grounded: comp_getCounts]_
- **(finding)** The Matrix package is used to store sparse matrices if the matrix is sparse.
- **(finding)** If RG tags are not used and each bam file represents an individual sample, the by_rg argument should be set to FALSE.
- **(finding)** The computeVariability function returns a data frame that contains the variability (standard deviation of the z scores) across all cell or samples for a set of peaks. _[grounded: comp_computeVariability]_
- **(finding)** The computeVariability function returns bootstrap confidence intervals for variability by resampling cells or samples. _[grounded: comp_computeVariability]_
- **(finding)** The computeVariability function returns a p-value for the variability being greater than the null hypothesis of 1. _[grounded: comp_computeVariability]_
- **(finding)** The deviationsTsne function performs t-SNE and returns a data frame with the results. _[grounded: comp_deviationsTsne]_
- **(finding)** With hundreds of cells, a perplexity of around 30 to 50 might make sense for t-SNE.
- **(finding)** The getJasparMotifs function fetches motifs from the JASPAR database. _[grounded: dataset_JASPAR]_
- **(finding)** The getJasparMotifs function by default gets human motifs from JASPAR core database. _[grounded: dataset_JASPAR]_
- **(finding)** The default p.cutoff value for motif matching is 0.00005.
- **(finding)** The computeDeviations function returns a SummarizedExperiment with two assays. _[grounded: comp_computeDeviations]_
- **(finding)** The first assay from computeDeviations contains bias corrected deviations in accessibility for each set of peaks per cell or sample. _[grounded: comp_computeDeviations]_
- **(finding)** The second assay from computeDeviations gives the deviation Z-score. _[grounded: comp_computeDeviations]_
- **(finding)** The deviationsCovariability function returns a normalized covariance between the bias corrected deviations of any pair of annotations. _[grounded: comp_deviationsCovariability]_
- **(finding)** The assembleKmers function builds de novo motifs using the kmer deviation results. _[grounded: comp_assembleKmers]_
- **(finding)** The pwmDistance function returns a list with three matrices: dist, strand, and offset. _[grounded: comp_pwmDistance]_
- **(finding)** chromVAR includes a function for computing the synergy between pairs of annotations or motifs. _[grounded: chromVAR_system]_
- **(finding)** Synergy is defined as the excess variability of chromatin accessibility for peaks sharing both motifs compared to a random sub-sample of peaks with one motif.

**Speculative claims (excluded from scoring):**
- **(finding)** chromVAR may be complementary to other methods as a way of annotating TF motif usage in cells and clusters. _[grounded: chromVAR_system]_

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- SnapATAC as alternative to chromVAR for clustering
- readNarrowpeaks can be used instead of getPeaks for narrowpeak format
- matchKmers can be used instead of matchMotifs for kmer-based annotations
- getMatrixSet from TFBSTools can be used instead of getJasparMotifs

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- For Windows, MulticoreParam will not work; use SnowParam instead

## Steps

### Step `task_001`
- Title: Reproduce chromVAR core deviation computation on example ATAC-seq data
- Task kind: `reproduction`
- Task: Execute the complete chromVAR preprocessing and deviation computation pipeline on the bundled example_counts dataset: filter samples and peaks, add GC bias, compute expectations and background peaks, then compute bias-corrected deviations using JASPAR motif annotations. Validate the output chromVARDeviations object for correct structure, dimensions, and deviation score ranges.
- Inputs:
  - example_counts: bundled chromVAR example dataset (RangedSummarizedExperiment with counts assay)
  - BSgenome.Hsapiens.UCSC.hg19: human genome sequence reference required for GC bias and motif matching
- Expected outputs:
  - chromVARDeviations object: RangedSummarizedExperiment with two assays (deviations and deviationScores) containing bias-corrected accessibility deviations and Z-scores for each motif (rows) and sample (columns)
  - Deviations matrix: numeric matrix of bias-corrected deviations in accessibility for each motif-sample pair, accessible via deviations()
  - DeviationScores matrix: numeric matrix of Z-scores for bias-corrected deviations, accessible via deviationScores()
- Tools: chromVAR, R, motifmatchr, SummarizedExperiment, Matrix, BiocParallel, BSgenome.Hsapiens.UCSC.hg19
- Landmark output files: example_counts_gc_bias.rds, counts_filtered_samples.rds, counts_filtered_peaks.rds, jaspar_motifs.rds, motif_matches.rds, background_peaks.rds

### Step `task_002`
- Depends on: `task_001`
- Title: Reproduce variability ranking of JASPAR motifs across GM and H1 cell lines
- Task kind: `reproduction`
- Task: Compute variability rankings and differential-deviation statistics for motifs using a chromVARDeviations object derived from the example 10-GM / 10-H1 dataset. Output a ranked variability table and a differential-deviation results table with per-motif statistics comparing cell types.
- Inputs:
  - chromVARDeviations object (dev) containing bias-corrected deviations and z-scores for JASPAR motifs matched to filtered peaks from 10 GM + 10 H1 example cells
- Expected outputs:
  - Ranked variability data frame with motif names, standard deviation of z-scores, bootstrap confidence intervals, and p-values for variability > 1
  - Differential-deviations results table with per-motif statistics comparing GM vs H1 cell types (p-values, test statistics)
- Tools: chromVAR, R, SummarizedExperiment
- Landmark output files: variability_table.csv, differential_deviations_table.csv, variability_plot.png
- Primary expected artifact: `variability_and_differential_deviations_results.csv`

### Step `task_003`
- Depends on: `task_001`
- Title: Reproduce the finding that 7-mers yield higher variability than 6-mers in chromVAR kmer analysis
- Task kind: `reproduction`
- Task: Assemble 6-mer and 7-mer kmer annotations from filtered peak regions using assembleKmers, compute chromatin accessibility deviations for each kmer set, and produce a summary table comparing mean and median variability scores between kmer sizes to validate the reported advantage of 7-mers over 6-mers.
- Inputs:
  - example_counts dataset (SummarizedExperiment with peak-by-sample count matrix and rowRanges)
  - BSgenome.Hsapiens.UCSC.hg19 reference genome sequence
- Expected outputs:
  - Numeric summary table with mean, median, and standard deviation of kmer variability scores for 6-mers and 7-mers
  - Kmer deviation object for 6-mers (RangedSummarizedExperiment with deviations and deviationScores assays)
  - Kmer deviation object for 7-mers (RangedSummarizedExperiment with deviations and deviationScores assays)
- Tools: chromVAR, R, motifmatchr, SummarizedExperiment, Matrix, BiocParallel, BSgenome.Hsapiens.UCSC.hg19
- Landmark output files: kmer6_annotation_matrix.rds, kmer6_deviations.rds, kmer6_variability_scores.csv, kmer7_annotation_matrix.rds, kmer7_deviations.rds, kmer7_variability_scores.csv
- Primary expected artifact: `kmer_variability_comparison_summary.csv`

### Step `task_004`
- Depends on: `task_001`
- Title: Reconstruct the annotation synergy and correlation computation between chromVAR annotation sets
- Task kind: `component_reconstruction`
- Task: Compute correlation and synergy scores between two annotation sets (e.g., JASPAR motifs and kmers) using a chromVARDeviations object, outputting a named correlation matrix and a synergy score table to assess redundancy and cooperative binding between motifs.
- Inputs:
  - chromVARDeviations object with computed deviations and z-scores, and rowData containing annotation metadata (fractionMatches, fractionBackgroundOverlap)
  - Filtered peak count matrix (RangedSummarizedExperiment) with GC bias and sample/cell metadata
  - Two annotation matrices (e.g., motif and kmer matches) stored as assays in separate SummarizedExperiment objects or subset from the same object
- Expected outputs:
  - Named correlation matrix (CSV format) with annotation pair identifiers as row and column names and Pearson correlation coefficients as values, rows ordered by decreasing correlation magnitude
  - Synergy score table (CSV format) with columns: annotation_pair, z_score, p_value, and variability_excess; one row per unique pairwise combination
- Tools: chromVAR, R, SummarizedExperiment, Matrix
- Landmark output files: annotation_subset_indices.txt, correlation_matrix_raw.csv, synergy_zscores.csv
- Primary expected artifact: `correlation_synergy_results.csv`

### Step `task_005`
- Depends on: `task_002`
- Title: Reproduce the clustering performance comparison: kmers+PCA vs SnapATAC on single-cell ATAC-seq
- Task kind: `reproduction`
- Task: Retrieve the clustering accuracy benchmark table from the Huidong Chen et al. preprint (bioRxiv 739011) comparing chromVAR kmers+PCA, SnapATAC, and other methods across datasets, and produce a structured TSV summary showing method-by-dataset clustering metrics with performance rankings.
- Inputs:
  - bioRxiv preprint 739011 (Huidong Chen et al.) — clustering benchmark results table or supplementary file
- Expected outputs:
  - Structured TSV table with methods as rows, datasets as columns, and clustering accuracy metrics (NMI, ARI, or purity) as cell values
  - Summary statistics (mean, median accuracy per method; per-dataset ranking) demonstrating SnapATAC superiority and chromVAR kmers+PCA as best chromVAR variant
- Tools: SnapATAC, chromVAR, R
- Landmark output files: raw_benchmark_table_extracted.txt, clustering_metrics_matrix.tsv, method_summary_statistics.tsv
- Primary expected artifact: `clustering_benchmark_metrics.tsv`

## Final expected outputs

- `Numeric summary table with mean, median, and standard deviation of kmer variability scores for 6-mers and 7-mers` (type: file, tolerance: hash)
- `Kmer deviation object for 6-mers (RangedSummarizedExperiment with deviations and deviationScores assays)` (type: file, tolerance: hash)
- `Kmer deviation object for 7-mers (RangedSummarizedExperiment with deviations and deviationScores assays)` (type: file, tolerance: hash)
- `Named correlation matrix (CSV format) with annotation pair identifiers as row and column names and Pearson correlation coefficients as values, rows ordered by decreasing correlation magnitude` (type: file, tolerance: hash)
- `Synergy score table (CSV format) with columns: annotation_pair, z_score, p_value, and variability_excess; one row per unique pairwise combination` (type: file, tolerance: hash)
- `Structured TSV table with methods as rows, datasets as columns, and clustering accuracy metrics (NMI, ARI, or purity) as cell values` (type: file, tolerance: hash)
- `Summary statistics (mean, median accuracy per method; per-dataset ranking) demonstrating SnapATAC superiority and chromVAR kmers+PCA as best chromVAR variant` (type: file, tolerance: hash)

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

- **Composition modularity:** flat

- **Abstraction level:** concrete

- **Orchestration planning:** static

- **Data transport:** in_memory

- **Characterisation confidence:** inferred


## Submission

Produce two artifacts in your output directory:

1. The output files at the paths declared under **Final expected outputs**.
2. An `attempt.json` matching the schema below.
3. _(Optional)_ `attempt_metrics.json` with `wall_time_s`, `total_tokens`, `cost_usd` for the EFFICIENCY rubric.

### `attempt.json` schema

```json
{
  "workflow_id": "coll_chromvar_workflow",
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
    "Numeric summary table with mean, median, and standard deviation of kmer variability scores for 6-mers and 7-mers": "<locator>",
    "Kmer deviation object for 6-mers (RangedSummarizedExperiment with deviations and deviationScores assays)": "<locator>",
    "Kmer deviation object for 7-mers (RangedSummarizedExperiment with deviations and deviationScores assays)": "<locator>",
    "Named correlation matrix (CSV format) with annotation pair identifiers as row and column names and Pearson correlation coefficients as values, rows ordered by decreasing correlation magnitude": "<locator>",
    "Synergy score table (CSV format) with columns: annotation_pair, z_score, p_value, and variability_excess; one row per unique pairwise combination": "<locator>",
    "Structured TSV table with methods as rows, datasets as columns, and clustering accuracy metrics (NMI, ARI, or purity) as cell values": "<locator>",
    "Summary statistics (mean, median accuracy per method; per-dataset ranking) demonstrating SnapATAC superiority and chromVAR kmers+PCA as best chromVAR variant": "<locator>"
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
