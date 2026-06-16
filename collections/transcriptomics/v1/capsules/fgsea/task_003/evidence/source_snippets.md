# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Does dimensionality reduction via PCA to 10 dimensions preserve the pathway enrichment results (pathway scores and p-values) obtained from geseca() analysis on the full-dimensional GSE200250 expression matrix?: 'gesecaRes <- geseca(exampleExpressionMatrix, examplePathways, minSize = 15, maxSize = 500)'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] fgsea enables fast and accurate calculation of GSEA P-values for gene set collections, supporting the feasibility of comparing pathway enrichment results across different input dimensionalities.: 'This package allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] GSE200250 microarray dataset from GEO (Th2 activation time course): 'gse200250 <- getGEO("GSE200250", AnnotGPL = TRUE)[[1]]'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Hallmark gene set collection from MSigDB: 'pathwaysDF <- msigdbr(species="mouse", collection="H")'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] GESECA results table from full matrix analysis (pathway, score, pval, padj, size): 'gesecaRes <- geseca(pathways, exprs(es), minSize = 15, maxSize = 500)'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] GESECA results table from reduced (10-PC) matrix analysis (pathway, score, pval, padj, size): 'gesecaResRed <- geseca(pathways, Ered, minSize = 15, maxSize = 500, center=FALSE)'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Scatterplot comparing log10(pval) from full vs reduced matrix, showing Pearson correlation ≥0.95: 'ggplot(data=merge(gesecaRes[, list(pathway, logPvalFull=-log10(pval))], gesecaResRed[, list(pathway, logPvalRed=-log10(pval))])) + geom_point(aes(x=logPvalFull, y=logPvalRed))'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] GEOquery: 'library(GEOquery)'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] limma: 'exprs(es) <- normalizeBetweenArrays(log2(exprs(es)), method="quantile")'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] fgsea: 'gesecaResRed <- geseca(pathways, Ered, minSize = 15, maxSize = 500, center=FALSE)'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] R: 'E <- t(base::scale(t(exprs(es)), scale=FALSE))'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] ggplot2: 'ggplot(data=merge(...)) + geom_point(aes(x=logPvalFull, y=logPvalRed))'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] data.table: 'library(data.table)'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] msigdbr: 'pathwaysDF <- msigdbr(species="mouse", collection="H")'

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog or version history available for the fgsea package: 'No changelog found.'

## ev_016

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Specific reference implementation or expected outputs for the full-matrix geseca() run on GSE200250 are not provided: '[UNTRUSTED_DOCUMENT]_No changelog found._'
