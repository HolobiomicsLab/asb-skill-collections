# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Does fgsea produce consistent enrichment scores and p-values for known pathway activations when applied to normalized gene expression data from a time-course experiment?: 'This package allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets.'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] fgsea enables fast and accurate calculation of arbitrarily low GSEA P-values for gene set collections, supporting reproducible pathway enrichment analysis.: 'This package allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets.'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] GSE200250 dataset from NCBI GEO (publicly accessible via GEOquery): 'gse200250 <- getGEO("GSE200250", AnnotGPL = TRUE)[[1]]'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] HALLMARK gene set collection from MSigDB via msigdbr: 'pathwaysDF <- msigdbr(species="mouse", collection="H")'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] GESECA results table with pathway names, scores, p-values, and adjusted p-values sorted by significance: 'gesecaRes <- geseca(pathways, exprs(es), minSize = 15, maxSize = 500)'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Temporal activation pattern confirmation for top pathways showing E2F targets active at 24h and hypoxia genes active at 48h: 'plotCoregulationProfile(pathway=pathways[["HALLMARK_E2F_TARGETS"]], E=exprs(es), titles = es$title, conditions=es$`time point:ch1`)'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] GEOquery: 'library(GEOquery)'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] limma: 'exprs(es) <- normalizeBetweenArrays(log2(exprs(es)), method="quantile")'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] fgsea: 'gesecaRes <- geseca(pathways, exprs(es), minSize = 15, maxSize = 500)'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] msigdbr: 'pathwaysDF <- msigdbr(species="mouse", collection="H")'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] data.table: 'library(data.table)'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] ggplot2: 'library(ggplot2)'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] R: 'fgsea is an R-package for fast preranked gene set enrichment analysis'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog available to document version history or changes to fgsea package used for analysis: 'No changelog found.'
