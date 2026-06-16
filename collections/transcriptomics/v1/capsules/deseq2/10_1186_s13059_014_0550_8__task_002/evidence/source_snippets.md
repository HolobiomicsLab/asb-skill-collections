# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] How do the three shrinkage estimators (apeglm, normal, ashr) in lfcShrink() differ in their shrunken log fold change estimates for the airway dataset treated-vs-untreated contrast?: 'Shrink log fold changes  [section=other; evidence='res <- lfcShrink(dds, coef="condition_trt_vs_untrt", type="apeglm")']'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] lfcShrink() can be applied with three different shrinkage estimator types (apeglm, normal, ashr) to produce shrunken log fold change estimates from DESeq2 results objects.: 'res <- lfcShrink(dds, coef="condition_trt_vs_untrt", type="apeglm")'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] airway SummarizedExperiment dataset: 'library("airway") data("airway") se <- airway'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] DESeqDataSet object after DESeq() analysis: 'dds <- DESeq(dds)'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Shrunken LFC results table from apeglm estimator: 'resLFC <- lfcShrink(dds, coef="condition_treated_vs_untreated", type="apeglm")'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Shrunken LFC results table from normal estimator: 'resNorm <- lfcShrink(dds, coef=2, type="normal")'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Shrunken LFC results table from ashr estimator: 'resAsh <- lfcShrink(dds, coef=2, type="ashr")'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Comparative MA-plots for three shrinkage estimators: 'plotMA(resLFC, xlim=xlim, ylim=ylim, main="apeglm") plotMA(resNorm, xlim=xlim, ylim=ylim, main="normal") plotMA(resAsh, xlim=xlim, ylim=ylim, main="ashr")'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] DESeq2: 'The package DESeq2 provides methods to test for differential expression by use of negative binomial generalized linear models'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog or version history provided for the DESeq2 source repository: '_No changelog found._'
