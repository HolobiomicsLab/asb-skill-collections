### `figures/geseca-spatial-top.png`
_binary file, 595539 bytes_

### `figures/geseca-vignette-score-toy-example.png`
_binary file, 18954 bytes_

### `paper.md`
```
# alserglab__fgsea

## Introduction

[![R-CMD-check](https://github.com/ctlab/fgsea/actions/workflows/R-CMD-check.yaml/badge.svg)](https://github.com/ctlab/fgsea/actions/workflows/R-CMD-check.yaml)

# fgsea 

`fgsea` is an R-package for fast preranked gene set enrichment analysis (GSEA). This package allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets. P-value estimation is based on an adaptive multi-level split Monte-Carlo scheme. 
See [the preprint](https://www.biorxiv.org/content/10.1101/060012v3) for algorithmic details.

Full vignette can be found here: http://bioconductor.org/packages/devel/bioc/vignettes/fgsea/inst/doc/fgsea-tutorial.html


## Methods

---
title: "Using fgsea package"
output: rmarkdown::html_vignette
vignette: >
  %\VignetteIndexEntry{Using fgsea package}
  %\VignetteEngine{knitr::rmarkdown}
  %\VignetteEncoding{UTF-8}
---

`fgsea` is an R-package for fast preranked gene set enrichment analysis (GSEA). 
This package allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets.
P-value estimation is based on an adaptive multi-level split Monte-Carlo scheme. See the [preprint](https://www.biorxiv.org/content/10.1101/060012v2) for algorithmic details. 

## Loading necessary libraries

```{r message=FALSE}
library(fgsea)
library(data.table)
library(ggplot2)
```

```{r echo=FALSE}
library(BiocParallel)
register(SerialParam())
```

## Quick run

Loading example pathways and gene-level statistics and setting random seed:
```{r}
data(examplePathways)
data(exampleRanks)
set.seed(42)
```

Running fgsea:
```{r}
fgseaRes <- fgsea(pathways = examplePathways, 
                  stats    = exampleRanks,
                  minSize  = 15,
                  maxSize  = 500)
```

The resulting table contains enrichment scores and p-values:
```{r}
head(fgseaRes[order(pval), ])
```

As you can see from the warning, `fgsea` has a default lower bound `eps=1e-10` for estimatin
…[truncated]
```
