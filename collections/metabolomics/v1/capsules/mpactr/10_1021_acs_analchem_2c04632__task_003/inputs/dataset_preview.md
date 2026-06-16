### `figures/apple-touch-icon.png`
_binary file, 49700 bytes_

### `figures/expected_treemap.png`
_binary file, 84368 bytes_

### `figures/favicon-96x96.png`
_binary file, 15784 bytes_

### `figures/favicon.svg`
_binary file, 148569 bytes_

### `figures/logo.png`
_binary file, 111124 bytes_

### `figures/web-app-manifest-192x192.png`
_binary file, 56331 bytes_

### `figures/web-app-manifest-512x512.png`
_binary file, 349006 bytes_

### `paper.md`
```
# mums2__mpactr

## Introduction


# mpactr <a href="https://www.mums2.org/mpactr/"><img src="man/figures/logo.png" align="right" height="138" alt="mpactr website" /></a>

<!-- README.md is generated from README.Rmd. Please edit that file -->

<!-- badges: start -->

[![R-CMD-check](https://github.com/mums2/mpactr/actions/workflows/r.yml/badge.svg)](https://github.com/mums2/mpactr/actions/workflows/r.yml)
[![test-coverage](https://github.com/mums2/mpactr/actions/workflows/test-coverage.yml/badge.svg)](https://github.com/mums2/mpactr/actions/workflows/test-coverage.yml)
[![lint](https://github.com/mums2/mpactr/actions/workflows/lintr.yml/badge.svg)](https://github.com/mums2/mpactr/actions/workflows/lintr.yml)
[![pkgdown](https://github.com/mums2/mpactr/actions/workflows/pkgdown.yaml/badge.svg)](https://github.com/mums2/mpactr/actions/workflows/pkgdown.yaml)
<!-- badges: end -->


## Methods

---
title: "Downstream Analyses"
output: rmarkdown::html_vignette
vignette: >
  %\VignetteIndexEntry{Downstream Analyses}
  %\VignetteEngine{knitr::rmarkdown}
  %\VignetteEncoding{UTF-8}
---

```{r, include = FALSE}
knitr::opts_chunk$set(
  collapse = TRUE,
  comment = "#>"
)
```

The goal of mpactr is to correct for errors that occur during the pre-processing of raw tandem MS/MS data. This data needs to be filtered prior to downstream analyses because of limitations in mass spectrometry detection capabilities. Once filtering is complete, you should have a feature table containing high quality MS1 features. This table can be used for a variety of analyses that can be conducted in R to better understand if and how samples differ from one another. 

In this article, we will highlight just a few analyses. This is not an exhaustive list, and there are certainly other ways to conduct the analyses shown below - the beauty of R! We will walk you through how to do the following:

- creating an interactive plot of input features and the filters they failed, if any, using `ggplot` and `plo
…[truncated]
```
