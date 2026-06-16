### `figures/MetaboAnnotatoR.jpeg`
_binary file, 106728 bytes_

### `paper.md`
```
# gggraca__MetaboAnnotatoR

## Introduction

# MetaboAnnotatoR


## Methods

---
title: "Introduction to MetaboAnnotatoR"
author: "Gonçalo Graça"
date: "`r Sys.Date()`"
output:
  BiocStyle::html_document:
    toc: true
    toc_float: true
    number_sections: true
vignette: >
  %\VignetteIndexEntry{Introduction to MetaboAnnotatoR}
  %\VignetteEngine{knitr::rmarkdown}
  %\VignetteEncoding{UTF-8}
---

```{r doc_options, include = FALSE}
knitr::opts_chunk$set(
    collapse = TRUE,
    comment = "#>"
)
```

# Introduction

MetaboAnnotatoR is designed to perform metabolite annotation of features from
LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases.
It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode.

# Installation

To install this package, start R (version "4.5.0" or higher) and enter:
```{r installation, eval=FALSE, echo=TRUE, message=FALSE}
if (!require("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

BiocManager::install("MetaboAnnotatoR")
```


# Example session

An example of feature annotation using LC-MS AIF chromatograms processed 
using xcms and RamClustR packages is illustrated here.
The details of how the example dataset was obtained check MetaboAnnotatoR
original paper for the full details: 
https://pubs.acs.org/doi/10.1021/acs.analchem.1c03032.

For more details on RAMClustR object, check the original publication:
https://pubs.acs.org/doi/10.1021/ac501530d.  

Firstly load library and dependencies:

```{r load_package, eval=TRUE, echo=TRUE, message=FALSE}
library(MetaboAnnotatoR)
```

## Feature table and data

As an input, MetaboAnnotatoR requires a data frame containing the features to
be annotated and either a raw AIF LC-MS chromatogram (as .mzML or CDF) or a 
processed dataset composed of two objects: 
RAMClustR (object containing the pseudo-MS/MS spectra) and 
an XCMS object containing the peak-picked data. 
Additionally, the fragment libraries need to be specified.

Firstly a data
…[truncated]
```
