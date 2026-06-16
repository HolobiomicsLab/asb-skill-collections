# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] How does the adaptive multi-level split Monte-Carlo scheme in fgsea adjust P-value precision when the eps parameter is set to zero rather than using a default lower-bound threshold?: 'P-value estimation is based on an adaptive multi-level split Monte-Carlo scheme'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] fgsea implements an adaptive multi-level split Monte-Carlo scheme that enables calculation of arbitrarily low GSEA P-values for gene set collections without a fixed lower-bound constraint.: 'This package allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets. P-value estimation is based on an adaptive multi-level split Monte-Carlo scheme.'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] examplePathways (list of gene sets from reactome.db): 'data(examplePathways)'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] exampleRanks (preranked gene-level statistics): 'data(exampleRanks)'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] fgsea results table (default eps=1e-10) with columns: pathway, pval, padj, ES, NES, size: 'head(fgseaRes[order(pval), ])'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] fgsea results table (eps=0) with same columns and refined P-values: 'fgseaRes <- fgsea(pathways = examplePathways, stats = exampleRanks, eps = 0.0, minSize = 15, maxSize = 500)'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Comparison table showing pathway, pval_default, pval_eps0, pval_ratio, pval_difference for all pathways: 'fgsea has a default lower bound `eps=1e-10` for estimating P-values. If you need to estimate P-value more accurately, you can set the `eps` argument to zero'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Visualization (scatter plot or histogram) of log10(pval_ratio) distribution across pathways: 'This package allows to quickly and accurately calculate arbitrarily low GSEA P-values'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] fgsea: '`fgsea` is an R-package for fast preranked gene set enrichment analysis (GSEA)'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] R: '`fgsea` is an R-package for fast preranked gene set enrichment analysis (GSEA)'

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

[discussion] No changelog or version history available to track changes to fgsea package, affecting reproducibility of exact algorithm implementation state at synthesis date: 'No changelog found.'
