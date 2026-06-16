# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] How many genes in the airway dataset show statistically significant differential expression (adjusted p-value < 0.1) between treated and untreated conditions when analyzed with DESeq2 using the default FDR threshold?: 'we load the package containing the `airway` dataset'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] The airway dataset is available in Bioconductor for use with DESeq2 differential expression analysis of treated versus untreated samples.: 'we load the package containing the `airway` dataset. ... library("airway") data("airway")'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] airway SummarizedExperiment object from Bioconductor airway package: 'library("airway")
data("airway")
se <- airway'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Results table with columns: baseMean, log2FoldChange, lfcSE, stat, pvalue, padj for treated-vs-untreated contrast: 'Results tables are generated using the function *results*, which extracts a results table with log2 fold changes, *p* values and adjusted *p* values.'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Count of genes with adjusted p-value < 0.1: 'How many adjusted p-values were less than 0.1?'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] DESeq2: 'The package DESeq2 provides methods to test for differential expression by use of negative binomial generalized linear models'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog or versioning information provided for DESeq2 source repository: 'No changelog found.'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Specific expected number of genes with adjusted p-value < 0.1 for treated-vs-untreated contrast on airway dataset not reported in provided section: 'No changelog found.'
