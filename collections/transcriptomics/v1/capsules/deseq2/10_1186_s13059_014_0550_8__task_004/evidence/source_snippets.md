# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] How does the results() function automatically perform independent filtering based on mean normalized counts, and what are the expected outputs when this filtering is applied to DESeq2 results?: 'the *results* function automatically performs independent filtering based on the mean of normalized counts for each gene'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] The results() function automatically performs independent filtering based on the mean of normalized counts for each gene.: 'the *results* function automatically performs independent filtering based on the mean of normalized counts for each gene'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] airway SummarizedExperiment dataset from Bioconductor airway package: 'library("airway"); data("airway"); se <- airway'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Results table with log2 fold changes, p-values, and adjusted p-values after automatic independent filtering (default alpha=0.1): 'the *results* function automatically performs independent filtering based on the mean of normalized counts for each gene, optimizing the number of genes which will have an adjusted *p* value below a'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Results table with IHW-adjusted p-values and metadata containing ihwResult object: 'resIHW <- results(dds, filterFun=ihw); metadata(resIHW)$ihwResult'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Summary statistics comparing gene counts retained after standard filtering vs. IHW filtering: 'summary(res); sum(res$padj < 0.1, na.rm=TRUE); summary(resIHW); sum(resIHW$padj < 0.1, na.rm=TRUE)'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] DESeq2: 'The package DESeq2 provides methods to test for differential expression by use of negative binomial generalized linear models'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] IHW: 'A Bioconductor package, [IHW](http://bioconductor.org/packages/IHW), is available that implements the method of *Independent Hypothesis Weighting*'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog found.: 'No changelog found.'
