# Workflow Challenge: `coll_fgsea_workflow`


> fgsea is an R-package for fast preranked gene set enrichment analysis (GSEA) that enables quick and accurate calculation of arbitrarily low GSEA P-values for gene set collections. The package implements an adaptive multi-level split Monte-Carlo scheme for P-value estimation and includes GESECA for gene set co-regulation analysis in multi-conditional data.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

fgsea provides fast and accurate GSEA P-value calculation for gene set collections through an adaptive multi-level split Monte-Carlo scheme. The package supports preranked GSEA on ranked gene lists (e.g., from example pathways and ranks) and includes GESECA, a method for identifying co-regulated gene sets in multi-conditional expression data without requiring explicit sample contrasts. GESECA calculates gene set scores based on the variance of correlated genes within each set and estimates P-values via adaptive multilevel Markov Chain Monte Carlo with gene permutations. The package has been demonstrated on diverse data types including bulk microarray time-course data (GSE200250 Th2 activation), single-cell RNA-seq (GSE116240 atherosclerosis), spatial transcriptomics (10X Visium glioblastoma), and high-resolution spatial data (10X Xenium ovarian cancer), supporting both full-matrix and PCA-reduced expression inputs.

## Research questions

- Can the fgsea package calculate gene set enrichment analysis results on preranked gene lists with arbitrarily low P-values using its default parameters?
- Does fgsea produce consistent enrichment scores and p-values for known pathway activations when applied to normalized gene expression data from a time-course experiment?
- Does dimensionality reduction via PCA to 10 dimensions preserve the pathway enrichment results (pathway scores and p-values) obtained from geseca() analysis on the full-dimensional GSE200250 expression matrix?
- Does the fgsea package enable accurate and rapid calculation of gene set enrichment P-values across arbitrarily low thresholds?
- How does the adaptive multi-level split Monte-Carlo scheme in fgsea adjust P-value precision when the eps parameter is set to zero rather than using a default lower-bound threshold?

## Methods overview

