### `figures/icobra.png`
_binary file, 253835 bytes_

### `paper.md`
```
# thelovelab__DESeq2

## Introduction

> Synthesized from a repository with no top-level README.

## Methods

---
title: "Analyzing RNA-seq data with DESeq2"
author: "Michael I. Love, Simon Anders, and Wolfgang Huber"
date: "`r format(Sys.Date(), '%m/%d/%Y')`"
abstract: >
  A basic task in the analysis of count data from RNA-seq is the
  detection of differentially expressed genes. The count data are
  presented as a table which reports, for each sample, the number of
  sequence fragments that have been assigned to each gene. Analogous
  data also arise for other assay types, including comparative ChIP-Seq,
  HiC, shRNA screening, and mass spectrometry.  An important analysis
  question is the quantification and statistical inference of systematic
  changes between conditions, as compared to within-condition
  variability. The package DESeq2 provides methods to test for
  differential expression by use of negative binomial generalized linear
  models; the estimates of dispersion and logarithmic fold changes
  incorporate data-driven prior distributions. This vignette explains the
  use of the package and demonstrates typical workflows.
  [An RNA-seq workflow](http://www.bioconductor.org/help/workflows/rnaseqGene/)
  on the Bioconductor website covers similar material to this vignette
  but at a slower pace, including the generation of count matrices from
  FASTQ files.
  DESeq2 package version: `r packageVersion("DESeq2")`
output:
  rmarkdown::html_document:
    highlight: pygments
    toc: true
    fig_width: 5
bibliography: library.bib
vignette: >
  %\VignetteIndexEntry{Analyzing RNA-seq data with DESeq2}
  %\VignetteEngine{knitr::rmarkdown}
  %\VignetteEncoding{UTF-8}
  %\usepackage[utf8]{inputenc}
---

```{r setup, echo=FALSE, results="hide"}
knitr::opts_chunk$set(tidy = FALSE,
                      cache = FALSE,
                      dev = "png",
                      message = FALSE, error = FALSE, warning = TRUE)
```	

# Standard workflow

**Note:** if you u
…[truncated]
```
