# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Does the fgsea package enable accurate and rapid calculation of gene set enrichment P-values across arbitrarily low thresholds?: 'This package allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets.'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] P-value estimation in fgsea is based on an adaptive multi-level split Monte-Carlo scheme.: 'P-value estimation is based on an adaptive multi-level split Monte-Carlo scheme.'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] GSE116240 Seurat object (single-cell RNA-seq from aortic CD45+ cells and foam cells): 'obj <- readRDS(url("https://alserglab.wustl.edu/files/fgsea/GSE116240.rds"))'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] KEGG_LEGACY pathway collection from MSigDB (human species): 'pathwaysDF <- msigdbr(species="mouse", collection="C2", subcollection = "CP:KEGG_LEGACY")
pathways <- split(pathwaysDF$gene_symbol, pathwaysDF$gs_name)'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] GESECA enrichment results table with pathway names, scores (pctEvar or similar), p-values, and adjusted p-values: 'gesecaRes <- geseca(pathways, E, minSize = 5, maxSize = 500, center = FALSE, eps=1e-100)

head(gesecaRes, 10)'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Reduction plots (tSNE or UMAP) showing co-regulation scores for KEGG_LEISHMANIA_INFECTION and KEGG_LYSOSOME pathways colored by cell type annotation: 'plotCoregulationProfileReduction(pathways[topPathways], obj,
                                       title=titles,
                                       reduction="tsne")'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Verification report confirming KEGG_LEISHMANIA_INFECTION association with non-foamy intimal macrophages and KEGG_LYSOSOME specificity to intimal foamy macrophages: 'We can see that inflammatory pathways (e.g. KEGG_LEISHMANIA_INFECTION) are more associated with the non-foamy intimal macrophages, which was one of the main points of the Kim et al. Another pathway'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] R: '`fgsea` is an R-package'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] fgsea: 'library(fgsea)
geseca(pathways, E, minSize = 5, maxSize = 500, center = FALSE, eps=1e-100)'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Seurat: 'suppressMessages(library(Seurat))
obj <- readRDS(url("https://alserglab.wustl.edu/files/fgsea/GSE116240.rds"))'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] msigdbr: 'library(msigdbr)
pathwaysDF <- msigdbr(species="mouse", collection="C2", subcollection = "CP:KEGG_LEGACY")'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] ggplot2: 'library(ggplot2)'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] data.table: 'library(data.table)'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog available for reproducibility tracking: 'No changelog found.'
