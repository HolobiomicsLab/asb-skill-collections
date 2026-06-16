### `figures/Component_131.png`
_binary file, 7311 bytes_

### `figures/Component_14.png`
_binary file, 6338 bytes_

### `figures/Component_15.png`
_binary file, 6953 bytes_

### `figures/Component_1576.png`
_binary file, 7482 bytes_

### `figures/Component_1577.png`
_binary file, 6767 bytes_

### `figures/Component_1578.png`
_binary file, 6999 bytes_

### `figures/Component_1583.png`
_binary file, 7294 bytes_

### `figures/Component_17.png`
_binary file, 6046 bytes_

### `figures/Component_179.png`
_binary file, 7435 bytes_

### `figures/Component_183.png`
_binary file, 8434 bytes_

### `figures/Component_21.png`
_binary file, 7008 bytes_

### `figures/Component_22.png`
_binary file, 6916 bytes_

### `figures/Component_23.png`
_binary file, 6058 bytes_

### `figures/Component_24.png`
_binary file, 6235 bytes_

### `figures/Component_25.png`
_binary file, 5981 bytes_

### `figures/Component_331.png`
_binary file, 7608 bytes_

### `figures/Component_7.png`
_binary file, 8013 bytes_

### `figures/Component_9.png`
_binary file, 7666 bytes_

### `figures/tardis.png`
_binary file, 133468 bytes_

### `figures/tardis_new.png`
_binary file, 133468 bytes_

### `paper.md`
```
# UGent-LIMET__TARDIS

## Introduction

<!-- badges: start -->
[![R-CMD-check](https://github.com/pablovgd/TARDIS/actions/workflows/R-CMD-check.yaml/badge.svg?branch=devel)](https://github.com/pablovgd/TARDIS/actions/workflows/R-CMD-check.yaml)
<!-- badges: end -->

# TARDIS <img src="man/figures/tardis.png" width="150" height="150" align = right />        

R package for *TArgeted Raw Data Integration In Spectrometry*


## Methods

---
title: "Quick start for targeted peak integration of LC-MS data using TARDIS"
author: "Pablo Vangeenderhuysen"
date: "`r Sys.Date()`"
output: 
  rmarkdown::html_document:
    toc: true
    toc_float: true
vignette: >
  %\VignetteIndexEntry{Quick start for Targeted peak integration of LC-MS data using TARDIS}
  %\VignetteEncoding{UTF-8}
  %\VignetteEngine{knitr::rmarkdown}
editor_options: 
  markdown: 
    wrap: 72
---

```{r "setup", include = FALSE}
knitr::opts_chunk$set(
    collapse = TRUE,
    comment = "#>"
)
```

# Introduction

`TARDIS` offers an easy and straightforward way to automatically
calculate area under the peak, max intensity and various quality metrics
for targeted chemical compounds in LC-MS data. It makes use of an
established retention time correction algorithm from the `xcms` package
and loads MS data as `Spectra` objects so it's easily integrated with
other tools of the *Rformassspectrometry* initiative.

See
[README](https://github.com/pablovgd/T.A.R.D.I.S./blob/main/README.md)
for installation instructions.

This quick start guide will briefly demonstrate the main functionalities
of `TARDIS` using the command line interface. For details on the GUI we 
refer to the `gui_tutorial ` vignette. For more information we refer 
to the publication : https://pubs.acs.org/doi/10.1021/acs.analchem.5c00567.

# File conversion

Input files need to be converted to the .mzML format and have to be centroided.
Polarity filtering is done within `TARDIS`, so no polarity subsetting has to be
performed when converting the files. F
…[truncated]
```
