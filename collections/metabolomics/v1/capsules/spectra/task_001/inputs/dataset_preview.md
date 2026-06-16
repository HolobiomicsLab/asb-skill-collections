### `figures/apple-touch-icon-120x120.png`
_binary file, 16229 bytes_

### `figures/apple-touch-icon-152x152.png`
_binary file, 22865 bytes_

### `figures/apple-touch-icon-180x180.png`
_binary file, 29301 bytes_

### `figures/apple-touch-icon-60x60.png`
_binary file, 6014 bytes_

### `figures/apple-touch-icon-76x76.png`
_binary file, 8298 bytes_

### `figures/apple-touch-icon.png`
_binary file, 29301 bytes_

### `figures/favicon-16x16.png`
_binary file, 1340 bytes_

### `figures/favicon-32x32.png`
_binary file, 2774 bytes_

### `figures/logo.png`
_binary file, 174445 bytes_

### `figures/plot-single-spectrum-basic.svg`
_binary file, 6075 bytes_

### `figures/plot-single-spectrum-labels-ass.svg`
_binary file, 7859 bytes_

### `figures/plot-single-spectrum-labels.svg`
_binary file, 7416 bytes_

### `figures/plot-single-spectrum-xlim.svg`
_binary file, 5762 bytes_

### `figures/plotmzdelta-1000.svg`
_binary file, 29179 bytes_

### `figures/plotspectra-asp05.svg`
_binary file, 10578 bytes_

### `figures/plotspectra-asp2.svg`
_binary file, 11521 bytes_

### `figures/plotspectra-color-each.svg`
_binary file, 10380 bytes_

### `figures/plotspectra-color-peaks-label-labelcol.svg`
_binary file, 12898 bytes_

### `figures/plotspectra-color-peaks-label.svg`
_binary file, 13078 bytes_

### `paper.md`
```
# rformassspectrometry__Spectra

## Introduction

# Low level infrastructure to handle MS spectra

[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![R-CMD-check-bioc](https://github.com/RforMassSpectrometry/Spectra/workflows/R-CMD-check-bioc/badge.svg)](https://github.com/RforMassSpectrometry/Spectra/actions?query=workflow%3AR-CMD-check-bioc)
[![codecov](https://codecov.io/gh/rformassspectrometry/Spectra/branch/main/graph/badge.svg?token=jy0Mid9gKn)](https://codecov.io/gh/rformassspectrometry/Spectra)
[![license](https://img.shields.io/badge/license-Artistic--2.0-brightgreen.svg)](https://opensource.org/licenses/Artistic-2.0)
[![years in bioc](http://bioconductor.org/shields/years-in-bioc/Spectra.svg)](https://bioconductor.org/packages/release/bioc/html/Spectra.html)
[![Ranking by downloads](http://bioconductor.org/shields/downloads/release/Spectra.svg)](https://bioconductor.org/packages/stats/bioc/Spectra/)
[![build release](http://bioconductor.org/shields/build/release/bioc/Spectra.svg)](https://bioconductor.org/checkResults/release/bioc-LATEST/Spectra/)
[![build devel](http://bioconductor.org/shields/build/devel/bioc/Spectra.svg)](https://bioconductor.org/checkResults/devel/bioc-LATEST/Spectra/)

The *Spectra* package defines an efficient infrastructure for storing and
handling mass spectrometry spectra and functionality to subset, process,
visualize and compare spectra da

## Methods

---
title: "Creating new `MsBackend` classes"
output:
    BiocStyle::html_document:
        toc_float: true
vignette: >
    %\VignetteIndexEntry{Creating new `MsBackend` class}
    %\VignetteEngine{knitr::rmarkdown}
    %\VignetteEncoding{UTF-8}
    %\VignettePackage{Spectra}
    %\VignetteDepends{Spectra,BiocStyle}
bibliography: references.bib
---

```{r style, echo = FALSE, results = 'asis', message=FALSE}
BiocStyle::markdown()
``
…[truncated]
```
