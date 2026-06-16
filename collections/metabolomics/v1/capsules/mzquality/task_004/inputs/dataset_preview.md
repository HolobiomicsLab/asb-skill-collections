### `figures/Rplot001.jpg`
_binary file, 4227 bytes_

### `paper.md`
```
# hankemeierlab__mzQuality

## Introduction

# mzQuality

[![R-CMD-check](https://github.com/hankemeierlab/mzQuality/actions/workflows/R-CMD-check.yaml/badge.svg)](https://github.com/hankemeierlab/mzQuality/actions/workflows/R-CMD-check.yaml) [![BiocCheck](https://github.com/hankemeierlab/mzQuality/workflows/R-CMD-check-bioc/badge.svg)](https://github.com/hankemeierlab/mzQuality/actions/workflows/bioc-check.yml) [![Codecov test coverage](https://codecov.io/gh/hankemeierlab/mzQuality/graph/badge.svg)](https://app.codecov.io/gh/hankemeierlab/mzQuality)

mzQuality is a user-friendly R package for quality control of metabolomics 
studies. It features outlier detection, batch-correction using pooled study 
quality control samples (SQC), filters for removing unreliable compounds, 
various plots for inspecting, and generating reports for further processing. 
See our [preprint](https://www.biorxiv.org/content/10.1101/2025.01.22.633547v1) 
for more information.

This R package forms the backbone of our interactive Shiny dashboard application 
_mzQualityDashboard_, which is recommended for interactive use. The dashboard
is also (strongly) recommended if you are a new R user. To install and use 
the dashboard, see the [mzQualityDashboard repository](https://github.com/hankemeierlab/mzQualityDashboard)
for instructions on how to proceed.

# Installing mzQuality

To install mzQuality and all needed dependencies, you can run the following script.
Installation should be fully automatic, but it might be necessary to provide
permission 

## Methods

---
title: "Data Input"
author:
- name: Pascal Maas
  affiliation: Metabolomics Analytical Centre, Leiden, The Netherlands
date: "`r Sys.Date()`"
output: html_document
package: mzQuality
vignette: >
    %\VignetteIndexEntry{Data Input}
    %\VignetteEngine{knitr::rmarkdown}
    %\VignetteEncoding{UTF-8}
---

```{r setup, include=FALSE, message=FALSE}
knitr::opts_chunk$set(echo = TRUE)
library(mzQuality)
```

## Reading data

mzQuality re
…[truncated]
```