Load fgsea package and bundled example datasets (examplePathways, exampleRanks). Execute fgsea() with preranked gene statistics, pathway collection, and default P-value estimation bounds (eps=1e-10, minSize=15, maxSize=500). Sort results by p-value and extract top upregulated and downregulated pathways. Generate enrichment curve visualization for a single pathway using plotEnrichment(). Create multi-pathway GSEA table heatmap using plotGseaTable() to display running enrichment sums and statistical significance across selected pathways. Validation: fgsea result table must contain pathways with computed pval, padj, ES, and NES fields; enrichment plots must display running sum curves; GSEA table must render top 20 pathways (10 up, 10 down) with gseaParam=0.5. References: GSE200250 (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE200250); GSE116240 (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE116240); GSE14308 (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE14308) Load GSE200250 from NCBI GEO and extract Th2 time-course samples. Apply log-transformation and quantile normalization using limma. Filter duplicates, invalid identifiers, and retain top 12,000 genes by mean expression. Obtain HALLMARK gene sets from MSigDB for mouse. Run GESECA with minSize=15, maxSize=500 to score gene set coregulation across time points. Validation: confirm that top pathways show expected temporal activation (E2F at 24h, hypoxia at 48h) with p-values and enrichment scores matching published ranges. References: GSE200250 (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE200250); GSE116240 (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE116240); GSE14308 (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE14308) Load GSE200250 microarray data from GEO and extract Th2 time-course samples Apply log2 transformation and quantile normalization to expression matrix Filter genes to top 12,000 by mean expression and remove duplicates/invalid identifiers Center gene expression matrix rows to zero mean and perform standard PCA extraction Retain first 10 principal components (feature loadings: genes × 10 PCs) as reduced expression matrix Run GESECA on full and reduced matrices with identical parameters (minSize=15, maxSize=500, center=FALSE for reduced) Compare pathway p-values between full and reduced results via Pearson correlation of log10-transformed p-values Validation: confirm log10 p-value correlation ≥0.95 to confirm dimensionality reduction preserves pathway scores References: GSE200250 (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE200250); GSE116240 (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE116240); GSE14308 (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE14308) Load GSE116240 Seurat object and annotate cell clusters into macrophage subtypes (Adventitial, Intimal non-foamy, Intimal foamy, ISG+). Apply SCTransform normalization with 10,000 variable features to stabilize variance and define gene universe. Run reverse PCA (npcs=50) on SCTransform-normalized expression to extract feature loadings matrix, reducing sample dimensionality while preserving gene-level signals. Load KEGG_LEGACY pathways from MSigDB and run GESECA with minSize=5, maxSize=500, center=FALSE, eps=1e-100 to compute gene-set co-regulation scores and empirical p-values. Generate tSNE/UMAP reduction plots showing pathway scores by cell type and verify that KEGG_LEISHMANIA_INFECTION localizes to non-foamy intimal macrophages and KEGG_LYSOSOME to foamy intimal macrophages. Validation: pathway-cell-type associations are confirmed when pathway score distributions show statistically significant separation (visual inspection or Mann-Whitney U test, p<0.05) between target and non-target cell types, and signals match published biology (Kim et al. findings on inflammatory vs. lysosomal programs). References: GSE200250 (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE200250); GSE116240 (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE116240); GSE14308 (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE14308) Load example gene set collection (examplePathways) and preranked gene statistics (exampleRanks) into R environment with reproducible random seed. Execute fgsea function with default eps=1e-10 lower bound, recording enrichment scores, raw P-values, adjusted P-values, and effect sizes (ES, NES) for all pathways. Re-execute fgsea with eps=0 to activate unrestricted adaptive multi-level Monte Carlo P-value refinement for the same input data. Construct merged comparison table indexed by pathway, computing pairwise differences and log-scale ratios of P-values from both runs. Visualize distribution of P-value improvements across pathways and verify ranking consistency between methods. Validation: confirm that eps=0 execution completes without error, produces valid numeric P-values for all pathways, and demonstrates lower (more precise) P-value estimates for top-ranked pathways relative to default run. References: GSE200250 (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE200250); GSE116240 (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE116240); GSE14308 (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE14308)

**Domain:** bioinformatics

