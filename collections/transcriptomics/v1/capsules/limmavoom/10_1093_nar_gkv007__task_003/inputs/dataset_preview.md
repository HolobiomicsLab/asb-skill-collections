### `paper.md`
```
# bioc__limma

## Introduction

> Synthesized from a repository with no top-level README.

## Methods

---
title: A brief introduction to limma
date: "23 October 2004 (last revised 19 May 2026)"
output:
  BiocStyle::html_document:
    toc: FALSE
    number_sections: FALSE
vignette: >
  %\VignetteIndexEntry{A brief introduction to limma}
  %\VignetteEngine{knitr::rmarkdown}
  %\VignetteEncoding{UTF-8}
---

```{r, include = FALSE}
knitr::opts_chunk$set(
  prompt = TRUE,
  comment = NA
)
```

# What is it?

Limma is an R package for the analysis of gene expression data, especially the use of linear models for analysing designed experiments and the assessment of differential expression.
Limma provides the ability to analyse comparisons between many RNA targets simultaneously in arbitrary complicated designed experiments.
Empirical Bayesian methods are used to provide stable results even when the number of arrays is small.
The normalization and background correction functions are provided for microarrays and similar technologies.
The linear model and differential expression functions apply to a wide variety of gene expression technologies including microarrays (single-channel or two-color), quantitative PCR, RNA-seq or proteomics.

# How to get help

The edgeR User's Guide is available by
```{r, eval=FALSE, echo=TRUE}
library(limma)
limmaRUsersGuide()
```
or alternatively from the [limma landing page](https://bioconductor.org/packages/limma).

Documentation for specific functions is available through the usual R help system, e.g., `?lmFit`.
Further questions about the package should be directed to the [Bioconductor support site](https://support.bioconductor.org).

# Further reading

Ritchie ME, Phipson B, Wu D, Hu Y, Law CW, Shi W, Smyth GK (2015). limma powers differential expression analyses for RNA-sequencing and microarray studies. *Nucleic Acids Research* 43, e47. [doi:10.1093/nar/gkv007](https://doi.org/10.1093/nar/gkv007)

Phipson B, Lee S, Majewski IJ, Alexander 
…[truncated]
```
