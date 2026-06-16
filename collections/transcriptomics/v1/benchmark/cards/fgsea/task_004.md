# SciTask Card: Reproduce GESECA scRNA-seq analysis on GSE116240 atherosclerosis data with KEGG_LEGACY pathways

- Task ID: `task_004`
- Schema version: `0.18.0`
- Created at: `2026-06-15T19:18:01.563888+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_transcriptomics/coll_fgsea/synthesized_package`
- Domain: `bioinformatics`
- Subtask categories: `data-processing`, `data-analysis`, `statistical-analysis`, `visualization`
- GitHub: `alserglab/fgsea`
- Input from: `task_002`

## Classification

- Task kind: `reproduction`
- Article type: `software-tool`
- Primary domain: `bioinformatics`
- Subdomains: `functional-genomics`, `multi-omics-integration`
- Techniques: `enrichment-analysis`, `pathway-analysis`, `statistical-analysis`, `false-discovery-rate-correction`

## Research Question
Does the fgsea package enable accurate and rapid calculation of gene set enrichment P-values across arbitrarily low thresholds?

## Connected Finding
P-value estimation in fgsea is based on an adaptive multi-level split Monte-Carlo scheme.

## Task Description
Load GSE116240 single-cell RNA-seq aortic CD45+ cell data via Seurat, normalize with SCTransform, reduce dimensionality via reverse PCA, run GESECA analysis with KEGG_LEGACY pathways, and verify pathway-cell-type associations: KEGG_LEISHMANIA_INFECTION with non-foamy intimal macrophages and KEGG_LYSOSOME with intimal foamy macrophages. Output enrichment results table and spatial/reduction plots showing pathway localization.

## Inputs
- GSE116240 Seurat object (single-cell RNA-seq from aortic CD45+ cells and foam cells)
- KEGG_LEGACY pathway collection from MSigDB (human species)

## Expected Outputs
- GESECA enrichment results table with pathway names, scores (pctEvar or similar), p-values, and adjusted p-values
- Reduction plots (tSNE or UMAP) showing co-regulation scores for KEGG_LEISHMANIA_INFECTION and KEGG_LYSOSOME pathways colored by cell type annotation
- Verification report confirming KEGG_LEISHMANIA_INFECTION association with non-foamy intimal macrophages and KEGG_LYSOSOME specificity to intimal foamy macrophages

## Expected Output File

- `geseca_kegg_results.csv`

## Landmark Outputs

- `seurat_annotated.rds`
- `feature_loadings_matrix.csv`
- `geseca_enrichment_table.csv`
- `kegg_leishmania_infection_plot.png`
- `kegg_lysosome_plot.png`

## Tools
- R
- fgsea
- Seurat
- msigdbr
- ggplot2
- data.table

## Skills
- single-cell-rna-seq-quality-control-and-normalization
- seurat-workflow-orchestration-for-scRNAseq
- dimensionality-reduction-via-reverse-pca
- gene-set-coregulation-analysis
- pathway-cell-type-association-validation
- reduction-plot-interpretation-and-visualization

