### `figures/CNAimage.jpg`
_binary file, 115334 bytes_

### `figures/CNAtext.jpg`
_binary file, 40007 bytes_

### `figures/DMR.jpg`
_binary file, 216207 bytes_

### `figures/DMRdistributionplot.png`
_binary file, 96616 bytes_

### `figures/DMRoutput.jpg`
_binary file, 281859 bytes_

### `figures/MVP1.jpg`
_binary file, 66284 bytes_

### `figures/MVP2.jpg`
_binary file, 123764 bytes_

### `figures/MVP3.jpg`
_binary file, 29972 bytes_

### `figures/checkBMIQ.jpg`
_binary file, 49419 bytes_

### `figures/densityPlot.jpg`
_binary file, 49023 bytes_

### `figures/failedProbes.jpg`
_binary file, 51002 bytes_

### `figures/lasso.jpg`
_binary file, 57344 bytes_

### `figures/logo4.jpg`
_binary file, 9490 bytes_

### `figures/mdsPlot.jpg`
_binary file, 38494 bytes_

### `figures/probeFeatures.jpg`
_binary file, 187423 bytes_

### `figures/radius.jpg`
_binary file, 145123 bytes_

### `figures/rawSampleCluster.jpg`
_binary file, 19369 bytes_

### `figures/sampleSheetexample.jpg`
_binary file, 97726 bytes_

### `figures/studyInfo.jpg`
_binary file, 55771 bytes_

### `figures/studyInfo.png`
_binary file, 27237 bytes_

### `paper.md`
```
# YuanTian1991__ChAMP

## Introduction

# ChAMP Package for DNA methylation analysis

> Note that this is NOT a proper release version ChAMP and under intensive modification and upgrade, the formally released one is on [Bioconductor](https://www.bioconductor.org/packages/release/bioc/html/ChAMP.html).

ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading, to final gene set enrichment analysis .e.g.

More information could be find in [Bioconductor page](https://bioconductor.org/packages/release/bioc/html/ChAMP.html). Also we provided a more detailed guide in the [HTML vignette](https://bioconductor.org/packages/release/bioc/vignettes/ChAMP/inst/doc/ChAMP.html).

Currently, ChAMP package is maintained by [YuanTian1991](https://github.com/YuanTian1991), if you met any problem during using the software, please email: champ450K@gmail.com

Install Code:

```
git clone https://github.com/YuanTian1991/ChAMP.git
R CMD INSTALL ChAMP
```


Current latest version: `2.29.1`, which support EPICv2, but it must be used along with [ChAMPdata >= 2.23.1](https://github.com/YuanTian1991/ChAMPdata)


## Methods

---
title: "The Chip Analysis Methylation Pipeline"
author: Yuan Tian, Tiffany J Morris, Amy P Webster, Zhen Yang, Stephan Beck, Andrew Feber, and Andrew E Teschendorff <br>
date: "`r Sys.Date()`"
csl: academic-medicine.csl
bibliography: ChAMP.bib
output:
  prettydoc::html_pretty:
    toc: true
    number_sections: true
    theme: architect
    highlight: vignette
runtime: shiny
vignette: >
  %\VignetteEngine{knitr::rmarkdown}
  %\VignetteIndexEntry{ChAMP: The Chip Analysis Methylation Pipeline}
---

> **[ChAMP paper](https://academic.oup.com/bioinformatics/article/doi/10.1093/bioinformatics/btx513/4082274/ChAMP-Updated-Methylation-Analysis-Pipeline-for) has been published on Bioconductor! As author of ChAMP, we really appriciate all your help and suggestions, in the future, I will continually make this package better and bett
…[truncated]
```
