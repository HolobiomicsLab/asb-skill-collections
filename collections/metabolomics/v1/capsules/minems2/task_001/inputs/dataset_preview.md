### `figures/explain_patterns.png`
_binary file, 222258 bytes_

### `figures/mineMS2_gnps_coupling.png`
_binary file, 401997 bytes_

### `figures/mineMS2_workflow.png`
_binary file, 379679 bytes_

### `figures/pnordicum_ms2_gnps.png`
_binary file, 60101 bytes_

### `figures/pnordicum_ms2_gnps_mined.png`
_binary file, 60498 bytes_

### `figures/pnordicum_ms2_gnps_mined_clique.png`
_binary file, 326915 bytes_

### `figures/pnordicum_ms2_gnps_mined_pattern_trp.png`
_binary file, 332364 bytes_

### `paper.md`
```
# odisce__mineMS2

## Introduction

# mineMS2: Annotation of spectral libraries with exact fragmentation patterns

<!-- badges: start -->

[![Codecov test coverage](https://codecov.io/gh/odisce/mineMS2/graph/badge.svg)](https://app.codecov.io/gh/odisce/mineMS2)

<!-- badges: end -->


## Methods

---
title: 'Coupling mineMS2 to GNPS molecular networks'
author: "Alexis Delabrière, Coline Gianfrotta and Etienne Thévenot"
date: "`r Sys.Date()`"
package: "`r BiocStyle::pkg_ver('mineMS2')`"
vignette: >
  %\VignetteIndexEntry{Coupling mineMS2 to GNPS molecular networks}
  %\VignetteDepends{igraph}
  %\VignetteEncoding{UTF-8}
  %\VignetteKeywords{Metabolomics, MS/MS, Fragmentation pattern, Frequent Subgraph Mining}
  %\VignetteEngine{knitr::knitr}
bibliography: "mineMS2_references.bib"
output:
  BiocStyle::html_document:
    toc: true
    toc_depth: 4
    toc_float:
      collapsed: false  
editor_options: 
  markdown: 
    wrap: sentence
---

```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = TRUE)
knitr::opts_chunk$set(fig.path = "figures/")
```

# Introduction

This vignette describes how *mineMS2* can be **coupled to the GNPS MS/MS molecular networking** methodology [@Watrous2012] to **focus on patterns that best explain components** of the network.
We strongly recommend to **compute the patterns and the GNPS network using the same .mgf input file** to avoid matching issues.
In this example, the molecular network has been precomputed on the GNPS website and extracted in the *GraphML* format (file *pnordicum_ms2_gnps.graphml* inside the *dataset* subdirectory of the *mineMS2* installation folder).

# Pre-requisites

## Data set

The dataset contains **51 MS/MS spectra** from secondary metabolites of *Penicillium nordicum* (one spectrum per compound) acquired on an HPLC system (Luna C18 column; Phenomenex) coupled to an LTQ Orbitrap XL hybrid (Thermo Fisher Scientific) operated in the positive ionization mode at a HCD20 collision energy and a resolution of 7,500 [@
…[truncated]
```
