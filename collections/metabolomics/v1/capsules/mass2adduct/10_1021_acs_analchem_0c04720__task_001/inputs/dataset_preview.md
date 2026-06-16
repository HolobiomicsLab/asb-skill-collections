### `paper.md`
```
# kbseah__mass2adduct

## Introduction

# mass2adduct - Finding molecular adducts in mass spectrometry data

In mass spectrometry imaging, adducts can form between target molecules (e.g. metabolites) and other substances such as matrix or salt ions. This package presents tools for counting and identifying possible adducts in MS data, and accompanies Janda et al. (2021).

Read [the paper here](https://doi.org/10.1021/acs.analchem.0c04720).


## Methods

---
title: "Exploring molecular adducts in MSI with mass2adduct"
author: "Brandon Seah"
date: "`r Sys.Date()`"
output: rmarkdown::html_vignette
vignette: >
  %\VignetteIndexEntry{mass2adduct}
  %\VignetteEngine{knitr::rmarkdown}
  %\VignetteEncoding{UTF-8}
---

```{r setup, include = FALSE}
knitr::opts_chunk$set(
  collapse = TRUE,
  comment = "#>"
)
```

## Background: Molecular adducts in mass spectrometry imaging

This package presents tools for counting and identifying possible adducts in MS data, and accompanies Janda et al. (in prep.). In mass spectrometry imaging (MSI), adducts can form between target molecules (e.g. metabolites) and other substances such as matrix or salt ions.

### Terminology

Each peak in a mass spectrum represents ions of a given mass/charge ratio (m/z) that have been detected by the instrument. In this documentation, we use the term *mass peak* (in short: mass or peak) to refer to both the ions themselves and to their nominal m/z values.[^1]

Two ions may differ chemically from each other by a certain chemical moiety, e.g. the gain/loss of a H2O molecule. This may represent two different metabolic compounds naturally present in the sample (e.g. sucrose vs. glucose, which differ from each other by a fructose unit). They may also represent changes that occur during the processing of a sample for MSI, or during the ionization process itself. We use the term *chemical transformation* to refer agnostically to the chemical difference between two ions. We coin the abbreviation *massdiff* for "ma
…[truncated]
```