**Techniques:** enrichment-analysis, pathway-analysis, statistical-analysis, false-discovery-rate-correction

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** fgsea is an R-package for fast preranked gene set enrichment analysis (GSEA). _[grounded: fgsea_system]_
- **(finding)** The fgsea package allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets. _[grounded: fgsea_system]_
- **(finding)** P-value estimation in fgsea is based on an adaptive multi-level split Monte-Carlo scheme. _[grounded: fgsea_system]_
- **(finding)** The fgsea package default lower bound for estimating P-values is eps=1e-10. _[grounded: fgsea_system]_
- **(finding)** GESECA is a method to identify gene sets that have high gene correlation. _[grounded: geseca_system]_
- **(finding)** GESECA takes as input a gene expression matrix E where rows and columns correspond to genes and samples respectively, and a list of gene sets P. _[grounded: geseca_system]_
- **(finding)** By default, GESECA method performs centering for rows of the matrix E. _[grounded: geseca_system]_
- **(finding)** GESECA score does not require an explicit sample annotation or a contrast. _[grounded: geseca_system]_
- **(finding)** GESECA can be applied to various types of sequencing technologies including RNA-seq, single-cell sequencing, and spatial RNA-seq. _[grounded: geseca_system]_
- **(finding)** GESECA assesses statistical significance for a given gene set by using gene permutations. _[grounded: geseca_system]_
- **(finding)** GESECA uses an adaptive multilevel Markov Chain Monte Carlo scheme for P-value estimation. _[grounded: geseca_system]_
- **(finding)** The first example in the GESECA tutorial considers a time course data of Th2 activation from the dataset GSE200250. _[grounded: geseca_system]_
- **(finding)** HALLMARK_E2F_TARGETS genes are strongly activated at 24 hours time point in Th2 cells. _[grounded: pathway_e2f_targets]_
- **(finding)** HALLMARK_HYPOXIA genes are activated around 48 hours in Th2 cells. _[grounded: fgsea_system]_
- **(finding)** When the expression matrix contains many samples, a PCA-reduced expression matrix can be used instead of the full matrix to improve performance.
- **(finding)** The sample space was reduced from a higher dimension to 10 dimensions in one GESECA example. _[grounded: geseca_system]_
- **(finding)** GESECA scores and P-values obtained on a reduced matrix are similar to those obtained for the full matrix. _[grounded: geseca_system]_
- **(finding)** The GSE116240 dataset features single cell RNA sequencing of aortic CD45+ cells and foam cells from atherosclerotic aorta. _[grounded: dataset_gse116240]_
- **(finding)** Inflammatory pathways such as KEGG_LEISHMANIA_INFECTION are more associated with non-foamy intimal macrophages. _[grounded: pathway_kegg_leishmania]_
- **(finding)** KEGG_LYSOSOME pathway is specific to intimal foamy macrophages. _[grounded: pathway_kegg_lysosome]_
- **(finding)** GESECA can be used for gene set enrichment analysis of spatial transcriptomics profiling. _[grounded: geseca_system]_
- **(finding)** A glioblastoma sample analyzed with GESECA shows a distinct hypoxic region defined by HALLMARK_HYPOXIA. _[grounded: geseca_system]_
- **(finding)** HALLMARK_INTERFERON_GAMMA_RESPONSE defines a reactive immune region in glioblastoma. _[grounded: pathway_ifn_gamma]_
- **(finding)** HALLMARK_OXIDATIVE_PHOSPHORYLATION pathway is more characteristic to normal tissue regions compared to diseased regions. _[grounded: pathway_oxphos]_
- **(finding)** GESECA can be applied to spatial transcriptomics data generated by high-plex in situ technologies with subcellular resolution such as 10X Genomics' Xenium platform. _[grounded: geseca_system]_
- **(finding)** A Human Ovarian Cancer sample was profiled using the Xenium 5K panel in a GESECA analysis example. _[grounded: geseca_system]_
- **(finding)** SCTransform normalization was performed on 10000 genes in Xenium data analysis. _[grounded: geseca_system]_
- **(finding)** Reverse PCA with 50 principal components was performed on Xenium scRNA-seq data.
- **(finding)** Reverse PCA with 30 principal components was performed on Xenium spatial transcriptomics data.
- **(finding)** HALLMARK gene sets from MSigDB collection were used in Xenium GESECA analysis. _[grounded: geseca_system]_
- **(finding)** Top enriched pathways identified by GESECA in Xenium data were visualized using UMAP embeddings. _[grounded: geseca_system]_
- **(finding)** The plotCoregulationProfileImage function enables visualization of how pathway activities vary across spatial coordinates in Xenium data. _[grounded: plot_coregulation_image_func]_
- **(finding)** An R-package for performing GESECA (GEne SEt Co-regulation Analysis) is available. _[grounded: geseca_system]_
- **(finding)** The exampleExpressionMatrix is a numeric expression matrix of the GSE14308 dataset with 10000 rows corresponding to genes and 12 columns corresponding to samples. _[grounded: dataset_example_expression_matrix]_
- **(finding)** The exampleExpressionMatrix values are log-scaled and the samples are quantile normalized. _[grounded: geseca_system]_
- **(finding)** examplePathways is a list of mouse pathways from the reactome.db package. _[grounded: tool_reactome_db]_
- **(finding)** The 5990980_Cell_Cycle pathway had a pctEvar of 1.0525898 and a pval of 2.276767e-39 in GESECA analysis. _[grounded: geseca_system]_
- **(finding)** The 5990979_Cell_Cycle,_Mitotic pathway had a pctEvar of 1.0466758 and a pval of 3.891185e-39 in GESECA analysis. _[grounded: geseca_system]_
- **(finding)** The 5991851_Mitotic_Prometaphase pathway had a pctEvar of 0.7485590 and a pval of 1.409623e-24 in GESECA analysis. _[grounded: geseca_system]_
- **(finding)** The 5992217_Resolution_of_Sister_Chromatid_Cohesion pathway had a pctEvar of 0.7075162 and a pval of 1.265783e-22 in GESECA analysis. _[grounded: geseca_system]_
- **(finding)** The 5991454_M_Phase pathway had a pctEvar of 0.6020886 and a pval of 6.237558e-22 in GESECA analysis. _[grounded: geseca_system]_
- **(finding)** The collapsePathways function can be used to select only independent pathways in fgsea results. _[grounded: fgsea_system]_
- **(finding)** The mapIdsList function is similar to AnnotationDbi::mapIds and can be used to convert leading edge to human-readable format. _[grounded: map_ids_list_func]_
- **(finding)** fgsea is parallelized using the BiocParallel package. _[grounded: fgsea_system]_
- **(finding)** By default the first registered backend returned by bpparam() is used in fgsea parallelization. _[grounded: fgsea_system]_
- **(finding)** fgsea has a reactomePathways function that obtains pathways from Reactome for a given set of genes. _[grounded: fgsea_system]_
- **(finding)** The reactomePathways function in fgsea requires the reactome.db package to be installed. _[grounded: fgsea_system]_
- **(finding)** fgsea can load pathways from .gmt files using the gmtPathways function. _[grounded: fgsea_system]_
- **(finding)** The fora function in fgsea performs over-representation analysis based enrichment tests using the hypergeometric test. _[grounded: fgsea_system]_
- **(finding)** The fora function requires a foreground set of genes, a background set of all robustly detected genes, and some pathways. _[grounded: fora_func]_

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- fgseaMultilevel can be used as an alternative P-value estimation procedure

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- Gene identifiers must be consistent between expression matrix and pathway list
- Expression matrix values must be log-scaled and quantile normalized
- Center parameter must be set to FALSE when using reduced/preprocessed matrices

