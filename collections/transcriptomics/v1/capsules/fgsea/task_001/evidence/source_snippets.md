# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Can the fgsea package calculate gene set enrichment analysis results on preranked gene lists with arbitrarily low P-values using its default parameters?: 'This package allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets.'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] fgsea is an R-package for fast preranked gene set enrichment analysis (GSEA) that enables quick and accurate calculation of arbitrarily low GSEA P-values for gene set collections.: '`fgsea` is an R-package for fast preranked gene set enrichment analysis (GSEA). This package allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets.'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] examplePathways: bundled list of mouse Reactome gene set pathways: 'data(examplePathways)'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] exampleRanks: bundled gene-level ranking statistics (t-statistics or log-fold-change): 'data(exampleRanks)'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] fgseaRes: data.table with columns pathway, pval, padj, ES, NES, size, leadingEdge sorted by p-value: 'The resulting table contains enrichment scores and p-values'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] enrichment_plot_programmed_cell_death.png: ggplot2 enrichment curve showing running sum of ES for 5991130_Programmed_Cell_Death pathway: 'plotEnrichment(examplePathways[["5991130_Programmed_Cell_Death"]], exampleRanks) + labs(title="Programmed Cell Death")'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] gsea_table_top_pathways.png: heatmap-style table visualization of top 20 pathways (10 up, 10 down) with running sum curves: 'plotGseaTable(examplePathways[topPathways], exampleRanks, fgseaRes, gseaParam=0.5)'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] fgsea: '`fgsea` is an R-package for fast preranked gene set enrichment analysis (GSEA)'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] R: 'R-package for fast preranked gene set enrichment analysis'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] data.table: 'library(data.table)'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] ggplot2: 'library(ggplot2)'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog available to track version history, breaking changes, or reproducibility constraints for the fgsea package used: 'No changelog found.'