## Workflow Description
1. Load GSE116240 Seurat object from URL and annotate cell clusters with macrophage subtypes (Adventitial MF, Intimal non-foamy MF, Intimal foamy MF, ISG+ MF, etc.) using RenameIdents. 2. Apply SCTransform normalization with variable.features.n=10000 to stabilize variance and select genes for universe. 3. Run reverse PCA (rev.pca=TRUE) on SCTransform-normalized matrix with npcs=50, extracting feature loadings matrix E. 4. Load KEGG_LEGACY pathways from MSigDB using msigdbr for human species. 5. Run geseca(pathways, E, minSize=5, maxSize=500, center=FALSE, eps=1e-100) on reduced feature space, producing enrichment scores and p-values. 6. Extract top-ranked pathways and generate plotCoregulationProfileReduction plots (reduction='tsne') to visualize pathway scores by cell type, confirming KEGG_LEISHMANIA_INFECTION prominence in non-foamy intimal macrophages and KEGG_LYSOSOME in foamy intimal macrophages.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/geseca-spatial-top.png` | figure | False |
| `figures/geseca-vignette-score-toy-example.png` | figure | False |
| `paper.md` | main_article | True |

## Data Deposits

| Kind | Accession | URL | Evidence |
|---|---|---|---|
| geo_series | `GSE200250` | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE200250 | sider a time course data of Th2 activation from the dataset GSE200250.  First, let prepare the dataset. We load it from Gene Expr |
| geo_series | `GSE116240` | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE116240 | ges(library(Seurat)) ```  As an example dataset we will use GSE116240 (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE1162 |
| geo_series | `GSE14308` | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE14308 | exampleExpressionMatrix` - numeric expression matrix of the GSE14308 dataset. Rows correspond to genes (ENTREZID is used as iden |

## Missing Information
- No changelog available for reproducibility tracking

## Domain Knowledge
- GESECA scores measure co-regulation of gene sets without explicit sample annotation by summing squared column sums of centered gene expression within each pathway, analogous to explained variance in PCA.
- Reverse PCA (rev.pca=TRUE) extracts feature loadings where rows are genes and columns are principal components derived from cell variation, enabling pathway analysis on reduced sample space while preserving gene-level interpretability.
- SCTransform normalization with variable.features.n=10000 stabilizes variance heterogeneity in scRNA-seq and establishes a gene universe; GESECA pathways must use identical gene identifiers.
- KEGG_LEGACY pathways use gene symbols as identifiers; msigdbr must specify species='human' for human datasets (GSE116240 is human ovarian/aortic tissue, not mouse).
- Pathway specificity to cell types is validated visually via tSNE/UMAP reduction plots colored by cell-type annotation, where high co-regulation scores should concentrate in expected cell populations (e.g., KEGG_LYSOSOME in foamy macrophages with high lysosomal content).

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: Seurat, msigdbr, ggplot2, data.table, GESECA enrichment results table with pathway names, scores (pctEvar or similar), p-values, and adjusted p-values, Reduction plots (tSNE or UMAP) showing co-regulation scores for KEGG_LEISHMANIA_INFECTION and KEGG_LYSOSOME pathways colored by cell type annotation, Verification report confirming KEGG_LEISHMANIA_INFECTION association with non-foamy intimal macrophages and KEGG_LYSOSOME specificity to intimal foamy macrophages.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] Does the fgsea package enable accurate and rapid calculation of gene set enrichment P-values across arbitrarily low thresholds?: 'This package allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets.'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] P-value estimation in fgsea is based on an adaptive multi-level split Monte-Carlo scheme.: 'P-value estimation is based on an adaptive multi-level split Monte-Carlo scheme.'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] GSE116240 Seurat object (single-cell RNA-seq from aortic CD45+ cells and foam cells): 'obj <- readRDS(url("https://alserglab.wustl.edu/files/fgsea/GSE116240.rds"))'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] KEGG_LEGACY pathway collection from MSigDB (human species): 'pathwaysDF <- msigdbr(species="mouse", collection="C2", subcollection = "CP:KEGG_LEGACY")
pathways <- split(pathwaysDF$gene_symbol, pathwaysDF$gs_name)'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] GESECA enrichment results table with pathway names, scores (pctEvar or similar), p-values, and adjusted p-values: 'gesecaRes <- geseca(pathways, E, minSize = 5, maxSize = 500, center = FALSE, eps=1e-100)

head(gesecaRes, 10)'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] Reduction plots (tSNE or UMAP) showing co-regulation scores for KEGG_LEISHMANIA_INFECTION and KEGG_LYSOSOME pathways colored by cell type annotation: 'plotCoregulationProfileReduction(pathways[topPathways], obj,
                                       title=titles,
                                       reduction="tsne")'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] Verification report confirming KEGG_LEISHMANIA_INFECTION association with non-foamy intimal macrophages and KEGG_LYSOSOME specificity to intimal foamy macrophages: 'We can see that inflammatory pathways (e.g. KEGG_LEISHMANIA_INFECTION) are more associated with the non-foamy intimal macrophages, which was one of the main points of the Kim et al. Another pathway'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] R: '`fgsea` is an R-package'
- `ev_009` from `agent2_synthesis` (agent2_traced): [methods] fgsea: 'library(fgsea)
geseca(pathways, E, minSize = 5, maxSize = 500, center = FALSE, eps=1e-100)'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] Seurat: 'suppressMessages(library(Seurat))
obj <- readRDS(url("https://alserglab.wustl.edu/files/fgsea/GSE116240.rds"))'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] msigdbr: 'library(msigdbr)
pathwaysDF <- msigdbr(species="mouse", collection="C2", subcollection = "CP:KEGG_LEGACY")'
- `ev_012` from `agent2_synthesis` (agent2_traced): [methods] ggplot2: 'library(ggplot2)'
- `ev_013` from `agent2_synthesis` (agent2_traced): [methods] data.table: 'library(data.table)'
- `ev_014` from `agent2_synthesis` (agent2_traced): [discussion] No changelog available for reproducibility tracking: 'No changelog found.'

## Evaluation Strategy
### Direct Checks
- verify file exists: GSE116240 dataset accessible via GEOquery at https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE116240
- verify script_runs: R script loads GSE116240 data using GEOquery::getGEO() without errors
- verify script_runs: Seurat SCTransform normalization completes on GSE116240 expression matrix
- verify script_runs: fgsea::geseca() executes with KEGG_LEGACY pathway collection and GSE116240 SCTransform-normalized data without errors
- verify output_matches_reference: KEGG_LEISHMANIA_INFECTION pathway appears in geseca results table with non-foamy intimal macrophage cell type assignment
- verify output_matches_reference: KEGG_LYSOSOME pathway appears in geseca results table with foamy macrophage cell type assignment
- verify field_present: geseca output table contains columns for pathway name, cell type annotation, and enrichment statistic

### Expert Review
- confirm that KEGG_LEISHMANIA_INFECTION association with non-foamy intimal macrophages is biologically plausible given known pathogen-response gene signatures
- confirm that KEGG_LYSOSOME specificity to intimal foamy macrophages is consistent with lipid catabolism and foam cell biology
- assess whether SCTransform normalization parameters and geseca settings (minSize, maxSize, other hyperparameters) are appropriate for single-cell RNA-seq data and KEGG_LEGACY pathway collection
- evaluate whether cell type annotations in GSE116240 are sufficiently granular and accurate to support macrophage subtype-specific enrichment claims

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** medium

## Methodology Summary
1. Load GSE116240 Seurat object and annotate cell clusters into macrophage subtypes (Adventitial, Intimal non-foamy, Intimal foamy, ISG+).
2. Apply SCTransform normalization with 10,000 variable features to stabilize variance and define gene universe.
3. Run reverse PCA (npcs=50) on SCTransform-normalized expression to extract feature loadings matrix, reducing sample dimensionality while preserving gene-level signals.
4. Load KEGG_LEGACY pathways from MSigDB and run GESECA with minSize=5, maxSize=500, center=FALSE, eps=1e-100 to compute gene-set co-regulation scores and empirical p-values.
5. Generate tSNE/UMAP reduction plots showing pathway scores by cell type and verify that KEGG_LEISHMANIA_INFECTION localizes to non-foamy intimal macrophages and KEGG_LYSOSOME to foamy intimal macrophages.
6. Validation: pathway-cell-type associations are confirmed when pathway score distributions show statistically significant separation (visual inspection or Mann-Whitney U test, p<0.05) between target and non-target cell types, and signals match published biology (Kim et al. findings on inflammatory vs. lysosomal programs).
7. References: GSE200250 (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE200250); GSE116240 (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE116240); GSE14308 (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE14308)

## Workflow Ports

**Inputs:**

- `seurat_obj` — GSE116240 Seurat object with scRNA-seq expression data ← `task_002/geseca_results`
- `kegg_pathways` — KEGG_LEGACY pathway collection from MSigDB

**Outputs:**

- `geseca_results` — GESECA enrichment table with p-values and scores
- `reduction_plots` — Reduction plots showing pathway scores by cell type
- `verification_report` — Pathway-cell-type association verification

**Used:** `urn:asb:port:task_002/geseca_results`

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:alserglab__fgsea`
- **Synthesized at:** 2026-06-15T19:26:40+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