## Steps

### Step `task_001`
- Title: Reproduce fgsea enrichment analysis on examplePathways and exampleRanks with default parameters
- Task kind: `reproduction`
- Task: Run fgsea() on bundled examplePathways and exampleRanks with default parameters (eps=1e-10), generate the enrichment result table, create an enrichment plot for the Programmed_Cell_Death pathway, and produce a GSEA table visualization for top-ranked pathways.
- Inputs:
  - examplePathways: bundled list of mouse Reactome gene set pathways
  - exampleRanks: bundled gene-level ranking statistics (t-statistics or log-fold-change)
- Expected outputs:
  - fgseaRes: data.table with columns pathway, pval, padj, ES, NES, size, leadingEdge sorted by p-value
  - enrichment_plot_programmed_cell_death.png: ggplot2 enrichment curve showing running sum of ES for 5991130_Programmed_Cell_Death pathway
  - gsea_table_top_pathways.png: heatmap-style table visualization of top 20 pathways (10 up, 10 down) with running sum curves
- Tools: fgsea, R, data.table, ggplot2
- Landmark output files: fgseaRes_sorted.csv, enrichment_plot_programmed_cell_death.png, top_pathways_list.txt, gsea_table_top_pathways.png

### Step `task_002`
- Title: Reproduce GESECA analysis on GSE200250 Th2 time-course full expression matrix and verify top pathway scores
- Task kind: `reproduction`
- Task: Load the GSE200250 Th2 activation time-course dataset via GEOquery, apply log and quantile normalization with limma, run GESECA analysis on the full expression matrix using HALLMARK gene sets, and verify that top enriched pathways match reported temporal activation patterns and p-values.
- Inputs:
  - GSE200250 dataset from NCBI GEO (publicly accessible via GEOquery)
  - HALLMARK gene set collection from MSigDB via msigdbr
