### `paper.md`
```
# GreenleafLab__chromVAR

## Introduction

---
[![Build Status](https://travis-ci.org/GreenleafLab/chromVAR.svg?branch=master)](https://travis-ci.org/GreenleafLab/chromVAR)

# chromVAR

chromVAR is an R package for the analysis of sparse chromatin accessibility data from single cell or bulk ATAC or DNAse-seq data. The package aims to identify motifs or other genomic annotations associated with variability in chromatin accessibility between individual cells or samples.  For a more detail overview of the method, please see the [publication](https://www.nature.com/nmeth/journal/vaop/ncurrent/full/nmeth.4401.html) ([pdf](http://greenleaf.stanford.edu/assets/pdf/nmeth.4401.pdf), [supplement](https://drive.google.com/file/d/0B8eUn6ZURmqvUjBCbE5Hc0p4UFU/view?usp=sharing)). 

For a paper evaluating chromVAR and other methods as a method for enabling clustering of single cells, see [the preprint from Huidong Chen et al](https://www.biorxiv.org/content/10.1101/739011v1). Using kmers + PCA appears to be the best variant of chromVAR for clustering, but newer methods such as [SnapATAC](https://github.com/r3fang/SnapATAC) outperform chromVAR for the clustering tasks evaluated in the paper. chromVAR may be complementary to some other methods, as a way of annotating TF motif usage in cells & clusters rather than cluster identification or embedding.


## Methods

---
output: rmarkdown::html_vignette
vignette: >
  %\VignetteIndexEntry{Annotations}
  %\VignetteEngine{knitr::rmarkdown}
  %\VignetteEncoding{UTF-8}
---

# Annotations

The main `computeDeviations` function from chromVAR requires an object storing what peaks overlap what motifs or other annotations.  The package includes functions for creating such an object from a set of motifs or kmers, or for converting an existing matrix, data.frame, list, GenomicRangesList, or list of bed files of annotations into the appropriate object.

```{r, message = FALSE}
library(chromVAR)
library(motifmatchr)
library(SummarizedExperiment)
libr
…[truncated]
```