- Expected outputs:
  - GESECA results table with pathway names, scores, p-values, and adjusted p-values sorted by significance
  - Temporal activation pattern confirmation for top pathways showing E2F targets active at 24h and hypoxia genes active at 48h
- Tools: GEOquery, limma, fgsea, msigdbr, data.table, ggplot2, R
- Landmark output files: normalized_expression_matrix.RData, filtered_expression_matrix.RData, geseca_results_sorted_by_pvalue.csv, temporal_activation_plot_E2F_targets.png, temporal_activation_plot_hypoxia.png
- Primary expected artifact: `geseca_results_table.csv`

### Step `task_003`
- Depends on: `task_002`
- Title: Reproduce GESECA PCA-reduced analysis on GSE200250 and verify score similarity to full-matrix results
- Task kind: `reproduction`
- Task: Apply principal component analysis (PCA) reduction to 10 dimensions on the GSE200250 expression matrix, re-run GESECA analysis on the reduced matrix with center=FALSE, and verify that resulting pathway scores and p-values remain similar to those from the full-matrix analysis.
- Inputs:
  - GSE200250 microarray dataset from GEO (Th2 activation time course)
  - Hallmark gene set collection from MSigDB
- Expected outputs:
  - GESECA results table from full matrix analysis (pathway, score, pval, padj, size)
  - GESECA results table from reduced (10-PC) matrix analysis (pathway, score, pval, padj, size)
  - Scatterplot comparing log10(pval) from full vs reduced matrix, showing Pearson correlation ≥0.95
- Tools: GEOquery, limma, fgsea, R, ggplot2, data.table, msigdbr
- Landmark output files: normalized_expression_matrix.rds, pca_reduced_matrix_10d.rds, geseca_full_results.tsv, geseca_reduced_results.tsv
- Primary expected artifact: `pval_comparison_full_vs_reduced.png`

### Step `task_004`
- Depends on: `task_002`
- Title: Reproduce GESECA scRNA-seq analysis on GSE116240 atherosclerosis data with KEGG_LEGACY pathways
- Task kind: `reproduction`
- Task: Load GSE116240 single-cell RNA-seq aortic CD45+ cell data via Seurat, normalize with SCTransform, reduce dimensionality via reverse PCA, run GESECA analysis with KEGG_LEGACY pathways, and verify pathway-cell-type associations: KEGG_LEISHMANIA_INFECTION with non-foamy intimal macrophages and KEGG_LYSOSOME with intimal foamy macrophages. Output enrichment results table and spatial/reduction plots showing pathway localization.
- Inputs:
  - GSE116240 Seurat object (single-cell RNA-seq from aortic CD45+ cells and foam cells)
  - KEGG_LEGACY pathway collection from MSigDB (human species)
- Expected outputs:
  - GESECA enrichment results table with pathway names, scores (pctEvar or similar), p-values, and adjusted p-values
  - Reduction plots (tSNE or UMAP) showing co-regulation scores for KEGG_LEISHMANIA_INFECTION and KEGG_LYSOSOME pathways colored by cell type annotation
  - Verification report confirming KEGG_LEISHMANIA_INFECTION association with non-foamy intimal macrophages and KEGG_LYSOSOME specificity to intimal foamy macrophages
- Tools: R, fgsea, Seurat, msigdbr, ggplot2, data.table
- Landmark output files: seurat_annotated.rds, feature_loadings_matrix.csv, geseca_enrichment_table.csv, kegg_leishmania_infection_plot.png, kegg_lysosome_plot.png
- Primary expected artifact: `geseca_kegg_results.csv`

### Step `task_005`
- Depends on: `task_001`
- Title: Reconstruct the fgseaMultilevel adaptive multilevel MCMC P-value estimation component under eps=0 exact mode
- Task kind: `component_reconstruction`
- Task: Run fgsea with adaptive multi-level Monte Carlo scheme (eps=0) on examplePathways and exampleRanks, then compare P-value precision and magnitude against default eps=1e-10 lower-bound estimates to demonstrate improved statistical accuracy.
- Inputs:
  - examplePathways (list of gene sets from reactome.db)
  - exampleRanks (preranked gene-level statistics)
- Expected outputs:
  - fgsea results table (default eps=1e-10) with columns: pathway, pval, padj, ES, NES, size
  - fgsea results table (eps=0) with same columns and refined P-values
  - Comparison table showing pathway, pval_default, pval_eps0, pval_ratio, pval_difference for all pathways
  - Visualization (scatter plot or histogram) of log10(pval_ratio) distribution across pathways
- Tools: fgsea, R, data.table, ggplot2
- Landmark output files: fgsea_default_eps1e10_results.csv, fgsea_eps0_results.csv, pvalue_improvement_summary.csv, pvalue_ratio_distribution.png
- Primary expected artifact: `fgsea_pvalue_comparison.csv`

## Final expected outputs

- `GESECA results table from full matrix analysis (pathway, score, pval, padj, size)` (type: file, tolerance: hash)
- `GESECA results table from reduced (10-PC) matrix analysis (pathway, score, pval, padj, size)` (type: file, tolerance: hash)
- `Scatterplot comparing log10(pval) from full vs reduced matrix, showing Pearson correlation ≥0.95` (type: file, tolerance: hash)
- `GESECA enrichment results table with pathway names, scores (pctEvar or similar), p-values, and adjusted p-values` (type: file, tolerance: hash)
- `Reduction plots (tSNE or UMAP) showing co-regulation scores for KEGG_LEISHMANIA_INFECTION and KEGG_LYSOSOME pathways colored by cell type annotation` (type: file, tolerance: hash)
- `Verification report confirming KEGG_LEISHMANIA_INFECTION association with non-foamy intimal macrophages and KEGG_LYSOSOME specificity to intimal foamy macrophages` (type: file, tolerance: hash)
- `fgsea results table (default eps=1e-10) with columns: pathway, pval, padj, ES, NES, size` (type: file, tolerance: hash)
- `fgsea results table (eps=0) with same columns and refined P-values` (type: file, tolerance: hash)
- `Comparison table showing pathway, pval_default, pval_eps0, pval_ratio, pval_difference for all pathways` (type: file, tolerance: hash)
- `Visualization (scatter plot or histogram) of log10(pval_ratio) distribution across pathways` (type: file, tolerance: hash)

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
  "workflow_id": "coll_fgsea_workflow",
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
    "GESECA results table from full matrix analysis (pathway, score, pval, padj, size)": "<locator>",
    "GESECA results table from reduced (10-PC) matrix analysis (pathway, score, pval, padj, size)": "<locator>",
    "Scatterplot comparing log10(pval) from full vs reduced matrix, showing Pearson correlation \u22650.95": "<locator>",
    "GESECA enrichment results table with pathway names, scores (pctEvar or similar), p-values, and adjusted p-values": "<locator>",
    "Reduction plots (tSNE or UMAP) showing co-regulation scores for KEGG_LEISHMANIA_INFECTION and KEGG_LYSOSOME pathways colored by cell type annotation": "<locator>",
    "Verification report confirming KEGG_LEISHMANIA_INFECTION association with non-foamy intimal macrophages and KEGG_LYSOSOME specificity to intimal foamy macrophages": "<locator>",
    "fgsea results table (default eps=1e-10) with columns: pathway, pval, padj, ES, NES, size": "<locator>",
    "fgsea results table (eps=0) with same columns and refined P-values": "<locator>",
    "Comparison table showing pathway, pval_default, pval_eps0, pval_ratio, pval_difference for all pathways": "<locator>",
    "Visualization (scatter plot or histogram) of log10(pval_ratio) distribution across pathways": "<locator>"
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
